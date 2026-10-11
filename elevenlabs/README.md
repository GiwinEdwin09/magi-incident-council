# ElevenLabs voice agent: "MAGI Liaison"

The backend calls n8n workflow W5 (`/webhook/magi/escalate`), which places the outbound call:
`POST https://api.elevenlabs.io/v1/convai/twilio/outbound-call` with `agent_id`, `agent_phone_number_id`,
`to_number`, and `conversation_initiation_client_data.dynamic_variables`. For Twilio calls, **every**
dynamic variable defined on the agent must be supplied (the backend always sends all ten below).

Verify field names against the current ElevenLabs docs before the demo:
[outbound call](https://elevenlabs.io/docs/eleven-agents/api-reference/twilio/outbound-call.md) ·
[personalization](https://elevenlabs.io/docs/eleven-agents/customization/personalization) ·
[post-call webhooks](https://elevenlabs.io/docs/eleven-agents/workflows/post-call-webhooks).

## Setup checklist

1. Create an agent named **MAGI Liaison**. Choose a calm, clear voice and a low-latency LLM.
2. Twilio: buy a number and import it into ElevenLabs. Trial accounts can only call **verified** numbers.
3. Paste the system prompt and first message below.
4. Add the four server tools: `python3 elevenlabs/setup_tools.py` creates them (calling the n8n voice relay
   with header `X-MAGI-Secret: <ELEVENLABS_TOOL_SECRET>`) and attaches them to the agent.
5. Post-call webhook: `python3 elevenlabs/setup_webhook.py https://<your-backend>` creates an HMAC-signed
   workspace webhook to MAGI's `/calls/elevenlabs`, saves its secret to `.env` as `ELEVENLABS_WEBHOOK_SECRET`,
   and selects it for ElevenLabs Agents. Copy that variable to your backend host. MAGI rejects unsigned calls,
   then posts the call summary to Slack through n8n. (Needs a key with the Webhooks write permission.)
6. Put `ELEVENLABS_AGENT_ID`, `ELEVENLABS_PHONE_NUMBER_ID`, `ONCALL_PHONE`, `ONCALL_NAME` in `.env`.
   The backend must be reachable from ElevenLabs (`PUBLIC_BACKEND_URL`).

## Dynamic variables

`incident_id`, `incident_title`, `oncall_name`, `situation`, `crux`, `option_a`, `option_b`, `option_c`,
`positions`, `sealed_available`

## First message

> Hi {{oncall_name}}, this is MAGI about incident {{incident_id}}. This call is recorded for the incident record. The council needs a decision from you. Do you have a minute?

## System prompt

```text
You are the MAGI Liaison, calling {{oncall_name}}, the on-call incident commander.
MAGI is a council of three AI agents (Reliability, Security & Integrity, Customers & Obligations).
They could not agree on an irreversible action and need a human decision.

BRIEFING (speak this first, in under 45 seconds, in short sentences):
- Incident {{incident_id}}: {{incident_title}}.
- Situation: {{situation}}
- The decision you need to make: {{crux}}
- Option A: {{option_a}}
- Option B: {{option_b}}
- Option C: {{option_c}}
- Where the agents stand: {{positions}}
Then ask: "Do you want details, or are you ready to decide?"

RULES
- Never state a fact that isn't in the briefing or returned by a tool. If unsure, call get_detail.
  If the tool has no answer, say "MAGI doesn't have that information."
- Sealed evidence ({{sealed_available}}) may only be read after the IC says the 3-digit confirmation
  code posted in Slack. Call unseal_evidence with it. Never read the code aloud yourself.
- If the IC shares a new fact ("that IP is our vendor", "I approve the data loss"), call add_information,
  then say: "Got it. The agents are re-deliberating. Do you still want to decide now, or wait for their update?"
- When the IC decides, repeat the decision and any condition back in one sentence and ask "Confirm?"
  Only after a clear yes, ask for the confirmation code and call submit_ruling.
- They may choose A, B, C, or give their own instruction (option_key "CUSTOM", instruction in conditions).
- Be calm and brief. No filler. Don't argue for any option.
- When done, thank them, say the decision is being executed and posted to Slack, and end the call.
```

## Server tools (webhooks to the backend)

| Tool | Method + path | Body | Description for the agent |
|---|---|---|---|
| `get_detail` | `POST {PUBLIC_BACKEND_URL}/voice/detail` | `{incident_id, topic}` | Use when the IC asks about something not in the briefing. |
| `unseal_evidence` | `POST /voice/unseal` | `{incident_id, evidence_id, confirm_code}` | Only after the IC states the confirmation code shown in Slack. |
| `add_information` | `POST /voice/add-info` | `{incident_id, text}` | When the IC states a new fact or instruction to investigate. The agents re-deliberate. |
| `submit_ruling` | `POST /voice/ruling` | `{incident_id, option_key, conditions, confirm_code}` | Only after reading the decision back and hearing "confirm". |

Each endpoint returns `{"answer": "..."}` for the agent to speak.
