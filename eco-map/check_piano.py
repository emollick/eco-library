#!/usr/bin/env python3
"""Compare the piano piles of books.json with the film reference eco-video/piano_piles.json, pile for pile and spine for spine.

For every pile the reference lists: the same number of spines; at every position from the top the same kind of spine (a blank where the reference
reads a blank, a book where it reads one); for a titled reference entry the same title (exactly, as a fragment the map's fuller title completes, as
the reference's own reading id, or as one of the map's alternative readings); for an untitled entry (an author, a publisher, a spine fragment)
no title on the map, and the same author where both give one; and the heights 5/9/11/13/7/8 on the lid and 11/18/14/4/9/9 on the keyboard shelf.
A first-pass title standing where the reference reads a blank is allowed (the map's readers read those spines; the frame confirms
them) and is listed as a note, not a difference. Prints every difference and exits 1 when there is one.

    python3 check_piano.py [--books books.json] [--ref ../eco-video/piano_piles.json] [-q]
"""
import argparse, json, os, re, sys, unicodedata

H = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--books', default=os.path.join(H, 'books.json'))
ap.add_argument('--ref', default=os.path.join(os.path.dirname(H), 'eco-video', 'piano_piles.json'))
ap.add_argument('-q', '--quiet', action='store_true', help='differences only, no per-pile listing')
args = ap.parse_args()

EXPECTED_HEIGHTS = {'lid': [5, 9, 11, 13, 7, 8], 'keyboard-shelf': [11, 18, 14, 4, 9, 9]}
STOP = {'the', 'a', 'an', 'of', 'and', 'in', 'on', 'to', 'de', 'la', 'le', 'les', 'der', 'die', 'das', 'et', 'il', 'lo', 'gli', 'i', 'l', 'un', 'una', 'uno', 'del', 'della', 'dei', 'delle', 'di', 'da', 'e', 'des', 'du', 'el', 'los', 'las', 'y', 'o'}

def fold(s):
    s = unicodedata.normalize('NFKD', str(s or ''))
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()
def norm(s):
    s = re.sub(r"[^\w]+", ' ', fold(s).replace('*', ' ')).replace('_', ' ')
    return re.sub(r'\s+', ' ', s).strip()
ROMAN = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5'}
def clean_ref(t):
    t = re.sub(r'\([^)]*\)', ' ', t or ''); t = re.sub(r'\.\.\.|…|\?', ' ', t).replace('[', ' ').replace(']', ' ')
    return ' '.join(ROMAN.get(w, w) for w in norm(t).split())
def prefix_match(ref_title, title):
    rt = clean_ref(ref_title).split(); tt = clean_ref(title).split()
    if not rt or not tt: return False
    j = 0
    for w in rt:
        while j < len(tt) and not tt[j].startswith(w): j += 1
        if j >= len(tt): return False
        j += 1
    return True
def surnames(a):
    """The name tokens of an author string (4+ letters; initials, roles and stop words dropped): two strings agree when they share one."""
    a = re.sub(r'\[|\]|\?|\(.*?\)', ' ', a or '')
    return {x for x in norm(a).split() if len(x) >= 4 and x not in STOP and x not in ('cura', 'edited', 'trad')}
def words_in(text, title):
    tw = [w for w in norm(title).split() if len(w) >= 4 and w not in STOP]; st = set(norm(text).split())
    return bool(tw) and all(w in st for w in tw)

books = json.load(open(args.books, encoding='utf-8'))
ref = json.load(open(args.ref, encoding='utf-8'))
by_case = {}
for b in books['books']:
    if str(b.get('bookcase', '')).startswith('obj:salotto:piano-pile-'): by_case.setdefault(b['bookcase'], []).append(b)
objects = {o['id']: o for o in books.get('objects') or []}

