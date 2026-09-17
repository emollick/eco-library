#!/usr/bin/env python3
"""Reconcile the Braidense export (braidense_eco_all.mrc, 2,105 records) with the library's own count of the transferred collection
(1,328 volumes in 73 boxes, August 2021; press kit of 4 May 2022, p. 6). Writes, next to this script's --out directory:
  braidense-reconciliation.jsonl   one line per record: what the record is (a volume, a set, a work bound with others, a reference copy),
                                   its ECO shelfmarks and inventory numbers, links to parent and component records, and the evidence
  braidense-shelfmarks.jsonl       one line per ECO.01-03 running number: the strings under it, the records, and how many volumes it stands for
  reconciliation-summary.json      the counts the About text quotes
A record is a catalogue entry, not a spine: the summary gives a range for the physical volumes and never forces the library's figure.
Usage: python3 reconcile_braidense.py [--mrc ../eco-sources/braidense_eco_all.mrc] [--out reconciliation]
"""
import argparse, collections, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--mrc', default=os.path.join(H, '..', 'eco-sources', 'braidense_eco_all.mrc'))
ap.add_argument('--out', default=os.path.join(H, 'reconciliation'))
args = ap.parse_args()

def iso2709_records(path):
    data = open(path, 'rb').read()
    for raw in data.split(b'\x1d'):
        if len(raw) < 24: continue
        try:
            base = int(raw[12:17]); directory = raw[24:base - 1].decode('ascii', 'replace'); body = raw[base:]
        except Exception: continue
        fields = []
        for i in range(0, len(directory) - 11, 12):
            tag, ln, st = directory[i:i + 3], int(directory[i + 3:i + 7]), int(directory[i + 7:i + 12])
            chunk = body[st:st + ln].rstrip(b'\x1e')
            if tag < '010': fields.append((tag, chunk.decode('utf-8', 'replace'), None)); continue
            parts = chunk.split(b'\x1f'); ind = parts[0].decode('utf-8', 'replace')
            subs = [(p[:1].decode('ascii', 'replace'), p[1:].decode('utf-8', 'replace')) for p in parts[1:] if p]
            fields.append((tag, ind, subs))
        yield fields
def sub(f, tag, code): return [v for t, ind, subs in f if t == tag and subs for c, v in subs if c == code]
def clean(t): return re.sub(r'[\x88\x89]', '', t or '').strip()
BW = re.compile(r'legat[oiae] (con|insieme|a)|in miscellanea|contiene anche|rilegato con', re.I)

recs = {}
for f in iso2709_records(args.mrc):
    bid = next((v for t, v, _ in f if t == '001'), None)
    if bid: recs[bid.strip()] = f
rows = {}
for bid, f in recs.items():
    holds = []
    for t, ind, subs in f:
        if t != '950' or not subs: continue
        cur = None
        for c, v in subs:
            if c == 'd': cur = dict(shelfmark=re.sub(r'\s+', '', v).replace('NBECO.', 'ECO.')); holds.append(cur)
            elif cur is None: continue
            elif c == 'e':
                inv = v[5:16].strip(); tail = v[16:].strip(); m = re.match(r'(VMA|VPA|OPA)\s*(.*)$', tail)
                cur['inventory'] = inv or None; cur['note'] = ((m.group(2) if m else tail).strip(' -') or None); cur['has_e'] = True
            elif c == 'h' and re.match(r'\d{8}$', v.strip()): cur['inventory_date'] = '%s-%s-%s' % (v[:4], v[4:6], v[6:8])
            elif c == 'b': cur['volumes'] = v.strip()
    eco = [h for h in holds if h['shelfmark'].startswith('ECO.')]
    notes = sub(f, '316', 'a') + sub(f, '300', 'a')
    coded = (sub(f, '100', 'a') or [''])[0]; m = re.match(r'\d{8}.(\d{4})', coded)
    rows[bid] = dict(_has_e=any(h.get('has_e') for h in eco), bid=bid, id='braidense:' + bid, title=clean(' '.join(sub(f, '200', 'a')))[:120], responsibility=clean(' '.join(sub(f, '200', 'f')))[:80], edition=' '.join(sub(f, '205', 'a')) or None,
                     date=' '.join(sub(f, '210', 'd')) or None, coded_year=m.group(1) if m else None, extent=' '.join(sub(f, '215', 'a')) or None,
                     parent_461=[v[3:].strip() for t, ind, subs in f if t == '461' and subs for c, v in subs if c == '1' and v.startswith('001')],
                     children_463=[v[3:].strip() for t, ind, subs in f if t == '463' and subs for c, v in subs if c == '1' and v.startswith('001')],
                     possessor_note=any('Possessore' in v for v in sub(f, '317', 'a')), ex_libris=any(re.search(r'ex.?libris', (h.get('note') or '') + ' '.join(notes), re.I) for h in eco),
                     bound_with_note=next((n for n in [h.get('note') or '' for h in eco] + notes if BW.search(n)), None),
                     eco_holdings=[{k: v for k, v in h.items() if v and k != 'has_e'} for h in eco], other_holdings=[h['shelfmark'] for h in holds if not h['shelfmark'].startswith('ECO.')],
                     sections=sorted({m.group(1) for h in eco for m in [re.match(r'ECO\.(\d\d)\.?\d', h['shelfmark'])] if m}))
