"""Deploy MAGI's workflows to an n8n instance through the n8n public API.

    python3 n8n/deploy.py            # create/update credentials + workflows, then publish
    python3 n8n/deploy.py --dry-run  # show what would happen

Reads everything from the repo-root .env (never prints secret values):
    N8N_BASE_URL        e.g. https://magi-defense.app.n8n.cloud
    N8N_API_KEY         n8n → Settings → n8n API → Create an API key
    N8N_SHARED_SECRET   becomes the "MAGI shared secret" Header Auth credential
    PUBLIC_BACKEND_URL  tunnel URL n8n uses to reach MAGI (fills the two placeholder URLs)
    SLACK_BOT_TOKEN     optional: xoxb-… token for the "Slack (MAGI bot)" credential
    ELEVENLABS_API_KEY  optional: for the "ElevenLabs API key" credential

Safe to re-run: credentials and workflows are matched by name and updated in place.
Workflows whose credentials are missing are imported but left unpublished.
Standard library only, so it runs with any Python 3.10+.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_workflows import BACKEND_PLACEHOLDER, build  # noqa: E402

REPO = Path(__file__).resolve().parent.parent

CREDENTIALS = {
    # credential name -> (n8n type, .env key, data builder)
    "MAGI shared secret": ("httpHeaderAuth", "N8N_SHARED_SECRET", lambda v: {"name": "X-MAGI-Secret", "value": v}),
    "Slack (MAGI bot)": ("slackApi", "SLACK_BOT_TOKEN", lambda v: {"accessToken": v}),
    "ElevenLabs API key": ("httpHeaderAuth", "ELEVENLABS_API_KEY", lambda v: {"name": "xi-api-key", "value": v}),
}


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        sys.exit(f"No {path}. Copy .env.example to .env in the repo root and fill it in.")
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


class N8n:
    def __init__(self, base: str, key: str, dry: bool):
        self.base = base.rstrip("/") + "/api/v1"
        self.key = key
        self.dry = dry

    def call(self, method: str, path: str, body: dict | None = None) -> dict:
        if self.dry and method != "GET":
            return {"id": "dry-run"}
        req = urllib.request.Request(
            self.base + path,
            method=method,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"X-N8N-API-KEY": self.key, "content-type": "application/json", "accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:400]
            raise RuntimeError(f"{method} {path} -> {e.code}: {detail}") from None

    def list_all(self, path: str) -> list[dict]:
        items, cursor = [], None
        while True:
            q = f"{path}?limit=100" + (f"&cursor={cursor}" if cursor else "")
            page = self.call("GET", q)
            items += page.get("data", [])
            cursor = page.get("nextCursor")
            if not cursor:
                return items


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--env-file", type=Path, default=REPO / ".env")
    args = ap.parse_args()

    env = load_env(args.env_file)
    base, key = env.get("N8N_BASE_URL", ""), env.get("N8N_API_KEY", "")
    if not base or not key:
        sys.exit("Set N8N_BASE_URL and N8N_API_KEY in .env (n8n → Settings → n8n API → Create an API key).")
    if not env.get("N8N_SHARED_SECRET"):
        sys.exit("Set N8N_SHARED_SECRET in .env first (any long random string).")
    backend = env.get("PUBLIC_BACKEND_URL", "").rstrip("/")
    api = N8n(base, key, args.dry_run)
    print(f"n8n: {base}{'  (dry run)' if args.dry_run else ''}")

    # ---------------------------------------------------------------- credentials
    existing = {c["name"]: c for c in api.list_all("/credentials")}
    cred_ids: dict[str, str] = {}
    for name, (ctype, env_key, data) in CREDENTIALS.items():
        value = env.get(env_key, "")
        if name in existing:
            cid = existing[name]["id"]
            if value:
                api.call("PATCH", f"/credentials/{cid}", {"name": name, "type": ctype, "data": data(value)})
                print(f"  credential  {name:22} updated from .env {env_key}")
            else:
                print(f"  credential  {name:22} exists (kept; {env_key} not set)")
            cred_ids[name] = cid
        elif value:
            created = api.call("POST", "/credentials", {"name": name, "type": ctype, "data": data(value)})
            cred_ids[name] = created["id"]
            print(f"  credential  {name:22} created from .env {env_key}")
        else:
            print(f"  credential  {name:22} MISSING (set {env_key} in .env, or create it in n8n)")

    # ---------------------------------------------------------------- workflows
    workflows = {w["name"]: w for w in api.list_all("/workflows")}
    publish_problems: list[str] = []
    for file_name, wf in build().items():
        missing: set[str] = set()
        nodes = []
        for node in wf["nodes"]:
            node = json.loads(json.dumps(node))
            for slot, ref in list((node.get("credentials") or {}).items()):
                if ref["name"] in cred_ids:
                    node["credentials"][slot] = {"id": cred_ids[ref["name"]], "name": ref["name"]}
                else:
                    # n8n Cloud rejects references to credentials that don't exist; leave the node unset
                    del node["credentials"][slot]
                    missing.add(ref["name"])
            if "credentials" in node and not node["credentials"]:
                del node["credentials"]
            url = node.get("parameters", {}).get("url")
            if isinstance(url, str) and BACKEND_PLACEHOLDER in url:
                if backend.startswith("https://"):
                    node["parameters"]["url"] = url.replace(BACKEND_PLACEHOLDER, backend)
                else:
                    missing.add("PUBLIC_BACKEND_URL (https tunnel)")
            nodes.append(node)
        body = {"name": wf["name"], "nodes": nodes, "connections": wf["connections"], "settings": wf["settings"]}

        if wf["name"] in workflows:
            wid = workflows[wf["name"]]["id"]
            api.call("PUT", f"/workflows/{wid}", body)
            action = "updated"
        else:
            wid = api.call("POST", "/workflows", body)["id"]
            action = "created"

        if missing:
            status = "NOT published, missing: " + ", ".join(sorted(missing))
            publish_problems.append(wf["name"])
        else:
            try:
                try:
                    api.call("POST", f"/workflows/{wid}/publish")
                except RuntimeError as e:
                    if " 404" in str(e) or "-> 404" in str(e):
                        api.call("POST", f"/workflows/{wid}/activate")  # older n8n
                    else:
                        raise
                status = "published"
            except RuntimeError as e:
                status = f"NOT published: {e}"
                publish_problems.append(wf["name"])
        print(f"  workflow    {wf['name']:30} {action}, {status}")

    print()
    if publish_problems:
        print("Some workflows are not live yet. Fix the items above and re-run this script.")
    else:
        print("All workflows are live. Restart the MAGI backend; its header should read n8n:on.")
    print(f"Webhooks: {base.rstrip('/')}/webhook/magi/<notify|tool|execute|confirm|escalate|close|alert|post-call>")


if __name__ == "__main__":
    main()
