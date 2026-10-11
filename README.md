# MAGI: Incident Council

An incident council of three AI agents with competing mandates (restore service, contain harm, protect customers). They each see only their own data, negotiate what to do during a production incident, act on their own when they agree on something reversible, and call a human only when they genuinely disagree about something irreversible.

Built for the UCSC AI Hackathon (Oct 10–11, 2026), Cisco Outshift / AGNTCY Cloud Track, Level 3 "Build a Collective Intelligence."

**Live demo:** https://magi-incident-council.onrender.com (pick a scenario, choose *Scripted (offline)* to run it at no cost, and press **Start incident**). Past runs are under **History**.

## Run it (no API keys needed)

Two terminals from the repo root:

```bash
cd backend && uv sync && uv run uvicorn magi.main:app --port 8787
```

```bash
cd frontend && npm install && npm run dev
```

Open http://localhost:5173, pick a scenario, and press **Start incident**.

- **Agents: Scripted (offline)** runs deterministic agent outputs with zero API calls. Use it for UI work, tests, and as a demo fallback.
- **Live LLM** uses `LLM_PROVIDER=openai` with `OPENAI_API_KEY` + `OPENAI_MODEL` (OpenAI or any OpenAI-compatible server via `OPENAI_BASE_URL`), or `LLM_PROVIDER=anthropic` with `ANTHROPIC_API_KEY`. Agents can be mixed per role with `MODEL_<AGENT>=provider:model`. **Live + record** saves responses so **Replay recording** can re-run the same incident offline.

Tests:

```bash
cd backend && uv run pytest -q
```

### Deploy on Render

The live demo runs as a single Render **web service** (Python 3, Starter instance, one instance only, since live incidents are held in memory):

| Setting | Value |
|---|---|
| Build command | `pip install uv && npm ci --prefix frontend && npm run build --prefix frontend && cd backend && uv sync --frozen` |
| Start command | `cd backend && uv run uvicorn magi.main:app --host 0.0.0.0 --port $PORT` |
| Health check path | `/healthz` |
| Disk | 1 GB mounted at `/data`, with `DB_PATH=/data/magi.sqlite` so incident history survives deploys |
| Environment | the variables from `.env.example` that you use, plus `PUBLIC_BACKEND_URL=https://<service>.onrender.com`. Leave out variables you'd set empty (an empty number fails startup), and the laptop-only ones (`NGROK_*`, `N8N_API_KEY`, `SLACK_BOT_TOKEN`) |

After the first deploy, set the same `PUBLIC_BACKEND_URL` in your local `.env` and run `python3 n8n/deploy.py`, so the n8n workflows call the Render URL. A redeploy ends any incident in progress; it shows as *interrupted* in History. Turn Auto-Deploy off during a demo if you don't want merges to restart the server.

### Or share it from your laptop

Build the UI once and the backend serves it at `/`, next to the API:

```bash
npm run build --prefix frontend
```

```bash
cd backend && uv run uvicorn magi.main:app --port 8787
```

```bash
scripts/tunnel.sh
```

`scripts/tunnel.sh` exposes port 8787 through ngrok (`NGROK_AUTHTOKEN`, `NGROK_DOMAIN`) or a cloudflared quick tunnel, writes the URL to `PUBLIC_BACKEND_URL`, and redeploys the n8n workflows to call it. Anyone with the URL can start incidents, which spends LLM credits in live mode and phones `ONCALL_PHONE` on escalation.

## The two demo scenarios