# classify
owners = collections.defaultdict(list)
for r in rows.values():
    for h in r['eco_holdings']: owners[h['shelfmark']].append(r['bid'])
for r in rows.values():
    kids = [k for k in r['children_463'] if k in rows]; own_inv = r['_has_e']   # the same test as the generator: a 950 $e line of its own
    sec4 = r['sections'] == ['04']
    if not r['eco_holdings']: cat = 'no ECO holding'; ev = 'the record holds only %s' % ', '.join(r['other_holdings'])
    elif kids and not own_inv: cat = 'ECO.04 set record' if sec4 else 'set record without its own inventory'; ev = 'links %d component records (463) and carries no inventory number: a bibliographic wrapper, not a volume' % len(kids)
    elif sec4: cat = 'ECO.04 reference holding'; ev = "section ECO.04 is the library's reference set of Eco's publications (Braidense, 4 May 2022, p. 6); inventoried %s" % ', '.join(h.get('inventory_date', '?') for h in r['eco_holdings'])
    elif kids and own_inv: cat = 'set record with its own inventory'; ev = 'links %d component records and also holds an inventoried copy at set level' % len(kids)
    elif r['parent_461'] and r['bound_with_note']: cat = 'component volume, bound with others'; ev = 'part of a set (461) and noted as bound: %s' % r['bound_with_note'][:120]
    elif r['parent_461']: cat = 'component volume of a set'; ev = 'part of the set %s (461)' % ', '.join(r['parent_461'])
    elif r['bound_with_note']: cat = 'work bound with others'; ev = r['bound_with_note'][:160]
    else: cat = 'transferred volume record'; ev = 'one ECO.01-03 holding with its own inventory number%s' % (', ex libris' if r['ex_libris'] else '')
    shared = [s for s in [h['shelfmark'] for h in r['eco_holdings']] if len(owners[s]) > 1]
    unresolved = None
    odd = [h['shelfmark'] for h in r['eco_holdings'] if not re.match(r'^ECO\.\d\d\.\d{4}(/.*)?$', h['shelfmark'])]
    if odd: r['shelfmark_form_note'] = 'read as ECO.nn.nnnn: %s' % ', '.join(odd)
    if any(not re.match(r'^ECO\.\d\d\.?\d+((?:\.\d+|\.bis)?)(/.*)?$', h['shelfmark']) for h in r['eco_holdings']): unresolved = 'shelfmark not in the ECO.nn.nnnn form: %s' % ', '.join(h['shelfmark'] for h in r['eco_holdings'])
    if cat == 'no ECO holding': unresolved = 'no ECO shelfmark at all (a periodical held under the library\'s own shelfmark)'
    r.update(category=cat, evidence=ev, shelfmark_shared_with_other_records=shared, unresolved=unresolved,
             counted_as='not a volume (its components are)' if cat.startswith('set record without') or cat == 'ECO.04 set record' else 'reference copy of the library, outside the transferred collection' if sec4 else 'not a volume of the transferred collection' if cat == 'no ECO holding' else 'a work in a volume shared with others' if 'bound' in cat else 'a volume (or one of the volumes under its running number)')
