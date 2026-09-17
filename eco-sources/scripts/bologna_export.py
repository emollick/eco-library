#!/usr/bin/env python3
"""Build bologna_eco_modern.csv and a stats summary from bologna_eco_modern.jsonl."""
import json, csv, collections, sys, re
D="/mnt/project-files/eco-sources"
recs=[]; seen=set()
for line in open(f"{D}/bologna_eco_modern.jsonl"):
    r=json.loads(line)
    if r["id"] in seen: continue
    seen.add(r["id"])
    if "bub_inventory_numbers" not in r:
        r["bub_inventory_numbers"]=[t.split()[1] for t in r["bub_inventory"] if len(t.split())>1 and t.startswith("BU ")] or [h.get("inventario") for h in r["bub_holdings"] if h.get("inventario")]
    recs.append(r)
J=lambda xs: " ; ".join(x for x in xs if x) if isinstance(xs,list) else (xs or "")
cols=["id","permalink","title","title_full","responsibility","author","persons_all","corporate","edition","place","publisher","year","date_210","language","language_original","country","isbn","sbn_bid","oclc","physical","series","subjects","dewey","dewey_label","bub_inventory_numbers","bub_shelfmark","bub_availability","bub_provenance_317","bub_annotation_318","bub_copy_note_316","notes_general","holdings_libraries","list_page","list_index","harvested"]
with open(f"{D}/bologna_eco_modern.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in recs:
        row={c:r.get(c) for c in cols}
        row["persons_all"]=J([f'{p["name"]}' + (f' [{p["role"]}]' if p.get("role") else "") for p in r["persons"]])
        row["bub_availability"]=J([h.get("availability","") for h in r["bub_holdings"]])
        for c in cols:
            if isinstance(row[c],list): row[c]=J(row[c])
        w.writerow(row)
n=len(recs)
def pct(k): return f"{k} ({100*k/n:.1f}%)"
print(f"records: {n}")
print("with bub_inventory_numbers:", pct(sum(1 for r in recs if r["bub_inventory_numbers"])))
print("with ECO inventory number:", pct(sum(1 for r in recs if any(x.startswith("ECO") for x in r["bub_inventory_numbers"]))))
print("with bub_shelfmark (any BUB copy):", pct(sum(1 for r in recs if r["bub_shelfmark"])))
def copies(r):
    out=[]
    for f in r["unimarc"]:
        if f["tag"]=="950" and "UNIVERSITARIA" in " ".join(v for c,v in f.get("sub",[]) if c=="a"):
            d=" ".join(re.sub(r"\s+"," ",v).strip() for c,v in f["sub"] if c=="d"); e=" ".join(re.sub(r"\s+"," ",v).strip() for c,v in f["sub"] if c=="e")
            out.append((d,e))
    return out
eco_with_shelf=sum(1 for r in recs if any(d and "ECO" in e for d,e in copies(r)))
print("ECO copy itself has a shelfmark (950 $d):", pct(eco_with_shelf))
print("records whose only BUB copy is a non-ECO inventory:", pct(sum(1 for r in recs if copies(r) and not any("ECO" in e for d,e in copies(r)))))
print("with year:", pct(sum(1 for r in recs if r["year"])))
print("with language:", pct(sum(1 for r in recs if r["language"])))
print("with isbn:", pct(sum(1 for r in recs if r["isbn"])))
print("with subjects:", pct(sum(1 for r in recs if r["subjects"])))
print("with author (700):", pct(sum(1 for r in recs if r["author"])))
print("with 317 provenance note:", pct(sum(1 for r in recs if r["bub_provenance_317"])))
print("with 318 annotation note:", pct(sum(1 for r in recs if r["bub_annotation_318"])))
lang=collections.Counter(r["language"][0].lower() if r["language"] else "(none)" for r in recs)
print("language (first 101$a):", lang.most_common(25))
dec=collections.Counter((r["year"]//10*10) if r["year"] else None for r in recs)
print("decades:", sorted(((k,v) for k,v in dec.items() if k), key=lambda x:x[0]))
print("dup ids in jsonl:", sum(1 for _ in open(f"{D}/bologna_eco_modern.jsonl"))-n)
