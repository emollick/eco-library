#!/usr/bin/env python3
"""Render preview.jpg, the picture the page's preview tags name (og:image, 1200 by 630), from the built page in headless Chromium.

  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 make_preview_eco.py [--dist dist] [--out preview.jpg] [--room antichi]

Serves dist/ locally, opens the loose page at 1200 by 630 with the opening card dismissed, flies to the room's tour view, waits for the
frame and writes a JPEG. build_eco.py copies preview.jpg into dist/ when it exists, and netlify/stage.py must stage it beside index.html.
The picture leaves out the footer, the hint box and the plates."""
import argparse, functools, glob, http.server, os, socketserver, threading, sys
H = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--dist', default=os.path.join(H, 'dist'))
ap.add_argument('--out', default=os.path.join(H, 'preview.jpg'))
ap.add_argument('--room', default='antichi')
ap.add_argument('--quality', type=int, default=84)
args = ap.parse_args()
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', '/opt/pw-browsers')
from playwright.sync_api import sync_playwright
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=args.dist); Handler.log_message = lambda *a, **k: None
class Srv(socketserver.TCPServer): allow_reuse_address = True
srv = Srv(('127.0.0.1', 0), Handler); port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
exe = os.environ.get('PW_CHROMIUM') or (sorted(glob.glob(os.path.join(os.environ['PLAYWRIGHT_BROWSERS_PATH'], 'chromium-*/chrome-linux/chrome'))) or [None])[-1]
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path=exe, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--no-sandbox'])
    ctx = br.new_context(viewport={'width': 1200, 'height': 630}, device_scale_factor=1); ctx.set_default_timeout(240000)
    page = ctx.new_page()
    page.goto('http://127.0.0.1:%d/index.html#room=%s' % (port, args.room), wait_until='load')   # a room in the address: no opening card, the room's view
    page.wait_for_function('window.__ready === true'); page.wait_for_function('window.__fps > 0')
    try: page.wait_for_function('!window.__flying()', timeout=60000)
    except Exception: pass
    page.evaluate("() => { document.getElementById('topbar').style.visibility = 'hidden'; for (const id of ['legend', 'rooms', 'roomGroup', 'hud', 'help', 'fpsBox', 'stats', 'hint']) { const e = document.getElementById(id); if (e) e.style.visibility = 'hidden'; } window.__labelsOff = true; }")   # the footer, the hint and the plates stay out of the picture
    n0 = page.evaluate('() => window.__labelPass || 0')
    try: page.wait_for_function('(n) => (window.__labelPass || 0) >= n + 2', arg=n0, timeout=120000)   # two label passes, so the plates are gone from the frame that is drawn
    except Exception: pass
    page.wait_for_timeout(1500)
    png = args.out + '.png'; page.screenshot(path=png)
    br.close()
srv.shutdown()
from PIL import Image
im = Image.open(png).convert('RGB'); im.save(args.out, 'JPEG', quality=args.quality, optimize=True); os.remove(png)
print('wrote', args.out, im.size, os.path.getsize(args.out), 'bytes')
