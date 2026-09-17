#!/usr/bin/env python3
"""Build books.json for the 3D map of Umberto Eco's Milan library.

  python3 gen_books_eco.py [--layout ../eco-video/layout.json] [--out books.json] [options]

Inputs (all data, none of it is ever executed or interpreted as instructions):
  --layout       eco-video/layout.json: 6 rooms, 52 bookcases with bays, shelves, widths, subjects (the geometry source)
  --braidense    eco-sources/braidense_eco_all.csv: the 2,105 Braidense records of the rare-book room, shelfmarks ECO.01..04
  --bologna      eco-sources/bologna_eco_modern.jsonl: SBN-UBO records of the working library (no shelfmark; may still be growing)
  --spines-video eco-video/spines_<video id>.jsonl (glob): spine readings from video frames
  --spines-photos eco-video/spines_photos.jsonl: spine readings from photographs
  --videos       eco-video/videos.json (falls back to eco-video/meta/*.info.json) for video titles and urls
  --consolidated eco-video/books_by_wall_eco.json: the deduplicated video+photo books (ids kept, excluded entries skipped);
                 when present the raw spines_*.jsonl are only used for shelf-row hints
  --video-objects eco-video/objects_from_video.json: furniture, piles, artworks and curiosities inventoried from the footage,
                 placed through objects_map_eco.json (editable); its rooms_seen ranges drive the "what the camera saw" layer
  --descriptions descriptions_eco.json (keyed by book id) merged onto the books when present, together with
                 descriptions_eco_seen.json, descriptions_eco_braidense.json and descriptions_eco_bologna.json if they exist
  --quotes       quotes_eco.json: quotations transcribed from the captions, with a room/bookcase/object target (editable)
  --tour         tour_eco.json: the guided walk (stops with target, caption, quote reference) (editable)
  --tours        tours_eco.json: the sourced tours (behind each novel, the perfect language, ...), each stop with a caption and its source (editable)
  --objects-map  objects_map_eco.json: how the filmed objects are merged and placed (editable)
  experience/    eco-sources/experience/{quotes.json, objects.json, notable_books.json, incunab*.json, tour.json, brief.md}, all optional
  --wall-map     wall_map_eco.json: reader labels (room_id, wall_id, Fondazione letters) -> layout bookcase ids   (editable)
  --subject-map  subject_map_eco.json: Dewey / subject keyword rules -> layout bookcase ids for the Bologna records (editable)

Output: books.json in the shape the page expects (meta, rooms[].bookcases[], books[]) plus books_for_descriptions.json
(the input list for fetch_descriptions_eco.py) and a printed report. Every slot on every working-library bookcase that is
not taken by an identified book is filled with an `unlabelled` placeholder so the shelves look as full as they are;
the rare-book cabinets hold only the catalogued records (the Braidense catalogue is complete), with spine widths set so
that the records fill the cabinets.

Book fields (see README.md): origin video|photo|catalog|unlabelled; placement catalogued|seen|inferred|filler;
source_kind, source_url, timestamp_s/video_id/time for video, sightings[] for video/photo, confidence, language (ISO 639-1
where known), description/description_kind/description_source when a description exists.
Ids: braidense:<bid>, bologna:<UBO id>, video:<video id>:<timestamp_s>:<title slug>, photo:<file stem>:<title slug>, u:<n>.
"""
import argparse, base64, collections, csv, datetime, glob, hashlib, io, json, math, os, random, re, sys, unicodedata
try:
    from PIL import Image   # object thumbnails; without Pillow the objects simply carry no `thumb`
except Exception:
    Image = None

H = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(H)
VIDEO_DIR = os.path.join(PROJ, 'eco-video')
SRC_DIR = os.path.join(PROJ, 'eco-sources')

ap = argparse.ArgumentParser()
ap.add_argument('--layout', default=os.path.join(VIDEO_DIR, 'layout.json'))
ap.add_argument('--braidense', default=os.path.join(SRC_DIR, 'braidense_eco_all.csv'))
ap.add_argument('--braidense-mrc', default=os.path.join(SRC_DIR, 'braidense_eco_all.mrc'), help='the same records as UNIMARC (ISO 2709): only the 461/462 set titles of numbered volumes are read from it; tolerated when absent')
ap.add_argument('--bologna', default=os.path.join(SRC_DIR, 'bologna_eco_modern.jsonl'))
ap.add_argument('--spines-video', default=os.path.join(VIDEO_DIR, 'spines_*.jsonl'), help='glob; spines_photos.jsonl is excluded')
ap.add_argument('--spines-photos', default=None, help='default: eco-video/spines_photos.jsonl')
ap.add_argument('--videos', default=os.path.join(VIDEO_DIR, 'videos.json'))
ap.add_argument('--galleries', default=os.path.join(SRC_DIR, 'fondazione_galleries.json'))
ap.add_argument('--descriptions', default=os.path.join(H, 'descriptions_eco.json'), help='plus descriptions_eco_{seen,braidense,bologna}.json next to it when present')
ap.add_argument('--consolidated', default=os.path.join(VIDEO_DIR, 'books_by_wall_eco.json'), help='deduplicated video+photo books; raw spines are the fallback')
ap.add_argument('--video-objects', default=os.path.join(VIDEO_DIR, 'objects_from_video.json'))
ap.add_argument('--objects-map', default=os.path.join(H, 'objects_map_eco.json'))
ap.add_argument('--quotes', default=os.path.join(H, 'quotes_eco.json'))
ap.add_argument('--tour', default=os.path.join(H, 'tour_eco.json'))
ap.add_argument('--tours', default=os.path.join(H, 'tours_eco.json'))
ap.add_argument('--copy-notes', default=os.path.join(H, 'copy_notes_eco.json'), help='qualifications of Bologna copy records, keyed by record id: {giver_note, drop_givers, status, source}')
ap.add_argument('--wall-map', default=os.path.join(H, 'wall_map_eco.json'))
ap.add_argument('--subject-map', default=os.path.join(H, 'subject_map_eco.json'))
ap.add_argument('--experience', default=os.path.join(SRC_DIR, 'experience'), help='folder with optional quotes.json, objects.json, notable_books.json, tour.json, brief.md')
ap.add_argument('--out', default=os.path.join(H, 'books.json'))
ap.add_argument('--desc-list', default=os.path.join(H, 'books_for_descriptions.json'))
ap.add_argument('--spine-width', type=float, default=0.029, help='mean spine width (m) of the working library; 0.029 = c. 34 volumes per metre')
ap.add_argument('--seed', type=int, default=7)
ap.add_argument('--no-fill', action='store_true', help='skip the unlabelled filler (debugging)')
ap.add_argument('--dropped-log', default=None, help='JSON-lines file listing the Braidense records not drawn (set records, editions of 2022 or later) and the editions of 2016 or later drawn as guesses')
ap.add_argument('--piano-ref', default=os.path.join(VIDEO_DIR, 'piano_piles.json'), help='the film reference of the piano piles (order, titles, blanks per pile); the piles it lists are stacked from it; tolerated when absent')
args = ap.parse_args()
random.seed(args.seed)

WARN = []
def warn(msg):
    WARN.append(msg); print('WARN', msg)

# ------------------------------------------------------------------ text helpers
def fold(s):
    s = unicodedata.normalize('NFKD', str(s or ''))
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()
def norm(s):
    s = fold(s).replace('*', ' ')
    s = re.sub(r"[^\w]+", ' ', s).replace('_', ' ')
    return re.sub(r'\s+', ' ', s).strip()
STOP = {'the', 'a', 'an', 'of', 'and', 'in', 'on', 'to', 'vol', 'vols', 'volume', 'ed', 'eds', 'with', 'for', 'by', 'de', 'la', 'le', 'les', 'der',
        'die', 'das', 'et', 'il', 'lo', 'gli', 'i', 'l', 'un', 'una', 'uno', 'del', 'della', 'dei', 'delle', 'di', 'da', 'e', 'ed', 'des', 'du', 'el', 'los', 'las', 'y', 'o', 'et',
        'sive', 'seu'}   # Latin 'or' ('Ars magna sciendi, sive Combinatoria') is not a title word shared with 'Musurgia universalis sive Ars magna consoni'
def tokens(s): return {t for t in norm(s).split() if t not in STOP and (len(t) > 1 or t.isdigit())}
def slug(s, n=40):
    s = norm(s).replace(' ', '-')
    return (s[:n].rstrip('-') or 'untitled')
def spine_key(title, author):
    """Dedup key of a spine reading: the title without parentheticals and stop words, plus the author's surname ('|<surname>' for an author-only reading)."""
    t = (' '.join(x for x in norm(re.sub(r'\(.*?\)', ' ', title)).split() if x not in STOP) or norm(title)) if title else ''
    a = [x for x in norm(re.sub(r'\(.*?\)', ' ', author or '')).split() if x not in STOP]
    return t + '|' + (a[0] if a else '')
def surname(author):
    """'Roberto Calasso' -> calasso; 'Calasso, Roberto' -> calasso; 'par Alexandre Dumas' -> dumas; None when nothing usable is left."""
    a = re.sub(r'\(.*?\)|<.*?>|\[.*?\]', ' ', author or '')
    head = a.split(',')[0] if ',' in a else a
    toks = [x for x in norm(head).split() if x not in STOP and len(x) > 1 and not re.match(r'^(par|by|von|van|de|di|del|della|dr|prof|sir|mr|mrs|ed|eds|cura|introduzione|introduction|trad|translated|edited)$', x)]
    if not toks: return None
    return toks[0] if ',' in a else toks[-1]
def work_key(title, author):
    """Key of a *work* for merging readings of the same physical book: title tokens minus stop words and parentheticals + the author's surname
    (spine_key keeps the author's first token, so 'John Locke' and 'Locke, John' would not meet)."""
    t = ' '.join(x for x in norm(re.sub(r'\(.*?\)', ' ', title or '')).split() if x not in STOP)
    return t + '|' + (surname(author) or '')
def hms(t):
    t = int(t or 0); return '%02d:%02d:%02d' % (t // 3600, t % 3600 // 60, t % 60)
def hid(s, n=8): return hashlib.sha1(s.encode('utf-8')).hexdigest()[:n]

# layout.json statements superseded by later checks (the file itself is the video pipeline's; the corrections are applied here so the page never shows the stale text)
LAYOUT_NOTE_FIXES = [
    (re.compile(r"17 of (?:the |Eco's )?36 incunabula \(AIB Studi 2022\) are absent from the Braidense export and are added from the experience/incunabula list"),
     'all 36 incunabula of the AIB Studi 2022 list are in the Braidense records (19 under ECO.03, 17 under ECO.01), each with Eco\'s own card'),
    (re.compile(r"17 of Eco's 36 incunabula are absent from the Braidense export and are listed from AIB Studi 2022"),
     'all 36 incunabula of the AIB Studi 2022 list are in the Braidense records: 19 under ECO.03 and 17 under ECO.01'),
    (re.compile(r"AIB Studi 2022 lists 36 incunabula, 17 of them absent from the Braidense export"), 'AIB Studi 2022 lists 36 incunabula, all of them in the Braidense records: 19 here and 17 under ECO.01'),
]
def fix_layout_text(s):
    for rx, rep in LAYOUT_NOTE_FIXES:
        if isinstance(s, str): s = rx.sub(rep, s)
    return s

# --- numbered volumes: a record whose own title is only '2', 'Vol. 1.', '[1]', '1: Aesthetica' gets a display title composed from the set title
# (UNIMARC 461, embedded 200 $a) as '<set title>, vol. N[: own title]'; the original statement is kept in volume_statement
VOL_RE = re.compile(r"^\s*\[?\s*(?:vol|vols|volume|volumen|v|t|tomo|tomus|tome|bd|band|parte|pars|part|partie|teil|livre|liber|libro|book|fasc|fascicolo|deel|cahier|heft)?\s*\.?\s*\]?\s*\[?(\d{1,2}(?:\.\d{1,2}){0,3}(?:\s*/\s*\d{1,2})?(?:\s*[-–]\s*\d{1,2}(?:\.\d{1,2}){0,3})?)\]?((?:\.\d{1,2}){0,3})(?:\s+(?:di|of|de|von|sur|su)\s+(\d{1,2}))?\s*\.?\s*(?:$|[:;,-]\s*\]?\s*(.*)$|\s*/(?!\s*\d).*$|\s+(\d{4}\s*[-\u2013]\s*\d{4})\s*\.?\s*$)", re.I)   # dotted numbering ('[1.3]', '[2.2].1.3', 'Vol. 1.2'), '[v.] 2', a ' / responsibility' tail; 'Volume 1 di 2' (the count kept as 'vol. 1 of 2'), '1/ Guillaume Libri' (no space before the slash); 'Tomus 2', 'Libro 1: ...', a bracket closed after the separator ('[1:] La camera da letto'), a year range as the volume's own title ('Vol.1 1857-1866'); two volumes bound as one ('3/4: Exact logic'); a range is the volume number as the catalogue writes it ('1-2: Principles of philosophy', '5 - 2: Corso di storia della chiesa', '31.1-2: Rhetorica'), the hyphen kept, never read as a separator that would print 'vol. 1: 2: Principles ...'
# a volume statement written in words ('Tome premier', 'Tome quatrieme', 'Parte seconda', 'Vol. II') is a volume too: fourteen rare-room spines read 'Tome second' with no set title
VOL_WORDS = {'premier': 1, 'premiere': 1, 'première': 1, 'first': 1, 'primo': 1, 'prima': 1, 'primus': 1, 'primum': 1, 'erster': 1, 'erste': 1, 'second': 2, 'seconde': 2, 'deuxieme': 2, 'deuxième': 2, 'secondo': 2, 'seconda': 2, 'secunda': 2, 'secundus': 2, 'secundum': 2, 'altera': 2, 'alter': 2, 'alterum': 2, 'zweiter': 2, 'zweite': 2,
             'troisieme': 3, 'troisième': 3, 'third': 3, 'terzo': 3, 'terza': 3, 'tertia': 3, 'tertius': 3, 'tertium': 3, 'dritter': 3, 'dritte': 3, 'quatrieme': 4, 'quatrième': 4, 'fourth': 4, 'quarto': 4, 'quarta': 4, 'quartus': 4, 'quartum': 4, 'vierter': 4, 'vierte': 4,
             'cinquieme': 5, 'cinquième': 5, 'fifth': 5, 'quinto': 5, 'quinta': 5, 'quintus': 5, 'quintum': 5, 'sixieme': 6, 'sixième': 6, 'sixth': 6, 'sesto': 6, 'sesta': 6, 'sexta': 6, 'sextus': 6, 'septieme': 7, 'septième': 7, 'seventh': 7, 'settimo': 7, 'settima': 7, 'septima': 7,
             'huitieme': 8, 'huitième': 8, 'eighth': 8, 'ottavo': 8, 'ottava': 8, 'octava': 8, 'neuvieme': 9, 'neuvième': 9, 'ninth': 9, 'nono': 9, 'nona': 9, 'dixieme': 10, 'dixième': 10, 'tenth': 10, 'decimo': 10, 'decima': 10}   # the Latin ordinals too ('Pars prima', 'Pars altera', 'Tomus primus')
VOL_WORD_RE = re.compile(r"^\s*\[?\s*(?:vol|volume|volumen|t|tomo|tomus|tome|bd|band|parte|pars|part|partie|teil|livre|liber|libro|book|deel)\s*\.?\s*\]?\s+([a-zà-ÿ]+|[ivxl]{1,6})\s*\.?\s*(?:$|[:;,-]\s*\]?\s*(.*)$|\s*/(?!\s*\d).*$)", re.I)
SET_RANGE_RE = re.compile(r"[\s.,;:]*(?:\.\.\.\s*)?\b(?:(?:tomus|tomi|tome|tomes|tomo|vol|vols|volume|volumes|volumen|pars|partes|parte|parti|partie|parties|libro|liber|libri|band|bände|teil|book|books|fasc|fascicolo|deel|cahier|centuria|centurie)\.?\s+(?:\d{1,3}|[ivxl]{1,6}|[a-zà-ÿ-]+)\.?\s*[\[(]\s*[-–]\s*(?:\d{1,3}|[ivxl]{1,6}|[a-zà-ÿ-]+)(?:\.?\s*(?:&|et|e|und|and)\s*(?:\d{1,3}|[a-zà-ÿ-]+))?\.?\s*[\])]|(?:\d{1,3}|[ivxl]{1,6}|[a-zà-ÿ-]+)\.?\s*[\[(]\s*[-–]\s*(?:\d{1,3}|[ivxl]{1,6}|[a-zà-ÿ-]+)\s+(?:tomus|tome|tomes|tomo|volume|volumes|pars|parte|partie|libro|band|teil|book|deel)\.?\s*[\])])\s*[;,.]?\s*(?:\.\.\.|…)?[\s.;,]*$", re.I)   # the set's own volume range at the end of its title ('Tome premier [-quatrieme]', 'Pars 1. [-4.], ...', 'Centuria prima [-seconda]', 'Premiere [-seconde tome]', 'Tome premier [-6. & dernier]') is not repeated beside the volume number
def tidy_volume_rest(rest):
    """The volume's own title after its number, without the ISBD responsibility tail, a bracket the record left open ('[Latréaumont', '] La camera da letto') or a closing stop."""
    rest = re.sub(r'\s+/\s+[^/]*$', '', rest or '').strip(' .:;,-')
    if rest.startswith('[') and ']' not in rest: rest = rest[1:]
    if rest.endswith(']') and '[' not in rest: rest = rest[:-1]
    if rest.startswith(']') and '[' not in rest: rest = rest[1:]
    return rest.strip(' .:;,-')
def roman_int(r):
    v, out = {'i': 1, 'v': 5, 'x': 10, 'l': 50}, 0
    r = r.lower()
    if not r or any(ch not in v for ch in r): return None
    for i, ch in enumerate(r): out += -v[ch] if i + 1 < len(r) and v[ch] < v[r[i + 1]] else v[ch]
    return out
def volume_of(title):
    """-> (volume number as written, rest of the title) when the title is a bare volume statement ('2', 'Vol. 1.', '[1]', '[1.3]', '1: A-E', '2: Pars 2', 'Volume 1 di 2' -> '1 of 2',
    'Tome second' -> '2'), else None. A number followed by plain words ('2 girls and a dog', '1779 les nuees') is a title: the rest must follow a separator."""
    t = (title or '').replace('*', '').replace('\x88', '').replace('\x89', '').strip()
    m = VOL_RE.match(t)
    if m:
        rest = tidy_volume_rest(m.group(4) or m.group(5))   # 'Premier partie, tome 2. / Henri de Lubac': the responsibility after the ISBD slash is not part of the volume's title; a year range ('Vol.1 1857-1866') is
        return re.sub(r'\s*[-\u2013]\s*', '-', m.group(1)) + (m.group(2) or '') + ((' of ' + m.group(3)) if m.group(3) else ''), rest   # a range prints with the catalogue's hyphen and no spaces ('5 - 2' -> '5-2')
    m = VOL_WORD_RE.match(t)
    if not m: return None
    w = m.group(1).lower(); n = VOL_WORDS.get(w) or roman_int(w)
    if not n: return None
    return str(n), tidy_volume_rest(m.group(2))
def clean_title(t):
    t = sbn_brackets(re.sub(r'\s*\[!\]', ' ' + SIC_MARK, (t or '')).replace('*', '').replace('̱', '').replace('\x88', '').replace('\x89', ''))   # the cataloguer's [!] (sic) taken out before the bracket pass, which turned it into '[]]' ('delea [!] naturale'); printed as '[sic]' ('delea [sic] naturale'), so the printer's misprint does not read as the map's
    return re.sub(r'\s+', ' ', t).strip()

# ------------------------------------------------------------------ reader-facing text (schema_eco.md, "Display cleaning")
LOCAL_SRC_RE = re.compile(r"\s*\((?:local|file|see)\s+[\w.-]+\.(?:txt|md|json|csv)\)")   # workshop provenance inside a citation: "(local carriere.txt)"
SIC_RE = re.compile(r"\s*\[!\]")                                                            # the cataloguer's [!] (sic)
SIC_MARK = '[sic]'                                                                            # how the page prints it
VOL_RANGE_RE = re.compile(r"^\s*\[(\d{1,3}\s*[-–]\s*\d{1,3})\]\s*:\s*")                        # "[24-32]: " volume-range prefix of a set title
NONSORT_STAR_RE = re.compile(r"(?<![^\s'’\"(\[/])\*(?=\w)")                                    # SBN non-sorting marker "Il *nome" (not the asterisks of "M***")
AUTHOR_QUAL_RE = re.compile(r"\s*:\s*([^\s#]+)#")                                              # SBN name qualifier "William : of#Ockham" -> "William of Ockham"
AUTHOR_PART_RE = re.compile(r"\s+:\s+((?:d[’']|de|da|di|du|des|del|della|von|van|of|le|la|dos|do)(?:\s+\S.*)?)$", re.I)   # "Balzac, Honoré : de" -> "Balzac, Honoré de"
AUTHOR_ROLE_RE = re.compile(r"^((?:a cura di|testi di|saggi di|scritti di|catalogued by|edited by|herausgegeben von|hrsg\.? von)[^!\[\]]*?)\s*!", re.I)   # "a cura di! X" -> "[a cura di] X"
def sbn_brackets(t):
    """SBN/UNIMARC exports write the cataloguer's square brackets as '\\...!' (also '°...!'): '\\Anversa!' -> '[Anversa]', '°1!:' -> '[1]:',
    'Paris [etc.!' -> 'Paris [etc.]'. A '!' with no bracket open ('GOSH!', 'Goodbye, Kant!') is left alone; a bracket still open at the end is closed."""
    if '\\' not in t and '!' not in t and '°' not in t: return t
    t = re.sub(r"\s{2,}(etc|ecc)\.?!\.?", r" [\1.]", t)          # 'Roma  etc.!' (the opening marker lost in the export) -> 'Roma [etc.]'
    t = t.replace('\\', '[')
    t = re.sub(r'°(?=[\w\[])', '[', t)                          # '°1!:' and '°s.n.!'; the degree sign of '1°.' stays
    t = re.sub(r'^(s\.\s?[ne]\.)!', r'[\1]', t)                   # 's. n.!' (sine nomine, opening marker lost)
    t = re.sub(r'(?<=\s)-(\w+)!(?![-\w])', r'[-\1]', t)             # 'tome premier -second!' (the bracket before the hyphen lost) -> 'tome premier [-second]'; not an exclamation set between dashes ('incontrarci -chissà!- nel Montefeltro')
    out = []; depth = 0
    for ch in t:
        if ch == '[': depth += 1
        elif ch == ']': depth = max(0, depth - 1)
        elif ch == '!' and depth > 0: ch = ']'; depth -= 1
        out.append(ch)
    t = ''.join(out)
    if depth > 0: t = t.rstrip() + ']' * depth
    return t
CLEAN_COUNTS = collections.Counter()
def clean_display(s, kind=None):
    """Reader-facing form of a catalogue or workshop string: SBN brackets and non-sorting markers resolved ('<<Les >>', 'Il *nome'), '[!]' sic
    marks printed as '[sic]', SBN name qualifiers joined (kind 'author': 'William : of#Ockham' -> 'William of Ockham', 'Albertus : Magnus' -> 'Albertus Magnus'),
    volume-range prefixes dropped (kind 'title': '[24-32]: Frederici Ruyschii ...'), and internal provenance notes removed ('(local carriere.txt)').
    Returns the string unchanged when nothing applies; never empties a string."""
    if not isinstance(s, str) or not s: return s
    t = s.replace('\x88', '').replace('\x89', '').replace('\u0331', '')
    t = re.sub(r'<<\s*', '', t); t = re.sub(r'\s*>>', ' ', t)
    t = NONSORT_STAR_RE.sub('', t)
    t = SIC_RE.sub(' ' + SIC_MARK, t)   # the cataloguer's mark stays, in the reader's form
    t = LOCAL_SRC_RE.sub('', t)
    if kind == 'author':
        t = AUTHOR_ROLE_RE.sub(r'[\1]', t)
        t = AUTHOR_QUAL_RE.sub(r' \1 ', t)
    t = sbn_brackets(t)
    if kind == 'author':
        t = AUTHOR_PART_RE.sub(r' \1', t)
        if ',' not in t: t = re.sub(r'^([^:]+?)\s+:\s+([^:]+)$', r'\1 \2', t)   # 'Albertus : Magnus', 'Robert : de Clari'
    if kind == 'title': t = VOL_RANGE_RE.sub('', t); t = re.sub(r'^\s*\d{1,2}\.\[\d{1,2}\]\s*:\s*', '', t)   # '1.[1]: De macrocosmi historia' (a part numbering in front of the title)
    if kind == 'title':   # the export's field separators and ISBD tails never reach the page ('contro tutti| quando la satira diventa criminale|', 'Luigi 13. /', 'in any age :', 'proponitur;'); title_raw keeps the export's words
        t2 = re.sub(r'\s*\|\s*$', '', t); t2 = re.sub(r'\s*\|\s*', ': ', t2); t2 = re.sub(r'\s*[/:;]\s*$', '', t2)
        if t2 != t: TITLE_TAILS.append((t, t2)); t = t2
    t = close_elisions(t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t if t else s
TITLE_TAILS = []   # every title the tail rule changed, (before, after)
# the SBN non-sorting marker of an elided article ('<<L' >>Ordre') and the name qualifier of a particle ('Ormesson, Jean : d'') left a
# space after the apostrophe ('L' Ordre', 'Jean d' Ormesson', 'D' Alembert'). The elisions of Italian, French and Catalan close up again; 'po' ',
# 'sta' ' and 'E' un dubbio' are not elisions and keep their space.
_ELIDED = r"(l|d|un|dell|dall|nell|all|sull|quell|coll|dagl|degl|negl|agl|sugl|gl|c|ch|s|m|t|v|n|qu|j|jusqu|lorsqu|puisqu|quoiqu)"
ELISION_RE = re.compile(r"(?<![\w'\u2019])" + _ELIDED + r"(['\u2019])\s+(?=[\w\u00c0-\u024f])")   # a lower-case elided form anywhere: "Jean d' Ormesson", "presso l' Accademia", "all' illustrazione"
ELISION_CAP_RE = re.compile(r"(?:^|(?<=[:.;!?(\[\"\u00ab]\s)|(?<=[(\[\"\u00ab]))" + _ELIDED.replace('(l|', '(L|l|').replace('|d|', '|D|d|').replace('|un|', '|Un|un|').replace('|dell|', '|Dell|dell|').replace('|dall|', '|Dall|dall|').replace('|nell|', '|Nell|nell|').replace('|all|', '|All|all|').replace('|sull|', '|Sull|sull|').replace('|quell|', '|Quell|quell|').replace('|coll|', '|Coll|coll|').replace('|gl|', '|Gl|gl|').replace('|c|', '|C|c|').replace('|ch|', '|Ch|ch|').replace('|s|', '|S|s|').replace('|m|', '|M|m|').replace('|t|', '|T|t|').replace('|v|', '|V|v|').replace('|n|', '|N|n|').replace('|qu|', '|Qu|qu|').replace('|j|', '|J|j|').replace('|jusqu|', '|Jusqu|jusqu|').replace('|lorsqu|', '|Lorsqu|lorsqu|').replace('|puisqu|', '|Puisqu|puisqu|').replace('|quoiqu)', '|Quoiqu|quoiqu)') + r"(['\u2019])\s+(?=[\w\u00c0-\u024f])")   # a capitalised form only where a sentence or a title begins ("L' envie", "D' Alembert"), never inside a line: "a print with 'AB C' letters" is a quotation, not an elision
ELISION_FIXED = []   # (before, after)
QUOTE_OPEN_RE = re.compile(r"(?:^|[\s(\[])['\u2019](?=\S)")   # an apostrophe that opens a quotation: after a space or a bracket, before a word ("a print with 'AB C' letters")
def close_elisions(t):
    def sub(m):   # inside an open single-quoted span the apostrophe closes the quotation, so "'ab c' seen" keeps its space
        return m.group(0) if len(QUOTE_OPEN_RE.findall(t[:m.start()])) % 2 == 1 else m.group(1) + m.group(2)
    t2 = ELISION_CAP_RE.sub(sub, ELISION_RE.sub(sub, t))
    if t2 != t: ELISION_FIXED.append((t, t2))
    return t2
def clean_field(d, key, kind=None, raw_key=None):
    """clean_display() one field in place (a string or a list of strings), keeping the original under raw_key when asked; counts what changed."""
    v = d.get(key)
    if isinstance(v, str):
        c = clean_display(v, kind)
        if c != v:
            if raw_key and raw_key not in d: d[raw_key] = v   # a title_raw set by the composer (the export's own words) stays
            d[key] = c; CLEAN_COUNTS[key] += 1
    elif isinstance(v, list) and v and all(isinstance(x, str) for x in v):
        c = [clean_display(x, kind) for x in v]
        if c != v: d[key] = c; CLEAN_COUNTS[key] += 1
def clean_quotes(qs):
    for q in qs or []:
        if isinstance(q, dict):
            for k in ('text', 'text_it', 'source', 'speaker', 'context'): clean_field(q, k)
PHOTO_BAY_RE = re.compile(r'^fondazione_(\d+)_(.+?)(?:\.\w+)?$')
def photo_name(frame):
    """A reader-facing name for a photograph file: 'fondazione_17_I.webp' -> "a Fondazione Umberto Eco photograph (bookcase I)"; never the file name."""
    f = os.path.basename(frame or '')
    m = PHOTO_BAY_RE.match(f)
    if m:
        bay = m.group(2).replace('_', ' ')
        if re.match(r'^(A-da 1 a 6)$', bay): bay = 'A, bays 1-6'
        if re.match(r'^[A-S](?:-[AB]|[abc]|\d+-\d+)?$', bay) or bay == 'A, bays 1-6': return 'a Fondazione Umberto Eco photograph (bookcase %s)' % bay
        if bay.lower().startswith('studio antichi') or bay.startswith('ANTICHI') or re.match(r'^\d', bay): return 'a Fondazione Umberto Eco photograph of the Stanza degli antichi (no. %s)' % m.group(1).lstrip('0')
        return 'a Fondazione Umberto Eco photograph (no. %s)' % m.group(1).lstrip('0')
    if f.startswith('flickr_'): return 'a Flickr photograph by Martin Gruner Larsen (2011)'
    if f.startswith('criticaletteraria'): return 'a CriticaLetteraria photograph (November 2022)'
    if f.startswith('getty'): return 'a Getty Images photograph'
    if f.startswith('zanni'): return 'a photograph by Andrea Zanni (2010)'
    return 'a photograph'
def mmss(t):
    """'00:13:02' -> '13:02'; '01:15:05' -> '1:15:05'."""
    if not t: return t
    m = re.match(r'^(\d\d):(\d\d):(\d\d)$', str(t))
    if not m: return t
    h, mi, s = int(m.group(1)), m.group(2), m.group(3)
    return ('%d:%s:%s' % (h, mi, s)) if h else ('%d:%s' % (int(mi), s))
def compose_volume_title(title, set_title):
    """'Vol. 1.' + 'Les historiettes' -> 'Les historiettes, vol. 1'; '1: Aesthetica' + 'Scritti minori' -> 'Scritti minori, vol. 1: Aesthetica'. None when not a volume."""
    v = volume_of(title)
    if not v or not set_title: return None
    n, rest = v
    base = SET_RANGE_RE.sub('', set_title.strip()).strip(' .,;:') or set_title.strip()   # '... Tome premier [-quatrieme], vol. 4' said the range and the number both
    if rest and fold(rest) == fold(base): rest = ''   # a volume whose own title repeats the set's ('[1:] La camera da letto' under 'La camera da letto') is 'La camera da letto, vol. 1'
    if rest and fold(rest).startswith(fold(base)) and len(fold(rest)) > len(fold(base)) + 3: return '%s, vol. %s' % (rest, n)   # a volume whose own title opens with the set's and goes on ('1: Dialogi di Antonio Brucioli della naturale philosophia humana') keeps its own title, the number after it, rather than printing the set's twice
    bw, rw = fold(base).split(), (fold(rest).split() if rest else []); k = 0
    while k < min(len(bw), len(rw)) and bw[k] == rw[k]: k += 1
    if rest and k >= 3 and k * 2 >= len(bw) and len(rw) > k: return '%s, vol. %s' % (rest, n)   # a volume title that opens with the set's first words and goes its own way ('5: Dialogi di Antonio Brucioli libro quinto' under 'Dialogi di Antonio Brucioli della morale philosophia') is kept whole too, the number after it
    return '%s, vol. %s%s' % (base, n, (': ' + rest) if rest else '')
def unimarc_embedded(subs, tag='200', codes=('a',)):
    """Subfield values of the embedded field `tag` inside a UNIMARC linking field (461 ...): the block after '$1 <tag>..' up to the next '$1'."""
    out, inside = [], False
    for c, v in subs:
        if c == '1': inside = str(v).startswith(tag); continue
        if inside and c in codes and v: out.append(str(v))
    return out
def iso2709_records(path):
    """Minimal ISO 2709 reader (no pymarc): yields lists of (tag, indicators, [(code, value), ...]) per record; control fields give (tag, value, None)."""
    data = open(path, 'rb').read()
    for rec in data.split(b'\x1d'):
        if len(rec) < 30: continue
        try:
            base = int(rec[12:17]); directory = rec[24:base - 1]; fields = []
            for i in range(0, len(directory), 12):
                e = directory[i:i + 12]
                if len(e) < 12: break
                tag = e[:3].decode(); ln = int(e[3:7]); st = int(e[7:12]); raw = rec[base + st:base + st + ln].rstrip(b'\x1e')
                if tag < '010': fields.append((tag, raw.decode('utf-8', 'replace'), None)); continue
                subs = [(chr(p[0]), p[1:].decode('utf-8', 'replace')) for p in raw[2:].split(b'\x1f')[1:] if p]
                fields.append((tag, raw[:2].decode('utf-8', 'replace'), subs))
            yield fields
        except Exception: continue

LANG = {'it': 'it', 'ita': 'it', 'italian': 'it', 'italiano': 'it', 'fr': 'fr', 'fre': 'fr', 'fra': 'fr', 'french': 'fr', 'francais': 'fr',
        'en': 'en', 'eng': 'en', 'english': 'en', 'inglese': 'en', 'de': 'de', 'ger': 'de', 'deu': 'de', 'german': 'de', 'deutsch': 'de', 'tedesco': 'de',
        'la': 'la', 'lat': 'la', 'latin': 'la', 'latino': 'la', 'es': 'es', 'spa': 'es', 'spanish': 'es', 'espanol': 'es', 'spagnolo': 'es',
        'pt': 'pt', 'por': 'pt', 'portuguese': 'pt', 'nl': 'nl', 'dut': 'nl', 'nld': 'nl', 'dutch': 'nl', 'ru': 'ru', 'rus': 'ru', 'russian': 'ru',
        'el': 'el', 'gre': 'el', 'ell': 'el', 'greek': 'el', 'grc': 'grc', 'he': 'he', 'heb': 'he', 'hebrew': 'he', 'ar': 'ar', 'ara': 'ar',
        'ja': 'ja', 'jpn': 'ja', 'zh': 'zh', 'chi': 'zh', 'pl': 'pl', 'pol': 'pl', 'cs': 'cs', 'cze': 'cs', 'hu': 'hu', 'hun': 'hu', 'sv': 'sv', 'swe': 'sv',
        'da': 'da', 'dan': 'da', 'no': 'no', 'nor': 'no', 'fi': 'fi', 'fin': 'fi', 'tr': 'tr', 'tur': 'tr', 'ca': 'ca', 'cat': 'ca', 'ro': 'ro', 'rum': 'ro',
        'sr': 'sr', 'srp': 'sr', 'hr': 'hr', 'hrv': 'hr', 'hbs': 'sh', 'mul': 'mul', 'und': None, 'inh': None, 'epo': 'eo', 'frm': 'fr', 'gr': 'el',
        'uk': 'uk', 'ukr': 'uk', 'lt': 'lt', 'lit': 'lt', 'bg': 'bg', 'bul': 'bg', 'ko': 'ko', 'kor': 'ko', 'fro': 'fro', 'zxx': 'zxx', 'sl': 'sl', 'slv': 'sl', 'sk': 'sk', 'slo': 'sk', 'et': 'et', 'est': 'et', 'lv': 'lv', 'lav': 'lv',
        'sq': 'sq', 'alb': 'sq', 'mk': 'mk', 'mac': 'mk', 'ka': 'ka', 'geo': 'ka', 'fa': 'fa', 'per': 'fa', 'eu': 'eu', 'baq': 'eu', 'gl': 'gl', 'glg': 'gl', 'is': 'is', 'ice': 'is', 'vi': 'vi', 'vie': 'vi', 'th': 'th', 'tha': 'th', 'id': 'id', 'ind': 'id',
        'ang': 'ang', 'enm': 'enm', 'dum': 'dum', 'gmh': 'gmh', 'goh': 'goh', 'pro': 'pro', 'oci': 'oc', 'oc': 'oc', 'chu': 'chu', 'san': 'sa', 'sa': 'sa', 'cop': 'cop', 'syr': 'syr', 'egy': 'egy', 'akk': 'akk', 'sux': 'sux'}   # a code with no entry here passed through as it was ('kor', 'lit', 'uk', 'zxx') and, with no name in LANG_NAME, printed as the language line; the three-letter codes of the records are read to their two-letter forms where one exists
LANG_NAME = {'it': 'Italian', 'fr': 'French', 'en': 'English', 'de': 'German', 'la': 'Latin', 'es': 'Spanish', 'pt': 'Portuguese', 'nl': 'Dutch', 'ru': 'Russian',
             'el': 'Greek', 'grc': 'Ancient Greek', 'he': 'Hebrew', 'ar': 'Arabic', 'ja': 'Japanese', 'zh': 'Chinese', 'pl': 'Polish', 'cs': 'Czech', 'hu': 'Hungarian',
             'sv': 'Swedish', 'da': 'Danish', 'no': 'Norwegian', 'fi': 'Finnish', 'tr': 'Turkish', 'ca': 'Catalan', 'ro': 'Romanian', 'sr': 'Serbian', 'hr': 'Croatian',
             'sh': 'Serbo-Croatian', 'mul': 'several languages', 'eo': 'Esperanto',
             'uk': 'Ukrainian', 'lt': 'Lithuanian', 'bg': 'Bulgarian', 'ko': 'Korean', 'fro': 'Old French', 'zxx': 'no linguistic content', 'sl': 'Slovene', 'sk': 'Slovak', 'et': 'Estonian', 'lv': 'Latvian', 'sq': 'Albanian', 'mk': 'Macedonian',
             'ka': 'Georgian', 'fa': 'Persian', 'eu': 'Basque', 'gl': 'Galician', 'is': 'Icelandic', 'vi': 'Vietnamese', 'th': 'Thai', 'id': 'Indonesian', 'ang': 'Old English', 'enm': 'Middle English', 'dum': 'Middle Dutch', 'gmh': 'Middle High German',
             'goh': 'Old High German', 'pro': 'Old Occitan', 'oc': 'Occitan', 'chu': 'Church Slavonic', 'sa': 'Sanskrit', 'cop': 'Coptic', 'syr': 'Syriac', 'egy': 'Egyptian', 'akk': 'Akkadian', 'sux': 'Sumerian'}   # every code the records carry has a name (twelve cards printed 'uk', 'lt', 'bg', 'kor', 'lit', 'fro' and 'zxx' as their language); 'zxx' is the cataloguer's code for a record with no linguistic content
LANG_UNNAMED = collections.Counter()   # codes served with no name, refused below
def lang_code(c):
    if not c: return None
    c = str(c).strip().lower()
    if c in LANG: return LANG[c]
    return c if 2 <= len(c) <= 3 else None

# ------------------------------------------------------------------ layout -> rooms / bookcases (page geometry)
L = json.load(open(args.layout, encoding='utf-8'))
ROOM_PLAN = {   # world origins (m) and, where the layout's approx_size_m must be transposed to fit its own bookcases, the size
    # the walk order of the 2015 take (salotto door -> vestibule -> corridor -> study door) and the corrections in layout.md:
    # the vestibule hangs below the salotto door, the corridor runs east from bookcase D's doorway, the rare-book room opens
    # off the print wall 3.5 m after the corridor start, the art leg and the study door are at the far end of the corridor
    # the salotto is drawn at its footage size, 7.5 x 7.6 m (salotto_layout.json); its door wall stays at world z 7.0 against the vestibule,
    # so the room grows north (origin z -0.6) and east (x to 7.5), and the rare-book room moves 1 m east with it (its corridor door too: layout.json doors_extra 4.5)
    'salotto': {'origin': [0.0, -0.6], 'size': [7.5, 7.6], 'short': 'Living room'},
    'vestibolo': {'origin': [0.5, 7.4], 'size': [3.0, 4.5], 'short': 'Vestibule'},
    'antichi': {'origin': [7.9, 0.9], 'size': [3.6, 6.5], 'short': 'Rare books'},
    'corridoio': {'origin': [3.9, 8.3], 'short': 'Corridor'},
    'corridoio-arte': {'origin': [25.1, 8.3], 'short': 'Art corridor'},
    'studio': {'origin': [23.5, 10.3], 'short': 'Study'},
}
FINISH = {'cabinet': 'cherry', 'display': 'steel', 'island': 'white', 'low': 'white', 'wall': 'white'}
GAP, MARGIN, DOOR_W = 0.02, 0.08, 0.9
ROOMS, BC, BC_ROOM, GROUP = [], {}, {}, collections.OrderedDict()   # GROUP: layout bookcase id -> rendered bookcase ids (door splits)
LAYOUT_BC = {}   # layout id -> layout record
WALL_BCS = collections.defaultdict(list)   # layout wall id -> layout bookcase ids

def short_subject(s, n=30):
    s = re.sub(r'\s*\(.*?\)\s*', ' ', s or '').strip()
    return s if len(s) <= n else s[:n - 1].rstrip(' ,;:') + '…'

def make_bc(lid, part, width, height, shelves, y0, label, lb, wall, room):
    bid = lid if part == '' else lid + '-' + part
    curio = lid == 'salotto-wood' or bool(re.search(r'cabinet of curiosities', lb.get('label') or '', re.I))   # a glazed cabinet of objects (bat skeleton, saint bust, ostrich egg, clock, photographs): drawn with those, not as 320 spines
    bc = dict(id=bid, layout_id=lid, label=label, long_label=lb.get('label') or lb.get('subject'), order=len(BC) + 1, wall=wall, x=0.0, z=0.0, rotationY=0,
              width=round(width, 3), height=round(height, 3), depth=lb.get('depth_m') or 0.32, shelves=int(shelves), kind='cabinet' if curio else (lb.get('kind') or 'wall'),
              finish='dark' if lid == 'salotto-wood' else FINISH.get(lb.get('kind') or 'wall', 'white'), subject=lb.get('subject'), subject_it=lb.get('subject_it'),
              fondazione_bay=lb.get('fondazione_bay'), confidence=lb.get('confidence'), evidence=fix_layout_text(lb.get('evidence')), source_ids=lb.get('source_ids'),
              catalog_range=lb.get('catalog_range'), est_volumes=lb.get('est_volumes'), glazed=bool(lb.get('glazed')) or curio, bays=lb.get('bays'), curio=curio,
              sections=[dict(id=bid + '-s', label=lb.get('subject') or '', topic=lb.get('subject_it'), blurb=fix_layout_text(lb.get('evidence') or ''), shelf_from=0, shelf_to=max(0, int(shelves) - 1))])
    if y0: bc['y0'] = round(y0, 3)
    if lb.get('kind') == 'island': bc['wall'] = 'free'
    BC[bid] = bc; BC_ROOM[bid] = room['id']; GROUP.setdefault(lid, []).append(bid)
    return bc

for lr in sorted(L['rooms'], key=lambda r: r['order']):
    plan = ROOM_PLAN.get(lr['id'], {})
    size = list(plan.get('size') or lr['approx_size_m'])
    room = dict(id=lr['id'], name=lr['name'], name_it=lr.get('name_it'), short_name=plan.get('short', lr['name']), order=lr['order'], blurb=lr.get('blurb') or '',
                description=lr.get('blurb') or '', size=size, origin=plan.get('origin', [0, 0]), doors=[], furniture=lr.get('furniture') or [],
                sources=lr.get('sources') or [], shelf_metres=lr.get('shelf_metres_m'), catalog_note=fix_layout_text(lr.get('catalog_note')), bookcases=[])
    if lr.get('door'):
        room['doors'].append(dict(wall=lr['door']['wall'], from_=lr['door']['offset_m'], to=lr['door']['offset_m'] + (lr['door'].get('width_m') or DOOR_W), note=lr['door'].get('note') or 'room door from layout.json'))
    for dd in lr.get('doors_extra') or []:   # further doorways (e.g. the rare-book room off the corridor's print wall)
        room['doors'].append(dict(wall=dd['wall'], from_=dd['offset_m'], to=dd['offset_m'] + (dd.get('width_m') or DOOR_W), note=dd.get('note') or 'door from layout.json doors_extra'))
    if lr.get('position_note'): room['position_note'] = lr['position_note']
    if isinstance(lr.get('windows'), list):   # layout.json windows: drawn by the page at their offsets (wall, offset_m from the wall start on the room-origin side, width_m, height_m, radiator)
        room['windows'] = [dict(wall=wd['wall'], offset=float(wd['offset_m']), width=float(wd.get('width_m') or 1.2), height=float(wd.get('height_m') or 2.5), radiator=bool(wd.get('radiator')), note=wd.get('note')) for wd in lr['windows'] if isinstance(wd, dict) and wd.get('wall') in ('N', 'E', 'S', 'W') and isinstance(wd.get('offset_m'), (int, float))]
    # check that each wall's units fit; transpose the room if that fixes it
    need = collections.Counter()
    for w in lr['walls']:
        for b in w['bookcases']: need[w['wall']] += b['width_m'] + GAP
    needx, needz = max(need['N'], need['S']) - GAP + 2 * MARGIN, max(need['E'], need['W']) - GAP + 2 * MARGIN
    if (needx > size[0] or needz > size[1]) and not plan.get('size') and needx <= size[1] and needz <= size[0]:
        size.reverse(); warn('%s: approx_size_m transposed to %s so the bookcases fit their walls' % (lr['id'], size))
    if needx > size[0] + 0.01 or needz > size[1] + 0.01:
        grown = [round(max(size[0], needx), 2), round(max(size[1], needz), 2)]
        warn('%s: room grown from %s to %s so the bookcases fit their walls' % (lr['id'], size, grown)); size[:] = grown
    ox, oz = room['origin']; w, d = size
    free_units = []
    for wl in sorted(lr['walls'], key=lambda x: x['order']):
        units = []   # (bc, width) in left-to-right order facing the wall
        for lb in sorted(wl['bookcases'], key=lambda x: x['order']):
            LAYOUT_BC[lb['id']] = lb; WALL_BCS[wl['wall_id']].append(lb['id'])
            bay = lb.get('fondazione_bay') or ''
            lab = (bay + ' · ' if bay and not bay.startswith('antichi') else '') + short_subject(lb.get('subject'))
            if lb.get('door_span_m') and lb.get('door_bay_indexes'):
                bw = lb['bay_widths_m']; di = sorted(lb['door_bay_indexes'])
                left = sum(bw[:di[0]]); door = sum(bw[di[0]:di[-1] + 1]); right = sum(bw[di[-1] + 1:])
                over_sh = int(lb.get('shelves_over_door') or 4); pitch = lb['height_m'] / lb['shelves']
                units.append((make_bc(lb['id'], '', left, lb['height_m'], lb.get('shelves_side_bays') or lb['shelves'], 0, lab + ' (left of door)', lb, wl['wall'], room), left))
                units.append((make_bc(lb['id'], 'over', door, lb['height_m'], over_sh, lb['height_m'] - over_sh * pitch, lab + ' (over the door)', lb, wl['wall'], room), door))
                units.append((make_bc(lb['id'], 'r', right, lb['height_m'], lb.get('shelves_side_bays') or lb['shelves'], 0, lab + ' (right of door)', lb, wl['wall'], room), right))
                units[-2][0]['is_door_bridge'] = True
            else:
                units.append((make_bc(lb['id'], '', lb['width_m'], lb['height_m'], lb['shelves'], 0, lab, lb, wl['wall'], room), lb['width_m']))
        if wl['wall'] == 'free': free_units.extend(u[0] for u in units); continue
        pos = MARGIN
        for bc, width in units:
            dep = bc['depth']
            pos += float(LAYOUT_BC[bc['layout_id']].get('offset_m') or 0)   # layout.json offset_m: extra run of wall left free before this unit (rare-04 starts clear of the rare-01 corner)
            sb = float(LAYOUT_BC[bc['layout_id']].get('setback_m') or 0)     # layout.json setback_m: the unit stands free that far in front of its wall, still facing the room (the salotto vitrines, 1.1 m off the display wall)
            if wl['wall'] == 'N': bc['x'], bc['z'], bc['rotationY'] = ox + pos + width / 2, oz + dep / 2 + sb, 0; along = pos
            elif wl['wall'] == 'E': bc['x'], bc['z'], bc['rotationY'] = ox + w - dep / 2 - sb, oz + pos + width / 2, -90; along = pos
            elif wl['wall'] == 'S': bc['x'], bc['z'], bc['rotationY'] = ox + w - pos - width / 2, oz + d - dep / 2 - sb, 180; along = w - pos - width
            else: bc['x'], bc['z'], bc['rotationY'] = ox + dep / 2 + sb, oz + d - pos - width / 2, 90; along = d - pos - width
            if sb: bc['setback'] = round(sb, 3)
            bc['x'] = round(bc['x'], 3); bc['z'] = round(bc['z'], 3)
            if bc.get('is_door_bridge'):
                # the doorway sits under this bridge: tell the page to cut the wall there (coordinates along the wall's own axis from the room origin)
                room['doors'] = [dd for dd in room['doors'] if dd['wall'] != wl['wall']] + [dict(wall=wl['wall'], from_=round(along + 0.05, 3), to=round(along + width - 0.05, 3), note='doorway inside bookcase ' + bc['layout_id'])]
            pos += width + GAP
            room['bookcases'].append(bc)
        # free-standing islands: rows across the room interior, facing +z (south), back-to-back pairs where the layout says so
    if free_units:
        # a free unit whose layout record carries "position" {x, z, rotationY} (room metres from the NW corner; rotationY 0 faces +z,
        # 90 faces +x, -90 faces -x, 180 faces -z) stands exactly there: the study's comb units run across the room, not along it (eco-video/studio/notes.md)
        fixed = [bc for bc in free_units if isinstance(LAYOUT_BC[bc['layout_id']].get('position'), dict)]
        for bc in fixed:
            ps = LAYOUT_BC[bc['layout_id']]['position']
            bc['x'] = round(ox + float(ps['x']), 3); bc['z'] = round(oz + float(ps['z']), 3); bc['rotationY'] = int(ps.get('rotationY') or 0); bc['fixed_position'] = True
            room['bookcases'].append(bc)
        free_units = [bc for bc in free_units if bc not in fixed]
    if free_units:
        rows = collections.OrderedDict()
        for bc in free_units: rows.setdefault(LAYOUT_BC[bc['layout_id']].get('island_of') or bc['id'], []).append(bc)
        nrows = len(rows); zs = [oz + d * (i + 1) / (nrows + 1) for i in range(nrows)]
        for (isl, group), zc in zip(rows.items(), zs):
            faces = [bc for bc in group if LAYOUT_BC[bc['layout_id']].get('face', '').upper() in ('A', 'B')] if len(group) == 2 else []
            if faces:   # one island, two faces back to back
                a, b = faces; a['x'] = b['x'] = round(ox + w / 2, 3); a['z'] = round(zc - a['depth'] / 2, 3); a['rotationY'] = 180; b['z'] = round(zc + b['depth'] / 2, 3); b['rotationY'] = 0
                room['bookcases'] += [a, b]
            else:
                tot = sum(bc['width'] for bc in group) + 1.2 * (len(group) - 1); x = ox + (w - tot) / 2
                for bc in group:
                    bc['x'] = round(x + bc['width'] / 2, 3); bc['z'] = round(zc, 3); bc['rotationY'] = 0; x += bc['width'] + 1.2
                    room['bookcases'].append(bc)
    for dd in room['doors']: dd['from'] = dd.pop('from_')
    room['door'] = room['doors'][0] if room['doors'] else None
    ROOMS.append(room)
for r in ROOMS:
    for bc in r['bookcases']: bc['order'] = r['bookcases'].index(bc) + 1

# Fondazione survey photograph of each lettered bookcase
GALLERY = {}
if os.path.exists(args.galleries):
    g = json.load(open(args.galleries, encoding='utf-8'))
    for fn in g.get('lavoro', {}).get('filenames', []):
        m = re.search(r'/\d+_(.+)\.webp$', fn)
        if not m: continue
        key = m.group(1); url = 'https://fondazioneumbertoeco.org' + fn.replace(' ', '%20')
        r = re.match(r'A-da (\d+) a (\d+)', key)
        if r:
            for i in range(int(r.group(1)), int(r.group(2)) + 1): GALLERY['A%d' % i] = url
        else: GALLERY[key] = url
for bc in BC.values():
    if bc.get('fondazione_bay') in GALLERY: bc['photo_url'] = GALLERY[bc['fondazione_bay']]
    bc['room_id'] = BC_ROOM[bc['id']]

# ------------------------------------------------------------------ slots
SIDE = 0.025
def usable_width(bc): return bc['width'] - 2 * SIDE - 0.02
SLOTS = {}    # bookcase id -> list per shelf of [book or None]
CAP = {}
RARE_W = {}
def init_slots(bc, spine_w):
    n = max(1, int(usable_width(bc) / spine_w))
    SLOTS[bc['id']] = [[None] * n for _ in range(bc['shelves'])]; CAP[bc['id']] = n
for bc in BC.values():
    if bc['kind'] == 'cabinet': continue   # sized once the rare records are counted
    init_slots(bc, args.spine_width * (1.25 if bc['fondazione_bay'] in ('E', 'H', 'F', 'G') else 1.0))   # art books are fatter

def first_free(bcid, shelf, slot):
    """Nearest free slot on the shelf around `slot`, then the following shelves, then the previous ones, then the group siblings."""
    rows = SLOTS[bcid]; n = CAP[bcid]
    shelf = max(0, min(len(rows) - 1, shelf)); slot = max(0, min(n - 1, slot))
    for dlt in range(n):
        for s in (slot + dlt, slot - dlt):
            if 0 <= s < n and rows[shelf][s] is None: return shelf, s
    for sh in list(range(shelf + 1, len(rows))) + list(range(shelf - 1, -1, -1)):
        for s in range(n):
            if rows[sh][s] is None: return sh, s
    return None
def place(bcid, shelf, slot, book):
    hit = first_free(bcid, shelf, slot)
    if hit is None:
        for sib in GROUP.get(BC[bcid]['layout_id'], []):
            if sib != bcid:
                hit = first_free(sib, shelf, slot)
                if hit: bcid = sib; break
    if hit is None: return False
    sh, s = hit; SLOTS[bcid][sh][s] = book
    book['bookcase'], book['shelf'], book['slot'], book['section'] = bcid, sh, s, bcid + '-s'
    return True
def move_book(book, bcid, shelf, slot):
    """Re-place an already placed book on another bookcase (its old slot is freed; on failure it stays where it was)."""
    ob, osh, osl = book.get('bookcase'), book.get('shelf'), book.get('slot')
    had = ob in SLOTS and osh is not None and osl is not None and SLOTS[ob][osh][osl] is book
    if had: SLOTS[ob][osh][osl] = None
    if place(bcid, shelf, slot, book): return True
    if had: SLOTS[ob][osh][osl] = book; book['bookcase'], book['shelf'], book['slot'] = ob, osh, osl
    return False
def place_spread(bcid, j, m, book):
    """j-th of m books spread evenly over the whole unit (shelf-major order)."""
    total = CAP[bcid] * len(SLOTS[bcid]); k = int(total * (j + 0.5) / max(1, m))
    return place(bcid, k // CAP[bcid], k % CAP[bcid], book)

# ------------------------------------------------------------------ experience files (optional) and objects
def load_exp(name):
    p = os.path.join(args.experience, name)
    if not os.path.exists(p): return None
    try:
        if name.endswith('.md'): return open(p, encoding='utf-8').read()
        return json.load(open(p, encoding='utf-8'))
    except Exception as e:
        warn('experience/%s unreadable: %s' % (name, e)); return None
def as_list(x, key=None):
    if x is None: return []
    if isinstance(x, dict): return x.get(key) or x.get('items') or []
    return x
EXP = dict(quotes=as_list(load_exp('quotes.json'), 'quotes'), objects=as_list(load_exp('objects.json'), 'objects'), notable=as_list(load_exp('notable_books.json'), 'books'),
           tour=load_exp('tour.json'), brief=load_exp('brief.md'))
EXP_PRESENT = {k: os.path.exists(os.path.join(args.experience, k)) for k in ('quotes.json', 'objects.json', 'notable_books.json', 'tour.json', 'brief.md')}
# layout.json notes addressed to the builder or superseded by this pipeline are not copied into meta.layout_notes (shown in About)
LAYOUT_NOTES_DROP = ('For the builder',      # schema notes for the viewer, not for readers
                     'Not modelled: piles on the piano',       # piles are modelled from the spine readers' stack frames
                     'Video evidence: only captions were available')   # frames were cut since; readings cite the second

OBJECTS = []
OBJ_KIND_RE = [(r'piano', 'piano'), (r'vetrin|vitrine|display case|glass', 'glass_case'), (r'desk|scrivania', 'desk'), (r'table|tavol', 'desk'), (r'sofa|divan|armchair|poltron|chair|sedia', 'chair'),
               (r'ladder|scala', 'ladder'), (r'lamp', 'lamp'), (r'framed|map|print|quadr|painting|poster|artwork', 'artwork'), (r'pile|stack|scatol|box', 'pile'),
               (r'lens|magnif|shell|conch|lute|recorder|flute|globe|curios|mirabil|objects|hi-fi|tv\b', 'curiosity')]
OBJ_SIZE = {'desk': [1.4, 0.75, 0.7], 'chair': [0.6, 0.85, 0.6], 'piano': [1.45, 1.2, 0.6], 'glass_case': [0.9, 2.0, 0.45], 'artwork': [0.8, 0.6, 0.04], 'curiosity': [0.4, 0.4, 0.4],
            'lamp': [0.35, 1.6, 0.35], 'ladder': [0.5, 3.2, 0.25], 'pile': [0.25, 0.3, 0.32]}
def room_of(rid):
    return next((r for r in ROOMS if r['id'] == rid), None)
def footprints(room):
    """Axis-aligned rectangles (x0, z0, x1, z1) of the bookcases and objects already in the room, with a walking margin."""
    fp = []
    for bc in room['bookcases']:
        w, d = (bc['width'], bc['depth']) if abs(bc['rotationY']) % 180 == 0 else (bc['depth'], bc['width'])
        fp.append((bc['x'] - w / 2 - 0.5, bc['z'] - d / 2 - 0.5, bc['x'] + w / 2 + 0.5, bc['z'] + d / 2 + 0.5))
    for o in OBJECTS:
        if o['room'] == room['id'] and o['kind'] != 'pile': fp.append((o['x'] - o['size'][0] / 2 - 0.4, o['z'] - o['size'][2] / 2 - 0.4, o['x'] + o['size'][0] / 2 + 0.4, o['z'] + o['size'][2] / 2 + 0.4))
    return fp
def rect_dist(x, z, r):
    dx = max(r[0] - x, 0, x - r[2]); dz = max(r[1] - z, 0, z - r[3])
    return math.hypot(dx, dz) if (dx or dz) else -1
def free_spot(room, prefer=None):
    """A free point of the room interior (metres, world): the grid point farthest from bookcases and other objects, or near `prefer`."""
    ox, oz = room['origin']; w, d = room['size']; fp = footprints(room)
    best, bs = None, -1e9
    x = ox + 0.6
    while x < ox + w - 0.6:
        z = oz + 0.6
        while z < oz + d - 0.6:
            dist = min([rect_dist(x, z, r) for r in fp] or [9])
            score = min(dist, 1.5) - (0.6 * math.hypot(x - prefer[0], z - prefer[1]) if prefer else 0)
            if dist >= 0 and score > bs: best, bs = (round(x, 2), round(z, 2)), score
            z += 0.4
        x += 0.4
    return best or (round(ox + w / 2, 2), round(oz + d / 2, 2))
def add_object(o, auto=False):
    room = room_of(o.get('room')) or room_of(ALIAS_ROOM.get(fold(o.get('room') or ''), ''))
    if room is None: warn('object %r: unknown room %r' % (o.get('label'), o.get('room'))); return None
    kind = o.get('kind') or next((k for rx, k in OBJ_KIND_RE if re.search(rx, fold(o.get('label') or ''))), 'curiosity')
    ox, oz = room['origin']
    pos = o.get('position')
    if isinstance(pos, dict): pos = [pos.get('x'), pos.get('z')]
    if pos and len(pos) == 2 and all(isinstance(v, (int, float)) for v in pos): x, z = round(ox + pos[0], 3), round(oz + pos[1], 3); placed = 'given'
    else:
        pref = None
        if re.search(r'near the e wall|east wall', fold(o.get('label') or '')): pref = (ox + room['size'][0] - 1.2, oz + room['size'][1] / 2)
        x, z = free_spot(room, pref); placed = 'auto'
    obj = dict(id=o.get('id') or ('obj:%s:%s' % (room['id'], slug(o.get('label') or kind, 24))), room=room['id'], kind=kind, x=x, z=z, rotation=o.get('rotation') or 0,
               base_y=o.get('base_y') or 0, size=o.get('size') or OBJ_SIZE.get(kind, [0.5, 0.5, 0.5]), label=o.get('label') or kind, description=o.get('description'),
               source=o.get('source'), source_url=o.get('source_url'), video_id=o.get('video_id'), timestamp_s=o.get('timestamp_s'), confidence=o.get('confidence') or ('low' if auto else 'medium'),
               placement='given' if placed == 'given' else 'inferred', auto=auto, quotes=o.get('quotes') or [])
    if obj['video_id'] and not obj['source_url']: obj['source_url'] = yt_url(obj['video_id'], obj['timestamp_s'])
    n = 2
    while any(x['id'] == obj['id'] for x in OBJECTS): obj['id'] = obj['id'].rsplit('~', 1)[0] + '~%d' % n; n += 1
    OBJECTS.append(obj); return obj
ALIAS_ROOM = {}   # filled once the wall map is loaded

# ------------------------------------------------------------------ mapping tables
WM = json.load(open(args.wall_map, encoding='utf-8'))
SM = json.load(open(args.subject_map, encoding='utf-8'))
ROOM_IDS = {r['id'] for r in ROOMS}
def expand(v, depth=0):
    """A wall-map value -> list of rendered bookcase ids (a layout bookcase id, a list, a Fondazione letter, a wall id, a room id)."""
    if v is None or depth > 4: return []
    if isinstance(v, list): return [b for x in v for b in expand(x, depth + 1)]
    v = str(v).strip()
    if v in GROUP: return list(GROUP[v])
    if v in BC: return [v]
    if v in WM.get('letters', {}) and depth < 3: return expand(WM['letters'][v], depth + 1)
    if v in WM.get('wall_default', {}) and depth < 3: return expand(WM['wall_default'][v], depth + 1)
    if v in WALL_BCS: return [b for lid in WALL_BCS[v] for b in GROUP[lid]]
    if v in WM.get('room_default', {}) and depth < 3: return expand(WM['room_default'][v], depth + 1)
    if v in ROOM_IDS: return [bc['id'] for bc in next(r for r in ROOMS if r['id'] == v)['bookcases']]
    return []
ALIAS = {fold(k).strip(): v for k, v in WM.get('aliases', {}).items()}
PATTERNS = [(re.compile(rx, re.I), tgt) for rx, tgt in WM.get('patterns', [])]
LETTER_RE = re.compile(r"bookcase\s*['‘’\"]?([A-Z](?:-[AB]|[abc])?)['‘’\"]?(?![A-Za-z])(?:,\s*(?:shelves|bays)\s*(\d+)\s*-\s*(\d+))?", re.I)   # the letter must end there ("bookcase and adjoining table" is not bookcase A)
UNRESOLVED = collections.Counter()
# shelf labels visible in the frames (the Fondazione's hand-written call tags 'Q4', 'Q4.9', 'L11.5', 'A 13') and the wall map's own label rules
LABEL_PATTERNS = [(re.compile(p[0], re.I), p[1], (p[2] if len(p) > 2 else 'bookcase'), (p[3] if len(p) > 3 else p[0])) for p in WM.get('label_patterns', []) if isinstance(p, list) and len(p) >= 2]
SHELF_TAG_RE = re.compile(r"(?<![A-Za-z0-9.])([A-S])\s?(\d{1,2})(?:\.\d{1,2})?(?![A-Za-z0-9])")
WORKING_ROOMS = {'studio', 'corridoio', 'corridoio-arte', 'vestibolo', 'salotto'}   # where the Fondazione letters apply
LABEL_HITS = collections.Counter()
def tag_targets(letter, bay):
    """A Fondazione call tag -> rendered bookcase ids: A + bay -> corridor bay; L + bay -> L1-4 / L5-7 / L8-12; other letters -> the lettered unit(s)."""
    if letter == 'A': return ['corridor-%02d' % bay] if 'corridor-%02d' % bay in BC else expand('A')
    if letter == 'L': return expand('L1-4' if bay <= 4 else 'L5-7' if bay <= 7 else 'L8-12')
    return expand(letter)
QUOTE_OPEN_RE = re.compile(r"""["'\u201c\u2018\u00ab][^"'\u201d\u2019\u00bb]{0,12}$"""); QUOTE_CLOSE_RE = re.compile(r"""^[^"'\u201d\u2019\u00bb]{0,12}["'\u201d\u2019\u00bb]""")
def tag_like(m, text):
    """Is the text a label pattern matched something read in the frame (a call tag such as Q4/Q5 or L11.5, a tab lettered in capitals such as
    ECO IBERICI, or words the reader quoted from a shelf or a spine, 'Il Pensiero Occidentale') rather than the pass's own description of the wall?"""
    span = m.group(0)
    if SHELF_TAG_RE.search(span): return True
    if span.isupper() and any(ch.isalpha() for ch in span): return True
    return bool(QUOTE_OPEN_RE.search(text[:m.start()]) and QUOTE_CLOSE_RE.match(text[m.end():]))
def label_target(rec):
    """-> (targets, level, note) from the shelf labels a reader recorded in wall_name / wall_id: the wall map's label_patterns first (level
    'bookcase' = seen, 'label' = the label names a subject and the bay is inferred, or 'context' = the pattern is the pass's own name for the wall, no tag:
    the bookcase is inferred from the shot's context), then the generic call tags. Only for the working-library rooms."""
    room = rec.get('_room') or ALIAS_ROOM.get(fold(rec.get('room_id') or '').strip()) or (fold(rec.get('room_id') or '').strip() if fold(rec.get('room_id') or '').strip() in ROOM_IDS else None)
    if room not in WORKING_ROOMS: return None
    text = ' '.join(x for x in (rec.get('wall_id') or '', rec.get('wall_name') or '') if x)
    for rx, tgt, level, name in LABEL_PATTERNS:
        m = rx.search(text)
        if not m: continue
        out, lvl = expand2(tgt)
        if not out: continue
        if level == 'context' or (level not in ('label',) and not tag_like(m, text)):   # the pass's own name for a wall ('Own-works library wall with rolling ladder') is not a tag in the frame: the bookcase is taken from the shot's context, the placement inferred, the tier a guess (the Greek Prague Cemetery read in the Louisiana clip was certain on it)
            if level != 'context': warn("label pattern %r matched %r in the reader's wall name %r, which is no tag: placed by the shot's context" % (name, m.group(0), text[:80]))
            LABEL_HITS['context: ' + (name if level == 'context' else m.group(0))] += 1; return out, 'context', None
        LABEL_HITS[name] += 1; return out, ('label' if level == 'label' else lvl), "shelf label '%s'" % m.group(0)
    tags = [(m.group(1), int(m.group(2)), m.group(0)) for m in SHELF_TAG_RE.finditer(text)]
    tags = [t for t in tags if t[0] in WM.get('letters', {}) and not (t[0] == 'A' and t[1] > 25)]
    if tags:
        out = []
        for letter, bay, _ in tags:
            for bc in tag_targets(letter, bay):
                if bc not in out and BC_ROOM.get(bc) == room: out.append(bc)
        if out: LABEL_HITS['call tag %s' % tags[0][0]] += 1; return out, 'bookcase', 'call tag%s %s' % ('s' if len(tags) > 1 else '', ', '.join(sorted({t[2].strip() for t in tags})))
    return None
def level_of(v):
    """How specific a wall-map value is: 'bookcase' (one unit or a listed set of units), 'wall', 'room' or 'fallback'."""
    if isinstance(v, list): return 'bookcase'
    v = str(v).strip()
    if v == '@fallback': return 'fallback'
    if v in GROUP or v in BC or v in WM.get('letters', {}): return 'bookcase'
    if v in WALL_BCS or v in WM.get('wall_default', {}): return 'wall'
    return 'room'
def expand2(v):
    if str(v).strip() == '@fallback': return expand(SM.get('fallback')), 'fallback'
    if str(v).strip() == '@pile': return ['@pile'], 'pile'
    if str(v).strip() == '@subject': return ['@subject'], 'subject'
    if str(v).strip() == '@exclude': return ['@exclude'], 'exclude'
    return expand(v), level_of(v)
def resolve(rec):
    """-> (candidate rendered bookcase ids, level) for a spine reading; ([], None) when nothing matches.
    level 'bookcase' / 'wall' -> placement seen; 'room' / 'fallback' -> placement inferred."""
    for k in ('build_bookcase_id', 'bookcase_id', 'bookcase'):
        if rec.get(k):
            out = expand(rec[k])
            if out: return out, 'bookcase'
    wn = rec.get('wall_name') or ''
    m = LETTER_RE.search(wn)
    if m:
        letter = m.group(1).upper() if len(m.group(1)) == 1 else m.group(1)
        if letter == 'A' and m.group(2): out = ['corridor-%02d' % i for i in range(int(m.group(2)), int(m.group(3)) + 1) if 'corridor-%02d' % i in BC]
        elif m.group(2): out = expand('%s%s-%s' % (letter, m.group(2), m.group(3))) or expand(letter) or expand(m.group(1))
        else: out = expand(letter) or expand(m.group(1))
        if out: return out, 'bookcase'
    m = re.search(r'\b(L\d+-\d+|M-[AB]|N[abc]|O[ab]|antichi-(?:SX|DX)|rare-0[123])\b', wn)
    if m:
        out = expand(m.group(1))
        if out: return out, 'bookcase'
    lab = label_target(rec)   # shelf labels visible in the frame (call tags Q4/Q5, L11.5 ...; wall_map label_patterns) beat the room-level fallback
    if lab:
        rec['_label_note'] = lab[2]; return lab[0], lab[1]
    for k in ('wall_id', 'room_id'):
        v = rec.get(k)
        if not v: continue
        key = fold(v).strip()
        if key in ALIAS:
            if ALIAS[key] is None: continue
            out, lvl = expand2(ALIAS[key])
            if out: return out, lvl
        out, lvl = expand2(v)
        if out: return out, lvl
    for text in (rec.get('wall_id') or '', wn):
        for rx, tgt in PATTERNS:
            if rx.search(text):
                out, lvl = expand2(tgt)
                if out: return out, lvl
    UNRESOLVED[(rec.get('room_id'), rec.get('wall_id'), wn[:60])] += 1
    return [], None

for k, v in ALIAS.items():
    if isinstance(v, str) and v in ROOM_IDS: ALIAS_ROOM[k] = v
# furniture named in layout.json becomes labelled objects (positions guessed) only where the film inventory says nothing; objects.json adds or overrides by id
VO = None
if os.path.exists(args.video_objects):
    try: VO = json.load(open(args.video_objects, encoding='utf-8'))
    except Exception as e: warn('objects_from_video.json unreadable: %s' % e)
VO_ROOMS = {s.get('room_id') for s in (VO or {}).get('shots') or []}
for lr in L['rooms']:
    if lr['id'] in VO_ROOMS: continue
    for item in lr.get('furniture') or []:
        add_object(dict(room=lr['id'], label=item, description=item + ' (furniture listed in eco-video/layout.json for this room; position guessed)', source='layout.json furniture list'), auto=True)

# ------------------------------------------------------------------ videos
VIDEOS = {}
if os.path.exists(args.videos):
    for v in json.load(open(args.videos, encoding='utf-8')): VIDEOS[v['video_id']] = v
else:
    for p in glob.glob(os.path.join(VIDEO_DIR, 'meta', '*.info.json')):
        try: m = json.load(open(p, encoding='utf-8'))
        except Exception: continue
        VIDEOS[m.get('id')] = dict(video_id=m.get('id'), title=m.get('title'), uploader=m.get('uploader') or m.get('channel'), upload_date=m.get('upload_date'),
                                   duration_s=m.get('duration'), url='https://www.youtube.com/watch?v=%s' % m.get('id'))
def yt_url(vid, t): return 'https://www.youtube.com/watch?v=%s&t=%ds' % (vid, int(round(t or 0)))
def video_offset(vid): return float((VIDEOS.get(vid) or {}).get('timestamp_offset_s') or 0)
def corrected_ts(vid, raw):
    """videos.json may carry a per-video timestamp_offset_s (the frame clock vs the YouTube clock): the corrected value is used everywhere."""
    if raw is None or not isinstance(raw, (int, float)): return None
    return int(round(raw + video_offset(vid)))

# ------------------------------------------------------------------ objects inventoried from the footage (objects_from_video.json through objects_map_eco.json)
OM = {'rules': []}
if os.path.exists(args.objects_map):
    try: OM = json.load(open(args.objects_map, encoding='utf-8'))
    except Exception as e: warn('objects map unreadable: %s' % e)
OM_RULES = [dict(r, _match=re.compile(r['match'], re.I) if r.get('match') else None, _hint=re.compile(r['hint'], re.I) if r.get('hint') else None) for r in OM.get('rules', []) if isinstance(r, dict)]
WALL2OBJ = {}                                   # consolidated wall id (without the video prefix) -> [(object id, raw_from, raw_to, defer)] holding its pile readings
SEEN_NOTES = collections.defaultdict(list)      # bookcase id -> what the film showed on / in it
ON_CAMERA = set()                               # bookcase ids with direct film evidence
BC_ID_PAREN_RE = re.compile(r"\s*\(([A-Za-z0-9]+(?:-[A-Za-z0-9]+)+)\)")
def strip_bc_id(text):
    """Reader-facing text without a parenthesised bookcase id of the layout ('Three glass vitrines (salotto-vetrine)' -> 'Three glass vitrines')."""
    if not text: return text
    return BC_ID_PAREN_RE.sub(lambda mm: '' if mm.group(1) in BC else mm.group(0), text).strip()
VO_STATS = collections.Counter()
VO_AUTO = []                                    # objects placed from their position hint alone (to check)
WALL_ROT = {'N': 0, 'S': 180, 'E': -90, 'W': 90}   # rotation that puts an object's back against that wall (rotationY 0 faces +z)
def wall_len(room, wall): return room['size'][0] if wall in ('N', 'S') else room['size'][1]
def wall_point(room, wall, at, dist):
    """World point `dist` m inside the room from `wall`, `at` m along it (N/S: from the west end; E/W: from the north end)."""
    ox, oz = room['origin']; w, d = room['size']
    if wall == 'N': return ox + at, oz + dist
    if wall == 'S': return ox + at, oz + d - dist
    if wall == 'E': return ox + w - dist, oz + at
    return ox + dist, oz + at
def wall_occupied(room, wall):
    ox, oz = room['origin']; iv = []
    for bc in room['bookcases']:
        if bc['wall'] != wall: continue
        iv.append((bc['x'] - bc['width'] / 2 - ox, bc['x'] + bc['width'] / 2 - ox) if wall in ('N', 'S') else (bc['z'] - bc['width'] / 2 - oz, bc['z'] + bc['width'] / 2 - oz))
    for dd in room['doors']:
        if dd['wall'] == wall: iv.append((dd.get('from', dd.get('from_', 0)) - 0.1, dd['to'] + 0.1))
    for wd in room.get('windows') or []:   # a listed window is not free wall for a framed print (the study's W wall window, with the prints beside the door)
        if wd['wall'] == wall: iv.append((wd['offset'] - 0.05, wd['offset'] + wd['width'] + 0.05))
    return sorted(iv)
WALL_CURSOR = collections.defaultdict(float)
def free_wall_at(room, wall, width):
    """Centre (m along the wall) of the next free stretch of `wall` at least `width` long, scanning from its start; None when the wall is full."""
    occ = wall_occupied(room, wall); L_ = wall_len(room, wall); x = max(0.3, WALL_CURSOR[(room['id'], wall)])
    while x + width <= L_ - 0.3:
        clash = next((b for a, b in occ if a < x + width and b > x), None)
        if clash is None: WALL_CURSOR[(room['id'], wall)] = x + width + 0.35; return x + width / 2
        x = clash + 0.15
    return None
def bc_front(bcid, dist, along=0.0):
    """World point `dist` m in front of bookcase `bcid`'s face, `along` m from its centre towards its right."""
    bc = BC[bcid]; a = math.radians(bc['rotationY'])
    return bc['x'] + math.sin(a) * (bc['depth'] / 2 + dist) + math.cos(a) * along, bc['z'] + math.cos(a) * (bc['depth'] / 2 + dist) - math.sin(a) * along
def bc_ref(key):
    if key in BC: return key
    lst = GROUP.get(key) or expand(key)
    return lst[0] if lst else None
def obj_by_id(oid): return next((o for o in OBJECTS if o['id'] == oid), None)
def fit_on_support(o, r, room):
    """An object anchored `on_top` of another object or a bookcase (same rotation as its support) is shrunk and shifted, in the
    support's own frame, so its footprint lies inside the support's top; the generator report says when it had to."""
    an = (r or {}).get('anchor') or {}
    if not an.get('on_top') or 'rotation' in (r or {}): return
    if an.get('object'):
        s = obj_by_id(an['object'])
        if s is None: return
        sx, sz, srot, sw, sd = s['x'], s['z'], s.get('rotation') or 0, s['size'][0], s['size'][2]
    elif an.get('bookcase'):
        bcid = bc_ref(an['bookcase'])
        if not bcid: return
        bc = BC[bcid]; sx, sz, srot, sw, sd = bc['x'], bc['z'], bc['rotationY'], bc['width'], bc['depth']
    else: return
    if (o.get('rotation') or 0) % 360 != srot % 360: return
    a = math.radians(srot); dx = (o['x'] - sx) * math.cos(a) - (o['z'] - sz) * math.sin(a); dz = (o['x'] - sx) * math.sin(a) + (o['z'] - sz) * math.cos(a)   # the object's offset in the support's frame
    w, d = o['size'][0], o['size'][2]; w2, d2 = min(w, sw - 0.04), min(d, sd - 0.04); moved = False
    if w2 < w - 0.001 or d2 < d - 0.001: o['size'] = [round(w2, 3), o['size'][1], round(d2, 3)]; moved = True
    lim_x, lim_z = max(0.0, sw / 2 - w2 / 2 - 0.02), max(0.0, sd / 2 - d2 / 2 - 0.02)
    dx2, dz2 = max(-lim_x, min(lim_x, dx)), max(-lim_z, min(lim_z, dz))
    if abs(dx2 - dx) > 0.005 or abs(dz2 - dz) > 0.005:   # a move under half a centimetre is the arithmetic's own noise (an offset of 0.00 read as -0.00), not a piece kept inside its support
        o['x'] = round(sx + dx2 * math.cos(a) + dz2 * math.sin(a), 3); o['z'] = round(sz - dx2 * math.sin(a) + dz2 * math.cos(a), 3); moved = True
    if moved:
        o['fitted'] = True; msg = 'objects map: %s kept inside the top of its support (%s): size %s, offset %.2f/%.2f -> %.2f/%.2f' % (o['id'], an.get('object') or an.get('bookcase'), o['size'], dx, dz, dx2, dz2)
        if abs(dx2 - dx) <= w / 2 and abs(dz2 - dz) <= d / 2 and o['size'][0] == w and o['size'][2] == d: o['fit_note'] = 'drawn at the edge of its support: the anchor put it %.2f m past it' % max(abs(dx2 - dx), abs(dz2 - dz)); print('note: ' + msg)   # a pile placed by a fraction of the lid's length that lands a few centimetres past the edge stands at the edge; the data says so, the page does not
        else: warn(msg)
def resolve_anchor(room, an, size):
    """-> (x, z, base_y, rotation, note) in world metres for an objects_map anchor, or None."""
    if not isinstance(an, dict): return None
    if an.get('bookcase'):
        bcid = bc_ref(an['bookcase'])
        if not bcid: warn('objects map: unknown bookcase %r in an anchor' % an['bookcase']); return None
        bc = BC[bcid]; ON_CAMERA.add(bcid)
        if an.get('on_top'):
            x, z = bc_front(bcid, -bc['depth'] / 2, an.get('along') or 0); return x, z, bc['height'] + 0.02, bc['rotationY'], 'on top of ' + bc['label']
        x, z = bc_front(bcid, (an.get('dist') or 0.6) + size[2] / 2, an.get('along') or 0)
        return x, z, an.get('base_y') or 0, (bc['rotationY'] + 180) % 360 if an.get('face') != 'away' else bc['rotationY'], 'in front of ' + bc['label']
    if an.get('object'):
        o = obj_by_id(an['object'])
        if o is None: warn('objects map: anchor object %r not (yet) defined' % an['object']); return None
        dx, dz = (an.get('offset') or [0, 0]); a = math.radians(o.get('rotation') or 0)
        if isinstance(an.get('along_frac'), (int, float)): dx += (float(an['along_frac']) - 0.5) * o['size'][0]   # 0 = the object's left end as seen from its front, 1 = its right end ("on the lid at 0.35 of its length")
        x = o['x'] + dx * math.cos(a) + dz * math.sin(a); z = o['z'] - dx * math.sin(a) + dz * math.cos(a)
        by = (o.get('base_y') or 0) + o['size'][1] + 0.01 if an.get('on_top') else (an.get('base_y') or 0)
        return x, z, by, o.get('rotation') or 0, ('on ' if an.get('on_top') else 'by ') + o['label']
    if an.get('wall'):
        wall = an['wall']
        if wall == 'auto' or an.get('auto'):
            for wl in ([wall] if wall in WALL_ROT else []) + ['N', 'W', 'E', 'S']:
                at = free_wall_at(room, wl, size[0])
                if at is not None: wall = wl; break
            else: return None
        else: at = an.get('at') if an.get('at') is not None else wall_len(room, wall) / 2
        x, z = wall_point(room, wall, at, (an.get('dist') or 0.03) + size[2] / 2)
        return x, z, an.get('base_y') or 0, WALL_ROT[wall], 'on the %s wall' % wall
    return None
KIND_ALIAS = {'sofa': 'sofa', 'other': 'other', 'door': None, 'window': None, 'rug': None}
def hint_position(room, kind, hint, size):
    """A world position guessed from a reader's position hint: a bookcase it names, a wall it names, the centre, or a free spot."""
    h = fold(hint)
    for tok in re.findall(r'\b([A-S](?:\d{1,2})?(?:-\d{1,2})?)\b', hint) + re.findall(r'\b(rare-0\d|corridor-\d\d|study-[A-Za-z0-9-]+|vest-[A-D]|salotto-[a-z]+)\b', hint):
        lst = expand(tok) if tok not in BC else [tok]
        lst = [b for b in lst if BC_ROOM.get(b) == room['id']]
        if lst:
            bcid = lst[len(lst) // 2]; ON_CAMERA.add(bcid)
            if kind == 'artwork': x, z = bc_front(bcid, 0.05); return x, z, 2.4, BC[bcid]['rotationY'], 'above ' + BC[bcid]['label']
            x, z = bc_front(bcid, 0.6 + size[2] / 2); return x, z, 0, (BC[bcid]['rotationY'] + 180) % 360, 'in front of ' + BC[bcid]['label']
    wall = None
    if re.search(r'left wall|left-hand wall', h): wall = 'N' if room['id'].startswith('corr') else 'W'
    elif re.search(r'right wall|right-hand wall', h): wall = 'S' if room['id'].startswith('corr') else 'E'
    elif re.search(r'end wall|far end|corridor end', h): wall = 'E'
    elif re.search(r'window|balcony', h): wall = 'S' if room['id'] == 'studio' else 'N'
    elif re.search(r'\bdoor\b', h) and room['doors']: wall = room['doors'][0]['wall']
    if kind == 'artwork':
        for wl in ([wall] if wall else []) + ['N', 'W', 'E', 'S']:
            at = free_wall_at(room, wl, size[0])
            if at is not None: x, z = wall_point(room, wl, at, 0.03 + size[2] / 2); return x, z, 0, WALL_ROT[wl], 'on the %s wall (hint: %s)' % (wl, hint[:40])
        x, z = free_spot(room); return x, z, 0, 0, 'no free wall; standing (hint: %s)' % hint[:40]
    if wall:
        at = free_wall_at(room, wall, size[0]) or wall_len(room, wall) / 2
        x, z = wall_point(room, wall, at, 0.5 + size[2] / 2); return x, z, 0, WALL_ROT[wall], 'by the %s wall (hint: %s)' % (wall, hint[:40])
    ox, oz = room['origin']
    if re.search(r'cent|middle', h): x, z = free_spot(room, (ox + room['size'][0] / 2, oz + room['size'][1] / 2)); return x, z, 0, 0, 'centre (hint: %s)' % hint[:40]
    x, z = free_spot(room); return x, z, 0, 0, 'free spot (hint: %s)' % hint[:40]
def rule_for(room, kind, label, hint, strict_kind=True):
    for r in OM_RULES:
        if r.get('room') not in ('*', room['id']): continue
        if r.get('kind') and kind and r['kind'] != kind:
            if strict_kind or r['_match'] is None: continue   # a rule for another kind only takes the thing when its label regex says so
        if r['_match'] is None and r['_hint'] is None: continue
        if r['_match'] is not None and not r['_match'].search(label): continue
        if r['_hint'] is not None and not r['_hint'].search(hint): continue
        return r
    return None
MERGED = collections.OrderedDict(); N_EACH = [0]
ROUTE_NOTES = []          # objects.json records that describe Eco's route rather than a thing
EXP_OBJ_STATS = collections.Counter()
def ingest(room, kind, label, hint, sight, description=None, titles=None, count=None, prefer=False, size=None, bookcases=None, source_name='video', rule=None):
    """One inventoried thing -> the merged record its objects_map rule (or an automatic key) names. `prefer` (objects.json) wins on label and description."""
    r = rule if rule is not None else (rule_for(room, kind, label, hint) or rule_for(room, kind, label, hint, strict_kind=False))
    stats = EXP_OBJ_STATS if source_name == 'experience' else VO_STATS
    if r is not None and r.get('skip'): stats['skipped_by_rule'] += 1; return None
    if r is not None and r.get('attach'):
        for tgt in (r['attach'] if isinstance(r['attach'], list) else [r['attach']]):
            bcid = bc_ref(tgt)
            if bcid: SEEN_NOTES[bcid].append(dict(sight, description=description or sight.get('description'))); ON_CAMERA.add(bcid); stats['attached_to_bookcases'] += 1
            else: warn('objects map: attach target %r unknown' % tgt)
        return None
    if r is None and bookcases and kind in ('attach', 'curiosity', 'other') and source_name == 'experience':
        for bcid in bookcases: SEEN_NOTES[bcid].append(dict(sight, description=description)); ON_CAMERA.add(bcid); stats['attached_to_bookcases'] += 1
        return None
    if r is not None and r.get('each'): key = 'each:%d' % N_EACH[0]; N_EACH[0] += 1
    elif r is not None: key = r.get('id') or ('rule:%d' % OM_RULES.index(r))
    else: key = 'auto:%s:%s:%s' % (room['id'], kind, ' '.join(sorted(tokens(label))))
    m = MERGED.get(key)
    if m is None:
        m = MERGED[key] = dict(room=room, kind=(r.get('kind') if r else None) or kind, label=(r.get('label') if r else None) or label, rule=r, labels=[], descriptions=[], sightings=[], titles=[], count=0, hints=[], size=None, bookcases=[], sources=set(), prefer=False)
    if prefer and not m['prefer']:
        m['prefer'] = True
        if not (r and r.get('label')): m['label'] = label
        if description: m['descriptions'].insert(0, description)
    elif description and description not in m['descriptions']: m['descriptions'].append(description)
    m['labels'].append(label); m['hints'].append(hint or ''); m['sightings'].append(sight); m['sources'].add(source_name)
    if count: m['count'] = max(m['count'], int(count))
    if size and (prefer or not m['size']): m['size'] = size
    for b in bookcases or []:
        if b not in m['bookcases']: m['bookcases'].append(b)
    for t in titles or []: m['titles'].append(t)
    stats['ingested'] += 1
    return m
SIZE_RE = re.compile(r'(\d+(?:[.,]\d+)?)\s*x\s*(\d+(?:[.,]\d+)?)(?:\s*x\s*(\d+(?:[.,]\d+)?))?\s*m\b')
def note_size(note, kind):
    """'2.4 x 1.0 x 0.78 m' -> [w, h, d] for the page (three numbers read as width x depth x height; two as width x height for artworks, width x depth otherwise)."""
    m = SIZE_RE.search(note or '')
    if not m: return None
    a, b, c = (float(v.replace(',', '.')) if v else None for v in m.groups())
    if c is not None: return [a, c, b]
    if kind == 'artwork': return [a, b, 0.04]
    base = OBJ_SIZE.get(kind) or [0.6, 0.8, 0.5]
    return [a, base[1], b]
def exp_kind(o):
    k = o.get('kind'); item = fold(o.get('item') or '')
    if k in ('room', 'corridor'): return 'room'
    if re.search(r'^eco |girl on roller|interview setting|reconstruction|playing the recorder', item): return 'route'
    if k in ('fixture', 'rare-book-room-fixture'):
        if re.search(r'pendant|ceiling|window|terrace|floor and ceiling|balcony onto|spotlight', item): return 'roomnote'
        if re.search(r'lamp', item): return 'lamp'
        if re.search(r'door', item): return 'attach'
        if re.search(r'bookcase|cabinet', item): return 'attach'
        if re.search(r'table', item): return 'desk'
        if re.search(r'armchair|chair', item): return 'chair'
        if re.search(r'lens|tray|glass case|music stand|recorder', item): return 'curiosity'
        return 'other'
    if k == 'artwork': return 'artwork'
    if k == 'pile': return 'pile'
    if k == 'furniture':
        if re.search(r'sofa', item): return 'sofa'
        if re.search(r'coat|television|\btv\b|chest|cabinet', item): return 'other'
        return next((kk for rx, kk in OBJ_KIND_RE if re.search(rx, item)), 'other')
    if o.get('bookcase'): return 'attach'
    return next((kk for rx, kk in OBJ_KIND_RE if re.search(rx, item)), 'curiosity')
def exp_sights(o):
    out = []
    for s in [o.get('source')] + list(o.get('also_seen') or []):
        if not isinstance(s, dict): continue
        vid = s.get('video_id'); raw = s.get('timestamp_s'); ts = corrected_ts(vid, raw) if vid and isinstance(raw, (int, float)) else None
        out.append(dict(kind='video' if vid else 'photo', video_id=vid, timestamp_s=ts, timestamp_raw_s=raw, time=hms(ts) if ts is not None else None, url=s.get('url') or (yt_url(vid, ts) if vid and ts is not None else None),
                        frame=os.path.basename(s.get('image') or '') or None, image=s.get('image'), label=o.get('item'), description=None, hint=o.get('modelling_note') or '',
                        path=image_path(s.get('image')), bbox=s.get('bbox') or s.get('crop') or o.get('bbox') or o.get('crop'), prefer=True))
    return out
def image_path(image):
    """An experience `image` value -> an existing file: absolute paths as given, `frames/<file>` under the experience folder, a bare frame name under eco-video/frames/<video>/."""
    if not image or not isinstance(image, str): return None
    cands = [image] if os.path.isabs(image) else [os.path.join(args.experience, image), os.path.join(SRC_DIR, image), os.path.join(VIDEO_DIR, image)]
    return next((p for p in cands if os.path.exists(p)), None)
def frame_path(vid, frame):
    """A frame basename of a video -> its file under eco-video/frames/<video id>/ (or the experience frames folder), when it exists."""
    if not frame: return None
    for p in ([os.path.join(VIDEO_DIR, 'frames', vid, frame)] if vid else []) + [os.path.join(args.experience, 'frames', frame)]:
        if os.path.exists(p): return p
    return None
def apply_experience_objects():
    """eco-sources/experience/objects.json: 95 records (rooms, fixtures, furniture, artworks, piles, objects) with a modelling note each; preferred over the film inventory where both name the same thing."""
    for o in EXP['objects']:
        if not isinstance(o, dict) or not (o.get('item') or o.get('label')): continue
        if o.get('position') or o.get('x') is not None:   # a hand-placed object in the generator's own schema: taken as is
            prev = next((x for x in OBJECTS if o.get('id') and x['id'] == o['id']), None)
            if prev: OBJECTS.remove(prev)
            add_object(dict(o, label=o.get('label') or o.get('item'))); EXP_OBJ_STATS['placed_directly'] += 1; continue
        EXP_OBJ_STATS['records'] += 1
        room = room_of(o.get('room')) or room_of(ALIAS_ROOM.get(fold(o.get('room') or ''), ''))
        if room is None: EXP_OBJ_STATS['unknown_room'] += 1; continue
        kind = exp_kind(o); item = o.get('item') or o.get('label'); note = o.get('modelling_note') or ''
        sights = exp_sights(o); first = sights[0] if sights else dict(kind='photo', video_id=None, timestamp_s=None, timestamp_raw_s=None, time=None, url=None, frame=None, image=None, label=item, description=None, hint=note)
        bcs = [b for b in (bc_ref(x.strip()) for x in re.split(r'\s*/\s*|\s*,\s*', o.get('bookcase') or '') if x.strip()) if b] if o.get('bookcase') else []
        if kind == 'route': ROUTE_NOTES.append(dict(id=o.get('id'), item=item, description=o.get('description'), note=note, url=first['url'], video_id=first['video_id'], timestamp_s=first['timestamp_s'])); continue
        if kind in ('room', 'roomnote'):
            room.setdefault('film_notes', []).append(dict(id=o.get('id'), item=strip_bc_id(item), description=strip_bc_id(o.get('description')), note=note, url=first['url'], video_id=first['video_id'], timestamp_s=first['timestamp_s'], image=first.get('image'), confidence=o.get('confidence')))
            for b in bcs: ON_CAMERA.add(b)
            EXP_OBJ_STATS['room_notes'] += 1; continue
        if kind == 'attach' and not bcs: kind = 'other'
        for s in sights: s['description'] = o.get('description'); s['exp_id'] = o.get('id'); s['confidence'] = o.get('confidence')
        size = note_size(note, kind)
        m = ingest(room, kind, item, note + ' ' + (o.get('description') or ''), first, description=o.get('description'), count=None, prefer=True, size=size, bookcases=bcs, source_name='experience')
        if m is not None:
            m['exp_ids'] = m.get('exp_ids', []) + [o.get('id')]; m['confidence_exp'] = o.get('confidence'); m['sightings'] += sights[1:]
def apply_video_objects():
    if not VO: return
    vid = VO.get('video_id')
    for s in VO.get('shots') or []:
        rid = s.get('room_id'); room = room_of(rid) or room_of(ALIAS_ROOM.get(fold(rid or ''), ''))
        for o in s.get('objects') or []:
            VO_STATS['objects'] += 1
            kind = (o.get('kind') or 'other').lower(); label = o.get('label') or ''; hint = o.get('position_hint') or ''
            if kind in KIND_ALIAS and KIND_ALIAS[kind] is None: VO_STATS['skipped_fixture'] += 1; continue
            if room is None: VO_STATS['skipped_other_room'] += 1; continue
            raw = o.get('timestamp_s'); ts = corrected_ts(vid, raw) if isinstance(raw, (int, float)) else None
            sight = dict(kind='video', video_id=vid, timestamp_s=ts, timestamp_raw_s=raw, time=hms(ts) if ts is not None else None, url=yt_url(vid, ts) if ts is not None else None,
                         frame=os.path.basename(o.get('best_frame') or '') or None, label=label, description=o.get('description'), hint=hint, count=o.get('count'), shot_room_confidence=s.get('room_confidence'),
                         path=(o.get('best_frame') if o.get('best_frame') and os.path.exists(o['best_frame']) else frame_path(vid, os.path.basename(o.get('best_frame') or ''))), bbox=o.get('bbox') or o.get('crop'), prefer=False)
            titles = [dict(t, _raw=t.get('timestamp_s', raw)) for t in (o.get('titles') or []) if isinstance(t, dict) and t.get('title')]
            ingest(room, kind, label, hint, sight, description=o.get('description'), titles=titles, count=o.get('count'), source_name='video')
    VO_STATS['shots'] = len(VO.get('shots') or []); VO_STATS['rules'] = len(OM_RULES)
SHAPE_RE = {   # semantic shape (schema "Object geometry") from the object kind and its labels; the page picks a mesh per shape
    'desk': [(r'l-shaped|\bl desk|return', 'desk_L'), (r'round|coffee|dining|oak table|\btable\b|tavol|console', 'table'), (r'.', 'desk')],
    'chair': [(r'armchair|club|eames|lounge|poltron', 'armchair'), (r'sofa|divan', 'sofa'), (r'.', 'chair')],
    'sofa': [(r'armchair', 'armchair'), (r'.', 'sofa')],
    'lamp': [(r'desk|table|brass', 'lamp_desk'), (r'.', 'lamp_floor')],
    'ladder': [(r'.', 'ladder')], 'piano': [(r'grand|coda', 'piano_grand'), (r'.', 'piano_upright')], 'glass_case': [(r'.', 'glass_case')], 'pile': [(r'.', 'pile')],
    'artwork': [(r'print|engrav|etch|map|drawing|photo|poster|caricatur|comic|sketch|calligraph|card|mirror', 'print'), (r'.', 'artwork')],
    'curiosity': [(r'statue|torso|figurin|bust|plaster|nude|statuett|sculpt|plaque', 'sculpture'), (r'globe|orrery|planetar', 'globe'), (r'\bjar\b|specimen', 'jar'),
                  (r'lute|recorder|music|instrument|flute', 'instrument'), (r'lens|lamp', 'lamp_desk'), (r'diorama|box|case|tray', 'box'), (r'.', 'other')],
    'other': [(r'\brug\b|carpet', 'rug'), (r'box|cabinet|chest|filing|cupboard|tower|console|tv|television|stand|stool', 'box'), (r'window|door', 'other'), (r'.', 'other')]}
def shape_of(kind, label, labels=''):
    text = fold(label + ' ' + labels)
    for rx, shp in SHAPE_RE.get(kind, [(r'.', 'other')]):
        if re.search(rx, text): return shp
    return 'other'
def build_objects():
    pending = list(MERGED.items()); order = []
    while pending:   # objects anchored on other objects wait until those are placed
        progress = False; rest = []
        for kv in pending:
            an = (kv[1]['rule'] or {}).get('anchor') or {}
            if an.get('object') and an['object'] in MERGED and an['object'] not in [k for k, _ in order] and any(k == an['object'] for k, _ in pending): rest.append(kv); continue
            order.append(kv); progress = True
        if not progress: order += rest; break
        pending = rest
    for key, m in order:
        room, r, kind = m['room'], m['rule'], m['kind']
        size = (r.get('size') if r else None) or m['size'] or OBJ_SIZE.get(kind) or [0.6, 0.8, 0.5]
        placed = None
        if r and r.get('position'): x, z = room['origin'][0] + r['position'][0], room['origin'][1] + r['position'][1]; by = r.get('base_y') or 0; rot = r.get('rotation') or 0; placed = 'objects_map position'
        elif r and r.get('anchor'):
            a = resolve_anchor(room, r['anchor'], size)
            if a: x, z, by, rot, note = a; rot = r.get('rotation', rot); by = r.get('base_y', by); placed = 'objects_map anchor: ' + note
            if a and kind == 'artwork' and r['anchor'].get('bookcase') and not r['anchor'].get('on_top') and 'rotation' not in r and r['anchor'].get('face') != 'toward' and bc_ref(r['anchor']['bookcase']):   # a picture leaning on or hung before a bookcase faces the room, not the shelves (the alfabeta poster showed its back)
                rot = BC[bc_ref(r['anchor']['bookcase'])]['rotationY']
        if placed is None and m['bookcases'] and kind == 'pile':
            bcid = m['bookcases'][0]; bc = BC[bcid]
            if re.search(r'floor|base of', fold(m['hints'][0])): x, z = bc_front(bcid, 0.35 + size[2] / 2); by = 0; note = 'at the foot of ' + bc['label']
            else: x, z = bc_front(bcid, -bc['depth'] / 2); by = bc['height'] + 0.02; note = 'on top of ' + bc['label']
            rot = bc['rotationY']; placed = 'objects.json bookcase: ' + note; ON_CAMERA.add(bcid)
        elif placed is None and m['bookcases']:
            bcid = m['bookcases'][0]; bc = BC[bcid]; x, z = bc_front(bcid, 0.6 + size[2] / 2); by = 0; rot = (bc['rotationY'] + 180) % 360; placed = 'objects.json bookcase: in front of ' + bc['label']; ON_CAMERA.add(bcid)
        if placed is None:
            x, z, by, rot, note = hint_position(room, kind, m['hints'][0], size); placed = 'position hint: ' + note; VO_STATS['auto_placed'] += 1
            VO_AUTO.append(dict(room=room['id'], kind=kind, label=m['label'][:50], hint=m['hints'][0][:60], placed=note, sources=sorted(m['sources'])))
        else: VO_STATS['rule_placed'] += 1
        with_t = [s for s in m['sightings'] if s.get('timestamp_s') is not None]
        first = sorted(with_t, key=lambda s: s['timestamp_s'])[0] if with_t else m['sightings'][0]
        vid = first.get('video_id')
        desc = r['description'] if r and r.get('description') else ' '.join(m['descriptions'][:2])   # a rule may state the description outright (an inventory note the frames contradict)
        desc = re.sub(r"\s*\(layout '[^']*'\)", '', desc or '').strip()   # the inventory's layout cross-reference is not reader's text
        oid = (r.get('id') if r else None) or ('obj:%s:%s' % (room['id'], slug(m['label'], 24)))
        o = add_object(dict(id=oid, room=room['id'], kind=kind, label=m['label'][:120], description=desc, position=[x - room['origin'][0], z - room['origin'][1]], rotation=rot, base_y=by, size=size,
                            video_id=vid, timestamp_s=first.get('timestamp_s'), source_url=first.get('url'), confidence='high' if placed.startswith('objects_map') else 'medium'))
        if o is None: continue
        o['placement'] = 'given' if placed.startswith('objects_map position') else 'inferred'; o['placement_note'] = placed; o['_placed'] = placed; o['shape'] = (r.get('shape') if r else None)
        fit_on_support(o, r, room)   # a thing on top of a desk, a cabinet or a bookcase stays inside its top (the desk piles hung 1.2 m past the desk's end)
        o['timestamp_raw_s'] = first.get('timestamp_raw_s'); o['time'] = first.get('time'); o['video_title'] = (VIDEOS.get(vid) or {}).get('title') if vid else None; o['frame'] = first.get('frame')
        o['count'] = m['count'] or None
        if r and 'count' in r: o['count'] = r['count']   # a rule may state the count, or clear it (one canvas is not 'c. 4 items')
        if r and isinstance(r.get('count'), int) and r['count'] > 0: o['count'] = r['count']   # the rule states what the film shows (six dining chairs); the inventory counted one frame
        if r and r.get('row'): o['row'] = True   # a row of standing books on a top (the ECO paperbacks on the low unit), drawn as spines side by side, unknown tier
        if r and isinstance(r.get('books_high'), int) and r['books_high'] > 0:
            o['books_high'] = r['books_high']; o['count'] = r['books_high']   # the height counted in the spine reading (books, unlabelled included)
            if o.get('description'): o['description'] = re.sub(r':?\s*\d+ books high\b.*$', '.', o['description']).replace('..', '.').strip()   # the inventory's own count of the frame is superseded by the reading (the panel prints one count line)
        o['sightings'] = [dict(kind=s.get('kind', 'video'), video_id=s.get('video_id'), timestamp_s=s.get('timestamp_s'), timestamp_raw_s=s.get('timestamp_raw_s'), time=s.get('time'), url=s.get('url'), frame=s.get('frame'), image=s.get('image'), label=s.get('label')) for s in m['sightings']]
        o['frames_seen'] = len(m['sightings']); o['seen_labels'] = sorted(set(m['labels']))[:8]; o['sources'] = sorted(m['sources'])
        if m.get('exp_ids'): o['experience_ids'] = m['exp_ids']; o['confidence'] = {'seen-clearly': 'high', 'partially-seen': 'medium', 'reported-in-text': 'low'}.get(m.get('confidence_exp'), o['confidence'])
        if r and r.get('confidence') in ('high', 'medium', 'low'): o['confidence'] = r['confidence']   # the rule's own placement confidence (e.g. the piano's wall is a medium guess) overrides the 'placed by rule' default
        if m['bookcases']: o['bookcases'] = m['bookcases']
        if m['titles']: o['_titles'] = m['titles']
        # geometry hints for the page (schema_eco.md, "Object geometry"): the modelling note's size as [w, d, h], a semantic shape, the wall unit it stands against, the facing angle
        o['primitive'] = (r.get('shape') if r else None)                    # the page's simple mesh (box | cylinder | sphere | torus | stand | flat | lute | window), from objects_map
        o['shape'] = shape_of(kind, m['label'], ' '.join(m['labels']))
        if m['size']: o['dims_m'] = [round(m['size'][0], 3), round(m['size'][2], 3), round(m['size'][1], 3)]
        if isinstance((r or {}).get('dims_m'), list) and len(r['dims_m']) == 3: o['dims_m'] = [round(float(v), 3) for v in r['dims_m']]   # a rule may state the size ([w, d, h] metres) when no modelling note does
        if r and r.get('size') and not isinstance(r.get('dims_m'), list) and o.get('dims_m') and kind not in ('artwork', 'pile'):   # a rule's size is the oriented one (w, h, d in the room's frame); the note's dims_m knows only the thing's long and short sides, and the page draws from dims_m (the rare-book table lay across the room while its rule, its guard and its piles had it along)
            want = [round(o['size'][0], 3), round(o['size'][2], 3), round(o['size'][1], 3)]
            turned = [o['dims_m'][1], o['dims_m'][0], o['dims_m'][2]]   # the note's width and depth exchanged is the same piece standing across the room (the rare-book table)
            if r.get('size_from'): o['size_note'] = r['size_from']   # a rule that says why its size is not the note's (two dioramas side by side where the inventory measured one)
            elif any(abs(a - b) > 0.011 for a, b in zip(o['dims_m'], want)) and any(abs(a - b) > 0.011 for a, b in zip(turned, want)): warn('objects map: %s drawn to its rule size %s (the note said w %.2f d %.2f h %.2f)' % (o['id'], o['size'], *o['dims_m']))
            o['dims_m'] = want
        an = (r.get('anchor') if r else None) or {}
        o['against_wall'] = (bc_ref(an['bookcase']) if an.get('bookcase') else None) or (m['bookcases'][0] if (placed.startswith('objects.json bookcase') and m['bookcases']) else None)
        o['facing'] = round(rot % 360, 1)
        o['_cands'] = [dict(path=s.get('path'), bbox=s.get('bbox'), prefer=s.get('prefer'), hint=s.get('hint') or '', frame=s.get('frame'), video_id=s.get('video_id')) for s in m['sightings'] if s.get('path')]
        if (r or {}).get('crop') or (r or {}).get('bbox'): o['_crop'] = r.get('crop') or r.get('bbox')
        # a rule may name the frame (`thumb_frame`, a file of eco-video/frames/<video>/, with the object's video) or the photograph
        # (`thumb_photo`, a file of eco-sources/eco-photos/) whose crop shows the thing, when the inventory's own frame shows the wrong wall;
        # `no_thumb: true` leaves it without a picture (the page draws a neutral canvas and says so)
        if (r or {}).get('no_thumb'): o['_no_thumb'] = True
        elif (r or {}).get('thumb_frame'):
            tv, tp = None, None
            for tv in [v for v in (r.get('thumb_video'), (VO or {}).get('video_id'), vid) if v]:   # the film's frames first: a rule names its frames even when the object's first sighting is another video's
                tp = frame_path(tv, r['thumb_frame'])
                if tp: break
            if tp: o['_thumb'] = dict(path=tp, bbox=None, hint='', frame=r['thumb_frame'], video_id=tv, prefer=True)
            else: warn('objects map: %s: thumb_frame %s not found' % (o['id'], r['thumb_frame']))
        elif (r or {}).get('thumb_photo'):
            tp = r['thumb_photo'] if os.path.isabs(r['thumb_photo']) else os.path.join(SRC_DIR, 'eco-photos', r['thumb_photo'])
            if os.path.exists(tp): o['_thumb'] = dict(path=tp, bbox=None, hint='', frame=os.path.basename(tp), video_id=None, prefer=True)
            else: warn('objects map: %s: thumb_photo %s not found' % (o['id'], r['thumb_photo']))
        for wkey in (r.get('walls') if r else None) or []:   # a string, or {"wall": ..., "raw_from": s, "raw_to": s} for a window of the reader's raw seconds
            if isinstance(wkey, dict) and wkey.get('wall'): WALL2OBJ.setdefault(fold(wkey['wall']).strip(), []).append((o['id'], wkey.get('raw_from'), wkey.get('raw_to'), bool(wkey.get('defer'))))
            elif isinstance(wkey, str): WALL2OBJ.setdefault(fold(wkey).strip(), []).append((o['id'], None, None, False))
        VO_STATS['objects_created'] += 1
def apply_created_objects():
    """objects_map_eco.json rules with `create: true`: things the footage shows that neither inventory lists (the lectern, the low chest, the
    radiator, the second white armchair ...). The rule itself is the sighting: `video_id` + `film_s` (true film seconds) + `frame` (a file of
    eco-video/frames/<video>/), or `photo` (a file of eco-sources/eco-photos/), give the object its link, its time and its thumbnail crop."""
    for r in OM_RULES:
        if not r.get('create') or not r.get('id'): continue
        room = room_of(r.get('room'))
        if room is None: warn('objects map: create rule %s: unknown room %r' % (r['id'], r.get('room'))); continue
        if r.get('id') in MERGED: continue   # an inventoried sighting already matched this rule
        kind = r.get('kind') or 'other'; label = r.get('label') or r['id']
        vid = r.get('video_id') or (VO or {}).get('video_id'); fs = r.get('film_s'); frame = r.get('frame'); photo = r.get('photo')
        if isinstance(fs, (int, float)) and vid:
            raw = round(float(fs) - video_offset(vid), 2)
            sight = dict(kind='video', video_id=vid, timestamp_s=float(fs), timestamp_raw_s=raw, time=hms(float(fs)), url=yt_url(vid, float(fs)), frame=frame, label=label, description=r.get('description'), hint='', count=None, path=frame_path(vid, frame), bbox=None, prefer=False)
            src = 'video'
        elif photo:
            pth = photo if os.path.isabs(photo) else os.path.join(SRC_DIR, 'eco-photos', photo)
            sight = dict(kind='photo', video_id=None, timestamp_s=None, timestamp_raw_s=None, time=None, url=r.get('photo_url'), frame=os.path.basename(photo), image=photo, label=label, description=r.get('description'), hint='', count=None, path=pth if os.path.exists(pth) else None, bbox=None, prefer=True)
            src = 'video'   # counted with the film objects; the sighting kind says 'photo'
        else: warn('objects map: create rule %s has neither film_s+frame nor photo' % r['id']); continue
        VO_STATS['created_by_rule'] += 1
        ingest(room, kind, label, '', sight, description=r.get('description'), count=r.get('count'), source_name=src, rule=r)
apply_experience_objects()
apply_video_objects()
apply_created_objects()
build_objects()
ROOMS_SEEN = {}
for rs in (VO or {}).get('rooms_seen') or []:
    r = room_of(rs.get('room_id'))
    if r is None: continue
    rngs = [[float(a), float(b)] for a, b in rs.get('ranges') or [] if isinstance(a, (int, float)) and isinstance(b, (int, float))]
    r['seen_ranges'] = [[corrected_ts(VO.get('video_id'), a), corrected_ts(VO.get('video_id'), b)] for a, b in rngs]; r['seen_seconds'] = round(sum(b - a for a, b in rngs), 1)
    r['seen_video_id'] = VO.get('video_id'); r['seen_first_url'] = yt_url(VO.get('video_id'), rngs[0][0] + video_offset(VO.get('video_id'))) if rngs else None
    ROOMS_SEEN[r['id']] = r['seen_seconds']

# ------------------------------------------------------------------ Braidense rare books
BOOKS = []
DESC_LIST = []
def add_desc(b):
    if '~' in b['id']: return   # a further copy of a reading (id~pile): looked up under the reading's id
    DESC_LIST.append(dict(id=b['id'], title=b['title'], author=b.get('author'), language=b.get('language'), year=b.get('year'), publisher=b.get('publisher'), source_kind=b['source_kind'], confidence=b.get('confidence')))
SM_RE = re.compile(r'ECO\.(\d\d)\.(\d+)(?:/(\d+))?')
rare = []
# UNIMARC 461 of the Braidense records (the CSV has no set titles): bid -> (set title, volume number, set responsibility) for the numbered volumes 'Vol. 1.', '2', '4: Manuscripts'
RARE_SETS = {}
RARE_NAMES = {}   # bid -> the record's own name headings (UNIMARC 700 and 701, '$a Manara $b , Milo' as 'Milo Manara'), read with the sets
if args.braidense_mrc and os.path.exists(args.braidense_mrc):
    try:
        for fields in iso2709_records(args.braidense_mrc):
            bid = next((v for t, v, _ in fields if t == '001'), None)
            if bid:   # the record's own name headings, for a set statement that is only surnames
                for t, ind, subs in fields:
                    if t in ('700', '701') and subs:
                        a = ' '.join(v for c, v in subs if c == 'a').strip(' ,'); fn = ' '.join(v for c, v in subs if c == 'b').strip(' ,')
                        if a: RARE_NAMES.setdefault(bid.strip(), []).append((a, fn))
            for want in ('461', '462', '463'):   # set level first; the Ruysch Thesaurus volumes ('5', '1739') link only to their subset (462)
                for t, ind, subs in fields:
                    if t == want and subs and bid:
                        st = ' '.join(unimarc_embedded(subs, '200', ('a',))); vol = next((v for c, v in subs if c == 'v'), None); resp = ' '.join(unimarc_embedded(subs, '200', ('f',)))   # the set's statement of responsibility too
                        if st: RARE_SETS[bid.strip()] = (st, vol, resp or None); break
                if bid and bid.strip() in RARE_SETS: break
    except Exception as e: warn('Braidense UNIMARC unreadable (%s): volume titles stay as in the CSV' % e)
# a Braidense record that describes a multi-volume set whose volumes have records of their own in the export, and that holds no inventory
# of its own (no 950 $e), is a bibliographic wrapper, not a book on the shelf: the volumes are the spines. Such a record is not drawn, and its id
# resolves to its first volume wherever the data names it (tours, notable books, film matches); its article description serves the volumes.
# The four set records that do carry an inventory line (a volume held at set level) stay.
# the export's holdings (950: shelfmark $d, inventory number and note $e, inventory date $h) and possessor notes (317) are read per
# record. Section ECO.04 is the Braidense's own reference section of Eco's publications (its account of the catalogue, 4 May 2022, p. 6): a
# shelfmark there says nothing about the flat, so those records are kept as reference entries (placement "reference", no bookcase; the page lists
# them on a reference table) and are never drawn on a cabinet nor counted among the identified books. No edition is dropped or demoted by its
# year: what the export says about the copy (its inventory date, an ex libris, a possessor note) is stated on the entry instead.
RARE_SET_ONLY = {}     # set bid -> [volume bids in the export, first volume first]
RARE_ID_ALIAS = {}     # 'braidense:<set bid>' -> 'braidense:<first volume bid>'
RARE_DROPPED = dict(set_records=[])
RARE_COPIES = {}       # bid -> copy facts from the export: inventory number and date, holding note (ex libris), possessor note
RARE_RECON = {}        # the export against the Braidense's own count of volumes: records by kind and distinct shelfmarks (About text)
RARE_EXPORT_N = 0
REFERENCE = []         # the ECO.04 records: in books[] with placement "reference" and no bookcase
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
def long_date(iso):
    y, m, d = iso.split('-'); return '%d %s %s' % (int(d), MONTHS[int(m) - 1], y)
def rare_copy(fields):
    """Copy-level facts of a Braidense record: its ECO holdings (950 $d shelfmark; $e '<code> <inventory no.> <VMA> <note>'; $h inventory date) and the
    possessor note (317). None when the record holds no ECO copy."""
    holds = []
    for t, ind, subs in fields:
        if t != '950' or not subs: continue
        cur = None
        for c, v in subs:
            if c == 'd': cur = dict(shelfmark=re.sub(r'\s+', '', v).replace('NBECO.', 'ECO.')); holds.append(cur)
            elif cur is None: continue
            elif c == 'e':
                inv = v[5:16].strip(); tail = v[16:].strip(); m = re.match(r'(VMA|VPA|OPA)\s*(.*)$', tail)
                cur['inventory'] = inv or None; cur['note'] = ((m.group(2) if m else tail).strip(' -') or None)
            elif c == 'h' and re.match(r'\d{8}$', v.strip()): cur['inventory_date'] = '%s-%s-%s' % (v[:4], v[4:6], v[6:8])
    eco = [h for h in holds if h['shelfmark'].startswith('ECO.')]
    if not eco: return None
    poss = [v.strip().rstrip('. ') for t, ind, subs in fields if t == '317' and subs for c, v in subs if c == 'a' and v.strip()]
    first = next((h for h in eco if h.get('inventory')), eco[0])
    out = dict(inventory=first.get('inventory'), inventory_date=first.get('inventory_date'), holding_note=first.get('note'),   # the library is read by the page from the id prefix (braidense:)
               ex_libris=any(re.search(r'ex.?libris', h.get('note') or '', re.I) for h in eco), provenance=poss or None,
               holdings=[{k: v for k, v in h.items() if v} for h in eco])
    return {k: v for k, v in out.items() if v not in (None, [], False)}
REFERENCE_SENTENCE = "Recorded in Braidense's ECO.04 reference section. This copy's presence and position in Eco's apartment have not been established."
POSTHUMOUS_KNOWN = set()   # ids of editions dated 2016 whose month of publication is documented after 19 February 2016 (record_notes_eco.json, field posthumous)
def reference_note(b):
    """The provenance text of an ECO.04 entry: the reference sentence, then what the export says about this copy (its inventory date, before or after
    the transfer of the rare books in August 2021), then a posthumous edition where the date proves it; never an inference from the year alone."""
    cp = b.get('copy') or {}; parts = [REFERENCE_SENTENCE]
    if cp.get('inventory_date'):
        parts.append("The library's inventory records this copy on %s, %s the rare books were transferred in August 2021." % (long_date(cp['inventory_date']), 'before' if cp['inventory_date'] < '2021-08' else 'after'))
    if (b.get('year') or 0) > 2016 or b['id'] in POSTHUMOUS_KNOWN:
        parts.append("This edition appeared after Eco's death." + ('' if cp.get('inventory_date') else " Whether this copy was subsequently kept in the apartment or acquired by the institution has not been established."))
    elif b.get('year') == 2016: parts.append("This edition is dated 2016, the year of Eco's death.")
    return ' '.join(parts)
if args.braidense_mrc and os.path.exists(args.braidense_mrc):
    try:
        _recs = {}
        for fields in iso2709_records(args.braidense_mrc):
            bid = next((v for t, v, _ in fields if t == '001'), None)
            if bid: _recs[bid.strip()] = fields
        def _volnum(k):
            v = RARE_SETS.get(k, (None, None, None))[1]
            m = re.search(r'\d+', str(v or '')) or re.match(r'\D{0,3}(\d+)', next((x for t, ind, subs in _recs[k] if t == '200' and subs for c, x in subs if c == 'a'), ''))
            return int(m.group(m.lastindex or 0)) if m else 10 ** 6
        _sm = collections.Counter(); _bw = 0; _par = 0
        for bid, fields in _recs.items():
            kids = [v[3:].strip() for t, ind, subs in fields if t == '463' and subs for c, v in subs if c == '1' and v.startswith('001')]
            kids = sorted({k for k in kids if k in _recs}, key=lambda k: (_volnum(k), k))
            own = any(c == 'e' for t, ind, subs in fields if t == '950' and subs for c, v in subs)
            if kids and not own: RARE_SET_ONLY[bid] = kids; RARE_ID_ALIAS['braidense:' + bid] = 'braidense:' + kids[0]
            cp = rare_copy(fields)
            if cp:
                RARE_COPIES[bid] = cp
                for h in cp['holdings']:
                    if not h['shelfmark'].startswith('ECO.04'): _sm[h['shelfmark']] += 1
                if any(re.search(r'legat[oi] (con|insieme)|in miscellanea', (h.get('note') or '') + ' ' + ' '.join(v for t, ind, subs in fields if t in ('316', '300') and subs for c, v in subs if c == 'a'), re.I) for h in cp['holdings']): _bw += 1
            if any(t == '461' and subs for t, ind, subs in fields): _par += 1
        RARE_RECON = dict(export_records=len(_recs), set_records_not_drawn=len(RARE_SET_ONLY), records_with_parent_set=_par, records_noting_works_bound_together=_bw,
                          distinct_shelfmarks_eco01_03=len(_sm), distinct_running_numbers_eco01_03=len({re.sub(r'/.*$', '', k) for k in _sm}), shelfmarks_shared_by_several_records=sum(1 for k, n in _sm.items() if n > 1),
                          braidense_volumes_at_transfer=1328, note='a record is a catalogue entry, not a spine: a set record stands behind its volumes, works bound together share a shelfmark, and the ECO.04 entries are the library\'s reference copies; the 1,328 volumes the Braidense counted at the transfer of August 2021 are not equated with any record count (eco-map/reconcile_braidense.py)')
    except Exception as e: warn('Braidense UNIMARC set links unreadable (%s): every record is drawn' % e)
VOLUME_TITLES = collections.Counter()   # how many numbered volumes got a composed title, per catalogue
AUTHORS_FROM_SET = collections.Counter()   # how many records without a statement of responsibility of their own took the set's, per catalogue
SET_RESP_SKIP_RE = re.compile(r"\b(partie|parties|tome|tomes|vol|vols|volume|volumes|parte|parti|band|bände|teil|livre|book)\b", re.I)   # a set statement that goes on to name the volumes ('[A.B.]. Premiere (-seconde) partie') is the set's title page, not an author line
def names_from_headings(resp, names):
    """A set statement of responsibility that is only surnames ('Manara, Eco') written out from the record's own name headings ('Milo Manara, Umberto Eco'); any other statement as transcribed."""
    if not resp or not names: return resp
    parts = [x.strip(' .') for x in re.split(r'\s*(?:,|;|&| e | and | et | und )\s*', resp) if x.strip(' .')]
    if not parts or len(parts) > len(names): return resp
    out = []
    for part in parts:
        hit = next((n for n in names if fold(n[0]) == fold(part)), None)
        if not hit or not hit[1]: return resp
        out.append('%s %s' % (hit[1], hit[0]))
    return ', '.join(out)
BARE_NUMBER_RE = re.compile(r"^\s*\[?\d{1,2}(?:\.\d{1,2}){0,3}(?:\s*/\s*\d{1,2})?\]?\s*:\s*\S")   # a title that opens with the catalogue's bare number and colon ('4: La filosofia moderna')
VOL_COLON_RE = re.compile(r"vol\. [\d./-]+: \d{1,2}(?:\s*:|\s*$)")   # a composed title that prints a volume number, a colon and a bare number ('vol. 1: 2: Principles ...', 'vol. 5: 1') has read the catalogue's range as a separator; the composer refuses it (a warning), as the suite refuses a bare number
def refuse_vol_colon(b, title, what):
    """Warn when a composed title (or an English title) prints 'vol. N: M', which the catalogue's own ranges produce ('1-2: ...', '5 - 2: ...', '31.1-2: ...', '5-1')."""
    if title and VOL_COLON_RE.search(title): warn('%s of %s prints a volume number, a colon and a bare number (%s) from the statement %r' % (what, b['id'], title[:80], (b.get('volume_statement') or '')[:60]))
def bare_volume_title(b, catalog):
    """A record whose title is the catalogue's bare number, a colon and the volume's own words, with no set title in the record ('2: L'Eta romantica',
    a volume of a set the record does not name): the words head the title and the number follows ('L'Eta romantica, vol. 2'); volume_statement keeps the record's own title."""
    t = clean_title(b.get('title'))
    if not BARE_NUMBER_RE.match(t) or b.get('volume_statement'): return
    v = volume_of(t)
    if not v or not v[1]: return
    n, rest = v
    if not re.search(r'[A-Za-zÀ-ÿ]{2}', rest): return
    b['volume_statement'] = t; b['title'] = '%s, vol. %s' % (rest, n); VOLUME_TITLES[catalog] += 1; VOLUME_TITLES['without a set title'] += 1; refuse_vol_colon(b, b['title'], 'composed title')
def apply_volume_title(b, set_title, catalog, set_resp=None):
    """Numbered volume -> title '<set title>, vol. N[: own title]', volume_statement = the record's own title, set_title kept. A record with no
    statement of responsibility of its own takes the set's (UNIMARC 461 embedded 200 $f, as the catalogue transcribes it) as its author line, flagged author_from_set.
    A set that is itself a numbered volume of a larger set the record does not name ('4: La filosofia moderna', the Storia della filosofia's fourth
    volume, under which '5: G. G. F. Hegel' stands) heads the title with its own words; its number is kept in set_volume, the transcription in set_title_raw."""
    if not set_title: return
    b['set_title'] = clean_title(set_title)
    if VOL_RANGE_RE.match(b['set_title']): b['set_title_raw'] = b['set_title']; b['set_title'] = VOL_RANGE_RE.sub('', b['set_title'])   # "[24-32]: Frederici Ruyschii ..." (the range of the set inside its series) is not part of the title on the spine
    if BARE_NUMBER_RE.match(b['set_title']):
        sv = volume_of(b['set_title'])
        if sv and sv[1] and re.search(r'[A-Za-zÀ-ÿ]{2}', sv[1]): b.setdefault('set_title_raw', b['set_title']); b['set_volume'] = sv[0]; b['set_title'] = sv[1]; VOLUME_TITLES['set within a set'] += 1
    comp = compose_volume_title(clean_title(b['title']), b['set_title'])   # cleaned first: the SBN export writes '[1]' as '\\1!'
    if comp: b['volume_statement'] = clean_title(b['title']); b['title'] = comp; VOLUME_TITLES[catalog] += 1; refuse_vol_colon(b, comp, 'composed title')
    if set_resp and not b.get('author') and not SET_RESP_SKIP_RE.search(set_resp):
        b['author'] = names_from_headings(clean_title(set_resp), RARE_NAMES.get(b['id'].split(':', 1)[-1])); b['author_from_set'] = True; AUTHORS_FROM_SET[catalog] += 1
RECORD_NOTES = {}   # record_notes_eco.json next to this script: {"<book id>": {"year": 1886, "date_note": "...", "note": "...", "source": "...", "posthumous": true}}
_rn_path = os.path.join(H, 'record_notes_eco.json')
if os.path.exists(_rn_path):
    try: RECORD_NOTES = {k: v for k, v in json.load(open(_rn_path, encoding='utf-8')).items() if isinstance(v, dict) and not k.startswith('_')}
    except Exception as e: warn('record_notes_eco.json unreadable: %s' % e)
if os.path.exists(args.braidense):
    for r in csv.DictReader(open(args.braidense, encoding='utf-8')):
        m = SM_RE.match(r.get('shelfmark') or '')
        sec, num, part = (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)) if m else (None, None, 0)
        yr = r.get('year') or ''
        b = dict(id='braidense:' + r['bid'], title=r['title'].strip(), author=(r.get('responsibility') or '').strip() or None, year=int(yr) if yr.strip().isdigit() else None,
                 date=r.get('date') or None, place=r.get('place') or None, language=lang_code(r.get('lang')), shelfmark=r.get('shelfmark') or None, all_shelfmarks=r.get('all_shelfmarks') or None,
                 origin='catalog', source_kind='catalog', catalog='braidense', source_url='http://opac.braidense.it/bid/' + r['bid'], confidence='high',
                 placement='catalogued' if m else 'inferred', rare=True, possessor_field=r.get('possessor_field_Eco') == 'yes', _sec=sec, _num=num, _part=part)
        if r['bid'].strip() in RARE_SETS: apply_volume_title(b, RARE_SETS[r['bid'].strip()][0], 'braidense', RARE_SETS[r['bid'].strip()][2])
        else: bare_volume_title(b, 'braidense')
        RARE_EXPORT_N += 1
        if r['bid'].strip() in RARE_SET_ONLY: RARE_DROPPED['set_records'].append(dict(id=b['id'], title=b['title'][:60], volumes=RARE_SET_ONLY[r['bid'].strip()])); continue
        if r['bid'].strip() in RARE_COPIES:   # the first holding's facts are the copy's own fields; the holdings list is shipped, compact, only when the record has several ECO holdings (volumes, works bound together)
            _cp = dict(RARE_COPIES[r['bid'].strip()]); _hl = _cp.pop('holdings', None) or []
            if len(_hl) > 1: _cp['holdings'] = [{k: h[k] for k in ('shelfmark', 'inventory', 'inventory_date') if h.get(k)} for h in _hl]
            b['copy'] = _cp
        rn = RECORD_NOTES.get(b['id'])
        if rn:   # curated corrections of a record's date, with the note that says why (record_notes_eco.json); the export's own date stays in `date`
            if rn.get('year'): b['year'] = rn['year']
            if rn.get('date_note'): b['date_note'] = rn['date_note']
            if rn.get('posthumous'): POSTHUMOUS_KNOWN.add(b['id'])
        if sec == 4:   # the Braidense's reference section of Eco's own publications, not a shelf of the flat (see REFERENCE above)
            b['placement'] = 'reference'; b['reference'] = True; b['bookcase'] = None; b['shelf'] = None; b['slot'] = None; b['section'] = None
            if b.get('copy'): b['copy']['library_copy'] = True
            b['placement_note'] = reference_note(b); b['width'] = round(random.uniform(0.022, 0.04), 4); b['height'] = round(random.uniform(0.18, 0.245), 3)
            REFERENCE.append(b); BOOKS.append(b); add_desc(b); continue
        rare.append(b)
else: warn('Braidense CSV not found: ' + args.braidense)
def rare_cabinet(b):
    if b['_sec'] == 1: return 'rare-01' if b['_num'] < 700 else 'rare-02'
    if b['_sec'] == 3: return 'rare-04' if 'rare-04' in BC else 'rare-02'   # the "most precious books" section
    if b['_sec'] == 2: return 'rare-02'
    return 'rare-02'

# incunabula listed by Nuovo & Coletto (AIB Studi 62, 2022): the ones absent from the Braidense export become catalogue books on the ECO.03 wall
AIB_URL = 'https://aibstudi.aib.it/article/view/13386'
INCUN = dict(files=[], listed=0, matched=0, added=0, unmatched_bids=[])
def load_incunabula():
    paths = sorted(glob.glob(os.path.join(args.experience, 'incunab*.json')) + glob.glob(os.path.join(args.experience, 'incunab*.jsonl')))
    items = []
    for p in paths:
        try: data = load_jsonl(p) if p.endswith('.jsonl') else json.load(open(p, encoding='utf-8'))
        except Exception as e: warn('experience/%s unreadable: %s' % (os.path.basename(p), e)); continue
        if isinstance(data, dict): data = data.get('incunabula') or data.get('items') or data.get('books') or data.get('list') or data.get('records') or []
        items += [x for x in data if isinstance(x, dict)]
        INCUN['files'].append(os.path.basename(p))
    return items
def g1(d, *keys):
    for k in keys:
        if d.get(k) not in (None, '', []): return d[k]
    return None
for k, x in enumerate(load_incunabula()):
    title = (g1(x, 'title', 'short_title', 'work') or '').strip()
    if not title: continue
    INCUN['listed'] += 1
    author = (g1(x, 'author', 'responsibility', 'creator') or '').strip() or None
    yr = g1(x, 'year', 'date', 'printed'); yr = int(re.search(r'1[45]\d\d', str(yr)).group(0)) if yr and re.search(r'1[45]\d\d', str(yr)) else None
    istc = g1(x, 'istc', 'istc_id', 'istc_no', 'ISTC'); bid = g1(x, 'bid', 'braidense_bid', 'sbn', 'braidense')
    absent = g1(x, 'absent', 'absent_from_braidense', 'missing', 'not_in_braidense') is True or fold(str(g1(x, 'status', 'in_braidense', 'braidense_status') or '')) in ('absent', 'missing', 'no', 'false', 'not in braidense')
    hit = None
    shelf = g1(x, 'braidense_shelfmark', 'shelfmark')
    if bid: hit = next((b for b in rare if b['id'] == 'braidense:' + str(bid)), None)
    if hit is None and shelf: hit = next((b for b in rare if (b.get('shelfmark') or '').startswith(str(shelf))), None)
    if hit is None and not absent:
        T = {t[:5] for t in tokens(re.sub(r'\(.*?\)', ' ', title)) if len(t) >= 5}; sur = fold(author).split()[0].strip(',')[:5] if author and fold(author).split() else None
        best, bs = None, 0
        for b in rare:
            if b.get('incunabulum'): continue   # one Braidense record per listed incunabulum: the two Annius editions of 1498 must not both take the same record
            if (b['year'] or 0) > 1501 and (b['_sec'] != 3): continue
            toks = {t[:5] for t in tokens(b['title']) if len(t) >= 5} | {t[:5] for t in tokens(b.get('author') or '') if len(t) >= 5}
            hitn = len(T & toks); has_sur = bool(sur and len(sur) >= 4 and (sur in fold(b.get('author') or '') + ' ' + fold(b['title']) or re.search(r'\b' + re.escape(sur[:4]), fold(b['title']))))   # 'Annius' ~ 'Annii'
            sc = hitn + (1.0 if has_sur else 0) + (1.5 if yr and b['year'] == yr else 0)
            if (hitn >= 1 or has_sur) and yr and b['year'] == yr and sc > bs: best, bs = b, sc
            elif hitn >= 2 and sc > bs: best, bs = b, sc
        hit = best
    if hit is None and not absent:   # second stage: the notable_books.json join (its incunabula records carry the Braidense id)
        for n in EXP['notable']:
            if not isinstance(n, dict) or (n.get('year') or 9999) > 1501: continue
            cm = n.get('catalog_match') if isinstance(n.get('catalog_match'), dict) else {}
            if not cm.get('books_json_id'): continue
            nsur = fold(n.get('author') or '').split()[0].strip(',')[:5] if n.get('author') else ''
            if yr and n.get('year') == yr and ((sur and len(sur) >= 4 and nsur == sur) or (norm(title)[:8] and norm(title)[:8] == norm(n.get('title') or '')[:8])):
                hit = next((b for b in rare if b['id'] == cm['books_json_id'] and not b.get('incunabulum')), None)   # a record already taken by another listed incunabulum is not reused
                if hit: break
    card = {k: g1(x, k) for k in ('place', 'printer', 'date', 'format', 'size_cm', 'binding_condition', 'provenance', 'price_dealer', 'note', 'article_page', 'pdf_page') if g1(x, k)}   # pdf_page shipped with article_page (the journal's printed page)
    if istc: card['istc'] = str(istc); card['istc_url'] = g1(x, 'istc_url') or 'https://data.cerl.org/istc/' + str(istc)
    card['source'] = "Nuovo & Coletto, 'Gli incunaboli di Umberto Eco', AIB Studi 62 (2022), with Eco's own card data"; card['source_url'] = AIB_URL
    hcm = re.match(r'\s*(\d+(?:[.,]\d+)?)', str(g1(x, 'size_cm') or ''))
    if hit is not None:
        INCUN['matched'] += 1
        hit['incunabulum'] = True; hit['card'] = card
        if istc: hit['istc'] = str(istc); hit['istc_url'] = card['istc_url']
        if hcm: hit['_height_cm'] = float(hcm.group(1).replace(',', '.'))
        continue
    INCUN['added'] += 1
    if bid: INCUN['unmatched_bids'].append(str(bid))
    bid_id = 'istc:' + slug(str(istc), 20) if istc else 'incunabula:' + slug(title, 40)
    b = dict(id=bid_id, title=title, author=author, year=yr, date=str(g1(x, 'date', 'year') or '') or None, place=g1(x, 'place', 'printed_at'), publisher=g1(x, 'printer', 'publisher'),
             language=lang_code(g1(x, 'language', 'lang')) or 'la', origin='catalog', source_kind='catalog', catalog='aib-2022', istc=str(istc) if istc else None,
             source_url=g1(x, 'url', 'istc_url', 'source_url') or ('https://data.cerl.org/istc/' + str(istc) if istc else AIB_URL), aib_url=AIB_URL, confidence='medium', rare=True, incunabulum=True,
             placement='inferred', placement_note="listed among Eco's 36 incunabula (Nuovo & Coletto, 'Gli incunaboli di Umberto Eco', AIB Studi 62, 2022) but absent from the Braidense export; shelved with the most precious books (ECO.03)",
             notes=g1(x, 'note', 'notes', 'remarks'), card=card, _sec=3, _num=9000 + k, _part=0)
    if hcm: b['_height_cm'] = float(hcm.group(1).replace(',', '.'))
    rare.append(b)
by_cab = collections.defaultdict(list)
for b in rare: by_cab[rare_cabinet(b)].append(b)
for cab, lst in by_cab.items():
    if cab not in BC: warn('rare cabinet %s missing from layout' % cab); continue
    lst.sort(key=lambda b: (b['_sec'] or 9, b['_num'] or 99999, b['_part']))
    bc = BC[cab]; metres = usable_width(bc) * bc['shelves']
    w = max(0.02, min(0.07, metres / (len(lst) * 1.03 + 2)))   # 3% slack for readings the catalogue match misses
    RARE_W[cab] = round(w, 4); init_slots(bc, w)
    per = CAP[cab]
    for i, b in enumerate(lst):
        b['width'] = round(w * random.uniform(0.75, 1.25), 4)
        b['height'] = round(min(0.33, b['_height_cm'] / 100.0), 3) if b.get('_height_cm') else round(random.uniform(0.17, 0.30) if (b['year'] or 1700) < 1830 else random.uniform(0.17, 0.24), 3)
        if not place(cab, i // per, i % per, b): warn('rare cabinet %s full at %s' % (cab, b['shelfmark'])); continue
        BOOKS.append(b); add_desc(b)
for cab in ('rare-01', 'rare-02', 'rare-03', 'rare-04'):
    if cab in BC and cab not in SLOTS: init_slots(BC[cab], 0.04)

# ------------------------------------------------------------------ Bologna modern records -> subject map
RULES = []
for rule in SM['rules']:
    RULES.append(dict(name=rule['name'], bookcase=rule['bookcase'], dewey=tuple(rule.get('dewey', [])),
                      kw=[re.compile(k, re.I) for k in rule.get('keywords', [])], author=re.compile(rule['author'], re.I) if rule.get('author') else None,
                      subj=[re.compile(k, re.I) for k in rule.get('subjects', [])],   # patterns read on the subject headings and Dewey labels only
                      publisher=re.compile(rule['publisher'], re.I) if rule.get('publisher') else None))
FALLBACK = SM.get('fallback')
RULE_HITS = collections.Counter()
def unimarc_sub(rec, tag, codes):
    """Subfield values of every UNIMARC field `tag` of a Bologna record (the export keeps the fields as [{tag, ind, sub: [[code, value], ...]}])."""
    out = []
    for f in rec.get('unimarc') or []:
        if not isinstance(f, dict) or f.get('tag') != tag: continue
        out += [v for c, v in (f.get('sub') or []) if c in codes and v]
    return out
BARE_VOL_TITLE_RE = re.compile(r"^\s*\[?\d{1,3}(?:\s*[-–.]\s*\d{1,3})*\]?\s*\.?\s*$")   # a volume record whose own title is only its number ('1', '5-1', '5 - 2', '31.1-2')
NAME_LIKE_RE = re.compile(r"^(?:(?:di|de|da|von|van|par|by|del|della|dei|degli|delle|du|des)\s+)?(?:(?:[A-ZÀ-Ý]\.\s*)+[A-ZÀ-Ý][\w'’-]+|[A-ZÀ-Ý][\w'’-]+(?:\s+(?:(?:de|da|di|del|della|von|van|le|la|du|des)\s+|d[’'])?[A-ZÀ-Ý][\w'’-]+){0,3}|[A-ZÀ-Ý][\w'’-]+,\s*[A-ZÀ-Ý].*)\.?$")   # 'L. Todesco', 'Umberto Eco', 'Todesco, Luigi', 'Robert de Clari', 'di Francesco Barberi' (a particle before the name is a statement of responsibility, not a title)
RESP_ROLE_RE = re.compile(r"(?:\ba cura di\b|\bcura\b|\bedited\b|\bed\.|\beds\.|\beditor|\bhrsg|\bherausgegeben|\btranslat|\btrad\b|\btrad\.|\btraduzione|\btraduction|\bintroduzione|\bprefazione|\bpr[ée]face|\bby\b|\bpar\b)", re.I)   # a statement that names a role is a responsibility, whatever else it says
def looks_like_name(s):
    """Does a statement of responsibility read as a name (or a role with a name), not as a title? 'L. Todesco' yes; 'La chiesa nei tempi moderni' and 'I primi 300 anni' no."""
    s = (s or '').strip()
    return bool(s) and (bool(NAME_LIKE_RE.match(s)) or bool(RESP_ROLE_RE.search(s)))
def unimarc_461_resp(rec):
    """The set's own statement of responsibility (UNIMARC 461 embedded 200 $f) of a numbered volume, from the first 461 that carries one."""
    for f in rec.get('unimarc') or []:
        if not isinstance(f, dict) or f.get('tag') != '461': continue
        r = ' '.join(unimarc_embedded([(c, v) for c, v in (f.get('sub') or []) if v], '200', ('f',)))
        if r: return r
    return None
def own_name_headings(rec):
    """The record's own name headings (UNIMARC 700-702 in the export's persons), the library's provenance heading apart (the 702 'Eco, Umberto' with role 320, the donor, flagged bub_only)."""
    return [p for p in (rec.get('persons') or []) if isinstance(p, dict) and not p.get('bub_only') and str(p.get('role') or '') not in ('320', '390')]
PART_TITLES = []   # the volume records whose statement of responsibility was the part's title: {id, title, phrase, author}
def part_title_from_responsibility(b, rec):
    """A volume record whose own title is only its number and whose statement of responsibility is not a name but the part's title
    ('5-1' / 'La chiesa nei tempi moderni', as the OPAC reads it, under the set 'Corso di storia della Chiesa / L. Todesco'): the set's statement
    becomes the author line (author_from_set) and the phrase the part's title (part_title; the composed title reads 'vol. 5-1: La chiesa nei tempi
    moderni', as the English title already did). A record with a name heading of its own, a title with words, or a statement that reads as a name is left alone."""
    own = clean_title(rec.get('title_full') or rec.get('title')); phrase = b.get('author')
    if not phrase or rec.get('author') or own_name_headings(rec) or not BARE_VOL_TITLE_RE.match(own) or looks_like_name(phrase): return
    set_f = unimarc_461_resp(rec)
    if not set_f: return
    PART_TITLES.append(dict(id=rec['id'], title=own, phrase=phrase, author=set_f))
    b['part_title'] = phrase; b['title'] = '%s: %s' % (own, phrase); b['author'] = clean_title(set_f); b['author_from_set'] = True; AUTHORS_FROM_SET['bologna'] += 1
TITLES_COMPOSED = []   # the Bologna records whose served title differs from the export's title_full: {id, export, composed}
ISBD_SEP = {'e': ' : ', 'd': ' = '}
def isbd_title(rec):
    """The record's title from its own UNIMARC 200 subfields, punctuated as the catalogue prints it: $a, a further $a after ' ; ', $e (other title
    information) after ' : ', $d (a parallel title) after ' = '. The export's title_full joined the same subfields with a bare space, so 1,291 subtitles ran on
    ('Torah e filosofia percorsi del pensiero ebraico') and the cards printed no colon. The responsibility ($f, $g), the material designation ($b) and a title by
    another author ($c, five records, whose brackets run into the $f that follows) stay out, as they did in title_full. None when the record carries no 200 field."""
    for f in rec.get('unimarc') or []:
        if not isinstance(f, dict) or f.get('tag') != '200': continue
        out = ''
        for code, val in (f.get('sub') or []):
            val = ' '.join(str(val or '').split()).rstrip('| ').strip()   # 'contro tutti|': the cataloguer's stray field separator (two records)
            if code == 'd': val = re.split(r'\s+;\s+(?=\\|a cura di|edited by|hrsg)', val)[0]   # 'Aristoteloys ; \a cura di Gerardo Marenghi!': the responsibility after the parallel title stays out with the others
            if not val: continue
            if code == 'a': out = out + ' ; ' + val if out else val
            elif code in ISBD_SEP and out: out = out + ISBD_SEP[code] + val
        if out: return out
    return None
def unimarc_461(rec):
    """-> (set title, set subtitle + responsibility, volume number) from the first UNIMARC 461 of a Bologna record. The 461 embeds the set's own
    fields as '$1 001..', '$1 2001 $a Title $e subtitle $f author', '$1 210 $a Place $c Publisher', '$1 215 $a 3 volumi'; only the embedded 200
    block is a title (the earlier parent_title() joined every $a, so 'Scritti minori' came out as 'Scritti minori Torino v.')."""
    for want in ('461', '462', '463'):   # set level first, then the subset / piece links
        for f in rec.get('unimarc') or []:
            if not isinstance(f, dict) or f.get('tag') != want: continue
            subs = [(c, v) for c, v in (f.get('sub') or []) if v]
            a = ' '.join(unimarc_embedded(subs, '200', ('a',))); ef = ' '.join(unimarc_embedded(subs, '200', ('e', 'f')))
            vol = next((v for c, v in subs if c == 'v'), None)
            if a: return a, ef, vol
    return None, None, None
def parent_title(rec):
    """UNIMARC 461 embedded 200 $a $e $f: the set title (with subtitle and responsibility, for the subject rules) of a numbered volume whose own title is only '1', 'Vol. 2', '1: A-E'."""
    a, ef, _ = unimarc_461(rec)
    return ' '.join(x for x in (a, ef) if x)
def classify(rec, extended=False):
    """First subject_map rule that fits: `author` regex on the 700 author, `dewey` prefixes, `publisher` regex on the 210 $c imprint, then
    `subjects` regexes on the subject headings and Dewey labels alone, then `keywords` on subjects + Dewey labels + series + title +
    title_full (accents folded). With `extended`, the UNIMARC 461 set title and the
    responsibility statements (200 $f/$g) are appended to the keyword text: the generator tries the record's own fields first and the extended
    text only when nothing matched, so numbered volume parts ('2', 'Vol. 1') are placed by their set without moving any record the plain
    fields already place."""
    parts = (rec.get('subjects') or []) + (rec.get('dewey_label') or []) + (rec.get('series') or []) + [rec.get('title') or '', rec.get('title_full') or '']
    pub = rec.get('publisher') if isinstance(rec.get('publisher'), str) else ' ; '.join(rec.get('publisher') or [])
    if extended:
        pt = rec.get('parent_title') or parent_title(rec)
        if pt: parts.append(pt)
        parts += [x for x in [rec.get('responsibility') or ''] + list(rec.get('responsibility_other') or []) if isinstance(x, str) and x]
    # the imprint is matched only by a rule's own `publisher` regex: in the keyword text, university presses and 'Edizioni di Storia e Letteratura' would hit generic words
    subj_f = fold(' | '.join(parts)); pub_f = fold(pub)
    head_f = fold(' | '.join((rec.get('subjects') or []) + (rec.get('dewey_label') or [])))   # the cataloguer's classification alone (subject headings and Dewey labels), for a rule's `subjects` patterns
    deweys = [d.strip() for d in (rec.get('dewey') or [])]
    author = fold(rec.get('author') or '')
    for rule in RULES:
        if rule['author'] and rule['author'].search(author): return rule
        if any(d.startswith(p) for d in deweys for p in rule['dewey']): return rule
        if rule['publisher'] and pub_f and rule['publisher'].search(pub_f): return rule
        if rule['subj'] and head_f and any(k.search(head_f) for k in rule['subj']): return rule
        if any(k.search(subj_f) for k in rule['kw']): return rule
    return None
def classify2(rec):
    """-> (rule, how): the rule from the record's own fields ('record'), else from the extended text ('set title' or 'responsibility', whichever
    alone suffices, else 'extended'), else (None, None)."""
    r = classify(rec)
    if r: return r, 'record'
    r = classify(rec, extended=True)
    if not r: return None, None
    pt = parent_title(rec)
    if pt and classify(dict(rec, unimarc=[], parent_title=pt, responsibility=None, responsibility_other=[], publisher=[]), extended=True) is r: return r, 'set title'
    if classify(dict(rec, unimarc=[], parent_title=None), extended=True) is r: return r, 'responsibility'
    return r, 'extended'
modern, bad_lines = [], 0
if os.path.exists(args.bologna):
    with open(args.bologna, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line: continue
            try: rec = json.loads(line)
            except Exception: bad_lines += 1; continue   # the file may still be growing: a truncated last line is skipped
            if not rec.get('id') or not rec.get('title'): bad_lines += 1; continue
            modern.append(rec)
    if bad_lines: warn('bologna jsonl: %d unreadable/incomplete lines skipped (file still growing?)' % bad_lines)
else: warn('Bologna jsonl not found: ' + args.bologna)
ECO_INV_RE = re.compile(r'\bECO\s*0*(\d+)\b')
COPY_NOTES = {}; COPY_NOTES_APPLIED = []
if os.path.exists(args.copy_notes):
    try: COPY_NOTES = {k: v for k, v in json.load(open(args.copy_notes, encoding='utf-8')).items() if not k.startswith('_') and isinstance(v, dict)}
    except Exception as e: warn('copy notes unreadable: %s' % e)
# the inscription extractor. The University of Bologna's cataloguer transcribes the words written in a copy after the dedication remark
# ('dedica autografa di X a Umberto Eco, datata. "Per Umberto Eco con amicizia ..."'). The extractor takes the span after the dedication
# remark, closes it at its own quotation mark (the last one before the cataloguer's next remark, when nothing but punctuation follows it), and otherwise ends it where the
# next remark begins; a note with no quotation marks but 'datata ... . Per Umberto ...' yields the sentence. The words keep their final stop and the
# cataloguer's [?] and [...] marks; only '[!]' prints as '[sic]' (clean_inscription).
INSCR_QUOTES = '"“”«»'
INSCR_OPEN_RE = re.compile(r'["“«]')
INSCR_DEDIC_RE = re.compile(r'dedic(?:a|he|ato|ata|atoria)\b', re.I)
# words that open one of the cataloguer's own remarks: the inscription never runs into one of them
INSCR_HARD1 = (r"(?:orecchi[ae]|sottolineat|segni di attenzion|segni a (?:matita|penna)|segno a penna|rar[ei] (?:sottolin|segni)|frequent[ei] (?:sottolin|segni)|numeros[ei] (?:sottolin|segni)"
         r"|evidenziaz|annotazion[ei]|annotat[oa]\b|vi era(?:no)?\b|ora in FONDO|inserit[aoei]|allegat[aoei]|not[ae] manoscritt[ae]|note dell[’']autore|postill[ae]|cedola|(?:con |tracce del )?timbro"
         r"|nel volume|segnalibr|fascett|ritagli|fotocopi|estratt|cartoncin|post-it|busta n|correzion|errata corrige|sigla numerica|pagine ripiegate|presente nel volume|è presente|ex libris|dopo la copertina)")
# ordinary words that open a remark only after a semicolon, a full stop, a bracket or a closing quotation mark, since a dedication may use them too ('una cartolina da Alberto')
INSCR_HARD2 = r"(?:foglietti?\b|biglietto|cartolina|disegno|segue\b|lettera\b|indirizzo|recapi[ot])"
# where in the copy a thing sits: a boundary inside the quotation, never inside the introduction that leads to it
INSCR_LOC = (r"(?:alla c(?:arta)?\. di guardia|alla carta di guardia|a p\.\s*\d|pp?\.\s*\d|alle pp\.|tra le pp\.|sul frontespizio|sull[’']occhietto|sulla (?:carta|seconda|prima|terza|quarta|controguardia|copertina)"
            r"|sul (?:verso|retro|piatto|risvolto|colophon)|al frontespizio|in ultima pagina|a c\.\s*\d|non datata|firma autografa)")
INSCR_SEP_ANY = r'(?:^|(?<=[;,.•\s"”»\])]))\s*'
INSCR_SEP_STRONG = r'(?:^|(?<=[;.•"”»\]]))\s*'
INSCR_HARD_RE = re.compile(INSCR_SEP_ANY + INSCR_HARD1 + '|' + INSCR_SEP_STRONG + INSCR_HARD2, re.I)
INSCR_FULL_RE = re.compile(INSCR_SEP_ANY + INSCR_HARD1 + '|' + INSCR_SEP_STRONG + INSCR_HARD2 + '|' + INSCR_SEP_ANY + INSCR_LOC, re.I)
INSCR_ANY_WORD = '(?:' + INSCR_HARD1 + '|' + INSCR_HARD2 + '|' + INSCR_LOC + ')'
INSCR_CAP_RE = re.compile(r'\.\s*["”»]?\s+(?=Orecchi|Sottolineat|Segni (?:di|a)|Segno a|Rar[ei] |Frequent|Numeros|Not[ae] manoscritt|Vi era|Postill|Timbro|Cedola|Inserit|Allegat|Annotaz|Annotat|Evidenziaz|Disegno|Con timbro|Ora in|Ex libris|Tracce|Correzion|Errata|Firma autografa|Sigla|Pagine ripiegate|Presente nel|Segue\b)')   # a lookahead: the remark begins at the capital, after the full stop and any closing quotation mark
# a closing quotation mark joined to the next remark by a semicolon or an 'e'
INSCR_JOIN_RE = re.compile(r'["”»]\s*(?:;|,?\s*(?:e|ed)\s+(?=' + INSCR_ANY_WORD + '))', re.I)
# what the text between the dedication remark and its quotation mark may not contain: then the quotation belongs to another remark
INSCR_NOT_INTRO_RE = re.compile(r';|\bora in\b|vi era|inserit|foglietti?\b|cartoncin|tratta da|ex libris|estratt|fotocopia|post-it|ritaglio|annotat[oi]\b|segnalibr|fascett|biglietto|cartolina|lettera\b|articolo|pre-print|rivista|orecchi|sottolineat|segni di attenzion|evidenziaz|postill|timbro', re.I)
INSCR_DATE_RE = re.compile(r"^[\[\]\s]*(?:[A-ZÀ-Ý][A-Za-zÀ-ÿ'’.-]*[ ,]+)?\d{1,2}[./ -]?(?:[IVXivx]{1,4}|\d{1,2}|[A-Za-zÀ-ÿ]{3,10})[./ ,-]*\d{2,4}\.?[\]\s]*$")   # a date alone, at most one word (a place) before it: 'Roma 5.IX.07', 'Milano, 23 maggio 1980', 'Toronto 18 nov. 2011'"
INSCR_JUNK = ' \t.,;:•*–—-' + INSCR_QUOTES
def inscr_unbracket(t): return re.sub(r'\[[^\]]*\]', '', t)

def inscr_remark_end(note, start, intro):
    """Where the cataloguer's next remark begins after `start`: a remark word outside brackets and parentheses, a capitalised remark after a full stop, a closing quotation mark followed by a semicolon; else the end of the note. In the introduction (the words between 'dedica' and the quotation) only the hard remark words count, since 'sul frontespizio' there says where the dedication is."""
    rx = INSCR_HARD_RE if intro else INSCR_FULL_RE
    depth = 0; i = start; n = len(note)
    while i < n:
        ch = note[i]
        if ch in '[(': depth += 1
        elif ch in '])': depth = max(0, depth - 1)
        elif depth == 0:
            if rx.match(note, i): return i
            if ch == '.':
                cm = INSCR_CAP_RE.match(note, i)
                if cm: return cm.end()
            if not intro and ch in '"”»' and INSCR_JOIN_RE.match(note, i): return i + 1
        i += 1
    return n

def inscr_quotes_in(note, a, b):
    out = []; depth = 0
    for i in range(a, b):
        ch = note[i]
        if ch in '[(': depth += 1
        elif ch in '])': depth = max(0, depth - 1)
        elif depth == 0 and ch in INSCR_QUOTES: out.append(i)
    return out

def inscr_finish(text):
    text = re.sub(r'\s+', ' ', text).lstrip(' •*–—-' + INSCR_QUOTES).rstrip(' ,;:•*–—-')
    return text or None

def inscr_span_from(note, start, bound, quoted):
    """The words from `start` to the last quotation mark before `bound` when nothing but punctuation and bracketed remarks follow that mark and the quotation marks inside pair off; else to `bound` itself (an unclosed quotation ends with the remark)."""
    qs = inscr_quotes_in(note, start, bound)
    if qs:
        last = qs[-1]; tail = note[last + 1:bound]
        if not inscr_unbracket(tail).strip(INSCR_JUNK): return note[start:last], 'closed'
    text = note[start:bound]
    return text, ('unclosed' if quoted else 'no-quote')

def inscr_valid(text): return bool(text) and not re.fullmatch(r'[\d./ -]+', inscr_unbracket(text)) and len(inscr_unbracket(text).strip()) >= 4

def inscription_span(note):
    for m in INSCR_DEDIC_RE.finditer(note):
        intro_end = inscr_remark_end(note, m.end(), True)
        seg = note[m.end():intro_end]
        q = INSCR_OPEN_RE.search(seg)
        if q and not INSCR_NOT_INTRO_RE.search(seg[:q.start()]):
            start = m.end() + q.end()
            bound = inscr_remark_end(note, start, False)
            direct = re.search(r'datat[ao]\s*[.:,]?\s*$', seg[:q.start()])
            qs = inscr_quotes_in(note, start, bound)
            text = how = None
            if direct and qs and INSCR_DATE_RE.match(inscr_unbracket(note[start:qs[0]])):   # 'datata "Roma 5.IX.07"': the quotation may give only the date; the words, if any, follow it
                start2 = qs[0] + 1; rest = note[start2:inscr_remark_end(note, start2, True)]; q2 = INSCR_OPEN_RE.search(rest)
                gap = rest[:q2.start()] if q2 else rest
                if not q2 and not gap.strip(INSCR_JUNK):   # nothing follows: the quotation is all that was written, a signature with its date
                    text, how = inscr_span_from(note, start, bound, True)
                elif not INSCR_NOT_INTRO_RE.search(gap):
                    if q2 and not gap.strip(INSCR_JUNK): start2 = start2 + q2.end()
                    text, how = inscr_span_from(note, start2, inscr_remark_end(note, start2, False), True)
            else:
                text, how = inscr_span_from(note, start, bound, True)
            text = inscr_finish(text) if text else None
            if inscr_valid(text): return text, how
        nq = re.match(r'[^;"“«]{0,160}?\bdatat[ao]\b[^;."“«]{0,40}\.\s+(?=[A-Z])', seg)
        if nq and not INSCR_NOT_INTRO_RE.search(seg[:nq.end()]):
            s = m.end() + nq.end()
            text, how = inscr_span_from(note, s, inscr_remark_end(note, s, False), False)
            text = inscr_finish(text) if text else None
            if text and re.search(r'\bUmberto\b|\bEco\b', inscr_unbracket(text)) and len(inscr_unbracket(text)) >= 12: return text, 'no-quote'
    return None, None

INSCRIPTION_HOW = collections.Counter()   # how each served inscription was closed (closed / unclosed / no-quote), for the change report
def inscription_of(annotation):
    """The words written in the copy, as the cataloguer transcribed them, or None when the note quotes none (a dedication only noted, a date alone, a quotation that belongs to another remark)."""
    if not annotation: return None
    text, how = inscription_span(annotation)
    if text: INSCRIPTION_HOW[how] += 1
    return text
def clean_inscription(t):
    """The reader's form of a transcribed inscription: the cataloguer's '[!]' printed as '[sic]', control characters and doubled spaces removed; the words themselves untouched."""
    if not isinstance(t, str): return t
    t = t.replace('\x88', '').replace('\x89', '').replace('\u0331', '')
    t = SIC_RE.sub(' ' + SIC_MARK, t)
    t = close_elisions(t)   # the same closing the copy note gets ("d' hors d'oeuvre"), so the quotation stays a passage of the note
    return re.sub(r'\s+', ' ', t).strip() or None
GIVER_DATES_RE = re.compile(r'\s*<[^>]*>')
def giver_name(catalogue_form):
    """'Alberoni, Francesco <1929-2023>' -> 'Francesco Alberoni'; 'Rijk, Lambertus Marie : de' -> 'Lambertus Marie de Rijk'; 'Di_Nola, Alfonso M.' -> 'Alfonso M. Di Nola'.
    The catalogue form stays in dedication_by; this is the name as a reader says it."""
    t = GIVER_DATES_RE.sub('', str(catalogue_form or '')).replace('_', ' ').strip()
    t = clean_display(t, 'author')
    if ',' in t:
        sur, giv = [x.strip() for x in t.split(',', 1)]
        t = (giv + ' ' + sur).strip() if giv else sur
        t = close_elisions(t)   # 'Jean d' Ormesson'
    return re.sub(r'\s+', ' ', t).strip() or None
def bologna_copy(rec):
    """The BUB copy-level fields (UNIMARC 316/317/318 + holdings) that make a record *Eco's* copy: inventory ECOnnn, provenance, dedication author,
    annotation note ('Note e decorazioni': ex-libris stamp, underlinings, marginalia, inserts), condition. Returned as book['copy'] for the panel."""
    inv = None
    for h in (rec.get('bub_holdings') or []):
        m = ECO_INV_RE.search(str(h.get('inventario') or h.get('block_id') or ''))
        if m: inv = 'ECO ' + m.group(1); break
    if not inv:
        m = ECO_INV_RE.search(' '.join(rec.get('bub_inventory') or []))
        if m: inv = 'ECO ' + m.group(1)
    prov, dedic = [], []
    for x in (rec.get('bub_provenance_317') or []):
        x = x.strip()
        if x.lower().startswith('autore della dedica'): dedic.append(x.split(':', 1)[1].strip())
        elif x and x not in prov: prov.append(x)
    ann, cond = [], []
    for x in (rec.get('bub_annotation_318') or []):
        x = x.strip()
        head, _, body = x.partition(':')
        if head.lower().startswith('stato di conservazione'): cond.append(body.strip() or x)
        elif head.lower().startswith('note e decorazioni'): ann.append(body.strip() or x)
        elif x: ann.append(x)
    text = ' '.join(ann).lower()
    marks = [k for k, pat in (('ex-libris stamp', r'ex libris|timbro'), ('dedication', r'dedica'), ('underlinings', r'sottolineat'), ('marginalia', r'postill|annotazion|note manoscritt|segni di attenzione'),
                               ('dog-ears', r'orecchi'), ('inserts', r'inserit|allegat|segnalibro|inserti')) if re.search(pat, text)]
    by_eco = [d for d in dedic if ECO_HEADING_RE.match(d)]   # 'Autore della dedica: Eco, Umberto': a dedication Eco wrote in this copy, to someone else; the copy was not given to him
    others = [d for d in dedic if d not in by_eco]
    if by_eco:
        marks = [m for m in marks if m != 'dedication'] + ['dedication by Eco'] if not others else marks
        if others and 'dedication' not in marks: marks.append('dedication')
    elif dedic and 'dedication' not in marks: marks.append('dedication')
    givers = [g for g in (giver_name(d) for d in others) if g]                                   # the givers as a reader names them
    out = {k: v for k, v in dict(inventory=inv, provenance=prov, dedication_by=dedic, givers=givers, inscription=inscription_of(' '.join(ann)), annotation=' '.join(ann) or None, condition=' '.join(cond) or None, marks=marks,
                                 inscribed_by_eco=bool(by_eco) or None, bub_shelfmark=(rec.get('bub_shelfmark') or [None])[0]).items() if v}
    return out or None
ECO_HEADING_RE = re.compile(r'\s*Eco,\s*Umberto\b', re.I)
seen_ids = set(); per_target = collections.defaultdict(list); unknown_n = 0
RULE_HOW = collections.Counter(); RESCUED = []   # records placed only through the 461 set title / responsibility / publisher
UNSHELVED = []   # Bologna records no subject rule places: kept in books[] with placement "unshelved" and no bookcase (the page lists them; they sit on no bay)
for rec in modern:
    if rec['id'] in seen_ids: continue
    seen_ids.add(rec['id'])
    rule, how = classify2(rec)
    if rule: RULE_HITS[rule['name']] += 1; RULE_HOW[how] += 1; targets = expand(rule['bookcase']); note = None if how == 'record' else 'placed through the %s (the record\'s own title is only a volume number or says nothing)' % how
    else: unknown_n += 1; targets = []; note = 'no subject match; not shelved on any bay (the Milan position of this record is unknown)'
    if rule and how != 'record': RESCUED.append(dict(id=rec['id'], title=(rec.get('title') or '')[:50], set_title=parent_title(rec)[:60], rule=rule['name'], bookcase=rule['bookcase'], how=how))
    if rule and not targets: warn('subject rule %r maps to no bookcase' % rule['name']); continue
    langs = rec.get('language') or []
    composed = isbd_title(rec)   # '$a : $e' with the colon the export's title_full drops
    b = dict(id='bologna:' + rec['id'], title=clean_title(composed or rec.get('title_full') or rec.get('title')), author=(rec.get('author') or rec.get('responsibility') or '').replace('_', ' ').strip() or None,
             year=rec.get('year'), publisher=', '.join(rec.get('publisher') or []) or None, place=', '.join(rec.get('place') or []) or None, language=lang_code(langs[0] if langs else None),
             series=', '.join(rec.get('series') or []) or None, subjects=(rec.get('subjects') or []) + (rec.get('dewey_label') or []), dewey=rec.get('dewey') or [],
             origin='catalog', source_kind='catalog', catalog='bologna', source_url=rec.get('permalink') or 'https://sol.unibo.it/SebinaOpac/resource/' + rec['id'],
             confidence='high', placement='inferred' if rule else 'unshelved', placement_rule=rule['name'] if rule else None, placement_match=how, placement_note=note, isbn=(rec.get('isbn') or [None])[0],
             width=round(random.uniform(0.022, 0.04), 4), height=round(random.uniform(0.18, 0.245), 3))
    if composed and composed != (rec.get('title_full') or rec.get('title')): b['title_raw'] = rec.get('title_full') or rec.get('title'); TITLES_COMPOSED.append(dict(id=rec['id'], export=rec.get('title_full'), composed=composed))
    if b['author'] and b['author'].lower().startswith('eco, umberto'): b['author'] = 'Umberto Eco'
    if b['author'] and b['author'].strip().lower() in ('auto-correction', 'autocorrection', 'travail personnel'): b['author'] = None   # a study aid's title words, promoted as a name by the responsibility statement
    set_a, set_ef, set_v = unimarc_461(rec)
    if set_a:   # UNIMARC 461: the set a numbered volume belongs to (its own title may be just '2'): display title '<set>, vol. N'
        part_title_from_responsibility(b, rec)   # '5-1' / 'La chiesa nei tempi moderni' is a part's title, not its author
        apply_volume_title(b, set_a, 'bologna')
        if b.get('part_title'): b['volume_statement'] = clean_title(rec.get('title_full') or rec.get('title'))   # the record's own words stay the statement ('5-1'); the phrase is in part_title
    else: bare_volume_title(b, 'bologna')   # no set in the record, the title the catalogue's bare number and colon ('2: L'Eta romantica')
    cp = bologna_copy(rec)
    if cp:
        cn = COPY_NOTES.get(rec['id'])   # copy_notes_eco.json, a qualification the catalogue's own fields contradict (the giver named cannot be the one who signed)
        if cn:
            if cn.get('giver_note'): cp['giver_note'] = cn['giver_note']
            if cn.get('drop_givers'): cp['givers'] = []; COPY_NOTES_APPLIED.append(dict(id=rec['id'], dropped=cp.get('dedication_by'), note=cn.get('giver_note')))
            cp = {k: v for k, v in cp.items() if v}
        b['copy'] = cp
    if not rule:
        b['bookcase'] = None; b['shelf'] = None; b['slot'] = None; b['section'] = None
        UNSHELVED.append(b); BOOKS.append(b); add_desc(b); continue
    tgt = targets[int(hid(rec['id'], 6), 16) % len(targets)]
    per_target[tgt].append(b)
for tgt, lst in per_target.items():
    lst.sort(key=lambda b: (fold(b.get('author') or '~'), fold(b['title'])))
    for j, b in enumerate(lst):
        if place_spread(tgt, j, len(lst), b): BOOKS.append(b); add_desc(b)
        else: warn('no room on %s for %s' % (tgt, b['id']))
# two or three Bologna records of one title by one author on the same bookcase are distinct copies (another edition or printing,
# or a second record of the same edition): the panel says so ("second copy"), the records are not merged. Same title, different author = different books.
SECOND_COPIES = []
_copies = collections.defaultdict(list)
for b in BOOKS:
    if b.get('catalog') == 'bologna' and b.get('bookcase'): _copies[(b['bookcase'], norm(b['title']), surname(b.get('author')) or '')].append(b)
for _k, lst in _copies.items():
    if len(lst) < 2 or len(lst) > 3: continue
    lst.sort(key=lambda b: (b.get('year') or 0, b['id']))
    for i, b in enumerate(lst):
        others = ', '.join('%s (%s%s)' % (o['id'].split(':')[-1], o.get('year') or 'n.d.', (', ' + o['publisher']) if o.get('publisher') else '') for o in lst if o is not b)
        same_ed = all((o.get('year'), fold(o.get('publisher') or '')) == (b.get('year'), fold(b.get('publisher') or '')) for o in lst)
        txt = ('second copy: ' if i else 'two copies: ') + 'the Bologna catalogue holds another record of this %s on this bookcase, %s' % ('edition' if same_ed else 'title (a different edition or printing)', others)
        b['placement_note'] = ((b['placement_note'] + '; ') if b.get('placement_note') else '') + txt
        b['second_copy'] = bool(i); SECOND_COPIES.append(b['id'])

# ------------------------------------------------------------------ spine readings (video frames + photographs)
CONF = {'high': 3, 'medium': 2, 'low': 1}
def load_jsonl(p):
    out = []
    for line in open(p, encoding='utf-8'):
        line = line.strip()
        if not line: continue
        try: out.append(json.loads(line))
        except Exception: pass
    return out
SP = dict(video_files=[], photo_files=[], frames_by_level=collections.Counter(), rejected_other=[], consolidated_untitled=0, frames=0, frames_unresolved=0, rows=0, readings=0, unlabelled_runs=0, deduped=0, merged_into_catalog=0, placed=0, unplaced=0, pile_deferred_only=0,
          author_only_placed=0, pile_fillers=0, alt_readings=0, alt_preferred=0, piles_with_height=0, pile_copies=0,
          # the heavy spine pass (spines_<video>_dense.jsonl, converted by eco-video/dense/staging/dense_to_spines.py): its entries carry dense_id / dense_tier /
          # dense_reason / dense_match / dense_tag_verified, read here from the raw files and used for the tier and the catalogue links (see DENSE_ENTRY)
          dense_entries=0, dense_readings=0, dense_only_books=0, dense_books_with_first_pass=0, dense_catalog_links=0, dense_catalog_links_failed=0, dense_catalog_upgraded=0,
          dense_catalog_disagree=0, dense_tier_capped=0, dense_certain_unverified=0, dense_pile_books=0, dense_conflict_dropped=0, dense_conflict_readings_lost=0,
          # catalogue matches rejected by the agreement rule, records named / forbidden by wall_map reading_fixes `catalog_record`,
          # working-library readings attached to a Braidense rare-room record, Bologna records moved to (or confirmed on) the bookcase a film sighting names,
          # pile sightings filmed in no room of the flat (dropped, the reading kept in rejected_other with its link)
          catalog_match_rejected=0, catalog_forced=0, catalog_forbidden=0, catalog_braidense_cross_room=0, catalog_moved_to_tag=0, pile_sightings_off_flat=0, pile_readings_off_flat=0, reference_title_on_film=0)
# wall_map_eco.json `reading_fixes`, applied to the consolidated readings as they are ingested (so a corrected title takes part in the merges); the notes are attached after the books are built
READING_FIXES_EARLY = {k: v for k, v in (WM.get('reading_fixes') or {}).items() if isinstance(v, dict)}
photo_path = args.spines_photos or os.path.join(VIDEO_DIR, 'spines_photos.jsonl')   # the project copy only (the fallback to a temporary folder that the first builds used is gone)
frames = []
for p in sorted(glob.glob(args.spines_video)):
    if os.path.basename(p) == 'spines_photos.jsonl': continue
    SP['video_files'].append(p)
    for f in load_jsonl(p): f.setdefault('source_kind', 'video'); f.setdefault('_file', os.path.basename(p)); frames.append(f)
if photo_path and os.path.exists(photo_path):
    SP['photo_files'].append(photo_path)
    for f in load_jsonl(photo_path): f.setdefault('source_kind', 'photo'); f['_file'] = os.path.basename(photo_path); frames.append(f)
frames.sort(key=lambda f: ((f.get('timestamp_s') if isinstance(f.get('timestamp_s'), (int, float)) else 0), f.get('frame') or ''))

def shelf_of(bc, row, label, rows_visible):
    n = bc['shelves']; lab = fold(label)
    if re.match(r'^(bottom|lowest|ultim)', lab) or 'bottom' == lab.strip(): return n - 1
    if re.match(r'^(top|topmost|upper|prim)', lab) or lab.strip() == 'top': return 0
    rv = max(rows_visible or 0, row)
    if rv <= n: return min(n - 1, max(0, row - 1))
    return int(round((row - 1) * (n - 1) / max(1, rv - 1)))

readings = {}   # spine key -> merged reading
PILE_RE = re.compile(r'stack|pile|coffee.?table|piano|table.?closeup|held', re.I)
def frame_room(f):
    for k in ('room_id', 'wall_id'):
        key = fold(f.get(k) or '').strip()
        if key in ROOM_IDS: return key
        if key in ALIAS_ROOM: return ALIAS_ROOM[key]
    for text in (f.get('wall_id') or '', f.get('wall_name') or ''):
        for rx, tgt in PATTERNS:
            if rx.search(text) and str(tgt) in ROOM_IDS: return str(tgt)
    return None
PILES = {}   # (room, pile label) -> pile object
pile_readings = collections.defaultdict(dict)   # pile id -> spine key -> reading
def wall_claim(wall_key, raw):
    """The objects_map `walls` entry (object id, raw_from, raw_to, defer) that takes a reading of `wall_key` at raw second `raw`: the window that
    contains it, else an unwindowed entry, else the first. A `defer` entry is only a fallback: see the consolidated ingest below."""
    cands = [c for c in WALL2OBJ[wall_key] if (obj_by_id(c[0]) or {}).get('kind') == 'pile'] or WALL2OBJ[wall_key]   # a table and its pile may list the same walls: the books go to the pile (the page registers piles as bookcases, not tables)
    return next((c for c in cands if c[1] is not None and isinstance(raw, (int, float)) and c[1] <= raw <= c[2]), None) or next((c for c in cands if c[1] is None), None) or cands[0]
def get_pile(rid, wall_key, label, vid, ts, src_url, raw=None):
    """The pile object for a wall label of a stack/closeup frame: the object that objects_map_eco.json claims for it (`walls`; an entry may be limited
    to a window of raw seconds, so one reader's wall can feed two piles of the same piece of furniture), else one created on the first table of the room.
    The object's room wins over the reader's room_id: the piles read on the salotto piano stay on the piano even where the reader wrote 'study'."""
    if wall_key in WALL2OBJ: return obj_by_id(wall_claim(wall_key, raw)[0])
    pkey = (rid, wall_key)
    if pkey in PILES: return PILES[pkey]
    table = next((o for o in OBJECTS if o['room'] == rid and o['kind'] in ('desk', 'piano')), None)
    pos = None
    if table: pos = [table['x'] + 0.3 * (len([p for p in PILES.values() if p['room'] == rid]) % 3 - 1) - room_of(rid)['origin'][0], table['z'] - room_of(rid)['origin'][1]]
    o = add_object(dict(id='pile:%s:%s' % (rid, slug(wall_key or label, 24)), room=rid, kind='pile', label=re.sub(r'\s*\(.*?\)', '', label)[:60], position=pos,
                        base_y=(table.get('base_y') or 0) + table['size'][1] if table else 0, description='Pile of books seen in the footage: ' + label, video_id=vid, timestamp_s=ts,
                        source_url=src_url or (yt_url(vid, ts) if vid else None), confidence='medium'))
    if o: o['placement'] = 'seen'; o['on'] = table['id'] if table else None; PILES[pkey] = o
    return o
# titles read on the filmed piles (objects_from_video.json) seed the pile readings; the consolidated/raw spine readings merge into them by title
for o in list(OBJECTS):
    for t in o.pop('_titles', []) or []:
        title = (t.get('title') or '').strip()
        if len(title) < 2: continue
        vid = VO.get('video_id'); raw = t.get('_raw'); ts = corrected_ts(vid, raw) if isinstance(raw, (int, float)) else o.get('timestamp_s')
        seed_id = ('video:%s:%d:%s' % (vid, int(raw), slug(title))) if isinstance(raw, (int, float)) else None   # the id this seed would get
        fx = READING_FIXES_EARLY.get(seed_id) if seed_id else None
        if fx:
            t = dict(t, **{k: v for k, v in fx.items() if k in ('title', 'author', 'language')}); title = (t.get('title') or '').strip()
            if len(title) < 2: continue
        sight = dict(kind='video', level='pile', video_id=vid, timestamp_s=ts, timestamp_raw_s=raw, time=hms(ts) if ts is not None else None, url=yt_url(vid, ts) if ts is not None else o.get('source_url'),
                     frame=os.path.basename(t.get('frame') or '') or o.get('frame'), stem=os.path.splitext(os.path.basename(t.get('frame') or 'frame'))[0], credit=None,
                     confidence=t.get('confidence') if t.get('confidence') in CONF else 'low', bookcase=o['id'], shelf=0, slot=len(pile_readings[o['id']]), spine_text=t.get('spine_text'), title=title,
                     author=(t.get('author') or '').strip() or None, language=lang_code(t.get('language')), series=None, publisher=None, room_id=o['room'])
        key = spine_key(title, sight['author']); cur = pile_readings[o['id']].get(key)
        if cur is None: pile_readings[o['id']][key] = dict(sightings=[sight], via='objects_from_video', fixed=bool(fx), **({'id': seed_id} if fx else {})); SP['readings'] += 1   # a corrected seed keeps the id its fix is keyed by
        else:
            cur['sightings'].append(sight); SP['deduped'] += 1
            if fx and not cur.get('id'): cur['id'] = seed_id; cur['fixed'] = True
        if o['kind'] != 'pile': o['kind'] = 'pile'
CONSOL = None
if args.consolidated and os.path.exists(args.consolidated):
    try: CONSOL = json.load(open(args.consolidated, encoding='utf-8'))
    except Exception as e: warn('consolidated books file unreadable, falling back to the raw spine files: %s' % e)
RAW_INDEX = {}   # (frame basename, normalised title) -> (row, row_label, pos, rows_visible, books in row): shelf hints for the consolidated readings
RAW_INDEX_WALL = {}   # the same keyed (frame basename, reader's wall_id, key): two readers of one frame may number the same title differently (the piano piles)
RAW_ROWS = {}    # (frame basename, reader's wall_id) -> dict(items=[(position from the top, raw entry)], n=spines counted, ttb=row read top to bottom, file): the stack frames, for the pile heights
RAW_ENTRY = {}   # (frame basename, reader's wall_id, key) -> (raw entry, spine file): the reader's own entry behind a consolidated sighting (its `read_as`, notes)
def raw_key(title, author):
    """Key of a raw entry / sighting in RAW_INDEX_WALL and RAW_ENTRY: the normalised title, or 'by:<normalised author>' for an author-only reading."""
    return norm(title) if title else ('by:' + norm(author or ''))
for f in frames:
    rows = f.get('rows') or []; rv = f.get('shelf_rows_visible') or max([r.get('row') or 1 for r in rows] or [1])
    fb = os.path.basename(f.get('frame') or ''); wk = fold(f.get('wall_id') or '').strip()
    for r in rows:
        items = []; top = 0
        for k, rd in enumerate(r.get('books') or []):
            top += 1; items.append((top, rd))
            if rd.get('unlabelled'): top += max(1, int(rd.get('count') or 1)) - 1; continue
            if rd.get('title') or rd.get('author'):
                hint = (int(r.get('row') or 1), r.get('row_label'), rd.get('pos') or (k + 1), rv, len(r.get('books') or []))
                key = raw_key(rd.get('title'), rd.get('author'))
                if rd.get('title'): RAW_INDEX.setdefault((fb, key), hint)
                RAW_INDEX_WALL.setdefault((fb, wk, key), hint); RAW_ENTRY.setdefault((fb, wk, key), (rd, f.get('_file')))
        if (f.get('view') or '').lower() in ('stack', 'pile', 'piano') and items:
            RAW_ROWS.setdefault((fb, wk), dict(items=items, n=top, ttb=bool(re.search(r'top to bottom|from the top', fold(r.get('row_label') or ''))), file=f.get('_file')))

def clean_label(s):
    """Visible pile labels: drop the readers' own bracketed working notes ('(dense pass, placed by ...)'), balanced parentheses included."""
    s = s or ''
    while True:
        i = s.find('(dense pass')
        if i < 0: break
        depth = 0; j = i
        while j < len(s):
            if s[j] == '(': depth += 1
            elif s[j] == ')':
                depth -= 1
                if depth == 0: break
            j += 1
        s = (s[:i] + s[j + 1:])
    return re.sub(r'\s+', ' ', s).replace(' :', ':').replace(' ,', ',').strip(' ,;:')

def strip_wall(wid): return re.sub(r'^(?:[A-Za-z0-9_-]{11}|photo):', '', wid or '')
# the heavy pass's audit fields, keyed like RAW_ENTRY but kept apart from it: on a re-read KEEP frame the first pass's entry wins RAW_ENTRY, the dense entry is still found here
DENSE_ENTRY = {}   # (frame basename, reader's wall_id, key) -> the dense entry (dense_id, dense_tier, dense_reason, dense_read_confidence, dense_match, dense_confirms, dense_tag_verified, ...)
DENSE_TIER_RANK = {'certain': 3, 'probable': 2, 'guess': 1}
for f in frames:
    fb = os.path.basename(f.get('frame') or ''); wk = fold(f.get('wall_id') or '').strip(); vid = f.get('video_id') or ''   # keyed by video too (t_000051.jpg exists in both trailers)
    for r in f.get('rows') or []:
        for rd in r.get('books') or []:
            if rd.get('unlabelled') or not rd.get('dense_id') or not (rd.get('title') or rd.get('author')): continue
            if isinstance(f.get('timestamp_true_s'), (int, float)): rd.setdefault('_true_ts', f['timestamp_true_s'])   # a dense frame re-shot inside a first-pass slot links at its own second
            DENSE_ENTRY.setdefault((vid, fb, wk, raw_key(rd.get('title'), rd.get('author'))), rd); SP['dense_entries'] += 1
# same-slot conflicts the dense pass won (dense_to_spines.py, conflicts_resolution.json: higher confidence wins, ties go to the first pass): the dense frame record's
# `dense_conflicts` names the first-pass sighting at that slot with drop_first_pass true; that consolidated sighting is skipped below (the lost pairs never reach the file)
CONFLICT_DROP = {}   # (video_id, first-pass frame basename, reader's wall_id, key) -> the dense id that took the slot
for f in frames:
    for c in f.get('dense_conflicts') or []:
        fp = c.get('first_pass') or {}
        if not c.get('drop_first_pass') or not fp.get('frame'): continue
        CONFLICT_DROP.setdefault((fp.get('video_id') or f.get('video_id'), os.path.basename(fp['frame']), fold(fp.get('wall_id') or '').strip(), raw_key(fp.get('title'), fp.get('author'))), c.get('dense_id'))
def conflict_dropped(vid, frame, wall_id, title, author):
    return bool(CONFLICT_DROP) and (vid, os.path.basename(frame or ''), fold(wall_id or '').strip(), raw_key(title, author)) in CONFLICT_DROP
def dense_of(sight):
    """The dense-pass entry behind a consolidated sighting, as a small dict, or None."""
    e = DENSE_ENTRY.get((sight.get('video_id') or '', os.path.basename(sight.get('frame') or ''), fold(sight.get('wall_id') or '').strip(), raw_key(sight.get('title'), sight.get('author'))))
    if not e: return None
    return dict(id=e.get('dense_id'), tier=e.get('dense_tier') if e.get('dense_tier') in DENSE_TIER_RANK else 'guess', reason=e.get('dense_reason') or '', read_confidence=e.get('dense_read_confidence'),
                match=e.get('dense_match') if isinstance(e.get('dense_match'), dict) else None, confirms=e.get('dense_confirms'), tag_verified=bool(e.get('dense_tag_verified')),
                bookcase_id=e.get('dense_bookcase_id'), basis=e.get('dense_placement_basis'), tags=e.get('dense_tags') or [], true_ts=e.get('_true_ts'))
def dense_summary(ss, best):
    """Per book: the dense ids behind its sightings, the best dense tier, whether the placing (best) sighting is a dense one and its tag was verified."""
    ds = [(s, s.get('dense')) for s in ss if s.get('dense')]
    if not ds: return None
    top = max(ds, key=lambda x: (DENSE_TIER_RANK.get(x[1]['tier'], 0), CONF.get(x[0].get('confidence') or 'low', 1)))[1]
    ids = []
    for _, d in ds:
        if d['id'] and d['id'] not in ids: ids.append(d['id'])
    bd = best.get('dense') if best is not None else None
    return dict(ids=ids, tier=top['tier'], reason=top['reason'], placing=bool(bd), placing_tier=(bd or {}).get('tier'), placing_reason=(bd or {}).get('reason'),
                tag_verified=bool((bd or {}).get('tag_verified')), placing_basis=(bd or {}).get('basis'), tags=(bd or {}).get('tags') or [], sightings=len(ds), first_pass_sightings=len(ss) - len(ds))
EXCLUDE_ROOMS = {fold(x) for x in WM.get('exclude_rooms', ['other'])}
AFTER_MOVE_RE = re.compile(r'bologna|palazzo poggi|biblioteca eco|reinstall')
BOLOGNA_VIDEOS = {vid for vid, v in VIDEOS.items() if re.search(r'bologna reopening|casa a bologna', fold((v.get('title') or '') + ' ' + (v.get('notes') or v.get('note') or '')))}   # the 2026 reopening clips
def after_move(s):
    """True when a sighting's room / wall label says the shelf was filmed in the Bologna reinstallation (2026), not in the Milan flat, or the video is a reopening clip."""
    return bool(AFTER_MOVE_RE.search(fold(s.get('room_id') or '') + ' ' + fold(s.get('wall_id') or ''))) or (s.get('video_id') in BOLOGNA_VIDEOS)
def subject_target(title, author):
    """Bookcase for a reading whose Milan position is unknown (Bologna reinstallation): the subject rules on title/author, else the fallback."""
    rule = classify(dict(title=title, subjects=[], dewey_label=[], series=[], dewey=[], author=author or ''))
    lst = expand(rule['bookcase']) if rule else expand(FALLBACK)
    return (lst[int(hid(norm(title), 6), 16) % len(lst)] if lst else None), (rule['name'] if rule else None)
def consol_sight_is_pile(f):
    targets, level = resolve(f)
    return level == 'pile' or (f.get('view') or '').lower() in ('stack', 'pile', 'piano') or (not targets and PILE_RE.search(f.get('wall_id') or '') is not None)
def consol_sight(rd, f):
    """One consolidated sighting -> a reading sighting with a bookcase/shelf/slot (or a pile), like the raw path builds; None when it resolves nowhere."""
    targets, level = resolve(f)
    is_pile = level == 'pile' or (f.get('view') or '').lower() in ('stack', 'pile', 'piano') or (not targets and PILE_RE.search(f.get('wall_id') or '') is not None)
    kind = f['source_kind']; vid = f.get('video_id'); ts = f.get('timestamp_s')
    src_url = f.get('source_url') or (yt_url(vid, ts) if vid else None)
    stem = os.path.splitext(os.path.basename(f.get('frame') or 'frame'))[0]
    conf = f.get('confidence') or rd.get('best_confidence')
    title = ((f.get('title_as_read') or '').strip() or (rd.get('title') or '')).strip() or None   # None: an author-only reading (placed in piles only)
    if title is None and not is_pile: return None
    base = dict(kind=kind, level=level, rule=None, video_id=vid, timestamp_s=ts, timestamp_raw_s=f.get('timestamp_raw_s'), time=hms(ts) if ts is not None else None, url=src_url, frame=f.get('frame'), stem=stem,
                credit=f.get('source_credit'), confidence=conf if conf in CONF else 'low', spine_text=f.get('spine_text') or None, title=title,
                author=((f.get('author_as_read') or '').strip() or (rd.get('author') or '').strip()) or None, language=lang_code(rd.get('language')), series=rd.get('series'), publisher=rd.get('publisher'), room_id=f.get('room_id'),
                wall_id=f.get('wall_id'), label_note=f.get('_label_note'))
    dn = dense_of(base)
    if dn: base['dense'] = dn
    if dn and vid and isinstance(dn.get('true_ts'), (int, float)) and isinstance(ts, (int, float)) and abs(dn['true_ts'] - ts) > 0.5:   # link at the frame's own second, not the first-pass slot it was filed under
        ts = int(round(dn['true_ts'])); src_url = yt_url(vid, ts); base.update(timestamp_s=ts, time=hms(ts), url=src_url)
    if is_pile:
        rid = frame_room(f) or 'salotto'
        pile = get_pile(rid, fold(f.get('wall_id') or '').strip(), clean_label(f.get('wall_name')) or f.get('wall_id') or 'pile of books', vid, ts, src_url, raw=f.get('timestamp_raw_s'))
        if pile is None: return None
        wk = fold(f.get('wall_id') or '').strip()
        base.update(level='pile', bookcase=pile['id'], shelf=0, slot=0, deferred=bool(wk in WALL2OBJ and wall_claim(wk, f.get('timestamp_raw_s'))[3])); return base
    if level == 'exclude': return None
    if level in ('room', 'fallback') and targets: targets = [targets[int(hid(str(f.get('wall_id') or f.get('room_id')), 6), 16) % len(targets)]]
    if level == 'subject' or not targets:
        bcid, rule_name = subject_target(base['title'], base['author']); base['level'] = 'subject'; base['rule'] = rule_name
        if not bcid: return None
        targets = [bcid]
    hint = RAW_INDEX.get((os.path.basename(f.get('frame') or ''), norm(f.get('title_as_read') or rd['title'])))
    n = len(targets)
    if hint:
        row, row_label, pos, rv, nb = hint; frac = (max(1, pos) - 1) / max(1, nb); k = min(n - 1, int(frac * n)); bcid = targets[k]
        shelf = shelf_of(BC[bcid], row, row_label, rv); slot = int((frac * n - k) * CAP[bcid]); base['shelf_hint'] = True
    else:
        h = int(hid(rd.get('id') or base['title'], 8), 16); bcid = targets[h % n]; shelf = h // 7 % BC[bcid]['shelves']; slot = h // 131 % CAP[bcid]
    base.update(bookcase=bcid, shelf=shelf, slot=slot); return base
if CONSOL is not None:
    items = CONSOL.get('books') if isinstance(CONSOL, dict) else CONSOL
    if not items and isinstance(CONSOL, dict): items = [b for w in CONSOL.get('walls') or [] for b in w.get('books') or []]
    WALLINFO = {w.get('wall_id'): w for w in (CONSOL.get('walls') or [])} if isinstance(CONSOL, dict) else {}
    SP['consolidated'] = os.path.basename(args.consolidated); SP['consolidated_books'] = len(items or []); SP['frames'] = ((CONSOL.get('totals') or {}).get('frames') if isinstance(CONSOL, dict) else None) or 0
    for rd in items or []:
        if not isinstance(rd, dict): continue
        if rd.get('excluded') or rd.get('exclude') or rd.get('is_excluded'):
            SP['rejected_other'].append(dict(title=(rd.get('title') or '').strip() or rd.get('author'), author=rd.get('author'), id=rd.get('id'), reason=rd.get('exclude_reason'), room_id=rd.get('room_id'), wall=strip_wall(rd.get('wall_id'))))
            continue
        # a `reading_fixes` entry for this id is applied now, before the piles are built, so the corrected title/author takes part in the merges
        # (the spine one reader read as "L'inconsolabile pensiero" and two others as "L'innominabile attuale" becomes one book); its note is attached later
        fx = READING_FIXES_EARLY.get(rd.get('id')); fixed = False
        if fx:
            rd = dict(rd)
            for k, v in fx.items():
                if k in ('title', 'author', 'language', 'series', 'publisher'): rd[k] = v; fixed = True
        title = (rd.get('title') or '').strip()
        author_only = len(title) < 2 and bool((rd.get('author') or '').strip())
        if len(title) < 2 and not author_only: SP['consolidated_untitled'] += 1; continue
        if author_only: title = None   # an author-only reading: a pile book with no title (never a shelf slot)
        sights = []; dropped_conf = 0; dropped_off = []
        for s in rd.get('sightings') or []:
            if not isinstance(s, dict) or s.get('excluded'): continue
            kind = s.get('source_kind') or ('photo' if s.get('photo') else 'video'); vid = s.get('video_id')
            raw = s.get('timestamp_raw_s', s.get('timestamp_s'))
            ts = s.get('timestamp_s') if ('timestamp_raw_s' in s and isinstance(s.get('timestamp_s'), (int, float))) else corrected_ts(vid, raw)
            if isinstance(ts, (int, float)): ts = int(round(ts))
            rid = s.get('room_id') or rd.get('room_id'); wid_full = s.get('wall_id') or rd.get('wall_id') or ''; winfo = WALLINFO.get(wid_full) or {}
            if fold(rid or '') in EXCLUDE_ROOMS: continue
            if conflict_dropped(vid, s.get('frame'), strip_wall(wid_full), s.get('title_as_read') or rd.get('title'), s.get('author_as_read') or rd.get('author')): SP['dense_conflict_dropped'] += 1; dropped_conf += 1; continue
            sd = dict(room_id=rid, wall_id=strip_wall(wid_full), wall_name=winfo.get('wall_name') or '', view=s.get('view'), video_id=vid, timestamp_s=ts, timestamp_raw_s=raw,
                      frame=s.get('frame') or s.get('photo'), source_kind=kind, source_url=s.get('source_url'), source_credit=s.get('credit') or s.get('source_credit') or winfo.get('credit'),
                      confidence=s.get('confidence'), title_as_read=None if fixed else s.get('title_as_read'), author_as_read=None if fixed else s.get('author_as_read'), spine_text=s.get('spine_text'))
            # a stack / pile frame in no room of the flat (the Bologna reinstallation, an unidentified room) makes no pile here: the sighting is dropped,
            # the reading kept in rejected_other with its link when nothing else places it (the way other-library books are handled)
            if consol_sight_is_pile(sd) and frame_room(sd) is None: dropped_off.append(sd); SP['pile_sightings_off_flat'] += 1; continue
            sights.append(sd)
        if not sights:
            if dropped_conf: SP['dense_conflict_readings_lost'] += 1
            reason = 'every sighting lost its slot to a dense-pass reading (same-slot conflict, conflicts_resolution.json)' if dropped_conf else 'every sighting excluded or in an excluded room'
            if dropped_off and not dropped_conf: reason = 'pile filmed in no room of the flat (reader room %s); kept as data, not drawn' % (dropped_off[0].get('room_id') or 'unknown'); SP['pile_readings_off_flat'] += 1
            SP['rejected_other'].append(dict(title=title or rd.get('author'), id=rd.get('id'), author=rd.get('author'), reason=reason, url=(dropped_off[0].get('source_url') if dropped_off else None),
                                             room_id=(dropped_off[0].get('room_id') if dropped_off else rd.get('room_id')), wall=strip_wall(rd.get('wall_id')))); continue
        if author_only and not any(consol_sight_is_pile(f) for f in sights): SP['consolidated_untitled'] += 1; continue
        SP['readings'] += 1; SP['rows'] += len(sights)
        recs = [x for x in (consol_sight(rd, f) for f in sights) if x]
        if not recs: SP['frames_unresolved'] += 1; continue
        for x in recs: SP['frames_by_level'][x['level']] += 1
        shelf_recs = [x for x in recs if x['level'] != 'pile']
        if shelf_recs: readings[rd.get('id') or spine_key(title, rd.get('author'))] = dict(sightings=shelf_recs + [x for x in recs if x['level'] == 'pile'], id=rd.get('id'), fixed=fixed)
        else:
            primary = next((x for x in recs if not x.get('deferred')), recs[0])   # a sighting on a deferred wall (objects_map `walls` {"defer": true}) never chooses the pile: the same book read on a per-pile wall does
            if primary.get('deferred'): SP['pile_deferred_only'] += 1
            # one pile book per pile the reading was seen in (a copy in each: the readers list the piles one by one); the deferred sightings follow the first
            groups = collections.OrderedDict()
            for x in recs:
                if not x.get('deferred'): groups.setdefault(x['bookcase'], []).append(x)
            if not groups: groups[primary['bookcase']] = list(recs)
            else: groups[next(iter(groups))].extend([x for x in recs if x.get('deferred')])
            if len(groups) > 1: SP['pile_copies'] += len(groups) - 1
            for gi, (pid, grecs) in enumerate(groups.items()):
                rid = rd.get('id') if gi == 0 or not rd.get('id') else '%s~%s' % (rd['id'], pid.split(':')[-1][-8:])   # a further copy: the same id with the pile as suffix
                key = spine_key(title, rd.get('author')); cur = pile_readings[pid].get(key)
                for i, x in enumerate(grecs): x['slot'] = len(pile_readings[pid])
                if author_only: SP['author_only_placed'] += 1
                if cur is None: pile_readings[pid][key] = dict(sightings=grecs, id=rid, fixed=fixed, author_only=author_only)
                else:
                    cur['sightings'].extend(grecs); SP['deduped'] += 1
                    if rid:
                        if not cur.get('id') or (cur.get('fixed') and not fixed):   # the reading that carries the title natively keeps the id; a corrected one is recorded in merged_ids
                            if cur.get('id'): cur.setdefault('merged_ids', []).append(cur['id'])
                            cur['id'] = rid; cur['fixed'] = fixed
                        elif rid != cur['id']: cur.setdefault('merged_ids', []).append(rid)
                    cur['author_only'] = bool(cur.get('author_only')) and author_only
for f in ([] if CONSOL is not None else frames):
    SP['frames'] += 1
    if f.get('video_id') and f.get('timestamp_s') is not None:
        f['timestamp_raw_s'] = f['timestamp_s']; f['timestamp_s'] = corrected_ts(f['video_id'], f['timestamp_s'])
        if not f.get('source_url') or 'youtube' in (f.get('source_url') or ''): f['source_url'] = yt_url(f['video_id'], f['timestamp_s'])
    if fold(f.get('room_id') or '') in EXCLUDE_ROOMS:
        for row in f.get('rows') or []:
            for rd in row.get('books') or []:
                if rd.get('title'): SP['rejected_other'].append(dict(title=rd['title'], author=rd.get('author'), frame=f.get('frame'), video_id=f.get('video_id'), timestamp_s=f.get('timestamp_s'), wall=f.get('wall_id') or f.get('wall_name')))
        continue
    targets, level = resolve(f)
    is_pile = level == 'pile' or (f.get('view') or '').lower() in ('stack', 'pile', 'piano') or (not targets and PILE_RE.search(f.get('wall_id') or '') is not None)
    if is_pile:
        rid = frame_room(f) or 'salotto'
        label = clean_label(f.get('wall_name')) or f.get('wall_id') or 'pile of books'
        pkey = (rid, fold(f.get('wall_id') or f.get('wall_name') or label).strip())
        if fold(f.get('wall_id') or '').strip() in WALL2OBJ:   # objects_map claims this wall for a pile object (possibly per time window)
            pile = get_pile(rid, fold(f.get('wall_id') or '').strip(), label, f.get('video_id'), f.get('timestamp_s'), f.get('source_url'), raw=f.get('timestamp_raw_s'))
        else:
            if pkey not in PILES:
                table = next((o for o in OBJECTS if o['room'] == rid and o['kind'] in ('desk', 'piano')), None)
                pos = None
                if table: pos = [table['x'] + 0.3 * (len([p for p in PILES.values() if p['room'] == rid]) % 3 - 1), table['z']]; pos = [pos[0] - room_of(rid)['origin'][0], pos[1] - room_of(rid)['origin'][1]]
                o = add_object(dict(id='pile:%s:%s' % (rid, slug(f.get('wall_id') or label, 24)), room=rid, kind='pile', label=re.sub(r'\s*\(.*?\)', '', label)[:60], position=pos,
                                    base_y=table['size'][1] if table else 0, description='Pile of books seen in the footage: ' + label, video_id=f.get('video_id'), timestamp_s=f.get('timestamp_s'),
                                    source_url=f.get('source_url') or (yt_url(f['video_id'], f.get('timestamp_s')) if f.get('video_id') else None), confidence='medium'))
                if o: o['placement'] = 'seen'; o['on'] = table['id'] if table else None; PILES[pkey] = o
            pile = PILES.get(pkey)
        if pile is None: SP['frames_unresolved'] += 1; continue
        SP['frames_by_level']['pile'] += 1
        kind = f.get('source_kind') or 'video'; vid = f.get('video_id'); ts = f.get('timestamp_s')
        src_url = f.get('source_url') or (yt_url(vid, ts) if vid else None)
        stem = os.path.splitext(os.path.basename(f.get('frame') or 'frame'))[0]
        for row in f.get('rows') or []:
            for k, rd in enumerate(row.get('books') or []):
                if rd.get('unlabelled'): continue
                title = (rd.get('title') or '').strip()
                if len(title) < 2 or re.match(r'^\[|^\?+$', title): continue
                SP['readings'] += 1
                sight = dict(kind=kind, level='pile', video_id=vid, timestamp_s=ts, timestamp_raw_s=f.get('timestamp_raw_s'), time=hms(ts) if ts is not None else None, url=src_url, frame=f.get('frame'), stem=stem, credit=f.get('source_credit'),
                             confidence=rd.get('confidence') if rd.get('confidence') in CONF else 'low', bookcase=pile['id'], shelf=0, slot=k, spine_text=rd.get('spine_text'), title=title,
                             author=(rd.get('author') or '').strip() or None, language=lang_code(rd.get('language')), series=rd.get('series'), publisher=rd.get('publisher'), room_id=rid)
                key = spine_key(title, sight['author'])
                cur = pile_readings[pile['id']].get(key)
                if cur is None: pile_readings[pile['id']][key] = dict(sightings=[sight])
                else: SP['deduped'] += 1; cur['sightings'].append(sight)
        continue
    if not targets: SP['frames_unresolved'] += 1; continue
    if level in ('room', 'fallback'):   # only the room is known: one bookcase of it per wall label, and the placement is inferred
        targets = [targets[int(hid(str(f.get('wall_id') or f.get('room_id')), 6), 16) % len(targets)]]
    SP['frames_by_level'][level] += 1
    if level == 'exclude': SP['frames_unresolved'] += 1; continue
    kind = f.get('source_kind') or ('photo' if f.get('timestamp_s') is None else 'video')
    vid = f.get('video_id'); ts = f.get('timestamp_s')
    src_url = f.get('source_url') or (yt_url(vid, ts) if vid else None)
    stem = os.path.splitext(os.path.basename(f.get('frame') or 'frame'))[0]
    rows_visible = f.get('shelf_rows_visible') or max([r.get('row') or 1 for r in f.get('rows') or []] or [1])
    for row in f.get('rows') or []:
        SP['rows'] += 1
        books = row.get('books') or []
        total = sum(max(1, int(b.get('count') or 1)) if b.get('unlabelled') else 1 for b in books) or 1
        cursor = 0
        for rd in books:
            if rd.get('unlabelled'):
                SP['unlabelled_runs'] += 1; cursor += max(1, int(rd.get('count') or 1)); continue
            title = (rd.get('title') or '').strip()
            if len(title) < 2 or re.match(r'^\[|^\?+$', title): continue
            if conflict_dropped(vid, f.get('frame'), f.get('wall_id'), title, rd.get('author')): SP['dense_conflict_dropped'] += 1; continue
            SP['readings'] += 1
            pos = rd.get('pos')
            frac = ((pos - 1) if isinstance(pos, (int, float)) and pos else cursor) / total
            cursor = (pos if isinstance(pos, (int, float)) and pos else cursor + 1)
            rule_name = None
            if level == 'subject':
                bcid, rule_name = subject_target(title, rd.get('author'))
                if not bcid: continue
                n, k, frac = 1, 0, 0.0
            else: n = len(targets); k = min(n - 1, int(frac * n)); bcid = targets[k]
            bc = BC[bcid]
            shelf = shelf_of(bc, int(row.get('row') or 1), row.get('row_label'), rows_visible)
            slot = int((frac * n - k) * CAP[bcid])
            sight = dict(kind=kind, level=level, rule=rule_name, video_id=vid, timestamp_s=ts, timestamp_raw_s=f.get('timestamp_raw_s'), time=hms(ts) if ts is not None else None, url=src_url, frame=f.get('frame'), stem=stem,
                         credit=f.get('source_credit'), confidence=rd.get('confidence') if rd.get('confidence') in CONF else 'low', bookcase=bcid, shelf=shelf, slot=slot,
                         spine_text=rd.get('spine_text'), title=title, author=(rd.get('author') or '').strip() or None, language=lang_code(rd.get('language')),
                         series=rd.get('series'), publisher=rd.get('publisher'), room_id=f.get('room_id'), label_note=f.get('_label_note'))
            key = spine_key(title, sight['author'])
            cur = readings.get(key)
            if cur is None: readings[key] = dict(sightings=[sight]); continue
            SP['deduped'] += 1; cur['sightings'].append(sight)

def best_sighting(ss):
    return sorted(ss, key=lambda s: (-CONF[s['confidence']], s['timestamp_s'] if s['timestamp_s'] is not None else 1e12, s['frame'] or ''))[0]
LEVEL_RANK = {'bookcase': 2, 'wall': 2, 'label': 1}   # a sighting whose reader's wall names a bookcase that exists (a Fondazione letter, a call tag) places the book before any room- or subject-level guess
def names_bookcase(s):
    """True when the sighting's own reader named the bookcase: its level is bookcase / wall and, for a dense sighting, the pass placed it by a tag or a
    first-pass label (dense_bookcase_id) rather than a room guess filed under a reused wall label."""
    d = s.get('dense')
    return s.get('level') in ('bookcase', 'wall') and not (d and not d.get('bookcase_id'))
def placing_sighting(ss):
    """The sighting that places a shelf reading: the most specific level first (bookcase / wall, then a subject tab, then room and subject guesses alike), then the clearest reading, then the earliest."""
    return sorted(ss, key=lambda s: (-(LEVEL_RANK.get(s.get('level'), 0) if (names_bookcase(s) or s.get('level') == 'label') else 0), -CONF[s['confidence']], s['timestamp_s'] if s['timestamp_s'] is not None else 1e12, s['frame'] or ''))[0]
def earliest(ss):
    vids = [s for s in ss if s['kind'] == 'video']
    return sorted(vids, key=lambda s: (s['timestamp_s'] or 0, s['frame'] or ''))[0] if vids else sorted(ss, key=lambda s: s['frame'] or '')[0]

# merge readings that name a catalogued book (same room kind: rare readings against Braidense, others against Bologna)
CAT_INDEX = collections.defaultdict(list)
for b in BOOKS:
    for t in ({norm(b['title'])} | ({norm(b['title'].split(':')[0])} if ':' in b['title'] else set())): CAT_INDEX[t].append(b)
CAT_TOK = [(tokens(b['title']), b) for b in BOOKS if len(tokens(b['title'])) >= 2]
def match_agrees(title, author, rec):
    """The agreement a catalogue match must show before a sighting is attached to the record: the reading's author surname in the
    record's author or title, or the whole normalised title, or at least two significant title words (4+ letters, stop words dropped) shared.
    A single shared word (the dense matcher's 'Aufstieg und Niedergang' -> Prost's 'Les sciences et les arts occultes, vol. 1') never attaches."""
    rt = (rec.get('author') or '') + ' ' + (rec.get('title') or '')
    if author and any(sur_hit(x, rt) for x in (surname(author), (fold(author).split() or [''])[-1]) if x): return True
    nt = norm(title)
    if nt and nt == norm(rec.get('title') or ''): return True
    T = {t for t in tokens(re.sub(r'\(.*?\)', ' ', title)) | tokens(title) if len(t) >= 4}
    return len(T & {t for t in tokens(rec.get('title') or '') if len(t) >= 4}) >= 2
CATALOG_REJECTED = []   # (reading title, record id, record title): dense matches the agreement rule refused
def sur_hit(sur, text):
    """The surname as a word of the text, allowing a Latin or Italian ending ('Kircher' / 'Kircheri', 'Aristotle' / 'Aristotele'): the same first
    seven letters and a length within three. A bare prefix inside a longer word never counts ('Philostratus' is not 'philosophica', 'Kant' is not 'Kantiana')."""
    key = max(norm(sur or '').split() or [''], key=len)
    if len(key) < 3: return False
    for w in norm(text).split():
        if w == key or (len(key) >= 5 and w.startswith(key[:7]) and abs(len(w) - len(key)) <= 3): return True
    return False
def match_catalog(title, author, rare_room, cross=False):
    """The catalogue record a spine reading names, or None. Exact normalised title first. Otherwise token overlap on the reading's
    significant tokens (4+ letters, exact token equality): in the rare room, where the photographs are captioned highlight volumes
    and the Braidense catalogue is complete, a share >= 0.5 (>= 0.34 with the author's surname in the record) of at least two
    tokens, or one token plus the surname; in the working library, where only a tenth of the books are catalogued, at least two
    tokens with a share >= 0.75 and the surname when the reading has an author. Best score wins.
    `cross`: a working-library reading tried against the Braidense rare-room records, so that a folio read on a working shelf
    is the catalogue copy and not a second, guessed book: at least two shared words with a share >= 0.5 and the surname, or three shared words."""
    nt = norm(title)
    cands = [b for b in CAT_INDEX.get(nt, []) if bool(b.get('rare')) == rare_room]
    sur = (surname(author) or (fold(author).split() or [''])[-1]) if author and fold(author).split() else None   # surname() drops parentheticals ('Kircher (Kircheri)') and handles 'Surname, Given'; matched as a word by sur_hit
    if cands:
        if sur: cands = [b for b in cands if sur_hit(sur, (b.get('author') or '') + ' ' + b['title'])] or cands
        cands = [b for b in cands if match_agrees(title, author, b)]   # a prefix before ':' that is one word does not attach
        if cands: return cands[0]
    T = {t for t in tokens(re.sub(r'\(.*?\)', ' ', title)) | tokens(title) if len(t) >= 4}
    if not T: return None
    best, bs = None, 0
    for toks, b in CAT_TOK:
        if bool(b.get('rare')) != rare_room: continue
        hit = len(T & toks); ratio = hit / len(T)
        has_sur = bool(sur and sur_hit(sur, (b.get('author') or '') + ' ' + b['title']))
        if cross:   # the surname must be the record's author or head its Latin title ('Athanasii Kircheri ...'), not a name the title is about ('Delle donne fiorentine di Dante Alighieri')
            strong = bool(sur and (sur_hit(sur, b.get('author') or '') or sur_hit(sur, ' '.join(fold(b['title']).split()[:3]))))
            ok = hit >= 2 and ratio >= 0.5 and (strong or (not sur and (hit >= 3 or ratio >= 1.0)) or (hit >= 3 and ratio >= 0.75))
        elif rare_room: ok = (hit >= 2 and (ratio >= 0.5 or (has_sur and ratio >= 0.34))) or (hit == 1 and has_sur)
        else: ok = hit >= 2 and ratio >= 0.75 and (has_sur or not sur) and hit / len(toks) >= 0.6   # the record's own title must be mostly covered too: 'Critica della ragion pura' is not 'Kant oggi nel bicentenario della Critica della ragion pura'
        sc = ratio + (0.5 if has_sur else 0) + hit / 100   # at an equal share, the record sharing more words wins
        if ok and sc > bs: best, bs = b, sc
    return best

# one physical sighting group = one placement (a): a work read twice with different spellings, or once on film and once in the Fondazione
# photograph of the same bay, whose best sightings land on the same layout unit is one book with all its sightings
SP['merged_same_bay'] = 0
_groups = {}
for key, rd in list(readings.items()):
    ss = rd['sightings']; shelf_ss = [s for s in ss if s.get('level') != 'pile'] or ss; best = best_sighting(shelf_ss); pl = placing_sighting(shelf_ss)
    wk = work_key(best['title'], best['author'])
    if not wk.split('|')[0]: continue
    unit = BC[pl['bookcase']]['layout_id'] if pl['bookcase'] in BC else pl['bookcase']
    prev = _groups.get((wk, unit))
    if prev is not None and prev is not rd:
        if prev.get('fixed') and not rd.get('fixed') and rd.get('id') and prev.get('id'):   # as in the piles, the reading that carries the title natively keeps the id; the corrected one goes to merged_ids
            prev.setdefault('merged_ids', []).append(prev['id']); prev['id'] = rd['id']; prev['fixed'] = False
        else: prev.setdefault('merged_ids', []).append(rd.get('id') or key)
        prev['sightings'].extend(ss); SP['merged_same_bay'] += 1; del readings[key]
    else: _groups[(wk, unit)] = rd
# (a) again for the piles: the same title read in two piles of one room within a minute of film is one book; the pile the object inventory
# names for it wins (the inventory says lid or keyboard shelf), else the pile read first
SP['merged_across_piles'] = 0
_PILE_ROOM = {o['id']: o['room'] for o in OBJECTS}
_pindex = collections.defaultdict(list)   # (room, title tokens) -> [(surname or '', pile id, key)]: a missing author is a wildcard on the same title (as in the consolidation's dedupe)
for pid in list(pile_readings):
    for key, rd in list(pile_readings[pid].items()):
        ss = rd['sightings']; best = best_sighting(ss)
        wk = work_key(best['title'], best['author']); tpart, sur = wk.split('|')[0], wk.split('|')[-1]
        if not tpart: continue
        rk = (_PILE_ROOM.get(pid), tpart); merged = False
        for psur, ppid, pkey in list(_pindex.get(rk) or []):
            if (ppid, pkey) == (pid, key) or (sur and psur and sur != psur) or pkey not in pile_readings.get(ppid, {}): continue
            prd = pile_readings[ppid][pkey]
            near = ppid == pid or any(a['kind'] == 'video' and b_['kind'] == 'video' and a['video_id'] == b_['video_id'] and abs((a['timestamp_s'] or 0) - (b_['timestamp_s'] or 0)) <= 60 for a in ss for b_ in prd['sightings'])
            if not near: continue
            def _own(r_, p_): return any(s.get('bookcase') == p_ and not s.get('deferred') for s in r_['sightings'])
            if ppid != pid and _own(rd, pid) and _own(prd, ppid) and rd.get('via') != 'objects_from_video' and prd.get('via') != 'objects_from_video': continue
            # the survivor: the inventory-seeded reading; else the one read on its own (non-deferred) pile; else the one with an author; else the first indexed
            rd_wins = (rd.get('via') == 'objects_from_video' and prd.get('via') != 'objects_from_video') or \
                      (prd.get('via') != 'objects_from_video' and ((_own(rd, pid) and not _own(prd, ppid)) or (_own(rd, pid) == _own(prd, ppid) and sur and not psur)))
            win, lose = (rd, prd) if rd_wins else (prd, rd)
            win['sightings'].extend(lose['sightings'])
            if lose.get('id') and lose['id'] != win.get('id'): win.setdefault('merged_ids', []).append(lose['id'])
            for m in lose.get('merged_ids') or []:
                if m != win.get('id') and m not in (win.get('merged_ids') or []): win.setdefault('merged_ids', []).append(m)
            win['id'] = win.get('id') or lose.get('id'); win['author_only'] = bool(win.get('author_only')) and bool(lose.get('author_only'))
            if rd_wins: del pile_readings[ppid][pkey]; _pindex[rk].remove((psur, ppid, pkey)); _pindex[rk].append((sur or psur, pid, key))
            else:
                del pile_readings[pid][key]
                if not psur and sur: _pindex[rk].remove((psur, ppid, pkey)); _pindex[rk].append((sur, ppid, pkey))
            SP['merged_across_piles'] += 1; merged = True; break
        if not merged: _pindex[rk].append((sur, pid, key))

spine_books = []
_BY_ID = {b['id']: b for b in BOOKS}   # the catalogue records, for the dense pass's own matches (braidense:<bid> / bologna:<UBO id>)
for _a, _t in RARE_ID_ALIAS.items():
    if _t in _BY_ID: _BY_ID.setdefault(_a, _BY_ID[_t])   # a set record's id names its first volume
DENSE_TIER_CHANGES = []
def dense_catalog(ss):
    """The catalogue record the heavy pass matched a reading to (rapidfuzz, author-aware): an exact / title+author match of any score >= 70, or a title-only match
    of score >= 90, on a braidense: or bologna: id that exists. Author-only matches (the same author, another title) and notable: ids never link."""
    for s in ss:
        m = (s.get('dense') or {}).get('match')
        if not m or not m.get('id') or m.get('source') not in ('braidense', 'bologna'): continue
        kind, score = m.get('kind'), float(m.get('score') or 0)
        if not ((kind in ('exact', 'title+author') and score >= 70) or (kind == 'title' and score >= 90)): continue
        rec = _BY_ID.get(m['id'])
        if rec is not None and rec.get('origin') == 'catalog':
            if not match_agrees(s.get('title') or '', s.get('author'), rec):
                SP['catalog_match_rejected'] += 1; CATALOG_REJECTED.append((s.get('title'), rec['id'], (rec.get('title') or '')[:60])); continue
            return rec, m
        SP['dense_catalog_links_failed'] += 1
    return None, None
CATALOG_MOVED = []   # (record id, from bookcase, to bookcase, reading title, time): Bologna records moved to the bookcase a film sighting names
CATALOG_CROSS = []   # (reading id, record id, record shelfmark, reading bookcase): working-library readings attached to a Braidense rare-room record
for key, rd in readings.items():
    ss = rd['sightings']; shelf_ss = [s for s in ss if s.get('level') != 'pile'] or ss; best = best_sighting(shelf_ss); pl = placing_sighting(shelf_ss); first = earliest(ss)   # best: the clearest reading (title, author, confidence); pl: the sighting that places it
    rare_room = pl['bookcase'].startswith('rare') or any(s['bookcase'].startswith('rare') for s in shelf_ss)   # any rare-room sighting -> the Braidense rule
    cat, dmatch = dense_catalog(ss)
    if cat is not None: SP['dense_catalog_links'] += 1
    else: cat = match_catalog(best['title'], best['author'], rare_room)
    if cat is None and not rare_room and pl['bookcase'] in BC:   # a folio read on a working shelf that names a Braidense record is that record, not a second guessed book
        cat = match_catalog(best['title'], best['author'], True, cross=True)
        if cat is not None: SP['catalog_braidense_cross_room'] += 1; CATALOG_CROSS.append((rd.get('id') or key, cat['id'], cat.get('shelfmark'), pl['bookcase'], best['title'], best['author'], (cat.get('title') or '')[:70]))
    # wall_map_eco.json reading_fixes may name the record a reading is (`catalog_record: "braidense:<bid>"`) or forbid any match (`catalog_record: false`)
    forced = next((READING_FIXES_EARLY[k]['catalog_record'] for k in [rd.get('id')] + (rd.get('merged_ids') or []) if k in READING_FIXES_EARLY and 'catalog_record' in READING_FIXES_EARLY[k]), None)
    if forced is False: cat, dmatch = None, None; SP['catalog_forbidden'] += 1
    elif isinstance(forced, str):
        rec = _BY_ID.get(forced)
        if rec is not None and rec.get('origin') == 'catalog': cat, dmatch = rec, None; SP['catalog_forced'] += 1
        else: warn('reading_fixes: catalog_record %s names no catalogue record' % forced)
    if cat is not None and cat.get('placement') == 'reference':   # a title read on a shelf of the flat is a copy in the flat, drawn where it was read; the library's ECO.04 reference copy is not that copy
        _s0 = next((s for s in shelf_ss if s.get('kind') == 'video' and s.get('time')), None)
        if _s0 and not cat.get('title_seen_on_film'):
            cat['title_seen_on_film'] = dict(time=_s0.get('time'), url=_s0.get('url'), video_id=_s0.get('video_id'), bookcase=_s0.get('bookcase'), level=_s0.get('level'))
            cat['placement_note'] = (cat.get('placement_note') or '') + ' A copy of this title appears in the film at %s; whether it is this copy is not established.' % _s0.get('time')
        if CATALOG_CROSS and CATALOG_CROSS[-1][1] == cat['id'] and CATALOG_CROSS[-1][0] == (rd.get('id') or key): CATALOG_CROSS.pop(); SP['catalog_braidense_cross_room'] -= 1
        SP['reference_title_on_film'] += 1; cat, dmatch = None, None
    sightings = [dict(kind=s['kind'], video_id=s['video_id'], timestamp_s=s['timestamp_s'], timestamp_raw_s=s.get('timestamp_raw_s'), time=s['time'], url=s['url'], frame=s['frame'], credit=s['credit'], confidence=s['confidence'], bookcase=s['bookcase'], level=s.get('level'),
                      **({'dense_id': s['dense']['id'], 'dense_tier': s['dense']['tier']} if s.get('dense') else {})) for s in ss]
    dsum = dense_summary(ss, best)
    if dsum:
        SP['dense_readings'] += 1
        if dsum['first_pass_sightings']: SP['dense_books_with_first_pass'] += 1
        else: SP['dense_only_books'] += 1
    if cat is not None:
        SP['merged_into_catalog'] += 1
        cat.setdefault('sightings', []).extend(sightings); cat['also_seen'] = True
        if rd.get('id'): cat.setdefault('merged_ids', []).append(rd['id'])
        for s in ss:
            if s['kind'] == 'video' and s['level'] in ('bookcase', 'wall', 'label', 'context'): ON_CAMERA.add(s['bookcase'])
        if not cat.get('spine_text') and best.get('spine_text'): cat['spine_text'] = best['spine_text']
        if dsum:
            for i in dsum['ids']:
                if i not in (cat.get('dense_ids') or []): cat.setdefault('dense_ids', []).append(i)
            if dmatch: cat['dense_match'] = dict(kind=dmatch.get('kind'), score=dmatch.get('score'))
        # a reader's bookcase tag beats the subject rule. A Bologna record placed by subject moves to the bookcase a film sighting names (the reader's
        # wall names a Fondazione letter or a call tag of a bookcase that exists) and becomes "seen"; its tier is decided in dense_tier_cap (certain only when the
        # tag is verified, as for video books). A Braidense record stays where its shelfmark places it; a sighting elsewhere is recorded (seen_elsewhere) and reported.
        _bcn = lambda x: (BC[x].get('fondazione_bay') or x) if x in BC else x
        tagged = [s for s in ss if s['kind'] == 'video' and s['level'] == 'bookcase' and names_bookcase(s) and s['bookcase'] in BC and BC_ROOM.get(s['bookcase']) in WORKING_ROOMS]
        if tagged and cat.get('catalog') == 'bologna' and cat.get('placement') == 'inferred':
            s = sorted(tagged, key=lambda s: (-CONF[s['confidence']], s['timestamp_s'] if s['timestamp_s'] is not None else 1e12))[0]; d = s.get('dense') or {}
            old = cat.get('bookcase'); moved = s['bookcase'] != old
            if not moved or move_book(cat, s['bookcase'], s['shelf'], s['slot']):
                how = s.get('label_note') or (('call tag ' + ', '.join(d.get('tags'))) if d.get('tags') else "the reader's wall label names the bookcase")
                cat['placement'] = 'seen'; cat['confidence'] = s['confidence']; cat['seen_on_film_agrees'] = not moved
                cat['seen_by_tag'] = dict(bookcase=s['bookcase'], time=s.get('time'), url=s.get('url'), video_id=s.get('video_id'), how=how, tags=d.get('tags') or [], dense_id=d.get('id'), dense_tier=d.get('tier'),
                                          tag_verified=bool(d.get('tag_verified')), moved_from=old if moved else None, rule=cat.get('placement_rule'), after_move=after_move(s))
                cat['placement_note'] = 'read %s at %s on bookcase %s (%s)%s' % ('in the Bologna reinstallation, which keeps the Milan tags,' if after_move(s) else 'on film', s.get('time'), _bcn(s['bookcase']), how,
                    ('; the subject rule %r had placed this record on bookcase %s' % (cat.get('placement_rule'), _bcn(old))) if moved else (', where the subject rule %r had already placed this record' % cat.get('placement_rule')))
                if moved: SP['catalog_moved_to_tag'] += 1; CATALOG_MOVED.append((cat['id'], old, s['bookcase'], best['title'], s.get('time')))
                else: SP['dense_catalog_upgraded'] += 1
            else: warn('no free slot to move %s to %s' % (cat['id'], s['bookcase']))
        elif cat.get('placement') == 'catalogued':
            for s in ss:
                if s['kind'] != 'video' or s['bookcase'] == cat.get('bookcase') or s['bookcase'] not in BC or cat.get('seen_elsewhere'): continue
                d = s.get('dense') or {}
                cat['seen_elsewhere'] = dict(bookcase=s['bookcase'], level=s.get('level'), time=s.get('time'), url=s.get('url'), video_id=s.get('video_id'), tags=d.get('tags') or [], dense_id=d.get('id'))
                _room = lambda x: (BC.get(x) or {}).get('room_id') or (BC.get(x) or {}).get('room')
                if s.get('level') == 'subject':   # a shot naming no room says so, instead of naming the bookcase the subject rule guessed
                    where = 'the film shows this title at %s in a shot that names no room or bookcase' % s.get('time')
                elif s.get('level') in ('room', 'fallback') and _room(s['bookcase']) and _room(s['bookcase']) == _room(cat.get('bookcase')):
                    where = 'the film shows this title at %s in the same room (the shot names no bookcase)' % s.get('time')
                else:
                    where = 'the film shows this title at %s on bookcase %s (%s)' % (s.get('time'), _bcn(s['bookcase']), s.get('label_note') or ('call tag ' + ', '.join(d.get('tags')) if d.get('tags') else ('the bookcase is a guess from the room' if s.get('level') in ('room', 'fallback') else 'the reader named the bookcase')))
                cat['placement_note'] = ((cat.get('placement_note') or '') + '; ' if cat.get('placement_note') else '') + where + '; the record stays where its shelfmark places it'
                SP['dense_catalog_disagree'] += 1
        continue
    kind = first['kind']
    bid = rd.get('id') or (('video:%s:%d:%s' % (first['video_id'], int(first['timestamp_raw_s'] if first.get('timestamp_raw_s') is not None else (first['timestamp_s'] or 0)), slug(best['title']))) if kind == 'video' else ('photo:%s:%s' % (first['stem'], slug(best['title']))))
    for s in ss:
        if s['kind'] == 'video' and s['level'] in ('bookcase', 'wall', 'pile', 'label', 'context'): ON_CAMERA.add(s['bookcase'])
    prim = best_sighting([s for s in ss if s['kind'] == 'video'] or ss) if kind == 'video' else first   # the primary link is the clearest sighting (the id stays with the earliest)
    b = dict(id=bid, title=best['title'], author=best['author'], language=best['language'] or next((s['language'] for s in ss if s['language']), None),
             series=best['series'], publisher=best['publisher'], spine_text=best['spine_text'], origin=kind, source_kind=kind, confidence=best['confidence'],
             placement='seen' if names_bookcase(pl) else 'inferred', source_url=prim['url'], sightings=sightings, frames_seen=len(ss),
             width=round(random.uniform(0.024, 0.038), 4), height=round(random.uniform(0.18, 0.245), 3))
    if kind == 'video': b.update(video_id=prim['video_id'], timestamp_s=prim['timestamp_s'], timestamp_raw_s=prim.get('timestamp_raw_s'), time=prim['time'], video_title=(VIDEOS.get(prim['video_id']) or {}).get('title'))
    else: b.update(photo_credit=first['credit'], frame=first['frame'])
    if pl.get('label_note') and pl['level'] in ('bookcase', 'label'): b['shelf_label'] = pl['label_note']
    if b['placement'] == 'inferred':
        b['placement_note'] = ('the reading names only the room (%s); the bookcase is a guess' % (pl['room_id'] or 'unknown')) if pl['level'] == 'room' else \
            ('placed from the %s in the frame, which names a subject rather than a bay; the bookcase whose Fondazione caption fits is inferred' % (pl.get('label_note') or 'shelf label')) if pl['level'] == 'label' else \
            (('seen after the move to Bologna; the Milan bookcase is inferred from the subject (%s)' if after_move(pl) else 'the shot shows no room or shelf label; the bookcase is inferred from the subject (%s)') % (pl.get('rule') or 'no subject rule matches the reading, so it is shown on a bookcase of the room')) if pl['level'] == 'subject' else \
            (('read in the Bologna reinstallation at %s; no Milan shelf tag is in the shot, and bookcase %s is inferred from the shot\'s context' if after_move(pl) else 'read on film at %s; the shot shows no shelf tag, and bookcase %s is inferred from the shot\'s context') % (pl.get('time') or 'an unrecorded second', _bcn(pl['bookcase'])))   # a title read in a shot of the flat whose bookcase the reader took from the shot's context (the Louisiana clip's shelf of Eco's own works) said "seen in the Bologna reconstruction", which the clip is not
    if b['placement'] == 'seen' and pl.get('label_note'): b['placement_note'] = 'placed on the bay named by the %s visible in the frame' % pl['label_note']
    if b['placement'] == 'seen' and pl['kind'] == 'video' and after_move(pl):   # a tag read in the Bologna reinstallation names the Milan bookcase (the shelves keep their tags) but is not a reading in the flat
        b['seen_after_move'] = True; b['placement_note'] = 'read in the Bologna reinstallation at a shelf carrying the Milan tag of this bookcase (%s); the bookcase is the tag\'s, the shelf is not the flat\'s' % (pl.get('label_note') or 'the shelf tag names the bookcase')
    variants = sorted({s['title'] for s in ss if s['title'] != best['title']})
    if variants: b['title_variants'] = variants
    if rd.get('merged_ids'): b['merged_ids'] = rd['merged_ids']
    if dsum: b['dense'] = dsum; b['dense_ids'] = dsum['ids']
    b['_target'] = (pl['bookcase'], pl['shelf'], pl['slot'])
    spine_books.append(b)
spine_books.sort(key=lambda b: (-CONF[b['confidence']], b['id']))
for b in spine_books:
    bcid, sh, sl = b.pop('_target')
    if place(bcid, sh, sl, b): SP['placed'] += 1; BOOKS.append(b); add_desc(b)
    else: SP['unplaced'] += 1; warn('no free slot for spine reading %s on %s' % (b['id'], bcid))

# pile books: one book per distinct title in each pile, stacked as the reader saw them: a stack frame's row read "top to bottom" gives each title a
# `pos` from the top (raw spine files, RAW_INDEX), so the largest pos is the bottom of the pile (slot 0); titles with no such position go beneath, in reading order
def stack_pos(rd, pid):
    """Position from the top of the pile of a pile reading: the smallest raw `pos` of its sightings on a stack frame whose row is read top to bottom
    (preferring the sightings the objects map placed on this very pile); None when no frame gives one."""
    own = [s for s in rd['sightings'] if s.get('bookcase') == pid]; ss = [s for s in own if not s.get('deferred')] or own or rd['sightings']; best = None   # a deferred (fallback) sighting numbers the pile by another reader's rows
    for walled in (True, False):   # the sightings that name their wall first; the un-walled index (first reader of the frame) only when none of them gives a position
        for s in ss:
            fb, nt = os.path.basename(s.get('frame') or ''), norm(s.get('title') or '')
            h = RAW_INDEX_WALL.get((fb, fold(s.get('wall_id') or '').strip(), nt)) if walled else RAW_INDEX.get((fb, nt))
            if h and re.search(r'top to bottom|from the top', fold(h[1] or '')): best = h[2] if best is None else min(best, h[2])
        if best is not None: break
    return best
def pile_rows(pid, rds):
    """The stack rows (RAW_ROWS) behind the readings placed on pile `pid`, fullest count first (the second, 1080p reading of the piano piles counts every spine)."""
    keys = []
    for rd in rds.values():
        for s in rd['sightings']:
            if s.get('bookcase') != pid or s.get('deferred'): continue
            k = (os.path.basename(s.get('frame') or ''), fold(s.get('wall_id') or '').strip())
            if k in RAW_ROWS and k not in keys: keys.append(k)
    return sorted((RAW_ROWS[k] for k in keys), key=lambda r: (-r['n'], r.get('file') or ''))
def row_position(row, title, author):
    """Position from the top of a reading in a raw stack row: by title, else (a reading whose title another pass supplied) by the author-only entry of that author; None when the row does not list it."""
    if not row.get('ttb'): return None
    keys = [raw_key(title, author)] + (['by:' + norm(author)] if title and author else [])
    for key in keys:
        hits = [top for top, rd in row['items'] if not rd.get('unlabelled') and raw_key(rd.get('title'), rd.get('author')) == key]
        if hits and (key.startswith('by:') is False or len(hits) == 1): return min(hits)
    return None
def effective_readings(rd):
    """What each sighting of a pile book actually read: the sighting's title/author, or the reader's `read_as` where the entry was aligned to another
    reading's spelling so that the consolidation merged them. Sorted: highest confidence first, then the earliest frame, then the first reading's file."""
    out = []
    for s in rd['sightings']:
        ent = RAW_ENTRY.get((os.path.basename(s.get('frame') or ''), fold(s.get('wall_id') or '').strip(), raw_key(s.get('title'), s.get('author'))))
        ra = ent[0].get('read_as') if ent and isinstance(ent[0].get('read_as'), dict) else None
        t = ((ra.get('title') if 'title' in ra else s.get('title')) if ra else s.get('title')) or None
        a = ((ra.get('author') if 'author' in ra else s.get('author')) if ra else s.get('author')) or None
        out.append(dict(title=t, author=a, confidence=s['confidence'], spine_text=s.get('spine_text'), frame=s.get('frame'), video_id=s.get('video_id'), timestamp_s=s.get('timestamp_s'), time=s.get('time'), url=s.get('url'),
                        source=ent[1] if ent else None, _s=s, _alt=bool(ra)))
    out.sort(key=lambda e: (-CONF.get(e['confidence'], 0), e['timestamp_s'] if e['timestamp_s'] is not None else 1e12, e.get('source') or '', e.get('frame') or ''))
    return out
def alt_label(a):
    src = 'second reading, sharper frames' if 'heavy' in (a.get('source') or '') else 'first reading'   # no upload jargon in the panel
    return '%s%s (%s confidence, %s%s)' % (a.get('title') or '[title not readable]', (' \u2014 ' + a['author']) if a.get('author') else '', a.get('confidence') or 'low', src, (' at ' + a['time']) if a.get('time') else '')
# ------------------------------------------------------------------ piles stacked from the film reference (eco-video/piano_piles.json)
# The reference lists every spine of each piano pile top to bottom as read from the 5-fps 1080p frames: titled entries, untitled entries (an author, a
# publisher or a spine fragment) and blanks. A pile it describes is laid out position for position from it: each entry takes the pile's reading that
# matches it (by the reference's own reading id, the title, a title fragment, the spine text or the author), a titled entry no reading matches becomes
# a book from the reference itself, an entry that names a reading of another pile of the room becomes a further copy, an untitled entry a fragment
# book, and a blank a filler carrying the reference's spine text. A first-pass reading the reference does not list keeps its place only where the
# reference has a blank or an untitled spine at the position the first pass read it (scaled to the reference height); elsewhere it is kept as an
# alternative reading ("Also read as") of the book at that position. So the drawn pile, the panel and the film agree spine for spine.
PIANO_REF = {}; PIANO_REF_META = {}
if args.piano_ref and os.path.exists(args.piano_ref):
    try:
        _pr = json.load(open(args.piano_ref, encoding='utf-8'))
        PIANO_REF_META = dict(video_id=_pr.get('video_id'), file=os.path.basename(args.piano_ref), items=(_pr.get('stats') or {}).get('items'), titled=(_pr.get('stats') or {}).get('titled'))
        for _p in _pr.get('piles') or []:
            if _p.get('object_id') and _p.get('books'): PIANO_REF[_p['object_id']] = dict(_p, video_id=_pr.get('video_id'))
    except Exception as e: warn('piano reference unreadable (%s): the piano piles are stacked from the readings' % e)
_ROMAN = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5'}
def _ref_clean(t):
    """A reference title for comparison: parenthesised notes, ellipses, question marks and bracket characters dropped (a bracketed word stays a word), roman volume numerals as arabic."""
    t = re.sub(r'\([^)]*\)', ' ', t or ''); t = re.sub(r'\.\.\.|…|\?', ' ', t).replace('[', ' ').replace(']', ' ')
    return ' '.join(_ROMAN.get(w, w) for w in norm(t).split())
def _ref_prefix_match(ref_title, title):
    """Every token of the reference title (brackets, ellipses and notes removed) is, in order, a prefix of a token of the title."""
    rt = _ref_clean(ref_title).split(); tt = _ref_clean(title).split()
    if not rt or not tt: return False
    j = 0
    for w in rt:
        while j < len(tt) and not tt[j].startswith(w): j += 1
        if j >= len(tt): return False
        j += 1
    return True
def _ref_words_in(text, title):
    """Every significant word of a title (4+ letters, stop words dropped) appears in a spine text (a blank the reference described whose print the first pass read)."""
    tw = [w for w in norm(title).split() if len(w) >= 4 and w not in STOP]; st = set(norm(text).split())
    return bool(tw) and all(w in st for w in tw)
def _rd_strings(rd):
    """The strings a pile reading can be recognised by: every sighting's title and author, the reader's read_as alternatives, the spine texts."""
    titles, authors, spines = [], [], []
    for s in rd['sightings']:
        if s.get('title'): titles.append(s['title'])
        if s.get('author'): authors.append(s['author'])
        if s.get('spine_text'): spines.append(s['spine_text'])
    for e in effective_readings(rd):
        if e.get('title'): titles.append(e['title'])
        if e.get('author'): authors.append(e['author'])
    return titles, authors, spines
def _rd_ids(rd): return [x for x in [rd.get('id')] + (rd.get('merged_ids') or []) if x]
def stack_from_reference(pid, pile, rds, ref):
    """-> (ordered [(key, rd, slot, top)], taken {top: (key, rd)}, height, {top: reference blank entry}). See the note above."""
    entries = sorted((e for e in ref['books'] if isinstance(e, dict) and e.get('pos')), key=lambda e: e['pos'])
    H = max([int(e['pos']) for e in entries] + [int(ref.get('book_count') or 0)])
    if pile.get('books_high') and pile['books_high'] != H: warn('piano reference: %s counts %d spines, the objects map %d; the reference count is drawn' % (pid, H, pile['books_high']))
    by_pos = {int(e['pos']): e for e in entries}
    free = collections.OrderedDict((k, rd) for k, rd in rds.items())   # readings not yet placed
    assign = {}     # pos -> (key, rd, entry, note)
    alts = collections.defaultdict(list)   # pos -> readings folded in as alternatives
    vid = ref.get('video_id') or PIANO_REF_META.get('video_id'); off = video_offset(vid) if vid else 0.0
    frames = [f for f in ref.get('frames') or [] if isinstance(f, dict) and isinstance(f.get('film_time_s'), (int, float))] or [dict(frame=pile.get('frame'), film_time_s=pile.get('timestamp_s') or 0, url=pile.get('source_url'))]
    def take(pos, key, rd, entry, note=None):
        assign[pos] = (key, rd, entry, note); free.pop(key, None)
    def same_title(entry, rd):
        t = _ref_clean(entry.get('title'))
        if not t: return False
        titles, _, _ = _rd_strings(rd)
        return any(_ref_clean(x) == t for x in titles) or any(norm(x) == t for x in titles)
    def frag_title(entry, rd):
        if not entry.get('title'): return False
        titles, _, _ = _rd_strings(rd)
        return any(_ref_prefix_match(entry['title'], x) for x in titles)
    def same_spine(entry, rd):
        st = norm(entry.get('spine_text') or '')
        if len(st) < 8: return False
        _, _, spines = _rd_strings(rd)
        return any(norm(x) == st for x in spines)
    def same_author_only(entry, rd):
        if entry.get('title') or not entry.get('author'): return False
        sur = surname(entry['author'])
        if not sur or len(sur) < 3: return False
        titles, authors, _ = _rd_strings(rd)
        return not any(titles) and any(surname(a) == sur for a in authors)
    def blank_reads(entry, rd):
        """the reference's blank (or untitled) spine text spells the words of the first-pass title ('TEMPO DI LIBRI ... Programma 2017')"""
        if entry.get('title'): return False
        titles, _, _ = _rd_strings(rd)
        return any(_ref_words_in(entry.get('spine_text') or '', x) for x in titles if x)
    # pass 0: the reference's own reading id (its `matched` of catalog "reading"), in this pile
    for e in entries:
        m = e.get('matched') if isinstance(e.get('matched'), dict) else {}
        if e.get('unlabelled') or m.get('catalog') != 'reading' or not m.get('id'): continue
        hit = next(((k, rd) for k, rd in free.items() if m['id'] in _rd_ids(rd)), None)
        if hit: take(int(e['pos']), hit[0], hit[1], e, 'reference id'); SP['pile_ref_by_id'] += 1
    # passes 1-4: exact title, title fragment, spine text, author-only; a titled entry whose title an already placed reading carries is a second copy
    for pass_no, test in enumerate((same_title, frag_title, same_spine, same_author_only, blank_reads), 1):
        for e in entries:
            pos = int(e['pos'])
            if pos in assign or e.get('unlabelled') and pass_no < 5: continue
            if pass_no == 5 and not e.get('unlabelled'): continue
            hit = next(((k, rd) for k, rd in free.items() if test(e, rd)), None)
            if hit: take(pos, hit[0], hit[1], e, ('title', 'title fragment', 'spine text', 'author', 'blank spine text')[pass_no - 1]); SP['pile_ref_matched'] += 1; continue
            if pass_no == 1 and e.get('title'):   # the same title twice in one pile (the two Novecento volumes, the two copies of Der ewige Faschismus): a second copy of the placed reading
                prev = next(((k, rd) for p2, (k, rd, e2, _) in assign.items() if e2 and not rd.get('_copy') and _ref_clean(e2.get('title')) == _ref_clean(e['title'])), None)
                if prev:
                    k, rd = prev; rd2 = dict(rd, id=(rd.get('id') + '~2') if rd.get('id') else None, _copy=True, _copy_note='second copy in the same pile: the film shows two')
                    assign[pos] = (k + '~2', rd2, e, 'second copy'); SP['pile_ref_copies'] += 1
    # the readings the reference does not list: their first-pass position, scaled to the reference height
    rows = pile_rows(pid, rds)
    def scaled_pos(rd):
        own = [s for s in rd['sightings'] if s.get('bookcase') == pid and not s.get('deferred')] or rd['sightings']
        for r in sorted(rows, key=lambda r: (r['n'] != H, -r['n'])):
            hits = [row_position(r, s.get('title'), s.get('author')) for s in own]; hits = [h for h in hits if h]
            if hits and r['n']: return max(1, min(H, int(round(min(hits) * H / float(r['n'])))))
        return None
    pending = []
    for k, rd in list(free.items()):
        p = scaled_pos(rd); placed = False
        if p is not None:
            titles, authors, spines = _rd_strings(rd); mine = {w for x in titles + authors + spines for w in norm(x).split() if len(w) >= 5 and w not in STOP}
            for q in (p, p - 1, p + 1):   # the same spine read differently by the two passes ('Luigi Spagnol ... davanti alla bellezza' / '[...]a alla bellezza'): an alternative reading of it
                e = by_pos.get(q)
                if e is None or q not in assign or e.get('unlabelled'): continue
                theirs = {w for w in norm((e.get('spine_text') or '') + ' ' + (e.get('title') or '') + ' ' + (e.get('author') or '')).split() if len(w) >= 5 and w not in STOP}
                if mine & theirs: alts[q].append(rd); free.pop(k, None); SP['pile_ref_alternatives'] += 1; placed = True; break
            if placed: continue
            for q in (p, p - 1, p + 1, p - 2, p + 2):
                e = by_pos.get(q)
                if e is None or q in assign or e.get('title'): continue
                if e.get('unlabelled') or not e.get('author') or same_author_only(e, rd):
                    take(q, k, rd, e, 'first-pass position (the reference reads a blank or an untitled spine here)'); SP['pile_ref_first_pass'] += 1; placed = True; break
        if not placed: pending.append((p, k, rd))
    # entries no reading matched: a copy of the reading of another pile of the room, else a book from the reference entry itself
    def other_pile_reading(e):
        m = e.get('matched') if isinstance(e.get('matched'), dict) else {}
        for opid, ords in pile_readings.items():
            if opid == pid or _PILE_ROOM.get(opid) != pile['room']: continue
            for k, rd in ords.items():
                if (m.get('catalog') == 'reading' and m.get('id') in _rd_ids(rd)) or (e.get('title') and same_title(e, rd)): return k, rd
        return None
    for e in entries:
        pos = int(e['pos'])
        if pos in assign or e.get('unlabelled'): continue
        hit = other_pile_reading(e)
        if hit:
            k, rd = hit; own = [s for s in rd['sightings'] if s.get('bookcase') == pid] or rd['sightings']
            rd2 = dict(rd, sightings=own, id=('%s~%s' % (rd['id'], pid.split(':')[-1][-8:])) if rd.get('id') else None, _copy=True, _copy_note='a second copy: the same title is read in another pile of the piano')
            assign[pos] = (k + '~' + pid[-2:], rd2, e, 'copy from another pile'); SP['pile_ref_copies'] += 1; continue
        title = (e.get('title') or '').strip() or None; author = (e.get('author') or '').strip() or None; pub = re.sub(r'\s*\([^)]*\)', '', e.get('publisher') or '').strip() or None
        if title and not _ref_clean(title): title = None   # '[...]': a spine the reference could not read at all
        pub_words = set(norm(re.sub(r'^possibly\s+|^\(\?\)\s*', '', pub or '')).split()) if pub else set()
        conf = e.get('confidence') if e.get('confidence') in CONF else 'low'
        sights = []
        for f in frames:
            ts = int(round(f['film_time_s'])); frm = os.path.basename(f.get('frame') or '')
            sights.append(dict(kind='video', level='pile', video_id=vid, timestamp_s=ts, timestamp_raw_s=int(round(f['film_time_s'] - off)), time=hms(ts), url=f.get('url') or (yt_url(vid, ts) if vid else None), frame=frm,
                               stem=os.path.splitext(frm)[0] or 'frame', credit=None, confidence=conf, bookcase=pid, shelf=0, slot=0, spine_text=e.get('spine_text'), title=title, author=author,
                               language=lang_code(e.get('language')), series=None, publisher=pub, room_id=pile['room'], wall_id='piano-reference'))
        raw0 = sights[0]['timestamp_raw_s']
        if title: sl = slug(title)
        elif author: sl = 'by-' + slug(re.sub(r'\[|\]|\?', ' ', author))
        elif pub: sl = slug(pub) + '-volume'
        else: sl = 'spine-' + slug(e.get('spine_text') or 'fragment', 24)
        rid = 'video:%s:%d:%s' % (vid, raw0, sl)
        if any(b['id'] == rid for b in BOOKS) or any(a[1].get('id') == rid for a in assign.values()): rid += '-%02d' % pos
        rd = dict(sightings=sights, id=rid, via='piano_reference', author_only=bool(author and not title), fixed=False, _ref=e)
        if not title:
            spine = re.sub(r'\s+', ' ', (e.get('spine_text') or '').strip())
            rest = [w for w in norm(re.sub(r'\.\.\.|…|\?|\[|\]|\(|\)|→|/', ' ', spine)).split() if w not in pub_words and not w.isdigit()]   # what the spine says beyond the publisher's name
            if author: disp = '%s (title not readable)' % re.sub(r'\s+', ' ', author)
            elif pub and len(rest) < 2:
                num = re.match(r'^\s*(\d{1,3})\b', spine)
                disp = '%s volume%s (title not readable)' % (re.sub(r'^possibly\s+', '', pub), (' no. ' + num.group(1)) if num else '')
            else: disp = 'spine reads ‘%s’ (title not readable)' % re.sub(r'\s*→\s*$', '', spine)[:60]
            rd['_display'] = disp; rd['_fragment'] = True
        assign[pos] = (rid, rd, e, 'from the reference'); SP['pile_ref_new'] += 1
    # the first-pass readings left over go in as alternative readings of the book at their scaled position (or the nearest book below it)
    for p, k, rd in pending:
        q = p if p is not None else H
        while q > 0 and q not in assign: q -= 1
        if q <= 0: q = next(iter(sorted(assign)), None)
        if q is None: continue
        alts[q].append(rd); SP['pile_ref_alternatives'] += 1
    for q, lst in alts.items():
        k, rd, e, note = assign[q]
        rd = dict(rd, _alts=(rd.get('_alts') or []) + lst); assign[q] = (k, rd, e, note)
    taken = {p: (k, rd) for p, (k, rd, e, note) in assign.items()}
    ordered = [(k, rd, H - p, p) for p, (k, rd) in sorted(taken.items())]
    blanks = {int(e['pos']): e for e in entries if e.get('unlabelled') and int(e['pos']) not in assign}
    if len(assign) + len(blanks) != H: warn('piano reference: %s has %d placed + %d blank spines for a height of %d' % (pid, len(assign), len(blanks), H))
    pile['reference'] = dict(file=PIANO_REF_META.get('file'), pile_id=ref.get('pile_id'), reader_label=ref.get('reader_label'), level=ref.get('level'), position=ref.get('position'), notes=ref.get('notes'))
    return ordered, taken, H, blanks
for _k in ('pile_ref_by_id', 'pile_ref_matched', 'pile_ref_copies', 'pile_ref_first_pass', 'pile_ref_new', 'pile_ref_alternatives', 'pile_ref_piles'): SP.setdefault(_k, 0)
PILE_FILLERS = 0
for pid, rds in pile_readings.items():
    pile = next(o for o in OBJECTS if o['id'] == pid); pile['books'] = []; pile['placement'] = pile.get('placement') or 'seen'
    HGT = pile.get('books_high') if isinstance(pile.get('books_high'), int) and pile['books_high'] > 0 else None
    REF = PIANO_REF.get(pid); ref_blanks = {}
    if REF:   # the film reference lays the pile out position for position
        ordered, taken, H_eff, ref_blanks = stack_from_reference(pid, pile, rds, REF); primary = None; HGT = H_eff; SP['piles_with_height'] += 1; SP['pile_ref_piles'] += 1
    elif HGT:
        # stacking from the fullest reading of the pile (its positions are from the top, unlabelled spines counted); a book that reading does not
        # list takes its position from another reading, scaled to the height; collisions push down; books no reading positions go beneath
        rows = pile_rows(pid, rds); primary = rows[0] if rows else None; pend = []
        for k, (key, rd) in enumerate(rds.items()):
            own = [s for s in rd['sightings'] if s.get('bookcase') == pid and not s.get('deferred')] or rd['sightings']; pos = None
            if primary:
                hits = [row_position(primary, s.get('title'), s.get('author')) for s in own]; hits = [h for h in hits if h]
                if hits: pos = min(hits)
            if pos is None:
                for r in rows[1:]:
                    hits = [row_position(r, s.get('title'), s.get('author')) for s in own]; hits = [h for h in hits if h]
                    if hits and r['n']: pos = max(1, min(HGT, int(round(min(hits) * HGT / float(r['n']))))); break
            pend.append((pos is None, pos or 0, k, key, rd))
        taken = {}; H_eff = max(HGT, len(pend))
        for none_pos, pos, k, key, rd in sorted(pend):
            if none_pos: p = next(x for x in range(H_eff, 0, -1) if x not in taken) if len(taken) < H_eff else H_eff + 1
            else: p = next((x for x in range(pos, H_eff + 1) if x not in taken), None) or next((x for x in range(pos - 1, 0, -1) if x not in taken), None) or H_eff + 1
            if p > H_eff: H_eff = p
            taken[p] = (key, rd)
        ordered = [(taken[p][0], taken[p][1], H_eff - p, p) for p in sorted(taken)]   # slot 0 = the bottom
        SP['piles_with_height'] += 1
    else:
        ordered = [(key, rd, k, None) for k, (key, rd) in enumerate(sorted(rds.items(), key=lambda kv: (0, 0) if stack_pos(kv[1], pid) is None else (1, -stack_pos(kv[1], pid))))]
        H_eff = len(ordered); taken = {}; primary = None
    for key, rd, slot, top in ordered:
        ss = rd['sightings']; first = earliest(ss); eff = effective_readings(rd); main = eff[0]; best = main['_s']
        sightings = [dict(kind=s['kind'], video_id=s['video_id'], timestamp_s=s['timestamp_s'], timestamp_raw_s=s.get('timestamp_raw_s'), time=s['time'], url=s['url'], frame=s['frame'], credit=s['credit'], confidence=s['confidence'], bookcase=pid, level='pile') for s in ss]
        kind = first['kind']
        bid = rd.get('id') or (('video:%s:%d:%s' % (first['video_id'], int(first['timestamp_raw_s'] if first.get('timestamp_raw_s') is not None else (first['timestamp_s'] or 0)), slug(main['title'] or ('by ' + (main['author'] or ''))))) if kind == 'video' else ('photo:%s:%s' % (first['stem'], slug(main['title'] or ('by ' + (main['author'] or ''))))))
        prim = best if (best['kind'] == 'video') == (kind == 'video') else first   # the primary link is the clearest reading's sighting
        b = dict(id=bid, bookcase=pid, shelf=0, slot=slot, section=None, title=main['title'], author=main['author'], language=best['language'] or next((s['language'] for s in ss if s['language']), None),
                 series=best['series'], publisher=best['publisher'], spine_text=best['spine_text'], origin=kind, source_kind=kind, confidence=main['confidence'], placement='seen', in_pile=True,
                 source_url=prim['url'], sightings=sightings, frames_seen=len(ss), width=round(random.uniform(0.02, 0.04), 4), height=round(random.uniform(0.19, 0.25), 3))
        if kind == 'video': b.update(video_id=prim['video_id'], timestamp_s=prim['timestamp_s'], timestamp_raw_s=prim.get('timestamp_raw_s'), time=prim['time'], video_title=(VIDEOS.get(prim['video_id']) or {}).get('title'))
        else: b.update(photo_credit=first['credit'], frame=first['frame'])
        if top is not None: b['pile_position'] = top   # 1 = the top of the pile, as the fullest reading counts (unlabelled spines included)
        # alternative readings: where the readers read the same spine differently, the highest-confidence reading is the book (ties: the first reading), the others are listed
        alts = []; seen_alt = [(norm(main['title'] or ''), norm(main['author'] or ''))]
        for e in eff[1:]:
            ek = (norm(e['title'] or ''), norm(e['author'] or ''))
            if any(ek[0] == t and (ek[1] == a or not ek[1] or not a) for t, a in seen_alt): continue   # the same title, the author missing on one side: one reading
            seen_alt.append(ek); alts.append({k: v for k, v in e.items() if not k.startswith('_')})
        if alts:
            SP['alt_readings'] += len(alts); b['alt_readings'] = alts
            if main['_alt']: SP['alt_preferred'] += 1
        if not b['title'] and b['author']:   # an author-only reading: a real book whose title no frame shows
            b['author_only'] = True; b['display_title'] = '%s (title not readable)' % b['author']
        if rd.get('_ref'):   # a book the film reference reads that no first-pass reading carried (a title, an author or a publisher's spine)
            e = rd['_ref']; b['from_reference'] = True
            if rd.get('_fragment'): b['fragment'] = True; b['display_title'] = rd.get('_display'); b['author_only'] = bool(b.get('author') and not b.get('title'))
            if e.get('title_note'): b['reading_note'] = e['title_note']
            if not b.get('publisher') and e.get('publisher'): b['publisher'] = e['publisher']
        if rd.get('_copy'):
            b['reading_note'] = rd.get('_copy_note')
            if b.get('title') and not b.get('display_title'): b['display_title'] = b['title'] + (' (second copy)' if 'same pile' in (rd.get('_copy_note') or '') else '')
        for a in rd.get('_alts') or []:   # first-pass readings the reference does not list, kept as "also read as" on the spine at their position
            ea = effective_readings(a)[0]
            b.setdefault('alt_readings', []).append(dict(title=ea.get('title'), author=ea.get('author'), confidence=ea.get('confidence'), spine_text=ea.get('spine_text'), frame=ea.get('frame'), video_id=ea.get('video_id'), timestamp_s=ea.get('timestamp_s'), time=ea.get('time'), url=ea.get('url'), source=ea.get('source'), first_pass_only=True))
            SP['alt_readings'] += 1
        variants = sorted({s['title'] for s in ss if s['title'] and s['title'] != b['title']} | {alt_label(a) for a in b.get('alt_readings') or []})
        if variants: b['title_variants'] = variants
        if rd.get('merged_ids'): b['merged_ids'] = [m for m in rd['merged_ids'] if m != bid]
        dsum = dense_summary(ss, best)
        if dsum: b['dense'] = dsum; b['dense_ids'] = dsum['ids']; SP['dense_pile_books'] += 1
        if any(x['id'] == bid for x in BOOKS): bid = b['id'] = bid + '~' + pid[-6:]
        BOOKS.append(b); add_desc(b); pile['books'].append(bid); SP['placed'] += 1
    if HGT:
        # the spines no reading identified: unlabelled books at the positions left free, so the stack is as high as the film shows
        for p in range(1, H_eff + 1):
            if p in taken: continue
            raw = next((rd for top_, rd in (primary['items'] if primary else []) if top_ <= p < top_ + (max(1, int(rd.get('count') or 1)) if rd.get('unlabelled') else 1)), None)
            if REF: raw = ref_blanks.get(p)   # the reference's description of the blank spine
            fb = dict(id='u:pile:%s:%02d' % (pid.split(':')[-1], p), bookcase=pid, shelf=0, slot=H_eff - p, section=None, origin='unlabelled', placement='filler', pile_filler=True, pile_position=p,
                      width=round(random.uniform(0.014, 0.036), 4), height=round(random.uniform(0.17, 0.24), 3))
            if raw and raw.get('spine_text'): fb['spine_text'] = raw['spine_text']
            BOOKS.append(fb); PILE_FILLERS += 1
        pile['books_high'] = HGT; pile['count'] = H_eff
    else: pile['count'] = max(len(pile['books']), pile.get('count') or 0)
    pile['books_identified'] = len(pile['books'])
# readable fragments among the blanks (objects_map_eco.json `pile_fragments`): a filler whose spine the second reading did read in part
# (a journal issue, a publisher's mark, a title seen on a second copy) becomes a low-confidence pile book with a display title, tier guess
PILE_FRAGMENTS = []
for fid, fx in (OM.get('pile_fragments') or {}).items():
    if not isinstance(fx, dict): continue
    fb = next((b for b in BOOKS if b['id'] == fid and b.get('pile_filler')), None)
    if fb is None:   # the blank may already be a fragment book from the film reference at that position: the rule then only refines its wording
        m = re.match(r'^u:pile:([^:]+):(\d+)$', fid); pid_ = 'obj:salotto:%s' % m.group(1) if m else None
        rb = next((b for b in BOOKS if m and b.get('bookcase') == pid_ and b.get('pile_position') == int(m.group(2)) and b.get('from_reference') and not b.get('title')), None)
        if rb is not None:
            for k_ in ('title', 'author', 'publisher', 'language'):
                if fx.get(k_): rb[k_] = fx[k_]
            if fx.get('display_title'): rb['display_title'] = fx['display_title']
            if fx.get('note'): rb['reading_note'] = fx['note']
            if fx.get('spine_text'): rb['spine_text'] = fx['spine_text']
            rb['author_only'] = bool(rb.get('author') and not rb.get('title')); SP['pile_fragment_refined'] = SP.get('pile_fragment_refined', 0) + 1; continue
        warn('pile_fragments: no blank spine with id %s' % fid); continue
    pile = obj_by_id(fb['bookcase'])
    if pile is None: continue
    vid = pile.get('video_id'); raw = pile.get('timestamp_raw_s')
    nid = 'video:%s:%d:%s' % (vid, int(raw if raw is not None else (pile.get('timestamp_s') or 0)), slug(fx.get('title') or fx.get('display_title') or fid.split(':')[-1]))
    if any(b['id'] == nid for b in BOOKS): nid += '~' + fid.split(':')[-1]
    fb.pop('pile_filler', None)
    fb.update(id=nid, origin='video', source_kind='video', placement='seen', in_pile=True, title=fx.get('title'), author=fx.get('author'), publisher=fx.get('publisher'), language=fx.get('language') or 'it', confidence='low',
              spine_text=fx.get('spine_text') or fb.get('spine_text'), video_id=vid, timestamp_s=pile.get('timestamp_s'), timestamp_raw_s=raw, time=pile.get('time'), source_url=pile.get('source_url'), video_title=(VIDEOS.get(vid) or {}).get('title') if vid else None,
              sightings=[dict(kind='video', video_id=vid, timestamp_s=pile.get('timestamp_s'), timestamp_raw_s=raw, time=pile.get('time'), url=pile.get('source_url'), frame=pile.get('frame'), credit=None, confidence='low', bookcase=pile['id'])],
              frames_seen=1, fragment=True, reading_note=fx.get('note'))
    if fx.get('display_title'): fb['display_title'] = fx['display_title']
    if not fb.get('title'): fb['author_only'] = bool(fb.get('author'))
    pile['books'] = [b['id'] for b in sorted((b for b in BOOKS if b.get('bookcase') == pile['id'] and b['origin'] != 'unlabelled'), key=lambda b: b.get('pile_position') or 99)]
    pile['books_identified'] = len(pile['books']); PILE_FILLERS -= 1; PILE_FRAGMENTS.append(nid)
SP['pile_fillers'] = PILE_FILLERS; SP['pile_fragments'] = len(PILE_FRAGMENTS)

# reading fixes (wall_map_eco.json `reading_fixes`): a reader's slip corrected by reading id, e.g. the neighbouring spine's author copied onto a title
READING_FIXES = {k: v for k, v in (WM.get('reading_fixes') or {}).items() if isinstance(v, dict)}
FIXED_READINGS = []
for b in BOOKS:
    fx = READING_FIXES.get(b['id']) or next((READING_FIXES[m] for m in (b.get('merged_ids') or []) if m in READING_FIXES), None)
    if not fx: continue
    if b['origin'] not in ('video', 'photo'):   # a catalogue record that a fixed reading was merged into shows the fix's note; the record's own fields stay
        if fx.get('note'): b['reading_note'] = fx['note']; FIXED_READINGS.append(b['id'])
        continue
    for k, v in fx.items():
        if k in ('note', '_comment', 'catalog_record'): continue   # catalog_record is read at the catalogue merge, not copied onto the book
        if v is None: b.pop(k, None)
        else: b[k] = v
    if fx.get('note'): b['reading_note'] = fx['note']
    FIXED_READINGS.append(b['id'])
for k in READING_FIXES:
    if not any(k == b['id'] or k in (b.get('merged_ids') or []) for b in BOOKS): warn('reading_fixes: no reading with id %s' % k)

# ------------------------------------------------------------------ quotes, notable books, tour
def video_quotes():
    """eco-video/quotes_<video id>.json: Eco's remarks transcribed by the readers. Tolerant of field names: text|text_en|quote|en,
    text_it|it|original, timestamp_s|t|start_s, target|bookcase|wall_id|room_id, speaker."""
    out = []
    for p in sorted(glob.glob(os.path.join(VIDEO_DIR, 'quotes_*.jsonl')) + glob.glob(os.path.join(VIDEO_DIR, 'quotes_*.json'))):
        vid = re.sub(r'^quotes_|\.jsonl?$', '', os.path.basename(p))
        try:
            if p.endswith('.jsonl'): items = load_jsonl(p)
            else:
                items = json.load(open(p, encoding='utf-8'))
                if isinstance(items, dict): items = items.get('quotes') or items.get('items') or []
        except Exception as e: warn('%s unreadable: %s' % (os.path.basename(p), e)); continue
        for q in items:
            if not isinstance(q, dict): continue
            text = q.get('text') or q.get('text_en') or q.get('quote') or q.get('en'); text_it = q.get('text_it') or q.get('it') or q.get('original')
            if not (text or text_it): continue
            raw = q.get('timestamp_s', q.get('t', q.get('start_s')))
            v = q.get('video_id') or vid
            ts = corrected_ts(v, raw) if isinstance(raw, (int, float)) else None
            tgt = q.get('target') or q.get('bookcase') or q.get('bookcase_id')
            if not tgt:
                lst, lvl = resolve(dict(room_id=q.get('room_id'), wall_id=q.get('wall_id'), wall_name=q.get('wall_name') or q.get('context') or ''))
                if lvl in ('bookcase', 'wall', 'context') and lst: tgt = lst[0]
                elif lvl == 'room' and lst: tgt = BC_ROOM[lst[0]]
                elif fold(q.get('room_id') or '') in ALIAS_ROOM: tgt = ALIAS_ROOM[fold(q['room_id'])]
            out.append(dict(text=text, text_it=text_it, source=q.get('source') or (VIDEOS.get(v) or {}).get('title') or v, url=q.get('url') or yt_url(v, ts or 0), speaker=q.get('speaker') or 'Umberto Eco',
                            where=dict(video_id=v, timestamp_s=ts, timestamp_raw_s=raw if isinstance(raw, (int, float)) else None, url=yt_url(v, ts or 0)), target=tgt, context=q.get('context')))
    return out
VQ = video_quotes()
def file_quotes(path):
    """quotes_eco.json (this folder): {video_id, timestamp_s (raw), speaker, text, text_it, target, context}; also accepts experience-style fields."""
    if not path or not os.path.exists(path): return []
    try: data = json.load(open(path, encoding='utf-8'))
    except Exception as e: warn('%s unreadable: %s' % (os.path.basename(path), e)); return []
    out = []
    for q in as_list(data, 'quotes'):
        if not isinstance(q, dict): continue
        text = q.get('text') or q.get('text_en') or q.get('quote') or q.get('en'); text_it = q.get('text_it') or q.get('it') or q.get('original')
        if not (text or text_it): continue
        v = q.get('video_id'); raw = q.get('timestamp_s', q.get('t')); ts = corrected_ts(v, raw) if v and isinstance(raw, (int, float)) else None
        where = q.get('where') if isinstance(q.get('where'), dict) else (dict(video_id=v, timestamp_s=ts, timestamp_raw_s=raw, url=yt_url(v, ts or 0)) if v else None)
        out.append(dict(text=text, text_it=text_it, source=q.get('source') or ((VIDEOS.get(v) or {}).get('title') if v else None), url=q.get('url') or q.get('source_url') or (yt_url(v, ts or 0) if v else None),
                        speaker=q.get('speaker') or 'Umberto Eco', where=where, target=q.get('target') or q.get('bookcase') or q.get('room') or q.get('room_id'), context=q.get('context') or q.get('about')))
    return out
QF = file_quotes(args.quotes)
TOPIC_TARGET = (json.load(open(args.quotes, encoding='utf-8')).get('topic_targets') if QF else None) or \
    {'read-them-all': 'salotto', 'antilibrary': 'salotto', 'the-library-as-tool': 'corridoio', 'corridor-walk': 'corridoio', 'arrangement-by-subject': 'studio', 'room-order': 'studio',
     'rare-books': 'antichi', 'collecting': 'antichi', 'lists-and-memory': 'studio'}
GENERAL_QUOTES = []
def exp_quotes():
    """experience/quotes.json: {id, text, language, translation, speaker, source, url, timestamp_s (YouTube clock), video_id, topic, room, bookcase, verification, notes}."""
    out = []
    for q in EXP['quotes']:
        if not isinstance(q, dict) or not q.get('text'): continue
        if q.get('target') is not None or q.get('text_it') is not None or q.get('where') is not None: out.append(q); continue   # already in the generator's shape
        it = (q.get('language') or '').lower().startswith('it')
        v = q.get('video_id'); ts = q.get('timestamp_s') if isinstance(q.get('timestamp_s'), (int, float)) else None
        where = dict(video_id=v, timestamp_s=int(round(ts)), timestamp_raw_s=round(ts - video_offset(v), 2), url=yt_url(v, ts)) if v and ts is not None else None
        tgt = q.get('bookcase') or q.get('room')
        rec = dict(id=q.get('id'), text=(q.get('translation') if it else q['text']) or q['text'], text_it=q['text'] if it else None, speaker=q.get('speaker'), source=q.get('source'), url=(q.get('url') or '').split(' (')[0] or (where['url'] if where else None),
                   where=where, target=tgt, context=q.get('notes'), topic=q.get('topic'), verification=q.get('verification'), language=q.get('language'))
        if not tgt:
            t2 = TOPIC_TARGET.get(q.get('topic') or '')
            if t2: rec['target'] = t2; rec['target_note'] = 'placed by topic (%s)' % q.get('topic')
            else: GENERAL_QUOTES.append(rec); continue
        out.append(rec)
    return out
EQ = exp_quotes()
def quote_key(q):
    w = q.get('where') if isinstance(q.get('where'), dict) else {}
    raw = w.get('timestamp_raw_s', w.get('timestamp_s'))
    return (w.get('video_id'), int(round(raw))) if w.get('video_id') and isinstance(raw, (int, float)) else None
ROOM_KW = [(r'rare|antichi|studiolo|fake books|libri falsi|libri antichi|collector|incunab|alchem|kircher', 'antichi'), (r'corridoi|corridor|feuilleton|fumett|comics', 'corridoio'),
           (r'\bstud(y|io)\b|scrivania|desk|philosoph|semiot', 'studio'), (r'salotto|living|sofa|piano|vitrin|vetrin', 'salotto'), (r'vestib|ingresso|joyce|kabbal', 'vestibolo')]
def all_quotes():
    """quotes_eco.json first (it wins on text and speaker), then experience/quotes.json, then eco-video/quotes_<id>.json; the same (video, second) is kept once."""
    seen = []; out = []
    for q in QF + EQ + VQ:
        k = quote_key(q)
        if k and any(k[0] == s[0] and abs(k[1] - s[1]) <= 3 for s in seen): continue
        if k: seen.append(k)
        if not (q.get('target') or q.get('bookcase') or q.get('room')):
            blob = fold(' '.join(str(q.get(x) or '') for x in ('context', 'text', 'text_it', 'about')))
            hit = next((rid for rx, rid in ROOM_KW if re.search(rx, blob)), None)
            if hit: q = dict(q, target=hit, target_note='room chosen from the wording of the quotation')
        out.append(q)
    return out
QALL = all_quotes()
def find_quote(video_id, raw_s):
    if not video_id or not isinstance(raw_s, (int, float)): return None
    best = None
    for q in QALL:
        k = quote_key(q)
        if k and k[0] == video_id and abs(k[1] - raw_s) <= 3 and (best is None or abs(k[1] - raw_s) < abs(quote_key(best)[1] - raw_s)): best = q
    return best
def attach_quotes():
    out = dict(placed=0, unplaced=[])
    for q in QALL:
        if not isinstance(q, dict) or not (q.get('text') or q.get('text_it')): continue
        tgt = q.get('target') or q.get('bookcase') or q.get('room')
        rec = dict(text=q.get('text'), text_it=q.get('text_it'), source=q.get('source'), url=q.get('url') or q.get('source_url'), speaker=q.get('speaker'), where=q.get('where'), context=q.get('context'))
        if rec.get('where') and isinstance(rec['where'], dict) and rec['where'].get('video_id') and not rec['where'].get('url'):
            rec['where']['url'] = yt_url(rec['where']['video_id'], rec['where'].get('timestamp_s'))
        holder = None
        if tgt:
            key = str(tgt).strip()
            if key in BC: holder = BC[key]
            elif key in GROUP: holder = BC[GROUP[key][0]]
            elif key in ROOM_IDS: holder = room_of(key)
            elif fold(key) in ALIAS_ROOM: holder = room_of(ALIAS_ROOM[fold(key)])
            elif expand(key) and level_of(key) in ('bookcase', 'wall'): lst = expand(key); holder = BC[lst[len(lst) // 2]]   # a Fondazione letter such as A: the middle bay of the run
            else:
                for o in OBJECTS:
                    if o['id'] == key: holder = o
        if holder is None: out['unplaced'].append(dict(target=tgt, text=(rec.get('text') or rec.get('text_it'))[:80])); GENERAL_QUOTES.append(rec); continue
        holder.setdefault('quotes', []).append(rec); out['placed'] += 1
    return out
QUOTES = attach_quotes()
ROLE_RE = re.compile(r"^\s*[\[(]?\s*(?:\d+\s+)?(a cura di|cura di|ed(?:ited|s?)\.?\s+by|edited|edizione|editor|introduction|introduzione|introd\.|preface|pr[eé]face|prefazione|foreword|compiled|redaktion|hrsg|herausgegeben|traduzione|translated|trad\.|transl\.|dessins|illustr|sotheby|christie)", re.I)
LATIN_SUBS = (('ph', 'f'), ('th', 't'), ('ch', 'c'), ('ae', 'e'), ('oe', 'e'), ('y', 'i'), ('v', 'u'), ('j', 'i'), ('w', 'u'), ('h', ''))
NAME_STOP = {'anon', 'anonymous', 'various', 'pseudo', 'incl', 'comm', 'attr', 'attributed', 'trad', 'the', 'and', 'with', 'von', 'van', 'sir', 'saint', 'san', 'santo', 'st', 'fra', 'frater',
             'fratris', 'fr', 'sancti', 'beati', 'magistri', 'episcopi', 'dr', 'doctor', 'docteur', 'chevalier', 'mm', 'par', 'autore', 'monsieur', 'maitre', 'junior', 'senior', 'jr'}
COLLECTED_RE = re.compile(r"\b(oeuvres|opera|opere|works|werke|omnia|scritti|obras|romans|novels)\b", re.I)
def lfold(x, n=4):
    """A token folded across Latin / vernacular spellings (Ethimologiarum ~ Etymologiae, Danthe ~ Dante, ciuitate ~ civitate, Lullii ~ Llull), cut to n letters."""
    x = fold(x)
    for a, b in LATIN_SUBS: x = x.replace(a, b)
    return re.sub(r'(.)\1', r'\1', x)[:n]
def overlap(A, B, prefix=True):
    """Folded stems that meet: equal, or (prefix) a three-letter stem that opens a longer one ('oto' ~ 'oton', 'lul' ~ 'luli'); author fields compare exactly ('sue' is not 'svelati')."""
    return sum(1 for a in A if any(a == b or (prefix and min(len(a), len(b)) == 3 and (a.startswith(b) or b.startswith(a))) for b in B))
def work_tokens(title, parens=True, n=4, minlen=3):
    """Significant stems of a work title (alternatives separated by ' / ' or '; ' all count; parentheticals optionally dropped)."""
    t = title or ''
    if not parens: t = re.sub(r'\(.*?\)', ' ', t)
    parts = re.split(r'\s+/\s+|;\s+', t)
    return {lfold(x, n) for p in parts for x in tokens(p) if len(x) >= minlen and not x.isdigit() and x not in NAME_STOP}
def name_tokens(author):
    return {lfold(x) for x in tokens(re.sub(r'[()\[\]]', ' ', author or '')) if len(x) >= 3 and not x.isdigit() and x not in NAME_STOP}
def name_keys(author, medieval=True):
    """Stems that identify a person: the surname ('Calasso, Roberto' / 'Roberto Calasso' -> calasso), for a curated id also the first name of a
    medieval 'X of Y' form (Isidore of Seville -> isidore, which heads the Latin title), and any name in parentheses (a pseudonym: 'Goedsche ... (Sir John Retcliffe)')."""
    keys = set()
    for part in re.split(r'\s+/\s+|;\s+|\band\b', author or ''):
        sur = surname(part)
        if sur: keys.add(lfold(sur))
        if medieval and ',' not in part and re.search(r"\b(of|de|da|di|von|van|del|della|d')\b", fold(part)):
            first = next((x for x in norm(part).split() if len(x) >= 3 and x not in NAME_STOP and x not in STOP), None)
            if first: keys.add(lfold(first))
        for m in re.finditer(r'\((.*?)\)', part): keys |= name_tokens(m.group(1))
    return {k for k in keys if len(k) >= 3}
def work_match(n, b, explicit=False):
    """(c) A notable entry matches a book only on the WORK: its (original) title against the record title / set title / title variants, with the author
    as the record's MAIN author (the author field, or the name at the head of a Latin title: 'Aurelii Augustini ... De ciuitate Dei') where both name one.
    A surname appearing anywhere else (a monograph *about* Borges, a translation *by* Bignami) never matches. Returns 'work', or for a curated explicit id
    also 'collected' (the author's collected works, which contain the work) or 'same-author' (the author's copy of another title: reported, not matched).
    The curated id is compared on four-letter Latin-folded stems; the open search over every identified book on five-letter stems with a stricter bar."""
    stem, minlen = (4, 3) if explicit else (5, 4)
    m = n.get('match') if isinstance(n.get('match'), dict) else {}
    T_main, T_all = set(), set()
    for t in (n.get('title'), n.get('original_title'), m.get('title')): T_main |= work_tokens(t, parens=False, n=stem, minlen=minlen); T_all |= work_tokens(t, n=stem, minlen=minlen)
    if not T_main: T_main = T_all
    if not T_all: return None
    B = work_tokens(b.get('title'), n=stem, minlen=minlen) | work_tokens(b.get('set_title'), n=stem, minlen=minlen)
    for v in (b.get('title_variants') or []): B |= work_tokens(v, n=stem, minlen=minlen)
    hit = overlap(T_all if explicit else T_main, B); ratio = hit / max(1, len(T_main))   # the open search ignores parenthetical glosses ('(Mussolini's death, Gladio ...)')
    nauth = n.get('author') or m.get('author') or ''
    anon = not nauth or bool(re.search(r'\b(anon|various|pseudo|biblia)', fold(nauth)))
    N = name_keys(nauth, medieval=explicit)
    bauth = b.get('author') or ''
    A = set() if (not bauth.strip() or ROLE_RE.search(bauth)) else name_tokens(bauth)
    head = {lfold(x) for x in norm(re.sub(r'\(.*?\)', ' ', b.get('title') or '')).split()[:12] if len(x) >= 3 and x not in STOP and x not in NAME_STOP}
    same_author = bool(overlap(N, A, prefix=False)) or (explicit and not A and bool(overlap(N, head)))   # the Latin title head stands in for a missing author field only for a curated id
    if N and not anon and not same_author and (A or not explicit): return None   # a named author must be the record's main author
    if explicit:
        # a record catalogued without an author field is matched on its title alone when half the notable title is there and either the title's first
        # word is (Steganographia, Iconologia) or the imprint is early (Liber chronicarum 1493, 'libri cronicarum'); 'Memoires de mr d'Artagnan' (1700) is not Les Trois Mousquetaires
        ntitle = re.sub(r'\(.*?\)', ' ', n.get('original_title') or n.get('title') or '').split(' / ')[0]
        first_tok = next((lfold(x, stem) for x in norm(ntitle).split() if x not in STOP and x not in NAME_STOP and len(x) >= minlen), None)
        title_alone = not bauth.strip() and ratio >= 0.5 and ((isinstance(b.get('year'), int) and b['year'] < 1600) or (first_tok is not None and first_tok in B))
        if hit >= 2 or (hit >= 1 and (same_author or title_alone)): return 'work'
        if same_author and COLLECTED_RE.search(b.get('title') or ''): return 'collected'
        if same_author: return 'same-author'
        return None
    if same_author: return 'work' if (hit >= 2 or (hit >= 1 and ratio >= 0.34)) else None
    return 'work' if (anon and hit >= 2 and ratio >= 0.6 and hit / max(1, len(B)) >= 0.3) else None
def nearest_by_author(n, cands):
    """The library's nearest record by the same author for a notable work that is absent: the notable's surname must be a token of the record's
    author field (never of its title); rare books first, then the earliest edition."""
    m = n.get('match') if isinstance(n.get('match'), dict) else {}
    nauth = n.get('author') or m.get('author') or ''
    if not nauth or re.search(r'\b(anon|various|pseudo|biblia|periodical|fiction|fictitious|invented)', fold(nauth)): return None
    first = re.sub(r'\(.*?\)', ' ', nauth.split(';')[0])
    sur = surname(first)
    if not sur or len(sur) < 4: return None
    toks = [x for x in norm(first).split() if x not in STOP and x not in NAME_STOP and len(x) >= 3]
    if ',' not in first and len(toks) > 1: need = set(toks)                 # 'Salimbene de Adam': every name must be there (not Villiers de l'Isle-Adam)
    else: need = {sur}
    given = {x for x in toks if x != sur}                                  # 'Bettini, Mario': the given name must agree where the record has one (not Maurizio Bettini)
    best = None
    for b in cands:
        ba = b.get('author') or ''
        if not ba.strip() or ROLE_RE.search(ba): continue
        bt = {x for x in norm(re.sub(r'\(.*?\)', ' ', ba)).split()}
        bgiven = {x for x in bt if x != sur and len(x) >= 3 and x not in STOP and x not in NAME_STOP}
        if need <= bt and (not given or not bgiven or given & bgiven):
            key = (0 if b.get('rare') else 1, b.get('year') or 9999, b['id'])
            if best is None or key < best[0]: best = (key, b)
    return best[1] if best else None
def attach_notable():
    out = dict(matched=0, unmatched=[], rejected=[])
    by_id = {b['id']: b for b in BOOKS}
    for a, t in RARE_ID_ALIAS.items(): by_id.setdefault(a, by_id[t]) if t in by_id else None   # a set record's id names its first volume
    out['categories'] = collections.OrderedDict(); out['stops'] = collections.OrderedDict()
    cands = [b for b in BOOKS if b['origin'] != 'unlabelled' and b.get('title')]
    for n in EXP['notable']:
        if not isinstance(n, dict): continue
        m = n.get('match') if isinstance(n.get('match'), dict) else n
        cm = n.get('catalog_match') if isinstance(n.get('catalog_match'), dict) else {}
        cat = n.get('category') or 'notable'
        hits = []; how = 'work'; nearest = None
        # an explicit id (match.id, or the research file's catalog_match.books_json_id) is accepted only when the record is the work itself (or, for a curated id,
        # the author's collected works); an AIB Studi incunabulum is identified by its shelfmark, so its listed record is the work by definition
        for bid in (m.get('id'), cm.get('books_json_id')):
            if bid and bid in by_id:
                rec = by_id[bid]
                sm = str(cm.get('shelfmark_or_id') or '')
                if cat == 'incunabula' and rec.get('incunabulum') and (bid.split(':', 1)[1] in sm or (rec.get('shelfmark') and rec['shelfmark'] in sm)): hits = [rec]; how = 'listed'; break
                r = work_match(n, rec, explicit=True)
                if r in ('work', 'collected'): hits = [rec]; how = r; break
                if r == 'same-author': nearest = rec
                out['rejected'].append(dict(title=m.get('title'), author=m.get('author'), id=bid, record_title=rec.get('title'), record_author=rec.get('author'), category=cat,
                                            reason=("another title by the same author (not the work)" if r == 'same-author' else
                                                    "the record is not the work (a study, translation or edition of something else that shares a name)")))
        if not hits:
            hits = [b for b in cands if work_match(n, b) == 'work']
            hits.sort(key=lambda b: (0 if b.get('rare') else 1, b['id']))
        if not hits:
            if nearest is None: nearest = nearest_by_author(n, cands)
            note = 'not found on these shelves'
            subj_bc = subj_rule = subj_room = None
            if nearest is not None: note += "; the nearest book by the same author is '%s'" % clean_display(nearest.get('title') or '', 'title')[:80]
            else:   # no record by the author either: the stop goes to the bookcase the subject rules would give the work, or, with no rule, to the room of the fallback bookcase
                subj_bc, subj_rule = subject_target(n.get('title') or m.get('title') or '', m.get('author') or n.get('author'))
                subj_room = BC_ROOM.get(subj_bc) if subj_bc else None
                if subj_rule: note += '; nothing by the author either: the stop shows the bookcase where its subject is shelved'
                else: note += '; nothing by the author either: the stop shows the room'; subj_bc = None
            out['unmatched'].append(dict(title=m.get('title'), author=m.get('author'), id=None, category=cat, status=note, nearest_id=nearest['id'] if nearest is not None else None,
                                         subject_bookcase=subj_bc, subject_rule=subj_rule, subject_room=subj_room))
            out['stops'].setdefault(cat, []).append(dict(id=None, title=n.get('title'), author=n.get('author'), year=n.get('year'), why=n.get('why'), source_url=n.get('source_url') or n.get('url'),
                                                        source=n.get('source'), missing=True, note=note, nearest_id=nearest['id'] if nearest is not None else None,
                                                        nearest_title=clean_display(nearest.get('title') or '', 'title') if nearest is not None else None,
                                                        nearest_bookcase=nearest.get('bookcase') if nearest is not None else None,
                                                        subject_bookcase=subj_bc, subject_rule=subj_rule, subject_room=subj_room))
            continue
        for b in hits[: (1 if n.get('first_only') or (cm.get('books_json_id') and hits[0]['id'] == cm.get('books_json_id')) else len(hits))]:
            b['notable'] = dict(why=n.get('why'), source_url=n.get('source_url') or n.get('url'), category=cat, source=n.get('source'), year=n.get('year'), rare_book=n.get('rare_book'))
            if isinstance(n.get('links'), list) and n['links']: b['notable']['links'] = [dict(text=clean_display(str(l.get('text') or '')), url=l.get('url')) for l in n['links'] if isinstance(l, dict) and l.get('text') and l.get('url')]   # a source the text names ('nota di vendita Christie's') linked in place
            if b['id'] not in out['categories'].setdefault(cat, []): out['categories'][cat].append(b['id'])
            out['stops'].setdefault(cat, []).append(dict(id=b['id'], title=n.get('title'), author=n.get('author'), year=n.get('year'), why=n.get('why'), missing=False, match=how,
                                                        note={'collected': "Eco's copy of the author's collected works, which contain the work", 'listed': 'identified by the AIB Studi shelfmark'}.get(how)))
        out['matched'] += 1
    return out
NOTABLE = attach_notable()
CATEGORY_TITLES = {'name-of-the-rose': 'The Name of the Rose (1980)', 'foucaults-pendulum': "Foucault's Pendulum (1988)", 'island-of-the-day-before': 'The Island of the Day Before (1994)',
                   'baudolino': 'Baudolino (2000)', 'queen-loana': 'The Mysterious Flame of Queen Loana (2004)', 'prague-cemetery': 'The Prague Cemetery (2010)', 'numero-zero': 'Numero Zero (2015)',
                   'essays-forgeries': 'Essays: forgeries and the Protocols', 'essays-kircher-lull-occult': 'Essays: Kircher, Lull and the occult', 'semiotics-and-theory': 'Semiotics and theory',
                   'personal-touchstone': 'Personal touchstones', 'lists-and-memory': 'Lists and memory', 'medieval-aesthetics': 'Medieval aesthetics', 'incunabula': 'The incunabula'}
NOTABLE_TOURS = [dict(id='notable-' + cat, title=CATEGORY_TITLES.get(cat, cat.replace('-', ' ').capitalize()), category=cat, books=NOTABLE['categories'].get(cat, []),
                      stops=stops, missing=sum(1 for s in stops if s.get('missing')))
                 for cat, stops in NOTABLE.get('stops', {}).items() if stops]
def tour_target_ok(t):
    return bool(t) and (t in BC or t in GROUP or t in ROOM_IDS or obj_by_id(t) is not None or any(b['id'] == t for b in BOOKS))
def build_tour():
    t, name = None, None
    if args.tour and os.path.exists(args.tour):
        try: t = json.load(open(args.tour, encoding='utf-8')); name = os.path.basename(args.tour)
        except Exception as e: warn('%s unreadable: %s' % (os.path.basename(args.tour), e))
    if t is None and EXP['tour']: t, name = EXP['tour'], 'experience/tour.json'
    stops = as_list(t, 'stops') if t else []
    out = []
    for s in stops:
        if not isinstance(s, dict): continue
        tgt = s.get('target')
        if not tour_target_ok(tgt):
            if tour_target_ok(s.get('fallback')): tgt = s['fallback']
            else: warn('tour stop %s: target %r unknown, stop dropped' % (s.get('id'), tgt)); continue
        if tgt in GROUP and tgt not in BC: tgt = GROUP[tgt][0]
        q = s.get('quote')
        if isinstance(q, dict) and q.get('video_id') and not (q.get('text') or q.get('text_it')):
            found = find_quote(q['video_id'], q.get('timestamp_s'))
            if found is None: warn('tour stop %s: no quotation at %s %s' % (s.get('id'), q['video_id'], q.get('timestamp_s')))
            q = found
        kind = 'room' if tgt in ROOM_IDS else 'bookcase' if tgt in BC else 'object' if obj_by_id(tgt) else 'book'
        out.append(dict(id=s.get('id') or 'stop-%d' % (len(out) + 1), target=tgt, kind=kind, caption=s.get('caption'), quote=q, url=s.get('url'), camera=s.get('camera')))
    if out: return dict(title=(t.get('title') if isinstance(t, dict) else None) or 'Tour', stops=out, auto=False, file=name)
    for r in ROOMS:
        blurb = (r.get('blurb') or '').split('. ')[0]
        q = (r.get('quotes') or [None])[0]
        out.append(dict(id='stop-' + r['id'], target=r['id'], kind='room', caption=r['name'] + (': ' + blurb if blurb else ''), quote=q))
    return dict(title='A walk through the apartment', stops=out, auto=True)
TOUR = build_tour()
TOUR_IMG_MAX, TOUR_IMG_Q = 200, 50
TOUR_IMG = collections.Counter()
def tour_image(tour_id, stop_id, im):
    """A stop's picture, {file (a file of eco-map/tour-images/), credit, link, alt} -> {src (a data URL, 200 px on the long side),
    credit, link, alt, w, h}. Only files that exist and open are embedded; the total is counted in TOUR_IMG for the report."""
    if not isinstance(im, dict) or not im.get('file'): return None
    if Image is None: warn('Pillow not available: tour images skipped'); return None
    path = im['file'] if os.path.isabs(im['file']) else os.path.join(H, 'tour-images', im['file'])
    if not os.path.exists(path): warn('tour %s stop %s: image %s not found' % (tour_id, stop_id, im['file'])); return None
    try:
        img = Image.open(path); img.load()
        if img.mode not in ('RGB', 'L'): img = img.convert('RGB')
        img.thumbnail((TOUR_IMG_MAX, TOUR_IMG_MAX))
        buf = io.BytesIO(); img.convert('RGB').save(buf, 'JPEG', quality=TOUR_IMG_Q, optimize=True, progressive=False)
        data = buf.getvalue()
    except Exception as e: warn('tour %s stop %s: image %s unreadable: %s' % (tour_id, stop_id, im['file'], e)); return None
    TOUR_IMG['n'] += 1; TOUR_IMG['bytes'] += len(data)
    return dict(src='data:image/jpeg;base64,' + base64.b64encode(data).decode('ascii'), credit=im.get('credit'), link=im.get('link'), alt=im.get('alt'), w=img.size[0], h=img.size[1])
def build_tours():
    """tours_eco.json -> meta.tours: the sourced tours. Each tour is {id, title, blurb, stops}; a stop is {id, target, title, caption,
    source {kind, label, video_id, t (link second), url, note}, quote, record}. Targets are book ids, object ids, bookcase ids or room ids; an unknown
    target falls back to the stop's `fallback` or is dropped with a warning, so the page never resolves a missing id. A film source without a url
    gets the YouTube link at its second. quote refs resolve like the room tour's. `record` names the Braidense reference entry (an ECO.04
    record, placement reference) of the same book when the stop opens on a copy of the flat; the page prints it as a catalogue-record line whose link
    opens that entry's panel. A record that is not a reference entry is dropped with a warning."""
    p = args.tours
    if not p or not os.path.exists(p): return []
    try: t = json.load(open(p, encoding='utf-8'))
    except Exception as e: warn('%s unreadable: %s' % (os.path.basename(p), e)); return []
    out = []
    for tr in as_list(t, 'tours'):
        if not isinstance(tr, dict) or not tr.get('id'): continue
        stops, dropped = [], 0
        for s in as_list(tr, 'stops'):
            if not isinstance(s, dict): continue
            tgt = RARE_ID_ALIAS.get(s.get('target'), s.get('target'))   # a set record's id names its first volume
            if not tour_target_ok(tgt):
                if tour_target_ok(s.get('fallback')): tgt = s['fallback']
                else: warn('tour %s stop %s: target %r unknown, stop dropped' % (tr['id'], s.get('id'), tgt)); dropped += 1; continue
            if tgt in GROUP and tgt not in BC: tgt = GROUP[tgt][0]
            src = dict(s.get('source') or {})
            if src.get('video_id') and src.get('t') is not None and not src.get('url'):
                src['url'] = 'https://www.youtube.com/watch?v=%s&t=%ds' % (src['video_id'], int(round(float(src['t']))))
            q = s.get('quote')
            if isinstance(q, dict) and q.get('video_id') and not (q.get('text') or q.get('text_it')):
                found = find_quote(q['video_id'], q.get('timestamp_s'))
                if found is None: warn('tour %s stop %s: no quotation at %s %s' % (tr['id'], s.get('id'), q['video_id'], q.get('timestamp_s')))
                q = found
            elif isinstance(q, dict) and q.get('text'):   # Eco's own words on the book, {text, lang?, translation?, attribution, url?}, checked for length (a sentence or two)
                if len(q['text'].split()) > 75: warn('tour %s stop %s: quotation runs to %d words' % (tr['id'], s.get('id'), len(q['text'].split())))
                if not q.get('attribution'): warn('tour %s stop %s: quotation without an attribution' % (tr['id'], s.get('id')))
                q = dict(text=q['text'], lang=q.get('lang') or 'en', translation=q.get('translation'), attribution=q.get('attribution'), url=q.get('url'))
            im = tour_image(tr['id'], s.get('id'), s.get('image'))
            kind = 'room' if tgt in ROOM_IDS else 'bookcase' if tgt in BC else 'object' if obj_by_id(tgt) else 'book'
            rec = RARE_ID_ALIAS.get(s.get('record'), s.get('record')) if s.get('record') else None   # the catalogue record of the same book
            if rec and not any(b['id'] == rec and b.get('placement') == 'reference' for b in BOOKS): warn('tour %s stop %s: record %r is not a reference entry, dropped' % (tr['id'], s.get('id'), rec)); rec = None
            if rec and kind == 'book' and tgt == rec: warn('tour %s stop %s: record names the stop\'s own target' % (tr['id'], s.get('id'))); rec = None
            stops.append(dict(id=s.get('id') or '%s-%d' % (tr['id'], len(stops) + 1), target=tgt, kind=kind, title=s.get('title'), caption=s.get('caption'), source=src or None, quote=q, image=im, **({'record': rec} if rec else {})))
        if stops: out.append(dict(id=tr['id'], title=tr.get('title') or tr['id'], blurb=tr.get('blurb'), stops=stops, dropped=dropped))
        else: warn('tour %s: no stop with a known target, tour dropped' % tr['id'])
    return out
TOURS = build_tours()
def build_walk():
    """walk_eco.json -> meta.walk: waypoints (world metres) on the Hq66X9f-zgc clock, captions, resolved quotations, links on both clocks."""
    p = os.path.join(H, 'walk_eco.json')
    if not os.path.exists(p): return None
    try: w = json.load(open(p, encoding='utf-8'))
    except Exception as e: warn('walk_eco.json unreadable: %s' % e); return None
    vid = w.get('video_id'); fvid = w.get('film_video_id'); foff = float(w.get('film_label_offset_s') or 0)
    pts = []
    for s in w.get('waypoints') or []:
        if not isinstance(s, dict) or not isinstance(s.get('pos'), list) or len(s['pos']) != 3: continue
        t = float(s.get('t') or 0); label = t + foff
        q = s.get('quote')
        if isinstance(q, dict) and q.get('video_id') and not (q.get('text') or q.get('text_it')): q = find_quote(q['video_id'], q.get('timestamp_s'))
        pts.append(dict(t=t, pos=[round(float(v), 2) for v in s['pos']], look=[round(float(v), 2) for v in (s.get('look') or s['pos'])], room=s.get('room'), caption=s.get('caption'), quote=q,
                        url=yt_url(vid, t) if vid else None, film_url=yt_url(fvid, corrected_ts(fvid, label)) if fvid and label >= 0 else None, film_label_s=round(label, 1)))
    if len(pts) < 2: return None
    return dict(title=w.get('title') or "Eco's walk", video_id=vid, video_title=(VIDEOS.get(vid) or {}).get('title'), film_video_id=fvid, film_title=(VIDEOS.get(fvid) or {}).get('title'),
                film_label_offset_s=foff, film_time_offset_s=video_offset(fvid) if fvid else 0, source=w.get('source'), waypoints=pts, duration_s=round(pts[-1]['t'] - pts[0]['t'], 1), route_notes=ROUTE_NOTES)
WALK = build_walk()

# ------------------------------------------------------------------ filler
FILL_TALL = {'E', 'H', 'F', 'G'}
filler_n = 0
if not args.no_fill:
    for r in ROOMS:
        for bc in r['bookcases']:
            if bc['kind'] == 'cabinet': continue   # rare cabinets: the catalogue is complete, no invented spines
            if bc['kind'] == 'display' or bc.get('curio'): continue   # glazed vitrines and the cabinet of curiosities: their contents are drawn from the footage (open books, shells, objects), not as invented spines
            tall = bc['fondazione_bay'] in FILL_TALL
            for sh, row in enumerate(SLOTS[bc['id']]):
                for sl, cur in enumerate(row):
                    if cur is not None: continue
                    filler_n += 1
                    b = dict(id='u:%06d' % filler_n, bookcase=bc['id'], shelf=sh, slot=sl, section=bc['id'] + '-s', origin='unlabelled', placement='filler',
                             width=round(random.uniform(0.03, 0.045) if tall else random.uniform(0.02, 0.038), 4), height=round(random.uniform(0.24, 0.30) if tall else random.uniform(0.175, 0.245), 3))
                    row[sl] = b; BOOKS.append(b)

# ------------------------------------------------------------------ descriptions
DESC, DESC_USED = {}, []
# descriptions_eco_overrides.json is read first and wins outright: an entry there (a verified text, or description: null with a `rejected` note) claims its id
# even against the fetched files, which the fetch scripts rewrite wholesale
for p in dict.fromkeys([os.path.join(os.path.dirname(args.descriptions) or H, 'descriptions_eco_overrides.json'), args.descriptions] +
                       [os.path.join(os.path.dirname(args.descriptions) or H, n) for n in ('descriptions_eco_seen.json', 'descriptions_eco_braidense.json', 'descriptions_eco_bologna.json')]):
    if not os.path.exists(p): continue
    try: d = json.load(open(p, encoding='utf-8'))
    except Exception as e: warn('descriptions file %s unreadable: %s' % (os.path.basename(p), e)); continue
    if isinstance(d, list): d = {x['id']: x for x in d if isinstance(x, dict) and x.get('id')}
    if not isinstance(d, dict): continue
    n = 0; override = os.path.basename(p) == 'descriptions_eco_overrides.json'
    for k, v in d.items():
        if not isinstance(v, dict) or k.startswith('_') or (DESC.get(k) or {}).get('_override'): continue
        if override: DESC[k] = dict(v, _file=os.path.basename(p), _override=True); n += 1
        elif v.get('description') and not (DESC.get(k) or {}).get('description'): DESC[k] = dict(v, _file=os.path.basename(p)); n += 1
    DESC_USED.append(dict(file=os.path.basename(p), entries=len(d), used=n, applied=0, by_kind=dict(collections.Counter(v.get('description_kind') for v in d.values() if isinstance(v, dict) and v.get('description')))))
for _sid, _kids in RARE_SET_ONLY.items():   # the article on a work serves the volumes of the set record that carried it
    _d = DESC.get('braidense:' + _sid)
    if not _d or not _d.get('description') or _d.get('description_kind') not in ('article', 'search'): continue
    for _k in _kids:
        _cur = DESC.get('braidense:' + _k)
        if _cur and (_cur.get('_override') or (_cur.get('description') and _cur.get('description_kind') not in ('author', 'none'))): continue
        DESC['braidense:' + _k] = dict(_d, _from_set='braidense:' + _sid)
desc_n = 0
DESC_APPLIED = collections.Counter()
DESC_REJECTED = collections.Counter(); DESC_REJECTED_IDS = []; DESC_CLEANED = collections.Counter()
MEDIUM_RE = re.compile(r"\b(?:is|was)\s+(?:a|an|the)\s+(?:\d{4}\s+|\w+\s+){0,3}(?:film|movie|opera|television series|tv series|album|band|video ?game|fictional character|comic|manga)\b"
                       r"|\b(?:è|fu)\s+(?:un|una|un')\s*(?:\w+\s+){0,2}(?:film|opera lirica|melodramma|personaggio immaginario|serie televisiva|album|videogioco|gruppo musicale|fumetto)\b"
                       r"|\b(?:est|fut)\s+(?:un|une)\s+(?:\w+\s+){0,2}(?:film|opéra|personnage de fiction|série télévisée|album|jeu vidéo|bande dessinée)\b"
                       r"|\b(?:ist|war)\s+(?:ein|eine)\s+(?:\w+\s+){0,2}(?:Film|Oper|Fernsehserie|Album|Videospiel|fiktive Figur|Comic)\b"
                       r"|\b(?:es|fue)\s+(?:un|una)\s+(?:\w+\s+){0,2}(?:película|ópera|personaje ficticio|serie de televisión|álbum|videojuego)\b", re.I)
DISAMBIG_RE = re.compile(r"may refer to|può riferirsi|può indicare|peut désigner|peut faire référence|steht für|puede referirse|is a surname|è un cognome", re.I)
TRUNC_RE = re.compile(r"\b(des|der|den|the|of|del|de|la|le|el|il|dal|nel|seit|since|am|on|au|em|geboren|born|nato|nata|né|née|died|gestorben|morto|morta|mort|morte)\s+\d{1,2}\.$|\(\*\s*\d+\.$|\b(?:vol|no|n|p|pp|ca|cap|ch|St|Bd|hrsg|ed|c|s)\.$", re.I)
def desc_body(text):
    m = re.match(r'^By .*?:\s*', text or '')
    return (text or '')[m.end():] if m else (text or '')
def validate_description(b, d):
    """(f) -> (text or None, reason). Rejects a description whose Wikipedia title shares neither a title word nor the author's surname with the book,
    author fallbacks whose 'author' is empty (unless the article's person heads a Latin title, 'Athanasii Kircheri ...') or a role statement (a cura di,
    introduction by), disambiguation pages, articles about a film / opera / character instead of the book, articles on a work merely named inside the
    book's title (Leggere I promessi sposi), and truncated texts (cut back to the last full sentence where one remains); strips IPA pronunciations and an
    implausible '(b. YEAR)'. Entries marked verified: true are taken as they are."""
    text = d.get('description') or ''
    if d.get('verified'): return text, None
    kind = d.get('description_kind') or 'article'; wt = d.get('wikipedia_title') or ''
    if DISAMBIG_RE.search(text): return None, 'disambiguation page'
    first_sentence = re.split(r'(?<=[.!?])\s+', desc_body(text).strip())[0] if text else ''
    if kind != 'author' and MEDIUM_RE.search(first_sentence): return None, 'article about a film, opera or character, not the book'
    author = b.get('author') or ''; sur = surname(author)
    title = b.get('title') or ''
    btoks = work_tokens(title) | work_tokens(b.get('set_title'))
    for v in (b.get('title_variants') or []): btoks |= work_tokens(v)
    wt_core = re.sub(r'\(.*?\)', ' ', wt).strip()
    wtoks = work_tokens(wt_core)
    wsur = next((x for x in reversed(norm(wt_core).split()) if len(x) >= 4 and x not in NAME_STOP), None)   # the article's person: last usable token
    head = [x for x in norm(re.sub(r'\(.*?\)', ' ', title)).split()[:8] if len(x) >= 3 and x not in STOP]
    if kind == 'author':
        if ROLE_RE.search(author): return None, 'author fallback with an empty or role-statement author'
        if not author.strip():
            if not (wsur and any(lfold(x) == lfold(wsur) for x in head)): return None, 'author fallback with an empty or role-statement author'
        elif not (sur and sur[:5] in fold(wt)) and not overlap(wtoks, name_tokens(author)): return None, 'article title names neither the author nor the book'
    elif wt:
        ft, fw = fold(re.sub(r'\(.*?\)', ' ', title)).strip(), fold(wt_core)
        if not overlap(wtoks, btoks) and not (sur and sur[:5] in fold(wt)) and not (fw and (fw in ft or ft in fw)): return None, 'article title shares no word with the book title or author'
        lead = []
        for x in [y for y in norm(re.sub(r'\(.*?\)', ' ', title)).split() if y not in STOP and len(y) >= 3]:
            if overlap({lfold(x)}, wtoks): break
            lead.append(x)
        names = name_tokens(author) | name_tokens(first_sentence)
        if lead and wtoks and len(btoks) >= 2 * len(wtoks) and not any(overlap({lfold(x)}, names) for x in lead if len(x) >= 4):
            return None, 'article on a work only named inside the book title'   # 'Leggere I promessi sposi' is not the novel; 'Athanasii Kircheri ... China ... illustrata' is Kircher's own book
    # cleanups
    t2 = re.sub(r"\s*\((?:[^()]*\[[^\]]*\][^()]*)\)", '', text)            # '( KAN-tor; German: [ˈɡeːɔʁk ...])' pronunciation parentheticals
    t2 = re.sub(r"\s*\((?:pronounced|pronuncia|prononcé)[^)]*\)", '', t2, flags=re.I)
    if t2 != text: DESC_CLEANED['ipa'] += 1
    m = re.match(r'^By (.*?) \(b\. (\d{4})\):', t2)
    if m:
        by = int(m.group(2)); yr = b.get('year') if isinstance(b.get('year'), int) else None
        if yr and (by > yr - 12 or by < yr - 110): t2 = t2.replace(' (b. %d)' % by, '', 1); DESC_CLEANED['birth_year'] += 1
    body = desc_body(t2).strip()
    truncated = len(body) < 25 or body.count('(') > body.count(')') or TRUNC_RE.search(body) or not re.search(r'[.!?»"\')\]]$', body)
    if truncated:
        sents = re.split(r'(?<=[.!?])\s+', body)
        keep = ' '.join(sents[:-1]).strip() if len(sents) > 1 else ''
        if len(keep) >= 40 and keep.count('(') <= keep.count(')') and not TRUNC_RE.search(keep): t2 = t2[:len(t2) - len(body)] + keep; DESC_CLEANED['truncation_cut'] += 1
        else: return None, 'truncated text'
    return t2, None
EDITION_WORD_RE = re.compile(r"^\s*(?:(?:A|An|The)\s+)?([A-Z][A-Za-z-]+(?:\s+[A-Z][a-z]+)?)\s+(?:edition|translation)\b")   # the language word an edition description opens with ('Serbian edition of ...', 'Old French translation ...')
LANG_NAME_SET = set(LANG_NAME.values())
def edition_contradiction(b, text):
    """An edition description whose language word contradicts the entry's language line ('Croatian edition' under LANGUAGE Serbian, 'English edition' under Italian)
    is refused: one of the two is wrong, and the card must not say both. The reason is counted with the other rejections and warned, since it means an input needs reading again."""
    m = EDITION_WORD_RE.match(text or '')
    if not m or m.group(1) not in LANG_NAME_SET: return None
    have = LANG_NAME.get(b.get('language'))
    if not have or m.group(1) == have: return None
    why = 'edition word contradicts the language line (%s edition under %s)' % (m.group(1), have)
    warn('description of %s refused: %s: %r' % (b['id'], why, (text or '')[:70])); return why
for b in BOOKS:
    d = DESC.get(b['id']) or DESC.get(b['id'].split('~')[0]) or next((DESC[m] for m in b.get('merged_ids', []) if m in DESC), None)
    if d and d.get('_override') and not d.get('description'):   # blocked by review
        why = 'rejected by review (descriptions_eco_overrides.json)'
        DESC_REJECTED[why] += 1; DESC_REJECTED_IDS.append(dict(id=b['id'], title=(b.get('title') or '')[:60], author=b.get('author'), wikipedia_title=d.get('wikipedia_title'), kind=d.get('description_kind'), reason=why, file=d.get('_file')))   # the review note stays in the overrides file, not in the shipped data
        b['description_kind'] = 'none'; continue
    if d and d.get('description'):
        text, why = validate_description(b, d)
        if not why and d.get('description_kind') == 'edition': why = edition_contradiction(b, text)
        if why:
            DESC_REJECTED[why] += 1; DESC_REJECTED_IDS.append(dict(id=b['id'], title=(b.get('title') or '')[:60], author=b.get('author'), wikipedia_title=d.get('wikipedia_title'), kind=d.get('description_kind'), reason=why, file=d.get('_file')))
            b['description_kind'] = 'none'; continue
        b['description'] = text; b['description_kind'] = d.get('description_kind'); b['description_source'] = d.get('description_source')
        if d.get('wikipedia_lang'): b['description_lang'] = d['wikipedia_lang']
        if d.get('_from_set'): b['_desc_set'] = d['_from_set']
        desc_n += 1; DESC_APPLIED[d.get('_file')] += 1
for du in DESC_USED: du['applied'] = DESC_APPLIED.get(du['file'], 0)   # books that carry a description from that file (an entry may serve several merged ids, or none)
DESC_VALIDATION = dict(rejected=sum(DESC_REJECTED.values()), by_reason=dict(DESC_REJECTED), cleaned=dict(DESC_CLEANED), rejected_ids=DESC_REJECTED_IDS)

# ------------------------------------------------------------------ English titles (the page's Native / English switch)
# titles_en_eco.json and descriptions_en_eco.json next to this script, keyed by book id: {"title_en" | "desc_en", "kind": "published" | "literal",
# "source", "confidence"}; both optional and possibly partial, tolerated when absent or unreadable. A book gets
# `title_en`, `title_en_kind`, `title_en_source` (and `desc_en`) only when an entry exists, so the slim build grows only for those books; the
# native title stays in `title` and is what the page shows by default. Keys starting with `_` are notes, ids that are not in the library are
# counted, and an English title equal to the native one (case-insensitive) is dropped: it would change nothing on the page.
EN_TITLES, EN_DESCS = {}, {}
EN_COUNTS = dict(books=0, published=0, literal=0, descriptions=0, same_as_native=0, unmatched=0, files=[])
def load_en(name, field):
    path = os.path.join(H, name)
    if not os.path.exists(path): return {}
    try: d = json.load(open(path, encoding='utf-8'))
    except Exception as e: warn('%s unreadable: %s' % (name, e)); return {}
    if isinstance(d, list): d = {x['id']: x for x in d if isinstance(x, dict) and x.get('id')}
    if not isinstance(d, dict): warn('%s is not an object keyed by book id' % name); return {}
    out = {}
    for k, v in d.items():
        if k.startswith('_') or not isinstance(v, dict): continue
        text = v.get(field) or v.get('title_en') or v.get('description_en') or v.get('description')
        if isinstance(text, str) and text.strip(): out[k] = dict(v, **{field: ' '.join(text.split())})
    EN_COUNTS['files'].append(dict(file=name, entries=len(out)))
    return out
TITLE_FIXES = {'video:ygvl-_gtAP8:94:самеliche-werke': 'Sämtliche Werke'}   # a spine reading the reader garbled (Cyrillic letters for Latin ones); the id keeps its slug
for b in BOOKS:
    if b['id'] in TITLE_FIXES: b['title'] = TITLE_FIXES[b['id']]
EN_TITLES = load_en('titles_en_eco.json', 'title_en')
EN_DESCS = load_en('descriptions_en_eco.json', 'desc_en')
if EN_TITLES or EN_DESCS:
    EN_SEEN = set()
    for b in BOOKS:
        ids = [b['id']] + list(b.get('merged_ids') or [])   # a reading merged into this record may be the key the translator used
        t = next((EN_TITLES[i] for i in ids if i in EN_TITLES), None)
        if t:
            EN_SEEN.update(i for i in ids if i in EN_TITLES)
            if (b.get('title') or '').strip().lower() == t['title_en'].lower(): EN_COUNTS['same_as_native'] += 1
            else:
                kind = 'published' if str(t.get('kind') or '').lower().startswith('pub') else 'literal'
                b['title_en'] = t['title_en']; b['title_en_kind'] = kind
                if BARE_NUMBER_RE.match(b['title_en']) and not BARE_NUMBER_RE.match(b.get('title') or ''):   # the set's bare number ('1: An Itinerary ...') is not part of the English title when the composed title has none
                    b['title_en'] = re.sub(r"^\s*\[?\d{1,2}(?:\.\d{1,2}){0,3}(?:\s*/\s*\d{1,2})?\]?\s*:\s*", '', b['title_en']); EN_COUNTS['bare_number_dropped'] = EN_COUNTS.get('bare_number_dropped', 0) + 1; warn('English title of %s opened with a bare number: dropped (%s)' % (b['id'], t['title_en'][:60]))
                refuse_vol_colon(b, b['title_en'], 'English title')   # the English title keeps the range too ('vol. 31.1-2: Rhetoric ...')
                if t.get('source'): b['title_en_source'] = ' '.join(str(t['source']).split())
                EN_COUNTS['books'] += 1; EN_COUNTS[kind] += 1
        d = next((EN_DESCS[i] for i in ids + ([b['_desc_set']] if b.get('_desc_set') else []) if i in EN_DESCS), None)   # a volume's description came from its set record
        if d:
            EN_SEEN.update(i for i in ids if i in EN_DESCS)
            b['desc_en'] = d['desc_en']; EN_COUNTS['descriptions'] += 1
    EN_COUNTS['unmatched'] = len((set(EN_TITLES) | set(EN_DESCS)) - EN_SEEN)
    ne = dict(total=0, catalog=0, video=0, photo=0, fragments=0)   # the identified books with no English entry (already English, proper names, fragments), for the About page
    for b in BOOKS:
        if b.get('origin') == 'unlabelled' or not (b.get('title') or b.get('display_title') or b.get('author')) or b.get('title_en'): continue
        ne['total'] += 1
        if b.get('author_only') or not (b.get('title') or '').strip() or len((b.get('title') or '').strip()) < 4: ne['fragments'] += 1
        elif b.get('origin') in ('video', 'photo'): ne[b['origin']] += 1
        else: ne['catalog'] += 1
    EN_COUNTS['no_entry'] = ne

# ------------------------------------------------------------------ what the camera saw
for r in ROOMS:
    for bc in r['bookcases']:
        bc['on_camera'] = bc['id'] in ON_CAMERA
        if SEEN_NOTES.get(bc['id']):
            seen_keys = set(); bc['seen_in_film'] = []
            for s in SEEN_NOTES[bc['id']]:   # one line per sighting (the vitrine note was filed once per frame of the same shot)
                k = (strip_bc_id(s['label']), s['timestamp_s'])
                if k in seen_keys: continue
                seen_keys.add(k); bc['seen_in_film'].append(dict(label=strip_bc_id(s['label']), description=strip_bc_id(s.get('description')), timestamp_s=s['timestamp_s'], time=s['time'], url=s['url'], video_id=s['video_id'], frame=s['frame']))
    r['bookcases_on_camera'] = sum(1 for bc in r['bookcases'] if bc['on_camera'])
    r['objects_on_camera'] = sum(1 for o in OBJECTS if o['room'] == r['id'] and o.get('video_id'))
    if 'seen_seconds' not in r: r['seen_seconds'] = 0; r['seen_ranges'] = []
BC_ON_CAMERA = sum(r['bookcases_on_camera'] for r in ROOMS)   # counted over the drawn bookcases (ON_CAMERA may also hold aliases), so About, the fog layer and the room panels agree
for o in OBJECTS:
    o['on_camera'] = bool(o.get('video_id'))
    if not o.get('shape'): o['shape'] = shape_of(o['kind'], o.get('label') or '')   # piles from the spine frames and layout.json furniture never went through build_objects
    if 'facing' not in o: o['facing'] = round((o.get('rotation') or 0) % 360, 1)
    if 'against_wall' not in o: o['against_wall'] = None

# ------------------------------------------------------------------ object thumbnails (schema_eco.md, "Object thumbnails")
THUMB_MAX, THUMB_Q, THUMB_BUDGET = 256, 68, 2.5 * 1024 * 1024
THUMB_PRIORITY = {'artwork': 0, 'curiosity': 1, 'desk': 2, 'piano': 2, 'pile': 3, 'glass_case': 4, 'chair': 5, 'sofa': 5, 'lamp': 6, 'ladder': 6, 'other': 7}
THUMB = collections.Counter()
BOOK_BY_ID = {b['id']: b for b in BOOKS}
for _a, _t in RARE_ID_ALIAS.items():
    if _t in BOOK_BY_ID: BOOK_BY_ID.setdefault(_a, BOOK_BY_ID[_t])
def crop_window(kind, hint, bbox=None):
    """Fractions (x0, y0, x1, y1) of the frame to keep. An explicit bbox/crop [x0, y0, x1, y1] (fractions, or pixels when > 1) wins; otherwise the
    centre 60% (artworks 50%: the frames were chosen for them, so the tighter window is what the notes allow), slid towards the side the
    position hint names (left / right / above, high, top / floor, below, bottom)."""
    if isinstance(bbox, (list, tuple)) and len(bbox) == 4 and all(isinstance(v, (int, float)) for v in bbox): return tuple(bbox), 'bbox'
    f = 0.5 if kind == 'artwork' else 0.6
    cx = cy = 0.5; h = fold(hint or '')
    if re.search(r'\bleft\b|sinistr', h) and not re.search(r'\bright\b', h): cx = 0.5 - (1 - f) / 2
    elif re.search(r'\bright\b|destr', h) and not re.search(r'\bleft\b', h): cx = 0.5 + (1 - f) / 2
    if re.search(r'\babove\b|\bhigh\b|\btop\b|upper|ceiling|hung at|head height', h): cy = 0.5 - (1 - f) / 2
    elif re.search(r'floor|\bbelow\b|bottom|\bbase\b|\blow\b|leaning', h): cy = 0.5 + (1 - f) / 2
    return (cx - f / 2, cy - f / 2, cx + f / 2, cy + f / 2), ('hint' if (cx, cy) != (0.5, 0.5) else 'centre')
def make_thumb(path, window, quality=THUMB_Q):
    """-> (data URL, bytes, crop aspect w/h) of the window of the image, resized to THUMB_MAX px on the long side."""
    im = Image.open(path); im.load()
    if im.mode not in ('RGB', 'L'): im = im.convert('RGB')
    W, Hh = im.size
    x0, y0, x1, y1 = window
    if max(window) > 1.0: box = (int(x0), int(y0), int(x1), int(y1))   # pixel bbox
    else: box = (int(x0 * W), int(y0 * Hh), int(x1 * W), int(y1 * Hh))
    box = (max(0, box[0]), max(0, box[1]), min(W, max(box[0] + 8, box[2])), min(Hh, max(box[1] + 8, box[3])))
    im = im.crop(box)
    im.thumbnail((THUMB_MAX, THUMB_MAX))
    buf = io.BytesIO(); im.convert('RGB').save(buf, 'JPEG', quality=quality, optimize=True, progressive=False)
    data = buf.getvalue()
    return 'data:image/jpeg;base64,' + base64.b64encode(data).decode('ascii'), len(data), round(im.size[0] / max(1, im.size[1]), 3)
def thumb_candidate(o):
    """The frame or photograph to crop for an object: the experience record's own image first (the film frame or photograph the brief chose for
    it), else the film inventory's best_frame, else, for the piles built from the spine readers' frames, the frame of their first reading."""
    cands = o.pop('_cands', []) or []
    cands = [c for c in cands if c.get('path')]
    if o.pop('_no_thumb', False): o['no_thumb'] = True; return None      # the rule says no frame shows the work: neutral canvas
    forced = o.pop('_thumb', None)
    if forced: return forced                                             # the rule's own frame / photograph
    if cands:
        cands.sort(key=lambda c: (0 if c.get('prefer') else 1))
        return cands[0]
    if o.get('video_id') and o.get('frame'):
        p = frame_path(o['video_id'], o['frame'])
        if p: return dict(path=p, bbox=None, hint=o.get('placement_note') or '', frame=o['frame'], video_id=o['video_id'])
    for bid in o.get('books') or []:
        b = BOOK_BY_ID.get(bid)
        for s in (b or {}).get('sightings') or []:
            p = frame_path(s.get('video_id'), s.get('frame'))
            if p: return dict(path=p, bbox=None, hint='', frame=s.get('frame'), video_id=s.get('video_id'))
    return None
def add_thumbs():
    if Image is None: warn('Pillow not available: no object thumbnails'); return
    jobs = []
    for o in OBJECTS:
        c = thumb_candidate(o)
        if not c: THUMB['no_frame'] += 1; continue
        window, how = crop_window(o['kind'], c.get('hint') or '', o.pop('_crop', None) or c.get('bbox'))
        jobs.append((THUMB_PRIORITY.get(o['kind'], 7), o, c, window, how))
    jobs.sort(key=lambda j: j[0])
    quality = THUMB_Q
    while True:
        total = 0; made = []
        for pr, o, c, window, how in jobs:
            try: url, n, aspect = make_thumb(c['path'], window, quality)
            except Exception as e: warn('thumbnail failed for %s (%s): %s' % (o['id'], os.path.basename(c['path']), e)); continue
            made.append((o, c, url, n, aspect, how)); total += n
        if total <= THUMB_BUDGET or quality <= 40: break
        quality -= 8; THUMB['quality_reduced'] += 1
    kept = 0; total = 0
    for o, c, url, n, aspect, how in made:
        if total + n > THUMB_BUDGET: THUMB['dropped_over_budget'] += 1; continue
        o['thumb'] = url; o['thumb_frame'] = c.get('frame') or os.path.basename(c['path']); o['thumb_bytes'] = n; o['thumb_crop'] = how
        if o['kind'] == 'artwork':
            # the artwork's own proportions: the modelling note's size when it gives one (dims_m = [w, d, h]), else the crop window's
            o['art_aspect'] = round(o['dims_m'][0] / max(0.01, o['dims_m'][2]), 3) if o.get('dims_m') and o['dims_m'][2] else aspect
        total += n; kept += 1
    THUMB['objects'] = kept; THUMB['bytes'] = total; THUMB['quality'] = quality
    THUMB['artworks'] = sum(1 for o in OBJECTS if o.get('thumb') and o['kind'] == 'artwork')
add_thumbs()
for o in OBJECTS: o.pop('_cands', None); o.pop('_crop', None); o.pop('_thumb', None); o.pop('_no_thumb', None); o['label'] = strip_bc_id(o['label']); o['description'] = strip_bc_id(o.get('description'))

# ------------------------------------------------------------------ certainty tiers (schema_eco.md, "Certainty tiers")
def bc_name(bcid):
    bc = BC.get(bcid)
    if bc is None: return bcid
    return bc.get('fondazione_bay') or bc['id']
def object_tier(o):
    """certain: placed by an objects_map rule (a position or an anchor, i.e. a position note) from a film frame or photograph; guess: everything else."""
    note = o.get('_placed') or o.get('placement_note') or ''
    has_frame = bool(o.get('thumb_frame') or o.get('frame') or any(s.get('frame') or s.get('image') for s in o.get('sightings') or []))
    if note.startswith('objects_map') and has_frame:
        where = ('seen on film at %s' % mmss(o.get('time'))) if o.get('video_id') and o.get('time') else ('seen in %s' % photo_name(o.get('frame') or o.get('thumb_frame')))
        return 'certain', '%s; position set from that %s' % (where, 'shot' if o.get('video_id') else 'photograph')
    if note.startswith('objects_map'): return 'guess', 'position set by hand; no frame shows it'
    if note.startswith('objects.json bookcase'): return 'guess', 'the research notes name the bookcase; the spot in front of / on top of it is a guess'
    if note.startswith('position hint'): return 'guess', "position guessed from the film: %s" % re.sub(r'\s*\(hint:.*$', '', note.split(':', 1)[1].strip())   # whole, not cut at sixty characters
    if o['kind'] == 'pile' and o.get('placement') == 'seen': return 'guess', "pile seen in the film; its place in the room is a guess"
    if o.get('auto'): return 'guess', 'furniture listed in the room notes; position guessed'
    return 'guess', 'position not evidenced by a frame'
def object_placement_text(o):
    """The reader's placement line: 'Seen on film at 13:02, in front of Q · Books by Eco…' (rule with a frame), 'Position inferred from the film' (guesses);
    never a rule name or a file name (the machine note stays in the generator)."""
    placed = o.get('_placed') or ''
    seen = ('seen on film at %s' % mmss(o.get('time'))) if o.get('video_id') and o.get('time') else ('seen in %s' % photo_name(o.get('frame') or o.get('thumb_frame'))) if (o.get('frame') or o.get('thumb_frame')) else None
    if placed.startswith('objects_map position'): return (seen[0].upper() + seen[1:]) if seen else 'Position taken from the film inventory'
    if placed.startswith('objects_map anchor'):
        where = placed.split(':', 1)[1].strip()
        return ('%s, %s' % (seen[0].upper() + seen[1:], where)) if seen else ('Position inferred from the film; %s' % where)
    if placed.startswith('objects.json bookcase'): return 'Position inferred from the film; %s' % placed.split(':', 1)[1].strip()
    if placed.startswith('position hint'): return 'Position inferred from the film'
    return o.get('placement_note')
for o in OBJECTS:
    o['tier'], o['tier_reason'] = object_tier(o)
    o['placement_note'] = object_placement_text(o)
    if o.get('_placed', '').startswith('objects_map') and o.get('source_url'): o['placement_url'] = o['source_url']
    o.pop('_placed', None)
OBJ_TIER = {o['id']: o['tier'] for o in OBJECTS}
OBJ_LABEL = {o['id']: o['label'] for o in OBJECTS}
def book_tier(b):
    """certain: a Braidense shelfmark, or a reading at an identified bookcase (or a pile whose position is certain) with confidence high or medium;
    guess: subject placements, room- or subject-level readings, low-confidence readings, piles at guessed positions; unknown: the filler."""
    pl = b.get('placement'); conf = b.get('confidence')
    if pl == 'filler': return 'unknown', 'empty slot'
    if pl == 'unshelved': return 'guess', 'Bologna record with no subject match; not shelved (Milan position unknown)'
    if pl == 'reference': return 'guess', "Braidense reference section ECO.04 (%s): the library's set of Eco's own publications; presence and position in the flat not established" % (b.get('shelfmark') or 'no shelfmark')
    if pl == 'catalogued' and b.get('_sec') == 2: return 'guess', 'Braidense shelfmark %s: section ECO.02 records books kept in the room off its shelves (on the desk, for example); the cabinet is a stand-in' % (b.get('shelfmark') or '(record without shelfmark)')
    if pl == 'catalogued' and b.get('_sec') == 3: return 'guess', 'Braidense shelfmark %s: section ECO.03 gathers the most precious books; the glazed cabinet is a stand-in' % (b.get('shelfmark') or '(record without shelfmark)')
    if pl == 'catalogued': return 'certain', "Braidense shelfmark %s, in the rare-book room's shelf order" % (b.get('shelfmark') or '(record without shelfmark)')
    if pl == 'seen':
        ss = b.get('sightings') or []
        at = [s for s in ss if s.get('bookcase') == b.get('bookcase') and s.get('level') in ('bookcase', 'wall', 'pile')] or [s for s in ss if s.get('bookcase') == b.get('bookcase')] or ss   # the sighting that named the bookcase, not a subject placement that happens to agree
        s = sorted(at, key=lambda s: (-CONF.get(s.get('confidence') or 'low', 1), s.get('timestamp_s') if s.get('timestamp_s') is not None else 1e12))[0] if at else None
        where = ('on film at %s' % s.get('time')) if s and s.get('kind') == 'video' and s.get('time') else ('in %s' % photo_name(s.get('frame'))) if s else 'in a frame'
        if b.get('in_pile'):
            pid = b.get('bookcase'); ptier = OBJ_TIER.get(pid, 'guess')
            lab = OBJ_LABEL.get(pid, pid)   # the whole label (a cut at forty characters left 77 reasons with an open parenthesis: 'pile 1 of 6 (leftm')
            if b.get('author_only'): return 'guess', 'only the author\'s name was read %s in pile "%s"; the title is not legible' % (where, lab)
            if ptier == 'certain' and conf in ('high', 'medium'): return 'certain', 'read %s in pile "%s" (pile position from an objects_map rule)' % (where, lab)
            if conf not in ('high', 'medium'): return 'guess', 'low-confidence reading %s in pile "%s"' % (where, lab)
            return 'guess', 'read %s in pile "%s", whose position is a guess' % (where, lab)
        pc = (s.get('confidence') if s else None) or conf   # the confidence of the sighting that named the bookcase, not of a clearer reading that a subject rule placed
        if pc in ('high', 'medium'): return 'certain', 'read %s at bookcase %s' % (where, bc_name(b.get('bookcase')))
        return 'guess', 'low-confidence reading %s at bookcase %s' % (where, bc_name(b.get('bookcase')))
    # inferred
    if b.get('catalog') == 'bologna':
        if b.get('placement_rule'): return 'guess', "Bologna record placed by subject rule '%s'" % b['placement_rule']
        return 'guess', 'Bologna record with no subject match; shown on a bookcase of the room'
    if b.get('catalog') == 'aib-2022': return 'guess', 'listed among the incunabula (AIB Studi 2022) but absent from the Braidense export; cabinet guessed'
    if b.get('catalog') == 'braidense': return 'guess', 'Braidense record without a parsable ECO shelfmark; cabinet guessed'
    note = b.get('placement_note') or ''
    if note.startswith('the reading names only the room'): return 'guess', 'reading names only the room (%s); bookcase guessed (no shelf label visible in the frame)' % (re.search(r'\((.*?)\)', note).group(1) if re.search(r'\((.*?)\)', note) else '?')
    if note.startswith('placed from the shelf label'): return 'guess', "shelf label names a subject ('%s'); the bay is inferred from the Fondazione caption" % (b.get('shelf_label') or '?')
    if note.startswith('seen after the move'): return 'guess', 'seen in the Bologna reinstallation; the room and the bookcase are guessed from the subject, not read in the flat'
    if note.startswith('the shot shows no room'): return 'guess', 'no room or shelf label in the shot; the room and the bookcase are guessed from the subject, not read in the flat'
    if note.startswith('read on film at') or note.startswith('read in the Bologna reinstallation at'): return 'guess', 'title read on film, but the shot shows no shelf tag: the bookcase is inferred from the shot\'s context'
    if note: return 'guess', note   # whole, not cut at ninety characters
    return 'guess', 'placement inferred'
def dense_tier_cap(b, tier, reason):
    """The heavy pass's three tiers mapped onto the map's two, honestly: its 'certain' (full title, placed by a shelf tag) stays certain only when the tag that
    placed it is in the frame or the same dense shot and parses with the map's own rules (dense_tag_verified); its 'probable' and 'guess' are guesses here,
    with the reason in the pass's own words. Only a book whose placing sighting is a dense one is capped: a first-pass reading of the same spine at a tagged
    bay keeps its own tier."""
    if b.get('seen_after_move'):   # placed by a tag read in the Bologna reinstallation
        return 'guess', 'read in the Bologna reinstallation at a shelf carrying the Milan tag of bookcase %s (the reinstallation keeps the tags); not read in the flat' % bc_name(b.get('bookcase'))
    sb = b.get('seen_by_tag')
    if sb and b['origin'] == 'catalog':   # a Bologna record on the bookcase a film sighting names: certain only when the tag is verified, as for video books
        if sb.get('after_move'):
            return 'guess', 'read in the Bologna reinstallation at a shelf carrying the Milan tag of bookcase %s (the reinstallation keeps the tags); not read in the flat%s' % (bc_name(sb['bookcase']), ('; the subject rule %r had placed it on %s' % (sb.get('rule'), bc_name(sb['moved_from']))) if sb.get('moved_from') else '')
        if sb.get('dense_id') and not (sb.get('dense_tier') == 'certain' and sb.get('tag_verified')):
            return 'guess', 'read on film at %s on bookcase %s, but the call tag that placed it (%s) is not in the frame or the same shot, or is not a tag the map recognises%s' % (
                sb.get('time'), bc_name(sb['bookcase']), ', '.join(sb.get('tags') or []) or 'none legible', ('; the subject rule %r had placed it on %s' % (sb.get('rule'), bc_name(sb['moved_from']))) if sb.get('moved_from') else '')
        return tier, reason + (' (%s)' % sb['how'] if sb.get('how') else '')
    d = b.get('dense')
    if not d or not d.get('placing') or b['origin'] not in ('video', 'photo'): return tier, reason
    dt, dr = d.get('placing_tier') or d['tier'], d.get('placing_reason') or d.get('reason') or ''
    note = b.get('placement_note') or ''
    if dt in ('probable', 'guess') and note.startswith(('seen after the move', 'the shot shows no room')):   # the reading names no room of the flat
        if tier == 'certain': SP['dense_tier_capped'] += 1; DENSE_TIER_CHANGES.append((b['id'], 'certain->guess', 'room guessed'))
        return 'guess', 'title read on film, %s: the room and the bookcase are guessed from the subject, not read in the flat' % ('but in the Bologna reinstallation' if note.startswith('seen after') else 'but the shot shows no room or shelf label')
    if dt == 'certain':
        if tier == 'certain' and not d.get('tag_verified'):
            SP['dense_certain_unverified'] += 1; DENSE_TIER_CHANGES.append((b['id'], 'certain->guess', 'tag not verified'))
            return 'guess', "full title read on film at bookcase %s, but the shelf tag that placed it (%s) is not in the frame or the same shot, or is not a tag the map recognises" % (bc_name(b.get('bookcase')) if b.get('bookcase') in BC else (b.get('bookcase') or '?'), ', '.join(d.get('tags') or []) or 'none legible')
        if tier == 'certain': return tier, reason + ' (full title read on film, placed by the shelf tag %s)' % (', '.join(d.get('tags') or []) or '?')
        return tier, reason
    if dt == 'probable':
        if 'confirmed by catalog' in dr: why = 'partial read confirmed by a catalogue record' + ('; the bookcase is known' if 'bookcase known' in dr else '')
        elif 'full title' in dr: why = 'full title read, but placed only by the shot context or the room'
        else: why = 'partial read on a tagged shelf, not confirmed by a catalogue record'
        if tier == 'certain': SP['dense_tier_capped'] += 1; DENSE_TIER_CHANGES.append((b['id'], 'certain->guess', why))
        return 'guess', 'probable reading on film: %s' % why
    if tier == 'certain': SP['dense_tier_capped'] += 1; DENSE_TIER_CHANGES.append((b['id'], 'certain->guess', 'dense guess'))
    return 'guess', 'uncertain reading on film: %s' % (dense_words(dr) or 'fragment, or the bookcase is unknown')
def dense_words(dr):
    """The heavy pass's shorthand reason in reader-facing words: match scores and the reader's own confidence marks are dropped."""
    t = ' ' + (dr or '') + ' '
    t = re.sub(r'\s*\((?:high|medium|low)\)', '', t)
    t = re.sub(r'\bno catalog match\b', 'no catalogue match', t)
    t = re.sub(r'\bcatalog/notable match \d+\b', 'a catalogue or notable-list match', t)
    t = re.sub(r'\bcatalog match \d+\b', 'a catalogue match', t)
    t = re.sub(r'\bweak match \d+\b', 'a weak catalogue match', t)
    t = re.sub(r'\bmatch \d+\b', 'a catalogue match', t)
    t = re.sub(r'\bbookcase unknown\b', 'the bookcase is unknown', t)
    t = re.sub(r'\bbookcase known\b', 'the bookcase is known', t)
    t = re.sub(r'\bno match\b', 'no catalogue match', t)
    return re.sub(r'\s+', ' ', t).strip(' ;,')
for b in BOOKS:
    b['tier'], b['tier_reason'] = book_tier(b)
    b['tier'], b['tier_reason'] = dense_tier_cap(b, b['tier'], b['tier_reason'])

# ------------------------------------------------------------------ order, tidy, counts
for b in BOOKS:
    for k in [k for k in b if k.startswith('_')]: b.pop(k)
    if b.get('language'):
        b['language_name'] = LANG_NAME.get(b['language']) or b['language']
        if b['language'] not in LANG_NAME: LANG_UNNAMED[b['language']] += 1   # a code with no name would print as the language line ('uk', 'zxx'): refused below
    for k in [k for k, v in list(b.items()) if v is None or v == []]: b.pop(k)
for _c, _n in sorted(LANG_UNNAMED.items()): warn('language code %r has no name in LANG_NAME: %d entr%s would print the code as the language' % (_c, _n, 'y' if _n == 1 else 'ies'))   # the generator refuses a bare code
# reader-facing strings (schema_eco.md, "Display cleaning"): catalogue markup and workshop notes never reach the page; the raw title is kept as title_raw
for b in BOOKS:
    clean_field(b, 'title', 'title', raw_key='title_raw')
    for k in ('set_title', 'volume_statement', 'title_variants', 'part_title'): clean_field(b, k, 'title')   # part_title
    clean_field(b, 'author', 'author')
    for k in ('place', 'date', 'publisher', 'series', 'video_title'): clean_field(b, k)
    if b.get('notable'):
        for k in ('why', 'source'): clean_field(b['notable'], k)
    if b.get('copy'):
        for k in ('annotation', 'provenance', 'dedication_by', 'condition', 'givers'): clean_field(b['copy'], k)
        if b['copy'].get('inscription'): b['copy']['inscription'] = clean_inscription(b['copy']['inscription'])   # the words as transcribed, not the catalogue-markup pass
for o in OBJECTS:
    for k in ('label', 'description', 'seen_labels', 'placement_note', 'video_title'): clean_field(o, k)
    clean_quotes(o.get('quotes'))
ORDER_BC = {bc['id']: i for i, bc in enumerate(bc for r in ROOMS for bc in r['bookcases'])}
BOOKS.sort(key=lambda b: (ORDER_BC.get(b.get('bookcase'), 999), b.get('shelf') if b.get('shelf') is not None else -1, b.get('slot') or 0, b['id']))   # unshelved records (no bookcase) sort last
by_origin = collections.Counter(b['origin'] for b in BOOKS if b.get('placement') != 'reference')   # the reference entries are counted apart (counts.reference)
by_placement = collections.Counter(b['placement'] for b in BOOKS)
by_lang = collections.Counter(b.get('language') or ('unlabelled' if b['origin'] == 'unlabelled' else 'unknown') for b in BOOKS)
# overlay dimensions (schema_eco.md, "Overlay counts"): the same classes per library, per room and per bookcase, so the page's legends can show counts
def source_class(b): return b['catalog'] if b['origin'] == 'catalog' and b.get('catalog') else b['origin']   # video | photo | braidense | bologna | aib-2022 | unlabelled
def century_class(b):
    if b['origin'] == 'unlabelled': return 'unlabelled'
    y = b.get('year')
    return '%d00s' % (y // 100) if isinstance(y, int) and 1400 <= y <= 2099 else 'unknown'
def lang_class(b): return b.get('language') or ('unlabelled' if b['origin'] == 'unlabelled' else 'unknown')
def dim_counts(bs):
    return dict(by_source=dict(collections.Counter(source_class(b) for b in bs)), by_tier=dict(collections.Counter(b['tier'] for b in bs)),
                by_century=dict(sorted(collections.Counter(century_class(b) for b in bs).items())), by_language=dict(collections.Counter(lang_class(b) for b in bs).most_common()))
by_room = {}
BOOKS_BY_BC = collections.defaultdict(list)
for b in BOOKS: BOOKS_BY_BC[b.get('bookcase')].append(b)
for r in ROOMS:
    ids = {bc['id'] for bc in r['bookcases']}
    ids |= {o['id'] for o in OBJECTS if o['room'] == r['id']}
    rb = [b for b in BOOKS if b.get('bookcase') in ids]
    by_room[r['id']] = dict(name=r['name'], slots=len(rb), bookcases=len(r['bookcases']), shelf_metres=r.get('shelf_metres'), by_origin=dict(collections.Counter(b['origin'] for b in rb)),
                            by_placement=dict(collections.Counter(b['placement'] for b in rb)), **dim_counts(rb))
    by_room[r['id']]['by_subject'] = {}
    for bc in r['bookcases']:
        bb = BOOKS_BY_BC.get(bc['id'], [])
        bc['counts'] = dict(slots=len(bb), identified=sum(1 for b in bb if b['origin'] != 'unlabelled'), **dim_counts(bb))
        subj = bc.get('subject') or '(no caption)'
        by_room[r['id']]['by_subject'][subj] = by_room[r['id']]['by_subject'].get(subj, 0) + len(bb)
    by_room[r['id']]['objects'] = dict(collections.Counter(o['kind'] for o in OBJECTS if o['room'] == r['id']))
    by_room[r['id']]['objects_by_tier'] = dict(collections.Counter(o['tier'] for o in OBJECTS if o['room'] == r['id']))
BY_SUBJECT = collections.OrderedDict()
for r in ROOMS:
    for bc in r['bookcases']:
        subj = bc.get('subject') or '(no caption)'
        e = BY_SUBJECT.setdefault(subj, dict(subject=subj, subject_it=bc.get('subject_it'), books=0, identified=0, bookcases=[], rooms=[]))
        e['books'] += bc['counts']['slots']; e['identified'] += bc['counts']['identified']; e['bookcases'].append(bc['id'])
        if r['id'] not in e['rooms']: e['rooms'].append(r['id'])
TIERS = dict(collections.Counter(b['tier'] for b in BOOKS))
TIERS['by_room'] = {rid: rc['by_tier'] for rid, rc in by_room.items()}
TIERS['by_bookcase'] = {bc['id']: bc['counts']['by_tier'] for r in ROOMS for bc in r['bookcases']}
TIERS['objects'] = dict(collections.Counter(o['tier'] for o in OBJECTS))
TIERS['note'] = 'certain = a Braidense ECO.01 shelfmark (the running number keeps the order of the shelves in the rare-book room), or read on film / in a photograph at an identified bookcase (confidence high or medium); guess = a Braidense ECO.02 or ECO.03 record (a section of the catalogue, drawn in a stand-in cabinet), an ECO.04 reference entry, placed by subject rule, room- or subject-level reading, low-confidence reading, or in a pile whose position is a guess; unknown = placeholder slot'
TIERS['reasons'] = dict(collections.Counter(re.sub(r"'.*?'|\".*?\"|ECO\.\S+|\d\d:\d\d:\d\d|\(.*?\)|(?<=bookcase )\S+|(?<=photograph )\S+", '…', b['tier_reason']) for b in BOOKS if b['tier'] != 'unknown').most_common(20))
slots_rare = sum(1 for b in BOOKS if b.get('bookcase') in BC and BC[b['bookcase']]['kind'] == 'cabinet')
slots_work = len(BOOKS) - slots_rare - len(UNSHELVED)
cap_work = sum(CAP[i] * len(SLOTS[i]) for i in SLOTS if BC[i]['kind'] != 'cabinet')
identified = [b for b in BOOKS if b['origin'] != 'unlabelled' and b.get('placement') != 'reference']   # a reference entry is not an identified book of the flat

sources = [dict(id='braidense-opac', kind='catalogue', title='Biblioteca Nazionale Braidense OPAC, fondo Umberto Eco (%d records of sections ECO.01 to ECO.03 drawn in the cabinets; %d ECO.04 reference entries)' % (sum(1 for b in rare if b.get('catalog') == 'braidense'), len(REFERENCE)),
                url='http://opac.braidense.it/', note='Record permalinks http://opac.braidense.it/bid/<BID>. Braidense\'s catalogue documents the transferred collection and its ordering. Its additional ECO.04 section brings together publications by Eco for research and does not by itself establish a copy\'s original position in the Milan apartment. The split of the ECO.01 run between the two wall cabinets (up to c. 700 on the left, the rest on the right) is a guess.'),
           dict(id='sbn-ubo', kind='catalogue', title='SBN-UBO SebinaYOU (University of Bologna), records with possessor "Eco, Umberto" (%d records, the complete export)' % len(modern),
                url='https://sol.unibo.it/SebinaOpac/query/KF_XP:%22eco%20umberto%22%20KF_BIBVIRT:ubobu?context=catalogo', note='No Milan shelfmark: each record is placed by subject on the bookcase whose Fondazione caption fits, so its position is inferred.'),
           dict(id='fondazione-galleries', kind='photo', title='Fondazione Umberto Eco, "Le biblioteche": rectified photographs of bookcases A-S with subject captions (Studio Curti Parini)',
                url='https://fondazioneumbertoeco.org/en/lebiblioteche', note='The geometry source, together with the visitor accounts listed under "Other sources for the layout".')]
for s in L.get('sources', []):   # a layout.json film that videos.json also lists (same YouTube id in the url) is reported once, from videos.json, with its spine count
    if s.get('kind') == 'video' and any(vid in (s.get('url') or '') for vid in VIDEOS): continue
    if s.get('id') not in {x['id'] for x in sources}: sources.append(dict(id=s.get('id'), kind=s.get('kind'), title=s.get('title'), url=s.get('url'), note=s.get('note')))
used_videos = collections.Counter(s['video_id'] for b in identified for s in b.get('sightings', []) if s.get('kind') == 'video' and s.get('video_id'))
for vid, v in VIDEOS.items():
    sources.append(dict(id='video-' + vid, kind='video', video_id=vid, title=v.get('title'), uploader=v.get('uploader'), url=v.get('url') or 'https://www.youtube.com/watch?v=' + vid,
                        duration_s=v.get('duration_s'), upload_date=v.get('upload_date'), books_seen=used_videos.get(vid, 0), spines_file=any(vid in os.path.basename(p) for p in SP['video_files'])))
photo_srcs = {}
for b in identified:
    for s in b.get('sightings', []):
        if s.get('kind') == 'photo' and s.get('url'): photo_srcs.setdefault(s['url'], dict(id='photo-' + hid(s['url']), kind='photo', title=photo_name(s.get('frame'))[0].upper() + photo_name(s.get('frame'))[1:], frame=s.get('frame'), url=s['url'], credit=s.get('credit'), books_seen=0))['books_seen'] += 1
sources.extend(photo_srcs.values())

_cp = [b['copy'] for b in BOOKS if b.get('catalog') == 'bologna' and b.get('copy')]
def given_class(c):
    """The class of a Bologna copy on the 'Given to Eco' legend, the page's rule in Python: 'eco' a dedication Eco wrote himself, 'named' a giver named,
    'unnamed' a dedication noted with no giver named, 'plain' a copy with no dedication."""
    if c.get('inscribed_by_eco'): return 'eco'
    if c.get('givers'): return 'named'
    if 'dedication' in (c.get('marks') or []) or c.get('dedication_by'): return 'unnamed'
    return 'plain'
HAND_MARKS = ('marginalia', 'underlinings', 'dog-ears', 'inserts')   # the marks of Eco's own hand or use (the ex-libris stamp is the heirs', a dedication the giver's)
_givers = collections.Counter(g for c in _cp for g in (c.get('givers') or []))
BOLOGNA_COPIES = dict(with_copy_notes=len(_cp), with_eco_inventory=sum(1 for c in _cp if c.get('inventory')), with_dedication=sum(1 for c in _cp if c.get('dedication_by')),
                      with_annotation_note=sum(1 for c in _cp if c.get('annotation')), marks=dict(collections.Counter(m for c in _cp for m in c.get('marks', []))),
                      # the inscriptions transcribed, the copies inscribed (a dedication noted or a giver named), the named givers, the hand marks per copy
                      with_inscription=sum(1 for c in _cp if c.get('inscription')), inscribed=sum(1 for c in _cp if given_class(c) in ('named', 'unnamed')),
                      with_named_giver=sum(1 for c in _cp if c.get('givers')), givers=len(_givers), top_givers=[[g, n] for g, n in _givers.most_common(12)],
                      # the classes of the 'Given to Eco' legend, as the page paints them (given_class); the copies Eco inscribed himself; how the inscriptions were closed
                      given=dict(collections.Counter(given_class(c) for c in _cp)), inscribed_by_eco=sum(1 for c in _cp if c.get('inscribed_by_eco')), inscription_how=dict(INSCRIPTION_HOW),
                      copy_notes_applied=COPY_NOTES_APPLIED,
                      hand=dict(collections.Counter(str(sum(1 for m in HAND_MARKS if m in (c.get('marks') or []))) for c in _cp)),
                      hand_any=sum(1 for c in _cp if any(m in (c.get('marks') or []) for m in HAND_MARKS)))
SERVED_VOLUME_TITLES = collections.Counter((b.get('catalog') or 'other') for b in BOOKS if b.get('volume_statement'))   # the composed titles actually drawn (a set record composed and then set aside is not among them)
SERVED_VOLUME_TITLES['set within a set'] = sum(1 for b in BOOKS if b.get('set_volume')); SERVED_VOLUME_TITLES['without a set title'] = sum(1 for b in BOOKS if b.get('volume_statement') and not b.get('set_title'))
meta = dict(
    library="Umberto Eco's library, Piazza Castello 13, Milan (the apartment as it stood before the rare books went to the Braidense in 2021 and the working library to the University of Bologna in 2026)",
    owner='Umberto Eco (1932-2016)', generated=datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
    dataset='reconstruction from public photographs, visitor accounts, two library catalogues and the spine readings listed in sources; nothing was measured',
    counts=dict(books=len(BOOKS), identified=len(identified), rooms=len(ROOMS), bookcases=sum(len(r['bookcases']) for r in ROOMS), by_origin=dict(by_origin), by_placement=dict(by_placement),
                by_language=dict(by_lang.most_common()), by_room=by_room, with_description=desc_n, tiers=TIERS,
                by_source=dict(collections.Counter(source_class(b) for b in BOOKS)), by_century=dict(sorted(collections.Counter(century_class(b) for b in BOOKS).items())),
                by_subject=list(BY_SUBJECT.values()), on_film=dict(bookcases_on_camera=BC_ON_CAMERA, bookcases_total=sum(len(r['bookcases']) for r in ROOMS),
                                                                    books_on_camera=sum(len(BOOKS_BY_BC.get(bc['id'], [])) for r in ROOMS for bc in r['bookcases'] if bc['on_camera'])),
                overlay_note=dict(subject="the Fondazione's bookcase captions; the Braidense running numbers give the order of the ECO.01 run (which cabinet is the map's guess), the Bologna records are placed by subject rule, which is inferred",
                                  source='origin of each slot: read on video, read in a photograph, a Braidense record (rare room), a Bologna record (working library), or an unlabelled placeholder',
                                  certainty='three tiers from placement and confidence: ' + TIERS['note'],
                                  century='year of publication from the catalogue record or the reading, by hundred-year block; unknown where no year is recorded',
                                  language='ISO 639-1 language of the record or reading; unknown where none is recorded',
                                  on_film='bookcases on which a reading, a pile or an inventoried object of the film was placed; the rest were photographed by the Fondazione, not filmed',
                                  hand="how many kinds of mark the University of Bologna's cataloguers found in the copy: marginal notes, underlinings, folded corners, papers left inside; the ex-libris stamp is the heirs' and does not count; a book that is not one of the Bologna copies has no note",
                                  given="the copies inscribed to Eco, as the cataloguers read the dedication; the giver is named where the catalogue names one, and the words are quoted on the book's card; six copies carry a dedication Eco wrote himself"),
                objects_thumbs=dict(THUMB),
                unshelved=len(UNSHELVED), reference=len(REFERENCE),
                catalog=dict(braidense_records=sum(1 for b in rare if b.get('catalog') == 'braidense'), braidense_reference_records=len(REFERENCE), braidense_set_records_not_drawn=len(RARE_DROPPED['set_records']), braidense_export_records=RARE_EXPORT_N,
                             braidense_reconciliation=RARE_RECON, bologna_records=len(modern), bologna_placement_unknown=unknown_n, bologna_unshelved=[b['id'] for b in UNSHELVED], bologna_rules=dict(RULE_HITS.most_common()),
                             bologna_matched_via=dict(RULE_HOW), bologna_rescued=RESCUED, bologna_copies=BOLOGNA_COPIES,
                             volume_titles=dict(dict(SERVED_VOLUME_TITLES), composed=dict(VOLUME_TITLES), note='numbered volumes drawn whose display title was composed as "<set title>, vol. N" from UNIMARC 461/462 (Bologna jsonl; Braidense .mrc) or, with no set in the record, as "<own words>, vol. N"; volume_statement keeps the record\'s own title. The counts are of the entries served; `composed` is the generator\'s tally, which also counts set records composed and then set aside'),
                             part_titles_from_responsibility=len(PART_TITLES), title_tails_cleaned=len(TITLE_TAILS), authors_from_set=dict(dict(AUTHORS_FROM_SET), note='records without a statement of responsibility of their own whose author line is the set\'s (UNIMARC 461 embedded 200 $f), flagged author_from_set')),
                spine=dict(dict(SP, frames_by_level=dict(SP['frames_by_level']), rejected_other_count=len(SP['rejected_other'])), frames_unresolved_labels=[dict(room_id=k[0], wall_id=k[1], wall_name=k[2], frames=v) for k, v in UNRESOLVED.most_common()],
                           label_hits=dict(LABEL_HITS)),
                estimate=dict(milan_working_library_volumes=33000, moved_to_bologna_volumes=32000, rare_volumes_at_transfer=1328, rare_records_drawn=sum(1 for b in rare if b.get('catalog') == 'braidense'), rare_reference_records=len(REFERENCE), rare_export_records=RARE_EXPORT_N, slots_modelled=len(BOOKS),
                              slots_working_library=slots_work, slot_capacity_working_library=cap_work, slots_rare_room=slots_rare, shelf_metres_total=L.get('counts', {}).get('shelf_metres_total'),
                              shelf_metres_working_library=L.get('counts', {}).get('shelf_metres_working_library'), mean_spine_width_m=args.spine_width,
                              note='slots = shelf metres / mean spine width; the Fondazione counts c. 33,000 volumes in Milan, so the modelled shelving is %.0f%% of the estimate' % (100.0 * slots_work / 33000))),
    sources=sources, mappings=dict(wall_map=os.path.basename(args.wall_map), subject_map=os.path.basename(args.subject_map), objects_map=os.path.basename(args.objects_map) if OM_RULES else None,
                                   quotes_file=os.path.basename(args.quotes) if QF else None, tour_file=TOUR.get('file'), consolidated_books=SP.get('consolidated'), video_objects=os.path.basename(args.video_objects) if VO else None,
                                   description_files=DESC_USED, description_validation=DESC_VALIDATION, rare_spine_widths_m=RARE_W),
    camera=dict(video_id=(VO or {}).get('video_id'), rooms_seen_seconds=ROOMS_SEEN, bookcases_on_camera=BC_ON_CAMERA, bookcases_total=sum(len(r['bookcases']) for r in ROOMS),
                objects=dict(VO_STATS), auto_placed=VO_AUTO, note='a bookcase counts as filmed when a spine reading, a pile or an inventoried object of the film was placed on it; the others are drawn in fog (they were photographed by the Fondazione, not filmed)'),
    incunabula=INCUN,
    warnings=WARN, layout_notes=[fix_layout_text(n) for n in L.get('notes', []) if not n.startswith(LAYOUT_NOTES_DROP)], layout_assumptions=L.get('assumptions'),
    notes=['Origins: video = read from a frame of one of the listed videos (link opens YouTube at that second); photo = read from a published photograph; catalog = a record of the Braidense (rare books, with the Milan shelfmark) or of the University of Bologna (working library, placed by subject); unlabelled = a slot the shelving must have held, drawn as a grey spine, book unknown.',
           'Placements: catalogued = the shelfmark fixes the run and its order (which cabinet is a guess); seen = the reader placed it on that shelf; inferred = subject match only; reference = a record of the Braidense\'s ECO.04 section, listed on the reference table, its presence in the flat not established; filler = placeholder.',
           'The rare-book cabinets hold only the %d Braidense records of sections ECO.01 to ECO.03 (spine widths set so the records fill the cabinets); the %d ECO.04 records lie on the reference table in the study; every other bookcase is filled to capacity with placeholders.' % (sum(1 for b in rare if b.get('catalog') == 'braidense'), len(REFERENCE)),
           'Rooms, walls and bookcases follow eco-video/layout.json; the free-standing island units of the study are placed in the middle of the room by guess.'],
    shelf_convention='shelf 0 is the top shelf; slot 0 is the left-most book facing the unit',
    tour=TOUR, tours=TOURS, walk=WALK, notable_tours=NOTABLE_TOURS, quotes_general=GENERAL_QUOTES, brief=None,   # brief.md is an internal build document (absolute paths, notes to the builder): read, never published
    experience=dict(folder=(os.path.relpath(args.experience, PROJ) if os.path.abspath(args.experience).startswith(PROJ + os.sep) else args.experience), files_present=EXP_PRESENT,   # a project-relative folder name, never a working path objects=len(OBJECTS), objects_from_file=sum(1 for o in OBJECTS if not o.get('auto') and o['kind'] != 'pile'),
                    piles=sum(1 for o in OBJECTS if o['kind'] == 'pile'), quotes=QUOTES,
                    notable=dict(matched=NOTABLE['matched'], unmatched=NOTABLE['unmatched'], rejected=NOTABLE['rejected'], books_flagged=sum(1 for b in BOOKS if b.get('notable')),
                                 join='by the work: the notable title (or original title) must share its words with the record title or set title, and a named author must be the record\'s author; a surname elsewhere never matches; entries without a copy are tour stops marked missing'),
                    tour_stops=len(TOUR['stops']), tour_auto=TOUR['auto'], video_quotes=len(VQ), experience_quotes=len(EQ), general_quotes=len(GENERAL_QUOTES),
                    experience_objects=dict(EXP_OBJ_STATS), route_notes=len(ROUTE_NOTES), film_notes=sum(len(r.get('film_notes') or []) for r in ROOMS), notable_tours=[(t['title'], len(t['books'])) for t in NOTABLE_TOURS],
                    walk_waypoints=len(WALK['waypoints']) if WALK else 0))
meta['counts']['objects'] = dict(collections.Counter(o['kind'] for o in OBJECTS))
meta['counts']['notable'] = sum(1 for b in BOOKS if b.get('notable'))
meta['counts']['notable_missing'] = sum(t['missing'] for t in NOTABLE_TOURS)                      # works Eco is known to have used that are in no public record: the tours' `missing: true` stops
meta['counts']['notable_missing_with_nearest'] = sum(1 for t in NOTABLE_TOURS for s in t['stops'] if s.get('missing') and s.get('nearest_id'))
meta['counts']['notable_missing_by_subject'] = sum(1 for t in NOTABLE_TOURS for s in t['stops'] if s.get('missing') and not s.get('nearest_id') and s.get('subject_bookcase'))   # ghost stops shown at the bookcase their subject would give them
meta['counts']['notable_missing_room_only'] = sum(1 for t in NOTABLE_TOURS for s in t['stops'] if s.get('missing') and not s.get('nearest_id') and not s.get('subject_bookcase'))
meta['counts']['in_piles'] = sum(1 for b in BOOKS if b.get('in_pile'))
meta['counts']['english_titles'] = EN_COUNTS                                                      # books with an English title (published vs literal), English descriptions, entries for ids not in the library
meta['english_titles'] = EN_COUNTS['books'] > 0                                                    # the page shows its Native / English switch only when this is true
for o in OBJECTS:
    for k in [k for k, v in list(o.items()) if v is None or v == []]: o.pop(k)
# the same display pass over the room, bookcase, tour, walk and notable-tour texts
for r in ROOMS:
    for k in ('name', 'blurb', 'description', 'catalog_note', 'position_note', 'furniture'): clean_field(r, k)
    clean_quotes(r.get('quotes'))
    for fn in r.get('film_notes') or []:
        for k in ('label', 'description', 'note', 'item'): clean_field(fn, k)
    for bc in r['bookcases']:
        for k in ('label', 'long_label', 'subject', 'evidence'): clean_field(bc, k)
        clean_quotes(bc.get('quotes'))
        for sec in bc.get('sections') or []:
            for k in ('label', 'blurb'): clean_field(sec, k)
        for fn in bc.get('seen_in_film') or []:
            for k in ('label', 'description'): clean_field(fn, k)
for s in meta['tour']['stops']: clean_field(s, 'caption'); clean_quotes([s.get('quote')] if s.get('quote') else [])
for t in meta.get('tours') or []:
    for s in t['stops']: clean_field(s, 'caption'); clean_field(s, 'title'); clean_quotes([s.get('quote')] if s.get('quote') else [])
for w in (meta.get('walk') or {}).get('waypoints') or []: clean_field(w, 'caption'); clean_quotes([w.get('quote')] if w.get('quote') else [])
for rn in (meta.get('walk') or {}).get('route_notes') or []:
    for k in ('description', 'note', 'item'): clean_field(rn, k)
for t in meta['notable_tours']:
    clean_field(t, 'title')
    for s in t['stops']:
        clean_field(s, 'title', 'title'); clean_field(s, 'author', 'author'); clean_field(s, 'nearest_title', 'title')
        for k in ('why', 'source', 'note'): clean_field(s, k)
for u in meta['experience']['notable']['unmatched']:
    clean_field(u, 'title', 'title'); clean_field(u, 'author', 'author'); clean_field(u, 'status')
clean_quotes(meta.get('quotes_general'))
for k in ('notes', 'layout_notes'): clean_field(meta, k)
for k in list(meta['counts']['overlay_note']): clean_field(meta['counts']['overlay_note'], k)
for s in meta['sources']:
    for k in ('title', 'note'): clean_field(s, k)
meta['counts']['display_cleaned'] = dict(CLEAN_COUNTS)
meta['counts']['spine']['video_files'] = [os.path.basename(p) for p in meta['counts']['spine'].get('video_files') or []]
meta['counts']['spine']['photo_files'] = [os.path.basename(p) for p in meta['counts']['spine'].get('photo_files') or []]
meta['counts']['reading_fixes'] = FIXED_READINGS
out = dict(meta=meta, rooms=ROOMS, objects=OBJECTS, books=BOOKS)
json.dump(out, open(args.out, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(DESC_LIST, open(args.desc_list, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

print('books.json: %d slots (%d identified) in %d rooms, %d bookcases -> %s' % (len(BOOKS), len(identified), len(ROOMS), meta['counts']['bookcases'], args.out))
print('by origin:', dict(by_origin)); print('by placement:', dict(by_placement))
print('by language:', dict(by_lang.most_common(12)))
for rid, rc in by_room.items(): print('  %-16s %6d slots  %s' % (rid, rc['slots'], rc['by_origin']))
print('rare cabinets: %s records, widths %s' % ({k: len(v) for k, v in by_cab.items()}, RARE_W))
print('bologna: %d records, %d with no subject match (fallback); top rules: %s' % (len(modern), unknown_n, RULE_HITS.most_common(8)))
print('bologna copies: %s' % BOLOGNA_COPIES)
print('Bologna titles composed from the 200 subfields, differing from the export (%d); with a further $a (%d), with a parallel title (%d)' % (len(TITLES_COMPOSED), sum(1 for x in TITLES_COMPOSED if ' ; ' in x['composed']), sum(1 for x in TITLES_COMPOSED if ' = ' in x['composed'])))
print('elisions closed (%d): %s' % (len(ELISION_FIXED), ELISION_FIXED))
print('inscriptions %d (%s); copies Eco inscribed himself: %s; copy notes applied: %s' % (BOLOGNA_COPIES['with_inscription'], dict(INSCRIPTION_HOW), [b['id'] for b in BOOKS if (b.get('copy') or {}).get('inscribed_by_eco')], COPY_NOTES_APPLIED))
print('bologna matched via: %s; rescued by the extended text: %s' % (dict(RULE_HOW), [(x['id'], x['title'][:30], x['set_title'][:30], x['rule'][:30], x['how']) for x in RESCUED]))
print('tiers: %s; per room: %s' % ({k: TIERS[k] for k in ('certain', 'guess', 'unknown') if k in TIERS}, TIERS['by_room']))
print('tiers of objects: %s; tier reasons: %s' % (TIERS['objects'], TIERS['reasons']))
print('object thumbnails: %s (budget %.1f MB)' % (dict(THUMB), THUMB_BUDGET / 1048576.0))
print('overlays: by_source %s; by_century %s; subjects %d' % (meta['counts']['by_source'], meta['counts']['by_century'], len(BY_SUBJECT)))
print('spines: %s' % {k: v for k, v in SP.items() if not k.endswith('files')}, 'files:', [os.path.basename(p) for p in SP['video_files'] + SP['photo_files']])
if UNRESOLVED: print('unresolved frame labels:', UNRESOLVED.most_common(10))
print('descriptions merged: %d of %d identified; description list for the fetcher: %s (%d entries)' % (desc_n, len(identified), args.desc_list, len(DESC_LIST)))
print('working library: %d slots of %d capacity vs c. 33,000 estimate' % (slots_work, cap_work))
print('experience: files %s; objects %s; quotes placed %d (unplaced %d; %d from eco-video/quotes_*.json); notable matched %d (unmatched %d); tour %d stops (%s)' % (
    {k: v for k, v in EXP_PRESENT.items() if v} or 'none', dict(meta['counts']['objects']), QUOTES['placed'], len(QUOTES['unplaced']), len(VQ), NOTABLE['matched'], len(NOTABLE['unmatched']), len(TOUR['stops']), 'auto' if TOUR['auto'] else 'tour.json'))
print('rejected (room_id other, not Eco\'s books): %d readings, e.g. %s' % (len(SP['rejected_other']), [(r.get('title') or '')[:30] for r in SP['rejected_other'][:5]]))
print('catalogue matches refused by the agreement rule %d %s; catalog_record forced %d, forbidden %d; working-shelf readings attached to a Braidense record %d %s; '
      'Bologna records moved to a tagged bookcase %d %s; pile sightings off the flat dropped %d (readings kept in rejected_other %d); second copies noted %d' % (
      SP['catalog_match_rejected'], [(t[0] or '')[:30] + ' -> ' + t[1] for t in CATALOG_REJECTED], SP['catalog_forced'], SP['catalog_forbidden'], SP['catalog_braidense_cross_room'], [('%s / %s' % (c[4], c[5]), c[2], c[6]) for c in CATALOG_CROSS],
      SP['catalog_moved_to_tag'], [(m[0], m[1], '->', m[2]) for m in CATALOG_MOVED], SP['pile_sightings_off_flat'], SP['pile_readings_off_flat'], len(SECOND_COPIES)))
print('spine source: %s' % ('consolidated %s (%d books, %d untitled skipped)' % (SP.get('consolidated'), SP.get('consolidated_books', 0), SP.get('consolidated_untitled', 0)) if CONSOL is not None else 'raw spines_*.jsonl'))
print('descriptions files: %s' % DESC_USED)
print('film objects: %s; auto-placed to check: %d' % (dict(VO_STATS), len(VO_AUTO)))
print('camera: rooms seen %s; bookcases on camera %d of %d' % (ROOMS_SEEN, len(ON_CAMERA), sum(len(r['bookcases']) for r in ROOMS)))
print('incunabula: %s' % INCUN)
print('display cleaning: %s; reading fixes: %s; notable missing: %d (%d with a nearest same-author record)' % (dict(CLEAN_COUNTS), FIXED_READINGS, meta['counts']['notable_missing'], meta['counts']['notable_missing_with_nearest']))
print('english titles: %d books (%d published, %d literal), %d descriptions; %d same as native, %d entries for ids not in the library; files %s' % (EN_COUNTS['books'], EN_COUNTS['published'], EN_COUNTS['literal'], EN_COUNTS['descriptions'], EN_COUNTS['same_as_native'], EN_COUNTS['unmatched'], [f['file'] for f in EN_COUNTS['files']] or 'none'))
print('quotes: %d in pool (%d experience placed, %d general, %d from %s, %d eco-video files); placed %d, unplaced %d' % (len(QALL), len(EQ), len(GENERAL_QUOTES), len(QF), os.path.basename(args.quotes), len(VQ), QUOTES['placed'], len(QUOTES['unplaced'])))
print('experience objects: %s; route notes %d; film notes %d' % (dict(EXP_OBJ_STATS), len(ROUTE_NOTES), sum(len(r.get('film_notes') or []) for r in ROOMS)))
print('tours: %s; quotes %d, images %d (%d KB)' % ([(t['id'], len(t['stops']), 'dropped %d' % t['dropped']) for t in TOURS] or 'none (no tours_eco.json)', sum(1 for t in TOURS for st in t['stops'] if st.get('quote')), TOUR_IMG['n'], TOUR_IMG['bytes'] // 1024))
print('notable: matched %d, unmatched %d, rejected stand-ins %d %s; tours: %s' % (NOTABLE['matched'], len(NOTABLE['unmatched']), len(NOTABLE['rejected']), [(r['id'], (r['record_title'] or '')[:30]) for r in NOTABLE['rejected']], [(t['title'], len(t['books']), 'missing %d' % t['missing']) for t in NOTABLE_TOURS]))
print('volume titles composed: %s; served: %s; unshelved Bologna records: %d' % (dict(VOLUME_TITLES), dict(SERVED_VOLUME_TITLES), len(UNSHELVED)))
print('Braidense export: %d records; %d set records not drawn (their ids resolve to the first volume); %d ECO.04 reference entries listed, not shelved (%d inventoried before August 2021, %d after, %d without an inventory date); %d records drawn in the cabinets; reconciliation %s' % (
    RARE_EXPORT_N, len(RARE_DROPPED['set_records']), len(REFERENCE), sum(1 for b in REFERENCE if (b.get('copy') or {}).get('inventory_date', '9') < '2021-08'), sum(1 for b in REFERENCE if (b.get('copy') or {}).get('inventory_date', '') >= '2021-08'),
    sum(1 for b in REFERENCE if not (b.get('copy') or {}).get('inventory_date')), sum(1 for b in rare if b.get('catalog') == 'braidense'), {k: v for k, v in RARE_RECON.items() if k != 'note'}))
if args.dropped_log:
    with open(args.dropped_log, 'w', encoding='utf-8') as _fh:
        for x in RARE_DROPPED['set_records']: _fh.write(json.dumps(dict(id=x['id'], title=x['title'], change='not drawn', why='a set record whose volumes have records of their own in the export and no inventory of its own: the volumes are the spines', volumes=['braidense:' + k for k in x['volumes']]), ensure_ascii=False) + '\n')
        for x in sorted(REFERENCE, key=lambda b: b.get('shelfmark') or ''): _fh.write(json.dumps(dict(id=x['id'], title=x['title'][:60], year=x.get('year'), date=x.get('date'), shelfmark=x.get('shelfmark'), change='reference entry, not shelved', copy={k: v for k, v in (x.get('copy') or {}).items() if k != 'holdings'}, note=x.get('placement_note')), ensure_ascii=False) + '\n')
    print('records log: %s (%d set records, %d reference entries)' % (args.dropped_log, len(RARE_DROPPED['set_records']), len(REFERENCE)))
print('shelf labels used: %s; readings merged on the same bay: %d; merged across piles: %d' % (dict(LABEL_HITS), SP['merged_same_bay'], SP['merged_across_piles']))
if SP['dense_entries']:
    _dense_books = [b for b in BOOKS if b.get('dense_ids')]
    print('dense pass: %d entries in the raw files; readings with a dense sighting %d (%d dense-only, %d also read by the first pass), pile books %d; catalogue links from the dense matches %d (%d pointed at no record), '
          'Bologna records upgraded to seen %d, records seen on another bookcase %d; tiers: dense certain kept at guess (tag unverified) %d, probable/guess capped from certain %d; books carrying dense ids %d, by tier %s, by origin %s; '
          'same-slot conflicts the dense pass won: first-pass sightings dropped %d (of %d listed in the dense files), readings that lost every sighting %d'
          % (SP['dense_entries'], SP['dense_readings'], SP['dense_only_books'], SP['dense_books_with_first_pass'], SP['dense_pile_books'], SP['dense_catalog_links'], SP['dense_catalog_links_failed'], SP['dense_catalog_upgraded'],
             SP['dense_catalog_disagree'], SP['dense_certain_unverified'], SP['dense_tier_capped'], len(_dense_books), dict(collections.Counter(b['tier'] for b in _dense_books)), dict(collections.Counter(b['origin'] for b in _dense_books)),
             SP['dense_conflict_dropped'], len(CONFLICT_DROP), SP['dense_conflict_readings_lost']))
    for x in DENSE_TIER_CHANGES[:40]: print('   dense tier cap: %s %s (%s)' % x)
    for b in BOOKS:
        if b.get('seen_elsewhere'): print('   catalogue record seen elsewhere on film: %s | %s | placed %s, dense pass read it on %s at %s (%s)' % (b['id'], (b.get('title') or '')[:40], b.get('bookcase'), b['seen_elsewhere']['bookcase'], b['seen_elsewhere'].get('time'), b['seen_elsewhere'].get('dense_id')))
print('descriptions validated: %d rejected %s; cleaned %s' % (DESC_VALIDATION['rejected'], DESC_VALIDATION['by_reason'], DESC_VALIDATION['cleaned']))
for x in DESC_VALIDATION['rejected_ids']: print('   rejected description: %s | %s | %s | %s | %s' % (x['id'], x['title'][:40], x['author'], x['wikipedia_title'], x['reason']))
PIANO_ROOMS = collections.Counter((BC_ROOM.get(b.get('bookcase')) or next((o['room'] for o in OBJECTS if o['id'] == b.get('bookcase')), None), b.get('bookcase')) for b in BOOKS
                                  if any(s.get('video_id') == 'zZEy10fpq3I' and 2570 <= (s.get('timestamp_raw_s') or -1) <= 2583 for s in b.get('sightings') or []))
print('books read on the piano pass (film 42:50-43:03), by room and holder: %s' % dict(PIANO_ROOMS))
print('piles with a counted height (books_high): %d; pile fillers %d; author-only pile books %d; further copies in other piles %d; alternative readings %d (%d preferred over the first reading)' % (SP['piles_with_height'], SP['pile_fillers'], SP['author_only_placed'], SP['pile_copies'], SP['alt_readings'], SP['alt_preferred']))
print('piano reference (%s): %d piles stacked from it; entries matched by reading id %d, by title / fragment / spine text / author %d, first-pass readings kept at blank positions %d, books from the reference %d, second copies %d, first-pass readings kept as alternatives %d' % (PIANO_REF_META.get('file') or 'none', SP['pile_ref_piles'], SP['pile_ref_by_id'], SP['pile_ref_matched'], SP['pile_ref_first_pass'], SP['pile_ref_new'], SP['pile_ref_copies'], SP['pile_ref_alternatives']))
for o in OBJECTS:
    if o.get('books_high'): print('   %s: %d high, %d identified (%s), %d unlabelled' % (o['id'], o['books_high'], o.get('books_identified', 0), ', '.join((BOOK_BY_ID[x].get('display_title') or BOOK_BY_ID[x]['title'] or '?')[:28] for x in o.get('books') or [] if x in BOOK_BY_ID), o['count'] - o.get('books_identified', 0)))
print('walk: %s' % ('%d waypoints, %.0f s' % (len(WALK['waypoints']), WALK['duration_s']) if WALK else 'none'))
print('timestamp offsets applied: %s' % {v: o for v, o in ((k, video_offset(k)) for k in VIDEOS) if o})
print('part titles taken from the statement of responsibility (%d): %s' % (len(PART_TITLES), PART_TITLES))
print('title-kind strings the tail rule changed (%d): %s' % (len(TITLE_TAILS), TITLE_TAILS))
