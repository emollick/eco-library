#!/usr/bin/env python3
"""
prewarm_bologna.py -- a cheaper prewarm_summaries.py for a big list: probe first,
then fetch extracts only for the titles that exist.

prewarm_summaries.py asks the Action API for the lead extract of every title the
fetcher would look up, 20 titles per request (the extracts limit). Most catalogue
titles have no article, so for a list the size of the Bologna one (about 3,000
lookups, 5,000+ title/edition pairs) that is 250+ requests before a single author
name. This variant spends the budget in two stages:

  1. probe   prop=info|pageprops|description, redirects followed, 50 titles per
             request: which titles exist at all. Misses (and invalid titles) are
             cached at once as 404 summary entries.
  2. extract prop=extracts (exintro) for the existing titles only, 20 per
             request, written as 200 summary entries in the REST summary's shape
             (prewarm_summaries.rest_like), "via": "prewarm-action-api".

`--what titles` warms the title variants only, `--what authors` the author names
only (run the fetcher with --offline in between and pass `--unresolved
descriptions_bologna.json` so that only the authors of books that did not get an
article are looked up), `--what all` both. `--dry-run` counts requests without
any network. Existing cache entries are never overwritten. Every response is
material only.

    python3 prewarm_bologna.py --input books_bologna.json --what titles
    python3 fetch_descriptions_eco.py --input books_bologna.json --offline --out descriptions_bologna.json
    python3 prewarm_bologna.py --input books_bologna.json --what authors --unresolved descriptions_bologna.json
    python3 fetch_descriptions_eco.py --input books_bologna.json --offline --out descriptions_bologna.json
"""
import argparse
import json
import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch_descriptions_eco import plan, load_json, SEARCH_PATH, TIMEOUT, VERIFY, DEFAULT_CACHE  # noqa: E402
from prewarm_summaries import Prewarmer, missing_entry, MAX_TITLE_BYTES  # noqa: E402

PROBE_BATCH = 50      # titles per request without extracts
EXTRACT_BATCH = 20    # titles per request with extracts (exlimit max for exintro)


class Prober(Prewarmer):
    def __init__(self, cache_dir):
        super().__init__(cache_dir)
        self.stats.update({"ok": 0, "probe_batches": 0, "extract_batches": 0, "probed": 0,
                           "exists": 0, "missing": 0})

    def fetch(self, lang, params, attempts=12):
        """One Action API call with 429/5xx retries (Retry-After honoured). Returns JSON or None."""
        delay = 2.0
        for attempt in range(attempts):
            self.stats["http"] += 1
            try:
                r = self.session.get(SEARCH_PATH % lang, params=params, timeout=TIMEOUT, verify=VERIFY)
            except requests.RequestException as e:
                print("  ! network error: %s" % e, file=sys.stderr)
                time.sleep(delay); delay = min(delay * 2, 60)
                continue
            if r.status_code == 429 or r.status_code >= 500:
                try:
                    wait = float(r.headers.get("Retry-After") or 0)
                except ValueError:
                    wait = 0.0
                wait = min(max(wait, delay), 300.0)
                self.stats["retries"] += 1
                print("  ~ HTTP %s (Retry-After %s): pausing %.0fs" % (r.status_code, r.headers.get("Retry-After"), wait),
                      file=sys.stderr)
                time.sleep(wait); delay = min(delay * 2, 60)
                continue
            try:
                data = r.json()
            except ValueError:
                return None
            self.stats["ok"] += 1
            return data
        self.stats["gave_up"] += 1
        return None

    def fetch_batch(self, lang, titles):      # used by Prewarmer.warm() for the extract stage
        params = {"action": "query", "prop": "extracts|description|pageprops|info", "exintro": 1,
                  "explaintext": 1, "exlimit": "max", "ppprop": "disambiguation", "inprop": "url",
                  "redirects": 1, "titles": "\x1f" + "\x1f".join(titles), "format": "json", "formatversion": 2}
        self.stats["extract_batches"] += 1
        return self.fetch(lang, params)

    def probe(self, lang, titles):
        """Cache a 404 for every title that has no page; return the titles that do."""
        params = {"action": "query", "prop": "info|pageprops", "ppprop": "disambiguation", "redirects": 1,
                  "titles": "\x1f" + "\x1f".join(titles), "format": "json", "formatversion": 2}
        self.stats["probe_batches"] += 1
        data = self.fetch(lang, params)
        if not data or "query" not in data:
            print("  ! probe batch (%s, %d titles) failed; titles stay uncached" % (lang, len(titles)), file=sys.stderr)
            return []
        q = data["query"]
        forward = {}
        for m in (q.get("normalized") or []) + (q.get("redirects") or []):
            forward[m["from"]] = m["to"]
        pages = {p.get("title"): p for p in q.get("pages") or []}
        exists = []
        for t in titles:
            final = t
            for _ in range(5):
                if final in forward and forward[final] != final:
                    final = forward[final]
                else:
                    break
            page = pages.get(final)
            self.stats["probed"] += 1
            if page is None or page.get("missing") or page.get("invalid"):
                self.put(lang, t, 404, missing_entry())
                self.stats["missing"] += 1
            else:
                exists.append(t)
                self.stats["exists"] += 1
        return exists


