"""FastAPI app.

/api/*            operator + UI endpoints (proxied by the Vite dev server)
/ws/incidents/*   event stream
/sim/*, /alerts, /confirm/*, /voice/*, /calls/*   integration endpoints for n8n and ElevenLabs
/                 the built UI from frontend/dist, when present
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import time
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, Header, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from magi.config import get_settings
from magi.facilitator import certificate
from magi.incident import Incident, build_record
from magi.integrations.n8n import N8nClient
from magi.llm import build_adapters
from magi.models import ActionCall, HumanRuling, Param
from magi.sim.feeds import ToolNotPermitted, tool_result
from magi.sim.scenario import list_scenarios, load_scenario
from magi.store import EventStore

settings = get_settings()
app = FastAPI(title="MAGI incident council")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

store = EventStore(settings.db_path)
# Nothing is live at startup, so any incident still open in the log was cut off by a restart.
store.mark_interrupted("The MAGI server restarted while this incident was running.")
n8n = N8nClient(settings)
INCIDENTS: dict[str, Incident] = {}


def get_incident(incident_id: str) -> Incident:
    inc = INCIDENTS.get(incident_id)
    if inc is None:
        raise HTTPException(404, f"incident {incident_id} not found")
    return inc


def require_secret(provided: Optional[str], expected: str) -> None:
    if expected and not hmac.compare_digest(provided or "", expected):
        raise HTTPException(401, "bad secret")


# ====================================================================== operator API
class StartRequest(BaseModel):
    speed: Optional[float] = None
    mode: Optional[str] = None  # scripted | live | record | replay
    models: Optional[dict[str, str]] = None


@app.get("/healthz")
async def healthz() -> dict[str, Any]:
    return {"ok": True, "mode": settings.mode, "n8n": settings.n8n_enabled, "phone": settings.phone_enabled}


@app.get("/api/config")
async def config() -> dict[str, Any]:
    return {"mode": settings.mode, "has_api_key": settings.has_llm, "provider": settings.provider,
            "n8n": settings.n8n_enabled, "phone": settings.phone_enabled, "oncall_name": settings.oncall_name,
            "models": {a: ":".join(settings.model_for(a)) for a in ("MELCHIOR", "BALTHASAR", "CASPER")}}


@app.get("/api/scenarios")
async def scenarios() -> list[dict[str, Any]]:
    return list_scenarios()


async def start_incident(scenario_id: str, req: StartRequest) -> Incident:
    try:
        scenario = load_scenario(scenario_id)
    except FileNotFoundError:
        raise HTTPException(404, f"scenario {scenario_id} not found")
    mode = req.mode or settings.mode
    if mode in ("live", "record") and not settings.has_llm:
        raise HTTPException(400, f"Live mode needs an API key for provider '{settings.provider}' in .env. Use scripted mode instead.")
    try:
        adapters = build_adapters(settings, scenario_id, mode=mode, models=req.models)
    except ValueError as e:
        raise HTTPException(400, str(e))
    inc = Incident(scenario, settings, adapters, n8n, store=store, speed=req.speed, mode=mode)
    INCIDENTS[inc.id] = inc
    inc.start()
    return inc


@app.post("/api/scenarios/{scenario_id}/start")
async def start(scenario_id: str, req: StartRequest) -> dict[str, Any]:
    inc = await start_incident(scenario_id, req)
    return {"incident_id": inc.id}


EVAL_DIR = Path(__file__).resolve().parents[1] / "eval_results"


@app.get("/api/eval/summary")
async def eval_summary() -> dict[str, Any]:
    """The newest live evaluation run (python -m magi.evaluation.run), for the Evaluation tab."""
    live = []
    for path in sorted(EVAL_DIR.glob("*/summary.json")):
        data = json.loads(path.read_text())
        if data.get("config", {}).get("mode") == "live":
            live.append((path.parent.name, data))
    if not live:
        raise HTTPException(404, "no evaluation results yet: run python -m magi.evaluation.run")
    name, data = live[-1]
    return {"run": name, **data}


@app.get("/api/incidents")
async def incidents() -> list[dict[str, Any]]:
    """Newest first, from the event log, so incidents from before a restart are listed too."""
    return store.incidents()


@app.get("/api/incidents/{incident_id}")
async def incident(incident_id: str) -> dict[str, Any]:
    return get_incident(incident_id).snapshot()


@app.get("/api/incidents/{incident_id}/events")
async def incident_events(incident_id: str, since: int = 0) -> list[dict[str, Any]]:
    inc = INCIDENTS.get(incident_id)
    if inc is None:
        return store.load(incident_id)
    return [e.model_dump() for e in inc.bus.since(since)]


@app.get("/api/incidents/{incident_id}/record")
async def incident_record(incident_id: str) -> dict[str, str]:
    inc = INCIDENTS.get(incident_id)
    if inc is not None:
        return {"markdown": inc.record()}
    events = store.load(incident_id)
    if not events:
        raise HTTPException(404, f"incident {incident_id} not found")
    title = next((e["payload"].get("title", "") for e in events if e["type"] == "incident.opened"), "")
    pages = next((e["payload"].get("pages") for e in events if e["type"] == "incident.resolved"), "n/a")
    return {"markdown": build_record(incident_id, title, pages, events)}


class InjectRequest(BaseModel):
    injection_id: Optional[str] = None
    content: str = ""
    source: str = "operator"
    visible_to: Optional[list[str]] = None
    is_false: bool = False


@app.post("/api/incidents/{incident_id}/inject")
async def inject(incident_id: str, req: InjectRequest) -> dict[str, Any]:
    inc = get_incident(incident_id)
    if not req.injection_id and not req.content:
        raise HTTPException(400, "injection_id or content required")
    ev = inc.inject(req.injection_id, source=req.source, content=req.content, visible_to=req.visible_to,
                    is_false=req.is_false)
    return {"evidence_id": ev.id}


class ControlRequest(BaseModel):
    action: str  # pause | resume | speed | stop
    speed: Optional[float] = None


@app.post("/api/incidents/{incident_id}/control")
async def control(incident_id: str, req: ControlRequest) -> dict[str, Any]:
    inc = get_incident(incident_id)
    if req.action == "pause":
        inc.paused = True
    elif req.action == "resume":
        inc.paused = False
    elif req.action == "speed" and req.speed:
        inc.speed = max(0.5, min(60.0, req.speed))
    elif req.action == "stop":
        await inc.stop()
    else:
        raise HTTPException(400, "unknown action")
    inc.bus.emit("incident.control", {"action": req.action, "speed": inc.speed, "paused": inc.paused})
    if req.action == "stop":
        inc.bus.emit("incident.ended", {"reason": "stopped", "detail": "Stopped by the operator."})
    return inc.snapshot()


@app.post("/api/incidents/{incident_id}/ruling")
async def ui_ruling(incident_id: str, ruling: HumanRuling) -> dict[str, Any]:
    ok, msg = get_incident(incident_id).submit_ruling(ruling)
    if not ok:
        raise HTTPException(400, msg)
    return {"ok": True, "message": msg}


class InfoRequest(BaseModel):
    text: str
    by: str = "IC"


@app.post("/api/incidents/{incident_id}/info")
async def ui_info(incident_id: str, req: InfoRequest) -> dict[str, Any]:
    ev = get_incident(incident_id).add_human_info(req.text, by=req.by, via="ui")
    return {"evidence_id": ev.id}


class UnsealRequest(BaseModel):
    evidence_id: str
    code: str


@app.post("/api/incidents/{incident_id}/unseal")
async def ui_unseal(incident_id: str, req: UnsealRequest) -> dict[str, Any]:
    ok, content = get_incident(incident_id).unseal(req.evidence_id, req.code)
    if not ok:
        raise HTTPException(400, content)
    return {"content": content}


class ConfirmRequest(BaseModel):
    approved: bool
    by: str = "on-call"


@app.post("/api/incidents/{incident_id}/confirm/{decision_id}")
async def ui_confirm(incident_id: str, decision_id: str, req: ConfirmRequest) -> dict[str, Any]:
    if not get_incident(incident_id).confirm_result(decision_id, req.approved, req.by):
        raise HTTPException(409, "no pending confirmation")
    return {"ok": True}


# ====================================================================== event stream
@app.websocket("/ws/incidents/{incident_id}")
async def ws_incident(ws: WebSocket, incident_id: str, since: int = 0) -> None:
    await ws.accept()
    inc = INCIDENTS.get(incident_id)
    if inc is None:
        # A past incident: replay its log, then hold the socket open so the client doesn't reconnect-loop.
        events = [e for e in store.load(incident_id) if e["seq"] > since]
        if not events and since == 0:
            await ws.send_json({"type": "error", "payload": {"message": "incident not found"}})
            await ws.close()
            return
        try:
            for e in events:
                await ws.send_json(e)
            while True:
                await ws.receive_text()
        except (WebSocketDisconnect, asyncio.CancelledError, RuntimeError):
            return
    q = inc.bus.subscribe()
    try:
        for e in inc.bus.since(since):
            await ws.send_json(e.model_dump())
        while True:
            e = await q.get()
            await ws.send_json(e.model_dump())
    except (WebSocketDisconnect, asyncio.CancelledError, RuntimeError):
        pass
    finally:
        inc.bus.unsubscribe(q)


# ====================================================================== n8n callbacks
@app.post("/alerts")
async def alerts(payload: dict[str, Any], x_magi_secret: Optional[str] = Header(None)) -> dict[str, Any]:
    """n8n W1: a PagerDuty/Datadog-shaped alert opens an incident."""
    require_secret(x_magi_secret, settings.n8n_shared_secret)
    data = payload.get("event", {}).get("data", payload)
    scenario_id = (data.get("custom_details") or {}).get("scenario_id") or payload.get("scenario_id")
    if not scenario_id:
        raise HTTPException(400, "scenario_id required (custom_details.scenario_id)")
    inc = await start_incident(scenario_id, StartRequest())
    return {"incident_id": inc.id}


@app.post("/sim/{incident_id}/tool")
async def sim_tool(incident_id: str, payload: dict[str, Any], x_magi_secret: Optional[str] = Header(None)) -> dict[str, Any]:
    """n8n W2 branch target. In production this branch would call Datadog/Splunk/CRM instead."""
    require_secret(x_magi_secret, settings.n8n_shared_secret)
    inc = get_incident(incident_id)
    agent, tool = payload.get("agent", ""), payload.get("tool", "")
    expected = getattr(settings, f"agent_token_{agent.lower()}", "")
    if expected and not hmac.compare_digest(payload.get("token", ""), expected):
        raise HTTPException(403, "agent token mismatch")
    try:
        return {"result": tool_result(inc.scenario, inc.state.world.state, agent, tool, payload.get("params") or {})}
    except ToolNotPermitted as e:
        raise HTTPException(403, str(e))


@app.post("/sim/{incident_id}/apply")
async def sim_apply(incident_id: str, payload: dict[str, Any], x_magi_secret: Optional[str] = Header(None)) -> dict[str, Any]:
    """n8n W3 executor target: apply one action, only with a valid decision certificate."""
    require_secret(x_magi_secret, settings.n8n_shared_secret)
    inc = get_incident(incident_id)
    d = next((x for x in inc.state.decisions if x.id == payload.get("decision_id")), None)
    if d is None or not certificate.verify(settings.magi_signing_key, payload.get("signature", ""), d.id,
                                           d.proposal_hash or "", d.outcome.value):
        inc.bus.emit("action.rejected", {"reason": "invalid certificate", "payload": payload})
        raise HTTPException(401, "invalid decision certificate")
    a = payload.get("action") or {}
    action = ActionCall(action_id=a.get("action_id", ""), params=[Param(**p) for p in a.get("params", [])])
    if action.label() not in {x.label() for x in d.actions}:
        raise HTTPException(400, "action not part of this decision")
    return {"changes": inc.apply_action(d.id, action, via="n8n")}


@app.post("/confirm/{incident_id}/{decision_id}")
async def n8n_confirm(incident_id: str, decision_id: str, req: ConfirmRequest,
                      x_magi_secret: Optional[str] = Header(None)) -> dict[str, Any]:
    require_secret(x_magi_secret, settings.n8n_shared_secret)
    return await ui_confirm(incident_id, decision_id, req)


# ====================================================================== ElevenLabs server tools
class VoiceRequest(BaseModel):
    incident_id: str = ""  # optional: defaults to the incident currently waiting on a human
    topic: str = ""
    evidence_id: str = ""
    confirm_code: str = ""
    text: str = ""
    option_key: str = ""
    conditions: str = ""


def voice_incident(req: VoiceRequest, secret: Optional[str], tool: str) -> Incident:
    require_secret(secret, settings.elevenlabs_tool_secret)
    if req.incident_id and req.incident_id in INCIDENTS:
        inc = INCIDENTS[req.incident_id]
    else:
        waiting = [i for i in INCIDENTS.values() if i.dossier is not None and not i.closed]
        if not waiting:
            raise HTTPException(404, "no incident is waiting for a human decision")
        inc = waiting[-1]
    request = {k: v for k, v in req.model_dump(exclude={"confirm_code", "incident_id"}).items() if v}
    inc.bus.emit("call.tool", {"tool": tool, "request": request})
    return inc


@app.post("/voice/detail")
async def voice_detail(req: VoiceRequest, x_magi_secret: Optional[str] = Header(None)) -> dict[str, str]:
    inc = voice_incident(req, x_magi_secret, "get_detail")
    return {"answer": inc.detail(req.topic)}


@app.post("/voice/unseal")
async def voice_unseal(req: VoiceRequest, x_magi_secret: Optional[str] = Header(None)) -> dict[str, str]:
    inc = voice_incident(req, x_magi_secret, "unseal_evidence")
    ok, content = inc.unseal(req.evidence_id, req.confirm_code)
    return {"answer": content if ok else f"Not unsealed: {content}"}


@app.post("/voice/add-info")
async def voice_add_info(req: VoiceRequest, x_magi_secret: Optional[str] = Header(None)) -> dict[str, str]:
    inc = voice_incident(req, x_magi_secret, "add_information")
    inc.add_human_info(req.text, by=settings.oncall_name, via="voice")
    return {"answer": "Got it. The agents are re-deliberating with that information."}


@app.post("/voice/ruling")
async def voice_ruling(req: VoiceRequest, x_magi_secret: Optional[str] = Header(None)) -> dict[str, str]:
    inc = voice_incident(req, x_magi_secret, "submit_ruling")
    key = req.option_key.strip().upper()
    if key not in {"A", "B", "C", "CUSTOM"}:
        return {"answer": "Please choose option A, B, C, or give a custom instruction."}
    ruling = HumanRuling(option_key=key, conditions=req.conditions, ruled_by=settings.oncall_name, via="voice",
                         confirm_code=req.confirm_code)
    ok, msg = inc.submit_ruling(ruling)
    return {"answer": msg}


def verify_elevenlabs_signature(raw: bytes, header: Optional[str], secret: str, tolerance_s: int = 1800) -> bool:
    """ElevenLabs-Signature: t=<unix ts>,v0=<hex HMAC-SHA256 of "<ts>.<raw body>">. Fails closed without a secret."""
    if not secret or not header:
        return False
    parts = dict(p.split("=", 1) for p in header.split(",") if "=" in p)
    ts, sig = parts.get("t", ""), parts.get("v0", "")
    if not ts.isdigit() or abs(time.time() - int(ts)) > tolerance_s:
        return False
    expected = hmac.new(secret.encode(), f"{ts}.".encode() + raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig)


@app.post("/calls/elevenlabs")
async def elevenlabs_post_call(request: Request, elevenlabs_signature: Optional[str] = Header(None)) -> dict[str, Any]:
    """ElevenLabs' workspace post-call webhook, verified here, then summarized to Slack through n8n."""
    raw = await request.body()
    if not verify_elevenlabs_signature(raw, elevenlabs_signature, settings.elevenlabs_webhook_secret):
        raise HTTPException(401, "bad signature")
    payload = json.loads(raw)
    if payload.get("type") != "post_call_transcription":
        return {"ok": True, "ignored": payload.get("type")}
    data = payload.get("data") or {}
    dyn = (data.get("conversation_initiation_client_data") or {}).get("dynamic_variables") or {}
    incident_id = dyn.get("incident_id") or ""
    summary = (data.get("analysis") or {}).get("transcript_summary") or "no summary"
    text = f"📞 Call ended for {incident_id or 'an unknown incident'}: {summary}"
    inc = INCIDENTS.get(incident_id)
    if inc is not None:
        inc.call_ended(text, summary, data.get("conversation_id"), (data.get("metadata") or {}).get("call_duration_secs"))
    elif n8n.enabled:  # the incident ended or the server restarted: still tell the channel
        await n8n.notify({"incident_id": incident_id, "text": text, "kind": "call_summary"})
    return {"ok": True}


@app.on_event("shutdown")
async def shutdown() -> None:
    for inc in INCIDENTS.values():
        await inc.stop()


# The built UI (npm run build --prefix frontend), so one URL serves the whole app. Mounted last so
# every API, WebSocket and integration route above takes precedence.
UI_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if UI_DIST.is_dir():
    app.mount("/", StaticFiles(directory=UI_DIST, html=True), name="ui")
