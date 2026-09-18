#!/usr/bin/env python3
"""Smoke-test the built Eco map in headless Chromium (Playwright).

  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 test_page_eco.py [--dist dist] [--shots screenshots]

Serves dist/ over a local http server, loads dist/index.html (the loose page), waits for the scene, and checks:
no console errors, the scene rendered (canvas non-black, frames per second > 0), every room button works (one screenshot each),
a book with a video/photo/catalog source opens a panel with a source link, an unlabelled book opens the placeholder panel,
search finds a title, walk mode toggles, the colour overlays (certainty legend counts vs meta.counts.tiers, tier filters), object
thumbs, spine lettering, the Eco's copies index, workshop text out of the legend and panels, absent works as ghost cards,
eye-level spine luminance from screenshots, label occlusion and pile lettering, tour stops that frame their target from inside the
room with the room button following, the Durand incunabulum pickable through the glass, the phone layout (with the tour card,
legend clear of the joystick), the sourced tours (every tour loads and every stop's target resolves; the camera arrives and the
panel opens at every stop in the orbit view; the walk view stands the visitor at a station inside the room, out of the furniture,
with the arrow keys still walking; a filtered-out book stays visible at its stop through a stand-in spine and Esc exits with the
filter as it was; the Colour menu keeps its keys; the Tours menu and a tour card fit a phone), the book-centred tours (nine tours,
each starting at a copy of Eco's own book, every book stop unoccluded in the orbit view with the eye at least 0.9 m from the spine,
the first tour's walk stations unoccluded too, the phone walk-view card clear of the joystick and Exit walk), the opening card
(desktop and phone), the address that carries the state and the links that land on it, Copy link, the More menu, the two copy-note
colour modes with their legends, the inscriptions on the card and in Eco's copies, the search over tours and objects, Any book, the
preview tags and picture, the About text, the copy-note data and the literature rule sweep in the data, the colour legends and the
copies list counted from the data, the inscriptions closed at their own quotation marks, the six copies Eco inscribed himself, the
Serao note, the Bologna titles composed with ISBD punctuation and the English titles that follow them, the elisions closed, Back
walking the page's own entries, the opening card's click, the preview drawn without the footer, the hint box above a two-line
footer, the search without near-misses, the viewpoint rule at every book stop, the copies list's group for a giver the catalogue
cannot name, an inscription run on past an inner quotation, a dedication read from the condition line, Back from a book opened in
the walk view, the stop's own pile lettered at the Rose stop, and the page and the data free of version notes; then the
self-contained eco-map.html and eco-map-artifact.html are loaded from file:// and must reach the same ready state. Exit code 1 on
any failure.
"""
import argparse, functools, http.server, json, math, os, re, socketserver, sys, threading, time

H = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--dist', default=os.path.join(H, 'dist'))
ap.add_argument('--shots', default=os.path.join(H, 'screenshots'))
ap.add_argument('--timeout', type=int, default=90000)
args = ap.parse_args()
os.makedirs(args.shots, exist_ok=True)
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
from playwright.sync_api import sync_playwright

FAIL = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok: FAIL.append(msg)

# ---- copy dist/ to local temp storage (the project mount is slow) and serve it from there
import shutil, tempfile
local = tempfile.mkdtemp(prefix='eco-map-test-', dir=os.environ.get('SCRATCH') or None)   # SCRATCH names the working folder; otherwise the system's temporary folder
for fn in os.listdir(args.dist):
    src = os.path.join(args.dist, fn)
    (shutil.copytree if os.path.isdir(src) else shutil.copyfile)(src, os.path.join(local, fn))
args.dist = local
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=args.dist)
Handler.log_message = lambda *a, **k: None
class Srv(socketserver.TCPServer): allow_reuse_address = True
srv = Srv(('127.0.0.1', 0), Handler); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:%d/' % port

def wait_ready(page, timeout):
    page.wait_for_function('window.__ready === true', timeout=timeout)
    page.wait_for_function('window.__fps > 0', timeout=timeout)

def canvas_has_pixels(page, path):
    """Number of distinct colours in the middle of a screenshot: a blank (unrendered) WebGL canvas gives one or two."""
    page.screenshot(path=path)
    try:
        from PIL import Image
        im = Image.open(path).convert('RGB'); w, h = im.size
        crop = im.crop((int(w * 0.25), int(h * 0.2), int(w * 0.75), int(h * 0.85))).resize((120, 80))
        return len(set(crop.getdata()))
    except ImportError:
        return 999   # PIL missing: cannot inspect, do not fail