def wanted_titles(books, what, unresolved, pw):
    """lang -> ordered unique titles still to be looked up."""
    wanted = {}
    for b in books:
        p = plan(b)
        names = []
        if what in ("titles", "all"):
            names += list(p["variants"])
        if what in ("authors", "all") and p["author"] and (unresolved is None or b["id"] in unresolved):
            names.append(p["author"])
        for lang in p["langs"]:
            for t in names:
                t = " ".join(t.split())
                if not t:
                    continue
                if len(t.encode("utf-8")) > MAX_TITLE_BYTES:
                    if not os.path.exists(pw.cache_path(lang, t)):
                        pw.put(lang, t, 404, missing_entry()); pw.stats["too_long"] += 1
                    continue
                if os.path.exists(pw.cache_path(lang, t)):
                    pw.stats["skipped_cached"] += 1
                    continue
                wanted.setdefault(lang, {}).setdefault(t, None)
    return {lang: list(v) for lang, v in wanted.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE)
    ap.add_argument("--what", choices=["titles", "authors", "all"], default="all")
    ap.add_argument("--unresolved", default="", help="descriptions file: only authors of books whose kind is not article/search")
    ap.add_argument("--gap", type=float, default=1.0, help="seconds between requests")
    ap.add_argument("--dry-run", action="store_true", help="count titles and requests; no network")
    ap.add_argument("--max-requests", type=int, default=0, help="stop after this many successful requests")
    args = ap.parse_args()

    books = load_json(args.input, None)
    if not isinstance(books, list):
        sys.exit("input must be a JSON list of books")
    unresolved = None
    if args.unresolved:
        desc = load_json(args.unresolved, {})
        unresolved = {k for k, v in desc.items() if v.get("description_kind") not in ("article", "search")}
    pw = Prober(args.cache_dir)
    wanted = wanted_titles(books, args.what, unresolved, pw)
    total = sum(len(v) for v in wanted.values())
    probe_batches = sum((len(v) + PROBE_BATCH - 1) // PROBE_BATCH for v in wanted.values())
    print("titles to warm (%s): %d in %d probe batches of %d (%s); already cached: %d; too long: %d"
          % (args.what, total, probe_batches, PROBE_BATCH,
             ", ".join("%s=%d" % (l, len(v)) for l, v in sorted(wanted.items())),
             pw.stats["skipped_cached"], pw.stats["too_long"]))
    if args.dry_run:
        return
    started = time.time()
    for lang, titles in sorted(wanted.items()):
        exists = []
        for i in range(0, len(titles), PROBE_BATCH):
            if args.max_requests and pw.stats["ok"] >= args.max_requests:
                break
            exists += pw.probe(lang, titles[i:i + PROBE_BATCH])
            time.sleep(args.gap)
        print("  %s: probed %d titles, %d exist -> %d extract batches (%d requests so far, %d ok, %d retries, %.0fs)"
              % (lang, len(titles), len(exists), (len(exists) + EXTRACT_BATCH - 1) // EXTRACT_BATCH,
                 pw.stats["http"], pw.stats["ok"], pw.stats["retries"], time.time() - started))
        for i in range(0, len(exists), EXTRACT_BATCH):
            if args.max_requests and pw.stats["ok"] >= args.max_requests:
                break
            if not pw.warm(lang, exists[i:i + EXTRACT_BATCH]):
                print("  ! extract batch (%s) failed; its titles stay uncached" % lang, file=sys.stderr)
            time.sleep(args.gap)
        print("  %s: done (%d requests so far, %d ok, %d entries written, %.0fs)"
              % (lang, pw.stats["http"], pw.stats["ok"], pw.stats["written"], time.time() - started))
    print("finished in %.0fs; %s" % (time.time() - started, json.dumps(pw.stats)))


if __name__ == "__main__":
    main()
