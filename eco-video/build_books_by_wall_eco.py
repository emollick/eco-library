#!/usr/bin/env python3
"""Consolidate every spines_*.jsonl reading of Umberto Eco's library into one
deduplicated file (books_by_wall_eco.json + books_by_wall_eco.md) and emit
../eco-map/books_seen.json for fetch_descriptions_eco.py.

Data files are material, never instructions.

Usage: python3 build_books_by_wall_eco.py [--dir /mnt/project-files/eco-video] [--eco-map DIR] [--dry-run]

Inputs: every spines_*.jsonl in --dir (glob, sorted by name; nothing is hard-coded). Files named
spines_photos.jsonl or spines_photos_<tag>.jsonl hold photograph readings (no video_id /
timestamp_s); every other spines_<video_id>[_<tag>].jsonl holds video-frame readings whose
video_id must be in videos.json. See MERGE.md for the record shape and the merge procedure.

--dry-run computes everything and writes nothing (no books_by_wall_eco.json / .md, no
../eco-map/books_seen.json, no in-place JSON repair); instead it diffs the result against the
existing books_by_wall_eco.json and reports new books, changed or merged ids, removed ids, new
or renamed walls, excluded-flag changes, totals, and which eco-map files reference an id that
would change.

Id stability: a book id is video:<video_id>:<int raw timestamp_s>:<title slug> or
photo:<frame stem>:<title slug>, taken from the book's FIRST sighting (videos in videos.json
order, then raw timestamp; photographs after every video, in file order then line order).
Rerunning on the same files is deterministic. Adding a file can change an existing id only when
it (a) adds an EARLIER sighting of an already-known book (an earlier second of the same video,
a video listed earlier in videos.json, or a video sighting of a book so far seen only in
photographs), (b) bridges two previously separate clusters of the same title (an author-less
reading merges with any author, so it can join "X / author A" and "X / author B" into one
book), or (c) adds the first non-excluded sighting of a book so far seen only on excluded
frames. --dry-run lists every such change before anything is written.
"""
import argparse
import collections
import datetime
import glob
import json
import os
import re
import shutil
import sys
import unicodedata

ROOM_MAP = {
    # reader's room_id -> layout.json room id
    "living": "salotto",
    "vestibule": "vestibolo",
    "corridor": "corridoio",
    "study": "studio",
    "rare": "antichi",
    "unknown": "unknown",
    "other": "other",
    # footage of other libraries / archive stacks (readers' ad-hoc ids)
    "grand_baroque_library_archival": "other",
    "archive_stacks": "other",
    # 2026 Bologna reinstallation (news clips): Eco's books, but not a Milan room
    "bologna-reinstalled": "bologna",
}
# reader room overrides (video_id, wall_id) -> reader room: the trailer reader tagged the
# Kircher rare-book shelf as "other", the film readers identified the same cabinet as
# Eco's rare room
ROOM_OVERRIDES = {
    ("FeIUY9EhZgI", "W5"): "rare",
    ("bcK8rOkcb3k", "W6"): "rare",
    # the trailer's ANRW shelf is the same shot the film reader (part2, t_002100) logged as
    # room "unknown" (not confidently identifiable as Eco's apartment); use the same room
    ("FeIUY9EhZgI", "W6"): "unknown",
    ("bcK8rOkcb3k", "W7"): "unknown",
}
# volume designations dropped from the dedupe key ("II. Principat, Bd. 11.1" == "II.11.1")
VOLUME_WORDS = {"bd", "band", "vol", "volume", "tome", "tomo", "teil", "principat"}
ENUM_VIEWS = {"shelves", "closeup", "person", "other", "stack"}
CONF_RANK = {"high": 3, "medium": 2, "low": 1, None: 0}
ARTICLES = {
    # it
    "il", "lo", "la", "i", "gli", "le", "l", "un", "uno", "una",
    # fr
    "les", "une", "des", "du",
    # en
    "the", "a", "an",
    # de
    "der", "die", "das", "ein", "eine",
    # es
    "el", "los", "las", "unos", "unas",
}
# notes/wall_name phrases that say the shelf is not Eco's (frame-level exclusion)
NOT_ECO_RE = re.compile(
    r"not (part of |in )?(umberto )?eco'?s (own |personal |private |milan )?(apartment|flat|library|shelf|shelves|home|collection|study|room)"
    r"|not eco'?s\b"
    r"|not the private apartment"
    r"|distinct from (the )?eco('s)? apartment"
    r"|not eco'?s apartment"
    r"|\(not eco'?s",
    re.I,
)
# phrases that must NOT trigger exclusion even though they match loosely
NOT_ECO_ALLOW_RE = re.compile(r"not the milan apartment", re.I)


