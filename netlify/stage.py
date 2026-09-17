#!/usr/bin/env python3
"""Stage a 3D library map for a Netlify drag-and-drop / MCP deploy.

  python3 stage.py eco                    # src + site defaults from sites.json
  python3 stage.py --src DIR --out DIR    # explicit paths (site name optional)
  python3 stage.py eco --out DIR          # override the output dir
  python3 stage.py eco --index index_eco.html   # page file other than index.html

Copies the page (index.html, or the file named by the site's "index" key in sites.json /
--index; the Eco source names its page index_eco.html), books.json and vendor/{three.module.min.js,OrbitControls.js,
PointerLockControls.js} from the source folder, rewrites the <script type="importmap">
block the way build_eco.py does (unpkg CDN -> ./vendor/), and writes
netlify.toml + _headers.  The page's preview tag (og:image) names a picture,
preview.jpg at the site's root: it is staged too, from dist/preview.jpg (where build_eco.py puts it
beside the loose page) or else from the source folder's own preview.jpg, and the run fails if the
page names it and neither exists.  The output dir is wiped first, so the run is idempotent.
Stdlib only.  Never writes under /mnt/project-files.
"""
import argparse, hashlib, json, os, re, shutil, signal, sys, tempfile

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # quiet exit when piped into head

HERE = os.path.dirname(os.path.abspath(__file__))
SITES_JSON = os.path.join(HERE, 'sites.json')
PROJECT_ROOT = '/mnt/project-files'
DEFAULT_OUT_ROOT = os.path.join(tempfile.gettempdir(), 'eco-netlify')   # a folder outside the source tree; --out overrides it

# --- replicated from build_eco.py (keep in sync; it is not imported
#     because it parses argv and reads files at import time)
IMPORTMAP_RE = re.compile(r'<script type="importmap">.*?</script>', re.S)
OG_IMAGE_RE = re.compile(r'<meta\s+property="og:image"\s+content="([^"]*)"')   # the preview picture the page names
DATA_RE = re.compile(r'<script id="data" type="application/json">.*?</script>', re.S)
LIBS = [('three', 'build/three.module.min.js', 'lib-three'),
        ('three/addons/controls/OrbitControls.js', 'examples/jsm/controls/OrbitControls.js', 'lib-orbit'),
        ('three/addons/controls/PointerLockControls.js', 'examples/jsm/controls/PointerLockControls.js', 'lib-plc')]
VENDOR_FILES = [os.path.basename(rel) for _, rel, _ in LIBS]

NETLIFY_TOML = '[build]\n  publish = "."\n'
HEADERS = ('/books.json\n  Cache-Control: public, max-age=3600\n'
           '/vendor/*\n  Cache-Control: public, max-age=3600\n')


def preview_name(html):
    """The site-relative path of the picture the page's og:image tag names (preview.jpg), or None when the page names none."""
    m = OG_IMAGE_RE.search(html)
    if not m:
        return None
    path = re.sub(r'^https?://[^/]*', '', m.group(1)).split('?')[0].split('#')[0].lstrip('/')
    if not path or '..' in path.split('/'):
        die('the page\'s og:image tag names an address this script cannot stage: %s' % m.group(1))
    return path


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def rewrite_importmap(html):
    """Same transformation as build_eco.py's loose dist/index.html."""
    imap = {'imports': {spec: './vendor/' + os.path.basename(rel) for spec, rel, _ in LIBS}}
    return IMPORTMAP_RE.sub(lambda m: '<script type="importmap">\n' + json.dumps(imap, indent=1) + '\n</script>', html)


def die(msg):
    sys.exit('stage.py: ' + msg)


