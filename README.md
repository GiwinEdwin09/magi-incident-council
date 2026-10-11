# MAGI: Incident Council

An incident council of three AI agents with competing mandates (restore service, contain harm, protect customers). They each see only their own data, negotiate what to do during a production incident, act on their own when they agree on something reversible, and call a human only when they genuinely disagree about something irreversible.

Built for the UCSC AI Hackathon (Oct 10–11, 2026), Cisco Outshift / AGNTCY Cloud Track, Level 3 "Build a Collective Intelligence."

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

### Share it on one public URL

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
  scenarios/        incident scenarios + scripted agent outputs
  tests/            invariants: need-to-know, sealed redaction, decision rules, end-to-end scenarios
frontend/           React + Vite + Tailwind control room (pure function of the event log)
n8n/                importable workflows + setup guide
elevenlabs/         voice agent prompt and server-tool definitions
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
| Live LLM mode (OpenAI-compatible or Claude) | ⚠️ implemented and unit-tested against a fake server; first real run pending an API key |
| n8n workflows (notify, alert intake, tool gateway, executor, T2 confirm, escalation call, post-call, decision record) | ✅ deployed with `python3 n8n/deploy.py` and tested end to end on n8n Cloud (S1 + S2 with zero fallbacks); guide in `n8n/README.md`. Escalation-call workflow waits for an ElevenLabs key |
| ElevenLabs agent + Twilio number | ⏳ to configure (see `elevenlabs/README.md`) |
| Evaluation harness and postmortem replay scenarios | ⏳ next (plan §15) |
| AGNTCY / Brev stretch goals | ⏳ |

## Research

- [`MAGI_BUILD_PLAN.md`](MAGI_BUILD_PLAN.md): architecture, protocol, scenarios, integrations, eval, schedule, demo script
- [`reports/`](reports/): competitive landscape (hackathon projects, open source, big tech, startups, research)
- [`research_notes/`](research_notes/): the underlying research notes with sources
