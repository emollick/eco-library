#!/usr/bin/env python3
"""
expand_braidense.py -- expand descriptions_braidense.json (keyed by the deduplicated
lookup ids from convert_braidense.py) back to every Braidense record, using
braidense_id_map.json, into descriptions_eco_braidense.json keyed "braidense:<bid>".

    python3 expand_braidense.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "descriptions_braidense.json")
MAP = os.path.join(HERE, "braidense_id_map.json")
OUT = os.path.join(HERE, "descriptions_eco_braidense.json")


def main():
    with open(SRC, encoding="utf-8") as fh:
        desc = json.load(fh)
    with open(MAP, encoding="utf-8") as fh:
        id_map = json.load(fh)
    out, missing = {}, []
    for bid, lookup in id_map.items():
        if lookup in desc:
            out[bid] = dict(desc[lookup])
        else:
            missing.append(bid)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("lookups %d -> records %d written to %s; %d records without a lookup result"
          % (len(desc), len(out), OUT, len(missing)))
    if missing:
        print("  missing:", ", ".join(missing[:10]), "..." if len(missing) > 10 else "")


if __name__ == "__main__":
    main()
