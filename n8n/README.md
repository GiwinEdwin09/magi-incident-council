# Setting up n8n for MAGI

n8n owns every boundary between MAGI and the outside world: agents' tool data, executing decided actions,
Slack messages, the human confirmation for irreversible actions, the escalation phone call, and the decision record.
If n8n isn't configured, MAGI does all of this locally, so you can set it up one piece at a time.

**Time: about 20 minutes.** Tested against n8n 2.41 (imported, published, and run end to end with the MAGI backend).

## Fast path: deploy with one command (recommended)

The deploy script creates the three credentials, imports all eight workflows, fills in the backend URL, and
publishes them through the n8n API. It reads secrets from the repo-root `.env` and never prints them.

1. Do **Step 1** (tunnel) and **Step 2** (Slack bot) below.
2. In n8n: **Settings → n8n API → Create an API key** (all scopes). Paste it into `.env` as `N8N_API_KEY=…`.
3. In `.env`, set `N8N_BASE_URL` (instance root), `PUBLIC_BACKEND_URL` (tunnel URL), `SLACK_BOT_TOKEN` (`xoxb-…`),
   and `N8N_SHARED_SECRET` (any long random string). Add `ELEVENLABS_API_KEY` once the voice agent exists.
4. Run:

   ```bash
   python3 n8n/deploy.py
   ```

It's safe to re-run (for example after the tunnel URL changes): everything is matched by name and updated in place.
A workflow whose credential is missing (e.g. ElevenLabs) is imported but left unpublished until you add it and
re-run. Then restart the MAGI backend and go to **Step 7** to test.

The manual steps below do the same thing through the n8n UI.

## What you'll create

| Workflow file | Webhook path | Called when | What it does |
|---|---|---|---|
| `0_notify.json` | `magi/notify` | Any MAGI message (incident opened, action executed, escalation + confirmation code) | Posts to `#incident` |
| `1_alert_intake.json` | `magi/alert` | An external alert (PagerDuty/Datadog shape) | Opens an incident in MAGI (optional for the demo) |
| `2_tool_gateway.json` | `magi/tool` | An agent requests data (e.g. BALTHASAR checks the IP allowlist) | Fetches the data; MAGI enforces which agent may see what |
| `3_executor.json` | `magi/execute` | The council (or a human) decides | Runs each action; MAGI rejects anything without a valid signed certificate |
| `4_confirm.json` | `magi/confirm` | An irreversible (T2) action passed 3/3 | Slack message with **Approve / Deny**; answer goes back to MAGI (no answer in 2 min = deny) |
| `5_escalate_call.json` | `magi/escalate` | Deadlock on an irreversible action | Phones the on-call engineer through ElevenLabs (needs the voice agent set up) |
| `7_decision_record.json` | `magi/close` | Incident closes | Posts the decision record (postmortem draft) to `#incident` |

## Step 1. Give n8n a way to reach your laptop

n8n Cloud runs on the internet, and several workflows call back into the MAGI backend. `localhost` won't work from
there, so open a tunnel:

```bash
brew install cloudflared
```

```bash
cloudflared tunnel --url http://127.0.0.1:8787
```

Copy the `https://….trycloudflare.com` URL it prints. It changes every time you restart the tunnel, so restart the
backend with the new value when that happens. (ngrok works too.)

> Self-hosting n8n on the same laptop? Skip the tunnel and use `http://127.0.0.1:8787` (not `localhost`: n8n
> resolves `localhost` to IPv6 and the connection is refused).

## Step 2. Create a Slack bot

1. Go to https://api.slack.com/apps → **Create New App** → **From scratch**, name it `MAGI`, pick your hackathon workspace.
2. **OAuth & Permissions** → **Bot Token Scopes** → add `chat:write`, `chat:write.public`, `channels:read`.
3. **Install to Workspace**, then copy the **Bot User OAuth Token** (`xoxb-…`).
4. In Slack, create a public channel `#incident` and type `/invite @MAGI`.

## Step 3. Create three credentials in n8n

In n8n: **Overview → Create → Credential**. Use these exact names; the imported workflows look for them.

