# Netlify kit for the Eco library map

Stages the loose build of the map (the page, `books.json`, `vendor/three*` and the preview
picture) and puts it on the live site, https://eco-library-map.netlify.app.

No token is kept in this folder. The upload command comes from the Netlify tooling at deploy
time, once the account owner approves the call, and it carries a short-lived URL: keep it in the
environment for the length of the run and never write it into a file in this repository.

## Files

- `stage.py` builds the folder that gets uploaded. It copies the page (the file named by the
  site's `index` key in `sites.json`, or by `--index`; for the Eco site that is
  `index_eco.html`), `books.json` and the three `vendor/` scripts out of the source folder,
  rewrites the page's import map from the unpkg CDN to `./vendor/`, and writes `netlify.toml`
  and `_headers`. When the page's `og:image` tag names a preview picture, it stages that too,
  from `dist/preview.jpg` where `build_eco.py` leaves it or else from the source folder, and
  prints its sha256. It checks that `books.json` parses, wipes the output folder first so a
  repeat run is identical, refuses to write into the source tree, prints every staged file with
  its size, and fails if an input is missing or if any `unpkg.com` reference survives.
- `deploy.sh` runs the upload command inside the staged folder, then polls the site URL until it
  answers 200 and serves the same `index.html` as the staged copy, then runs `verify.js` against
  the live page. The log and the screenshot go beside the staged folder, never into the project
  tree, and the log holds a redacted copy of the command. Its exit code is `verify.js`'s.
- `verify.js` is the Playwright check: it loads a URL, waits for the `#loading` overlay to clear,
  and reports the page title, console errors, failed requests and the canvas WebGL state as JSON,
  with a screenshot. It exits 0 only when the overlay cleared with no console error and no failed
  request.
- `sites.json` holds, per site, the site id, the live URL, the source folder and the page file.
  Both scripts read it.

## Redeploy

1. Stage the build:

       python3 netlify/stage.py eco --src eco-map --out /tmp/eco-library-map

   It prints the staged path and the staged page's `<title>`, so the wrong page is caught at
   once, and it fails when an input file is missing.

2. Ask the Netlify tooling for the upload command for this site, and hand it to `deploy.sh`,
   which runs it from the staged folder and then verifies the live page:

       NETLIFY_DEPLOY_CMD='<upload command>' bash netlify/deploy.sh /tmp/eco-library-map --site eco

   The command can also be passed as the second argument. Exit code 0 means the page loaded with
   no console errors; read the JSON summary and the screenshot either way.

To run the check by hand:

    NODE_PATH=/opt/node22/lib/node_modules PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
      node netlify/verify.js <url> <screenshot.png>

## The site

`eco` is https://eco-library-map.netlify.app, built from `eco-map/` (page `index_eco.html`, data
`books.json`, scripts in `vendor/`). Its site id is in `sites.json`.
