"""Create the workspace post-call webhook and point ElevenLabs Agents at it.

    python3 elevenlabs/setup_webhook.py https://<your-magi-backend>

ElevenLabs signs each post-call webhook with HMAC; MAGI verifies it at /calls/elevenlabs using
ELEVENLABS_WEBHOOK_SECRET. The secret is shown only once, at creation, so this script writes it
straight into .env (never printing it). Copy that one variable to your host (e.g. Render) too.

Needs an API key with the Webhooks write permission (plus ElevenLabs Agents write).
Safe to re-run: if .env already has a secret and the webhook exists, it only re-selects it.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API = "https://api.elevenlabs.io/v1"
NAME = "MAGI post-call summary"


def load_env() -> dict[str, str]:
    env = {}
    for line in (REPO / ".env").read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def call(key: str, method: str, path: str, body: dict | None = None) -> dict:
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": key, "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {path} -> {e.code}: {e.read().decode(errors='replace')[:400]}") from None


def save_secret(secret: str) -> None:
    path = REPO / ".env"
    lines = [l for l in path.read_text().splitlines() if not l.startswith("ELEVENLABS_WEBHOOK_SECRET=")]
    path.write_text("\n".join(lines + [f"ELEVENLABS_WEBHOOK_SECRET={secret}"]) + "\n")
    os.chmod(path, 0o600)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    url = sys.argv[1].rstrip("/") + "/calls/elevenlabs"
    env = load_env()
    key = env.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY missing from .env")

    existing = [w for w in call(key, "GET", "/workspace/webhooks").get("webhooks", []) if w.get("webhook_url") == url]
    if existing and env.get("ELEVENLABS_WEBHOOK_SECRET"):
        webhook_id = existing[0]["webhook_id"]
        print(f"  webhook {NAME}: exists, reusing")
    else:
        if existing:
            print("  a webhook for this URL exists but .env has no secret for it; creating a fresh one")
        resp = call(key, "POST", "/workspace/webhooks",
                    {"settings": {"auth_type": "hmac", "name": NAME, "webhook_url": url}})
        webhook_id, secret = resp.get("webhook_id"), resp.get("webhook_secret")
        if not (webhook_id and secret):
            sys.exit(f"unexpected response fields: {sorted(resp)}")
        save_secret(secret)
        print(f"  webhook {NAME}: created; secret saved to .env as ELEVENLABS_WEBHOOK_SECRET")

    call(key, "PATCH", "/convai/settings", {"webhooks": {"post_call_webhook_id": webhook_id, "send_audio": False}})
    print(f"  ElevenLabs Agents post-call webhook -> {url}")
    print("  Next: set ELEVENLABS_WEBHOOK_SECRET on your backend host (copy it from .env) and redeploy.")


if __name__ == "__main__":
    main()