| Credential name | Type | Fields |
|---|---|---|
| `MAGI shared secret` | **Header Auth** | Name: `X-MAGI-Secret` · Value: a long random string (e.g. output of `openssl rand -hex 24`). Save it; MAGI needs the same value. |
| `Slack (MAGI bot)` | **Slack API** | Access Token: your `xoxb-…` token |
| `ElevenLabs API key` | **Header Auth** | Name: `xi-api-key` · Value: your ElevenLabs API key (add later if you don't have it yet) |

## Step 4. Import the eight workflows

For each file in `n8n/workflows/`:

1. **Create Workflow** (or **+** → Workflow).
2. Click the **⋯** menu (top right) → **Import from File…** → pick the JSON file.
3. If any node shows a red credential warning, open it and select the matching credential from Step 3.
4. **Save.**

Then edit two placeholders (only needed for those two workflows):

- **MAGI 1 · Alert intake** → node *Open incident in MAGI* → URL: replace `https://YOUR-MAGI-BACKEND` with your tunnel URL.
- **MAGI 6 · Post-call summary** → node *Send call record to MAGI* → same replacement.

All other workflows get the backend URL from MAGI itself on every call, so nothing else is hardcoded.

## Step 5. Publish each workflow

Click **Publish** (top right) on each workflow. On older n8n versions this is the **Active** toggle. Only published
workflows answer on the production URLs `https://<your-instance>.app.n8n.cloud/webhook/magi/<path>`. The
`/webhook-test/…` URLs only work while the editor is listening, so don't use them for MAGI.

## Step 6. Point MAGI at n8n

In the repo root, copy `.env.example` to `.env` (if you haven't) and set:

```bash
N8N_BASE_URL=https://<your-instance>.app.n8n.cloud
N8N_SHARED_SECRET=<the same value as the "MAGI shared secret" credential>
PUBLIC_BACKEND_URL=https://<your-tunnel>.trycloudflare.com
```

`N8N_BASE_URL` is the instance root, without `/webhook`. Restart the backend. The MAGI header should now read
**n8n:on**.

## Step 7. Test it

1. **Slack wiring** (replace the two values):

   ```bash
   curl -X POST https://<your-instance>.app.n8n.cloud/webhook/magi/notify -H "X-MAGI-Secret: <secret>" -H "content-type: application/json" -d '{"text":"MAGI test message"}'
   ```

   A message should appear in `#incident`.
2. **Routine path:** start *Checkout errors after Friday deploy*. In Slack you should see the incident opened, the
   rollback executed, and the decision record. In the MAGI log, the execute line says **via n8n**.
3. **Tool gateway:** start *Payments failing on a possibly compromised database*. Tool results in the evidence panel
   should say **via n8n**.
4. **Human confirmation:** in the same scenario, when it escalates, use **Preset: approve the write loss**. The
   council re-deliberates, all three accept the irreversible failover, and Slack shows **Approve / Deny**.
   Clicking opens a small n8n page in the browser; that's normal. Approve, and MAGI executes.

To debug anything, open the workflow in n8n → **Executions** to see each run's input and output.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `403` from n8n | Shared secret mismatch between the n8n credential and `N8N_SHARED_SECRET` |
| `404` from n8n | Workflow not published, or `N8N_BASE_URL` includes `/webhook` |
| n8n execution fails at an HTTP node with `ECONNREFUSED` or timeout | n8n can't reach MAGI: tunnel down or `PUBLIC_BACKEND_URL` stale; restart both |
| Slack `not_in_channel` / `channel_not_found` | `/invite @MAGI` in `#incident`, or open the Slack node and pick the channel **From list** |
| Slack `invalid_auth` | Wrong or revoked bot token in the `Slack (MAGI bot)` credential |
| MAGI log shows `integration.fallback` | n8n returned an error; MAGI did the step locally so the demo keeps running. Check n8n Executions |
| An action shows **Rejected action: invalid certificate** | Working as intended: n8n forwarded an action MAGI didn't sign |

## Notes

- **Security model:** n8n webhooks require the shared secret; MAGI re-verifies an HMAC certificate on every action
  n8n tries to execute (tested: a forged action sent straight to n8n is refused and logged). ElevenLabs' post-call
  webhook goes straight to MAGI (`/calls/elevenlabs`), which verifies its HMAC signature before posting the call
  summary to Slack through the notify workflow (the old unauthenticated workflow 6 was removed).
- **Production path:** the tool gateway currently fetches simulated data from MAGI. At a real company you would point
  its HTTP node(s) at Datadog, Splunk, or the CRM instead; the council code doesn't change.
- **Regenerating:** edit `n8n/build_workflows.py` and run `python3 n8n/build_workflows.py`.
