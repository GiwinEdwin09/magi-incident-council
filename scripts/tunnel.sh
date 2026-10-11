#!/usr/bin/env bash
# Expose the MAGI backend publicly, write the URL into .env as PUBLIC_BACKEND_URL, and re-deploy
# the n8n workflows so they point at it. Then restart the backend so it picks up the new .env.
#
# Provider: ngrok when NGROK_AUTHTOKEN is set in .env (stable URL: your free ngrok dev domain, or
# NGROK_DOMAIN if you set one), otherwise a cloudflared quick tunnel (random URL, no account).
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${MAGI_PORT:-8787}"
LOG="${TMPDIR:-/tmp}/magi-tunnel.log"
envval() { grep -E "^$1=" .env | head -1 | cut -d= -f2- | tr -d '"' || true; }
NGROK_AUTHTOKEN="$(envval NGROK_AUTHTOKEN)"
NGROK_DOMAIN="$(envval NGROK_DOMAIN)"

pkill -f "ngrok http 127.0.0.1:${PORT}" 2>/dev/null || true
pkill -f "cloudflared tunnel --no-autoupdate --url http://127.0.0.1:${PORT}" 2>/dev/null || true
URL=""

if [ -n "$NGROK_AUTHTOKEN" ]; then
  args=(http "127.0.0.1:${PORT}" --authtoken "$NGROK_AUTHTOKEN" --log stdout)
  [ -n "$NGROK_DOMAIN" ] && args+=(--url "$NGROK_DOMAIN")
  nohup ngrok "${args[@]}" >"$LOG" 2>&1 &
  for _ in $(seq 1 30); do
    sleep 1
    URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null \
      | python3 -c 'import sys,json; t=[x["public_url"] for x in json.load(sys.stdin).get("tunnels",[]) if x["public_url"].startswith("https")]; print(t[0] if t else "")' 2>/dev/null || true)
    [ -n "$URL" ] && break
    grep -qiE "ERR_NGROK|authentication failed|lvl=crit" "$LOG" && break
  done
  [ -n "$URL" ] || { echo "ngrok did not start a tunnel; see $LOG" >&2; grep -iE "err|crit" "$LOG" | tail -3 >&2; exit 1; }
else
  for attempt in 1 2 3; do
    pkill -f "cloudflared tunnel --no-autoupdate --url http://127.0.0.1:${PORT}" 2>/dev/null || true
    nohup cloudflared tunnel --no-autoupdate --url "http://127.0.0.1:${PORT}" >"$LOG" 2>&1 &
    for _ in $(seq 1 30); do
      sleep 2
      # Real quick-tunnel hosts are hyphenated words; never match api.trycloudflare.com from an error line.
      URL=$(grep -oE "https://[a-z0-9]+(-[a-z0-9]+)+\.trycloudflare\.com" "$LOG" | head -1 || true)
      [ -n "$URL" ] && break
      grep -q "failed to request quick Tunnel" "$LOG" && break
    done
    [ -n "$URL" ] && break
    echo "Tunnel request failed (attempt $attempt); retrying..." >&2
  done
  [ -n "$URL" ] || { echo "cloudflared did not produce a tunnel; see $LOG" >&2; exit 1; }
fi

# Wait until the tunnel actually serves the backend before handing its URL to n8n.
ok=""
for _ in $(seq 1 20); do
  if curl -s -m 5 -H "ngrok-skip-browser-warning: 1" "$URL/healthz" | grep -q '"ok"'; then ok=1; break; fi
  sleep 3
done
[ -n "$ok" ] || echo "Warning: $URL is up but the backend didn't answer /healthz. Is the backend running on :${PORT}?" >&2

python3 - "$URL" <<'EOF'
import re, sys
s = open(".env").read()
s = re.sub(r"^PUBLIC_BACKEND_URL=.*$", f"PUBLIC_BACKEND_URL={sys.argv[1]}", s, flags=re.M)
open(".env", "w").write(s)
EOF
echo "Tunnel: $URL (written to .env)"
python3 n8n/deploy.py
echo "Now restart the MAGI backend so it uses the new PUBLIC_BACKEND_URL."
