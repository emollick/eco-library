// Usage: node verify.js <url> <screenshot.png>
const url = process.argv[2], shot = process.argv[3];
if (!url || !shot) { console.error('usage: node verify.js <url> <screenshot.png>'); process.exit(2); }
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('@playwright/test')); }
(async () => {
  const browser = await chromium.launch({ headless: true,
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  const errors = [], failed = [], responses = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => failed.push(r.url() + ' :: ' + (r.failure() && r.failure().errorText)));
  page.on('response', async r => {
    let size = null; try { const b = await r.body(); size = b.length; } catch (e) {}
    responses.push({ url: r.url(), status: r.status(), type: r.headers()['content-type'], size });
  });
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  let loadingState = 'unknown';
  try {
    await page.waitForFunction(() => {
      const l = document.getElementById('loading');
      return !l || l.classList.contains('err');
    }, null, { timeout: 60000 });
    loadingState = await page.evaluate(() => {
      const l = document.getElementById('loading');
      if (!l) return 'cleared';
      return 'error: ' + (document.getElementById('loadMsg') || {}).textContent;
    });
  } catch (e) { loadingState = 'timeout: still loading after 60s'; }
  await page.waitForTimeout(2500);
  const canvas = await page.evaluate(() => {
    const c = document.querySelector('canvas'); if (!c) return null;
    return { w: c.width, h: c.height, webgl: !!(c.getContext('webgl2') || c.getContext('webgl')) };
  });
  const title = await page.title();
  await page.screenshot({ path: shot });
  const wanted = responses.filter(r => /books\.json|vendor\//.test(r.url) || r.url.replace(/\/$/, '') === url.replace(/\/$/, ''));
  console.log(JSON.stringify({ url, title, elapsedMs: Date.now() - t0, loadingState, canvas,
    consoleErrors: errors, failedRequests: failed, keyResponses: wanted, totalResponses: responses.length }, null, 2));
  await browser.close();
  process.exit(loadingState === 'cleared' && errors.length === 0 && failed.length === 0 ? 0 : 1);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
