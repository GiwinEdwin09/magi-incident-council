"""Create (or update) MAGI's four ElevenLabs server tools and attach them to the agent.

    python3 elevenlabs/setup_tools.py            # create/update tools, attach to ELEVENLABS_AGENT_ID
    python3 elevenlabs/setup_tools.py --only get_detail

Reads ELEVENLABS_API_KEY, ELEVENLABS_AGENT_ID, ELEVENLABS_TOOL_SECRET and N8N_BASE_URL from the
repo-root .env. Tools call the stable n8n voice relay, so they never change when the tunnel does.
Safe to re-run: tools are matched by name and updated in place. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API = "https://api.elevenlabs.io/v1/convai"

TOOLS = {
    "get_detail": ("detail", "Use when the incident commander asks about something not in the briefing.",
                   {"topic": "What the incident commander asked about, in their words."}, ["topic"]),
    "unseal_evidence": ("unseal", "Read sealed evidence. Only after the incident commander states the 3-digit "
                        "confirmation code shown in Slack.",
                        {"evidence_id": "The sealed evidence ID, e.g. S-1.",
                         "confirm_code": "The 3-digit confirmation code the commander said."},
                        ["evidence_id", "confirm_code"]),
    "add_information": ("add-info", "When the incident commander states a new fact or instruction. The MAGI "
                        "agents will re-deliberate with it.",
                        {"text": "The new fact or instruction, in the commander's words."}, ["text"]),
    "submit_ruling": ("ruling", "Record the commander's decision. Only after reading the decision back and "
                      "hearing a clear 'confirm', and after they say the confirmation code.",
                      {"option_key": "A, B, C, or CUSTOM for the commander's own instruction.",
                       "conditions": "Any condition or custom instruction attached to the ruling; empty if none.",
                       "confirm_code": "The 3-digit confirmation code the commander said."},
                      ["option_key", "confirm_code"]),
}


def load_env() -> dict[str, str]:
    env = {}
    for line in (REPO / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
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
        raise RuntimeError(f"{method} {path} -> {e.code}: {e.read().decode(errors='replace')[:600]}") from None


def tool_config(name: str, relay_base: str, secret: str) -> dict:
    path, desc, params, required = TOOLS[name]
    return {
        "type": "webhook",
        "name": name,
        "description": desc,
        "response_timeout_secs": 20,
        "api_schema": {
            "url": f"{relay_base}?tool={path}",
            "method": "POST",
            "request_headers": {"X-MAGI-Secret": secret},
            "request_body_schema": {
                "type": "object",
                "description": f"Arguments for {name}.",
                "properties": {p: {"type": "string", "description": d} for p, d in params.items()},
                "required": required,
            },
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="create/update just this tool")
    args = ap.parse_args()
    env = load_env()
    key, agent_id = env.get("ELEVENLABS_API_KEY", ""), env.get("ELEVENLABS_AGENT_ID", "")
    secret, n8n = env.get("ELEVENLABS_TOOL_SECRET", ""), env.get("N8N_BASE_URL", "").rstrip("/")
    if not (key and agent_id and secret and n8n):
        sys.exit("Need ELEVENLABS_API_KEY, ELEVENLABS_AGENT_ID, ELEVENLABS_TOOL_SECRET and N8N_BASE_URL in .env")
    relay = f"{n8n}/webhook/magi/voice"

    existing = {t["tool_config"]["name"]: t["id"] for t in call(key, "GET", "/tools").get("tools", [])
                if t.get("tool_config", {}).get("name") in TOOLS}
    ids = []
    for name in TOOLS:
        if args.only and name != args.only:
            if name in existing:
                ids.append(existing[name])
            continue
        cfg = {"tool_config": tool_config(name, relay, secret)}
        if name in existing:
            call(key, "PATCH", f"/tools/{existing[name]}", cfg)
            ids.append(existing[name])
            print(f"  tool {name:16} updated")
        else:
            ids.append(call(key, "POST", "/tools", cfg)["id"])
            print(f"  tool {name:16} created")

    agent = call(key, "GET", f"/agents/{agent_id}")
    current = agent["conversation_config"]["agent"]["prompt"].get("tool_ids") or []
    merged = list(dict.fromkeys(current + ids))
    call(key, "PATCH", f"/agents/{agent_id}",
         {"conversation_config": {"agent": {"prompt": {"tool_ids": merged}}}})
    print(f"  agent {agent['name']}: {len(merged)} tool(s) attached")


if __name__ == "__main__":
    main()