# per running number of ECO.01-03
byno = collections.defaultdict(lambda: dict(strings=set(), records=set(), bound=False, setpart=False))
for r in rows.values():
    if r['category'] in ('no ECO holding',): continue
    for h in r['eco_holdings']:
        s = h['shelfmark']; m = re.match(r'^ECO\.(\d\d)\.?(\d+)((?:\.\d+|\.bis)?)(/.*)?$', s)
        if s.startswith('ECO.04') or not m: continue
        base = 'ECO.%s.%04d' % (m.group(1), int(m.group(2))); s = base + (m.group(3) or '') + (m.group(4) or '')   # the export writes some numbers without zero padding (ECO.01.435/03), some with a sub-number (ECO.01.1056.1/), one without its dot (ECO.010610/1)
        e = byno[base]; e['strings'].add(s); e['records'].add(r['bid'])
        if r['bound_with_note'] or 'bound' in r['category']: e['bound'] = True
        if r['parent_461'] or r['category'].startswith('set record'): e['setpart'] = True
shelf_rows = []; vmin = vmax = 0; unresolved_bases = 0
for base in sorted(byno):
    e = byno[base]; n = len(e['strings']); rng = [s for s in e['strings'] if re.search(r'/\d+-\d+$', s)]
    if n == 1: lo = hi = 1; how = 'one string, one volume'
    elif e['setpart'] and not e['bound']: lo = hi = max(1, n - len(rng)); how = 'suffixes are the volumes of a set'
    elif e['bound'] and not e['setpart']: lo, hi = 1, n; how = 'suffixes are works bound together: one volume at least, %d at most' % n
    else: lo, hi = 1, n; how = 'suffixes mix set volumes and bound works: unresolved between 1 and %d' % n; unresolved_bases += 1
    vmin += lo; vmax += hi
    shelf_rows.append(dict(running_number=base, strings=sorted(e['strings']), records=sorted(e['records']), volumes_min=lo, volumes_max=hi, how=how))
cats = collections.Counter(r['category'] for r in rows.values())
summary = dict(export_records=len(rows), by_category=dict(cats.most_common()),
               eco01_03=dict(records=sum(1 for r in rows.values() if r['sections'] and r['sections'] != ['04']), distinct_shelfmark_strings=len({s for e in byno.values() for s in e['strings']}), running_numbers=len(byno),
                             distinct_inventory_numbers=len({h['inventory'] for r in rows.values() for h in r['eco_holdings'] if h.get('inventory') and not h['shelfmark'].startswith('ECO.04')}),
                             volumes_estimate_min=vmin, volumes_estimate_max=vmax, running_numbers_unresolved=unresolved_bases),
               eco04=dict(records=sum(1 for r in rows.values() if r['sections'] == ['04']), holdings=sum(len(r['eco_holdings']) for r in rows.values() if r['sections'] == ['04']),
                          inventoried_before_august_2021=sum(1 for r in rows.values() if r['sections'] == ['04'] for h in r['eco_holdings'] if h.get('inventory_date', '9') < '2021-08'),
                          inventoried_after=sum(1 for r in rows.values() if r['sections'] == ['04'] for h in r['eco_holdings'] if h.get('inventory_date', '') >= '2021-08'),
                          without_inventory=sum(1 for r in rows.values() if r['sections'] == ['04'] for h in r['eco_holdings'] if not h.get('inventory'))),
               braidense_volumes_at_transfer=1328, records_unresolved=[r['bid'] for r in rows.values() if r['unresolved']],
               reading="The library's 1,328 volumes lie inside the estimate's range; the export does not allow an exact count because a running number can carry several volumes of a set (each with a suffix) or several works bound in one volume (also with suffixes), and 335 records note works bound together. No record count is a count of spines.")
os.makedirs(args.out, exist_ok=True)
with open(os.path.join(args.out, 'braidense-reconciliation.jsonl'), 'w', encoding='utf-8') as fh:
    for bid in sorted(rows): fh.write(json.dumps({k: v for k, v in rows[bid].items() if not k.startswith('_')}, ensure_ascii=False) + '\n')
with open(os.path.join(args.out, 'braidense-shelfmarks.jsonl'), 'w', encoding='utf-8') as fh:
    for x in shelf_rows: fh.write(json.dumps(x, ensure_ascii=False) + '\n')
json.dump(summary, open(os.path.join(args.out, 'reconciliation-summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