def load_sites():
    try:
        with open(SITES_JSON, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def netlify_name(site, cfg):
    url = (cfg or {}).get('url')
    if url:
        return re.sub(r'^https?://', '', url).split('.')[0]
    return site + '-library-map'


def writable_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
        probe = tempfile.NamedTemporaryFile(dir=path, delete=True)
        probe.close()
        return True
    except OSError:
        return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('site', nargs='?', help='key in sites.json (eco)')
    ap.add_argument('--src', help='source folder (default: sites.json src for the site)')
    ap.add_argument('--out', help='output folder (default: %s/<netlify-site-name>/)' % DEFAULT_OUT_ROOT)
    ap.add_argument('--index', help='page file inside src (default: sites.json "index" for the site, else index.html)')
    args = ap.parse_args()

    sites = load_sites()
    cfg = sites.get(args.site) if args.site else None
    if args.site and cfg is None:
        die('unknown site %r; known: %s' % (args.site, ', '.join(sorted(sites)) or '(sites.json missing)'))
    if not args.site and not (args.src and args.out):
        die('give a site name (eco) or both --src and --out')

    src = os.path.abspath(args.src or cfg['src'])
    index = args.index or (cfg or {}).get('index') or 'index.html'
    name = netlify_name(args.site, cfg) if args.site else os.path.basename(src.rstrip('/'))
    out = args.out or os.path.join(DEFAULT_OUT_ROOT, name)
    out = os.path.abspath(out)

    # --- safety: never stage into the project tree or onto the source
    if out == src or out.startswith(src + os.sep):
        die('output dir must not be the source dir or inside it')
    if out == PROJECT_ROOT or out.startswith(PROJECT_ROOT + os.sep):
        die('refusing to write under %s (use --out somewhere else)' % PROJECT_ROOT)

    # --- check inputs, fail loudly
    if not os.path.isdir(src):
        die('source folder missing: ' + src)
    missing = [p for p in [index, 'books.json'] + [os.path.join('vendor', v) for v in VENDOR_FILES]
               if not os.path.isfile(os.path.join(src, p))]
    if missing:
        die('missing in %s: %s' % (src, ', '.join(missing)))

    html = open(os.path.join(src, index), encoding='utf-8').read()
    if not IMPORTMAP_RE.search(html) or not DATA_RE.search(html):
        die(index + ' is missing the importmap or data block')
    m = re.search(r'<title>([^<]*)', html)
    title = m.group(1).strip() if m else '(no <title>)'
    json.loads(open(os.path.join(src, 'books.json'), encoding='utf-8').read())  # validate
    # --- the preview picture the page names (og:image), staged at the path the tag expects
    preview = preview_name(html)
    preview_src = None
    if preview:
        cands = [os.path.join(src, 'dist', preview), os.path.join(src, preview)]
        preview_src = next((c for c in cands if os.path.isfile(c)), None)
        if not preview_src:
            die('the page names %s in its og:image tag, but neither %s nor %s exists' % (preview, cands[0], cands[1]))
        with open(preview_src, 'rb') as f:
            head = f.read(3)
        if preview.lower().endswith(('.jpg', '.jpeg')) and head != b'\xff\xd8\xff':
            die('%s is not a JPEG' % preview_src)

    # --- pick a writable output dir
    if not writable_dir(os.path.dirname(out)):
        fallback = tempfile.mkdtemp(prefix='netlify-stage-')
        print('note: %s not writable, using %s' % (os.path.dirname(out), fallback), file=sys.stderr)
        out = os.path.join(fallback, name)

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, 'vendor'))

    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(rewrite_importmap(html))
    shutil.copyfile(os.path.join(src, 'books.json'), os.path.join(out, 'books.json'))
    for v in VENDOR_FILES:
        shutil.copyfile(os.path.join(src, 'vendor', v), os.path.join(out, 'vendor', v))
    if preview_src:
        os.makedirs(os.path.dirname(os.path.join(out, preview)) or out, exist_ok=True)
        shutil.copyfile(preview_src, os.path.join(out, preview))
    with open(os.path.join(out, 'netlify.toml'), 'w', encoding='utf-8') as f:
        f.write(NETLIFY_TOML)
    with open(os.path.join(out, '_headers'), 'w', encoding='utf-8') as f:
        f.write(HEADERS)

    # --- report
    print('staged: ' + out)
    print('page: %s -> index.html  (title: %s)' % (index, title))
    if preview_src:
        other = [c for c in [os.path.join(src, 'dist', preview), os.path.join(src, preview)] if c != preview_src and os.path.isfile(c)]
        same = all(sha256_of(c) == sha256_of(preview_src) for c in other)
        print('preview: %s -> %s  (og:image; sha256 %s%s)' % (os.path.relpath(preview_src, src), preview, sha256_of(preview_src), '' if same else '; NOTE: %s differs from it' % ', '.join(os.path.relpath(c, src) for c in other)))
    else:
        print('preview: the page names no og:image, nothing staged for it')
    total = 0
    for root, dirs, files in os.walk(out):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(root, fn)
            sz = os.path.getsize(p)
            total += sz
            print('  %10d  %s' % (sz, os.path.relpath(p, out)))
    print('  %10d  total (%.1f MB)' % (total, total / 1e6))

    hits = []
    for root, _, files in os.walk(out):
        for fn in files:
            if fn.endswith(('.html', '.js', '.json', '.toml')) or fn == '_headers':
                p = os.path.join(root, fn)
                for i, line in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
                    if 'unpkg.com' in line:
                        hits.append('%s:%d:%s' % (os.path.relpath(p, out), i, line.rstrip()[:120]))
    if hits:
        print('FAIL: unpkg.com references remain:')
        print('\n'.join('  ' + h for h in hits))
        sys.exit(1)
    print('grep -r unpkg.com %s -> no matches (import map points at ./vendor/)' % out)
    if args.site:
        print('site: %s  site_id: %s  url: %s' % (args.site, cfg.get('site_id') or 'TODO (sites.json)', cfg.get('url') or 'TODO (sites.json)'))


if __name__ == '__main__':
    main()
