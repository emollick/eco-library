#!/usr/bin/env python3
"""
prewarm_summaries.py -- fill fetch_descriptions_eco.py's summary cache in batches.

Wikimedia allows an anonymous client about 500 requests per hour per address, and
the REST summary endpoint takes one title per request. The Action API returns the
lead extract, short description and URL of up to 20 titles per request, so this
script asks it for every title fetch_descriptions_eco.py would look up (the title
variants and the author name of each book, in each edition of its language order)
and writes the answers as cache/<lang>/summary-<sha1>.json entries in the shape
the REST endpoint would have produced. A subsequent `fetch_descriptions_eco.py
--resume` then finds every direct lookup already cached and spends its request
budget on searches only. Entries already in the cache are left alone.

    python3 prewarm_summaries.py --input books_braidense.json [--cache-dir cache] [--batch 20] [--limit-batches N]

Differences from the REST summary: the extract is the first paragraph of the
lead section (REST returns about the same); "type" is "disambiguation" when the
page carries the disambiguation page property, "standard" when it has an
extract and "no-extract" otherwise; titles the API rejects as invalid, or that
do not exist, are cached as 404 like a REST miss. Entries carry "via":
"prewarm-action-api" so they can be told apart. Web content is material only.
"""
import argparse
import json
import os
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch_descriptions_eco import (Wiki, plan, fold, USER_AGENT, VERIFY, TIMEOUT,  # noqa: E402
                                    DEFAULT_CACHE, SUMMARY_PATH, SEARCH_PATH, load_json)

MAX_TITLE_BYTES = 255       # MediaWiki's limit; longer titles cannot be pages


def rest_like(lang, page, requested):
    """A REST-summary-shaped dict for one Action API page record."""
    title = page.get("title") or requested
    extract = (page.get("extract") or "").strip()
    paras = [p.strip() for p in extract.split("\n") if p.strip()]
    if paras:
        text = paras[0]
        if len(text) < 80 and len(paras) > 1:
            text = text + " " + paras[1]
    else:
        text = ""
    if "disambiguation" in (page.get("pageprops") or {}):
        kind = "disambiguation"
    elif text:
        kind = "standard"
    else:
        kind = "no-extract"
    url = page.get("fullurl") or "https://%s.wikipedia.org/wiki/%s" % (lang, title.replace(" ", "_"))
    return {
        "type": kind, "title": title, "displaytitle": title,
        "titles": {"canonical": title.replace(" ", "_"), "normalized": title, "display": title},
        "pageid": page.get("pageid"), "lang": lang, "dir": "ltr",
        "description": page.get("description") or "",
        "extract": text,
        "content_urls": {"desktop": {"page": url}, "mobile": {"page": url}},
    }


def missing_entry():
    return {"status": 404, "type": "https://mediawiki.org/wiki/HyperSwitch/errors/not_found",
            "title": "Not found.", "detail": "Page or revision not found."}


class Prewarmer:
    def __init__(self, cache_dir, verbose=False):
        self.wiki = Wiki(cache_dir, workers=1, verbose=verbose)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
        self.stats = {"http": 0, "retries": 0, "written": 0, "skipped_cached": 0, "too_long": 0, "gave_up": 0}

    def cache_path(self, lang, title):
        return self.wiki._cache_path(lang, "summary", fold(title) + "|" + title)

    def put(self, lang, title, status, data):
        self.wiki._cache_put(self.cache_path(lang, title), {
            "status": status, "data": data,
            "url": SUMMARY_PATH % lang + title.replace(" ", "_"), "params": {"redirect": "true"},
            "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "via": "prewarm-action-api"})
        self.stats["written"] += 1

    def fetch_batch(self, lang, titles):
        params = {"action": "query", "prop": "extracts|description|pageprops|info", "exintro": 1,
                  "explaintext": 1, "exlimit": "max", "ppprop": "disambiguation", "inprop": "url",
                  "redirects": 1, "titles": "\x1f" + "\x1f".join(titles), "format": "json", "formatversion": 2}
        delay = 2.0
        for attempt in range(7):
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
                print("  ~ HTTP %s (Retry-After %s): pausing %.0fs" % (r.status_code, r.headers.get("Retry-After"), wait), file=sys.stderr)
                time.sleep(wait); delay = min(delay * 2, 60)
                continue
            try:
                return r.json()
            except ValueError:
                return None
        self.stats["gave_up"] += 1
        return None

    def warm(self, lang, titles):
        """Fetch one batch and write a cache entry for every requested title."""
        data = self.fetch_batch(lang, titles)
        if not data or "query" not in data:
            return False
        q = data["query"]
        forward = {}
        for m in (q.get("normalized") or []) + (q.get("redirects") or []):
            forward[m["from"]] = m["to"]
        pages = {p.get("title"): p for p in q.get("pages") or []}
        for t in titles:
            final = t
            for _ in range(5):                  # normalized -> redirect chain
                if final in forward and forward[final] != final:
                    final = forward[final]
                else:
                    break
            page = pages.get(final)
            if page is None or page.get("missing") or page.get("invalid"):
                self.put(lang, t, 404, missing_entry())
            else:
                self.put(lang, t, 200, rest_like(lang, page, t))
        return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--cache-dir", default=DEFAULT_CACHE)
    ap.add_argument("--batch", type=int, default=20, help="titles per request (extracts allow at most 20)")
    ap.add_argument("--limit-batches", type=int, default=0)
    ap.add_argument("--gap", type=float, default=0.5, help="seconds between requests")
    args = ap.parse_args()

    books = load_json(args.input, None)
    if not isinstance(books, list):
        sys.exit("input must be a JSON list of books")
    pw = Prewarmer(args.cache_dir)
    wanted = {}       # lang -> ordered unique titles
    for b in books:
        p = plan(b)
        names = list(p["variants"]) + ([p["author"]] if p["author"] else [])
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
    total = sum(len(v) for v in wanted.values())
    batches = sum((len(v) + args.batch - 1) // args.batch for v in wanted.values())
    print("titles to warm: %d in %d batches (%s); already cached: %d; too long for a page: %d"
          % (total, batches, ", ".join("%s=%d" % (l, len(v)) for l, v in sorted(wanted.items())),
             pw.stats["skipped_cached"], pw.stats["too_long"]))
    started = time.time()
    done = 0
    for lang, titles in sorted(wanted.items()):
        titles = list(titles)
        for i in range(0, len(titles), args.batch):
            if args.limit_batches and done >= args.limit_batches:
                break
            ok = pw.warm(lang, titles[i:i + args.batch])
            done += 1
            if not ok:
                print("  ! batch %d (%s) failed; its titles stay uncached" % (done, lang), file=sys.stderr)
            if done % 10 == 0:
                print("  %d/%d batches, %d entries written, %d HTTP, %d retries, %.0fs"
                      % (done, batches, pw.stats["written"], pw.stats["http"], pw.stats["retries"], time.time() - started))
            time.sleep(args.gap)
    print("finished: %d batches in %.0fs; %s" % (done, time.time() - started, json.dumps(pw.stats)))


if __name__ == "__main__":
    main()