diffs, notes = [], []
heights = {'lid': [], 'keyboard-shelf': []}
totals = dict(ref_items=0, ref_titled=0, ref_blank=0, map_books=0, map_blank=0, map_identified=0)
for p in ref['piles']:
    oid = p['object_id']; entries = sorted((e for e in p['books'] if e.get('pos')), key=lambda e: e['pos'])
    H_ref = int(p.get('book_count') or len(entries))
    heights.setdefault(p['level'], []).append(H_ref)
    rows = by_case.get(oid) or []
    if not rows: diffs.append('%s: no books in books.json (reference: %d spines)' % (oid, H_ref)); continue
    n = max(int(b.get('pile_position') or 0) for b in rows) if any(b.get('pile_position') for b in rows) else len(rows)
    by_pos = {}
    for b in rows:
        pos = b.get('pile_position') or (n - int(b.get('slot') or 0))
        if pos in by_pos: diffs.append('%s: two spines at position %d (%s, %s)' % (oid, pos, by_pos[pos]['id'], b['id']))
        by_pos[pos] = b
    o = objects.get(oid) or {}
    if len(rows) != H_ref: diffs.append('%s: %d spines in books.json, the reference counts %d' % (oid, len(rows), H_ref))
    if o.get('count') not in (None, H_ref): diffs.append('%s: object count %s, the reference counts %d' % (oid, o.get('count'), H_ref))
    if o.get('books_high') not in (None, H_ref): diffs.append('%s: books_high %s, the reference counts %d' % (oid, o.get('books_high'), H_ref))
    totals['ref_items'] += len(entries); totals['map_books'] += len(rows)
    if not args.quiet: print('%s (%s, %d high)' % (oid, p['level'], H_ref))
    for e in entries:
        pos = int(e['pos']); b = by_pos.get(pos)
        blank_ref = bool(e.get('unlabelled')); title_ref = (e.get('title') or '').strip(); author_ref = (e.get('author') or '').strip()
        if title_ref and not clean_ref(title_ref): title_ref = ''   # '[...]': the reference could not read the title
        m = e.get('matched') if isinstance(e.get('matched'), dict) else {}
        totals['ref_blank' if blank_ref else 'ref_titled'] += 1
        if b is None: diffs.append('%s pos %d: nothing in books.json (reference: %s)' % (oid, pos, 'blank' if blank_ref else title_ref or author_ref or e.get('spine_text'))); continue
        is_blank = b.get('origin') == 'unlabelled' or b.get('pile_filler')
        totals['map_blank' if is_blank else 'map_identified'] += 1
        mt = b.get('title') or ''; disp = b.get('display_title') or mt or (b.get('author') and b['author'] + ' (title not readable)') or '(blank)'
        alt_titles = [x for x in (b.get('title_variants') or [])] + [a.get('title') or '' for a in (b.get('alt_readings') or [])]
        line = '   %2d  ref: %-42s  map: %s' % (pos, ('blank' if blank_ref else (title_ref or ('[' + (author_ref or e.get('publisher') or 'spine') + ']')))[:42], disp[:60])
        if blank_ref:
            if is_blank: ok = True
            else:
                ok = True; notes.append('%s pos %d: the reference reads a blank (%s); the map keeps the first-pass reading "%s"%s' % (oid, pos, (e.get('spine_text') or '')[:50], disp, ' (spine text agrees)' if words_in(e.get('spine_text') or '', mt) else ''))
        elif title_ref:
            if is_blank: ok = False; diffs.append('%s pos %d: reference reads "%s", the map has a blank' % (oid, pos, title_ref))
            else:
                ok = (clean_ref(title_ref) == clean_ref(mt) and bool(mt)) or prefix_match(title_ref, mt) or (bool(mt) and prefix_match(mt, title_ref)) \
                     or (m.get('catalog') == 'reading' and m.get('id') and (m['id'] == b['id'] or m['id'] in (b.get('merged_ids') or []) or b['id'].startswith(m['id'] + '~'))) \
                     or any(clean_ref(title_ref) == clean_ref(x) or prefix_match(title_ref, x) for x in alt_titles if x) \
                     or (not mt and b.get('author') and clean_ref(title_ref) == clean_ref(b['author']))   # the spine carries only a name: the reference's title is the map's author
                if not ok: diffs.append('%s pos %d: reference reads "%s", the map has "%s" (%s)' % (oid, pos, title_ref, disp, b['id']))
        else:   # untitled: an author, a publisher or a spine fragment
            if is_blank: ok = True; notes.append('%s pos %d: the reference reads an untitled spine (%s); the map has a blank' % (oid, pos, (e.get('spine_text') or '')[:50]))
            elif m.get('catalog') == 'reading' and m.get('id') and (m['id'] == b['id'] or m['id'] in (b.get('merged_ids') or []) or b['id'].startswith(m['id'] + '~')): ok = True   # the reference names this very reading (its title read by the other pass)
            elif mt and not words_in(e.get('spine_text') or '', mt) and not any(prefix_match(mt, x) for x in [e.get('spine_text') or '']):
                ok = False; diffs.append('%s pos %d: reference reads an untitled spine (%s), the map has the title "%s"' % (oid, pos, (e.get('spine_text') or '')[:50], mt))
            elif author_ref and b.get('author') and surnames(author_ref) and surnames(b['author']) and not (surnames(author_ref) & surnames(b['author'])):
                ok = False; diffs.append('%s pos %d: reference reads author %s, the map has %s' % (oid, pos, author_ref, b['author']))
            else: ok = True
        if not args.quiet: print(line + ('' if ok else '   <-- DIFFERENT'))
    for pos, b in sorted(by_pos.items()):
        if pos > H_ref or pos < 1: diffs.append('%s: a spine at position %d outside the reference height %d (%s)' % (oid, pos, H_ref, b['id']))

for level, exp in EXPECTED_HEIGHTS.items():
    if heights.get(level) != exp: diffs.append('heights on the %s: reference %s, expected %s' % (level, heights.get(level), exp))
map_heights = {}
for level in ('lid', 'keyboard-shelf'):
    map_heights[level] = [len(by_case.get(p['object_id']) or []) for p in ref['piles'] if p['level'] == level]
    if map_heights[level] != EXPECTED_HEIGHTS[level]: diffs.append('heights on the %s in books.json: %s, expected %s' % (level, map_heights[level], EXPECTED_HEIGHTS[level]))

print('reference: %d spines (%d read, %d blank); books.json: %d spines (%d identified, %d blank); heights lid %s, keyboard shelf %s' % (
    totals['ref_items'], totals['ref_titled'], totals['ref_blank'], totals['map_books'], totals['map_identified'], totals['map_blank'], map_heights['lid'], map_heights['keyboard-shelf']))
if notes:
    print('%d note%s (allowed):' % (len(notes), '' if len(notes) == 1 else 's'))
    for x in notes: print('  - ' + x)
if diffs:
    print('%d difference%s:' % (len(diffs), '' if len(diffs) == 1 else 's'))
    for x in diffs: print('  * ' + x)
    sys.exit(1)
print('no differences: every piano pile matches the film reference')
