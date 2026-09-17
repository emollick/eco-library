#!/usr/bin/env python3
"""
prioritise_braidense.py -- reorder books_braidense.json so that the lookups most
likely to yield something, or most valuable on the map, run first:

  +1  shelfmark in the ECO.03 section (the "most precious" books)
  +1  printed before 1600
  +1  author has a Wikipedia article (judged offline from the pre-warmed summary
      cache: cache/<lang>/summary-* for the author name is a standard page that
      looks like a person)

Books are sorted by score, descending, stable within a score; content is unchanged.
    python3 prioritise_braidense.py
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fetch_descriptions_eco import Wiki, plan, fold, is_standard, looks_like_person  # noqa: E402
from convert_braidense import SRC, OUT_BOOKS, OUT_MAP  # noqa: E402


def main():
    with open(OUT_BOOKS, encoding="utf-8") as fh:
        books = json.load(fh)
    with open(OUT_MAP, encoding="utf-8") as fh:
        id_map = json.load(fh)
    with open(SRC, encoding="utf-8") as fh:
        shelf = {"braidense:%s" % r["bid"].strip(): r.get("shelfmark") or "" for r in csv.DictReader(fh)}
    precious = set()
    for bid, lookup in id_map.items():
        if shelf.get(bid, "").startswith("ECO.03"):
            precious.add(lookup)
    wiki = Wiki(os.path.join(HERE, "cache"), workers=1, offline=True)
    known = {}

    def author_known(p):
        key = fold(p["author"])
        if key not in known:
            ok = False
            for lang in p["langs"]:
                s = wiki.summary(lang, p["author"])
                if s and is_standard(s) and looks_like_person(s, p["surname"]):
                    ok = True
                    break
            known[key] = ok
        return known[key]

    scored = []
    for i, b in enumerate(books):
        p = plan(b)
        score = (b["id"] in precious) + (bool(b.get("year")) and b["year"] < 1600) + (bool(p["author"]) and author_known(p))
        scored.append((-score, i, b))
    scored.sort(key=lambda x: (x[0], x[1]))
    counts = {}
    for s, _, _ in scored:
        counts[-s] = counts.get(-s, 0) + 1
    with open(OUT_BOOKS, "w", encoding="utf-8") as fh:
        json.dump([b for _, _, b in scored], fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("reordered %d lookups by priority score: %s (ECO.03 lookups %d, pre-1600 %d, known authors %d)"
          % (len(books), dict(sorted(counts.items(), reverse=True)), len(precious),
             sum(1 for b in books if b.get("year") and b["year"] < 1600), sum(1 for v in known.values() if v)))


if __name__ == "__main__":
    main()
