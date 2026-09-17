#!/usr/bin/env python3
"""Assemble videos.json from meta/*.info.json, frames/*/_stats.json and captions/."""
import json, os, glob
R = "/mnt/project-files/eco-video"
ORDER = ["Hq66X9f-zgc","zj1kwT87ne0","B-M8V0PcCrw","iRXEQVTI95k","NtPk4irDiM8","KZfOaug0mM4",
         "FeIUY9EhZgI","bcK8rOkcb3k","ygvl-_gtAP8","M8IWTOFNlOc","rMSOvDAyH5c","zZEy10fpq3I"]
notes = json.load(open(f"{R}/notes.json")) if os.path.exists(f"{R}/notes.json") else {}
# Interval-frame label offset: 11 folders were renamed to true source times (_labels_fixed marker);
# frames/zZEy10fpq3I keeps the raw fps=0.5 slot labels (2k) and must not be renamed (see README).
OFFSET = {"zZEy10fpq3I": 0.96}
OFFSET_NOTE = {"zZEy10fpq3I": ("t_ frame labels and INDEX/KEEP timestamps for this video are slot labels (2k); "
                              "true source time is label + 0.96 s; downstream links should add 1 s")}
out = []
for vid in ORDER:
    rec = {"video_id": vid, "title": None, "uploader": None, "upload_date": None, "duration_s": None,
           "resolution_obtained": None, "url": f"https://www.youtube.com/watch?v={vid}",
           "captions": {"it": None, "en": None}, "frames_total": 0, "frames_kept": 0,
           "timestamp_offset_s": OFFSET.get(vid, 0), "timestamp_note": OFFSET_NOTE.get(vid),
           "notes": notes.get(vid, "")}
    mp = f"{R}/meta/{vid}.info.json"
    if os.path.exists(mp):
        m = json.load(open(mp))
        rec.update(title=m.get("title"), uploader=m.get("uploader") or m.get("channel"),
                   upload_date=m.get("upload_date"), duration_s=m.get("duration"))
        kinds = []
        for lang in ("it", "en"):
            if lang in (m.get("subtitles") or {}): kinds.append(f"{lang}:manual")
            elif lang in (m.get("automatic_captions") or {}): kinds.append(f"{lang}:auto")
        if kinds: rec["notes"] = (rec["notes"] + " " if rec["notes"] else "") + "captions " + ", ".join(kinds) + "."
    for lang in ("it", "en"):
        p = f"captions/{vid}.{lang}.vtt"
        if os.path.exists(f"{R}/{p}"): rec["captions"][lang] = p
    sp = f"{R}/frames/{vid}/_stats.json"
    if os.path.exists(sp):
        s = json.load(open(sp))
        rec.update(resolution_obtained=s["resolution_obtained"], frames_total=s["frames_total"], frames_kept=s["frames_kept"])
        if rec["duration_s"] is None: rec["duration_s"] = round(s["duration_s"])
    out.append(rec)
json.dump(out, open(f"{R}/videos.json", "w"), indent=2, ensure_ascii=False)
print(json.dumps([(r["video_id"], r["resolution_obtained"], r["frames_total"], r["frames_kept"]) for r in out]))