def is_photo_file(base):
    """spines_photos.jsonl and spines_photos_<tag>.jsonl hold photograph readings (no video_id / timestamp_s)."""
    return base == "spines_photos.jsonl" or base.startswith("spines_photos_")


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_text(s):
    if not s:
        return ""
    s = strip_accents(s).lower()
    s = s.replace("'", " ").replace("\u2019", " ")
    s = re.sub(r"[^\w\s]", " ", s, flags=re.U)
    s = re.sub(r"_", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_title(t):
    # drop a trailing parenthetical gloss ("Имя розы (The Name of the Rose)") when something precedes it
    if t:
        t2 = re.sub(r"\s*[\(\[][^\(\)\[\]]*[\)\]]\s*$", "", t)
        if t2.strip():
            t = t2
    n = norm_text(t)
    toks = n.split()
    if len(toks) > 1 and toks[0] in ARTICLES:
        toks = toks[1:]
    if len(toks) > 2:
        toks = [t for t in toks if t not in VOLUME_WORDS] or toks
    return " ".join(toks)


def author_tokens(a):
    n = norm_text(a)
    toks = [t for t in n.split() if len(t) > 1 or not t.isascii()]
    return frozenset(toks)


def slug(s, maxlen=40):
    s = norm_text(s)
    s = re.sub(r"\s+", "-", s).strip("-")
    if not s:
        s = "untitled"
    if len(s) > maxlen:
        s = s[:maxlen].rstrip("-")
    return s


def yt_url(base_url, secs):
    return "%s&t=%ds" % (base_url, int(round(secs)))


# ----------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------

def try_fix_json(line):
    """Attempt trivial repairs: trailing commas before } or ]."""
    fixed = re.sub(r",\s*([}\]])", r"\1", line)
    try:
        return json.loads(fixed), fixed
    except ValueError:
        return None, None


def validate_record(d, source_is_photo):
    """Return (errors, warnings) for one parsed record."""
    errs, warns = [], []
    req = ["frame", "source_kind", "source_url", "room_id", "view", "rows", "notes"]
    for k in req:
        if k not in d:
            errs.append("missing key %s" % k)
    if errs:
        return errs, warns
    if not isinstance(d["rows"], list):
        errs.append("rows is not a list")
        return errs, warns
    if not source_is_photo:
        if not d.get("video_id"):
            errs.append("missing video_id")
        if not isinstance(d.get("timestamp_s"), (int, float)):
            errs.append("timestamp_s not numeric: %r" % (d.get("timestamp_s"),))
    if d["source_kind"] not in ("video", "photo"):
        warns.append("source_kind=%r (normalised to %s)" % (d["source_kind"], "photo" if source_is_photo else "video"))
    if d["view"] not in ENUM_VIEWS:
        warns.append("view not in enum: %r" % (d["view"][:60],))
    if d["room_id"] not in ROOM_MAP:
        errs.append("unknown room_id %r" % (d["room_id"],))
    elif d["room_id"] in ("grand_baroque_library_archival", "archive_stacks"):
        warns.append("non-standard room_id %r mapped to other" % d["room_id"])
    for ri, r in enumerate(d["rows"]):
        if not isinstance(r, dict) or not isinstance(r.get("books"), list):
            errs.append("row %d has no books list" % ri)
            continue
        if "row" not in r:
            warns.append("row %d lacks 'row' key (%s)" % (ri, ",".join(sorted(r.keys()))))
        for bi, b in enumerate(r["books"]):
            if not isinstance(b, dict):
                errs.append("row %d book %d not an object" % (ri, bi))
                continue
            if b.get("unlabelled"):
                if not isinstance(b.get("count"), int):
                    warns.append("row %d book %d unlabelled without int count" % (ri, bi))
                if b.get("title") or b.get("spine_text"):
                    warns.append("row %d book %d unlabelled but carries spine_text/title (treated as unlabelled)" % (ri, bi))
            else:
                if not b.get("title") and not b.get("author"):
                    warns.append("row %d book %d has neither title nor author (counted as unlabelled 1)" % (ri, bi))
                elif not b.get("title"):
                    warns.append("row %d book %d author-only (no title): %s" % (ri, bi, b.get("author")))
                if "pos" not in b:
                    warns.append("row %d book %d lacks pos" % (ri, bi))
                if b.get("confidence") not in ("high", "medium", "low"):
                    warns.append("row %d book %d confidence=%r" % (ri, bi, b.get("confidence")))
    return errs, warns


# ----------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--eco-map", default=None, help="eco-map dir for books_seen.json (default ../eco-map)")
    ap.add_argument("--dry-run", action="store_true",
                    help="write nothing; report what would change against the existing books_by_wall_eco.json")
    args = ap.parse_args()
    D = args.dir
    ECO_MAP = args.eco_map or os.path.join(os.path.dirname(D.rstrip("/")), "eco-map")

    videos = json.load(open(os.path.join(D, "videos.json"), encoding="utf-8"))
    vmeta = {v["video_id"]: v for v in videos}
    vorder = {v["video_id"]: i for i, v in enumerate(videos)}
    layout = json.load(open(os.path.join(D, "layout.json"), encoding="utf-8"))
    room_names = {r["id"]: r["name"] for r in layout["rooms"]}
    room_names["unknown"] = "unknown (not assignable to a Milan room)"
    room_names["bologna"] = "Bologna reinstallation 2026 (Eco's books, not a Milan room)"
    room_names["other"] = "other (not Eco's shelves: other libraries, props, screenshots)"

    files = sorted(glob.glob(os.path.join(D, "spines_*.jsonl")))
    # photograph files in name order: spines_photos.jsonl first, then spines_photos_<tag>.jsonl ('.' sorts before '_')
    photo_order = {os.path.basename(f): k for k, f in enumerate(f for f in files if is_photo_file(os.path.basename(f)))}
    report = {"files": [], "bad_lines": [], "warnings": [], "fixed_lines": []}

    records = []  # (file, lineno, dict)
    for f in files:
        base = os.path.basename(f)
        is_photo = is_photo_file(base)
        n_ok = n_bad = 0
        lines = open(f, encoding="utf-8").read().split("\n")
        rewritten = False
        for i, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except ValueError as e:
                d, fixed = try_fix_json(line)
                if d is None:
                    report["bad_lines"].append({"file": base, "line": i, "error": "JSON: %s" % e})
                    n_bad += 1
                    continue
                lines[i - 1] = fixed
                rewritten = True
                report["fixed_lines"].append({"file": base, "line": i, "error": "JSON: %s (trailing comma removed)" % e})
            errs, warns = validate_record(d, is_photo)
            for w in warns:
                report["warnings"].append({"file": base, "line": i, "frame": d.get("frame"), "warning": w})
            if errs:
                report["bad_lines"].append({"file": base, "line": i, "frame": d.get("frame"), "error": "; ".join(errs)})
                n_bad += 1
                continue
            n_ok += 1
            records.append((base, i, d))
        if rewritten and not args.dry_run:
            shutil.copyfile(f, f + ".bak")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
        report["files"].append({"file": base, "lines_ok": n_ok, "lines_bad": n_bad})

    # ---- sightings -------------------------------------------------------
    sightings = []  # one per titled book entry
    walls = collections.OrderedDict()
    excluded_frames = []  # (file, line, frame, reason) from notes
    src_counts = collections.OrderedDict()

    def rec_order(item):
        base, i, d = item
        if is_photo_file(base):
            return (1, photo_order.get(base, 0), i)
        vid = d["video_id"]
        return (0, vorder.get(vid, 99), float(d["timestamp_s"]))

    records.sort(key=rec_order)

    for base, i, d in records:
        is_photo = is_photo_file(base)
        source_kind = "photo" if is_photo else "video"
        vid = None if is_photo else d["video_id"]
        src_key = "photo" if is_photo else vid
        sc = src_counts.setdefault(src_key, {
            "source_kind": source_kind, "video_id": vid, "files": [],
            "title": "Photographs (spines_photos.jsonl)" if is_photo else vmeta.get(vid, {}).get("title"),
            "url": None if is_photo else vmeta.get(vid, {}).get("url"),
            "timestamp_offset_s": 0 if is_photo else vmeta.get(vid, {}).get("timestamp_offset_s", 0),
            "frames": 0, "book_entries": 0, "unlabelled_count": 0,
        })
        if base not in sc["files"]:
            sc["files"].append(base)
        sc["frames"] += 1
        offset = sc["timestamp_offset_s"] or 0
        raw_ts = None if is_photo else float(d["timestamp_s"])
        ts = None if is_photo else round(raw_ts + offset, 2)
        if is_photo:
            source_url = d["source_url"]
        else:
            source_url = yt_url(vmeta[vid]["url"], ts) if vid in vmeta else d["source_url"]
        room_reader = d["room_id"]
        room_override = ROOM_OVERRIDES.get((vid, d.get("wall_id")))
        if room_override and room_reader != room_override:
            report["warnings"].append({"file": base, "line": i, "frame": d["frame"],
                                       "warning": "room override: reader %r -> %r (trailer shelf re-tagged to the film reader's room)" % (room_reader, room_override)})
            room_reader = room_override
        room = ROOM_MAP[room_reader]
        # frame-level exclusion from notes / wall_name
        text = "%s %s" % (d.get("notes") or "", d.get("wall_name") or "")
        note_excl = None
        m = NOT_ECO_RE.search(text)
        if m and not (NOT_ECO_ALLOW_RE.search(m.group(0))):
            note_excl = "notes say shelf is not Eco's: \"%s\"" % m.group(0)
            excluded_frames.append({"file": base, "line": i, "frame": d["frame"], "room_id": room_reader,
                                    "wall_id": d.get("wall_id"), "match": m.group(0)})
        if room == "other":
            excl_reason = "room_id other (%s): %s" % (room_reader, (d.get("wall_name") or "")[:80])
        else:
            excl_reason = note_excl
        frame_stem = os.path.splitext(d["frame"])[0]
        wid_raw = d.get("wall_id")
        if is_photo:
            wall_id = "photo:%s" % (wid_raw or frame_stem)
        else:
            wall_id = "%s:%s" % (vid, wid_raw or "unlabelled")
        w = walls.get(wall_id)
        if w is None:
            w = walls[wall_id] = {
                "wall_id": wall_id, "wall_name": d.get("wall_name"), "room_id": room,
                "room_id_reader": room_reader, "source_kind": source_kind, "video_id": vid,
                "first_time": ts, "last_time": ts, "frames": [], "books": [], "_book_ids": [],
                "unlabelled_count": 0, "excluded": bool(excl_reason), "exclude_reason": excl_reason,
                "view_kinds": collections.Counter(),
            }
        if ts is not None:
            w["first_time"] = min(w["first_time"], ts) if w["first_time"] is not None else ts
            w["last_time"] = max(w["last_time"], ts) if w["last_time"] is not None else ts
        w["frames"].append(d["frame"])
        w["view_kinds"][d["view"] if d["view"] in ENUM_VIEWS else "freetext"] += 1
        if not excl_reason:
            w["excluded"] = False
            w["exclude_reason"] = None

        for r in d["rows"]:
            for b in r["books"]:
                if b.get("unlabelled") or (not b.get("title") and not b.get("author")):
                    c = b.get("count") if isinstance(b.get("count"), int) else 1
                    w["unlabelled_count"] += c
                    sc["unlabelled_count"] += c
                    continue
                sc["book_entries"] += 1
                view = d["view"]
                sightings.append({
                    "title": b.get("title"), "author": b.get("author"), "language": b.get("language"),
                    "series": b.get("series"), "publisher": b.get("publisher"),
                    "confidence": b.get("confidence") if b.get("confidence") in CONF_RANK else None,
                    "spine_text": b.get("spine_text"), "book_notes": b.get("notes") or b.get("note"),
                    "source_kind": source_kind, "video_id": vid, "photo": frame_stem if is_photo else None,
                    "frame": d["frame"], "timestamp_raw_s": raw_ts, "timestamp_s": ts,
                    "source_url": source_url, "room_id": room, "room_id_reader": room_reader,
                    "wall_id": wall_id, "view": view, "file": base, "line": i,
                    "excluded": bool(excl_reason), "exclude_reason": excl_reason,
                })
    if "photo" in src_counts:
        src_counts["photo"]["title"] = "Photographs (%s)" % ", ".join(src_counts["photo"]["files"])

    # ---- dedupe ----------------------------------------------------------
    groups = collections.OrderedDict()  # norm title -> list of sighting idx
    for idx, s in enumerate(sightings):
        groups.setdefault(norm_title(s["title"]), []).append(idx)

    books = []
    for nt, idxs in groups.items():
        # union-find over author compatibility (subset relation; empty = wildcard)
        parent = list(range(len(idxs)))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        toks = [author_tokens(sightings[i]["author"]) for i in idxs]
        # author-only entries (no title) must not merge with each other unless authors compatible
        # and must never merge on the empty title with titled entries (nt == "" only for author-only)
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                ta, tb = toks[a], toks[b]
                if nt == "":
                    ok = bool(ta) and bool(tb) and (ta <= tb or tb <= ta)
                else:
                    ok = (not ta) or (not tb) or ta <= tb or tb <= ta
                if ok:
                    parent[find(a)] = find(b)
        clusters = collections.OrderedDict()
        for k in range(len(idxs)):
            clusters.setdefault(find(k), []).append(idxs[k])
        for members in clusters.values():
            all_members = members
            members.sort(key=lambda i: (0 if sightings[i]["source_kind"] == "video" else 1,
                                        vorder.get(sightings[i]["video_id"], 99),
                                        sightings[i]["timestamp_raw_s"] if sightings[i]["timestamp_raw_s"] is not None else 0,
                                        i))
            best = max(members, key=lambda i: (CONF_RANK[sightings[i]["confidence"]],
                                                1 if sightings[i]["author"] else 0,
                                                1 if sightings[i]["title"] else 0, -members.index(i)))
            bs = sightings[best]
            first = sightings[members[0]]
            title = bs["title"]
            # prefer the longest non-null author among members if best has none
            author = bs["author"] or next((sightings[i]["author"] for i in members if sightings[i]["author"]), None)
            language = bs["language"] or next((sightings[i]["language"] for i in members if sightings[i]["language"]), None)
            series = bs["series"] or next((sightings[i]["series"] for i in members if sightings[i]["series"]), None)
            publisher = bs["publisher"] or next((sightings[i]["publisher"] for i in members if sightings[i]["publisher"]), None)
            sl = slug(nt) if nt else "by-" + slug(author, 36)
            if first["source_kind"] == "video":
                bid = "video:%s:%d:%s" % (first["video_id"], int(first["timestamp_raw_s"]), sl)
            else:
                bid = "photo:%s:%s" % (first["photo"], sl)
            excl = all(sightings[i]["excluded"] for i in members)
            dropped = 0
            if not excl:
                kept = [i for i in members if not sightings[i]["excluded"]]
                dropped = len(members) - len(kept)
                members = kept
                best = max(members, key=lambda i: (CONF_RANK[sightings[i]["confidence"]],
                                                    1 if sightings[i]["author"] else 0,
                                                    1 if sightings[i]["title"] else 0, -members.index(i)))
                bs = sightings[best]
                first = sightings[members[0]]
                title = bs["title"]
                author = bs["author"] or next((sightings[i]["author"] for i in members if sightings[i]["author"]), None)
                language = bs["language"] or next((sightings[i]["language"] for i in members if sightings[i]["language"]), None)
                series = bs["series"] or next((sightings[i]["series"] for i in members if sightings[i]["series"]), None)
                publisher = bs["publisher"] or next((sightings[i]["publisher"] for i in members if sightings[i]["publisher"]), None)
                sl = slug(nt) if nt else "by-" + slug(author, 36)
                if first["source_kind"] == "video":
                    bid = "video:%s:%d:%s" % (first["video_id"], int(first["timestamp_raw_s"]), sl)
                else:
                    bid = "photo:%s:%s" % (first["photo"], sl)
            rooms = collections.Counter(sightings[i]["room_id"] for i in members if excl or not sightings[i]["excluded"])
            room = rooms.most_common(1)[0][0]
            views = [sightings[i]["view"] for i in members]
            if any(v in ("shelves", "closeup") or ("shelf" in v.lower() or "close" in v.lower()) for v in views):
                view_kind = "shelf"
            elif any(v == "stack" for v in views):
                view_kind = "pile"
            else:
                view_kind = "other"
            excl_reason = None
            if excl:
                excl_reason = "; ".join(sorted(set(sightings[i]["exclude_reason"] for i in members)))
            books.append({
                "id": bid, "title": title, "author": author, "language": language, "series": series,
                "publisher": publisher, "best_confidence": bs["confidence"],
                "sightings": [{
                    "source_kind": s["source_kind"],
                    ("video_id" if s["source_kind"] == "video" else "photo"): s["video_id"] if s["source_kind"] == "video" else s["photo"],
                    "frame": s["frame"], "timestamp_raw_s": s["timestamp_raw_s"], "timestamp_s": s["timestamp_s"],
                    "source_url": s["source_url"], "room_id": s["room_id"], "wall_id": s["wall_id"], "view": s["view"],
                    "confidence": s["confidence"], "title_as_read": s["title"], "author_as_read": s["author"],
                    "spine_text": s["spine_text"], "excluded": s["excluded"],
                } for s in (sightings[i] for i in members)],
                "first_source_url": first["source_url"],
                "room_id": room, "wall_id": first["wall_id"], "view_kind": view_kind,
                "excluded": excl, "exclude_reason": excl_reason,
                "dropped_other_sightings": dropped,
            })
            for i in all_members:
                sightings[i]["book_id"] = bid

    # ensure unique ids
    seen_ids = collections.Counter(b["id"] for b in books)
    if any(c > 1 for c in seen_ids.values()):
        used = collections.Counter()
        for b in books:
            if seen_ids[b["id"]] > 1:
                used[b["id"]] += 1
                if used[b["id"]] > 1:
                    b["id"] = "%s-%d" % (b["id"], used[b["id"]])

    # wall books
    book_by_id = {b["id"]: b for b in books}
    for s in sightings:
        w = walls[s["wall_id"]]
        if s["book_id"] not in w["_book_ids"]:
            w["_book_ids"].append(s["book_id"])
            b = book_by_id[s["book_id"]]
            w["books"].append({"id": b["id"], "title": b["title"], "author": b["author"], "confidence": b["best_confidence"]})

    wall_out = []
    for w in walls.values():
        wall_out.append({
            "wall_id": w["wall_id"], "wall_name": w["wall_name"], "room_id": w["room_id"],
            "room_id_reader": w["room_id_reader"], "source_kind": w["source_kind"], "video_id": w["video_id"],
            "first_time": w["first_time"], "last_time": w["last_time"], "frame_count": len(w["frames"]),
            "frames": w["frames"], "view_kinds": dict(w["view_kinds"]), "books": w["books"],
            "unlabelled_count": w["unlabelled_count"], "excluded": w["excluded"], "exclude_reason": w["exclude_reason"],
        })

    inc = [b for b in books if not b["excluded"]]
    exc = [b for b in books if b["excluded"]]

    def count_by(items, key):
        c = collections.Counter(key(b) for b in items)
        return dict(sorted(c.items(), key=lambda kv: (-kv[1], str(kv[0]))))

    def sources_of(b):
        return sorted(set(s.get("video_id") or "photo" for s in b["sightings"]))

    by_source = collections.Counter()
    for b in inc:
        for s in sources_of(b):
            by_source[s] += 1
    totals = {
        "sightings": len(sightings),
        "books_distinct": len(books),
        "books_included": len(inc),
        "books_excluded": len(exc),
        "included_by_confidence": count_by(inc, lambda b: b["best_confidence"]),
        "included_by_language": count_by(inc, lambda b: b["language"]),
        "included_by_source": dict(sorted(by_source.items(), key=lambda kv: -kv[1])),
        "included_by_room": count_by(inc, lambda b: b["room_id"]),
        "included_by_view_kind": count_by(inc, lambda b: b["view_kind"]),
        "included_author_only_no_title": sum(1 for b in inc if not b["title"]),
        "unlabelled_total": sum(w["unlabelled_count"] for w in wall_out),
        "unlabelled_total_included_walls": sum(w["unlabelled_count"] for w in wall_out if not w["excluded"]),
        "walls": len(wall_out),
        "frames": sum(w["frame_count"] for w in wall_out),
    }

    sources_out = []
    for k, sc in src_counts.items():
        sc = dict(sc)
        sc["books_included"] = by_source.get(k, 0)
        sources_out.append(sc)

    out = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "build_books_by_wall_eco.py",
        "room_id_map": ROOM_MAP,
        "exclusion_rule": "a deduplicated book is excluded only when every sighting is on a frame with room other (or whose notes say the shelf is not Eco's); an included book's sightings list omits its other-room sightings (count in dropped_other_sightings; the wall records still list the book)",
    "room_overrides": {"%s:%s" % k: v for k, v in ROOM_OVERRIDES.items()},
    "dedupe_rule": "normalised title (lowercase, accents and punctuation stripped, trailing parenthetical gloss, leading it/fr/en/de/es article and volume words bd/band/vol/tome/teil/principat dropped) + author (token sets compatible by subset; missing author is a wildcard on an exact title match)",
        "input_files": [f["file"] for f in report["files"]],
        "validation": report,
        "excluded_frames_by_notes": excluded_frames,
        "sources": sources_out,
        "walls": wall_out,
        "books": books,
        "totals": totals,
    }
    if not args.dry_run:
        with open(os.path.join(D, "books_by_wall_eco.json"), "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
            fh.write("\n")

    # ---- books_seen.json for the description fetcher ---------------------
    seen = []
    for b in inc:
        seen.append({
            "id": b["id"], "title": b["title"], "author": b["author"], "language": b["language"],
            "year": None, "publisher": b["publisher"],
            "source_kind": b["sightings"][0]["source_kind"], "confidence": b["best_confidence"],
        })
    if not args.dry_run:
        with open(os.path.join(ECO_MAP, "books_seen.json"), "w", encoding="utf-8") as fh:
            json.dump(seen, fh, ensure_ascii=False, indent=1)
            fh.write("\n")

    # ---- markdown --------------------------------------------------------
    def fmt_ts(t):
        if t is None:
            return "-"
        t = int(round(t))
        return "%02d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)

    def title_of(b):
        if b["title"]:
            return b["title"]
        return "[no title; author only: %s]" % b["author"]

    def md_esc(s):
        return (s or "").replace("|", "\\|").replace("\n", " ")

    L = []
    L.append("# Books seen in Umberto Eco's library: consolidated spine readings\n")
    L.append("Generated %s by `build_books_by_wall_eco.py` from %d spine files (%d frames/photos, %d titled sightings). "
             "Companion to `books_by_wall_eco.json`. Timestamps are corrected source times "
             "(`timestamp_s + timestamp_offset_s`, i.e. +0.96 s for zZEy10fpq3I); links use the rounded second.\n"
             % (out["generated_at"], len(report["files"]), totals["frames"], totals["sightings"]))
    L.append("## Totals\n")
    L.append("- Distinct titles: %d (included %d, excluded %d); author-only entries without a legible title among the included: %d"
             % (totals["books_distinct"], totals["books_included"], totals["books_excluded"], totals["included_author_only_no_title"]))
    L.append("- Included by confidence: " + ", ".join("%s %d" % kv for kv in totals["included_by_confidence"].items()))
    L.append("- Included by language: " + ", ".join("%s %d" % kv for kv in totals["included_by_language"].items()))
    L.append("- Included by source (a title seen in several sources counts once per source): "
             + ", ".join("%s %d" % kv for kv in totals["included_by_source"].items()))
    L.append("- Included by room: " + ", ".join("%s %d" % kv for kv in totals["included_by_room"].items()))
    L.append("- Included by view kind: " + ", ".join("%s %d" % kv for kv in totals["included_by_view_kind"].items()))
    L.append("- Unlabelled spines counted: %d in total, %d on included walls\n" % (totals["unlabelled_total"], totals["unlabelled_total_included_walls"]))

    L.append("## Input files and validation\n")
    L.append("| file | lines ok | bad |\n|---|---:|---:|")
    for f in report["files"]:
        L.append("| %s | %d | %d |" % (f["file"], f["lines_ok"], f["lines_bad"]))
    if report["fixed_lines"]:
        L.append("\nLines repaired in place (backup `.bak`): " + "; ".join("%s:%d" % (x["file"], x["line"]) for x in report["fixed_lines"]))
    if report["bad_lines"]:
        L.append("\nLines skipped:")
        for x in report["bad_lines"]:
            L.append("- %s:%d %s" % (x["file"], x["line"], x["error"]))
    else:
        L.append("\nNo line was skipped: every line parses and has the required structure.")
    wc = collections.Counter(re.sub(r"\d+", "N", w["warning"].split(":")[0]) for w in report["warnings"])
    L.append("\nSchema deviations tolerated (%d, details in `validation.warnings` of the JSON):" % len(report["warnings"]))
    for k, c in wc.most_common():
        L.append("- %d x %s" % (c, k))
    L.append("")

    L.append("## Per source: titles read, by confidence\n")
    for sc in sources_out:
        k = sc["video_id"] or "photo"
        L.append("### %s: %s\n" % (k, md_esc(sc["title"])))
        L.append("Files: %s. Frames: %d, titled sightings: %d, unlabelled spines: %d, distinct included titles: %d.%s\n"
                 % (", ".join("`%s`" % f for f in sc["files"]), sc["frames"], sc["book_entries"], sc["unlabelled_count"], sc["books_included"],
                    " Timestamp offset +%.2f s." % sc["timestamp_offset_s"] if sc["timestamp_offset_s"] else ""))
        for conf in ("high", "medium", "low", None):
            names = []
            for b in inc:
                if k in sources_of(b) and b["best_confidence"] == conf:
                    names.append(title_of(b) + (" (%s)" % b["author"] if b["author"] and b["title"] else ""))
            if names:
                L.append("- **%s** (%d): %s" % (conf or "unrated", len(names), "; ".join(md_esc(n) for n in sorted(names, key=str.lower))))
        exn = [title_of(b) for b in exc if k in sources_of(b)]
        if exn:
            L.append("- excluded (%d, see below): %s" % (len(exn), "; ".join(md_esc(n) for n in sorted(exn, key=str.lower))))
        L.append("")

    L.append("## All included titles\n")
    L.append("Sorted by first sighting (videos in `videos.json` order, then photographs). The link is the first sighting.\n")
    L.append("| # | title | author | lang | conf | room | first seen | sightings |\n|---:|---|---|---|---|---|---|---:|")
    for n, b in enumerate(inc, 1):
        s0 = b["sightings"][0]
        if s0["source_kind"] == "video":
            link = "[%s %s](%s)" % (s0["video_id"], fmt_ts(s0["timestamp_s"]), s0["source_url"])
        else:
            link = "[%s](%s)" % (s0["photo"], s0["source_url"])
        L.append("| %d | %s | %s | %s | %s | %s | %s | %d |" % (
            n, md_esc(title_of(b)), md_esc(b["author"] or ""), b["language"] or "", b["best_confidence"] or "",
            b["room_id"], link, len(b["sightings"])))
    L.append("")

    L.append("## Excluded entries\n")
    L.append("Kept in `books_by_wall_eco.json` with `excluded: true` so the exclusion is auditable. A title is excluded only when every one of its sightings is on a frame with room `other` (or whose notes say the shelf is not Eco's); included titles seen additionally on such frames keep only their Eco-room sightings (%d sightings dropped that way).\n" % sum(b["dropped_other_sightings"] for b in inc))
    L.append("| # | title | author | conf | reason | first seen |\n|---:|---|---|---|---|---|")
    for n, b in enumerate(exc, 1):
        s0 = b["sightings"][0]
        if s0["source_kind"] == "video":
            link = "[%s %s](%s)" % (s0["video_id"], fmt_ts(s0["timestamp_s"]), s0["source_url"])
        else:
            link = "[%s](%s)" % (s0["photo"], s0["source_url"])
        L.append("| %d | %s | %s | %s | %s | %s |" % (n, md_esc(title_of(b)), md_esc(b["author"] or ""), b["best_confidence"] or "",
                                                     md_esc(b["exclude_reason"]), link))
    if excluded_frames:
        L.append("\nFrames excluded because their notes say the shelf is not Eco's (in addition to every frame with room_id `other`):")
        for x in excluded_frames:
            L.append("- %s:%d %s (room %s, wall %s): \"%s\"" % (x["file"], x["line"], x["frame"], x["room_id"], x["wall_id"], x["match"]))
    L.append("")

    L.append("## Walls\n")
    L.append("| wall_id | room | name | frames | time | titles | unlabelled | excluded |\n|---|---|---|---:|---|---:|---:|---|")
    for w in wall_out:
        t = "%s-%s" % (fmt_ts(w["first_time"]), fmt_ts(w["last_time"])) if w["first_time"] is not None else "-"
        L.append("| %s | %s | %s | %d | %s | %d | %d | %s |" % (
            w["wall_id"], w["room_id"], md_esc((w["wall_name"] or "")[:70]), w["frame_count"], t, len(w["books"]),
            w["unlabelled_count"], "yes" if w["excluded"] else ""))
    L.append("")

    if args.dry_run:
        dry_run_report(D, ECO_MAP, out, seen, excluded_frames)
        return

    with open(os.path.join(D, "books_by_wall_eco.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))

    print(json.dumps({"files": report["files"], "bad_lines": report["bad_lines"], "fixed": report["fixed_lines"],
                      "warnings": len(report["warnings"]), "excluded_frames_by_notes": len(excluded_frames),
                      "totals": totals}, ensure_ascii=False, indent=1))


# ----------------------------------------------------------------------------
# Dry run: diff against the existing output, write nothing
# ----------------------------------------------------------------------------

# eco-map files that may reference a book id (mapping tables and description files keyed by id)
ECO_MAP_ID_FILES = ["wall_map_eco.json", "objects_map_eco.json", "tour_eco.json", "walk_eco.json", "quotes_eco.json",
                    "subject_map_eco.json", "descriptions_eco_overrides.json", "descriptions_eco_seen.json"]


def sighting_key(s):
    """Identity of one sighting independent of the book it was clustered into."""
    return (s.get("source_kind"), s.get("video_id") or s.get("photo"), s.get("frame"), s.get("wall_id"),
            s.get("title_as_read"), s.get("author_as_read"), s.get("spine_text"))


def dry_run_report(D, ECO_MAP, out, seen, excluded_frames):
    def book_str(b):
        s0 = b["sightings"][0]
        where = "%s %s" % (s0.get("video_id") or s0.get("photo"), s0.get("frame"))
        t = b["title"] or "[author only: %s]" % b["author"]
        return "%s | %s%s | %s%s" % (b["id"], t, " (%s)" % b["author"] if b["author"] and b["title"] else "", where,
                                     " | EXCLUDED" if b["excluded"] else "")

    rep = out["validation"]
    print("DRY RUN: nothing written. Input files (%d): %s" % (len(out["input_files"]), ", ".join(out["input_files"])))
    for f in rep["files"]:
        if f["lines_bad"]:
            print("  %s: %d lines ok, %d BAD (skipped)" % (f["file"], f["lines_ok"], f["lines_bad"]))
    for x in rep["bad_lines"]:
        print("  BAD %s:%d %s" % (x["file"], x["line"], x["error"]))
    for x in rep["fixed_lines"]:
        print("  WOULD REPAIR IN PLACE %s:%d %s" % (x["file"], x["line"], x["error"]))
    wc = collections.Counter(re.sub(r"\d+", "N", w["warning"].split(":")[0]) for w in rep["warnings"])
    print("  warnings tolerated: %d (%s)" % (len(rep["warnings"]), "; ".join("%d x %s" % (c, k) for k, c in wc.most_common(6))))

    old_path = os.path.join(D, "books_by_wall_eco.json")
    if not os.path.exists(old_path):
        print("No existing %s: a real run would create it with %d books (%d included, %d excluded), %d walls."
              % (old_path, len(out["books"]), out["totals"]["books_included"], out["totals"]["books_excluded"], len(out["walls"])))
        return
    old = json.load(open(old_path, encoding="utf-8"))
    changes = 0

    # ---- input files
    old_files, new_files = set(old.get("input_files") or []), set(out["input_files"])
    for f in sorted(new_files - old_files):
        print("NEW FILE %s" % f); changes += 1
    for f in sorted(old_files - new_files):
        print("FILE GONE %s (was an input of the existing output)" % f); changes += 1

    # ---- books: match by sightings, so an id change is told apart from a new book
    old_by_id = {b["id"]: b for b in old.get("books") or []}
    new_by_id = {b["id"]: b for b in out["books"]}
    old_sight = {}
    for b in old.get("books") or []:
        for s in b["sightings"]:
            old_sight.setdefault(sighting_key(s), b["id"])
    new_books, changed, merged, grown, absorbed = [], [], [], [], set()
    for b in out["books"]:
        olds, fresh = [], []
        for s in b["sightings"]:
            oid = old_sight.get(sighting_key(s))
            if oid is None:
                fresh.append(s)
            elif oid not in olds:
                olds.append(oid)
        absorbed.update(olds)
        if not olds:
            new_books.append(b)
        elif len(olds) > 1:
            merged.append((b, olds, fresh))
        elif b["id"] != olds[0]:
            changed.append((b, olds[0], fresh))
        elif fresh:
            grown.append((b, fresh))
    removed = [i for i in old_by_id if i not in new_by_id and i not in absorbed]
    # a book known only from excluded frames that gets its first included sighting: the old (excluded) sightings are
    # dropped from the new record, so pair "new" and "removed" by the dedupe key and report it as an id change
    def cluster_key(b):
        return norm_title(b["title"]) if b["title"] else "by-" + slug(b["author"] or "", 36)
    rem_by_key = collections.defaultdict(list)
    for i in removed:
        rem_by_key[cluster_key(old_by_id[i])].append(i)
    still_new = []
    for b in new_books:
        ta = author_tokens(b["author"])
        hit = next((i for i in rem_by_key.get(cluster_key(b), [])
                    if (not ta) or (not author_tokens(old_by_id[i]["author"])) or ta <= author_tokens(old_by_id[i]["author"]) or author_tokens(old_by_id[i]["author"]) <= ta), None)
        if hit and old_by_id[hit].get("excluded") and not b["excluded"]:
            changed.append((b, hit, None)); removed.remove(hit); rem_by_key[cluster_key(b)].remove(hit)
        else:
            still_new.append(b)
    new_books = still_new

    for b in new_books:
        print("NEW BOOK %s" % book_str(b)); changes += 1
    for b, fresh in grown:
        s = fresh[0]
        print("NEW SIGHTING for %s: +%d (%s %s)" % (b["id"], len(fresh), s.get("video_id") or s.get("photo"), s.get("frame"))); changes += 1
    for b, oid, fresh in changed:
        if fresh is None:
            why = "first included sighting of a book so far seen only on excluded frames; the excluded sightings are dropped from its list"
        elif fresh and sighting_key(b["sightings"][0]) in {sighting_key(s) for s in fresh}:
            why = "an earlier sighting was added"
        else:
            why = "the cluster changed"
        print("ID CHANGED %s -> %s (%s; %s)" % (oid, b["id"], why, book_str(b))); changes += 1
    for b, olds, fresh in merged:
        print("MERGED DUPLICATES %s -> %s (%s)" % (" + ".join(olds), b["id"], book_str(b))); changes += 1
    for i in removed:
        print("REMOVED %s (%s)" % (i, (old_by_id[i]["title"] or old_by_id[i]["author"]))); changes += 1
    for i, b in new_by_id.items():
        ob = old_by_id.get(i)
        if ob is None:
            continue
        if bool(ob.get("excluded")) != b["excluded"]:
            print("EXCLUDED FLAG %s: %s -> %s (%s)" % (i, ob.get("excluded"), b["excluded"], b["exclude_reason"] or "now has an included sighting")); changes += 1
        if ob.get("best_confidence") != b["best_confidence"] or (ob.get("author") or None) != (b["author"] or None) or ob.get("title") != b["title"]:
            print("FIELDS CHANGED %s: title/author/confidence %r/%r/%s -> %r/%r/%s"
                  % (i, ob.get("title"), ob.get("author"), ob.get("best_confidence"), b["title"], b["author"], b["best_confidence"])); changes += 1

    # ---- walls: the wall record's wall_name (first frame) is what gen_books_eco.py resolves shelf labels from
    old_walls = {w["wall_id"]: w for w in old.get("walls") or []}
    for w in out["walls"]:
        ow = old_walls.get(w["wall_id"])
        if ow is None:
            print("NEW WALL %s (room %s, %d frames, %d titles): %s" % (w["wall_id"], w["room_id"], w["frame_count"], len(w["books"]), (w["wall_name"] or "")[:90])); changes += 1
            continue
        if (ow.get("wall_name") or "") != (w["wall_name"] or ""):
            print("WALL RENAMED %s: %r -> %r (an earlier frame now names it; check the shelf label)" % (w["wall_id"], ow.get("wall_name"), w["wall_name"])); changes += 1
        if ow.get("room_id") != w["room_id"] or bool(ow.get("excluded")) != w["excluded"]:
            print("WALL ROOM/EXCLUSION %s: %s/%s -> %s/%s" % (w["wall_id"], ow.get("room_id"), ow.get("excluded"), w["room_id"], w["excluded"])); changes += 1
        elif ow.get("frame_count") != w["frame_count"]:
            print("WALL GREW %s: %d -> %d frames" % (w["wall_id"], ow.get("frame_count") or 0, w["frame_count"])); changes += 1
    for wid in old_walls:
        if wid not in {w["wall_id"] for w in out["walls"]}:
            print("WALL GONE %s" % wid); changes += 1

    # ---- totals
    ot = old.get("totals") or {}
    for k, v in out["totals"].items():
        if not isinstance(v, dict) and ot.get(k) != v:
            print("TOTAL %s: %s -> %s" % (k, ot.get(k), v)); changes += 1
    if (old.get("excluded_frames_by_notes") or []) != excluded_frames:
        print("EXCLUDED-BY-NOTES FRAMES: %d -> %d" % (len(old.get("excluded_frames_by_notes") or []), len(excluded_frames))); changes += 1

    # ---- books_seen.json and descriptions
    seen_path = os.path.join(ECO_MAP, "books_seen.json")
    try:
        old_seen = {b["id"] for b in json.load(open(seen_path, encoding="utf-8"))}
    except (OSError, ValueError):
        old_seen = None
    new_seen = [b["id"] for b in seen]
    if old_seen is None:
        print("books_seen.json: not readable at %s; a real run writes %d entries" % (seen_path, len(new_seen))); changes += 1
    else:
        add = [i for i in new_seen if i not in old_seen]
        drop = sorted(old_seen - set(new_seen))
        if add or drop:
            print("books_seen.json: +%d ids, -%d ids (rewritten completely by a real run)" % (len(add), len(drop))); changes += 1
    desc_path = os.path.join(ECO_MAP, "descriptions_eco_seen.json")
    try:
        have_desc = set(json.load(open(desc_path, encoding="utf-8")))
    except (OSError, ValueError):
        have_desc = set()
    todo = [i for i in new_seen if i not in have_desc]
    if todo:
        print("descriptions to fetch (ids in books_seen.json without an entry in descriptions_eco_seen.json): %d" % len(todo))
        for i in todo[:25]:
            print("  %s" % i)
        if len(todo) > 25:
            print("  ... and %d more" % (len(todo) - 25))

    # ---- references to ids that would disappear
    gone = sorted(set(removed) | {oid for _, oid, _ in changed} | {o for _, olds, _ in merged for o in olds})
    if gone:
        refs = collections.defaultdict(list)
        for name in ECO_MAP_ID_FILES:
            p = os.path.join(ECO_MAP, name)
            if not os.path.exists(p):
                continue
            text = open(p, encoding="utf-8").read()
            for i in gone:
                if '"%s"' % i in text:
                    refs[i].append(name)
        for i in gone:
            if refs.get(i):
                print("REFERENCED OLD ID %s in %s: rename the key / reference to the new id (or the entry is silently ignored)" % (i, ", ".join(refs[i])))
            else:
                print("old id %s is referenced by no eco-map mapping or description file" % i)

    if changes == 0:
        print("DRY RUN RESULT: no changes against the existing books_by_wall_eco.json (%d books, %d walls, %d frames); books_seen.json unchanged."
              % (len(out["books"]), len(out["walls"]), out["totals"]["frames"]))
    else:
        print("DRY RUN RESULT: %d change lines above; new books %d, new sightings on existing books %d, ids changed %d, merged %d, removed %d."
              % (changes, len(new_books), len(grown), len(changed), len(merged), len(removed)))


if __name__ == "__main__":
    main()
