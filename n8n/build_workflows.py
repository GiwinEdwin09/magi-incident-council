"""Generate the importable n8n workflows in n8n/workflows/.

Run:  python3 n8n/build_workflows.py
Every workflow uses only stock nodes (Webhook, HTTP Request, Split Out, Slack, Respond to Webhook)
so it imports on n8n Cloud without community nodes or Code-node sandboxes.

Credentials referenced by name (create them in n8n first; see n8n/README.md):
  - "MAGI shared secret"  (Header Auth: X-MAGI-Secret)
  - "Slack (MAGI bot)"    (Slack API: bot token)
  - "ElevenLabs API key"  (Header Auth: xi-api-key)
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parent / "workflows"
NS = uuid.UUID("6f0c4a52-6d1b-4f1e-9d8e-5b3a1c2d4e5f")  # stable ids => clean diffs on regenerate

SECRET = {"httpHeaderAuth": {"id": "magiSecretCred01", "name": "MAGI shared secret"}}
SLACK = {"slackApi": {"id": "magiSlackCred001", "name": "Slack (MAGI bot)"}}
ELEVEN = {"httpHeaderAuth": {"id": "magiElevenCred01", "name": "ElevenLabs API key"}}
CHANNEL = {"__rl": True, "value": "#incident", "mode": "name"}
BACKEND_PLACEHOLDER = "https://YOUR-MAGI-BACKEND"


def uid(*parts: str) -> str:
    return str(uuid.uuid5(NS, "/".join(parts)))


def webhook(wf: str, path: str, response: str, auth: bool = True) -> dict:
    node = {
        "parameters": {"httpMethod": "POST", "path": path, "responseMode": response, "options": {}},
        "id": uid(wf, "Webhook"),
        "name": "Webhook",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [0, 0],
        "webhookId": uid(wf, "webhookId"),
    }
    if auth:
        node["parameters"]["authentication"] = "headerAuth"
        node["credentials"] = SECRET
    return node


def http(wf: str, name: str, url: str, body: str, creds: dict | None, x: int, y: int = 0,
         never_error: bool = False, timeout_ms: int = 10000) -> dict:
    params: dict = {
        "method": "POST",
        "url": url,
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": body,
        "options": {"timeout": timeout_ms},
    }
    if never_error:
        params["options"]["response"] = {"response": {"neverError": True}}
    node = {"parameters": params, "id": uid(wf, name), "name": name, "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2, "position": [x, y]}
    if creds:
        params["authentication"] = "genericCredentialType"
        params["genericAuthType"] = "httpHeaderAuth"
        node["credentials"] = creds
    return node


def respond(wf: str, body: str, x: int) -> dict:
    return {"parameters": {"respondWith": "json", "responseBody": body, "options": {}},
            "id": uid(wf, "Respond"), "name": "Respond to MAGI", "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1, "position": [x, 0]}


def slack_post(wf: str, name: str, text: str, x: int) -> dict:
    return {"parameters": {"select": "channel", "channelId": CHANNEL, "messageType": "text", "text": text,
                           "otherOptions": {}},
            "id": uid(wf, name), "name": name, "type": "n8n-nodes-base.slack", "typeVersion": 2.3,
            "position": [x, 0], "credentials": SLACK}


def chain(*names: str) -> dict:
    return {a: {"main": [[{"node": b, "type": "main", "index": 0}]]} for a, b in zip(names, names[1:])}


def workflow(name: str, nodes: list[dict], connections: dict) -> dict:
    return {"name": name, "nodes": nodes, "connections": connections, "active": False,
            "settings": {"executionOrder": "v1"}, "pinData": {}, "meta": {"templateCredsSetupCompleted": False}}


W = "$('Webhook').first().json.body"


def build() -> dict[str, dict]:
    wfs: dict[str, dict] = {}

    # 0 · notify: every MAGI message -> #incident
    wfs["0_notify"] = workflow("MAGI 0 · Slack notify", [
        webhook("0", "magi/notify", "onReceived"),
        slack_post("0", "Post to #incident", "={{ $json.body.text }}", 260),
    ], chain("Webhook", "Post to #incident"))

    # 1 · alert intake: PagerDuty/Datadog-shaped alert -> MAGI opens an incident
    wfs["1_alert_intake"] = workflow("MAGI 1 · Alert intake", [
        webhook("1", "magi/alert", "responseNode"),
        http("1", "Open incident in MAGI", f"{BACKEND_PLACEHOLDER}/alerts",
             "={{ JSON.stringify($json.body) }}", SECRET, 260),
        respond("1", "={{ JSON.stringify($json) }}", 520),
    ], chain("Webhook", "Open incident in MAGI", "Respond to MAGI"))

    # 2 · tool gateway: an agent's data request. MAGI's /sim endpoint enforces per-agent entitlement;
    # in production these requests would branch to Datadog, Splunk, the CRM, etc.
    wfs["2_tool_gateway"] = workflow("MAGI 2 · Agent tool gateway", [
        webhook("2", "magi/tool", "responseNode"),
        http("2", "Fetch tool data",
             "={{ $json.body.backend_url }}/sim/{{ $json.body.incident_id }}/tool",
             "={{ JSON.stringify({ agent: $json.body.agent, token: $json.body.token, tool: $json.body.tool, params: $json.body.params }) }}",
             SECRET, 260),
        respond("2", "={{ JSON.stringify({ result: $json.result }) }}", 520),
    ], chain("Webhook", "Fetch tool data", "Respond to MAGI"))

    # 3 · executor: run each action of a signed decision. MAGI verifies the HMAC certificate on every call.
    split = {"parameters": {"fieldToSplitOut": "body.decision.actions", "include": "noOtherFields", "options": {}},
             "id": uid("3", "Split"), "name": "One item per action", "type": "n8n-nodes-base.splitOut",
             "typeVersion": 1, "position": [260, 0]}
    wfs["3_executor"] = workflow("MAGI 3 · Action executor", [
        webhook("3", "magi/execute", "responseNode"),
        split,
        http("3", "Apply action",
             f"={{{{ {W}.backend_url }}}}/sim/{{{{ {W}.incident_id }}}}/apply",
             f"={{{{ JSON.stringify({{ decision_id: {W}.decision.id, signature: {W}.signature, action: {{ action_id: $json.action_id, params: $json.params }} }}) }}}}",
             SECRET, 520),
        respond("3", "={{ JSON.stringify({ applied: $input.all().map(i => i.json.changes) }) }}", 780),
    ], chain("Webhook", "One item per action", "Apply action", "Respond to MAGI"))

    # 4 · confirm: irreversible action passed 3/3 -> human approves or denies in Slack
    message = ("=🟠 *Confirm irreversible action* for {{ $json.body.incident_id }}\n"
               "{{ $json.body.proposal.draft.title }} ({{ $json.body.proposal.id }}@{{ $json.body.proposal.version }}, tier {{ $json.body.proposal.tier }})\n"
               "Actions: {{ $json.body.proposal.draft.actions.map(a => a.action_id).join(', ') }}\n"
               "All three agents voted ACCEPT. No answer in 2 minutes counts as deny.")
    wfs["4_confirm"] = workflow("MAGI 4 · T2 confirmation", [
        webhook("4", "magi/confirm", "onReceived"),
        {"parameters": {"operation": "sendAndWait", "select": "channel", "channelId": CHANNEL, "message": message,
                        "approvalOptions": {"values": {"approvalType": "double", "approveLabel": "Approve",
                                                       "disapproveLabel": "Deny"}},
                        "options": {"limitWaitTime": {"values": {"limitType": "afterTimeInterval",
                                                                 "resumeAmount": 2, "resumeUnit": "minutes"}}}},
         "id": uid("4", "Ask"), "name": "Ask on-call in Slack", "type": "n8n-nodes-base.slack", "typeVersion": 2.3,
         "position": [260, 0], "credentials": SLACK, "webhookId": uid("4", "askWebhook")},
        http("4", "Send answer to MAGI", f"={{{{ {W}.callback }}}}",
             "={{ JSON.stringify({ approved: $json.data ? $json.data.approved === true : false, by: 'Slack' }) }}",
             SECRET, 520, never_error=True),
    ], chain("Webhook", "Ask on-call in Slack", "Send answer to MAGI"))

    # 5 · escalate: phone the on-call engineer through ElevenLabs (Twilio number)
    wfs["5_escalate_call"] = workflow("MAGI 5 · Escalation call", [
        webhook("5", "magi/escalate", "responseNode"),
        http("5", "Call on-call (ElevenLabs)", "https://api.elevenlabs.io/v1/convai/twilio/outbound-call",
             "={{ JSON.stringify({ agent_id: $json.body.agent_id, agent_phone_number_id: $json.body.agent_phone_number_id, "
             "to_number: $json.body.to_number, conversation_initiation_client_data: { dynamic_variables: $json.body.dynamic_variables } }) }}",
             ELEVEN, 260, timeout_ms=20000),
        respond("5", "={{ JSON.stringify({ conversation_id: $json.conversation_id, callSid: $json.callSid, success: $json.success, message: $json.message }) }}", 520),
    ], chain("Webhook", "Call on-call (ElevenLabs)", "Respond to MAGI"))

    # 7 · close: the decision record (postmortem draft) -> #incident
    wfs["7_decision_record"] = workflow("MAGI 7 · Decision record", [
        webhook("7", "magi/close", "onReceived"),
        slack_post("7", "Post decision record", "=📋 *Decision record*\n{{ $json.body.record_markdown }}", 260),
    ], chain("Webhook", "Post decision record"))
    # 8 · voice tool relay (…/webhook/magi/voice?tool=detail|unseal|add-info|ruling): ElevenLabs server
    # tools call this stable n8n URL instead of the tunnel, which
    # changes on every restart. deploy.py rewrites the placeholder to the current PUBLIC_BACKEND_URL.
    # The X-MAGI-Secret header from ElevenLabs is passed through; MAGI checks it.
    relay = {"parameters": {
                "method": "POST",
                "url": f"={BACKEND_PLACEHOLDER}/voice/{{{{ $json.query.tool }}}}",
                "sendHeaders": True,
                "headerParameters": {"parameters": [
                    {"name": "X-MAGI-Secret", "value": "={{ $json.headers['x-magi-secret'] || '' }}"}]},
                "sendBody": True, "specifyBody": "json", "jsonBody": "={{ JSON.stringify($json.body) }}",
                "options": {"timeout": 10000, "response": {"response": {"neverError": True}}}},
             "id": uid("8", "Relay"), "name": "Forward to MAGI", "type": "n8n-nodes-base.httpRequest",
             "typeVersion": 4.2, "position": [260, 0]}
    wfs["8_voice_tool_relay"] = workflow("MAGI 8 · Voice tool relay", [
        webhook("8", "magi/voice", "responseNode", auth=False),
        relay,
        respond("8", "={{ JSON.stringify($json) }}", 520),
    ], chain("Webhook", "Forward to MAGI", "Respond to MAGI"))
    return wfs


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, wf in build().items():
        (OUT / f"{name}.json").write_text(json.dumps(wf, indent=2, ensure_ascii=False) + "\n")
        print("wrote", OUT / f"{name}.json")