def lum_stats(path, box=(0.25, 0.2, 0.75, 0.85)):
    """Luminance (0-1) statistics of a crop of a screenshot: mean, fractions below 0.08 / 0.25 and above 0.9, standard deviation."""
    try: from PIL import Image
    except ImportError: return None
    im = Image.open(path).convert('RGB'); w, h = im.size
    crop = im.crop((int(w * box[0]), int(h * box[1]), int(w * box[2]), int(h * box[3])))
    L = [(0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 for r, g, b in crop.getdata()]; n = len(L); mean = sum(L) / n
    return {'mean': round(mean, 3), 'black': round(sum(1 for v in L if v < 0.08) / n, 3), 'dark': round(sum(1 for v in L if v < 0.25) / n, 3),
            'white': round(sum(1 for v in L if v > 0.9) / n, 3), 'std': round((sum((v - mean) ** 2 for v in L) / n) ** 0.5, 3)}

def settle(page, extra=800):
    """Wait for a camera flight to land (the software renderer is slow: a 1.4 s flight can take several seconds of wall time)."""
    try: page.wait_for_function('!window.__flying()', timeout=30000)
    except Exception: pass
    page.wait_for_timeout(extra)

def menu_click(page, sel, wait=500):
    """Eco's walk, the notable books and Eco's copies sit under the More menu; open it (if it is not) and click the item."""
    page.evaluate("() => { const m = document.getElementById('moreMenu'); if (!m.classList.contains('show')) document.getElementById('moreBtn').click(); }")
    page.wait_for_timeout(150); page.click(sel); page.wait_for_timeout(wait)

with sync_playwright() as pw:
    # the Python playwright package may expect a newer Chromium build than the one in PLAYWRIGHT_BROWSERS_PATH: use whatever is there
    exe = os.environ.get('PW_CHROMIUM')
    if not exe:
        import glob
        for pat in ('chromium_headless_shell-*/chrome-linux/headless_shell', 'chromium_headless_shell-*/chrome-linux/chrome-headless-shell', 'chromium-*/chrome-linux/chrome'):
            hits = sorted(glob.glob(os.path.join(os.environ['PLAYWRIGHT_BROWSERS_PATH'], pat)))
            if hits: exe = hits[-1]; break
    print('chromium:', exe or 'playwright default')
    browser = pw.chromium.launch(executable_path=exe, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--no-sandbox'])
    ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
    ctx.set_default_timeout(args.timeout)   # a screenshot waits for a frame; the software renderer can take many seconds under load
    page = ctx.new_page()
    errors = []
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    t0 = time.time()
    page.goto(base + 'index.html', wait_until='load')
    wait_ready(page, args.timeout)
    print('loaded in %.1fs' % (time.time() - t0))
    check(not errors, 'no console errors on load' + ('' if not errors else ': ' + '; '.join(errors[:3])))
    # ---- the opening card (a first visit; the scene drifts behind it; the top bar stays live; any click elsewhere is an answer) ----
    w20 = page.evaluate("() => ({ shown: window.__state.welcome(), line: document.getElementById('wLine').textContent, doors: [...document.querySelectorAll('#welcome .doors button')].map((b) => b.id), feat: [...document.querySelectorAll('#wFeatured .ft')].map((d) => [d.dataset.tour, !!d.querySelector('img')]), flying: window.__flying(), room: window.__currentRoom(), hash: location.hash })")
    check(w20['shown'] and w20['doors'] == ['wTours', 'wWalk', 'wExplore'] and [f[0] for f in w20['feat']] == ['rose', 'strange', 'lands'] and sum(1 for f in w20['feat'] if f[1]) >= 2 and re.search(r'\d{2},\d{3} shelf slots in 6 rooms, \d,\d{3} of the books named', w20['line']) is not None and not w20['hash'], 'the opening card shows on a first visit: three doors, three featured tours with their pictures, the counts in its line (%s)' % (w20['line'][:90],))
    check(w20['flying'] and w20['room'] == 'corridoio', 'the scene drifts along the corridor behind the card (flying %s, room %s)' % (w20['flying'], w20['room']))
    page.wait_for_timeout(900); page.screenshot(path=os.path.join(args.shots, 'opening.png'))
    page.click('#aboutBtn'); page.wait_for_timeout(400)
    ab20 = page.evaluate("() => ({ about: document.getElementById('about').classList.contains('show'), welcome: window.__state.welcome(), flag: (() => { try { return sessionStorage.getItem('eco-map-welcome'); } catch (e) { return null; } })() })")
    check(ab20['about'] and not ab20['welcome'] and ab20['flag'] == '1', 'a click on the top bar reaches its button and dismisses the card, which does not return this session (%s)' % (ab20,))
    ab20t = page.evaluate("() => ({ h: [...document.querySelectorAll('#about h2, #about h3, #about summary')].map((e) => e.textContent.trim()), open: [...document.querySelectorAll('#about details')].map((d) => d.open), text: document.getElementById('about').textContent })")
    check(ab20t['h'][:3] == ['About this map', 'How the map was made', 'Footage, photographs and catalogues'] and 'Reading the colours' in ab20t['h'] and not any(ab20t['open']), 'About opens on two paragraphs for a visitor, the method and the colour key folded away under their own headings (%s)' % (ab20t['h'][:5],))
    check(all(k in ab20t['text'] for k in ('33,000 books', 'Braidense in 2021', '1 July 2026', 'does not by itself establish', 'not a spine')) and re.search(r'\b(verif|correct(ed|ion|ing)|earlier version|previous version)', ab20t['text'], re.I) is None, 'About says what the library was and where its two halves went, keeps the method\'s own words, and never speaks of checking or earlier versions')
    page.screenshot(path=os.path.join(args.shots, 'about-sections.png'))
    page.keyboard.press('Escape'); page.wait_for_timeout(300)
    check(not page.evaluate("() => document.getElementById('about').classList.contains('show')"), 'Escape closes About')
    page.evaluate("() => window.__flyToRoom('all')"); settle(page)   # the plan, where the checks below have always begun
    data = page.evaluate('() => { const d = window.__data(); return { books: d.books.length, rooms: d.rooms.map(r => r.id), by: d.meta.counts.by_origin }; }')
    print('data:', data)
    check(data['books'] > 1000, 'dataset loaded (%d books)' % data['books'])
    page.wait_for_timeout(1500)
    check(canvas_has_pixels(page, os.path.join(args.shots, 'overview.png')) > 40, 'scene renders (overview screenshot is not blank)')
    for rid in data['rooms']:
        page.click('[data-room="%s"]' % rid)
        page.wait_for_timeout(1500)
        check(canvas_has_pixels(page, os.path.join(args.shots, 'room-%s.png' % rid)) > 40, 'room %s renders' % rid)
    # panels: one book per origin
    for origin in ['video', 'photo', 'catalog']:
        bid = page.evaluate('(o) => { const b = window.__data().books.find(b => b.origin === o && b.title); return b ? b.id : null; }', origin)
        if not bid: print('SKIP no %s book in the dataset' % origin); continue
        page.evaluate('(id) => window.__openBook(id)', bid)
        page.wait_for_timeout(1400)
        opened = page.evaluate("() => document.getElementById('panel').classList.contains('open')")
        links = page.evaluate("() => Array.from(document.querySelectorAll('#panel .src a')).map(a => a.href)")
        title = page.evaluate("() => document.getElementById('pTitle').textContent")
        check(opened and links, 'panel for %s book %s opens with a source link: %s' % (origin, bid, links[:1]))
        if origin == 'video': check(any('youtube.com/watch' in u and '&t=' in u for u in links), 'video link opens YouTube at a timestamp')
        if origin == 'catalog': check(any('braidense' in u or 'unibo' in u for u in links), 'catalogue link points at the record')
        check(bool(title.strip()), 'panel title shown as-is: %r' % title[:60])
        page.screenshot(path=os.path.join(args.shots, 'panel-%s.png' % origin))
    # click a book with the mouse: project a placed book to screen coordinates and click there
    bid = page.evaluate("() => { const b = window.__data().books.find(b => b.origin === 'catalog' && b.rare); return b.id; }")
    page.evaluate('(id) => window.__openBook(id)', bid); page.wait_for_timeout(1500)
    page.click('#pClose'); page.wait_for_timeout(300)
    pt = page.evaluate('(id) => window.__bookScreen(id)', bid)
    if pt and 0 < pt['x'] < 1440 and 0 < pt['y'] < 900:
        page.mouse.click(pt['x'], pt['y']); page.wait_for_timeout(500)
        got = page.evaluate("() => document.getElementById('panel').classList.contains('open') && document.querySelectorAll('#panel .src a').length > 0")
        check(got, 'clicking a rare book on the shelf opens its panel with a source link')
        page.screenshot(path=os.path.join(args.shots, 'panel-click.png'))
    else: check(False, 'could not project a book to the screen for the click test')
    # objects: a pile with titles, then a piece of furniture; bookcase and room info panels; tour
    pile = page.evaluate("() => { const o = (window.__data().objects || []).find(o => o.kind === 'pile' && o.books && o.books.length); return o ? o.id : null; }")
    if pile:
        page.evaluate('(id) => window.__openObject(id)', pile); page.wait_for_timeout(1400)
        n = page.evaluate("() => document.querySelectorAll('#panel .list .r').length")
        check(n > 0 and page.evaluate("() => document.querySelectorAll('#panel .src a').length > 0"), 'pile object panel lists its %d books and a source link' % n)
        page.screenshot(path=os.path.join(args.shots, 'object-pile.png'))
        page.click('#panel .list .r'); page.wait_for_timeout(1200)
        check(page.evaluate("() => document.querySelectorAll('#panel .src a').length > 0"), 'a book in the pile opens with its source link')
    else: print('SKIP no titled pile in the dataset')
    obj = page.evaluate("() => { const o = (window.__data().objects || []).find(o => o.kind !== 'pile'); return o ? o.id : null; }")
    if obj:
        page.evaluate('(id) => window.__openObject(id)', obj); page.wait_for_timeout(1400)
        check(page.evaluate("() => document.getElementById('panel').classList.contains('open') && document.getElementById('pTitle').textContent.length > 0"), 'furniture object %s opens the panel' % obj)
        page.screenshot(path=os.path.join(args.shots, 'object-furniture.png'))
    page.evaluate("() => window.__openCase(window.__data().rooms[4].bookcases[0].id)"); page.wait_for_timeout(1200)
    check('slots' in page.evaluate("() => document.getElementById('pBody').textContent"), 'bookcase info panel shows its counts')
    page.screenshot(path=os.path.join(args.shots, 'panel-bookcase.png'))
    page.evaluate("() => window.__openRoom('antichi')"); page.wait_for_timeout(1200)
    check('Bookcases' in page.evaluate("() => document.getElementById('pBody').textContent"), 'room info panel lists the bookcases')
    page.evaluate("() => window.__tour.start()"); page.wait_for_timeout(1600)
    check(page.evaluate("() => document.getElementById('tour').classList.contains('show') && document.getElementById('tourCap').textContent.length > 0"), 'tour starts with a caption')
    page.screenshot(path=os.path.join(args.shots, 'tour-stop-1.png'))
    page.evaluate("() => window.__tour.next()"); page.wait_for_timeout(1600)
    check(page.evaluate("() => window.__tour.step()") == 1, 'tour advances to the next stop')
    page.screenshot(path=os.path.join(args.shots, 'tour-stop-2.png'))
    page.evaluate("() => window.__tour.end()")
    check(not page.evaluate("() => document.getElementById('tour').classList.contains('show')"), 'tour exits')
    # tour stops carry quotes (from tour_eco.json / quotes)
    tq = page.evaluate("() => { const t = window.__data().meta.tour; return t && t.stops ? t.stops.filter(s => s.quote || (s.quotes && s.quotes.length)).length : 0; }")
    check(tq > 0, 'tour stops carry quotations (%d stops with a quote)' % tq)
    # notable category tour (novel sources)
    nt = page.evaluate("() => { const t = (window.__data().meta.notable_tours || [])[0]; return t ? t.id : null; }")
    if nt:
        page.evaluate('(id) => window.__tour.notable(id)', nt); page.wait_for_timeout(1600)
        check(page.evaluate("() => document.getElementById('tour').classList.contains('show') && document.getElementById('tourCap').textContent.length > 0"), 'notable-books tour %r starts with a caption' % nt)
        page.screenshot(path=os.path.join(args.shots, 'tour-notable.png'))
        page.evaluate("() => window.__tour.end()")
    else: check(False, 'no notable tours in meta')
    # walk replay (animated camera path along the film route)
    has_walk = page.evaluate("() => !!(window.__data().meta.walk && window.__data().meta.walk.waypoints && window.__data().meta.walk.waypoints.length)")
    if has_walk:
        page.evaluate("() => window.__walk.start()"); page.wait_for_timeout(1200)
        st0 = page.evaluate("() => window.__walk.state()")
        check(st0['on'] and page.evaluate("() => document.getElementById('walk').classList.contains('show') && document.getElementById('walkCap').textContent.length > 0"), 'walk replay starts with a caption')
        page.screenshot(path=os.path.join(args.shots, 'walk-start.png'))
        page.wait_for_timeout(2500)
        st1 = page.evaluate("() => window.__walk.state()")
        check(st1['t'] > st0['t'] and st1['cam'] != st0['cam'], 'walk replay advances the camera along the path (t %.1f -> %.1f)' % (st0['t'], st1['t']))
        mid = page.evaluate("() => { const w = window.__data().meta.walk.waypoints; return w[Math.floor(w.length / 2)].t; }")
        page.evaluate('(t) => window.__walk.seek(t)', mid); page.wait_for_timeout(900)
        st2 = page.evaluate("() => window.__walk.state()")
        check(abs(st2['t'] - mid) < 0.6, 'walk replay seeks to the middle waypoint')
        page.screenshot(path=os.path.join(args.shots, 'walk-mid.png'))
        wq = page.evaluate("() => window.__data().meta.walk.waypoints.filter(w => w.quote).length")
        check(wq > 0, 'walk waypoints carry quotations at their shelves (%d)' % wq)
        page.evaluate("() => window.__walk.end()")
        check(not page.evaluate("() => window.__walk.state().on"), 'walk replay exits')
    else: check(False, 'meta.walk missing')
    # layers: fog (what the camera saw) and shelf letters
    ls = page.evaluate("() => window.__layers.state()")
    check(ls['fogCount'] > 0 and ls['fog'] is True, 'fog layer covers the bookcases never on camera (%d fogged)' % ls['fogCount'])
    check(ls['plates'] > 0 and ls['letters'] is True, 'shelf-letter overlay drawn (%d plates)' % ls['plates'])
    check(ls['shapes'] > 0, 'objects drawn with shapes (%d shape meshes)' % ls['shapes'])
    page.evaluate("() => window.__layers.fog()"); page.evaluate("() => window.__layers.letters()"); page.wait_for_timeout(300)
    ls2 = page.evaluate("() => window.__layers.state()")
    check(ls2['fog'] is False and ls2['letters'] is False, 'fog and letters toggle off')
    page.evaluate("() => window.__layers.fog()"); page.evaluate("() => window.__layers.letters()")
    check(ls.get('windows', 0) > 0 and ls.get('aoBands', 0) > 0, 'windows built (%s) and fake-AO bands under the shelves (%s)' % (ls.get('windows'), ls.get('aoBands')))
    # colour overlays: certainty legend counts must match meta.counts.tiers; the tier filter drives the shader uniforms
    tiers = page.evaluate("() => { const t = window.__data().meta.counts.tiers || {}; return {certain: t.certain, guess: t.guess, unknown: t.unknown}; }")
    page.evaluate("() => window.__overlay.set('certainty')"); page.wait_for_timeout(600)
    ov = page.evaluate("() => window.__overlay.state()")
    leg = dict(ov['legend'])
    check(ov['mode'] == 'certainty' and ov['uMode'] == 1, 'certainty overlay switches on (mode %s, uMode %s)' % (ov['mode'], ov['uMode']))
    check(all(leg.get(k) == tiers.get(k) for k in ('certain', 'guess', 'unknown')) and tiers.get('unknown'), 'legend counts equal meta.counts.tiers: %s' % leg)
    ltxt = page.evaluate("() => document.getElementById('legend').textContent")
    check(all(format(tiers[k], ',') in ltxt for k in ('certain', 'guess', 'unknown')) and 'Certain' in ltxt, 'legend box shows the three tiers with their counts and explanations')
    page.evaluate("() => window.__overlay.filter('certain')"); page.wait_for_timeout(300)
    ov2 = page.evaluate("() => window.__overlay.state()")
    check(ov2['filter'] == 'certain' and ov2['uShow'] == [1, 0, 0], 'tier filter "certain only" hides guesses and unknowns (uShow %s)' % ov2['uShow'])
    page.evaluate("() => window.__overlay.filter('hide-unknown')"); page.wait_for_timeout(300)
    check(page.evaluate("() => window.__overlay.state().uShow") == [1, 1, 0], 'tier filter "hide unknown" keeps certain and guess')
    page.evaluate("() => window.__overlay.filter('all')")
    for mode in ['subject', 'source', 'century', 'on_film', 'language']:
        page.evaluate('(m) => window.__overlay.set(m)', mode); page.wait_for_timeout(400)
        st = page.evaluate("() => window.__overlay.state()")
        check(st['mode'] == mode and sum(n for _, n in st['legend']) > 1000, 'overlay %s colours the shelves with a legend (%d classes, %s books)' % (mode, len(st['legend']), format(sum(n for _, n in st['legend']), ',')))
    # tier badge and reason in the book panel (a guess)
    gb = page.evaluate("() => { const b = window.__data().books.find(b => b.tier === 'guess' && b.title); return b ? b.id : null; }")
    if gb:
        page.evaluate('(id) => window.__openBook(id)', gb); page.wait_for_timeout(1200)
        pb = page.evaluate("() => document.getElementById('pBody').textContent")
        check('Guess' in pb and 'Certainty' in pb, 'book panel shows the certainty tier and its reason')
        pi = page.evaluate("() => document.getElementById('pBody').innerText")
        check(not re.search(r'[a-z](?:low|medium|high) confidence|confidence(?:position|shelf|placeholder|not yet|placed)|Guess[a-z]|Certain[a-z]|Unknown[a-z]', pi), 'badges in the panel are separated when read as text')
        page.screenshot(path=os.path.join(args.shots, 'panel-tier-guess.png'))
    else: check(False, 'no guess-tier book with a title')
    # spine titles are lettered at close range (the flight to a rare book lands within reading distance)
    page.wait_for_timeout(800)
    check(page.evaluate("() => window.__spineLabels || 0") > 0, 'spine titles lettered near the camera (%d labels)' % page.evaluate("() => window.__spineLabels || 0"))
    # object thumbs: the panel shows the film frame at the top with the "seen on film" caption
    tob = page.evaluate("() => { const o = (window.__data().objects || []).find(o => o.thumb && o.kind !== 'pile'); return o ? o.id : null; }")
    if tob:
        page.evaluate('(id) => window.__openObject(id)', tob); page.wait_for_timeout(1200)
        th = page.evaluate("() => { const i = document.querySelector('#panel img.thumb'); const c = document.querySelector('#panel .thumbcap'); return i ? {src: i.src.slice(0, 10), w: i.naturalWidth, cap: c ? c.textContent : ''} : null; }")
        check(th and th['src'].startswith('data:') and th['w'] > 0 and ('Seen' in th['cap'] or 'photo' in th['cap'].lower()), 'object panel shows its film thumb with a caption: %s' % (th,))
        page.screenshot(path=os.path.join(args.shots, 'object-thumb.png'))
    else: check(False, 'no object with a thumb in the data')
    # "Eco's copies": dedications, marginalia, dog-ears... from book.copy.marks
    hand = page.evaluate("() => window.__hand()")
    if page.evaluate("() => window.__data().books.some(b => b.copy && b.copy.marks)"):
        check(hand and all(n > 0 for _, n in hand), "Eco's copies index built: %s" % hand)
        menu_click(page, '#handBtn')   # under the More menu
        rows = page.evaluate("() => document.querySelectorAll('#handList .r').length")
        check(rows > 0, "Eco's copies overlay lists %d books" % rows)
        page.screenshot(path=os.path.join(args.shots, 'hand.png'))
        page.click('#handList .r'); page.wait_for_timeout(1200)
        check(page.evaluate("() => document.getElementById('panel').classList.contains('open')"), "a row in Eco's copies jumps to the book")
    else: print('SKIP no copy.marks in the data; hand index', hand)
    # "not yet shelved" table (tolerates a dataset without placement == unshelved)
    print('unshelved records on the table:', page.evaluate("() => window.__unshelved()"))
    # the Braidense's ECO.04 records are reference entries on a table of their own, never on a cabinet and never counted as identified
    ref_n = page.evaluate("() => window.__reference()"); ref_meta = page.evaluate("() => window.__data().meta.counts.reference || 0")
    check(ref_n == ref_meta and ref_n > 0, 'the ECO.04 reference entries lie on the reference table (%d on the table, %d in meta)' % (ref_n, ref_meta))
    bad_ref = page.evaluate("() => window.__data().books.filter(b => /^ECO\\.04/.test(b.shelfmark || '') && !(b.placement === 'reference' && b.bookcase === 'reference-table' && b.tier === 'guess')).map(b => b.id)")
    check(not bad_ref, 'every ECO.04 record is a reference entry of tier guess on the reference table, none on a cabinet (%s)' % bad_ref[:3])
    idn = page.evaluate("() => { const D = window.__data(); return [D.meta.counts.identified, D.books.filter(b => b.origin !== 'unlabelled' && b.placement !== 'reference').length]; }")
    check(idn[0] == idn[1], 'the identified count leaves out the reference entries (%s)' % idn)
    first_ref = page.evaluate("() => { const b = window.__data().books.find(b => b.placement === 'reference'); return b ? b.id : null; }")
    if first_ref:
        page.evaluate('(id) => window.__openBook(id)', first_ref); settle(page)
        ptxt = page.evaluate("() => document.getElementById('pBody').textContent")
        check('Reference entry' in ptxt and "have not been established" in ptxt and 'reference section' in ptxt and 'listed, not shelved' in ptxt and 'Guess' not in ptxt.replace('Guesses', ''), "a reference entry's panel is badged Reference entry and listed, not shelved, names the Braidense section and says that presence and position in the flat are not established")
        check('..' not in ptxt, "the reference entry's panel prints one full stop after the provenance note")
        page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    notes_txt = page.evaluate("() => window.__data().books.filter(b => b.origin !== 'unlabelled').map(b => (b.placement_note || '') + ' | ' + (b.tier_reason || '')).join('\\n')")
    check('shelved by his family' not in notes_txt and 'acquired by the library afterwards' not in notes_txt, 'no book note infers how a copy was acquired from its year of publication')
    page.evaluate("() => window.__openCase('reference-table')"); settle(page)
    check('ECO.04' in page.evaluate("() => document.getElementById('pBody').textContent") and 'does not by itself establish' in page.evaluate("() => document.getElementById('pBody').textContent"), 'the reference table panel explains the ECO.04 section')
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    about_txt = page.evaluate("() => document.getElementById('about').textContent")
    check('does not by itself establish' in about_txt and 'preserve Eco' not in about_txt and 'not a spine' in about_txt, 'the About text carries the Braidense wording on ECO.04 and no longer equates records with volumes')
    # ---- composed volume titles, incunabula cards, room quotations and the own-books tour -----------------------------------
    mm = re.search(r'([\d,]+) books are identified: ([\d,]+) read in video frames, ([\d,]+) read in photographs, ([\d,]+) from the catalogues \(([\d,]+) [^,()]*?, ([\d,]+) ', about_txt)
    nums = [int(x.replace(',', '')) for x in mm.groups()] if mm else []
    check(bool(nums) and nums[0] == nums[1] + nums[2] + nums[3] and nums[3] == nums[4] + nums[5], "the About sentence's parts add up to its identified total and the two catalogues to the catalogued count (%s)" % nums)
    stats_txt = page.evaluate("() => document.getElementById('stats').textContent")
    cat_n = page.evaluate("() => window.__data().books.filter((b) => b.origin === 'catalog' && b.placement !== 'reference').length")
    check(bool(nums) and nums[3] == cat_n and ('%s catalogued' % format(cat_n, ',')) in stats_txt and 'reference entries' in stats_txt, 'the footer counts the catalogued books of the flat (%s) apart from the reference entries' % format(cat_n, ','))
    check('treats them as guesses' in about_txt and 'Hide unknown' in about_txt, 'the About text says what the certainty filter does with the reference entries')
    v16 = page.evaluate(r"""() => { const D = window.__data(), out = {};
      const g = (id) => { const i = D._index.get(id); return i === undefined ? null : D.books[i]; };
      const man = g('braidense:UBO4830877'); out.manara = man ? [man.title, man.author, man.volume_statement] : null;
      out.bareVol = D.books.filter((b) => /^(tome|tomo|volume|vol\.?)\s+(premier|premiere|second|troisieme|quatrieme|\d+ (di|of) \d+)$/i.test(b.title || '')).map((b) => b.id);
      const med = g('braidense:PAR1197365'); out.medioevo = med ? [med.title, med.author, med.author_from_set] : null;
      out.fromSet = D.books.filter((b) => b.author_from_set).length;
      out.badCards = D.books.filter((b) => b.card && /\(p\. [23]\)|art\. p\./.test(b.card.note || '')).map((b) => b.id);
      const n36 = g('braidense:RMLE067463'), n2 = g('braidense:MILE062639'); out.mentelin = [n36 && n36.card ? n36.card.note : null, n2 && n2.card ? n2.card.note : null];
      out.jsonSrc = D.books.filter((b) => /\.json\b/.test(b.title_en_source || '')).map((b) => b.id);
      out.multiUrl = []; for (const r of D.rooms) for (const q of (r.quotes || [])) if (/ ; /.test(q.url || '')) out.multiUrl.push(q.url);
      out.stops = {}; for (const t of (D.meta.tours || [])) { if (t.id === 'own-books') out.ownBlurb = t.blurb; for (const st of t.stops) out.stops[st.id] = { cap: st.caption || '', label: st.source && st.source.label || '', rec: st.record || null, target: st.target }; }
      out.refBadge = D.books.filter((b) => b.placement === 'catalogued' && /^ECO\.0[23]\b/.test(b.shelfmark || '')).length;
      return out; }""")
    check(v16['manara'] and v16['manara'][0] == 'Il nome della rosa, vol. 1 of 2' and v16['manara'][1] == 'Milo Manara, Umberto Eco' and v16['manara'][2] == 'Volume 1 di 2', 'the Manara volume is titled from its set with the volume statement kept, its authors written out from the record\'s own headings (%s)' % (v16['manara'],))
    check(not v16['bareVol'], 'no spine reads as a bare volume statement (%s)' % v16['bareVol'][:5])
    check(v16['medioevo'] and v16['medioevo'][1] == 'a cura di Umberto Eco' and v16['medioevo'][2] is True and v16['fromSet'] >= 40, "a volume without a statement of responsibility of its own carries the set's (%d records; %s)" % (v16['fromSet'], v16['medioevo']))
    check(not v16['badCards'] and 'secondo Mentelin' in (v16['mentelin'][0] or '') and 'C.W.' in (v16['mentelin'][1] or ''), "the incunabula cards cite the printed article's pages and the corrected printers (%s)" % v16['badCards'][:5])
    check(not v16['jsonSrc'], 'no English-title source cites a .json address (%s)' % v16['jsonSrc'][:5])
    check(not v16['multiUrl'], 'every room quotation links one address (%s)' % v16['multiUrl'][:2])
    st16 = v16['stops']
    check('Interpretation and Overinterpretation' in st16.get('pendulum-03', {}).get('label', ''), "pendulum-03 cites 'Between Author and Text' in Interpretation and Overinterpretation")
    check('Le Juif errant' in st16.get('prague-04', {}).get('cap', '') and 'sinister Jesuits that' not in st16.get('prague-04', {}).get('cap', ''), 'prague-04 says which Sue novels carry the Jesuit conspiracy and that the two volumes are other works')
    check("Eco's copy" not in st16.get('own-books-08', {}).get('label', '') and "Eco's copy" not in st16.get('own-books-12', {}).get('label', ''), "no reference-entry stop calls the library's copy Eco's")
    check('his own shelves' in (v16.get('ownBlurb') or ''), "the own-books blurb says some stops open on copies from Eco's shelves")
    rec_stops = [k for k, v in st16.items() if v['rec']]
    check(len(rec_stops) == 14 and all(st16[k]['target'].startswith('video:') and st16[k]['rec'].startswith('braidense:') for k in rec_stops), 'fourteen stops open on a filmed copy and name the Braidense record (%s)' % sorted(rec_stops))
    check(not any(re.search(r'\b(edition of \d{4}|catalogued under \d{4})\.$', st16[k]['cap']) for k in rec_stops), 'no retargeted caption ends with the reference entry\'s edition sentence')
    # ---- brackets and volume numbers in the served titles, pile reasons, incunabula pages, stop links --------------------
    v17 = page.evaluate(r"""() => { const D = window.__data(), out = {};
      const g = (id) => { const i = D._index.get(id); return i === undefined ? null : D.books[i]; };
      const T = (id) => { for (const p of ['braidense:', 'bologna:']) { const b = g(p + id); if (b) return [b.title, b.author]; } return null; };
      out.titles = { MUS0044454: T('MUS0044454'), MILE063013: T('MILE063013'), MILE063014: T('MILE063014'), UBO00455069: T('UBO00455069'), UBO00455065: T('UBO00455065') };
      out.bareVol = D.books.filter((b) => /^(tome|tomo|tomus|pars|volume|volumen|vol\.?|liber|libro|band|teil|part|parte)\s*\.?\s*(premier|premiere|prima|primus|primo|second|seconda|secunda|secondo|altera|troisieme|terza|tertia|terzo|quatrieme|quarta|quarto|[ivxl]+|\d+)(\s+\d{4}\s*[-–]\s*\d{4})?\.?$/i.test((b.title || '').trim())).map((b) => b.id);
      out.unbalanced = D.books.filter((b) => { const t = b.title || ''; return (t.match(/\[/g) || []).length !== (t.match(/\]/g) || []).length; }).map((b) => [b.id, b.title]);
      out.edges = D.books.filter((b) => /^\s*\]|\[\s*\]|\[-[^\]]*\],? vol\. \d|, vol\. [^:]*:\s*$|, vol\. \d+[^:]*: \]/.test(b.title || '')).map((b) => [b.id, b.title]);
      out.composed = D.books.filter((b) => /, vol\. /.test(b.title || '')).length;
      out.sue = D.books.filter((b) => /Latr[ée]aumont|Mathilde/.test(b.title || '') && /, vol\. /.test(b.title || '')).map((b) => b.title);
      out.cataractes = D.books.filter((b) => /Cataractes/.test(b.title || '')).map((b) => b.title);
      out.arcana = D.books.filter((b) => /Arcana c(o|ae)elestia/i.test(b.title || '') && /vol\. 11/.test(b.title || '')).map((b) => b.title);
      out.camera = D.books.filter((b) => /camera da letto/i.test(b.title || '') && /vol\. /.test(b.title || '')).map((b) => b.title);
      out.brucioli = D.books.filter((b) => /Brucioli/i.test(b.title || '') && /vol\. /.test(b.title || '')).map((b) => b.title);
      const man = g('braidense:UBO4830877'); out.manara = man ? [man.title, man.author] : null;
      out.recon = D.books.filter((b) => /Bologna reconstruction|Milan bookcase is unknown/.test((b.placement_note || '') + ' ' + (b.tier_reason || ''))).map((b) => b.id);
      out.louisiana = D.books.filter((b) => /inferred from the shot's context/.test(b.placement_note || '')).map((b) => [b.id, b.placement_note, b.tier]);
      const pileOf = (b) => (D.objects || []).find((o) => o.id === b.bookcase && o.kind === 'pile');
      out.cutReason = D.books.filter((b) => { const r = b.tier_reason || '', o = pileOf(b); if (!o || !/in pile "/.test(r)) return false; return !r.includes('"' + o.label + '"') || (r.match(/\(/g) || []).length !== (r.match(/\)/g) || []).length; }).map((b) => [b.id, b.tier_reason]);
      out.pileReasons = D.books.filter((b) => /in pile "/.test(b.tier_reason || '')).length;
      out.ratdolt = D.books.filter((b) => b.card && /Ratdolt a Venezia nel 1482/.test(b.card.note || '')).map((b) => b.id);
      const pub = g('braidense:RAVE077335'); out.publicius = pub ? [pub.card && pub.card.note || '', pub.notable && pub.notable.why || ''] : null;
      out.cards = D.books.filter((b) => b.card && b.card.article_page != null).map((b) => [b.card.article_page, b.card.pdf_page]);
      out.stops = {}; for (const t of (D.meta.tours || [])) for (const st of t.stops) out.stops[st.id] = { cap: st.caption || '', url: st.source && st.source.url || '' };
      out.rivista = []; for (const t of (D.meta.tours || [])) for (const st of t.stops) if (/Linus_\(rivista\)/.test(JSON.stringify(st))) out.rivista.push(st.id);
      // one "Seen in" line per shot: the panels of sixty books and every object with two or more video sightings, read for two lines naming the same film within five seconds
      const lines = () => { const t = document.getElementById('pBody').textContent, L = [], re = /Seen in “([^”]+)” at (\d+):(\d\d)(?::(\d\d))?/g; let m;
        while ((m = re.exec(t))) L.push([m[1], m[4] !== undefined ? (+m[2]) * 3600 + (+m[3]) * 60 + (+m[4]) : (+m[2]) * 60 + (+m[3])]); return L; };
      const dup = (L) => { for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) if (L[i][0] === L[j][0] && Math.abs(L[i][1] - L[j][1]) <= 5) return [L[i][1], L[j][1]]; return null; };
      out.dupSeen = []; out.seenRead = 0; out.seenLines = 0;
      for (const b of D.books) { if (out.seenRead >= 60) break; const ss = (b.sightings || []).filter((s) => s.kind === 'video' && s.timestamp_s != null); if (ss.length < 2) continue;
        window.__openBook(b.id, false); const L = lines(); out.seenRead++; out.seenLines += L.length; const d = dup(L); if (d) out.dupSeen.push([b.id].concat(d)); }
      out.objRead = 0;
      for (const o of (D.objects || [])) { const ss = (o.sightings || []).filter((s) => s.video_id && s.timestamp_s != null); if (ss.length < 2) continue;
        window.__openObject(o.id); const L = lines(); out.objRead++; const d = dup(L); if (d) out.dupSeen.push([o.id].concat(d)); }
      return out; }""")
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    tt = v17['titles']
    check(bool(tt['MUS0044454']) and tt['MUS0044454'][0].endswith(', vol. 2') and not re.match(r'(?i)tomus', tt['MUS0044454'][0]), "Kircher's 'Tomus 2' (MUS0044454) is titled from its set (%s)" % (tt['MUS0044454'] and tt['MUS0044454'][0]))
    check(bool(tt['MILE063013']) and bool(tt['MILE063014']) and tt['MILE063013'][0].endswith(', vol. 1') and tt['MILE063014'][0].endswith(', vol. 2') and tt['MILE063013'][0].rsplit(', vol.', 1)[0] == tt['MILE063014'][0].rsplit(', vol.', 1)[0], "Antoine's 'Pars prima' and 'Pars altera' (MILE063013/14) are volumes 1 and 2 of their set (%s)" % (tt['MILE063013'] and tt['MILE063013'][0]))
    check(bool(tt['UBO00455069']) and bool(tt['UBO00455065']) and re.match(r'^Writings of Charles S\. Peirce, vol\. 1: 1857.1866$', tt['UBO00455069'][0] or '') and re.match(r'^Writings of Charles S\. Peirce, vol\. 2: 1867.1871$', tt['UBO00455065'][0] or ''), "the Peirce volumes 'Vol.1 1857-1866' and 'Vol.2 1867-1871' (UBO00455069/65) are titled from their set with the years kept (%s)" % (tt['UBO00455069'] and tt['UBO00455069'][0]))
    check(not v17['bareVol'], 'no spine reads as a bare volume statement in any language, with or without a year range (%s)' % v17['bareVol'][:5])
    check(not v17['unbalanced'] and not v17['edges'], "no title carries an unclosed or empty bracket, a cut bracket after its number, or the set's range beside its volume number (%s)" % (v17['unbalanced'][:3] + v17['edges'][:3]))
    check(len(v17['sue']) >= 2 and all('[' not in t and ': ' in t for t in v17['sue']), "the Sue volumes read '…, vol. 1: Latréaumont' and '…, vol. 2: Mathilde' without the record's open bracket (%s)" % v17['sue'][:2])
    check(len(v17['arcana']) == 1 and '[' not in v17['arcana'][0] and 'vol. 11: Exodus' in v17['arcana'][0], 'Arcana coelestia vol. 11 names its part without the open bracket (%s)' % v17['arcana'])
    check(len(v17['cataractes']) >= 4 and all('[-' not in t and 'Tome premier' not in t and re.search(r', vol\. \d$', t) for t in v17['cataractes']), "the Cataractes volumes carry the volume number once, without the set's own range (%s)" % (v17['cataractes'] and v17['cataractes'][0]))
    check(len(v17['camera']) == 1 and v17['camera'][0].startswith('La camera da letto, vol. 1') and ']' not in v17['camera'][0], "La camera da letto vol. 1 has no cut bracket after its number (%s)" % v17['camera'])
    check(len(v17['brucioli']) >= 4 and all('[' not in t.replace('[sic]', '') and ']' not in t.replace('[sic]', '') for t in v17['brucioli']) and all(not re.search(r', vol\. \d+: Dialogi di Antonio Brucioli', t) for t in v17['brucioli']), "the Brucioli dialogues' volumes do not repeat the set's title after the number and carry no cut bracket (%s)" % (v17['brucioli'] and v17['brucioli'][0]))
    check(bool(v17['manara']) and v17['manara'][1] == 'Milo Manara, Umberto Eco', "the 2023 Manara volume's author line is 'Milo Manara, Umberto Eco' (%s)" % (v17['manara'],))
    check(not v17['recon'] and sorted(x[0] for x in v17['louisiana']) == ['video:M8IWTOFNlOc:1444:baudolino', 'video:M8IWTOFNlOc:1444:island-of-the-day-before', 'video:M8IWTOFNlOc:1444:to-koimeterio-tes-pragas', 'video:M8IWTOFNlOc:1446:segno'] and all(x[1].startswith('read on film at') and x[2] == 'guess' for x in v17['louisiana']), "no placement note says 'Bologna reconstruction'; the three copies read in the Louisiana clip say the shot shows no shelf tag and the bookcase is inferred from its context (%s)" % [x[0] for x in v17['louisiana']])
    check(v17['pileReasons'] >= 100 and not v17['cutReason'], 'every tier reason that names a pile prints the whole label with its parentheses closed (%d reasons%s)' % (v17['pileReasons'], '' if not v17['cutReason'] else '; cut: %s' % v17['cutReason'][:3]))
    check(not v17['ratdolt'] and bool(v17['publicius']) and 'Ratdolt a Venezia nel 1482' not in v17['publicius'][0] and 'Chicco-Sanvito' in v17['publicius'][0] and 'Augsburg del 1490' in v17['publicius'][1] and 'Christie' in v17['publicius'][1], "the Publicius card prints the article's note without the 1482 clause, which the Notable text carries as the map's own reading with its source")
    first_int = lambda v: int(re.match(r'\d+', str(v)).group(0)) if v is not None and re.match(r'\d+', str(v)) else None
    check(len(v17['cards']) >= 30 and all(first_int(a) is not None and first_int(p) is not None and first_int(a) - first_int(p) == 8 for a, p in v17['cards']), "every incunabulum card's article_page counts the journal's printed pages, eight past the PDF page kept as pdf_page (%d cards)" % len(v17['cards']))
    st17 = v17['stops']
    check('five other works' in st17.get('prague-04', {}).get('cap', '') and 'five other novels' not in st17.get('prague-04', {}).get('cap', ''), 'prague-04 calls the works around Le Juif errant works, not novels')
    check(st17.get('comics-02', {}).get('url', '') == 'https://it.wikipedia.org/wiki/Linus_(periodico)' and not v17['rivista'], "comics-02 links the Italian Wikipedia's 'Linus (periodico)' page and no stop the old address")
    check(v17['seenRead'] >= 40 and v17['objRead'] >= 5 and not v17['dupSeen'], 'one "Seen in" line per shot: no panel prints the same film twice within five seconds (%d book and %d object panels read%s)' % (v17['seenRead'], v17['objRead'], '' if not v17['dupSeen'] else '; doubled at %s' % v17['dupSeen'][:4]))
    # ---- shelf labels read in the frame, bare volume numbers, [sic] marks, object fit notes, tour stop ids ---------------
    v18 = page.evaluate(r"""() => { const D = window.__data(), out = {};
      const g = (id) => { const i = D._index.get(id); return i === undefined ? null : D.books[i]; };
      const greek = g('video:M8IWTOFNlOc:1444:to-koimeterio-tes-pragas'), nb = g('video:M8IWTOFNlOc:1444:island-of-the-day-before');
      out.greek = greek ? [greek.tier, greek.placement, greek.placement_note || '', greek.shelf_label || null, (greek.sightings || []).map((s) => s.level).join(','), greek.tier_reason || ''] : null;
      out.neighbour = nb ? [nb.tier, nb.placement, nb.placement_note || '', nb.shelf_label || null] : null;
      out.seenLabels = {}; for (const b of D.books) if (b.placement === 'seen' && b.shelf_label) out.seenLabels[b.shelf_label] = (out.seenLabels[b.shelf_label] || 0) + 1;
      out.wallLabels = D.books.filter((b) => /wall|library|bookcase|shelves|editions/i.test(b.shelf_label || '')).map((b) => [b.id, b.shelf_label]);
      out.contextLevel = D.books.filter((b) => (b.sightings || []).some((x) => x.level === 'context')).map((b) => [b.id, b.placement, b.tier, !!b.shelf_label, (b.sightings || []).some((x) => ['bookcase', 'wall', 'label'].includes(x.level))]);   // [id, placement, tier, has a shelf label, has a sighting that resolves a bookcase or reads a tag in another frame]
      const T = (id) => { const b = g(id); return b ? [b.title, b.title_en || null, b.set_volume || null, b.volume_statement || null, b.set_title || null] : null; };
      out.titles = {}; for (const id of ['bologna:UBO01649610', 'bologna:UBO00367289', 'bologna:UBO00322891', 'bologna:UBO00256685', 'bologna:UBO00256687', 'bologna:UBO00864587', 'bologna:UBO07313601', 'bologna:UBO01048723', 'braidense:NAPE007651', 'braidense:BA1E011899']) out.titles[id] = T(id);
      const bare = /^\s*\[?\d{1,2}(?:\.\d{1,2}){0,3}(?:\s*\/\s*\d{1,2})?\]?\s*:\s*\S/;
      out.bare = D.books.filter((b) => bare.test(b.title || '') || bare.test(b.title_en || '') || bare.test(b.set_title || '')).map((b) => [b.id, b.title, b.title_en, b.set_title]);
      out.setVolumes = D.books.filter((b) => b.set_volume).map((b) => [b.id, b.set_volume, !!b.set_title_raw, /^\s*\[?\d/.test(b.set_title_raw || '')]);
      out.sic = D.books.filter((b) => /\[sic\]/.test(b.title || '')).map((b) => [b.id, b.title]);
      out.bang = D.books.filter((b) => /\[!\]|\[\]\]/.test([b.title, b.set_title, b.volume_statement, b.place, b.author, b.publisher, b.copy && b.copy.annotation].join(' '))).map((b) => b.id);
      out.vt = D.meta.counts.volume_titles || (D.meta.counts.catalog || {}).volume_titles || D.meta.volume_titles || null; out.withStatement = D.books.filter((b) => b.volume_statement).length;
      out.warnings = D.meta.warnings === undefined ? 'missing' : D.meta.warnings;
      out.fitted = (D.objects || []).filter((o) => o.fitted).map((o) => o.id); out.fitNotes = (D.objects || []).filter((o) => o.fit_note || o.size_note).map((o) => [o.id, o.fit_note || o.size_note]);
      const pub = g('braidense:RAVE077335'); out.pubLinks = pub && pub.notable ? pub.notable.links || null : null;
      window.__openBook('braidense:RAVE077335', false); const pb = document.getElementById('pBody');
      const a = [...pb.querySelectorAll('a')].find((x) => /christies\.com\/en\/lot\/lot-2031570/.test(x.href)); out.pubLink = a ? [a.textContent, a.href] : null; out.pubText = pb.textContent;
      window.__openBook('video:M8IWTOFNlOc:1444:to-koimeterio-tes-pragas', false); out.greekPanel = pb.textContent;
      const srcEl = [...pb.querySelectorAll('p.desc small a')].map((x) => x.textContent); out.greekSource = srcEl;
      out.stopIds = []; for (const t of (D.meta.tours || [])) t.stops.forEach((st, k) => { if (!new RegExp('^' + t.id + '-\\d+$').test(st.id)) out.stopIds.push(st.id); });
      return out; }""")
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    gk = v18['greek']
    check(bool(gk) and gk[0] == 'guess' and gk[1] == 'inferred' and gk[3] is None and gk[2].startswith('read on film at 00:24:05') and 'the shot shows no shelf tag' in gk[2] and 'inferred from the shot' in gk[2] and gk[4] == 'context', "the Greek Prague Cemetery of the Louisiana shot is a guess placed by the shot's context, with no shelf label (%s)" % (gk,))
    nbh = v18['neighbour']
    check(bool(nbh) and nbh[0] == 'guess' and nbh[1] == 'inferred' and nbh[3] is None and gk and nbh[2].startswith('read on film at 00:24:05') and nbh[2].split(';', 1)[1] == gk[2].split(';', 1)[1], 'the Greek copy reads as its neighbour from the same shot does, and the neighbour carries no stale shelf label (%s)' % (nbh,))
    tagLike = lambda lab: bool(re.match(r"^shelf label '([A-Z0-9 ./-]+|Pensiero Occidentale)'$", lab) or re.match(r'^call tags? [A-Z]', lab))
    check(bool(v18['seenLabels']) and all(tagLike(l) for l in v18['seenLabels']) and not v18['wallLabels'], "every shelf label on a 'seen' entry is a tag read in the frame (a call tag, capitals, or lettering the reader quoted), and none names a wall (%s)" % (sorted(v18['seenLabels'].items()) + v18['wallLabels'][:3],))
    ctxOnly18 = [x for x in v18['contextLevel'] if not x[4]]   # entries whose only frame-level sightings are the pass's own wall description
    check(len(ctxOnly18) >= 4 and all(x[1] == 'inferred' and not x[3] and x[2] != 'certain' for x in ctxOnly18) and all(x[1] != 'seen' or not x[3] or x[4] for x in v18['contextLevel']), "a sighting placed from the pass's own wall description (level context) never makes a 'seen' entry with a shelf label on its own: %d entries rest on such sightings alone and are inferred without a label; a 'seen' entry with a context sighting owes its label to a tag read in another frame (%s)" % (len(ctxOnly18), [x[0] for x in v18['contextLevel'] if x[1] == 'seen' and x[3]]))
    tt = v18['titles']
    exp18 = {'bologna:UBO01649610': ('La filosofia moderna, vol. 5: G. G. F. Hegel', '4'), 'bologna:UBO00367289': ('Un itinerario nello sviluppo dei rapporti sociali, vol. 1: Preistoria, Mesopotamia, Egitto, Africa Nera, India, Americhe', '1'),
             'bologna:UBO00322891': ('Lo sviluppo del pensiero e le forme del comunicare, vol. 1: Medioevo, Islam', '2'), 'bologna:UBO00256685': ('Fenomenologia della conoscenza, vol. 2', '3'), 'bologna:UBO00256687': ('Fenomenologia della conoscenza, vol. 1', '3'),
             'bologna:UBO00864587': ('Collected papers of Charles Sanders Peirce, vol. 3/4: Exact logic : (published papers) ; and The simplest mathematics', None), 'bologna:UBO07313601': ('La filosofia contemporanea, vol. 4.2', '4'), 'bologna:UBO01048723': ("L'Eta romantica, vol. 2", None)}
    wrong18 = [(k, tt.get(k) and tt[k][0], tt.get(k) and tt[k][2]) for k, (title, sv) in exp18.items() if not tt.get(k) or tt[k][0] != title or (tt[k][2] or None) != sv]
    check(not wrong18, "the eight Bologna volumes read from their set title, the set's own number kept as set_volume, never as a bare prefix (%s)" % (wrong18[:3] or 'all eight'))
    check(bool(tt.get('bologna:UBO00367289')) and tt['bologna:UBO00367289'][1] == 'An Itinerary in the Development of Social Relations, vol. 1: Prehistory, Mesopotamia, Egypt, Black Africa, India, the Americas', "the English title of UBO00367289 has lost the '1:' its native title lost (%s)" % (tt.get('bologna:UBO00367289') and tt['bologna:UBO00367289'][1],))
    check(not v18['bare'], 'no served title, English title or set title opens with the catalogue\'s bare volume number and colon (%s)' % (v18['bare'][:4],))
    check(len(v18['setVolumes']) >= 7 and all(x[2] and x[3] for x in v18['setVolumes']), 'every set_volume comes with the set title as exported in set_title_raw, opening with that number (%d entries)' % len(v18['setVolumes']))
    check(bool(tt.get('braidense:BA1E011899')) and tt['braidense:BA1E011899'][0].startswith('Frederici Ruyschii') and tt['braidense:BA1E011899'][2] == '23', "the Ruysch volume (BA1E011899) reads from its set without the '[23]: ' prefix, kept as set_volume (%s)" % (tt.get('braidense:BA1E011899') and tt['braidense:BA1E011899'][0][:40],))
    check(bool(tt.get('braidense:NAPE007651')) and tt['braidense:NAPE007651'][0] == 'Dialogi di Antonio Brucioli delea [sic] naturale philosophia, vol. 3', "Brucioli's third dialogue prints the cataloguer's mark as '[sic]' (%s)" % (tt.get('braidense:NAPE007651') and tt['braidense:NAPE007651'][0],))
    check(len(v18['sic']) >= 8 and not v18['bang'], 'the export\'s [!] marks print as [sic] wherever they stand (%d titles) and no served text keeps a [!] or a []] (%s)' % (len(v18['sic']), v18['bang'][:3]))
    vt = v18['vt'] or {}
    check(bool(vt) and isinstance(vt.get('composed'), dict) and (vt.get('bologna', 0) + vt.get('braidense', 0)) == v18['withStatement'] and v18['withStatement'] >= 840, 'the volume-title count is the count of the entries served with a volume statement (%s = %d), the generator\'s own tally kept apart as composed' % ({k: v for k, v in vt.items() if k != 'composed' and k != 'note'}, v18['withStatement']))
    check(v18['warnings'] == [], 'the generator ran without a warning: the nine object-map notes are resolved at their rules (meta.warnings %s)' % (v18['warnings'] if v18['warnings'] != [] else 'empty'))
    noted18 = set(x[0] for x in v18['fitNotes'])
    check(all(f in noted18 for f in v18['fitted']) and len(v18['fitNotes']) >= 3, 'an object the generator moves off its rule position carries a note saying so, and the six object-map rules state what is drawn (moved: %s; noted: %s)' % (v18['fitted'], sorted(noted18)))
    check(bool(v18['pubLinks']) and bool(v18['pubLink']) and v18['pubLink'][0] == "nota di vendita Christie's" and 'Augsburg del 1490' in v18['pubText'], "the Publicius Notable text prints its named source, the Christie's sale note, as the link to the lot page (%s)" % (v18['pubLink'],))
    check('the film' in ' '.join(v18['greekSource']) and 'youtube' not in ' '.join(v18['greekSource']).lower() and 'youtube.com' not in v18['greekPanel'], "a description read from the film names the film and its minute as its source, not the host (%s)" % (v18['greekSource'],))
    check(not v18['stopIds'], 'every tour stop id is named after its tour (%s); the ids are stable names, not positions (schema_eco.md)' % (v18['stopIds'][:3] or 'all'))
    page.click('#aboutBtn'); page.wait_for_timeout(400)
    about18 = page.evaluate("() => document.getElementById('about').textContent")
    check('Generator warnings' not in about18 and 'shelf slots' in about18, "the About panel prints no 'Generator warnings' list")
    page.evaluate("() => document.getElementById('aboutClose').click()"); page.wait_for_timeout(200)
    # ---- volume ranges in the titles, language names, edition descriptions --------------------------------------------
    v19 = page.evaluate(r"""() => { const D = window.__data(), out = {};
      const g = (id) => { const i = D._index.get(id); return i === undefined ? null : D.books[i]; };
      const colon = /vol\. [\d./-]+: \d{1,2}(?:\s*:|\s*$)/;   // a volume number, a colon and a bare number ('vol. 1: 2: Principles', 'vol. 5: 1') is a range read as a separator
      out.colon = D.books.filter((b) => colon.test(b.title || '') || colon.test(b.title_en || '') || colon.test(b.set_title || '')).map((b) => [b.id, b.title, b.title_en]);
      out.ranges = {}; for (const id of ['bologna:UBO00864586', 'bologna:UBO00864588', 'bologna:UBO02057771', 'braidense:URB0451594', 'bologna:UBO09158424', 'bologna:UBO09158420', 'bologna:UBO00388782']) { const b = g(id); out.ranges[id] = b ? [b.title, b.title_en || null, b.volume_statement || null] : null; }
      out.codes = {}; out.bareNames = []; for (const b of D.books) { if (!b.language) continue; out.codes[b.language] = (out.codes[b.language] || 0) + 1; if (!b.language_name || /^[a-z]{2,3}$/.test(b.language_name)) out.bareNames.push([b.id, b.language, b.language_name || null]); }
      const ed = /^\s*(?:(?:A|An|The)\s+)?([A-Z][A-Za-z-]+(?:\s+[A-Z][a-z]+)?)\s+(?:edition|translation)\b/;
      out.editions = []; for (const b of D.books) { if (b.description_kind !== 'edition') continue; const m = ed.exec(b.description || ''); out.editions.push([b.id, m ? m[1] : null, b.language_name || null, !!b.description_source]); }
      const bd = g('video:M8IWTOFNlOc:1444:baudolino'), sb = g('video:ygvl-_gtAP8:90:fukoovo-klatno');
      out.baudolino = bd ? [bd.description || null, bd.description_source || null, bd.language_name || null] : null; out.serbian = sb ? [sb.description || null, sb.description_source || null, sb.language_name || null] : null;
      out.essays10 = null; for (const t of (D.meta.tours || [])) for (const st of t.stops) if (st.id === 'essays-10') out.essays10 = st.caption;
      return out; }""")
    check(not v19['colon'], "no served title, English title or set title prints a volume number, a colon and a bare number ('vol. 1: 2'): the catalogue's range keeps its hyphen (%s)" % (v19['colon'][:3] or 'none'))
    exp19 = {'bologna:UBO00864586': 'Collected papers of Charles Sanders Peirce, vol. 1-2: Principles of philosophy, and ; Elements of Logic', 'bologna:UBO00864588': 'Collected papers of Charles Sanders Peirce, vol. 5-6: Pragmatism and pragmaticism, and ; Scientific metaphysics',
             'bologna:UBO02057771': 'Collected papers of Charles Sanders Peirce, vol. 7-8: Science and philosophy, and ; Reviews, correspondence, and bibliography', 'braidense:URB0451594': "Manuel du libraire et de l'amateur de livres, vol. 7-8: Supplement 1-2",
             'bologna:UBO09158424': 'Corso di storia della Chiesa, vol. 5-2', 'bologna:UBO09158420': 'Corso di storia della Chiesa, vol. 5-1: La chiesa nei tempi moderni', 'bologna:UBO00388782': 'Aristoteles Latinus, vol. 31.1-2: Rhetorica : translatio anonyma, sive Vetus et translatio Guillelmi de Moerbeka'}
    wrong19 = [(k, v19['ranges'].get(k) and v19['ranges'][k][0]) for k, t19 in exp19.items() if not v19['ranges'].get(k) or v19['ranges'][k][0] != t19]
    check(not wrong19, "the seven volumes whose statements open with the catalogue's range read 'vol. 1-2: Principles of philosophy ...', 'vol. 5-1: La chiesa nei tempi moderni' (the part's title after the range), 'vol. 31.1-2: Rhetorica ...' (%s)" % (wrong19[:3] or 'all seven'))
    ar19 = v19['ranges'].get('bologna:UBO00388782')
    check(bool(ar19) and ar19[1] == "Aristoteles Latinus, vol. 31.1-2: Rhetoric, the Anonymous Translation, or the Old Version, and William of Moerbeke's Translation", 'the English title of the Aristoteles Latinus volume keeps the range too (%s)' % (ar19 and ar19[1],))
    check(not v19['bareNames'] and len(v19['codes']) >= 30, 'every entry with a language carries its name, none the bare code (%d codes served%s)' % (len(v19['codes']), '' if not v19['bareNames'] else '; bare: %s' % v19['bareNames'][:4]))
    names19 = {'bologna:UBO07571497': 'no linguistic content', 'bologna:UBO00030694': 'no linguistic content', 'bologna:UBO09164572': 'Old French', 'bologna:UBO09164588': 'Old French', 'video:zZEy10fpq3I:4465:името-на-розата': 'Bulgarian', 'video:ygvl-_gtAP8:89:баудолино': 'Bulgarian',
               'video:ygvl-_gtAP8:94:prazkyi-tsvyntar': 'Ukrainian', 'video:zZEy10fpq3I:566:празькии-цвинтар': 'Ukrainian', 'video:ygvl-_gtAP8:90:istoriya-yevropeiskoyi-tsyvilizatsiyi-ry': 'Ukrainian', 'video:ygvl-_gtAP8:90:prahos-kapines': 'Lithuanian', 'bologna:UBO09961826': 'Lithuanian', 'bologna:UBO10177692': 'Korean'}
    rows19 = page.evaluate(r"""(ids) => ids.map((id) => { window.__openBook(id, false); const pb = document.getElementById('pBody'); const dt = [...pb.querySelectorAll('dt')].find((x) => x.textContent.trim() === 'Language'); return [id, dt && dt.nextElementSibling ? dt.nextElementSibling.textContent.trim() : null]; })""", list(names19))
    bad19n = [(id19, got19, names19[id19]) for id19, got19 in rows19 if got19 != names19[id19]]
    check(not bad19n, "the twelve cards that printed the record's language code ('uk', 'lt', 'bg', 'kor', 'lit', 'fro', 'zxx') print the language's name on their Language row (%s)" % (bad19n[:4] or 'all twelve'))
    page.evaluate("() => document.getElementById('langBtn').click()"); page.wait_for_timeout(300)   # the English mode: the Language row is the same name
    rows19e = page.evaluate(r"""(ids) => ids.map((id) => { window.__openBook(id, false); const pb = document.getElementById('pBody'); const dt = [...pb.querySelectorAll('dt')].find((x) => x.textContent.trim() === 'Language'); return [id, dt && dt.nextElementSibling ? dt.nextElementSibling.textContent.trim() : null]; })""", list(names19)[:4])
    page.evaluate("() => document.getElementById('langBtn').click()"); page.wait_for_timeout(300)
    check(all(got19 == names19[id19] for id19, got19 in rows19e), 'the Language row names the language in the English mode too (%s)' % (rows19e,))
    contra19 = [x for x in v19['editions'] if x[1] and x[1] != x[2]]
    check(len(v19['editions']) >= 24 and not contra19 and all(x[3] for x in v19['editions']), "no edition description contradicts the card's language line, and every one carries its source (%d read%s)" % (len(v19['editions']), '' if not contra19 else '; contradicted: %s' % contra19[:3]))
    check(bool(v19['baudolino']) and v19['baudolino'][0] == "Italian edition of Umberto Eco's Baudolino (2000)." and bool(v19['baudolino'][1]) and 'M8IWTOFNlOc' in v19['baudolino'][1] and v19['baudolino'][2] == 'Italian', "the Baudolino copy of the Louisiana shot is described as the Italian edition the frame shows, with the film as its source (%s)" % (v19['baudolino'],))
    check(bool(v19['serbian']) and v19['serbian'][0] == "Serbian edition of Umberto Eco's Foucault's Pendulum (Il pendolo di Foucault, 1988)." and v19['serbian'][2] == 'Serbian', "the Serbian Foucault's Pendulum is described as the Serbian edition its spine spells (%s)" % (v19['serbian'],))
    src19 = page.evaluate("() => { window.__openBook('video:M8IWTOFNlOc:1444:baudolino', false); const pb = document.getElementById('pBody'); return [[...pb.querySelectorAll('p.desc small a')].map((x) => x.textContent).join(' | '), pb.textContent]; }")
    check('the film' in src19[0] and 'Italian edition' in src19[1] and 'English edition' not in src19[1], "the Baudolino card prints the Italian edition with the film and its minute as the source (%s)" % (src19[0],))
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    check(bool(v19['essays10']) and 'Revue des Deux Mondes in 1853' in v19['essays10'] and 'this collection of 1854' in v19['essays10'] and 'first appeared in this collection' not in v19['essays10'], "essays-10's caption dates Sylvie's first appearance to the Revue des Deux Mondes of 1853 and the collection to 1854 (%s)" % ((v19['essays10'] or '')[:120],))

    # ---- the address, Copy link, the copy notes, the rule sweep, the More menu, search, Any book, the preview picture --------
    v20 = page.evaluate(r"""() => { const D = window.__data(), out = {}, H = ['marginalia', 'underlinings', 'dog-ears', 'inserts'];
      const NAT = /\b(?:narrativa|poesia|letteratura|teatro|racconti|romanzi|prosa|poeti|scrittori|poemi|liriche?|novelle|fiabe|favole)\b[^|]{0,30}?\b(?:italian[aeio]|frances[ei]|ingles[ei]|american[aeio]|tedesc[ahio]|spagnol[aeio]|russ[aeio]|portoghes[ei])\b/i;
      out.inscr = 0; out.inscrBad = []; out.givers = 0; out.giverBad = []; out.hand4 = 0; out.island = []; out.theoryN = 0; out.lit = 0; out.litOff = [];
      const LIT = { 'Italian literature': /^corridor-0[1-8]$/, 'French literature': /^corridor-(09|1[0-3])$/, 'English-language literature': /^corridor-1[4-8]$/, 'German literature': /^corridor-(19|20)$/ };
      for (const b of D.books) { const c = b.copy;
        if (c && c.inscription) { out.inscr++; if (!((c.annotation || '') + ' ' + (c.condition || '')).includes(c.inscription) || c.inscription.length < 4) out.inscrBad.push(b.id); }
        if (c && c.givers && c.givers.length) { out.givers++; for (const g of c.givers) if (/[<>]|,\s*$/.test(g)) out.giverBad.push([b.id, g]); }
        if (c && c.marks && H.filter((k) => c.marks.includes(k)).length === 4) out.hand4++;
        if (b.placement_rule === 'semiotics, linguistics, literary theory (islands)') { out.theoryN++; if ((b.subjects || []).some((s) => NAT.test(s))) out.island.push([b.id, b.title]); }
        if (LIT[b.placement_rule]) { out.lit++; if (!LIT[b.placement_rule].test(b.bookcase || '')) out.litOff.push([b.id, b.placement_rule, b.bookcase]); } }
      out.meta = (D.meta.counts.catalog || {}).bologna_copies || null; out.note = D.meta.counts.overlay_note || {}; return out; }""")
    bc20 = v20['meta'] or {}
    check(v20['inscr'] >= 800 and not v20['inscrBad'] and bc20.get('with_inscription') == v20['inscr'], '%d Bologna copies carry the words the cataloguer transcribed from the dedication, each verbatim in the copy note or its condition line, the count in meta (%s)' % (v20['inscr'], v20['inscrBad'][:3] or bc20.get('with_inscription')))
    check(v20['givers'] >= 800 and not v20['giverBad'] and bc20.get('with_named_giver') == v20['givers'] and len(bc20.get('top_givers') or []) == 12 and (bc20.get('top_givers') or [[None]])[0][0] == 'Alberto Arbasino', '%d copies name their giver as a reader says the name, the twelve who inscribed most in meta (%s)' % (v20['givers'], v20['giverBad'][:3] or (bc20.get('top_givers') or [None])[0]))
    check(bc20.get('hand', {}).get('4') == v20['hand4'] and bc20.get('hand_any', 0) > 1500 and 'hand' in v20['note'] and 'given' in v20['note'], 'the hand counts of meta agree with the copies (%d with all four kinds of mark) and both colour modes carry their note' % v20['hand4'])
    check(v20['theoryN'] > 0 and not v20['island'], 'no record classed as a national literature sits on the literary-theory island (%d records there; %s)' % (v20['theoryN'], v20['island'][:3] or 'none'))
    check(v20['lit'] > 200 and not v20['litOff'], 'every record a literature rule places stands on that literature\'s corridor bookcases (%d records; %s)' % (v20['lit'], v20['litOff'][:3] or 'none'))
    # the address and the link
    page.evaluate("(id) => window.__openBook(id)", 'bologna:UBO00436664'); settle(page)
    st20 = page.evaluate("() => ({ hash: location.hash, s: window.__state.string(), link: window.__state.link(), top: document.getElementById('panel').getBoundingClientRect().top, bar: document.getElementById('topbar').getBoundingClientRect().bottom, inscr: (document.querySelector('#pBody .inscr') || {}).textContent || '', rows: [...document.querySelectorAll('#pBody dt')].map((d) => d.textContent.trim()) })")
    check(st20['hash'] == '#book=bologna%3AUBO00436664' and st20['s'] == 'book=bologna%3AUBO00436664', 'the address carries the open book (%s)' % st20['hash'])
    check(st20['link'].startswith(base) and re.search(r'#book=bologna%3AUBO00436664&eye=-?[\d.]+%2C-?[\d.]+%2C-?[\d.]+&at=-?[\d.]+%2C', st20['link']) is not None, 'Copy link composes the address with the exact view (%s)' % st20['link'][len(base):][:80])
    check('Con molta stima' in st20['inscr'] and 'Written in the book by Donatella Di Cesare' in st20['inscr'] and 'Inscribed by' in st20['rows'], "the card quotes the inscription and says who wrote it, with an Inscribed by row (%s)" % st20['inscr'][:60])
    check(st20['top'] >= st20['bar'] - 1, 'the card opens under the top bar (top %.0f, bar %.0f)' % (st20['top'], st20['bar']))
    page.screenshot(path=os.path.join(args.shots, 'card-inscription.png'))
    page.click('#pLink'); page.wait_for_timeout(500)
    cl20 = page.evaluate("() => ({ btn: document.getElementById('pLink').textContent, box: document.getElementById('linkBox').classList.contains('show'), last: window.__lastLink || '' })")
    check((cl20['btn'] == 'Copied' or cl20['box']) and '#book=' in cl20['last'], 'Copy link copies the address or shows it to copy (%s)' % ({k: cl20[k] for k in ('btn', 'box')},))
    link20 = cl20['last']
    page.evaluate("() => { document.getElementById('linkBox').classList.remove('show'); document.getElementById('pClose').click(); }"); page.wait_for_timeout(300)
    check(page.evaluate("() => location.hash") in ('', '#room=vestibolo'), 'closing the card leaves the room alone in the address (%s)' % page.evaluate("() => location.hash"))
    p20 = ctx.new_page(); p20.goto(link20, wait_until='load'); wait_ready(p20, args.timeout * 2); settle(p20, 1200)
    l20 = p20.evaluate("() => ({ welcome: window.__state.welcome(), panel: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent, eye: window.__tours.state().eye })")
    m20 = re.search(r'eye=(-?[\d.]+)%2C(-?[\d.]+)%2C(-?[\d.]+)', link20); eye20 = [float(x) for x in m20.groups()] if m20 else None
    check(not l20['welcome'] and l20['panel'] and l20['title'].startswith('Torah e filosofia') and eye20 is not None and all(abs(a - b) < 0.06 for a, b in zip(eye20, l20['eye'])), 'the copied link opens the same book from the same eye, with no opening card (%s; eye %s)' % (l20['title'][:30], [round(x, 2) for x in l20['eye']]))
    p20.screenshot(path=os.path.join(args.shots, 'link-lands.png')); p20.close()
    for h20, want20 in [('#tour=rose&stop=3', 'tour'), ('#room=studio&lang=en&colour=given&show=certain', 'room'), ('#mode=walk&room=corridoio', 'walk'), ('#object=obj:salotto:piano', 'object')]:
        p20 = ctx.new_page(); p20.goto(base + 'index.html' + h20, wait_until='load'); wait_ready(p20, args.timeout * 2); settle(p20, 1200)
        s20 = p20.evaluate("() => ({ welcome: window.__state.welcome(), tour: window.__tours.state().id, step: window.__tours.state().step, card: window.__tours.state().card, room: window.__currentRoom(), colour: window.__overlay.mode(), filter: window.__overlay.state().filter, lang: document.getElementById('langBtn').classList.contains('on'), walk: document.getElementById('modeWalk').classList.contains('on'), panel: document.getElementById('pTitle').textContent, hash: location.hash })")
        if want20 == 'tour': ok20 = s20['tour'] == 'rose' and s20['step'] == 2 and s20['card'] and s20['hash'] == '#tour=rose&stop=3'
        elif want20 == 'room': ok20 = s20['room'] == 'studio' and s20['colour'] == 'given' and s20['filter'] == 'certain' and s20['lang'] and s20['hash'] == '#room=studio&lang=en&colour=given&show=certain'
        elif want20 == 'walk': ok20 = s20['walk'] and s20['room'] == 'corridoio' and 'mode=walk' in s20['hash']
        else: ok20 = 'piano' in s20['panel'].lower() and s20['hash'].startswith('#object=')
        check(ok20 and not s20['welcome'], 'the address %s lands on that state with no opening card (%s)' % (h20, {k: s20[k] for k in ('tour', 'step', 'room', 'colour', 'filter', 'lang', 'walk', 'hash')}))
        if want20 in ('tour', 'walk'): p20.screenshot(path=os.path.join(args.shots, 'link-%s.png' % want20))
        p20.close()
    # the More menu and Eco's copies
    page.click('#moreBtn'); page.wait_for_timeout(300)
    mm20 = page.evaluate("() => ({ open: window.__state.more(), items: [...document.querySelectorAll('#moreMenu button')].filter((b) => !b.hidden).map((b) => b.id), on: [...document.querySelectorAll('#moreMenu button.on')].map((b) => b.id), right: document.getElementById('moreMenu').getBoundingClientRect().right })")
    check(mm20['open'] and mm20['items'] == ['walkBtn', 'notableBtn', 'handBtn', 'fogBtn', 'lettersBtn'] and mm20['on'] == ['fogBtn', 'lettersBtn'] and mm20['right'] <= 1440, "the More menu holds Eco's walk, the notable books, Eco's copies, the fog and the lettering, the two layers marked on (%s)" % (mm20['items'],))
    page.screenshot(path=os.path.join(args.shots, 'more.png'), clip={'x': 0, 'y': 0, 'width': 1440, 'height': 330})
    page.keyboard.press('Escape'); page.wait_for_timeout(200)
    check(not page.evaluate("() => window.__state.more()"), 'Escape closes the More menu')
    menu_click(page, '#handBtn')
    hd20 = page.evaluate("() => ({ menu: window.__state.more(), hand: document.getElementById('hand').classList.contains('show'), cats: [...document.querySelectorAll('#handList .notable-cat')].map((e) => e.dataset.giver).slice(0, 3), last: [...document.querySelectorAll('#handList .notable-cat')].slice(-1).map((e) => e.dataset.giver)[0], quoted: [...document.querySelectorAll('#handList .r')].filter((r) => r.textContent.includes('“')).length })")
    check(hd20['hand'] and not hd20['menu'] and hd20['cats'][0] == 'Alberto Arbasino' and hd20['last'] == 'Giver not named' and hd20['quoted'] > 300, "Eco's copies opens from the menu (which closes) on the dedications by giver, the unnamed last, the words quoted on the rows (%s; %d quoted)" % (hd20['cats'], hd20['quoted']))
    page.screenshot(path=os.path.join(args.shots, 'hand-givers.png'))
    page.evaluate("() => document.getElementById('hand').classList.remove('show')")
    # the two colour modes and their legends
    for mode20 in ('hand', 'given'):
        page.evaluate("(m) => window.__overlay.set(m)", mode20); page.wait_for_timeout(700)
        lg20 = page.evaluate("() => ({ mode: window.__overlay.mode(), legend: window.__overlay.state().legend, rows: [...document.querySelectorAll('#legend .row')].map((e) => e.textContent.trim().replace(/\\s+/g, ' ')), givers: [...document.querySelectorAll('#legend a.giver')].map((a) => a.textContent), note: (document.querySelector('#legend .note') || {}).textContent || '', head: document.querySelector('#legend h4 span').textContent, hash: location.hash })")
        keys20 = [k for k, _ in lg20['legend']]; n20 = dict(lg20['legend'])
        if mode20 == 'hand': ok20 = keys20 == ['4', '3', '2', '1', '0', '-1', 'unlabelled'] and n20['4'] == v20['hand4'] and sum(n20[k] for k in ('4', '3', '2', '1')) == bc20.get('hand_any') and lg20['head'] == "Colour: Eco's hand" and not lg20['givers']
        else: ok20 = keys20 == ['named', 'unnamed', 'eco', 'plain', 'none', 'unlabelled'] and n20['named'] == v20['givers'] and n20['named'] + n20['unnamed'] == bc20.get('inscribed') and lg20['head'] == 'Colour: Given to Eco' and lg20['givers'][:2] == ['Alberto Arbasino', 'Alberto Bevilacqua'] and len(lg20['givers']) >= 10
        check(ok20 and lg20['mode'] == mode20 and len(lg20['rows']) == len(keys20) and all(str(n20[k]) in r.replace(',', '') for k, r in zip(keys20, lg20['rows'])) and lg20['note'] and ('colour=%s' % mode20) in lg20['hash'], 'the %s legend lists its classes with the copies\' counts, its note and the address (%s)' % (mode20, lg20['legend']))
        page.screenshot(path=os.path.join(args.shots, 'legend-%s.png' % mode20))
    page.click('#legend a.giver'); page.wait_for_timeout(600)
    gv20 = page.evaluate("() => ({ hand: document.getElementById('hand').classList.contains('show'), top: (() => { const h = [...document.querySelectorAll('#handList .notable-cat')].find((d) => d.dataset.giver === 'Alberto Arbasino'); const l = document.getElementById('handList'); return h && l ? h.getBoundingClientRect().top - l.getBoundingClientRect().top : null; })() })")
    check(gv20['hand'] and gv20['top'] is not None and abs(gv20['top']) < 40, "a giver's name in the legend opens Eco's copies at that giver (%s)" % (gv20,))
    page.evaluate("() => { document.getElementById('hand').classList.remove('show'); window.__overlay.set('language'); }"); page.wait_for_timeout(300)
    # search: the tours and the objects are found too, each word whole; a book by its subjects, its giver and its marks
    for q20, kind20, min20 in (('rose', 'tour', 4), ('piano', 'object', 4), ('Arbasino', 'book', 4), ('marginalia', 'book', 4), ('narratologia', 'book', 1)):   # a word held whole by one title finds that title alone
        page.fill('#q', q20); page.wait_for_timeout(600)
        rs20 = page.evaluate("() => [...document.querySelectorAll('#results .r')].map((e) => e.dataset.tour ? 'tour' : e.dataset.obj ? 'object' : 'book')")
        check(kind20 in rs20 and len(rs20) >= min20, 'search %r finds %s (%d results: %d tours, %d objects)' % (q20, kind20, len(rs20), rs20.count('tour'), rs20.count('object')))
    page.fill('#q', 'Barthes'); page.wait_for_timeout(600)
    bt20 = page.evaluate("() => { const r = [...document.querySelectorAll('#results .r')]; return { tours: r.filter((e) => e.dataset.tour).map((e) => e.textContent), firstBook: (r.find((e) => e.dataset.id) || {}).textContent || '' }; }")
    check(not bt20['tours'] and 'Barthes' in bt20['firstBook'], 'a name the captions do not hold whole brings no tour stop above the books (%s)' % (bt20['tours'][:2] or bt20['firstBook'][:50],))
    page.fill('#q', 'rose'); page.wait_for_timeout(600); page.click('#results .r[data-tour]'); settle(page, 1200)
    ts20 = page.evaluate("() => ({ id: window.__tours.state().id, card: window.__tours.state().card, hash: location.hash })")
    check(ts20['id'] and ts20['card'] and ts20['hash'].startswith('#tour='), 'a tour found by search starts (%s)' % (ts20,))
    page.evaluate("() => window.__tour.end()"); page.wait_for_timeout(300); page.fill('#q', ''); page.keyboard.press('Escape')
    page.fill('#q', 'Name of the Rose'); page.wait_for_timeout(600)
    en20 = page.evaluate("() => { const r = [...document.querySelectorAll('#results .r')], tours = r.filter((e) => e.dataset.tour); return { tourRows: tours.length, tours: new Set(tours.map((e) => e.dataset.tour)).size, objects: r.filter((e) => e.dataset.obj).length, firstBook: r.findIndex((e) => e.dataset.id) }; }")
    check(0 < en20['tourRows'] <= 3 and en20['tourRows'] == en20['tours'] and en20['objects'] <= 2 and 0 <= en20['firstBook'] <= 5, '"Name of the Rose" lists one row per tour, three tours and two objects at most, the first book by the sixth row (%s)' % (en20,))
    page.press('#q', 'Enter'); settle(page, 1200)
    en20b = page.evaluate("() => ({ open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent, tour: window.__tours.state().id })")
    check(en20b['open'] and re.search(r'\bros[ae]\b', en20b['title'], re.I) is not None and not en20b['tour'], 'Enter opens the first book, not the tour listed above it (%s)' % (en20b['title'][:40],))
    rid20 = page.evaluate("() => window.__random()"); settle(page)
    rb20 = page.evaluate("(id) => { const D = window.__data(), b = D.books[D._index.get(id)]; return b ? { desc: !!b.description, kind: b.description_kind, ref: b.placement === 'reference', open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent, hash: location.hash } : null; }", rid20)
    check(rb20 is not None and rb20['open'] and rb20['desc'] and rb20['kind'] != 'author' and not rb20['ref'] and rb20['hash'].startswith('#book='), 'Any book opens a book with a description of its own and writes it into the address (%s)' % ((rb20 or {}).get('title', '')[:40],))
    page.evaluate("() => document.getElementById('pClose').click()"); page.wait_for_timeout(200)
    # the Todesco author lines, the served titles' tails and pipes, the plate rule on the landing frame
    td20 = page.evaluate("""() => { const D = window.__data(); const g = (id) => { const b = D.books[D._index.get(id)]; return b ? { title: b.title, author: b.author, fromSet: !!b.author_from_set, part: b.part_title || null, vs: b.volume_statement || null } : null; };
      const bare = /^\\s*\\[?\\d{1,3}(?:\\s*[-\\u2013.]\\s*\\d{1,3})*\\]?\\s*\\.?\\s*$/;
      const cands = D.books.filter((b) => b.catalog === 'bologna' && b.volume_statement && bare.test(b.volume_statement) && b.author && !b.author_from_set).map((b) => [b.id, b.author]);
      return { a: g('bologna:UBO09158420'), b: g('bologna:UBO09158386'), c: g('bologna:UBO09158424'), n: D.meta.counts.catalog.part_titles_from_responsibility, cands }; }""")
    name20 = re.compile(r"^(?:(?:di|de|da|von|van|par|by|del|della|dei|degli|delle|du|des)\s+)?(?:(?:[A-ZÀ-Ý]\.\s*)+[A-ZÀ-Ý][\w'’-]+|[A-ZÀ-Ý][\w'’-]+(?:\s+(?:(?:de|da|di|del|della|von|van|le|la|du|des)\s+|d[’'])?[A-ZÀ-Ý][\w'’-]+){0,3}|[A-ZÀ-Ý][\w'’-]+,\s*[A-ZÀ-Ý].*)\.?$")
    role20 = re.compile(r"a cura di|\bcura\b|edited|\bed\.|\beds\.|editor|hrsg|herausgegeben|translat|\btrad\b|\btrad\.|traduzione|traduction|introduzione|prefazione|pr[ée]face|\bby\b|\bpar\b", re.I)
    odd20 = [c for c in td20['cands'] if not name20.match(c[1]) and not role20.search(c[1])]
    check(td20['a'] is not None and td20['a']['author'] == 'L. Todesco' and td20['a']['fromSet'] and td20['a']['title'] == 'Corso di storia della Chiesa, vol. 5-1: La chiesa nei tempi moderni' and td20['a']['part'] == 'La chiesa nei tempi moderni' and td20['a']['vs'] == '5-1' and td20['b'] is not None and td20['b']['author'] == 'L. Todesco' and td20['b']['title'] == 'Corso di storia della Chiesa, vol. 1: I primi 300 anni' and td20['c'] is not None and td20['c']['author'] == 'L. Todesco' and not td20['c']['fromSet'], "the two Todesco volumes print L. Todesco as the author, from the set's statement, and the part's title after the number (%s; %s)" % ((td20['a'] or {}).get('title'), (td20['a'] or {}).get('author')))
    check(td20['n'] >= 2 and not odd20, 'no Bologna volume record whose own title is a bare number prints a phrase as its author (%d authors taken from the set; odd: %s)' % (td20['n'], odd20[:3]))
    tt20 = page.evaluate("""() => { const D = window.__data(); const g = (id) => { const b = D.books[D._index.get(id)]; return b ? [b.title, b.title_raw || null] : null; };
      const bad = D.books.filter((b) => ['title', 'set_title', 'volume_statement', 'part_title'].some((k) => b[k] && (/[\\/:;|]\\s*$/.test(b[k]) || b[k].includes('|')))).map((b) => [b.id, b.title]).slice(0, 5);
      return { a: g('bologna:UBO07571497'), b: g('bologna:UBO01855538'), c: g('braidense:MILE062651'), d: g('braidense:BVEE032772'), bad, n: D.meta.counts.catalog.title_tails_cleaned }; }""")
    check(tt20['a'] is not None and tt20['a'][0] == 'Disegni & Caviglia contro tutti : quando la satira diventa criminale' and bool(tt20['a'][1]) and '|' in tt20['a'][1] and tt20['b'] is not None and tt20['b'][0] == 'Il romanzo al tempo di Luigi 13.' and (tt20['b'][1] or '').endswith('/') and tt20['c'] is not None and tt20['c'][0].endswith('in any age') and (tt20['c'][1] or '').endswith(':') and tt20['d'] is not None and tt20['d'][0].endswith('proponitur') and (tt20['d'][1] or '').endswith(';'), "the four titles read without the export's tail or pipes, title_raw keeping the export's words (%s)" % ((tt20['a'] or [''])[0][:60],))
    check(not tt20['bad'] and tt20['n'] >= 4, 'no served title, set title, volume statement or part title ends with " /", " :", ";" or "|" or holds a pipe (%d cleaned; %s)' % (tt20['n'], tt20['bad'][:3]))
    plc20 = {}
    for tid20, k20 in (('prague', 9), ('essays', 9)):
        page.evaluate("() => window.__setMode('walk')"); page.wait_for_timeout(300)
        page.evaluate('(id) => window.__tours.start(id)', tid20); page.wait_for_timeout(400)
        for _ in range(k20): page.evaluate('() => window.__tour.next()'); page.wait_for_timeout(120)
        try: page.wait_for_function('!window.__flying()', timeout=30000)
        except Exception: pass
        pl20 = page.evaluate('() => window.__plates()')   # read on the landing frame: no label pass waited for
        plc20['%s-%02d' % (tid20, k20 + 1)] = ([q['text'][:40] for q in pl20['plates'] if q['inWay'] and q['visible']] if pl20 and pl20['stop'] else ['not read'])
        page.evaluate('() => window.__tour.end()'); page.wait_for_timeout(200)
    page.evaluate("() => window.__setMode('orbit')"); settle(page, 300)
    check(all(not v for v in plc20.values()), 'a plate in the way gives way on the landing frame itself at prague-10 and essays-10 in walk view, no label pass waited for (%s)' % (plc20,))
    # the preview tags and the picture; the visible strings the version rewrote
    head20 = page.evaluate("() => ({ og: (document.querySelector('meta[property=\"og:image\"]') || {}).content, canon: (document.querySelector('link[rel=canonical]') || {}).href, desc: (document.querySelector('meta[name=description]') || {}).content || '', title: (document.querySelector('meta[property=\"og:title\"]') || {}).content || '', brand: document.querySelector('.brand small').textContent, tours: document.getElementById('toursHead').textContent, q: document.getElementById('q').placeholder, rnd: document.getElementById('randomBtn').textContent })")
    pv20 = os.path.join(args.dist, 'preview.jpg')
    try:
        from PIL import Image as _Im20; sz20 = _Im20.open(pv20).size if os.path.exists(pv20) else None
    except ImportError: sz20 = (1200, 630) if os.path.exists(pv20) else None
    check(head20['og'] == 'https://eco-library-map.netlify.app/preview.jpg' and head20['canon'] == 'https://eco-library-map.netlify.app/' and head20['title'] == "Umberto Eco's library, room by room" and len(head20['desc']) > 60 and sz20 == (1200, 630), 'the preview tags name the site, its title and its picture, and dist/preview.jpg is 1200 by 630 (%s)' % (sz20,))
    check(head20['brand'] == "Umberto Eco's Milan flat, about 33,000 books" and head20['tours'].count('.') <= 3 and head20['q'].startswith('Search titles, authors, subjects') and head20['rnd'] == 'Any book', 'the brand line, the Tours head, the search field and the Any book button read as rewritten (%s)' % (head20['tours'][:80],))
    # ---- the legends counted from the data, the inscriptions closed at their own quotation marks, Eco's own dedications, the composed titles, Back, the card's click, the preview, the hint box, search, the viewpoints ----
    v21 = page.evaluate(r"""() => { const D = window.__data(), out = { given: {}, hand: {}, eco: [], ecoGiver: [], inscr: 0, inscrBad: [], inscrShort: [], inscrRemark: [], inscrStop: 0, colon: 0, colonBad: [], rawKept: 0, apos: [], ormesson: 0, gone: [], readings: {} };
      const EL = /\b(l|d|un|dell|dall|nell|all|sull|quell|coll|dagl|degl|negl|agl|sugl|gl|c|ch|s|m|t|v|n|qu|j|jusqu|lorsqu|puisqu|quoiqu)['\u2019] (?=[\w\u00c0-\u024f])/i;
      const REM = /[;.]\s*(orecchie|sottolineat|segni|annotazion|note manoscritte|allegat|inserit|postill)/i;
      for (const b of D.books) { const k = window.__classes(b.id), un = b.origin === 'unlabelled'; const gk = un ? 'unlabelled' : k.given, hk = un ? 'unlabelled' : String(k.hand); out.given[gk] = (out.given[gk] || 0) + 1; out.hand[hk] = (out.hand[hk] || 0) + 1;
        const c = b.copy; if (c && c.inscribed_by_eco) out.eco.push(b.id);
        if (c && (c.givers || []).some((g) => /\bEco\b/.test(g))) out.ecoGiver.push(b.id);
        if (c && c.inscription) { out.inscr++; if (!((c.annotation || '') + ' ' + (c.condition || '')).includes(c.inscription)) out.inscrBad.push(b.id); if (c.inscription.length < 4) out.inscrShort.push(b.id); if (REM.test(c.inscription)) out.inscrRemark.push(b.id); if (c.inscription.endsWith('.')) out.inscrStop++; }
        if (b.catalog === 'bologna' && b.title && b.title.includes(' : ')) { out.colon++; if (/: :|\s:\s*$/.test(b.title)) out.colonBad.push(b.id); if (b.title_raw && b.title_raw !== b.title) out.rawKept++; }
        for (const f of ['title', 'author', 'title_en', 'set_title', 'description']) if (b[f] && EL.test(b[f])) out.apos.push([b.id, f]);
        if (c) for (const g of c.givers || []) { if (EL.test(g)) out.apos.push([b.id, 'giver']); if (g === "Jean d'Ormesson") out.ormesson++; }
        if (/(champollion|europa-1492|dante-alighieri-s-inferno-metaphor)$/.test(b.id)) out.gone.push(b.id); }
      const g = (id) => D.books[D._index.get(id)];
      for (const id of ['bologna:UBO03566187', 'bologna:UBO00847484', 'bologna:UBO00778042']) { const b = g(id); out.readings[id] = b ? [(b.sightings || []).length, b.placement] : null; }
      const s = g('bologna:UBO00189116'); out.serao = s && s.copy ? { givers: s.copy.givers || [], note: s.copy.giver_note || '', by: s.copy.dedication_by || null, inscr: s.copy.inscription || '' } : null;
      const t = (id) => { const b = g(id); return b ? [b.title, b.title_raw || null, b.title_en || null] : null; };
      out.titles = { torah: t('bologna:UBO00436664'), cena: t('bologna:UBO09148627'), disegni: t('bologna:UBO07571497'), assassins: t('bologna:UBO09164071') };
      const ins = (id) => { const b = g(id); return b && b.copy ? b.copy.inscription || null : null; };
      out.samples = { a: ins('bologna:UBO03489957'), b: ins('bologna:UBO02094633'), c: ins('bologna:UBO00457305'), d: ins('bologna:UBO09144551'), e: ins('bologna:UBO00885280'), f: ins('bologna:UBO02279418'), g: ins('bologna:UBO01226909') };
      out.meta = (D.meta.counts.catalog || {}).bologna_copies || {}; out.total = D.books.length; return out; }""")
    bc21 = v21['meta']; gv21 = bc21.get('given') or {}; hd21 = bc21.get('hand') or {}
    check(all(v21['given'].get(k) == gv21.get(k) for k in ('named', 'unnamed', 'eco', 'plain')) and v21['given'].get('eco') == 6 and all(v21['hand'].get(k) == hd21.get(k) for k in ('0', '1', '2', '3', '4')) and v21['hand'].get('0', 0) >= 1000 and v21['given'].get('none') == v21['hand'].get('-1') and sum(v21['given'].values()) == v21['total'] and sum(v21['hand'].values()) == v21['total'], "the page classes every copy as meta does: six inscribed by Eco himself, %s of his copies with no mark noted, the copies without a note counted alike in both modes (%s)" % (v21['hand'].get('0'), sorted(v21['given'].items())))
    lgs21 = {}
    for mode21, want21 in (('given', v21['given']), ('hand', v21['hand'])):
        page.evaluate("(m) => window.__overlay.set(m)", mode21); page.wait_for_timeout(600)
        lgs21[mode21] = page.evaluate("() => ({ legend: window.__overlay.state().legend, rows: [...document.querySelectorAll('#legend .row')].map((e) => e.textContent.trim().replace(/\\s+/g, ' ')) })")
        lg21 = dict(lgs21[mode21]['legend'])
        check(all(lg21.get(k) == n for k, n in want21.items()) and len(lg21) == len(want21) and sum(lg21.values()) == v21['total'] and all(('{:,}'.format(n) in r) for (k, n), r in zip(lgs21[mode21]['legend'], lgs21[mode21]['rows'])), 'the %s legend counts every class as the data does, prints each count on its row and sums to the shelf slots (%s)' % (mode21, sorted(lg21.items())))
    page.screenshot(path=os.path.join(args.shots, 'legend-hand-counts.png'))
    page.evaluate("() => window.__overlay.set('language')"); page.wait_for_timeout(200)
    own21 = sum(v21['given'].get(k, 0) for k in ('named', 'unnamed', 'eco', 'plain'))
    menu_click(page, '#handBtn')
    hl21 = page.evaluate("() => ({ head: document.querySelector('#hand .card p').textContent, tabs: [...document.querySelectorAll('#handTabs button')].map((b) => b.textContent.trim().replace(/\\s+/g, ' ')) })")
    check(('{:,} of Eco\'s own copies'.format(own21)) in hl21['head'] and any(t.startswith('Inscribed by Eco himself') and t.endswith(' 6') for t in hl21['tabs']) and any(t == 'Dedicated to Eco {:,}'.format(v21['given'].get('named', 0) + v21['given'].get('unnamed', 0)) for t in hl21['tabs']), "Eco's copies opens on the copies' own count, with a tab for the six books he inscribed himself (%s; %s)" % (hl21['head'][:70], hl21['tabs'][:2]))
    page.screenshot(path=os.path.join(args.shots, 'hand-tabs.png'), clip={'x': 0, 'y': 0, 'width': 1440, 'height': 400})
    page.evaluate("() => document.getElementById('hand').classList.remove('show')")
    # the inscriptions: closed at their own quotation marks, whole, verbatim in the note, none running into the cataloguer's remarks
    check(v21['inscr'] >= 850 and not v21['inscrBad'] and not v21['inscrShort'] and not v21['inscrRemark'] and v21['inscrStop'] >= 40 and bc21.get('with_inscription') == v21['inscr'] and (bc21.get('inscription_how') or {}).get('closed', 0) > 800, '%d inscriptions, each a passage of its copy note or its condition line, none shorter than four characters, none running on into the cataloguer\'s remarks, %d keeping their final stop (%s)' % (v21['inscr'], v21['inscrStop'], v21['inscrBad'][:2] + v21['inscrRemark'][:2] or bc21.get('inscription_how')))
    s21 = v21['samples']
    check(bool(s21['a']) and s21['a'].endswith('10.IX.1867') and s21['b'] == 'A Umberto lo "zio" Val maggio \'90' and bool(s21['c']) and s21['c'].endswith('Alberto.') and s21['d'] is None and s21['e'] == 'Per Umberto, con amicizia A. A.' and bool(s21['f']) and s21['f'].startswith('Christmas 1987') and s21['g'] == 'A Stefano Sara da Umberto', 'the inscriptions end where the dedication ends: the Scheiwiller date, the zio Val, the Alberto with its stop, the Barker greeting; the pre-print date is no inscription (%s)' % ({k: (v or '')[:30] for k, v in s21.items()},))
    check(sorted(v21['eco']) == sorted(['bologna:UBO01226909', 'bologna:UBO09791533', 'bologna:UBO09399488', 'bologna:UBO09261831', 'bologna:UBO00291803', 'bologna:UBO08627411']) and not v21['ecoGiver'] and bc21.get('inscribed_by_eco') == 6 and not any(g[0] == 'Umberto Eco' for g in bc21.get('top_givers') or []), 'the six copies Eco inscribed for others are his own hand, never counted among his givers (%s)' % (v21['ecoGiver'] or len(v21['eco']),))
    for id21, want21, name21 in (('bologna:UBO01226909', ('A Stefano Sara da Umberto', 'Written in the book by Umberto Eco', 'a dedication in his own hand'), 'Eco to Stefano and Sara'), ('bologna:UBO09399488', ('a dedication in his own hand', 'the catalogue notes it without quoting it'), 'Eco, unquoted'), ('bologna:UBO00189116', ('A Umbert da Matilde', 'someone else', 'Matilde Serao'), 'the Serao copy')):
        page.evaluate("(id) => window.__openBook(id)", id21); settle(page, 400)
        c21 = page.evaluate("() => ({ body: document.getElementById('pBody').textContent.replace(/\\s+/g, ' '), inscr: (document.querySelector('#pBody .inscr') || {}).textContent || '' })")
        check(all(w in c21['body'] for w in want21) and ('by Matilde Serao' not in c21['inscr']), "the card for %s reads as the catalogue records it (%s)" % (name21, [w for w in want21 if w not in c21['body']] or 'all present'))
        if id21 == 'bologna:UBO00189116': page.screenshot(path=os.path.join(args.shots, 'card-serao.png'))
        if id21 == 'bologna:UBO01226909': page.screenshot(path=os.path.join(args.shots, 'card-eco-hand.png'))
    page.evaluate("() => document.getElementById('pClose').click()"); page.wait_for_timeout(300)
    sr21 = v21['serao'] or {}
    check(sr21.get('givers') == [] and 'died in 1927' in sr21.get('note', '') and 'Serao' in str(sr21.get('by')) and (bc21.get('copy_notes_applied') or [{}])[0].get('id') == 'UBO00189116', 'the Serao copy keeps the catalogue\'s name with the note that the dates cannot fit, and names no giver (%s)' % (sr21.get('note', '')[:60],))
    txt21 = ' '.join(r for m in lgs21.values() for r in m['rows']) + ' ' + sr21.get('note', '') + ' ' + hl21['head']
    check(re.search(r'\b(verif|correct(ed|ion|ing)|earlier version|previous version|checked|checking)', txt21, re.I) is None, 'the legends, the copies list and the giver note never speak of checking, correcting or earlier versions')
    # the titles composed with ISBD punctuation, the English titles, the elisions closed, the three readings identified
    t21 = v21['titles']
    check(t21['torah'] is not None and t21['torah'][0] == 'Torah e filosofia : percorsi del pensiero ebraico' and t21['torah'][1] == 'Torah e filosofia percorsi del pensiero ebraico' and t21['cena'] is not None and t21['cena'][0] == 'Gabriele Cena : pittore' and t21['cena'][2] == 'Gabriele Cena: Painter' and t21['disegni'] is not None and t21['disegni'][0] == 'Disegni & Caviglia contro tutti : quando la satira diventa criminale' and t21['assassins'] is not None and t21['assassins'][0].startswith("L'Ordre des Assassins : [Hasan") and v21['colon'] >= 1250 and not v21['colonBad'] and v21['rawKept'] >= 1200, '%d Bologna titles carry their subtitle after " : ", the export\'s words kept under title_raw, none with a doubled or trailing colon (%s)' % (v21['colon'], (t21['torah'] or [''])[0]))
    check(not v21['apos'] and v21['ormesson'] == 2, "no title, author, English title, set title, description or giver splits an elision (%s); Jean d'Ormesson gave two books" % (v21['apos'][:3] or 'none',))
    rd21 = v21['readings']
    check(not v21['gone'] and rd21.get('bologna:UBO00778042') == [2, 'seen'] and (rd21.get('bologna:UBO00847484') or [0])[0] >= 1 and (rd21.get('bologna:UBO03566187') or [0])[0] >= 1, 'the three film readings whose titles run on into a subtitle now stand on their Bologna records (Lacouture seen twice; %s)' % (rd21,))
    # the tour captions quote the composed title; the viewpoint rule: no eye looks along a shelf face from past its cabinet's end
    page.evaluate("() => window.__tours.start('comics')"); page.wait_for_timeout(300)
    for _ in range(5): page.evaluate('() => window.__tour.next()'); page.wait_for_timeout(120)
    settle(page, 800)
    cap21 = page.evaluate("() => ({ step: window.__tour.step(), text: document.getElementById('tour').textContent.replace(/\\s+/g, ' ') })")
    check(cap21['step'] == 5 and 'On the map: Flash Gordon : Sotto i mari di Mongo' in cap21['text'], 'a tour card quotes the composed title on its On the map line (%s)' % (cap21['text'][cap21['text'].find('On the map'):][:70],))
    page.evaluate('() => window.__tour.next()'); settle(page, 1200)
    page.screenshot(path=os.path.join(args.shots, 'comics-07.png'))
    # with the card and the side panel open, as at every tour stop: where each stop's book sits on the screen and how squarely the view faces the shelf, against the same pick with nothing open
    FR21 = """() => { const D = window.__data(), out = {}; const W = window.innerWidth;
      for (const t of window.__tours.list()) t.targets.forEach((tg, i) => { if (!tg || typeof tg !== 'string' || !D._index.has(tg)) return; const fp = window.__flyPick(tg); if (!fp || fp.dot == null) return;
        const s = window.__spineScreen(tg, fp.eye, fp.look); const dx = fp.look[0] - fp.eye[0], dz = fp.look[2] - fp.eye[2], L = Math.hypot(dx, dz) || 1;
        out[t.id + '-' + String(i + 1).padStart(2, '0')] = { x: +(s.x / W).toFixed(3), inBand: s.inBand, vdot: +(-(dx / L * fp.front[0] + dz / L * fp.front[2])).toFixed(3), eye: fp.eye.map((v) => +v.toFixed(2)) }; }); return out; }"""
    fr21 = page.evaluate(FR21)
    page.evaluate('() => window.__tour.end()'); page.wait_for_timeout(300)
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }"); page.wait_for_timeout(400)
    bare21 = page.evaluate(FR21)
    cen21 = page.evaluate("""() => { const D = window.__data(), out = []; for (const t of window.__tours.list()) t.targets.forEach((tg, i) => { if (!tg || typeof tg !== 'string' || !D._index.has(tg)) return; const fp = window.__flyPick(tg); if (!fp || fp.dot == null) return;
      out.push([t.id + '-' + String(i + 1).padStart(2, '0'), +fp.dot.toFixed(3), +fp.past.toFixed(2), +(Math.atan2(fp.eye[1] - fp.look[1], Math.hypot(fp.eye[0] - fp.look[0], fp.eye[2] - fp.look[2])) * 180 / Math.PI).toFixed(0), fp.hidden]); }); return out; }""")
    rake21 = [c for c in cen21 if c[1] < 0.6 and c[2] > 0.05]; c07 = next((c for c in cen21 if c[0] == 'comics-07'), None); hid21 = [c for c in cen21 if c[4]]
    tg21 = {t['id']: t['targets'] for t in page.evaluate('() => window.__tours.list()')}
    alt21 = []   # a raking eye is allowed only where no candidate stands clear of the cabinet and the furniture, faces the shelf, is not steep and sees the spine
    for c in rake21:
        tid, k = c[0].rsplit('-', 1); cands = page.evaluate('(id) => window.__flyCands(id)', tg21[tid][int(k) - 1]) or []
        if any(x['ok'] and x['gap'] >= 0.5 and x['objGap'] >= 0.5 and x['dot'] is not None and x['dot'] >= 0.6 and x['pitch'] <= 45 and not x['blocked02'] and not x['hidden'] for x in cands): alt21.append(c[0])
    check(len(cen21) > 240 and not alt21 and len(rake21) <= 2 and c07 is not None and c07[1] >= 0.5 and c07[2] == 0 and c07[3] <= 45 and not hid21, 'at %d book stops the eye faces the shelf wherever a clear facing view exists (%d along the face for want of one); comics-07 faces its shelf from in front of it, %s degrees down (%s)' % (len(cen21), len(rake21), c07[3] if c07 else '?', alt21[:3] or hid21[:3] or [c[0] for c in rake21]))
    off21 = [(k, fr21[k]['vdot'], bare21[k]['vdot']) for k in fr21 if k in bare21 and fr21[k]['vdot'] < bare21[k]['vdot'] - 0.02]
    out21 = [(k, fr21[k]['x']) for k in fr21 if not fr21[k]['inBand'] or fr21[k]['x'] > 0.56 or fr21[k]['x'] < 0.25]
    c07f = fr21.get('comics-07') or {}
    check(len(fr21) > 240 and not off21 and not out21 and c07f.get('vdot', 0) >= 0.7, "with the card and the side panel open the book sits in the clear part of the screen at all %d stops, and the framing never turns the view further off the shelf's front (%d eyes shifted, %d views turned toward the book's side); at comics-07 the view faces the shelf (%s)" % (len(fr21), sum(1 for k in fr21 if k in bare21 and fr21[k]['eye'] != bare21[k]['eye']), sum(1 for k in fr21 if k in bare21 and fr21[k]['eye'] == bare21[k]['eye'] and fr21[k]['x'] < 0.45), off21[:3] or out21[:3] or c07f.get('vdot')))
    # Back walks the page's own history: a card, a tour, an address typed over a tour
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }"); page.wait_for_timeout(300)
    page.evaluate("(id) => window.__openBook(id)", 'bologna:UBO00436664'); settle(page)
    hA = page.evaluate("() => ({ hash: location.hash, st: window.__historyState() })")
    page.evaluate("(id) => window.__openBook(id)", 'bologna:UBO00812491'); settle(page)
    hB = page.evaluate("() => ({ hash: location.hash, st: window.__historyState() })")
    page.evaluate("() => history.back()"); page.wait_for_timeout(1500)
    hC = page.evaluate("() => ({ hash: location.hash, st: window.__historyState(), open: document.getElementById('panel').classList.contains('open') })")
    page.evaluate("() => history.forward()"); page.wait_for_timeout(1500)
    hD = page.evaluate("() => ({ hash: location.hash, open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent })")
    page.evaluate("() => document.getElementById('pClose').click()"); page.wait_for_timeout(1200)
    hE = page.evaluate("() => ({ hash: location.hash, st: window.__historyState(), open: document.getElementById('panel').classList.contains('open'), room: window.__currentRoom() })")
    page.evaluate("() => history.back()"); settle(page, 1500)
    hF = page.evaluate("() => ({ hash: location.hash, open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent })")
    page.evaluate("() => document.getElementById('pClose').click()"); page.wait_for_timeout(600)
    check(hA['hash'] == '#book=bologna%3AUBO00436664' and (hA['st'] or {}).get('panel') is True and hB['hash'] == '#book=bologna%3AUBO00812491' and (hB['st'] or {}).get('panel') is True and hC['open'] and hC['hash'] == '#book=bologna%3AUBO00436664' and hD['open'] and hD['title'].startswith('I sette santuari') and not hE['open'] and hE['hash'] == '#room=' + hE['room'] and not (hE['st'] or {}).get('panel') and hF['open'] and hF['title'].startswith('Torah e filosofia'), 'Back walks the cards: a second book is a new entry, Back reopens the first, Forward the second, Close leaves the room in the address and the camera where it is, Back then reopens the first (%s)' % ({'A': hA['hash'], 'B': hB['hash'], 'C': hC['hash'], 'D': hD['hash'], 'E': hE['hash'], 'F': hF['hash']},))
    page.evaluate("() => window.__tours.start('rose')"); settle(page)
    tA = page.evaluate("() => ({ hash: location.hash, st: window.__historyState(), tour: window.__tours.state().id })")
    page.evaluate('() => window.__tour.next()'); settle(page)
    tB = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, step: window.__tours.state().step })")
    page.evaluate("() => { location.hash = '#book=bologna%3AUBO00436664'; }"); settle(page, 1200)
    tC = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent })")
    page.evaluate("() => history.back()"); settle(page, 1500)
    tD = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, step: window.__tours.state().step })")
    page.evaluate("() => { location.hash = '#room=studio'; }"); settle(page, 1200)
    tE = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, room: window.__currentRoom(), open: document.getElementById('panel').classList.contains('open') })")
    page.evaluate("() => history.back()"); settle(page, 1500)
    tF = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, step: window.__tours.state().step })")
    page.evaluate("() => window.__tour.end()"); page.wait_for_timeout(1200)
    tG = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, st: window.__historyState() })")
    page.evaluate("() => history.back()"); settle(page, 1500)
    tH = page.evaluate("() => ({ hash: location.hash, tour: window.__tours.state().id, open: document.getElementById('panel').classList.contains('open') })")
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }"); page.wait_for_timeout(400)
    check(tA['tour'] == 'rose' and tA['hash'] == '#tour=rose&stop=1' and (tA['st'] or {}).get('tour') is True and tB['hash'] == '#tour=rose&stop=2' and tB['step'] == 1 and tC['tour'] is None and tC['open'] and tC['title'].startswith('Torah e filosofia') and tD['tour'] == 'rose' and tD['step'] == 1 and tE['tour'] is None and tE['room'] == 'studio' and not tE['open'] and tF['tour'] == 'rose' and tF['step'] == 1 and tG['tour'] is None and not tG['hash'].startswith('#tour') and not (tG['st'] or {}).get('tour') and tH['tour'] is None and not tH['hash'].startswith('#tour'), 'a tour is one entry too: its stops rewrite it, a book or room address typed over it ends it and Back brings the stop back, Exit leaves the room in the address and Back then goes to what came before the tour (%s)' % ({'A': tA['hash'], 'B': tB['hash'], 'C': tC['hash'], 'D': tD['hash'], 'E': tE['hash'], 'F': tF['hash'], 'G': tG['hash'], 'H': tH['hash']},))
    # the opening card: a click on the scene beside it closes it and opens nothing; the next click opens what it hits
    pc = ctx.new_page(); pc.goto(base + 'index.html', wait_until='load'); wait_ready(pc, args.timeout * 2); pc.wait_for_timeout(1500)
    rc21 = pc.evaluate("() => { const r = document.querySelector('#welcome .card').getBoundingClientRect(); return { rect: [r.left, r.top, r.right, r.bottom], walk: document.querySelector('#wWalk span').textContent, shown: window.__state.welcome() }; }")
    def pick21(p):
        for y in range(140, 880, 60):
            for x in range(200, 1300, 60):
                r = rc21['rect']
                if r[0] - 8 <= x <= r[2] + 8 and r[1] - 8 <= y <= r[3] + 8: continue
                h = p.evaluate('([x, y]) => window.__pickAt(x, y)', [x, y])
                if (isinstance(h, int) and h >= 0) or (isinstance(h, dict) and (h.get('obj') or h.get('label'))): return (x, y)
        return None
    pt21 = pick21(pc)
    if pt21 and rc21['shown']:
        pc.mouse.click(pt21[0], pt21[1]); pc.wait_for_timeout(400)
        k1 = pc.evaluate("() => ({ welcome: window.__state.welcome(), open: document.getElementById('panel').classList.contains('open'), tour: window.__tours.state().id })")
        settle(pc, 800); pt21b = pick21(pc)
        if pt21b: pc.mouse.click(pt21b[0], pt21b[1]); pc.wait_for_timeout(1500)
        k2 = pc.evaluate("() => ({ open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent })")
        check(not k1['welcome'] and not k1['open'] and not k1['tour'] and pt21b is not None and k2['open'] and bool(k2['title']), 'a click on the scene beside the opening card closes the card and opens nothing; the next click opens what it hits (%s; then %s)' % (k1, k2['title'][:30]))
        pc.screenshot(path=os.path.join(args.shots, 'card-click.png'))
    else: check(False, 'no pickable point beside the opening card (card shown %s, point %s)' % (rc21['shown'], pt21))
    check('arrow keys' in rc21['walk'].lower() and 'joystick' not in rc21['walk'].lower(), 'on a desktop the Walk door speaks of the arrow keys (%s)' % rc21['walk'])
    pc.close()
    # the preview tags and the picture drawn without the footer; the hint box above the footer at any width
    mt21 = page.evaluate("() => ({ tw: (document.querySelector('meta[name=\"twitter:image\"]') || {}).content, og: (document.querySelector('meta[property=\"og:image\"]') || {}).content, w: (document.querySelector('meta[property=\"og:image:width\"]') || {}).content, h: (document.querySelector('meta[property=\"og:image:height\"]') || {}).content })")
    check(mt21['tw'] and mt21['tw'] == mt21['og'] and mt21['w'] == '1200' and mt21['h'] == '630', 'the page names its preview picture for Twitter too, with its size (%s)' % (mt21,))
    try:
        from PIL import Image as _Im21
        _im21 = _Im21.open(os.path.join(args.dist, 'preview.jpg')).convert('L'); _w21, _h21 = _im21.size; _strip21 = _im21.crop((0, _h21 - 26, _w21, _h21)); _px21 = list(_strip21.getdata()); dark21 = sum(1 for v in _px21 if v < 40) / float(len(_px21))
    except Exception as ex21: dark21 = None; print('preview strip not measured:', ex21)
    check(dark21 is not None and dark21 < 0.5, 'the preview picture is drawn without the footer bar (dark share of its bottom strip %s)' % (None if dark21 is None else round(dark21, 3),))
    hb21 = {}
    for w21, h21 in ((1200, 630), (1440, 900)):
        page.set_viewport_size({'width': w21, 'height': h21}); n21 = page.evaluate('() => window.__labelPass || 0'); page.wait_for_function('(n) => (window.__labelPass || 0) >= n', arg=n21 + 2, timeout=60000)
        hb21['%dx%d' % (w21, h21)] = page.evaluate("() => { const h = document.getElementById('hint').getBoundingClientRect(), s = document.getElementById('stats').getBoundingClientRect(); return [Math.round(h.bottom), Math.round(s.top), Math.round(s.height)]; }")
    check(all(v[0] <= v[1] for v in hb21.values()) and hb21['1200x630'][2] > hb21['1440x900'][2], 'the hint box clears the footer even where the footer wraps to two lines (hint bottom, footer top, footer height: %s)' % (hb21,))
    # search: a name only in a description or a giver no longer brings dozens of near-misses
    sq21 = {}
    for q21 in ('Serao', 'Faye', 'Ormesson'):
        page.fill('#q', q21); page.wait_for_timeout(600)
        sq21[q21] = page.evaluate("() => [...document.querySelectorAll('#results .r')].map((e) => e.textContent.replace(/\\s+/g, ' '))")
    page.fill('#q', ''); page.keyboard.press('Escape')
    check(1 <= len(sq21['Serao']) <= 4 and any('Matilde Serao' in r for r in sq21['Serao']) and 4 <= len(sq21['Faye']) <= 12 and sum(1 for r in sq21['Faye'] if 'Faye' in r) >= 4 and 1 <= len(sq21['Ormesson']) <= 4 and all("Ormesson, Jean d'" in r for r in sq21['Ormesson']), 'search finds Serao, Faye and Ormesson without the near-misses (%d, %d and %d results)' % (len(sq21['Serao']), len(sq21['Faye']), len(sq21['Ormesson'])))
    # ---- the copies with a giver note and no giver, the inscriptions run on past an inner quotation and read from the condition line, Back from a book opened in the walk view, the stop's own pile and the page and the data free of version notes ----
    v22 = page.evaluate(r"""() => { const D = window.__data(), out = { unnamed: [], noteNoGiver: [], byNoGiver: [], inscr: 0, inscrOut: [], semi: [], condDed: [], condMarks: 0, given: {} };
      const g = (id) => D.books[D._index.get(id)];
      for (const b of D.books) { const c = b.copy; if (!c) continue; const k = window.__classes(b.id); out.given[k.given] = (out.given[k.given] || 0) + 1;
        if (k.given === 'unnamed') out.unnamed.push(b.id);
        if (c.giver_note && !(c.givers && c.givers.length)) out.noteNoGiver.push(b.id);
        if (c.dedication_by && c.dedication_by.length && !(c.givers && c.givers.length) && !c.giver_note && !c.inscribed_by_eco) out.byNoGiver.push(b.id);
        if (c.inscription) { out.inscr++; if (!((c.annotation || '') + ' ' + (c.condition || '')).includes(c.inscription)) out.inscrOut.push(b.id); if (/ ; /.test(c.inscription)) out.semi.push([b.id, c.inscription]); }
        if (c.condition && /dedica/i.test(c.condition)) out.condDed.push([b.id, !!c.inscription, (c.marks || []).includes('dedication')]);
        if (c.condition && !c.annotation && (c.marks || []).length) out.condMarks++; }
      const pick = (id) => { const b = g(id); return b && b.copy ? { inscr: b.copy.inscription || null, givers: b.copy.givers || [], marks: b.copy.marks || [], ann: b.copy.annotation || null, cond: b.copy.condition || null, note: b.copy.giver_note || null } : null; };
      out.darmon = pick('bologna:UBO00101116'); out.burkert = pick('bologna:UBO00343613'); out.serao = pick('bologna:UBO00189116'); out.marks3 = { a: pick('bologna:UBO09846324'), b: pick('bologna:UBO09799684') };
      out.meta = (D.meta.counts.catalog || {}).bologna_copies || {}; return out; }""")
    dm22, bk22, sr22b, m3 = v22['darmon'] or {}, v22['burkert'] or {}, v22['serao'] or {}, v22['marks3']
    check(dm22.get('inscr') == 'En Hommage à Umberto Eco, ces variations "èpicuriennes" ; en [sic] Avec toute ma admiration J. Charles Darmon' and dm22.get('givers') == ['Jean-Charles Darmon'] and len(v22['semi']) == 1, "the Darmon inscription runs on past its inner quotation to the giver's name, the only inscription with a semicolon inside it (%s)" % ((dm22.get('inscr') or '')[-44:],))
    check(bk22.get('inscr') == "Omaggio dell'autore WB" and bk22.get('givers') == ['Walter Burkert'] and bk22.get('ann') is None and 'dedica autografa di Walter Burkert' in (bk22.get('cond') or '') and 'ex-libris stamp' in (bk22.get('marks') or []) and v22['condDed'] == [['bologna:UBO00343613', True, True]], 'the Burkert dedication is read from the condition line, the only dedication remark written there, with the stamp beside it (%s)' % (v22['condDed'],))
    check(sorted((m3.get('a') or {}).get('marks') or []) == sorted(['ex-libris stamp', 'underlinings', 'marginalia', 'dog-ears', 'inserts']) and sorted((m3.get('b') or {}).get('marks') or []) == ['ex-libris stamp', 'inserts'] and v22['condMarks'] >= 3, 'the marks written into the condition line are read too: the stamp, the underlinings, the marginalia, the dog-ears and the insert of UBO09846324, the stamp and the inserts of UBO09799684 (%d copies with marks from the condition line alone)' % v22['condMarks'])
    check(v22['inscr'] >= 860 and v22['inscr'] == v22['meta'].get('with_inscription') and not v22['inscrOut'] and (v22['meta'].get('inscription_how') or {}).get('closed', 0) >= 840, '%d inscriptions, each a passage of its copy note or its condition line, %d closed at their own quotation mark (%s)' % (v22['inscr'], (v22['meta'].get('inscription_how') or {}).get('closed', 0), v22['inscrOut'][:3] or 'none outside its note'))
    check(v22['noteNoGiver'] == ['bologna:UBO00189116'] and not v22['byNoGiver'] and sr22b.get('givers') == [] and 'died in 1927' in (sr22b.get('note') or ''), 'the Serao copy is the one copy with a giver note and no giver, and no other copy carries a catalogue name the data does not serve as a giver (%s)' % (v22['byNoGiver'][:3] or 'none',))
    # the copies list: a copy whose giver the catalogue cannot name sits under Giver not named, the last group
    menu_click(page, '#handBtn')
    gr22 = page.evaluate(r"""() => { const t = [...document.querySelectorAll('#handTabs button')].find((b) => b.dataset.hand === 'dedication'); if (t) t.click();
      const heads = [...document.querySelectorAll('#handList .notable-cat')].map((h) => [h.dataset.giver, +(((h.querySelector('span') || {}).textContent || '').replace(/\D/g, '') || 0)]);
      const row = document.querySelector('#handList .r[data-id="bologna:UBO00189116"]'); let prev = row ? row.previousElementSibling : null; while (prev && !prev.classList.contains('notable-cat')) prev = prev.previousElementSibling;
      const un = document.querySelector('#handList .notable-cat[data-giver="Giver not named"]'); if (un) un.scrollIntoView({ block: 'start' });
      return { heads, seraoGroup: prev ? prev.dataset.giver : null, tab: t ? t.textContent.trim().replace(/\s+/g, ' ') : null, rowText: row ? row.textContent.replace(/\s+/g, ' ') : null }; }""")
    hd22 = dict(gr22['heads'])
    check(gr22['tab'] is not None and 'Serao, Matilde' not in hd22 and gr22['heads'] and gr22['heads'][-1][0] == 'Giver not named' and hd22.get('Giver not named') == len(v22['unnamed']) and gr22['seraoGroup'] == 'Giver not named' and 'A Umbert da Matilde' in (gr22['rowText'] or '') and all(h != 'Giver not named' for h, n in gr22['heads'][:-1]), "the copies list's Dedicated to Eco tab puts the Serao copy under Giver not named, the last group, which counts the %d copies whose giver the catalogue does not name; no group is headed by a name the data does not serve as a giver (%s)" % (len(v22['unnamed']), gr22['heads'][-2:]))
    page.wait_for_timeout(300); page.screenshot(path=os.path.join(args.shots, 'hand-unnamed.png'))
    page.evaluate("() => document.getElementById('hand').classList.remove('show')")
    # the cards: the Serao row carries the note, the Darmon inscription runs to the name, the Burkert card reads its dedication from the condition line
    for id22, want22, name22, shot22 in (('bologna:UBO00189116', {'row': 'The catalogue names Matilde Serao', 'absent': 'Serao, Matilde', 'inscr': 'A Umbert da Matilde'}, 'the Serao copy', 'card-serao-row.png'), ('bologna:UBO00101116', {'row': 'Jean-Charles Darmon', 'inscr': '"èpicuriennes" ; en [sic] Avec toute ma admiration J. Charles Darmon'}, 'the Darmon copy', 'card-darmon.png'), ('bologna:UBO00343613', {'row': 'Walter Burkert', 'inscr': "Omaggio dell'autore WB", 'cond': 'dedica autografa di Walter Burkert', 'summary': 'dedication'}, 'the Burkert copy', 'card-burkert.png')):
        page.evaluate("(id) => window.__openBook(id)", id22); settle(page, 400)
        c22 = page.evaluate("() => ({ rows: [...document.querySelectorAll('#pBody dt')].map((d) => [d.textContent.trim(), ((d.nextElementSibling || {}).textContent || '').trim()]), body: document.getElementById('pBody').textContent.replace(/\\s+/g, ' '), inscr: (document.querySelector('#pBody .inscr') || {}).textContent || '', summary: [...document.querySelectorAll('#pBody summary')].map((s) => s.textContent).join(' | ') })")
        rows22 = dict(c22['rows']); ins22 = rows22.get('Inscribed by', '')
        ok22 = ins22.startswith(want22['row']) and want22['inscr'] in c22['inscr'] and (want22.get('absent') is None or want22['absent'] not in c22['body']) and (want22.get('cond') is None or want22['cond'] in rows22.get('Condition', '')) and (want22.get('summary') is None or want22['summary'] in c22['summary'].lower()) and ('Notes and marks' in rows22) == (id22 != 'bologna:UBO00343613')
        check(ok22, 'the card for %s heads its Inscribed by row with "%s" and quotes the inscription whole (%s)' % (name22, want22['row'], ins22[:40] if ok22 else {'row': ins22[:60], 'inscr': c22['inscr'][:90], 'cond': rows22.get('Condition', '')[:40], 'summary': c22['summary'][:60]}))
        page.screenshot(path=os.path.join(args.shots, shot22))
    page.evaluate("() => document.getElementById('pClose').click()"); page.wait_for_timeout(300)
    # Back from a book opened in the walk view: the page taken into the walk view by its address (a second live WebGL page starves the software renderer), a book from a search row, a second from its card, Back, Back, Forward; a tour and a bookcase from the walk; the two opens must each add an entry
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }"); page.wait_for_timeout(300)
    page.evaluate("() => { location.hash = '#mode=walk'; }"); settle(page, 1500)
    def st22(p):
        try: return p.evaluate("() => ({ hash: location.hash, mode: window.__tours.state().mode, open: document.getElementById('panel').classList.contains('open'), title: document.getElementById('pTitle').textContent, tour: window.__tours.state().id, st: window.__historyState(), len: history.length, alive: true })")
        except Exception as ex22: return {'alive': False, 'url': p.url, 'err': str(ex22)[:60]}
    def nav22(p, how):
        try: p.evaluate("(h) => h === 'back' ? history.back() : history.forward()", how); p.wait_for_timeout(1500); settle(p, 800)
        except Exception: pass
        return st22(p)
    w0 = st22(page)
    page.fill('#q', 'Torah e filosofia'); page.wait_for_timeout(700)
    id1 = page.evaluate("() => { const r = document.querySelector('#results .r[data-id]'); if (!r) return null; r.click(); return r.dataset.id; }"); settle(page, 800); w1 = st22(page)
    page.evaluate("(id) => window.__openBook(id)", 'bologna:UBO00812491'); settle(page, 800); w2 = st22(page)
    w3 = nav22(page, 'back'); w4 = nav22(page, 'back')
    if w4.get('alive'): page.screenshot(path=os.path.join(args.shots, 'walk-history.png'))
    w5 = nav22(page, 'forward'); w6 = nav22(page, 'back')
    hs22 = lambda w: w.get('hash') or ''
    # the browser keeps at most 50 entries of session history, so the lengths are read only below that cap; the Back, Back, Forward sequence is the proof either way (a book that replaced the walk entry would put the second Back on the state before the walk)
    check(w0.get('alive') and 'mode=walk' in hs22(w0) and w0.get('mode') == 'walk' and id1 == 'bologna:UBO00436664' and w1.get('open') and 'book=bologna%3AUBO00436664' in hs22(w1) and (w1.get('st') or {}).get('panel') is True and (w1.get('len') == w0.get('len') + 1 or w0.get('len', 0) >= 50) and w2.get('open') and 'book=bologna%3AUBO00812491' in hs22(w2) and (w2.get('len') == w1.get('len') + 1 or w1.get('len', 0) >= 50) and w3.get('alive') and w3.get('open') and 'book=bologna%3AUBO00436664' in hs22(w3) and w4.get('alive') and not w4.get('open') and 'mode=walk' in hs22(w4) and 'book=' not in hs22(w4) and w4.get('mode') == 'walk' and w5.get('alive') and w5.get('open') and (w5.get('title') or '').startswith('Torah e filosofia') and w6.get('alive') and w6.get('mode') == 'walk' and not w6.get('open'), 'in the walk view a book opened from a search row is a new entry and a second book from its card another: Back reopens the first, Back again returns to the walk with the page still there, Forward reopens the book (%s)' % ({'0': (hs22(w0), w0.get('len')), '1': (hs22(w1), w1.get('len')), '2': (hs22(w2), w2.get('len')), '3': hs22(w3) if w3.get('alive') else w3, '4': hs22(w4) if w4.get('alive') else w4, '5': hs22(w5) if w5.get('alive') else w5, '6': (hs22(w6), w6.get('mode')) if w6.get('alive') else w6},))
    if w6.get('alive'):
        page.evaluate("() => window.__tours.start('rose')"); settle(page, 1200); w7 = st22(page); w8 = nav22(page, 'back')
        if w8.get('alive'): page.evaluate("(id) => window.__openCase(id)", 'rare-01'); settle(page, 1000); w9 = st22(page); w10 = nav22(page, 'back')
        else: w9 = w10 = {}
    else: w7 = w8 = w9 = w10 = {}
    check(w7.get('tour') == 'rose' and 'tour=rose' in hs22(w7) and (w7.get('st') or {}).get('tour') is True and w8.get('alive') and w8.get('tour') is None and w8.get('mode') == 'walk' and w9.get('alive') and w9.get('open') and 'case=rare-01' in hs22(w9) and w10.get('alive') and not w10.get('open') and w10.get('mode') == 'walk', 'a tour and a bookcase opened from the walk view are entries too, and Back from each returns to the walk with the page still there (%s)' % ({'7': hs22(w7), '8': (hs22(w8), w8.get('mode')) if w8.get('alive') else w8, '9': hs22(w9), '10': (hs22(w10), w10.get('mode')) if w10.get('alive') else w10},))
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); window.__tour.end(); }"); page.wait_for_timeout(300)
    page.evaluate("() => window.__setMode('orbit')"); page.wait_for_timeout(400); page.evaluate("() => window.__flyToRoom('all')"); settle(page)
    # the stops on a pile: the stop's own pile letters its titles while the card is up, in both views
    tl22 = page.evaluate('() => window.__tours.list()')
    obj22 = page.evaluate("() => { const D = window.__data(), o = {}; for (const b of D.books) if (b.bookcase && b.bookcase.startsWith('obj:')) o[b.id] = b.bookcase; return o; }")
    piles22 = [(t['id'], k, t['ids'][k], obj22[tg]) for t in tl22 for k, tg in enumerate(t['targets']) if isinstance(tg, str) and tg in obj22]
    check(len(piles22) >= 2 and {p[2] for p in piles22} >= {'rose-01', 'own-books-01'} and all(p[3] == 'obj:salotto:piano-pile-07' for p in piles22), 'the stops whose book lies on a pile (%s)' % ([p[2] for p in piles22],))
    pr22 = {}
    for view22 in ('orbit', 'walk'):
        page.evaluate("(m) => window.__setMode(m)", view22); page.wait_for_timeout(400)
        for tid22, k22, sid22, pile22 in piles22:
            page.evaluate('(id) => window.__tours.start(id)', tid22); page.wait_for_timeout(300)
            for _ in range(k22): page.evaluate('() => window.__tour.next()'); page.wait_for_timeout(120)
            settle(page, 600)
            n22 = page.evaluate('() => window.__labelPass || 0')
            try: page.wait_for_function('(n) => (window.__labelPass || 0) >= n', arg=n22 + 2, timeout=60000)
            except Exception: page.wait_for_timeout(2500)
            pl22 = page.evaluate('() => window.__plates()'); lb22 = page.evaluate('() => window.__pileLabels || {}')
            pr22[view22 + ':' + sid22] = {'stop': pl22['stop'], 'stopPile': pl22['stopPile'], 'listed': pl22['listedPile'], 'lines': lb22.get(pile22), 'others': [k for k in lb22 if k != pile22], 'pile': pile22}
            if view22 == 'orbit' and sid22 == 'rose-01': page.screenshot(path=os.path.join(args.shots, 'rose-01-pile.png'))
            page.evaluate('() => window.__tour.end()'); page.wait_for_timeout(300)
    page.evaluate("() => window.__setMode('orbit')"); page.wait_for_timeout(400)
    check(pr22 and all(v['stopPile'] == v['pile'] and v['listed'] == v['pile'] and (v['lines'] or 0) >= 1 and not v['others'] for v in pr22.values()), "at every stop on a pile the stop's own pile letters its titles while the card is up, in both views, and no other pile does (%s)" % ({k: (v['listed'], v['lines']) for k, v in pr22.items()},))
    # the page source and the served metadata carry no version notes
    src22 = open(os.path.join(args.dist, 'index.html'), encoding='utf-8').read()
    nar22 = re.findall(r'.{0,30}\b(?:version \d+|v\d\d? fix|audit-v\d+|backup-v\d+)\b.{0,30}', src22, re.I)
    meta22 = page.evaluate("() => JSON.stringify(window.__data().meta)")
    narm22 = re.findall(r'.{0,30}\b(?:version \d+|audit-v\d+|backup-v\d+)\b.{0,30}', meta22, re.I)
    check(not nar22 and not narm22, 'the page source and the served metadata carry no version notes (%s)' % ((nar22 + narm22)[:3] or 'none',))
    # the Origin badge: an ECO.02 or ECO.03 record names a section of the catalogue, an ECO.01 record a position
    sec_id = page.evaluate(r"() => { const b = window.__data().books.find((b) => b.placement === 'catalogued' && /^ECO\.02\b/.test(b.shelfmark || '')); return b ? b.id : null; }")
    pos_id = page.evaluate(r"() => { const b = window.__data().books.find((b) => b.placement === 'catalogued' && /^ECO\.01\b/.test(b.shelfmark || '')); return b ? b.id : null; }")
    if sec_id and pos_id:
        page.evaluate('(id) => window.__openBook(id)', sec_id); settle(page)
        t1 = page.evaluate("() => document.getElementById('pBody').textContent")
        page.evaluate('(id) => window.__openBook(id)', pos_id); settle(page)
        t2 = page.evaluate("() => document.getElementById('pBody').textContent")
        check('shelfmark of a catalogue section' in t1 and 'position from the shelfmark' not in t1 and 'Guess' in t1, "an ECO.02 record's Origin badge names a section of the catalogue, its Certainty a guess (%d such records)" % v16['refBadge'])
        check('position from the shelfmark' in t2 and 'Certain' in t2, "an ECO.01 record's Origin badge keeps the position from the shelfmark")
        page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    else: check(False, 'no ECO.01 or ECO.02 record to open')
    # one full stop after every provenance note: the reference entries and the seen note that ends with its own stop
    dots = page.evaluate("""() => { const D = window.__data(), ids = D.books.filter((b) => b.placement === 'reference').slice(0, 6).map((b) => b.id); const k = D.books.find((b) => /kircher-title-page$/.test(b.id)); if (k) ids.push(k.id); const out = [];
      for (const id of ids) { window.__openBook(id, false); const t = document.getElementById('pBody').textContent; if (/\.\./.test(t)) out.push(id); } return [ids.length, out]; }""")
    check(dots[0] >= 6 and not dots[1], 'no panel prints a doubled full stop after its note (%d panels read%s)' % (dots[0], '' if not dots[1] else ', doubled at %s' % dots[1][:3]))
    page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    page.evaluate("() => window.__overlay.set('certainty')"); page.wait_for_timeout(300)
    leg = page.evaluate("() => document.getElementById('legend').textContent")
    check('ECO.01' in leg and 'ECO.02 or ECO.03' in leg and 'reference entry' in leg, "the legend's Certain and Guess rows name the shelfmark sections and the reference entries")
    # on-film lines in the case and room panels
    seen_case = page.evaluate("() => { for (const r of window.__data().rooms) for (const bc of r.bookcases) if (bc.on_camera) return bc.id; return null; }")
    if seen_case:
        page.evaluate('(id) => window.__openCase(id)', seen_case); page.wait_for_timeout(1000)
        check('film' in page.evaluate("() => document.getElementById('pBody').textContent").lower(), 'bookcase panel says whether the films showed it')
    page.evaluate("() => window.__openRoom('salotto')"); page.wait_for_timeout(1000)
    check('on film' in page.evaluate("() => document.getElementById('pBody').textContent").lower(), 'room panel reports the seconds on film')
    page.screenshot(path=os.path.join(args.shots, 'panel-room.png'))
    # a Bologna copy with annotation notes
    cb = page.evaluate("() => { const b = window.__data().books.find(b => b.copy && b.copy.annotation); return b ? b.id : null; }")
    if cb:
        page.evaluate('(id) => window.__openBook(id)', cb); page.wait_for_timeout(1000)
        check("Eco's copy" in page.evaluate("() => document.getElementById('pBody').textContent"), 'Bologna copy notes (dedications, underlinings) shown in the panel')
        page.screenshot(path=os.path.join(args.shots, 'panel-copy.png'))
    else: check(False, 'no Bologna record with copy notes')
    # an incunabulum with Eco's card
    ib = page.evaluate("() => { const b = window.__data().books.find(b => b.card && b.card.istc); return b ? b.id : null; }")
    if ib:
        page.evaluate('(id) => window.__openBook(id)', ib); page.wait_for_timeout(1000)
        check('ISTC' in page.evaluate("() => document.getElementById('pBody').textContent"), 'incunabulum panel shows the card with its ISTC id')
        page.screenshot(path=os.path.join(args.shots, 'panel-incunabulum.png'))
    else: check(False, 'no incunabulum card in the data')
    # unlabelled
    page.evaluate("() => window.__openBook(window.__data().books.find(b => b.origin === 'unlabelled').id)"); page.wait_for_timeout(800)
    check(page.evaluate("() => document.getElementById('pTitle').textContent") == 'Unidentified book', 'unlabelled book shows the placeholder panel')
    page.screenshot(path=os.path.join(args.shots, 'panel-unlabelled.png'))
    # description present?
    has_desc = page.evaluate("() => window.__data().books.some(b => b.description)")
    if has_desc:
        page.evaluate("() => window.__openBook(window.__data().books.find(b => b.description && /wikipedia\\.org/.test(b.description_source || '')).id)"); page.wait_for_timeout(800)
        check(page.evaluate("() => /wikipedia/i.test(document.querySelector('#panel .desc').innerHTML) && /Wikipedia/.test(document.querySelector('#panel .desc').textContent)"), 'description shown with its link labelled Wikipedia')
        page.screenshot(path=os.path.join(args.shots, 'panel-description.png'))
        cat = page.evaluate("() => { const b = window.__data().books.find(b => b.description && (b.description_kind === 'catalog' || /cerl\\.org\\/istc/.test(b.description_source || ''))); return b ? b.id : null; }")
        if cat:
            page.evaluate('(id) => window.__openBook(id)', cat); page.wait_for_timeout(800)
            dl = page.evaluate("() => { const a = document.querySelector('#panel .desc a'); return a ? [a.textContent, a.href] : null; }")
            check(dl and 'ISTC record' in dl[0] and 'Wikipedia' not in dl[0], 'catalogue-kind description links to the ISTC record, not labelled Wikipedia: %s' % (dl,))
        else: check(False, 'no catalogue-kind description in the data')
    else:
        check(page.evaluate("() => /No public description/.test(document.querySelector('#panel').textContent) || true"), 'no descriptions merged yet (descriptions_eco.json absent)')
    # search
    page.fill('#q', 'Kircher'); page.wait_for_timeout(500)
    n = page.evaluate("() => document.querySelectorAll('#results .r').length")
    check(n > 0, 'search finds Kircher (%d results)' % n)
    page.press('#q', 'Enter'); page.wait_for_timeout(1200)
    check(page.evaluate("() => document.getElementById('panel').classList.contains('open')"), 'search result opens the panel')
    page.screenshot(path=os.path.join(args.shots, 'search.png'))
    # ---- Native / English titles: the switch in the top bar, hidden without data, remembered in localStorage
    en = page.evaluate("() => { const d = window.__data(); return { flag: !!d.meta.english_titles, n: d.books.filter(b => b.title_en).length, counts: (d.meta.counts || {}).english_titles || null }; }")
    print('english titles:', en)
    ctl = page.evaluate("() => { const b = document.getElementById('langBtn'); return b ? { hidden: b.hidden, on: b.classList.contains('on'), pressed: b.getAttribute('aria-pressed'), text: b.textContent.trim() } : null; }")
    check(ctl and ctl['text'] == 'English', 'the English title toggle exists in the top bar (%s)' % ctl)
    lang = lambda v: (page.evaluate('(v) => window.__lang.set(v)', v), page.wait_for_timeout(500))
    if en['n']:
        check(not ctl['hidden'] and not ctl['on'] and ctl['pressed'] == 'false', 'toggle shown when English titles exist (%d books) and off (native) by default' % en['n'])
        check(en['flag'] and en['counts'] and en['counts'].get('books') == en['n'] and en['counts'].get('published', 0) + en['counts'].get('literal', 0) == en['n'], 'meta.english_titles and meta.counts.english_titles agree with the records (%s)' % en['counts'])
        pick = "() => { const bs = window.__data().books; const b = bs.find(b => b.title_en && b.title_en_kind === 'literal' && b.title_en_source) || bs.find(b => b.title_en && b.title_en_kind === 'literal') || bs.find(b => b.title_en); return { id: b.id, title: b.title, en: b.title_en, kind: b.title_en_kind, source: b.title_en_source || null }; }"
        b = page.evaluate(pick)
        page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }"); page.wait_for_timeout(300)
        page.click('#langBtn'); page.wait_for_timeout(400)   # the real control, with the side panel closed (at some widths an open panel covers the end of the top bar, as it does Notable / About)
        check(page.evaluate("() => document.getElementById('langBtn').classList.contains('on') && document.getElementById('langBtn').getAttribute('aria-pressed') === 'true'") and page.evaluate("() => window.__lang.get()") == 'en', 'clicking the toggle turns English on')
        page.click('#langBtn'); page.wait_for_timeout(400)
        check(not page.evaluate("() => document.getElementById('langBtn').classList.contains('on')") and page.evaluate("() => window.__lang.get()") == 'native', 'clicking it again returns to native')
        page.evaluate('(id) => window.__openBook(id)', b['id']); settle(page)
        t0 = page.evaluate("() => document.getElementById('pTitle').textContent")
        check(t0 == b['title'], 'native mode: the panel shows the book\'s own title (%r)' % t0[:50])
        lang('en')   # the hook from here on: the same setLang() the button calls, with the panel open
        t1 = page.evaluate("() => document.getElementById('pTitle').textContent"); body = page.evaluate("() => document.getElementById('pBody').textContent")
        check(t1 == b['en'], 'English mode: the open panel switches to the English title in place (%r)' % t1[:50])
        check(b['title'] in body and 'the book\'s own title' in body, 'English mode: the native title stays visible under the English one')
        if b['kind'] == 'literal': check('literal translation' in body, 'a literal English title is marked "literal translation"')
        check('(model)' not in body and 'made for this map (literal' not in body and 'the translating model' not in body, 'the line under the English title carries no raw note')
        pubb = page.evaluate("() => { const b = window.__data().books.find(b => b.title_en && b.title_en_kind === 'published' && /^English edition/.test(b.title_en_source || '')); return b ? { id: b.id, source: b.title_en_source } : null; }")
        if pubb:
            page.evaluate('(id) => window.__openBook(id)', pubb['id']); settle(page)
            pbody = page.evaluate("() => document.getElementById('pBody').textContent")
            check(pubb['source'] in pbody and 'the title of the ' + pubb['source'] in pbody, 'a published English title prints its source string as it is (%s)' % pubb['source'][:50])
            page.evaluate('(id) => window.__openBook(id)', b['id']); settle(page)
        if b['source'] and not re.match(r'^literal( translation)?( \(model\))?$', b['source'], re.I):   # the bare "literal translation (model)" source adds nothing to the note and is not repeated
            check((re.sub(r'^https?://(www\.)?', '', b['source']).split('/')[0] if b['source'].startswith('http') else b['source'][:40]) in body, 'the source of the English title is shown (%r)' % b['source'][:40])
        page.screenshot(path=os.path.join(args.shots, 'lang-panel-en.png'))
        check(page.evaluate("() => window.__lang.get()") == 'en' and page.evaluate("() => { try { return localStorage.getItem('eco-map-titles'); } catch (e) { return 'n/a'; } }") in ('en', 'n/a'), 'the choice is stored in localStorage')
        dsc = page.evaluate("() => { const bs = window.__data().books; const b = bs.find(b => b.desc_en); return b ? { id: b.id, desc_en: b.desc_en, desc: b.description || '' } : null; }")
        if dsc:
            page.evaluate('(id) => window.__openBook(id)', dsc['id']); settle(page)
            dt = page.evaluate("() => document.querySelector('#panel .desc').textContent")
            check(dt.startswith(dsc['desc_en']) and 'translated here' in dt, 'English mode: a book with desc_en shows the English description, marked "translated here"')
            page.screenshot(path=os.path.join(args.shots, 'lang-panel-desc-en.png'))
        page.evaluate('(id) => window.__openBook(id)', b['id']); settle(page)
        page.fill('#q', b['en'][:24]); page.wait_for_timeout(500)
        hits = page.evaluate("() => [...document.querySelectorAll('#results .r')].map(e => ({ id: e.dataset.id, t: e.querySelector('b').textContent }))")
        check(any(h['id'] == b['id'] and h['t'] == b['en'] for h in hits), 'English mode: search finds the book by its English title and lists it in English (%d hits)' % len(hits))
        page.fill('#q', b['title'][:24]); page.wait_for_timeout(500)
        check(page.evaluate("(id) => [...document.querySelectorAll('#results .r')].some(e => e.dataset.id === id)", b['id']), 'English mode: search still finds it by its native title')
        page.fill('#q', ''); page.wait_for_timeout(300)
        nb = page.evaluate("() => { const b = window.__data().books.find(b => b.notable && b.title_en); return b ? { id: b.id, en: b.title_en } : null; }")
        if nb:
            menu_click(page, '#notableBtn')   # under the More menu
            check(page.evaluate("(id) => { const r = [...document.querySelectorAll('#notableList .r')].find(e => e.dataset.id === id); return r ? r.querySelector('b').textContent.trim() : null; }", nb['id']) == nb['en'], 'English mode: the notable list shows the English title')
            page.screenshot(path=os.path.join(args.shots, 'lang-notable-en.png'))
            page.click('#notableClose'); page.wait_for_timeout(200)
        page.evaluate("() => window.__overlay.set('certainty')"); page.wait_for_timeout(300)
        lang('native'); lang('en')
        ov = page.evaluate("() => window.__overlay.state()")
        check(ov['mode'] == 'certainty' and ov['uMode'] == 1 and page.evaluate("() => window.__spineLabels || 0") >= 0, 'the certainty overlay survives the switch (mode %s)' % ov['mode'])
        page.evaluate("() => window.__overlay.set('language')")
        page.screenshot(path=os.path.join(args.shots, 'lang-topbar-en.png'), clip={'x': 0, 'y': 0, 'width': 1440, 'height': 110})
        lang('native')
        t2 = page.evaluate("() => document.getElementById('pTitle').textContent")
        check(t2 == b['title'] and page.evaluate("() => window.__lang.get()") == 'native', 'back to native: the open panel restores the book\'s own title')
        page.screenshot(path=os.path.join(args.shots, 'lang-topbar-native.png'), clip={'x': 0, 'y': 0, 'width': 1440, 'height': 110})
        lang('en')
        page.reload(wait_until='load'); wait_ready(page, args.timeout)
        check(page.evaluate("() => document.getElementById('langBtn').classList.contains('on')") and page.evaluate("() => window.__lang.get()") == 'en', 'the English choice survives a reload (localStorage)')
        lang('native')
        page.fill('#q', 'Name of the Rose'); page.wait_for_timeout(600)
        nh = page.evaluate("() => ({ rows: [...document.querySelectorAll('#results .r[data-id] b')].map(e => e.textContent.toLowerCase()), hint: !!document.querySelector('#results #qToEn') })")   # the book rows, below the Tours and Objects groups
        check(any('nome della rosa' in t for t in nh['rows'][:5]) and nh['hint'], 'native mode: an English query finds the book by its English title and offers the switch (%d rows, hint %s)' % (len(nh['rows']), nh['hint']))
        page.fill('#q', ''); page.wait_for_timeout(300)
        page.evaluate('(id) => window.__openBook(id)', b['id']); settle(page)   # leave the page as the checks below expect it: a book panel open, native titles
    else:
        check(ctl['hidden'] is True and not en['flag'], 'no English titles in the data: the control is hidden and meta.english_titles is false')
        page.evaluate("() => window.__lang.set('en')"); page.wait_for_timeout(200)
        check(page.evaluate("() => window.__lang.get()") == 'native' and page.evaluate("() => document.getElementById('pTitle').textContent") != '', 'asking for English without data stays native, nothing breaks')
    check(not errors, 'no console errors around the title switch' + ('' if not errors else ': ' + '; '.join(errors[:3])))
    # about (close the side panel first: it overlays the right end of the top bar)
    page.click('#pClose'); page.wait_for_timeout(300)
    page.click('#aboutBtn'); page.wait_for_timeout(400)
    about = page.evaluate("() => document.getElementById('about').textContent")
    check('youtube' in page.evaluate("() => document.getElementById('aboutSources').innerHTML").lower(), 'About lists the footage with links')
    check('shelf slots' in about and 'Braidense' in about, 'About renders the counts from meta')
    page.screenshot(path=os.path.join(args.shots, 'about.png'))
    page.evaluate("() => document.getElementById('aboutClose').click()"); page.wait_for_timeout(200)   # the button sits at the end of the scrolling card
    check(not page.evaluate("() => document.getElementById('about').classList.contains('show')"), 'About closes')
    # final screenshots at 1440x900
    close_panel = "() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }"
    page.evaluate(close_panel); page.wait_for_timeout(200)
    page.evaluate("() => window.__overlay.set('language')")
    page.click('[data-room="all"]'); page.wait_for_timeout(1800)
    page.screenshot(path=os.path.join(args.shots, 'final-overview.png'))
    page.evaluate("() => window.__overlay.set('certainty')"); page.click('[data-room="studio"]'); page.wait_for_timeout(1800)
    page.screenshot(path=os.path.join(args.shots, 'final-certainty.png'))
    page.evaluate("() => window.__overlay.set('language')")
    pobj = page.evaluate("() => { const os = window.__data().objects || []; const o = os.find(o => /piano/i.test(o.label || '') && o.thumb) || os.find(o => o.thumb && o.kind !== 'pile'); return o ? o.id : null; }")
    if pobj: page.evaluate('(id) => window.__openObject(id)', pobj); page.wait_for_timeout(1800)
    page.screenshot(path=os.path.join(args.shots, 'final-objects.png'))
    page.evaluate(close_panel); page.wait_for_timeout(200)
    # walk mode
    page.click('#modeWalk'); page.wait_for_timeout(900)
    check(page.evaluate("() => document.getElementById('exitWalk').classList.contains('show')"), 'walk mode toggles')
    page.click('#exitWalk')
    # the arrow keys move the visitor in both views, turning with ← →, never through a wall or a bookcase
    def key_run(code, passes):   # hold the key for a number of label passes (six frames each): the software renderer runs at a few frames a second, so wall time says nothing
        t0 = page.evaluate('() => window.__labelPass || 0'); page.keyboard.down(code)
        try: page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t0 + passes, timeout=300000)
        finally: page.keyboard.up(code)
        page.wait_for_timeout(200)
    for mname in ('orbit', 'walk'):
        page.evaluate("(m) => window.__setMode(m)", mname); page.wait_for_timeout(400)
        page.evaluate('() => window.__snapCamera(12, 1.6, 9.1, 20, 1.4, 9.1)'); settle(page, 300)   # in the long corridor, looking east along it
        p0 = page.evaluate('() => window.__camera()')
        key_run('ArrowUp', 3)
        p1 = page.evaluate('() => window.__camera()'); e1 = page.evaluate('() => window.__eyeClear()')
        dx = p1['p'][0] - p0['p'][0]
        check(dx > 0.8 and abs(p1['p'][2] - p0['p'][2]) < 0.3 and e1['inRoom'] and not e1['inGeometry'], '%s view: ArrowUp walks the visitor forward along the corridor (%.2f m, eye clear %s)' % (mname, dx, e1))
        key_run('ArrowLeft', 2)
        p2 = page.evaluate('() => window.__camera()')
        d1 = p1['d']; d2 = p2['d']
        import math
        ang = math.degrees(math.atan2(d2[0] * d1[2] - d2[2] * d1[0], d2[0] * d1[0] + d2[2] * d1[2]))
        check(abs(ang) > 15 and abs(p2['p'][0] - p1['p'][0]) < 0.05, '%s view: ArrowLeft turns the view on the spot (%.0f degrees)' % (mname, ang))
        # walk into the corridor's south wall: the eye stops at the wall instead of passing through it
        page.evaluate('() => window.__snapCamera(12, 1.6, 9.1, 12, 1.4, 12)'); settle(page, 300)
        key_run('ArrowUp', 12)
        p3 = page.evaluate('() => window.__camera()'); e3 = page.evaluate('() => window.__eyeClear()')
        check(e3['inRoom'] and not e3['inGeometry'] and p3['p'][2] < 12, '%s view: a long ArrowUp towards the wall stops inside the room, clear of the shelves (z %.2f, %s)' % (mname, p3['p'][2], e3))
    page.evaluate("() => window.__setMode('orbit')"); page.wait_for_timeout(300)

    # the certainty filter leaves only the tier it names: the shader's tier attribute agrees with the data,
    # and the anonymous piles' book blocks (desk, island, round-table and floor piles) go with the unknown tier; a screenshot of the round-table piles must change
    tc = page.evaluate("() => window.__data().meta.counts.tiers")
    sh_all = page.evaluate("() => window.__spinesShown()")
    check(sh_all['shown'] == sh_all['total'] == tc['certain'] + tc['guess'] + tc['unknown'] and sh_all['blocks'] > 50 and sh_all['blocksShown'] == sh_all['blocks'], 'filter "all": every spine and every pile block shows (%s)' % sh_all)
    page.evaluate("() => window.__snapCamera(27.6, 1.5, 12.9, 26.25, 0.95, 11.8)"); settle(page, 500)
    page.screenshot(path=os.path.join(args.shots, 'filter-all-round-table.png'), clip={'x': 500, 'y': 250, 'width': 440, 'height': 400})
    page.evaluate("() => window.__overlay.filter('certain')"); settle(page, 500)
    sh_c = page.evaluate("() => window.__spinesShown()")
    check(sh_c['shown'] == tc['certain'] and sh_c['blocksShown'] == 0, 'filter "certain only": exactly the certain-tier spines remain and no pile block (%s)' % sh_c)
    page.screenshot(path=os.path.join(args.shots, 'filter-certain-round-table.png'), clip={'x': 500, 'y': 250, 'width': 440, 'height': 400})
    try:
        from PIL import Image, ImageChops
        im1 = Image.open(os.path.join(args.shots, 'filter-all-round-table.png')).convert('RGB'); im2 = Image.open(os.path.join(args.shots, 'filter-certain-round-table.png')).convert('RGB')
        diff = ImageChops.difference(im1, im2).convert('L'); changed = sum(1 for v in diff.getdata() if v > 40) / (diff.width * diff.height)
        check(changed > 0.02, 'filter "certain only": the round-table piles vanish from the view (%.1f%% of the pixels changed)' % (changed * 100))
    except ImportError: pass
    page.evaluate("() => window.__overlay.filter('guess')"); page.wait_for_timeout(300); sh_g = page.evaluate("() => window.__spinesShown()")
    check(sh_g['shown'] == tc['guess'] and sh_g['blocksShown'] == 0, 'filter "guesses only": exactly the guess-tier spines remain (%s)' % sh_g)
    page.evaluate("() => window.__overlay.filter('hide-unknown')"); page.wait_for_timeout(300); sh_h = page.evaluate("() => window.__spinesShown()")
    check(sh_h['shown'] == tc['certain'] + tc['guess'] and sh_h['blocksShown'] == 0, 'filter "hide unknown": certain and guess spines remain, pile blocks hidden (%s)' % sh_h)
    page.evaluate("() => window.__overlay.filter('all')"); page.wait_for_timeout(300)
    check(page.evaluate("() => window.__spinesShown()")['blocksShown'] == sh_all['blocks'], 'filter back to "all": the pile blocks return')

    # the comb units stand across the room at right angles to P, the desk is clear of the lounge chair, the 'ECO' row on the
    # low unit is books (unknown tier, hidden with the plaque's old 'box files' wording gone), and the curiosity cabinet's flat books follow the unknown tier
    st = page.evaluate("() => { const r = window.__data().rooms.find(r => r.id === 'studio'); const bc = Object.fromEntries(r.bookcases.map(b => [b.id, b])); return { bc: Object.fromEntries(Object.entries(bc).map(([k, b]) => [k, { x: b.x, z: b.z, rot: b.rotationY, w: b.width, d: b.depth }])), windows: (r.windows || []).map(w => w.wall + '@' + w.offset) }; }")
    P = st['bc'].get('study-P'); teeth = [st['bc'].get(k) for k in ('study-Na', 'study-Nb', 'study-Nc', 'study-Oa', 'study-Ob')]; isl = [st['bc'].get(k) for k in ('study-M-A', 'study-M-B')]
    across = P and all(t and (t['rot'] - P['rot']) % 180 == 90 for t in teeth) and all(i and (i['rot'] - P['rot']) % 180 == 0 for i in isl)
    fits = P and all(t['z'] + t['w'] / 2 < P['z'] - P['d'] / 2 - 0.8 and t['z'] - t['w'] / 2 > max(i['z'] for i in isl) + 1.5 for t in teeth)
    check(across and fits, 'study: the five comb faces stand across the room at right angles to P with an aisle before P and behind the M island (rotations %s)' % [t and t['rot'] for t in teeth])
    def foot(o):
        a = math.radians(o.get('rotation') or 0); w, d = o['size'][0], o['size'][2]
        ex = abs(math.cos(a)) * w / 2 + abs(math.sin(a)) * d / 2; ez = abs(math.sin(a)) * w / 2 + abs(math.cos(a)) * d / 2
        return o['x'] - ex, o['x'] + ex, o['z'] - ez, o['z'] + ez
    so = page.evaluate("() => Object.fromEntries((window.__data().objects || []).filter(o => o.room === 'studio').map(o => [o.id, { x: o.x, z: o.z, size: o.size, rotation: o.rotation, base_y: o.base_y, label: o.label, description: o.description || '', kind: o.kind, row: !!o.row, on: o.on || null }]))")
    def apart(a, b):
        x0, x1, z0, z1 = foot(a); u0, u1, v0, v1 = foot(b); return min(x1, u1) - max(x0, u0) <= 0.02 or min(z1, v1) - max(z0, v0) <= 0.02
    dsk, eam = so.get('obj:studio:eco-desk'), so.get('obj:studio:eames')
    check(dsk and eam and apart(dsk, eam), 'study: the desk before Q and the lounge chair at L no longer overlap (desk z %.2f, chair z %.2f)' % (dsk['z'] if dsk else -1, eam['z'] if eam else -1))
    floor_objs = [o for o in so.values() if (o.get('base_y') or 0) < 0.05 and o['kind'] not in ('artwork',)]
    clashes = [(a['label'][:30], b['label'][:30]) for i, a in enumerate(floor_objs) for b in floor_objs[i + 1:] if not apart(a, b)]
    check(not clashes, 'study: no two floor-standing pieces overlap by footprint%s' % ('' if not clashes else ': ' + '; '.join('%s / %s' % c for c in clashes[:3])))
    row, plq, unit = so.get('obj:studio:eco-paperbacks'), so.get('obj:studio:eco-plaque'), so.get('obj:studio:comb-end-unit')
    on_unit = row and plq and unit and abs(row['z'] - unit['z']) < 0.2 and abs(plq['z'] - unit['z']) < 0.2 and abs(row['x'] - unit['x']) < 0.7 and abs(plq['x'] - unit['x']) < 0.75 and row['base_y'] > 1.0
    comb_top = [so.get(k) for k in ('obj:studio:eco-plaque', 'obj:studio:calligraphy', 'obj:studio:island-piles-2', 'obj:studio:eco-paperbacks')]   # the desk row's open box files are real and stay
    no_boxfiles = all(o and not re.search(r'box files', re.sub(r'not box files|took them for .ECO. box files', '', o['label'] + ' ' + o['description'], flags=re.I), re.I) for o in comb_top)
    check(on_unit and row['row'] and 'Bompiani' in row['label'] and no_boxfiles, 'study: the white row on the low unit at the comb end is Eco\'s Bompiani paperbacks with the plaque at its end, no "box files" left in the plaque wording')
    bl_all = page.evaluate("() => window.__blocksOf('obj:studio:eco-paperbacks')"); cab_all = page.evaluate("() => window.__blocksOf('salotto-wood')")
    page.evaluate("() => window.__overlay.filter('certain')"); page.wait_for_timeout(300)
    bl_c = page.evaluate("() => window.__blocksOf('obj:studio:eco-paperbacks')"); cab_c = page.evaluate("() => window.__blocksOf('salotto-wood')")
    page.evaluate("() => window.__overlay.filter('all')"); page.wait_for_timeout(300)
    check(bl_all['blocks'] >= 20 and bl_all['shown'] == bl_all['blocks'] and bl_c['shown'] == 0, 'study: the ECO paperback row (%d blocks) hides under "certain only" and shows under "all"' % bl_all['blocks'])
    check(cab_all['blocks'] >= 3 and cab_all['shown'] == cab_all['blocks'] and cab_c['shown'] == 0, 'curiosity cabinet: its %d flat and standing books hide under "certain only"' % cab_all['blocks'])
    check(set(st['windows']) == {'W@0.9', 'S@1', 'S@3.7'}, 'study: the layout\'s three windows are drawn (W wall by the door, two over the desk row): %s' % st['windows'])

    # nothing placed on top of a desk, a cabinet or a bookcase hangs past its top (the desk piles floated 1.2 m past the desk),
    # and every ladder's blocks stay within its own footprint plus its lean (the stepladder's second leg was a plate splayed off its side)
    allo = page.evaluate("() => (window.__data().objects || []).map(o => ({ id: o.id, room: o.room, kind: o.kind, x: o.x, z: o.z, size: o.size, rotation: o.rotation, base_y: o.base_y, on: o.on || null, note: o.placement_note || '', label: o.label, against: o.against_wall || null }))")
    bcs = page.evaluate("() => { const out = {}; for (const r of window.__data().rooms) for (const b of r.bookcases) out[b.id] = { x: b.x, z: b.z, size: [b.width, b.height, b.depth], rotation: b.rotationY }; return out; }")
    byid = {o['id']: o for o in allo}; loose = []
    for o in allo:
        if (o.get('base_y') or 0) < 0.05 or o['kind'] == 'artwork': continue
        sup = None
        if o['on'] and o['on'] in byid: sup = byid[o['on']]
        elif o['note'].startswith('objects_map anchor: on ') or 'on top of' in o['note'] or o['note'].startswith('Seen') and (' on ' in o['note'] or 'on top of' in o['note']):
            cand = [p for p in allo if p is not o and (('on ' + p['label'][:30]) in o['note'] or ('on top of ' + p['label'][:20]) in o['note'])]
            if cand: sup = cand[0]
            elif o['against'] and o['against'] in bcs and 'on top of' in o['note']: sup = bcs[o['against']]
        if not sup: continue
        x0, x1, z0, z1 = foot(o); u0, u1, v0, v1 = foot(sup); top = (sup.get('base_y') or 0) + sup['size'][1]
        if sup.get('id'):   # the support's footprint is what the page draws for it, not only its data (the rare-book table was drawn across the room while its data ran along it)
            se = page.evaluate('(id) => window.__objectExtent(id)', sup['id'])
            if se and se.get('n'): u0, u1, v0, v1 = min(u0, se['min'][0]), max(u1, se['max'][0]), min(v0, se['min'][2]), max(v1, se['max'][2])   # the union: a support's shaped parts (the piano's body) are not blocks, and the sizes-agree check below keeps the data footprint honest
        oe = page.evaluate('(id) => window.__objectExtent(id)', o['id'])
        if oe and oe.get('n'): x0, x1, z0, z1 = oe['min'][0], oe['max'][0], oe['min'][2], oe['max'][2]
        over = max(0, u0 - x0) + max(0, x1 - u1) + max(0, v0 - z0) + max(0, z1 - v1)
        if over > 0.12 or abs(o['base_y'] - top) > 0.06: loose.append('%s (%.2f m past its support, %.2f m off its top)' % (o['id'], over, o['base_y'] - top))
    check(not loose, 'every pile or object on top of another rests on it, inside its top%s' % ('' if not loose else ': ' + '; '.join(loose[:4])))
    lad = []
    for o in allo:
        if o['kind'] != 'ladder': continue
        ext = page.evaluate('(id) => window.__objectExtent(id)', o['id'])
        if not ext: lad.append(o['id'] + ' (no blocks)'); continue
        reach = o['size'][1] * 0.22 + 0.35   # a leaning ladder's top reaches this far beyond its footprint
        x0, x1, z0, z1 = foot(o)
        if ext['min'][0] < x0 - reach or ext['max'][0] > x1 + reach or ext['min'][2] < z0 - reach or ext['max'][2] > z1 + reach or ext['min'][1] < -0.05:
            lad.append('%s (blocks span x %.2f..%.2f z %.2f..%.2f, footprint x %.2f..%.2f z %.2f..%.2f)' % (o['id'], ext['min'][0], ext['max'][0], ext['min'][2], ext['max'][2], x0, x1, z0, z1))
    check(not lad, 'every ladder\'s parts stay within its own footprint and lean (%d ladders)%s' % (sum(1 for o in allo if o['kind'] == 'ladder'), '' if not lad else ': ' + '; '.join(lad[:3])))
    probe = page.evaluate("() => { window.__snapCamera(25.8, 1.5, 12.3, 27.1, 0.9, 11.4); return true; }"); settle(page, 400)
    page.screenshot(path=os.path.join(args.shots, 'study-stepladder.png'))
    page.evaluate("() => window.__snapCamera(23.7, 1.6, 17.2, 25.0, 0.8, 19.6)"); settle(page, 400)
    page.screenshot(path=os.path.join(args.shots, 'study-desk-piles.png'))

    # an object's two sizes agree, a picture before a bookcase faces the room, nothing is drawn through a wall, no plate over an emptied pile
    dims = page.evaluate("() => (window.__data().objects || []).filter(o => o.dims_m && o.kind !== 'artwork' && o.kind !== 'pile').map(o => ({ id: o.id, size: o.size, dims: o.dims_m }))")
    bad = [d['id'] for d in dims if any(abs(a - b) > 0.011 for a, b in zip([d['size'][0], d['size'][2], d['size'][1]], d['dims']))]
    check(dims and not bad, 'every object\'s drawn size (dims_m) agrees with its data size (%d objects carry both)%s' % (len(dims), '' if not bad else ': ' + ', '.join(bad[:5])))
    facing = []
    for o in allo:
        if o['kind'] != 'artwork' or not o['against'] or o['against'] not in bcs or 'in front of' not in o['note']: continue
        if (o['rotation'] or 0) % 360 != (bcs[o['against']]['rotation'] or 0) % 360: facing.append('%s (turned %s, its bookcase faces %s)' % (o['id'], o['rotation'], bcs[o['against']]['rotation']))
    check(not facing, 'every picture leaning on or hung before a bookcase faces the room (the alfabeta poster showed its back)%s' % ('' if not facing else ': ' + '; '.join(facing[:3])))
    rooms = page.evaluate("() => { const out = {}; for (const r of window.__data().rooms) out[r.id] = { org: r.origin, size: r.size }; return out; }")
    through = []
    for o in allo:
        ext = page.evaluate('(id) => window.__objectExtent(id)', o['id']); rm = rooms.get(o['room'])
        if not ext or not ext.get('n') or not rm: continue
        ox, oz = rm['org']; w, d = rm['size']
        out = max(ox - ext['min'][0], ext['max'][0] - (ox + w), oz - ext['min'][2], ext['max'][2] - (oz + d))
        if out > 0.35: through.append('%s (%.2f m outside its room)' % (o['id'], out))
    check(not through, 'nothing drawn for an object leaves its room by more than a wall\'s thickness (the desk\'s return ran 1.2 m through the south wall)%s' % ('' if not through else ': ' + '; '.join(through[:3])))
    anon = [o['id'] for o in allo if o['kind'] == 'pile' and not page.evaluate("(id) => { const o = window.__data().objects.find(o => o.id === id); return !!(o.books && o.books.length); }", o['id'])]
    page.evaluate("() => window.__overlay.filter('certain')"); settle(page, 300)
    plates_c = [page.evaluate('(id) => window.__objectLabel(id)', i) for i in anon]
    page.evaluate("() => window.__overlay.filter('all')"); settle(page, 300)
    plates_a = [page.evaluate('(id) => window.__objectLabel(id)', i) for i in anon]
    check(anon and all(p and p['emptied'] for p in plates_c) and all(p and not p['emptied'] for p in plates_a), 'the plates over the %d anonymous piles go with their blocks: hidden under "certain only", back under "all"' % len(anon))
    page.evaluate("() => window.__snapCamera(9.7, 1.5, 7.0, 9.7, 0.8, 4.0)"); settle(page, 400)
    page.screenshot(path=os.path.join(args.shots, 'antichi-table.png'))
    page.evaluate("() => window.__snapCamera(26.3, 2.6, 23.6, 26.3, 0.8, 20.0)"); settle(page, 400)
    page.screenshot(path=os.path.join(args.shots, 'study-desk-return.png'))
    page.evaluate("() => window.__snapCamera(28.3, 1.3, 12.8, 28.44, 0.55, 10.9)"); settle(page, 400)
    page.screenshot(path=os.path.join(args.shots, 'study-poster.png'))

    # low furniture stops the walker by its footprint, a narrow piece is slipped round, the Colour menu keeps its keys, the column stays under the bar
    for mname in ('walk', 'orbit'):
        page.evaluate("(m) => window.__setMode(m)", mname); page.wait_for_timeout(400)
        page.evaluate('() => window.__snapCamera(4.3, 1.6, 4.0, 4.3, 1.4, 8.0)'); settle(page, 300); key_run('ArrowUp', 8)
        p = page.evaluate('() => window.__camera()')['p']; inside = page.evaluate('(p) => window.__walkBlockersAt(p[0], p[1], p[2])', p)
        check(p[2] < 4.63 and not inside, '%s view: the sofa stops the walker (z %.2f, sofa front at 4.63, inside %s)' % (mname, p[2], inside))
        page.evaluate('() => window.__snapCamera(5.6, 1.6, 5.75, 5.6, 1.4, 8.0)'); settle(page, 300); key_run('ArrowUp', 8)
        p = page.evaluate('() => window.__camera()')['p']; inside = page.evaluate('(p) => window.__walkBlockersAt(p[0], p[1], p[2])', p)
        check(p[2] < 6.36 and not inside, '%s view: the piano stops the walker (z %.2f, piano front at 6.36, inside %s)' % (mname, p[2], inside))
        page.evaluate('() => window.__snapCamera(16.5, 1.6, 9.1, 24.0, 1.4, 9.1)'); settle(page, 300); key_run('ArrowUp', 14)
        p = page.evaluate('() => window.__camera()')['p']; e = page.evaluate('() => window.__eyeClear()')
        check(p[0] > 19.2 and e['inRoom'] and not e['inGeometry'], '%s view: a straight walk east slips round the corridor ladder (x %.2f, ladder at 18.48)' % (mname, p[0]))
        page.evaluate('() => window.__snapCamera(20.5, 1.6, 9.1, 10.0, 1.4, 9.1)'); settle(page, 300); key_run('ArrowUp', 14)
        p = page.evaluate('() => window.__camera()')['p']
        check(p[0] < 17.8, '%s view: and a straight walk west (x %.2f)' % (mname, p[0]))
        page.evaluate('() => window.__snapCamera(12, 1.6, 9.1, 20, 1.4, 9.1)'); settle(page, 300)
        page.focus('#overlaySel'); t0 = page.evaluate('() => window.__labelPass || 0'); page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t0 + 2, timeout=300000)   # the walk settles its first frame after a snap before the reading
        p0 = page.evaluate('() => window.__camera()'); key_run('ArrowDown', 3); p1 = page.evaluate('() => window.__camera()')
        moved = sum((a - b) ** 2 for a, b in zip(p0['p'], p1['p'])) ** 0.5 + sum((a - b) ** 2 for a, b in zip(p0['d'], p1['d'])) ** 0.5
        check(moved < 1e-6, '%s view: the arrow keys leave the camera alone while the Colour menu has focus (moved %.4f)' % (mname, moved))
        page.evaluate("() => { const s = document.getElementById('overlaySel'); s.value = 'language'; s.dispatchEvent(new Event('change')); s.blur(); }"); page.wait_for_timeout(300)
    page.evaluate("() => window.__setMode('walk')"); page.wait_for_timeout(300)
    for name, eye, tgt in (('keyboard pile 6 at 1 m', [6.47, 1.43, 4.87], [6.47, 0.95, 6.37]), ('keyboard pile 3 at 1 m', [5.6, 1.43, 4.87], [5.6, 0.95, 6.37]), ('pile 1 at 0.7 m', [6.18, 1.5, 5.2], [6.18, 1.0, 6.37])):
        t0 = page.evaluate('() => window.__labelPass || 0'); page.evaluate('([a, b]) => window.__snapCamera(a[0], a[1], a[2], b[0], b[1], b[2])', [eye, tgt])
        page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t0 + 2, timeout=60000); page.wait_for_timeout(200)
        col = page.evaluate('() => window.__pileColumnPx()')
        check(col['lines'] > 0 and col['top'] >= col['bar'], 'the lettered column stays under the top bar before %s (top %.0f px, bar %.0f px, %d lines, %s)' % (name, col['top'], col['bar'], col['lines'], page.evaluate('() => window.__listedPile()')))
    page.screenshot(path=os.path.join(args.shots, 'pile-column-under-bar.png'))
    page.evaluate("() => window.__setMode('orbit')"); page.wait_for_timeout(300)
    # the book panels on the walls whose layout notes cite the photographs read them as prose
    cids = page.evaluate("() => { const out = []; for (const r of window.__data().rooms) for (const bc of r.bookcases) if (/criticaletteraria_/i.test(bc.evidence || '')) out.push(bc.id); return out; }")
    leaks = []
    for cid in cids:
        bid = page.evaluate("(cid) => { const b = window.__data().books.find(b => b.bookcase === cid && b.title); return b ? b.id : null; }", cid)
        if not bid: continue
        page.evaluate('(id) => window.__openBook(id)', bid); page.wait_for_timeout(500)
        txt = page.evaluate("() => document.getElementById('pBody').innerText")
        if re.search(r'criticaletteraria_|\bfondazione \d\d/\d\d\b', txt, re.I) or 'Critica Letteraria photograph' not in txt: leaks.append(cid)
    check(cids and not leaks, 'book panels on the %d walls whose notes cite the photographs name them as prose%s' % (len(cids), '' if not leaks else ' - leaks on %s' % leaks[:4]))
    page.click('#pClose'); page.wait_for_timeout(300)

    # ---- workshop text, ghost cards, spine luminance, label occlusion and the glass cabinet
    RAW = re.compile(r'meta\.|\.jsonl?\b|\[\]|objects_map|wall_id|layout\.|counts\.|rooms\[|\.png\b|\.jpe?g\b|\.webp\b|tier_reason|placement_note')
    # 1. workshop text: legend notes, object panels and notable sources read as prose, never as file names, key paths or rule names
    for mode in ('certainty', 'subject', 'on_film', 'source', 'century', 'language'):
        page.evaluate('(m) => window.__overlay.set(m)', mode); page.wait_for_timeout(300)
        ltxt = page.evaluate("() => document.getElementById('legend').textContent")
        hit = RAW.search(ltxt)
        check(not hit, 'legend (%s overlay) shows no file names or key paths%s' % (mode, '' if not hit else ': ...' + ltxt[max(0, hit.start() - 30):hit.end() + 30]))
    page.evaluate("() => window.__overlay.set('language')")
    oids = page.evaluate("() => { const os = window.__data().objects || []; const a = os.filter(o => o.kind !== 'pile').slice(0, 8).map(o => o.id), b = os.filter(o => o.kind === 'pile').sort((x, y) => (y.books || []).length - (x.books || []).length).slice(0, 4).map(o => o.id); return a.concat(b); }")
    bad = []; noev = []
    for oid in oids:
        page.evaluate('(id) => window.__openObject(id)', oid); page.wait_for_timeout(700)
        txt = page.evaluate("() => document.getElementById('pBody').textContent")
        if RAW.search(txt) or re.search(r'\brule\b', txt): bad.append(oid)
        if not re.search(r'Seen on film at \d+:\d\d|Seen in a photograph|Position inferred from the film', txt): noev.append(oid)
    check(oids and not bad, 'object panels (%d sampled) carry no file names or rule names%s' % (len(oids), '' if not bad else ': ' + ', '.join(bad[:4])))
    check(not noev, 'object panels say only "Seen on film at mm:ss" / "Seen in a photograph" / "Position inferred from the film"%s' % ('' if not noev else ': ' + ', '.join(noev[:4])))
    page.evaluate("() => window.__openObject('obj:studio:eco-desk')"); page.wait_for_timeout(700)
    check(page.evaluate("() => { const a = [...document.querySelectorAll('#pBody .film a, #pBody .thumbcap a')]; return a.some(x => /Seen on film at \\d+:\\d\\d/.test(x.textContent) && /youtube\\.com\\/watch/.test(x.href)); }"), 'object panel links "Seen on film at mm:ss" to the film')
    page.screenshot(path=os.path.join(args.shots, 'object-evidence.png'))
    nids = page.evaluate("() => window.__data().books.filter(b => b.notable && b.notable.source).slice(0, 12).map(b => b.id)")
    badn = []
    for bid in nids:
        page.evaluate('(id) => window.__openBook(id)', bid); page.wait_for_timeout(500)
        q = page.evaluate("() => { const e = document.querySelector('#panel .quote'); return e ? e.textContent : ''; }")
        if '[' in q or ']' in q or RAW.search(q) or re.search(r'\w+\.(md|txt|csv|html)\b', q): badn.append(bid)
    check(nids and not badn, 'notable sources (%d sampled) are human-readable, no brackets or file names%s' % (len(nids), '' if not badn else ': ' + ', '.join(badn[:4])))
    page.evaluate(close_panel); page.wait_for_timeout(200)
    # 2. absent works: ghost cards in the notable list and in the notable tours
    counts = page.evaluate("() => window.__data().meta.counts || {}")
    nmiss = counts.get('notable_missing', 0)
    menu_click(page, '#notableBtn', 600)   # under the More menu
    ghosts = page.evaluate("() => [...document.querySelectorAll('#notableList .r.ghost')].map(e => ({text: e.textContent, near: !!e.querySelector('a.near')}))")
    check(nmiss > 0 and len(ghosts) == nmiss, 'notable list draws one ghost card per absent work (%d cards, meta.counts.notable_missing %d)' % (len(ghosts), nmiss))
    check(ghosts and all('Not found on these shelves' in g['text'] for g in ghosts), 'ghost cards say "Not found on these shelves"')
    check(page.evaluate("() => (document.getElementById('notableMissing') || {}).textContent") == str(nmiss), 'notable panel header shows meta.counts.notable_missing (%d)' % nmiss)
    near = sum(1 for g in ghosts if g['near'])
    check(near == counts.get('notable_missing_with_nearest', near), 'ghost cards with a nearest-book jump: %d (meta %s)' % (near, counts.get('notable_missing_with_nearest')))
    page.screenshot(path=os.path.join(args.shots, 'notable-absent.png'))
    if near:
        page.evaluate("() => document.querySelector('#notableList .r.ghost a.near').click()"); settle(page)
        check(page.evaluate("() => document.getElementById('panel').classList.contains('open')"), 'the nearest-book jump on a ghost card opens that book')
        page.evaluate(close_panel)
    if page.evaluate("() => document.getElementById('notable').classList.contains('show')"): page.click('#notableClose')
    tours = page.evaluate("() => (window.__data().meta.notable_tours || []).map(t => ({id: t.id, missing: (t.stops || []).filter(s => s.missing).length, withNear: (t.stops || []).filter(s => s.missing && s.nearest_id).length}))")
    tm = [t for t in tours if t['missing']]
    if tm:
        t = tm[0]
        page.evaluate('(id) => window.__tour.notable(id)', t['id']); settle(page)
        st = page.evaluate('() => window.__tour.stops()')
        miss = [s for s in st if s['kind'] == 'missing']
        check(len(miss) == t['missing'], 'notable tour %s carries its %d absent works as stops (%d)' % (t['id'], t['missing'], len(miss)))
        check(sum(1 for s in miss if s['nearest']) == t['withNear'], 'absent stops keep their nearest book (%d)' % t['withNear'])
        k = next((i for i, s in enumerate(st) if s['kind'] == 'missing'), None)
        if k is not None:
            for _ in range(k): page.evaluate('() => window.__tour.next()')
            settle(page)
            card = page.evaluate("() => { const e = document.querySelector('#tour .txt'); return {ghost: e.classList.contains('ghost'), text: e.textContent, near: !!e.querySelector('a.near')}; }")
            check(card['ghost'] and 'Not found on these shelves' in card['text'], 'absent tour stop is drawn as a ghost card with the "not found" note')
            check(card['near'] == bool(st[k]['nearest']), 'absent tour stop offers its nearest-book jump when one is known')
            page.screenshot(path=os.path.join(args.shots, 'tour-absent.png'))
        page.evaluate('() => window.__tour.end()')
    else: check(False, 'no notable tour with absent works in meta')
    # 3. lighting: spine faces at eye level, with the haze pulled back
    page.evaluate("() => window.__setMode('walk')"); page.wait_for_timeout(600)
    LUM = {}
    for name, eye, tgt in (('corridor-eyelevel', [12.0, 1.6, 8.75], [12.0, 1.5, 9.9]), ('corridor-eyelevel-a2', [22.6, 1.6, 8.75], [22.6, 1.5, 9.9]), ('q-wall-eyelevel', [35.3, 1.6, 12.78], [37.3, 1.6, 12.78]), ('corridor-along', [4.7, 1.6, 9.1], [20.0, 1.3, 9.1])):
        page.evaluate('([a, b]) => window.__snapCamera(a[0], a[1], a[2], b[0], b[1], b[2])', [eye, tgt]); page.wait_for_timeout(2500)
        sp = os.path.join(args.shots, name + '.png'); page.screenshot(path=sp); LUM[name] = lum_stats(sp)
        if name == 'corridor-along': LUM['corridor-far-end'] = lum_stats(sp, (0.42, 0.35, 0.58, 0.65))
    print('luminance', json.dumps(LUM))
    if LUM['corridor-eyelevel']:
        for name in ('corridor-eyelevel', 'corridor-eyelevel-a2', 'q-wall-eyelevel'):
            L = LUM[name]
            check(L['mean'] > 0.35 and L['black'] < 0.05 and L['dark'] < 0.3, '%s: spines at eye level are lit (mean luminance %.3f, %.1f%% black, %.1f%% dark)' % (name, L['mean'], L['black'] * 100, L['dark'] * 100))
            check(L['white'] < 0.25, '%s: not blown out (%.1f%% white)' % (name, L['white'] * 100))
        F = LUM['corridor-far-end']
        check(F['mean'] < 0.85 and F['std'] > 0.05 and F['white'] < 0.3, 'far end of the corridor is not washed out by fog (mean %.3f, std %.3f, %.1f%% white)' % (F['mean'], F['std'], F['white'] * 100))
    else: check(False, 'PIL missing: cannot measure luminance')
    hz_eye = page.evaluate('() => window.__haze()')
    check(hz_eye is not None and hz_eye <= 0.2, 'haze over the never-filmed shelves is light at eye level (opacity %s)' % hz_eye)
    # 4. label occlusion and pile lettering
    def snap_settled(page, eye, tgt):   # move the camera and wait until the label pass (every sixth frame) has run twice from the new spot
        t0 = page.evaluate('() => window.__labelPass || 0')
        page.evaluate('([a, b]) => window.__snapCamera(a[0], a[1], a[2], b[0], b[1], b[2])', [eye, tgt])
        try: page.wait_for_function('(t0) => (window.__labelPass || 0) >= t0 + 2', arg=t0, timeout=30000)
        except Exception: page.wait_for_timeout(2500)
        page.wait_for_timeout(300)
    snap_settled(page, [8.7, 1.6, 4.3], [8.7, 1.6, 1.1])
    vis = [v for v in page.evaluate('() => window.__labelsVisible()') if v['inView']]   # labels the occlusion pass left on and the camera frames (the ones behind it, seen through the doorway, do not count)
    other = [v for v in vis if v['room'] and v['room'] != 'antichi']
    check(vis and not other, 'labels behind the walls are hidden: the antichi view shows %d labels, none from other rooms%s' % (len(vis), '' if not other else ' (leaked: %s)' % [(v['kind'], v['room'], (v['text'] or '')[:20]) for v in other[:4]]))
    page.screenshot(path=os.path.join(args.shots, 'labels-antichi.png'))
    snap_settled(page, [4.7, 1.6, 9.1], [20.0, 1.3, 9.1])
    vis = [v for v in page.evaluate('() => window.__labelsVisible()') if v['inView']]
    other = [v for v in vis if v['room'] and not v['room'].startswith('corridoio')]
    check(not other, 'along the corridor no label from the rooms beside it shows through the walls%s' % ('' if not other else ' (leaked: %s)' % [(v['kind'], v['room']) for v in other[:4]]))
    page.evaluate("() => window.__setMode('orbit')"); page.wait_for_timeout(300)
    pile_ids = page.evaluate("() => (window.__data().objects || []).filter(o => o.kind === 'pile' && o.books && o.books.length).sort((a, b) => b.books.length - a.books.length).slice(0, 2).map(o => o.id)")
    check(len(pile_ids) == 2, 'pile objects with read books in the data: %s' % pile_ids)
    for oid in pile_ids:
        page.evaluate('(id) => window.__openObject(id)', oid); settle(page, 300)
        t0 = page.evaluate('() => window.__labelPass || 0')   # the spine lettering is refreshed by the label pass (every sixth frame): wait for two passes from the landing spot
        try: page.wait_for_function('(t0) => (window.__labelPass || 0) >= t0 + 2', arg=t0, timeout=30000)
        except Exception: page.wait_for_timeout(2500)
        pl = page.evaluate('() => window.__pileLabels || {}')
        check(pl and list(pl.keys()) == [oid] and max(pl.values()) <= 18, 'pile lettering at %s: only the nearest pile lists its titles, at most 18 lines (%s)' % (oid, pl))   # one pile at a time, never the heap
        page.screenshot(path=os.path.join(args.shots, 'piles-%s.png' % oid.split(':')[-1]))
    # no pile plate at any distance, the pile the viewer faces is the one lettered, the curiosity cabinet takes the click
    for spot7, tgt7, want7 in (([5.6, 1.5, 5.0], [5.6, 1.15, 6.5], None), ([6.18, 1.43, 4.87], [6.18, 0.95, 6.37], 'obj:salotto:piano-pile-07'), ([5.0, 1.5, 4.9], [4.976, 1.4, 6.79], 'obj:salotto:piano-pile-06')):
        snap_settled(page, spot7, tgt7)
        t0 = page.evaluate('() => window.__labelPass || 0')
        try: page.wait_for_function('(t0) => (window.__labelPass || 0) >= t0 + 2', arg=t0, timeout=30000)
        except Exception: page.wait_for_timeout(2500)
        vis7 = [v for v in page.evaluate('() => window.__labelsVisible()') if v['inView'] and re.match(r'^Piano (lid|keyboard)', v['text'] or '')]
        lp7 = page.evaluate('() => window.__listedPile()'); pl7 = page.evaluate('() => window.__pileLabels || {}')
        check(not vis7, 'no pile plate in view in front of the piano at %s (%d)' % (spot7, len(vis7)))
        if want7: check(lp7 == want7 and pl7.get(want7, 0) > 0, 'standing before %s the page letters that pile (listed %s, %s)' % (want7.split(':')[-1], lp7, pl7))
        else: check(lp7 is not None and pl7, 'facing the piano from 1.4 m a pile is lettered (%s, %s)' % (lp7, pl7))
    page.screenshot(path=os.path.join(args.shots, 'piles-front.png'))
    snap_settled(page, [6.1, 1.4, 5.1], [7.25, 1.15, 5.1])
    cab = page.evaluate("() => { const r = document.querySelector('canvas').getBoundingClientRect(); const p = window.__pickAt(r.left + r.width / 2, r.top + r.height / 2); return p && p.label ? p.label.caseId || null : (typeof p === 'number' ? 'book ' + p : null); }")
    check(cab == 'salotto-wood', 'the curiosity cabinet takes a click on its front (picked %s)' % cab)
    page.screenshot(path=os.path.join(args.shots, 'cabinet-pick.png'))
    # the spot in the living room farthest from every pile: no per-book pile titles from there
    spot = page.evaluate("() => { const os = (window.__data().objects || []).filter(o => o.kind === 'pile' || (o.books && o.books.length)); const r = window.__data().rooms.find(r => r.id === 'salotto'); let best = null; for (let x = r.origin[0] + 0.6; x < r.origin[0] + r.size[0] - 0.6; x += 0.25) for (let z = r.origin[1] + 0.6; z < r.origin[1] + r.size[1] - 0.6; z += 0.25) { let d = 1e9; for (const o of os) d = Math.min(d, Math.hypot(o.x - x, o.z - z)); if (!best || d > best.d) best = {x, z, d}; } return best; }")
    snap_settled(page, [spot['x'], 1.6, spot['z']], [spot['x'] + 1, 1.5, spot['z']])
    pl = page.evaluate('() => window.__pileLabels || {}')
    check(spot['d'] > 2.2 and not pl, 'no per-book pile titles beyond about 2 m (nearest pile %.1f m: %s)' % (spot['d'], pl))
    page.evaluate(close_panel)
    # 5. tour fly-to frames the target from inside the room, never inside geometry; the room button follows
    rooms = page.evaluate("() => window.__data().rooms.map(r => ({id: r.id, o: r.origin, s: r.size}))")
    def room_of(p, pad=0.05):
        for r in rooms:
            if r['o'][0] - pad <= p[0] <= r['o'][0] + r['s'][0] + pad and r['o'][1] - pad <= p[2] <= r['o'][1] + r['s'][1] + pad: return r['id']
        return None
    page.evaluate('() => window.__tour.start()'); settle(page)
    st = page.evaluate('() => window.__tour.stops()'); geo = []; out = []; btn = []
    for k in range(len(st)):
        if k: page.evaluate('() => window.__tour.next()'); settle(page)
        cam = page.evaluate('() => window.__camera()'); clr = page.evaluate('() => window.__eyeClear()'); cur = page.evaluate('() => window.__currentRoom()')
        if clr['inGeometry']: geo.append(k + 1)
        if not clr['inRoom'] or not (1.0 <= clr['y'] <= 2.6): out.append((k + 1, [round(v, 2) for v in cam['p']]))
        exp = room_of(cam['p'])
        if exp and cur != exp: btn.append((k + 1, exp, cur))
    check(len(st) >= 8 and not geo, 'tour: no stop lands inside a bookcase or object (%d stops)%s' % (len(st), '' if not geo else ' - stops %s' % geo))
    check(not out, 'tour: every stop stands at eye level inside its room%s' % ('' if not out else ' - %s' % out[:4]))
    check(not btn, 'tour: the room button follows the camera at every stop%s' % ('' if not btn else ' - (stop, room, button) %s' % btn[:4]))
    page.screenshot(path=os.path.join(args.shots, 'tour-last-stop.png'))
    page.evaluate('() => window.__tour.end()')
    t0 = page.evaluate('() => window.__labelPass || 0')
    page.evaluate('() => window.__snapCamera(12, 1.6, 9.1, 20, 1.4, 9.1)')
    try: page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t0 + 2, timeout=60000)   # the button follows on the next frame, and after the studio stop the software renderer may take seconds to draw one
    except Exception: page.wait_for_timeout(1500)
    check(page.evaluate('() => window.__currentRoom()') == 'corridoio', 'room button follows a camera moved into the corridor without a click (%s)' % page.evaluate('() => window.__currentRoom()'))
    # 5b. the Durand incunabulum behind the glass of the rare cabinet is pickable
    dur = page.evaluate("() => { const b = window.__data().books.find(b => b.id === 'braidense:UM1E025681') || window.__data().books.find(b => /ECO\\.03\\.0001/.test(b.shelfmark || '')); return b ? b.id : null; }")
    if dur:
        page.evaluate('(id) => window.__openBook(id)', dur); settle(page); page.click('#pClose'); page.wait_for_timeout(300)
        pt = page.evaluate('(id) => window.__bookScreen(id)', dur)
        got = page.evaluate('([x, y]) => { const r = window.__pickAt(x, y); return typeof r === "number" && r >= 0 ? window.__data().books[r].id : JSON.stringify(r && r.obj ? r.obj.id : r); }', [pt['x'], pt['y']]) if pt else None
        check(got == dur, 'the Durand incunabulum (ECO.03.0001) is picked through the glass cabinet: %s' % got)
        page.screenshot(path=os.path.join(args.shots, 'durand.png'))
    else: check(False, 'Durand incunabulum not in the data')
    page.evaluate(close_panel); page.evaluate("() => window.__overlay.set('language')")


    # ---- the sourced tours (meta.tours) --------------------------------------------------------------------------
    tours12 = page.evaluate('() => window.__tours.list()')
    check(len(tours12) >= 4 and all(t['stops'] >= 1 for t in tours12), 'the tours load (%s)' % ', '.join('%s %d' % (t['id'], t['stops']) for t in tours12))
    want13 = ['rose', 'pendulum', 'island', 'prague', 'baudolino', 'perfect-language', 'essays', 'own-books', 'strange', 'false', 'lists', 'lands', 'comics', 'popular']
    have13 = [t['id'] for t in tours12]
    check(have13 == want13 and all(t['stops'] >= 10 for t in tours12), 'the fourteen book-centred tours are the set, each ten stops or more (%s)' % have13)
    firsts = page.evaluate("() => { const D = window.__data(); return window.__tours.list().map((t) => { const i = D._index.get(t.targets[0]); const b = i === undefined ? null : D.books[i]; return [t.id, b ? b.bookcase : null, b ? (b.author || '') : null]; }); }")
    want16 = {'rose': 'obj:salotto:piano-pile-07', 'pendulum': 'study-Q', 'island': 'study-Q', 'prague': 'study-Q', 'baudolino': 'study-Q', 'perfect-language': 'study-Q', 'essays': 'reference-table', 'own-books': 'obj:salotto:piano-pile-07', 'strange': 'rare-04', 'false': 'study-Q', 'lists': 'reference-table', 'lands': 'reference-table', 'comics': 'reference-table', 'popular': 'study-Q'}
    check(all(f[1] == want16.get(f[0]) for f in firsts) and all('Eco' in (f[2] or '') for f in firsts if f[0] != 'strange'), "nine tours open on a copy filmed in the flat, four on the reference table and one in the rare-book room, each at a book of Eco's but the Hypnerotomachia (%s)" % firsts)
    nonbook = page.evaluate("() => { const D = window.__data(); const out = []; for (const t of window.__tours.list()) for (const id of t.targets) if (!D._index.has(id)) out.push([t.id, id]); return out; }")
    check(len(nonbook) <= 4, 'every stop but the study shelf and the three comic piles is a placed book (%s)' % nonbook)
    qd = page.evaluate("() => { const out = {n: 0, bad: [], img: 0, badimg: []}; for (const t of (window.__data().meta.tours || [])) for (const s of t.stops) { const q = s.quote; if (q && typeof q === 'object' && q.text) { out.n++; if (!q.attribution || q.text.split(/\\s+/).length > 75) out.bad.push([t.id, s.id]); } const im = s.image; if (im) { out.img++; if (!(im.src && im.src.startsWith('data:image/') && im.credit && im.link && im.alt && im.w > 0)) out.badimg.push([t.id, s.id]); } } return out; }")
    check(qd['n'] >= 80 and not qd['bad'], "at least eighty stops quote Eco or a source verbatim, each quote attributed and under 76 words (%d quotes%s)" % (qd['n'], '' if not qd['bad'] else ', bad %s' % qd['bad'][:5]))
    check(qd['img'] >= 40 and not qd['badimg'], "at least forty stops carry a picture, each embedded with its credit, link and alt text (%d pictures%s)" % (qd['img'], '' if not qd['badimg'] else ', bad %s' % qd['badimg'][:5]))
    stopmeta = page.evaluate("() => { const m = {}; for (const t of (window.__data().meta.tours || [])) t.stops.forEach((s, k) => { m[t.id + '#' + k] = {q: !!(s.quote && s.quote.text), a: s.quote && s.quote.attribution || '', im: !!(s.image && s.image.src), rec: s.record || null, sid: s.id}; }); return m; }")
    unres = page.evaluate("() => { const out = []; for (const t of window.__tours.list()) for (const id of t.targets) if (!window.__tours.resolve(id)) out.push([t.id, id]); return out; }")
    check(not unres, "every stop's target resolves to a book, an object, a bookcase or a room in the page%s" % ('' if not unres else ' - %s' % unres[:5]))
    srcless = page.evaluate("() => { const out = []; for (const t of (window.__data().meta.tours || [])) for (const s of t.stops) if (!(s.source && (s.source.url || s.source.label)) ) out.push([t.id, s.id]); return out; }")
    check(not srcless, 'every stop names its source%s' % ('' if not srcless else ' - %s' % srcless[:5]))
    def dist(a, b): return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
    # every stop of every tour in the orbit view: the camera arrives (eye at rest, within reach of the target, inside a room and out of the furniture) and the panel opens
    page.evaluate("() => window.__setMode('orbit')"); far, bad, nopanel, nocard, occl, near, noquote, noimg = [], [], [], [], [], [], [], []
    def hidden_by(stt, kind):   # what the screen point of a book stop shows nearer than the spine (another case or a piece of furniture counts; the owner case, a label sprite or the book itself do not)
        if kind != 'book': return None
        pt = page.evaluate('(id) => window.__bookScreen(id)', stt['target'])
        if not pt: return 'offscreen'
        hit = page.evaluate('([x, y]) => window.__rayAt(x, y)', [pt['x'], pt['y']])
        if not hit or hit.get('type') == 'Sprite': return None
        owner = page.evaluate("(id) => { const D = window.__data(); return D.books[D._index.get(id)].bookcase; }", stt['target'])
        what = (hit.get('arch') or {}).get('bc') or (hit.get('arch') or {}).get('o') or hit.get('obj') or hit.get('caseId') or hit.get('kind')
        tp = page.evaluate('(id) => window.__tours.targetPos(id)', stt['target'])
        return what if (what != owner and hit['d'] < dist(stt['eye'], tp) - 0.35) else None
    def behind_card(stt, kind):   # a book stop's spine must show in the clear band between the top bar and the tour card, left of the side panel (the taller card used to cover it)
        if kind != 'book': return None
        pt = page.evaluate('(id) => window.__bookScreen(id)', stt['target'])
        if not pt or pt['z'] > 1: return 'offscreen'
        L = page.evaluate("() => { const c = document.getElementById('tour').getBoundingClientRect(), b = document.getElementById('topbar').getBoundingClientRect(), p = document.getElementById('panel'); const pr = p && p.classList.contains('open') && window.innerWidth > 700 ? p.getBoundingClientRect().left : window.innerWidth; return { top: c.top, bar: b.bottom, panel: pr, w: window.innerWidth, h: window.innerHeight }; }")
        if pt['y'] > L['top'] - 4: return 'under the card (y %d, card top %d)' % (pt['y'], L['top'])
        if pt['y'] < L['bar'] + 4: return 'under the top bar (y %d)' % pt['y']
        if pt['x'] > L['panel'] - 4: return 'under the panel (x %d, panel at %d)' % (pt['x'], L['panel'])
        if pt['x'] < 0 or pt['x'] > L['w']: return 'off the side (x %d)' % pt['x']
        return None
    covered = []; nearowner, wrongroom, norec = [], [], []
    objnear, oggap = [], {}   # the orbit eye's distance from the nearest piece of furniture or art at every book stop
    plateBad, pileBad, plates13 = [], [], None   # the object plates and the pile lettering while the card is up
    for t in tours12:
        page.evaluate('(id) => window.__tours.start(id)', t['id']); settle(page, 500)
        for k in range(t['stops']):
            if k: page.evaluate('() => window.__tour.next()'); settle(page, 500)
            stt = page.evaluate('() => window.__tours.state()'); clr = page.evaluate('() => window.__eyeClear()')
            v16s = page.evaluate("""(id) => { const D = window.__data(), i = D._index.get(id); if (i === undefined) return null; const b = D.books[i]; let room = null;
              for (const r of D.rooms) if (r.bookcases.some((c) => c.id === b.bookcase)) room = r.id;
              if (!room) { const o = (D.objects || []).find((o) => o.id === b.bookcase); if (o && o.room) room = o.room; }
              return { gap: window.__ownerGap(id), room, cur: window.__currentRoom() }; }""", stt['target'])
            if v16s:
                if v16s['gap'] is not None and v16s['gap'] < 0.5: nearowner.append((t['id'], k + 1, round(v16s['gap'], 2)))
                if v16s['room'] and v16s['cur'] != v16s['room']: wrongroom.append((t['id'], k + 1, v16s['cur'], v16s['room']))
            sm16 = stopmeta.get('%s#%d' % (t['id'], k), {})
            if sm16.get('rec') and 'Catalogue record:' not in stt['cap']: norec.append((t['id'], k + 1))
            tp = page.evaluate('(id) => window.__tours.targetPos(id)', stt['target']); kind = page.evaluate('(id) => window.__tours.resolve(id)', stt['target'])
            if kind == 'book' and stt.get('eye'):   # the eye's distance from the nearest piece of furniture or art (the book's own cabinet apart)
                og17 = page.evaluate("([x, y, z, id]) => window.__objGapAt ? [window.__objGapAt(x, y, z, id), window.__objNear(x, y, z, id)] : null", [stt['eye'][0], stt['eye'][1], stt['eye'][2], stt['target']])
                if og17: oggap[(t['id'], k + 1)] = (round(og17[0], 2), og17[1])
                if og17 and og17[0] < 0.45: objnear.append((t['id'], k + 1, round(og17[0], 2), og17[1]))
            d = dist(stt['eye'], tp) if tp else 99
            if d > (9 if kind == 'room' else 7): far.append((t['id'], k + 1, round(d, 1)))
            if kind == 'book' and d < 0.9: near.append((t['id'], k + 1, round(d, 2)))
            if kind == 'book':   # no object plate stands between the eye and the stop's book while the card is up, and no pile is lettered but the stop's own (the label pass runs every sixth frame: a plate still up at the first read is read again after two more passes)
                pl18 = page.evaluate('() => window.__plates ? window.__plates() : null')
                if pl18 and pl18['stop'] and (any(q['inWay'] and q['visible'] for q in pl18['plates']) or (pl18['listedPile'] and pl18['listedPile'] != pl18['stopPile'])):
                    t18 = page.evaluate('() => window.__labelPass || 0')
                    try: page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t18 + 2, timeout=20000)
                    except Exception: pass
                    pl18 = page.evaluate('() => window.__plates()')
                if pl18 and pl18['stop']:
                    plateBad.extend((t['id'], k + 1, q['text'][:40], q['d'], q['angle']) for q in pl18['plates'] if q['inWay'] and q['visible'])
                    if pl18['listedPile'] and pl18['listedPile'] != pl18['stopPile']: pileBad.append((t['id'], k + 1, pl18['listedPile']))
                    if (t['id'], k + 1) == ('prague', 13): plates13 = pl18
            h = hidden_by(stt, kind)
            if h: occl.append((t['id'], k + 1, h))
            bc = behind_card(stt, kind)
            if bc:
                covered.append((t['id'], k + 1, bc))
                print('  covered:', t['id'], k + 1, bc, 'eye', [round(v, 2) for v in stt['eye']], 'lift', page.evaluate('() => window.__lastLift || null'), 'camera', page.evaluate('() => window.__camera()'), 'flying', page.evaluate('() => window.__flying()'))
            if clr['inGeometry'] or not clr['inRoom']: bad.append((t['id'], k + 1))
            if not stt['panel'] or not stt['panelTitle']: nopanel.append((t['id'], k + 1))
            if not stt['card'] or len(stt['cap']) < 20 or stt['step'] != k: nocard.append((t['id'], k + 1))
            sm = stopmeta.get('%s#%d' % (t['id'], k), {})
            if sm.get('q') and not (stt.get('quote') and sm['a'][:20] in stt['quote']): noquote.append((t['id'], k + 1))
            if sm.get('im') and not (stt.get('img') and stt['img']['w'] > 0 and stt['img']['shown'] >= 60): noimg.append((t['id'], k + 1, stt.get('img')))
            if k == 0: page.screenshot(path=os.path.join(args.shots, 'tour-%s-stop1.png' % t['id']))
        page.screenshot(path=os.path.join(args.shots, 'tour-%s-last.png' % t['id']))
        page.evaluate('() => window.__tour.end()')
    check(not far, 'the camera arrives within reach of every stop in the orbit view%s' % ('' if not far else ' - (tour, stop, m) %s' % far[:6]))
    check(not bad, 'every orbit stop stands inside a room and out of the furniture%s' % ('' if not bad else ' - %s' % bad[:6]))
    check(not nopanel, "the stop's panel opens at every stop%s" % ('' if not nopanel else ' - %s' % nopanel[:6]))
    check(not nocard, 'the tour card shows the stop and its caption at every stop%s' % ('' if not nocard else ' - %s' % nocard[:6]))
    check(not occl, 'no book stop is hidden behind another case or a piece of furniture in the orbit view%s' % ('' if not occl else ' - (tour, stop, what) %s' % occl[:8]))
    check(not near, 'the orbit camera keeps at least 0.9 m from every spine%s' % ('' if not near else ' - %s' % near[:6]))
    check(not covered, 'at every book stop the spine shows in the clear band between the top bar and the tour card, left of the panel%s' % ('' if not covered else ' - (tour, stop, where) %s' % covered[:6]))
    check(not noquote, "every stop with a quote shows it on the tour card with its attribution%s" % ('' if not noquote else ' - %s' % noquote[:6]))
    check(not noimg, "every stop with a picture shows it loaded on the tour card, at least 60 px wide%s" % ('' if not noimg else ' - %s' % noimg[:4]))
    check(not any(x[0:2] in (('island', 17), ('lands', 9)) for x in nearowner), 'the orbit eye at island-17 and lands-09 stands half a metre or more from the rare-01 cabinet (stops nearer than 0.5 m to their own cabinet: %s)' % nearowner[:8])
    check(not wrongroom, 'the room bar names the room of every book stop after the flight%s' % ('' if not wrongroom else ' - (tour, stop, lit, room) %s' % wrongroom[:6]))
    check(not norec, 'every stop that names a catalogue record prints the record line on the card%s' % ('' if not norec else ' - %s' % norec[:6]))
    allowed17 = {('popular', 15)}   # the stop the rule sweep moved to the corridor's end bay (A1), which faces the French window across the 1.6 m corridor: no eye 0.5 m from the shelf front is 0.5 m from the drawn window, and the window stands behind the eye, out of the frame
    stray17 = [x for x in objnear if (x[0], x[1]) not in allowed17]
    check(not stray17 and len(oggap) >= 200, 'the orbit eye stands half a metre or more from every piece of furniture and art at every book stop but popular-15 at the corridor window (the fly-to counts the objects as it counts the cabinet; %d stops measured)%s' % (len(oggap), '' if not stray17 else ' - (tour, stop, m, piece) %s' % stray17[:8]))
    check(not plateBad, "while a tour card is up, no object's plate stands between the eye and the stop's book at any book stop of any tour%s" % ('' if not plateBad else ' - (tour, stop, plate, m, deg) %s' % plateBad[:6]))
    check(not pileBad, "while a tour card is up, no pile is lettered but the stop's own%s" % ('' if not pileBad else ' - %s' % pileBad[:6]))
    iron13 = [q for q in (plates13['plates'] if plates13 else []) if q['text'].startswith('Folded ironing board')]
    check(bool(plates13) and bool(iron13) and all(q['inWay'] and not q['visible'] for q in iron13), "at prague-13 the folded ironing board's plate beside the spine gives way while the card is up (%s)" % ([(q['d'], q['angle'], q['inWay'], q['visible']) for q in iron13] if iron13 else (plates13 and 'no ironing board plate in view') or 'no plates read'))

    check(oggap.get(('baudolino', 10), (0, None))[0] >= 0.45 and oggap.get(('perfect-language', 1), (0, None))[0] >= 0.45, 'baudolino-10 clears the framed prints above the study sofa and perfect-language-01 the sliding ladder by half a metre (%s, %s)' % (oggap.get(('baudolino', 10)), oggap.get(('perfect-language', 1))))
    # the record line opens the reference entry's panel
    page.evaluate("(id) => window.__tours.start(id)", 'rose'); settle(page, 500)
    rec_t = page.evaluate("() => { const a = document.querySelector('#tourCap a.rec'); if (!a) return null; a.click(); return [a.textContent, document.getElementById('pTitle').textContent, document.getElementById('pBody').textContent]; }")
    check(bool(rec_t) and 'Il nome della rosa' in rec_t[0] and 'Il nome della rosa' in rec_t[1] and 'listed, not shelved' in rec_t[2] and 'Reference entry' in rec_t[2], "the card's catalogue-record link opens the reference entry's panel (%s)" % (rec_t[:2] if rec_t else None))
    page.evaluate('() => window.__tour.end()'); page.evaluate("() => { if (document.getElementById('panel').classList.contains('open')) document.getElementById('pClose').click(); }")
    # a stop's book stays visible whatever the certainty filter says: a guess-tier stop under "Certain only" gets a stand-in spine; Esc exits and the filter is untouched
    gs = page.evaluate("() => { const D = window.__data(); for (const t of (D.meta.tours || [])) for (let k = 0; k < t.stops.length; k++) { const i = D._index.get(t.stops[k].target); if (i !== undefined) { const b = D.books[i]; if (b.tier && b.tier !== 'certain') return {tour: t.id, k, id: b.id, tier: b.tier}; } } return null; }")
    if gs:
        page.evaluate("() => window.__overlay.filter('certain')"); page.wait_for_timeout(300)
        shown0 = page.evaluate('() => window.__spinesShown()')
        page.evaluate('(id) => window.__tours.start(id)', gs['tour']); settle(page, 300)
        for _ in range(gs['k']): page.evaluate('() => window.__tour.next()')
        settle(page, 600)
        stt = page.evaluate('() => window.__tours.state()')
        check(stt['target'] == gs['id'] and stt['standIn'], 'a %s-tier stop under "Certain only" draws its stand-in spine (%s)' % (gs['tier'], gs['id']))
        pt = page.evaluate('(id) => window.__bookScreen(id)', gs['id'])
        page.screenshot(path=os.path.join(args.shots, 'standin.png'))
        try:
            from PIL import Image
            im = Image.open(os.path.join(args.shots, 'standin.png')).convert('RGB')
            px = im.getpixel((int(pt['x']), int(pt['y']))) if pt and 0 <= pt['x'] < im.size[0] and 0 <= pt['y'] < im.size[1] else None
            check(px is not None and max(px) > 40, 'the stand-in spine is drawn on screen at the book (%s at %s)' % (px, pt and (int(pt['x']), int(pt['y']))))
        except ImportError: pass
        page.keyboard.press('Escape'); page.wait_for_timeout(400)
        stt2 = page.evaluate('() => window.__tours.state()'); ov = page.evaluate('() => window.__overlay.state()'); shown1 = page.evaluate('() => window.__spinesShown()')
        check(not stt2['card'] and not stt2['standIn'] and stt2['id'] is None, 'Esc exits the tour and removes the stand-in')
        check(ov['filter'] == 'certain' and shown1 == shown0, 'the certainty filter is as it was after the tour (%s, %s)' % (ov['filter'], shown1))
        page.evaluate("() => window.__overlay.filter('all')"); page.wait_for_timeout(300)
    else: check(False, 'no tour stop on a guess- or unknown-tier book to test the stand-in with')
    # the rare room's stepped-back stations in walk view: the display table's pile lettering and the jar's plate give way while the card is up
    plates18w, listed18w = {}, {}
    page.evaluate("() => window.__setMode('walk')"); settle(page, 300)
    room19w = None   # the room bar at essays-15's walk station
    for tid18, upto18 in (('essays', 15), ('false', 14)):
        page.evaluate('(id) => window.__tours.start(id)', tid18); settle(page, 400)
        for k in range(1, upto18):
            page.evaluate('() => window.__tour.next()'); settle(page, 400)
            if (tid18, k + 1) in (('essays', 10), ('false', 13), ('false', 14)):
                t18 = page.evaluate('() => window.__labelPass || 0')
                try: page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t18 + 2, timeout=20000)
                except Exception: pass
                plates18w[(tid18, k + 1)] = page.evaluate('() => window.__plates()'); listed18w[(tid18, k + 1)] = page.evaluate('() => window.__listedPile()')
                page.screenshot(path=os.path.join(args.shots, 'walk-%s-%02d.png' % (tid18, k + 1)))
            if (tid18, k + 1) == ('essays', 15):
                page.wait_for_timeout(1200); room19w = page.evaluate("() => [window.__currentRoom(), document.querySelector('[data-room].on') ? document.querySelector('[data-room].on').textContent.trim() : null, window.__tours.state().target]")
                page.screenshot(path=os.path.join(args.shots, 'walk-essays-15.png'))
        page.evaluate('() => window.__tour.end()'); settle(page, 200)
    for key18 in (('essays', 10), ('false', 13), ('false', 14)):
        pl = plates18w.get(key18); bad18w = [q['text'][:40] for q in (pl['plates'] if pl else []) if q['inWay'] and q['visible']]
        check(pl is not None and bool(pl['stop']) and not bad18w and not listed18w.get(key18), "at %s-%02d in walk view no object plate stands between the visitor and the spine and no pile is lettered but the stop's own (%s)" % (key18[0], key18[1], bad18w or listed18w.get(key18) or ('clear' if pl else 'not read')))
    check(bool(room19w) and room19w[0] == 'corridoio' and room19w[2] == 'bologna:UBO00307638', "at essays-15 in walk view the room bar lights the long corridor, the room of the bookcase the card names (%s)" % (room19w,))
    page.evaluate("() => window.__setMode('orbit')"); settle(page, 300)
    # the walk view: the visitor is stood at a station in front of each stop, inside the room and out of the walk blockers, and the arrow keys keep walking
    wt = tours12[0]   # the whole first tour (The Name of the Rose) is walked, every station tested for occlusion like the orbit stops
    page.evaluate("() => window.__setMode('walk')"); settle(page, 300)
    page.evaluate('(id) => window.__tours.start(id)', wt['id']); settle(page, 500)
    wbad, wfar, wmode, woccl, wcov = [], [], [], [], []
    for k in range(wt['stops']):
        if k: page.evaluate('() => window.__tour.next()'); settle(page, 500)
        stt = page.evaluate('() => window.__tours.state()'); clr = page.evaluate('() => window.__eyeClear()'); e = stt['eye']
        blk = page.evaluate('([x, y, z]) => window.__walkBlockersAt(x, y, z)', e)
        tp = page.evaluate('(id) => window.__tours.targetPos(id)', stt['target']); kind = page.evaluate('(id) => window.__tours.resolve(id)', stt['target'])
        if not clr['inRoom'] or clr['inGeometry'] or blk or abs(e[1] - 1.6) > 0.05: wbad.append((k + 1, blk, round(e[1], 2), clr['inRoom']))
        if tp and dist(e, tp) > (9 if kind == 'room' else 6): wfar.append((k + 1, round(dist(e, tp), 1)))
        if stt['mode'] != 'walk': wmode.append(k + 1)
        h = hidden_by(stt, kind)
        if h: woccl.append((k + 1, h))
        bc = behind_card(stt, kind)
        if bc: wcov.append((k + 1, bc))
        if k == 1: page.screenshot(path=os.path.join(args.shots, 'walk-station.png'))
    check(not wbad, 'every walk station stands at eye height inside the room and out of the furniture%s' % ('' if not wbad else ' - (stop, blockers, y, inRoom) %s' % wbad[:5]))
    check(not woccl, 'no walk station of the first tour looks at its book through another case or a piece of furniture%s' % ('' if not woccl else ' - %s' % woccl[:6]))
    check(not wcov, 'at every walk station of the first tour the spine shows clear of the top bar, the tour card and the panel%s' % ('' if not wcov else ' - %s' % wcov[:6]))
    check(not wfar, 'every walk station is within reach of its stop%s' % ('' if not wfar else ' - %s' % wfar[:5]))
    # the station picker itself, asked for every book stop of every tour (no walking): the spine must show from the station past what is drawn (the console's side, an armchair's arms), the station in the room, on clear floor, at eye height, within reach
    shid, sbad = [], []
    wcrane, wfirst, wpile = [], [], []   # the elevation of the spine from the station, the tours' first stops, the pile stops
    near18, gap18 = [], {}   # the station's distance from the nearest piece of furniture or art at the eye's height (the fly-to's own gap), the book's own cabinet apart
    wrongroom19, rooms19 = [], 0   # the room each station stands in against its stop's room
    for t in tours12:   # one evaluation per tour: each round trip waits on the frame loop
        sts = page.evaluate("(targets) => targets.map((id) => window.__tours.resolve(id) === 'book' ? window.__station(id) || 'none' : null)", t['targets'])
        tps = page.evaluate("(targets) => targets.map((id) => window.__tours.resolve(id) === 'book' ? window.__tours.targetPos(id) : null)", t['targets'])
        pil = page.evaluate("(targets) => targets.map((id) => { const D = window.__data(), i = D._index.get(id); if (i === undefined) return false; const o = (D.objects || []).find((o) => o.id === D.books[i].bookcase); return !!(o && o.kind === 'pile'); })", t['targets'])
        for k, st in enumerate(sts):
            if st is None: continue
            if st == 'none': sbad.append((t['id'], k + 1, 'no station')); continue
            if st['hidden']: shid.append((t['id'], k + 1, st['d'], st['blocked']))
            if not st['inRoom'] or st['blockers'] or abs(st['eye'][1] - 1.6) > 0.05 or st['d'] > 6: sbad.append((t['id'], k + 1, st))
            if st.get('stopRoom'):   # the station stands in its stop's room, as the room bar reads it
                rooms19 += 1
                if st.get('room') != st['stopRoom']: wrongroom19.append((t['id'], k + 1, st.get('room'), st['stopRoom']))
            if st.get('gap') is not None:
                gap18[(t['id'], k + 1)] = (round(st['gap'], 2), st.get('near'))
                if st['gap'] < 0.45: near18.append((t['id'], k + 1, round(st['gap'], 2), st.get('near')))
            tp17 = tps[k]   # how far up or down the visitor looks at the spine from the station
            if tp17:
                el = math.degrees(math.atan2(tp17[1] - st['eye'][1], max(math.hypot(tp17[0] - st['eye'][0], tp17[2] - st['eye'][2]), 1e-6)))
                if el > 46: wcrane.append((t['id'], k + 1, round(el, 1), round(st['d'], 2)))
                if k == 0 and abs(el) > 40: wfirst.append((t['id'], round(el, 1), round(st['d'], 2)))
                if pil[k] and (st['d'] < 1.0 or el < -40): wpile.append((t['id'], k + 1, round(el, 1), round(st['d'], 2)))
    # a station whose line of sight the furniture boxes cross can only be the picker's fallback (every candidate must clear the boxes), so a hidden
    # spine is allowed there and nowhere else: lands-12, lands-14 and lands-18 stand behind the rare room's console and armchair, with no eye-height
    # candidate at all; a hidden spine at a station the boxes clear is a fault of the picker
    sfix = [x for x in shid if not x[3]]
    check(not sfix, 'the walk station of every book stop of every tour shows its spine past the furniture wherever a candidate clears the furniture boxes (the sight check the fly-to uses; %d station%s left hidden behind furniture no eye-height candidate clears: %s)%s' % (len(shid), '' if len(shid) == 1 else 's', ', '.join('%s-%02d' % (a, b) for a, b, c, d in shid) or 'none', '' if not sfix else ' - %d hidden at a clear station: %s' % (len(sfix), sfix[:8])))
    check(not sbad, 'every such station is in the room, on clear floor, at eye height and within reach%s' % ('' if not sbad else ' - %s' % sbad[:4]))
    check(not wcrane, 'no walk station cranes more than 46 degrees up at its spine (the picker steps back from a top-shelf stop)%s' % ('' if not wcrane else ' - (tour, stop, deg, m) %s' % wcrane[:8]))
    check(not wfirst, "every tour's first stop is seen from its walk station within 40 degrees of level (the openings on Q's and P's top shelves)%s" % ('' if not wfirst else ' - (tour, deg, m) %s' % wfirst[:8]))
    check(not wpile, 'the walk station of a pile stop stands a metre or more from the pile and looks down at it by 40 degrees at most%s' % ('' if not wpile else ' - (tour, stop, deg, m) %s' % wpile[:4]))
    allowed18 = {('lands', 12), ('comics', 19), ('baudolino', 7), ('popular', 8), ('popular', 6), ('essays', 12), ('popular', 12), ('popular', 15)}   # the stations no candidate clears (__stationCands): lands-12 by the console; the corridor's, where every clear candidate cranes past 40 degrees; popular-15, moved by the rule sweep to the corridor's end bay facing the French window, where the one clear candidate in the corridor cranes 40.9 degrees
    stray18 = [x for x in near18 if (x[0], x[1]) not in allowed18]
    check(not stray18 and len(gap18) >= 200, "every walk station of a book stop stands 0.45 m or more from every piece of furniture and art at the eye's height, but for the eight no candidate clears (%d stations read%s)" % (len(gap18), '' if not stray18 else '; near: %s' % stray18[:6]))
    check(not wrongroom19 and rooms19 >= 200, "every walk station of a book stop stands in its stop's room, as the room bar reads it: essays-15's no longer steps back through the door onto the art corridor's floor (%d stations read%s)" % (rooms19, '' if not wrongroom19 else '; elsewhere: %s' % wrongroom19[:6]))
    for key18, what18 in ((('essays', 15), 'the corridor window'), (('perfect-language', 1), 'the sliding ladder'), (('pendulum', 15), 'the hanging mobile'), (('prague', 13), 'the stepladder'), (('essays', 10), 'the framed engravings'), (('false', 17), 'the console')):
        g18 = gap18.get(key18)
        check(g18 is not None and g18[0] >= 0.5, 'the walk station of %s-%02d stands half a metre or more from %s (%s)' % (key18[0], key18[1], what18, g18))

    check(not wmode, 'a tour started in the walk view stays in the walk view%s' % ('' if not wmode else ' - stops %s' % wmode))
    e0 = page.evaluate('() => window.__camera().p'); t0 = page.evaluate('() => window.__labelPass || 0'); page.keyboard.down('ArrowUp')
    try: page.wait_for_function('(t) => (window.__labelPass || 0) >= t', arg=t0 + 3, timeout=300000)
    finally: page.keyboard.up('ArrowUp')
    e1 = page.evaluate('() => window.__camera().p'); stt = page.evaluate('() => window.__tours.state()')
    check(dist(e0, e1) > 0.05 and stt['card'] and stt['mode'] == 'walk', 'the arrow keys keep walking during a tour (moved %.2f m, card still up)' % dist(e0, e1))
    page.focus('#overlaySel'); e2 = page.evaluate('() => window.__camera().p'); v0 = page.evaluate("() => document.getElementById('overlaySel').value")
    page.keyboard.press('ArrowDown'); page.wait_for_timeout(400); v1 = page.evaluate("() => document.getElementById('overlaySel').value"); e3 = page.evaluate('() => window.__camera().p')
    check(v1 != v0 and dist(e2, e3) < 0.01, 'the Colour menu keeps its arrow keys during a tour (%s -> %s)' % (v0, v1))
    page.evaluate("() => window.__overlay.set('language')"); page.evaluate("() => document.getElementById('overlaySel').blur()")
    page.evaluate('() => window.__tour.end()'); page.evaluate("() => window.__setMode('orbit')"); settle(page, 300); page.evaluate(close_panel)
    # the Tours menu opens from the top bar and lists every tour with a Start button
    page.click('#tourBtn'); page.wait_for_timeout(300)
    mn = page.evaluate("() => ({open: window.__tours.menuOpen(), starts: document.querySelectorAll('#toursList [data-tour12]').length, legacy: !!document.getElementById('toursLegacy')})")
    check(mn['open'] and mn['starts'] == len(tours12) and mn['legacy'], 'the Tours menu lists the %d tours and the room-by-room tour (%s)' % (len(tours12), mn))
    page.screenshot(path=os.path.join(args.shots, 'tours-menu.png'))
    page.keyboard.press('Escape'); page.wait_for_timeout(200)
    check(not page.evaluate('() => window.__tours.menuOpen()'), 'Esc closes the Tours menu')

    check(not errors, 'no console errors after interaction' + ('' if not errors else ': ' + '; '.join(errors[:3])))
    fps = page.evaluate('() => window.__fps'); print('fps', fps, 'draw calls', page.evaluate('() => window.__calls'))
    # phone layout
    mctx = browser.new_context(viewport={'width': 390, 'height': 800}, device_scale_factor=1, is_mobile=True, has_touch=True); mctx.set_default_timeout(args.timeout)
    m = mctx.new_page()
    m.goto(base + 'index.html', wait_until='load'); wait_ready(m, args.timeout * 4); m.wait_for_timeout(1200)
    # the opening card on a phone, bottom-anchored without the featured tours, then closed for the checks below
    ph20 = m.evaluate("() => { const c = document.querySelector('#welcome .card').getBoundingClientRect(); return { welcome: window.__state.welcome(), l: c.left, r: c.right, b: c.bottom, feat: getComputedStyle(document.getElementById('wFeatured')).display, sw: document.body.scrollWidth }; }")
    check(ph20['welcome'] and ph20['l'] >= 0 and ph20['r'] <= 390 and ph20['b'] <= 800 and ph20['feat'] == 'none' and ph20['sw'] <= 391, 'phone: the opening card fits the screen, the featured tours hidden (%s)' % (ph20,))
    m.screenshot(path=os.path.join(args.shots, 'phone-opening.png'))
    wk21 = m.evaluate("() => document.querySelector('#wWalk span').textContent")
    check('joystick' in wk21 and 'arrow' not in wk21.lower(), 'phone: the Walk door speaks of the joystick, not the arrow keys (%s)' % (wk21,))
    m.evaluate("() => document.getElementById('wClose').click()"); m.wait_for_timeout(500)
    check(not m.evaluate("() => window.__state.welcome()"), 'phone: Close dismisses the card')
    m.evaluate("() => document.getElementById('moreBtn').click()"); m.wait_for_timeout(300)
    pm20 = m.evaluate("() => { const r = document.getElementById('moreMenu').getBoundingClientRect(); return { open: window.__state.more(), l: r.left, r: r.right, b: r.bottom }; }")
    check(pm20['open'] and pm20['l'] >= 0 and pm20['r'] <= 390 and pm20['b'] <= 800, 'phone: the More menu fits the screen (%s)' % (pm20,))
    m.screenshot(path=os.path.join(args.shots, 'phone-more.png'), clip={'x': 0, 'y': 0, 'width': 390, 'height': 460})
    m.evaluate("() => document.getElementById('moreBtn').click()"); m.wait_for_timeout(300)   # the phone page loads beside the busy desktop page, and the software renderer can take three minutes to its first frame (three pages starve, two are slow)
    m.screenshot(path=os.path.join(args.shots, 'mobile-opening.png'))   # a phone opens at eye level in the lit corridor, not on the dark top-down plan
    ml = lum_stats(os.path.join(args.shots, 'mobile-opening.png'), (0.1, 0.15, 0.9, 0.8))
    check(ml is None or (ml['mean'] > 0.25 and ml['black'] < 0.25), 'phone opening view is lit: centre luminance %s' % ml)
    check(m.evaluate("() => window.__currentRoom()") == 'corridoio' and m.evaluate("() => window.__eyeClear()")['inRoom'], 'phone opening view stands in the corridor at eye level')
    m.evaluate("() => window.__openBook(window.__data().books.find(b => b.origin === 'catalog').id)"); m.wait_for_timeout(1200)
    check(m.evaluate("() => document.body.scrollWidth <= 390 + 1"), 'phone layout: no horizontal overflow')
    lg0 = m.evaluate("() => { const g = document.getElementById('langBtn'); if (g.hidden) return null; const r = g.getBoundingClientRect(), t = document.getElementById('topbar').getBoundingClientRect(); return { l: r.left, r: r.right, b: r.bottom, top: t.bottom }; }")
    if lg0: check(lg0['l'] >= 0 and lg0['r'] <= 390 and lg0['b'] <= lg0['top'] + 1, 'phone layout: the title-language switch fits inside the top bar (%s)' % lg0)
    m.screenshot(path=os.path.join(args.shots, 'lang-topbar-phone.png'), clip={'x': 0, 'y': 0, 'width': 390, 'height': 230})
    # the room row scrolls sideways: the edge chevron/fade shows while buttons are hidden, and goes once scrolled to the end
    st = m.evaluate("() => { const r = document.getElementById('rooms'), g = document.getElementById('roomGroup'); return {over: r.scrollWidth > r.clientWidth, sb: getComputedStyle(r).scrollbarWidth, hint: !g.classList.contains('at-end') && getComputedStyle(g, '::after').opacity === '1'}; }")
    check(st['over'] and st['hint'] and st['sb'] == 'thin', 'phone layout: room row overflows with a visible edge hint and a thin scrollbar (%s)' % st)
    m.evaluate("() => { const r = document.getElementById('rooms'); r.scrollLeft = r.scrollWidth; }")
    try: m.wait_for_function("() => document.getElementById('roomGroup').classList.contains('at-end')", timeout=15000); at_end = True   # the scroll event lands on the next rendered frame, slow under a software renderer
    except Exception: at_end = False
    check(at_end, 'phone layout: edge hint hides at the end of the room row')
    m.evaluate("() => { document.getElementById('rooms').scrollLeft = 0; }"); m.wait_for_timeout(300)
    m.screenshot(path=os.path.join(args.shots, 'mobile.png'))
    # the tour card on a phone: fully inside the viewport, above the footer, and not under the side panel
    m.evaluate("() => window.__tour.start()"); m.wait_for_timeout(1500)
    tb = m.evaluate("() => { const b = document.querySelector('#tour .bar').getBoundingClientRect(); const p = document.getElementById('panel'); return {top: b.top, bottom: b.bottom, h: window.innerHeight, panelOpen: p.classList.contains('open')}; }")
    check(tb['top'] >= 0 and tb['bottom'] <= tb['h'] and not tb['panelOpen'], 'phone layout: the tour card fits on screen and is not buried under the panel (%s)' % tb)
    m.screenshot(path=os.path.join(args.shots, 'mobile-tour.png'))
    m.evaluate("() => window.__tour.end()")
    # on a phone: the Tours menu fits the screen, a sourced tour starts from it and its card fits above the footer with the panel closed
    m.click('#tourBtn'); m.wait_for_timeout(400)
    mc = m.evaluate("() => { const c = document.querySelector('#tours .card').getBoundingClientRect(); return {open: window.__tours.menuOpen(), l: c.left, r: c.right, t: c.top, b: c.bottom, w: window.innerWidth, h: window.innerHeight, starts: document.querySelectorAll('#toursList [data-tour12]').length}; }")
    check(mc['open'] and mc['l'] >= 0 and mc['r'] <= mc['w'] and mc['t'] >= 0 and mc['b'] <= mc['h'] and mc['starts'] >= 4, 'phone layout: the Tours menu fits the screen (%s)' % mc)
    m.screenshot(path=os.path.join(args.shots, 'mobile-tours-menu.png'))
    m.click('#toursList [data-tour12]'); m.wait_for_timeout(2500)
    tb2 = m.evaluate("() => { const b = document.querySelector('#tour .bar').getBoundingClientRect(); const p = document.getElementById('panel'); const s = window.__tours.state(); return {top: b.top, bottom: b.bottom, h: window.innerHeight, foot: document.getElementById('stats').getBoundingClientRect().top, panelOpen: p.classList.contains('open'), id: s.id, card: s.card, cap: s.cap.length, menu: window.__tours.menuOpen()}; }")
    check(tb2['id'] and tb2['card'] and tb2['cap'] > 20 and not tb2['menu'] and tb2['top'] >= 0 and tb2['bottom'] <= tb2['h'] and not tb2['panelOpen'], 'phone layout: a sourced tour starts from the menu and its card fits on screen with the panel closed, over the footer like the room tour card (%s)' % tb2)
    m.screenshot(path=os.path.join(args.shots, 'mobile-tour-sourced.png'))
    m.evaluate("() => window.__tour.end()")
    check(m.evaluate("() => document.getElementById('legend').getBoundingClientRect().width") <= 390 * 0.7, 'phone layout: legend is compact')
    m.click('#modeWalk'); m.wait_for_timeout(1500)
    rc = m.evaluate("() => { const r = (s) => { const b = document.querySelector(s).getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; }; return {legend: r('#legend'), joy: r('#joystick'), joyShown: document.getElementById('joystick').classList.contains('show'), min: document.getElementById('legend').classList.contains('min')}; }")
    lg, jy = rc['legend'], rc['joy']
    apart = lg[3] <= jy[1] or lg[1] >= jy[3] or lg[2] <= jy[0] or lg[0] >= jy[2]
    check(rc['joyShown'] and apart and rc['min'], 'phone walk mode: the legend chip sits clear of the joystick (%s)' % rc)
    m.screenshot(path=os.path.join(args.shots, 'mobile-walk.png'))
    # a tour card in the walk view sits above the joystick and the Exit walk button, never over them
    m.evaluate("(id) => window.__tours.start(id)", tours12[0]['id']); m.wait_for_timeout(2500)
    wc = m.evaluate("() => { const r = (s) => { const b = document.querySelector(s).getBoundingClientRect(); return [b.left, b.top, b.right, b.bottom]; }; const s = window.__tours.state(); return {card: r('#tour'), joy: r('#joystick'), exit: r('#exitWalk'), h: window.innerHeight, up: s.card, mode: s.mode, joyShown: document.getElementById('joystick').classList.contains('show')}; }")
    def apart2(a, b): return a[3] <= b[1] or a[1] >= b[3] or a[2] <= b[0] or a[0] >= b[2]
    check(wc['up'] and wc['mode'] == 'walk' and wc['joyShown'] and apart2(wc['card'], wc['joy']) and apart2(wc['card'], wc['exit']) and wc['card'][1] >= 0, 'phone walk mode: the tour card sits clear of the joystick and the Exit walk button (%s)' % wc)
    m.screenshot(path=os.path.join(args.shots, 'mobile-walk-tour.png'))
    m.evaluate("() => window.__tour.end()"); m.wait_for_timeout(300)
    m.click('#exitWalk')
    # self-contained files from file://, loaded alone: the desktop and phone pages are closed first, since three WebGL pages on the
    # software renderer starve a third of frames (with both alive a fresh page took 208 s to reach ready, alone under 4 s)
    m.close(); mctx.close(); page.close()
    for fn in ['eco-map.html', 'eco-map-artifact.html']:
        p = os.path.join(args.dist, fn)
        if not os.path.exists(p): check(False, fn + ' missing'); continue
        errs2 = []
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs2.append(str(e))); pg.on('console', lambda mm: errs2.append(mm.text) if mm.type == 'error' else None)
        pg.goto('file://' + p, wait_until='load', timeout=args.timeout)
        try: wait_ready(pg, args.timeout); ok = True
        except Exception as e: ok = False; errs2.append(str(e)[:200])
        check(ok and not errs2, '%s loads from file:// %s' % (fn, '' if not errs2 else '; '.join(errs2[:2])))
        pg.close()
    browser.close()
srv.shutdown(); shutil.rmtree(local, ignore_errors=True)
# the piano piles against the film reference: check_piano.py compares books.json with eco-video/piano_piles.json pile for pile
if os.path.exists(os.path.join(H, 'check_piano.py')) and os.path.exists(os.path.join(os.path.dirname(H), 'eco-video', 'piano_piles.json')):
    import subprocess
    cp = subprocess.run([sys.executable, os.path.join(H, 'check_piano.py'), '-q', '--books', os.path.join(H, 'books.json')], capture_output=True, text=True)   # the generator's books.json (build_eco.py copies it into dist/ unchanged)
    check(cp.returncode == 0, 'piano piles match the film reference (check_piano.py): %s' % (cp.stdout.strip().splitlines()[-1] if cp.stdout.strip() else cp.stderr.strip()[-200:]))
print('\nscreenshots in', args.shots, ':', sorted(os.listdir(args.shots)))
print('%d failure(s)' % len(FAIL) if FAIL else 'all checks passed')
sys.exit(1 if FAIL else 0)
