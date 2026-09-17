#!/usr/bin/env python3
"""Build the self-contained pages of the Eco library map.

  python3 build_eco.py [--src index_eco.html] [--data books.json] [--out dist] [--three vendor]

`--three` may be the flat vendor/ folder shipped here (three.module.min.js, OrbitControls.js, PointerLockControls.js,
three r160) or an unpacked npm `three` package (build/three.module.min.js, examples/jsm/controls/*.js); both layouts are
looked up. Writes:
  dist/eco-map.html            self-contained: three.js served through blob: URLs via an import map + books.json inlined
  dist/eco-map-artifact.html   the same for hosts that ignore import maps or block blob: module scripts (the module
                               specifiers are rewritten at load time; falls back to the jsdelivr ESM builds of three r160)
  dist/index.html              the loose page (fetches books.json, loads three from ./vendor/)
  dist/books.json, dist/vendor/*.js, dist/preview.jpg (when eco-map/preview.jpg exists)
"""
import argparse, json, os, re, shutil, sys

H = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--src', default=os.path.join(H, 'index_eco.html'))
ap.add_argument('--data', default=os.path.join(H, 'books.json'))
ap.add_argument('--out', default=os.path.join(H, 'dist'))
ap.add_argument('--three', default=os.path.join(H, 'vendor'), help='flat vendor/ folder or unpacked npm three package')
ap.add_argument('--name', default='eco-map', help='base name of the output files')
ap.add_argument('--cdn', action='store_true', help='keep the CDN import map in the loose dist/index.html')
args = ap.parse_args()

html = open(args.src, encoding='utf-8').read()
data_text = open(args.data, encoding='utf-8').read()
data = json.loads(data_text)   # validate
os.makedirs(args.out, exist_ok=True)

IMPORTMAP_RE = re.compile(r'<script type="importmap">.*?</script>', re.S)
DATA_RE = re.compile(r'<script id="data" type="application/json">.*?</script>', re.S)
assert IMPORTMAP_RE.search(html) and DATA_RE.search(html), 'the template is missing the importmap or data block'

LIBS = [('three', ['three.module.min.js', 'build/three.module.min.js'], 'lib-three'),
        ('three/addons/controls/OrbitControls.js', ['OrbitControls.js', 'examples/jsm/controls/OrbitControls.js'], 'lib-orbit'),
        ('three/addons/controls/PointerLockControls.js', ['PointerLockControls.js', 'examples/jsm/controls/PointerLockControls.js'], 'lib-plc')]

def lib_path(rels):
    for rel in rels:
        p = os.path.join(args.three, rel)
        if os.path.exists(p): return p
    sys.exit('three.js file not found under %s: tried %s' % (args.three, rels))
def read_lib(rels):
    src = open(lib_path(rels), encoding='utf-8').read()
    src = re.sub(r'//# sourceMappingURL=.*$', '', src, flags=re.M)
    if '</script' in src.lower() or '<!--' in src:
        sys.exit('library %s contains a </script> or <!-- sequence; cannot inline verbatim' % rels[0])
    return src

# ---- loose copy + vendor dir
vend = os.path.join(args.out, 'vendor'); os.makedirs(vend, exist_ok=True)
for spec, rels, _ in LIBS:
    shutil.copyfile(lib_path(rels), os.path.join(vend, os.path.basename(rels[0])))
loose = html
if not args.cdn:
    imap = {'imports': {spec: './vendor/' + os.path.basename(rels[0]) for spec, rels, _ in LIBS}}
    loose = IMPORTMAP_RE.sub(lambda m: '<script type="importmap">\n' + json.dumps(imap, indent=1) + '\n</script>', loose)
open(os.path.join(args.out, 'index.html'), 'w', encoding='utf-8').write(loose)
shutil.copyfile(args.data, os.path.join(args.out, 'books.json'))
prev = os.path.join(H, 'preview.jpg')   # the picture the preview tags name (og:image); rendered from the page by make_preview_eco.py, copied beside the loose page
if os.path.exists(prev): shutil.copyfile(prev, os.path.join(args.out, 'preview.jpg'))

