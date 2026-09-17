#!/usr/bin/env bash
# Upload a staged folder to Netlify with the one-time command from the Netlify MCP
# connector, then poll the site and run verify.js against it.
#
#   deploy.sh <staged-dir> "<npx command from the connector>" [--site eco] [--url URL]
#   NETLIFY_DEPLOY_CMD="npx -y @netlify/mcp@latest ..." deploy.sh <staged-dir> [--site ...]
#
# The command comes from the connector's deploy-site operation (see README.md); it embeds
# a short-lived proxy URL, so it is never written to disk here: the log gets a redacted
# copy and logs/screenshots go NEXT TO the staged dir (never under /mnt/project-files).
set -euo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITES_JSON="$KIT_DIR/sites.json"
PROJECT_ROOT="/mnt/project-files"
export NODE_PATH="${NODE_PATH:-/opt/node22/lib/node_modules}"
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}"
export PATH="/opt/node22/bin:$PATH"
POLL_SECS="${POLL_SECS:-300}"
CMD_TIMEOUT="${CMD_TIMEOUT:-900}"

usage() { sed -n '2,10p' "$0" >&2; exit 2; }
redact() { sed -E 's#(--proxy-path[= ]+)"?[^" ]+"?#\1<redacted>#g'; }

STAGED=""; CMD="${NETLIFY_DEPLOY_CMD:-}"; SITE=""; URL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --site) SITE="$2"; shift 2 ;;
    --url)  URL="$2";  shift 2 ;;
    -h|--help) usage ;;
    *) if [ -z "$STAGED" ]; then STAGED="$1"; elif [ -z "$CMD" ]; then CMD="$1"; else echo "unexpected arg: $1" >&2; usage; fi; shift ;;
  esac
done
[ -n "$STAGED" ] && [ -d "$STAGED" ] || { echo "staged dir missing: '$STAGED'" >&2; usage; }
[ -n "$CMD" ] || { echo "no deploy command (arg 2 or NETLIFY_DEPLOY_CMD)" >&2; usage; }
[ -f "$STAGED/index.html" ] && [ -f "$STAGED/books.json" ] || { echo "$STAGED lacks index.html/books.json; run stage.py first" >&2; exit 1; }
STAGED="$(cd "$STAGED" && pwd)"

# --- resolve site name / url from sites.json
if [ -z "$SITE" ]; then
  base="$(basename "$STAGED")"
  SITE="$(python3 - "$SITES_JSON" "$base" <<'PY'
import json, sys, re
sites = json.load(open(sys.argv[1])); base = sys.argv[2]
for k, v in sites.items():
    u = v.get('url') or ''
    if base == k or base == k + '-library-map' or (u and re.sub(r'^https?://', '', u).split('.')[0] == base):
        print(k); break
PY
)"
fi
if [ -z "$URL" ] && [ -n "$SITE" ]; then
  URL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get(sys.argv[2],{}).get("url") or "")' "$SITES_JSON" "$SITE")"
fi
[ -n "$URL" ] || { echo "no site URL: pass --url, or fill sites.json for site '${SITE:-?}'" >&2; exit 1; }
SITE="${SITE:-$(basename "$STAGED")}"

# --- log location: beside the staged dir, never inside the project tree
LOG_DIR="$(dirname "$STAGED")"
case "$LOG_DIR" in "$PROJECT_ROOT"|"$PROJECT_ROOT"/*) LOG_DIR="$(mktemp -d -t netlify-deploy-XXXX)"; echo "log dir moved out of project files: $LOG_DIR" ;; esac
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$LOG_DIR/deploy-$SITE-$TS.log"
SHOT="$LOG_DIR/verify-$SITE-$TS.png"

{
  echo "== deploy $SITE  $(date -Is)"
  echo "staged: $STAGED"
  echo "url:    $URL"
  echo "cmd:    $(printf '%s' "$CMD" | redact)"
} | tee "$LOG"

# --- run the one-time upload command inside the staged folder
echo "== upload" | tee -a "$LOG"
set +e
( cd "$STAGED" && timeout "$CMD_TIMEOUT" bash -c "$CMD" ) 2>&1 | redact | tee -a "$LOG"
rc=${PIPESTATUS[0]}
set -e
echo "upload exit code: $rc" | tee -a "$LOG"
[ "$rc" -eq 0 ] || { echo "upload failed; see $LOG" >&2; exit "$rc"; }

# --- poll until the site answers 200, then compare index.html with what we staged
echo "== poll $URL (up to ${POLL_SECS}s)" | tee -a "$LOG"
want="$(sha256sum "$STAGED/index.html" | cut -c1-64)"
deadline=$(( $(date +%s) + POLL_SECS )); code=000; match=no
while [ "$(date +%s)" -lt "$deadline" ]; do
  code="$(curl -sS -o "$LOG_DIR/.index.$TS" -w '%{http_code}' -H 'Cache-Control: no-cache' "$URL/?_=$TS" || echo 000)"
  if [ "$code" = "200" ]; then
    got="$(sha256sum "$LOG_DIR/.index.$TS" | cut -c1-64)"
    [ "$got" = "$want" ] && match=yes
    [ "$match" = yes ] && break
  fi
  echo "  $(date +%T) http $code, index.html matches staged: $match" | tee -a "$LOG"
  sleep 5
done
rm -f "$LOG_DIR/.index.$TS"
echo "final: http $code, index.html matches staged: $match" | tee -a "$LOG"
[ "$code" = "200" ] || { echo "site never returned 200" >&2; exit 1; }
[ "$match" = yes ] || echo "warning: live index.html differs from staged copy (CDN cache or older deploy still live)" | tee -a "$LOG"

# --- verify with Playwright
echo "== verify.js" | tee -a "$LOG"
set +e
node "$KIT_DIR/verify.js" "$URL" "$SHOT" 2>&1 | tee -a "$LOG"
vrc=${PIPESTATUS[0]}
set -e
echo "verify exit code: $vrc" | tee -a "$LOG"
echo "log: $LOG"
echo "screenshot: $SHOT"
exit "$vrc"