| Scenario | What happens |
|---|---|
| **Checkout errors after Friday deploy** (`s1_friday_deploy`) | All three agents independently propose the same rollback. It is reversible (T1), passes 3/3, n8n executes it, and **nobody is paged**. |
| **Payments failing on a possibly compromised database** (`s2_ghost_process`) | DP1: three different plans; the reversible containment steps (memory snapshot, egress block, breach assessment) pass 3/3. DP2: the rankings form a cycle, BALTHASAR vetoes the restart, and two written policies collide (SEC-4: isolate within 15 min vs CUS-2: no knowing loss of payment writes), so the council **escalates to a human** with the crux. Use **Inject: Pentest rumor** to watch the agents verify and reject false evidence. In the escalation screen, either rule A/B/C (code is in #incident) or add information (e.g. "I approve the write loss") and watch the council re-deliberate. |

## Running a scenario: what you'll be asked to do

| Scenario | Your part |
|---|---|
| S1 | Nothing. It resolves on its own; #incident in Slack gets the updates and the decision record. |
| S2 | After the first decision, press **Inject: Pentest rumor** (optional). At DP2 the council escalates: Slack #incident posts the crux and a **3-digit confirmation code**, and MAGI phones `ONCALL_PHONE`. On a Twilio trial number, press any key when the trial message plays. On the call you can ask for details, say "unseal S-1, code ###", add information, or say "go with option A, code ###" and then "confirm". Without a phone, use the escalation panel in the UI. If the council then agrees on an irreversible (T2) action, approve or deny it in Slack within 2 minutes (no answer = deny). |

## Incident history

Every event is written to an append-only SQLite log (`DB_PATH`). Live incidents run in memory; the log is what survives a restart:

- **History** in the top bar lists past incidents with their status: *running*, *resolved*, *stopped*, or *interrupted*.
- The page URL ends in `#INC-XXXX`, so a refresh or a shared link reopens that incident, replayed from the log, with its decision record.
- On startup, any incident a restart cut off is closed as *interrupted*. Finished incidents are read-only.

## Evaluation: does the council beat one agent?

`python -m magi.evaluation.run` replays labeled incidents and scores three conditions on the same decision points:

| Condition | What it is |
|---|---|
| **B1** | One agent that sees *every* feed and all evidence (deliberately ignoring need-to-know), picks actions, and may escalate |
| **B2** | Three agents propose, score, rank (Schulze), and vote once: no critique, dissent, or amendments |
| **C** | The full MAGI council |

**Scenarios** (`backend/scenarios/`, 13 decision points). Six are adapted, anonymized, from public postmortems; each decision point is labeled in advance with best, acceptable, and harmful actions and whether a human should decide:

| Scenario | Adapted from | The trap |
|---|---|---|
| `pm_cascade_regex` | Cloudflare, Jul 2019 | Security has to yield: switch the firewall off globally, briefly |
| `pm_wrong_host` | GitLab, Jan 2017 | A wipe proposed on the wrong host, with empty backups |
| `pm_typo_takedown` | AWS S3, Feb 2017 | Slow full restart, and the status page is down too |
| `pm_dormant_flag` | Knight Capital, Aug 2012 | The familiar rollback makes it worse |
| `pm_dark_backbone` | Facebook, Oct 2021 | Tools are blind: say "not enough information" |
| `pm_wrong_ids` | Atlassian, Apr 2022 | Customers must hear from us directly |
| `syn_leaked_key`, `syn_phantom_spike`, `syn_lagging_failover`, `syn_pentest_rumor` | synthetic | Security should win · nobody should be paged · a human must decide · reject the rumor |
| `s1_friday_deploy`, `s2_ghost_process` | the demo scenarios | |

**Metrics** (all from event logs): harmful recommendation rate, harmful actions that would run with no human check, escalation accuracy and precision/recall, false-evidence rejection, best and acceptable action rates, pages, initial disagreement, changes of mind by cause, and tokens / time per decision point. Rates come with bootstrap 95% CIs over decision points. Open-loop: nothing executes; the world is set to each decision point's moment.

**Hypotheses** (from the build plan, written before running): **H1** the council recommends fewer harmful actions than B1; **H2** it escalates more accurately than B1; **H3** it rejects false evidence more often than B1; **H4** (expected null) on best-action rate it is about equal to B2.

```bash
cd backend && uv run python -m magi.evaluation.run --estimate          # run count, no API calls
cd backend && uv run python -m magi.evaluation.run --conditions B1,B2,C --runs 1
```

Results land in `backend/eval_results/<timestamp>/` (`summary.md`, `summary.json`, `runs.jsonl`, and a full trace of every run) and in the **Evaluation** tab of the UI.

### First results (`eval_results/20261011-121959`, gpt-6-luna, 1 run per decision point)

| | B1 single agent | B2 vote only | C council |
|---|---|---|---|
| Harmful recommendation | 0% | 0% | 0% |
| Escalation accuracy | 38% | **77%** | 31% |
| Best action | 30% | **40%** | 20% |
| False evidence rejected | 3/3 | 3/3 | 3/3 |
| Pages per decision point | 0.69 | 0.54 | 0.77 |
| Tokens / wall time per decision point | 4.5k / 22s | 70k / 88s | 145k / 174s |

**H1 tie, H2 not supported, H3 tie, H4 council lower.** Nothing harmful ran in any condition, and every condition caught the planted false evidence. The council escalated to a human too often, and the traces show why:

1. **A protocol bug:** "≥2 agents lack information → escalate" fires before voting, even when every proposal is the information-gathering step itself (`pm_wrong_host`: all three proposed verifying the host and backups, then escalated instead of doing it).
2. **Latency:** at this model's speed, critique rounds hit the 180-second decision budget, which forces an escalation (`pm_typo_takedown`).
3. **Policy text written as a human gate:** in `pm_cascade_regex` BALTHASAR's policy requires the security on-call's approval to disable a control, and it enforced that. Defensible, but the label said no human was needed.

With 13 decision points and one run each, the CIs are wide (see `summary.md`). Labels were written by one person, not two independently as the plan asks; three scoring mistakes (a version string format and two too-narrow acceptable-action lists) were fixed after the run by re-scoring the stored outputs (`report.py --rescore`), applied identically to all conditions; no escalation label was changed.


## How it decides

- **No chair.** A code-only Facilitator routes messages, enforces visibility, computes tiers, counts votes and applies the rules. It never picks a winner.
- **Need-to-know.** Each agent's prompt is built only from evidence it is entitled to; sealed evidence (S-*) is visible only to BALTHASAR and the human IC. Tests enforce both.
- **Protocol:** blind proposals → mandate-axis scoring → Pareto filter + Schulze ranking → critique and versioned amendments → mandatory dissent → vote on an exact version + hash.
- **Risk tiers (computed from the live system):** T0 prepare (any ACCEPT), T1 reversible (2/3, no veto from the affected mandate), T2 irreversible (3/3 plus a human tap). Deadlock, stable positions, or a blocking policy objection → phone escalation.
- **Every change of mind names its cause** (new evidence, new argument, own error, or peer agreement only, which is flagged as possible conformity).
- **Fail toward the human:** any timeout, refusal or parse error is an ABSTAIN, which never helps an irreversible action pass.

## Repo layout

```text
backend/            FastAPI + asyncio council engine (Python 3.12, uv)
  magi/facilitator/ council state machine, tiers, voting (Schulze/Pareto), attribution, certificates
  magi/agents/      charter, mandates, phase prompts, agent wrapper
  magi/llm/         OpenAI-compatible + Claude adapters (structured outputs), scripted, record/replay
  magi/sim/         scenario loader, simulated world, tool feeds
  magi/evaluation/  eval harness: conditions B1/B2/C, label scoring, report
  scenarios/        demo, postmortem-based and synthetic scenarios (with labels) + scripted agent outputs
  eval_results/     evaluation runs: summary, scored runs, full traces
  tests/            invariants: need-to-know, sealed redaction, decision rules, end-to-end scenarios
frontend/           React + Vite + Tailwind control room (pure function of the event log)
n8n/                workflow builder, one-command deploy (deploy.py), setup guide
elevenlabs/         voice agent prompt; setup_tools.py creates and attaches the four voice tools
scripts/tunnel.sh   expose a local backend (ngrok or cloudflared) and repoint n8n at it
MAGI_BUILD_PLAN.md  the full build plan
reports/, research_notes/   competitive landscape research
```

## Status

| Area | Status |
|---|---|
| Council protocol, tiers, vetoes, Schulze/Pareto, attribution, escalation dossier | ✅ built and tested |
| Scenario engine, S1 + S2 with scripted agents | ✅ |
| Control-room UI (evidence, agents, ballot, proposals, log, escalation, confirm, decision record) | ✅ |
| Integration endpoints for n8n (`/alerts`, `/sim/*`, `/confirm/*`) and ElevenLabs (`/voice/*`) | ✅ built, local fallback when not configured |
| Live LLM mode (OpenAI Responses API with native tool calls, OpenAI-compatible servers, or Claude) | ✅ run live on S1 |
| n8n workflows (notify, alert intake, tool gateway, executor, T2 confirm, escalation call, decision record, voice tool relay) | ✅ deployed with `python3 n8n/deploy.py`, tested end to end on n8n Cloud with zero fallbacks; guide in `n8n/README.md` |
| ElevenLabs phone escalation (Twilio number, four voice tools) | ✅ tested on a real call: unseal by code, add information by voice, council re-deliberates, T2 approved in Slack. `submit_ruling` by voice not yet exercised |
| Hosting | ✅ Render web service with a persistent disk; incident history survives deploys |
| Evaluation harness (B1 / B2 / council) and 10 labeled postmortem + synthetic scenarios | ✅ first live run done (council over-escalates; two protocol fixes identified, see Evaluation) |
| ElevenLabs post-call summary webhook | ✅ HMAC-verified at `/calls/elevenlabs`; set up with `elevenlabs/setup_webhook.py` |
| AGNTCY / Brev stretch goals | ⏳ |

## Research

- [`MAGI_BUILD_PLAN.md`](MAGI_BUILD_PLAN.md): architecture, protocol, scenarios, integrations, eval, schedule, demo script
- [`reports/`](reports/): competitive landscape (hackathon projects, open source, big tech, startups, research)
- [`research_notes/`](research_notes/): the underlying research notes with sources