# ---- self-contained file: the inlined dataset drops what the page can reconstruct (null fields; the filler slots'
# tier_reason "empty slot", which the page's tierReason() supplies), keeping the artifact well under the 16 MB limit.
# A filler slot (origin unlabelled, placement filler, tier unknown, section <bookcase>-s) ships as {id, bookcase,
# shelf, slot, width, height, f: 1} and the page's loadData() puts the four fields back (about 1.7 MB over 22,000 slots);
# books.json itself, copied into dist/ unchanged, keeps every field.
def slim(o):
    if isinstance(o, dict):
        out = {k: slim(v) for k, v in o.items() if v is not None}
        if out.get('tier') == 'unknown' and out.get('tier_reason') == 'empty slot': del out['tier_reason']
        if out.get('placement') == 'filler' and out.get('origin') == 'unlabelled' and out.get('tier') == 'unknown' and not out.get('pile_filler'):
            for k in ('placement', 'origin', 'tier'): del out[k]
            if out.get('section') == str(out.get('bookcase')) + '-s': del out['section']
            out['f'] = 1
        return out
    if isinstance(o, list): return [slim(v) for v in o]
    return o
compact = json.dumps(slim(data), ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
blocks = ''.join('<script type="text/plain" id="%s">%s</script>\n' % (bid, read_lib(rels)) for _, rels, bid in LIBS)
loader = '''<script>
(function () {
  function blob(id) { return URL.createObjectURL(new Blob([document.getElementById(id).textContent], { type: 'text/javascript' })); }
  var im = document.createElement('script'); im.type = 'importmap';
  im.textContent = JSON.stringify({ imports: {%s} });
  document.currentScript.after(im);
})();
</script>''' % ', '.join("'%s': blob('%s')" % (spec, bid) for spec, _, bid in LIBS)
single = IMPORTMAP_RE.sub(lambda m: blocks + loader, html, count=1)
single = DATA_RE.sub(lambda m: '<script id="data" type="application/json">' + compact + '</script>', single, count=1)
single = single.replace('<title>', '<!-- Self-contained build: three.js r160 (MIT, https://github.com/mrdoob/three.js) and the dataset are inlined. -->\n<title>', 1)
outp = os.path.join(args.out, args.name + '.html')
open(outp, 'w', encoding='utf-8').write(single)
# ---- artifact variant (no import map)
MAIN_RE = re.compile(r'<script type="module">(.*?)</script>', re.S)
main_src = MAIN_RE.findall(html)[-1]
assert '</script' not in main_src.lower(), 'the page module contains a </script> sequence'
artifact_loader = '''<script>
(async function () {
  const T = (id) => document.getElementById(id).textContent;
  const CDN = { three: 'https://cdn.jsdelivr.net/npm/three@0.160.0/+esm',
    orbit: 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js/+esm',
    plc: 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/PointerLockControls.js/+esm' };
  const wire = (src, u) => src.replace(/from\\s*(['"])three\\1/g, () => "from '" + u.three + "'")
    .replace(/(['"])three\\/addons\\/controls\\/OrbitControls\\.js\\1/g, () => "'" + u.orbit + "'")
    .replace(/(['"])three\\/addons\\/controls\\/PointerLockControls\\.js\\1/g, () => "'" + u.plc + "'");
  const blob = (src) => URL.createObjectURL(new Blob([src], { type: 'text/javascript' }));
  let urls;
  try {
    const three = blob(T('lib-three'));
    await import(three);   // rejects where blob: module scripts are not allowed
    urls = { three, orbit: blob(wire(T('lib-orbit'), { three })), plc: blob(wire(T('lib-plc'), { three })) };
  } catch (e) { urls = CDN; }
  const s = document.createElement('script'); s.type = 'module'; s.textContent = wire(T('app-main'), urls); document.body.appendChild(s);
})();
</script>'''
art = IMPORTMAP_RE.sub(lambda m: blocks, html, count=1)
art = DATA_RE.sub(lambda m: '<script id="data" type="application/json">' + compact + '</script>', art, count=1)
art = art.replace('<script type="module">' + main_src + '</script>', '<script type="text/plain" id="app-main">' + main_src + '</script>\n' + artifact_loader)
art = art.replace('<title>', '<!-- Self-contained build for hosts without import maps: three.js r160 (MIT, https://github.com/mrdoob/three.js) and the dataset are inlined. -->\n<title>', 1)
open(os.path.join(args.out, args.name + '-artifact.html'), 'w', encoding='utf-8').write(art)

print('books:', len(data['books']), ' bookcases:', sum(len(r['bookcases']) for r in data['rooms']))
for f in [args.name + '.html', args.name + '-artifact.html', 'index.html', 'books.json']:
    p = os.path.join(args.out, f); print('%-24s %8.0f KB' % (f, os.path.getsize(p) / 1024))
LIMIT = 16 * 1024 * 1024
art_size = os.path.getsize(os.path.join(args.out, args.name + '-artifact.html'))
if art_size >= LIMIT: sys.exit('the artifact file is %.1f MB, over the 16 MB limit' % (art_size / 1048576))
print('artifact %.2f MB of the 16 MB limit' % (art_size / 1048576))
