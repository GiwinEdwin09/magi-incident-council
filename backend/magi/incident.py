"""Incident runtime: sim clock, timeline, decision points, execution, confirmation,
escalation, and the decision record."""

from __future__ import annotations

import asyncio
import hmac
import random
import re
import time
import uuid
from typing import Any, Optional

from magi.agents import prompts
from magi.agents.agent import Agent
from magi.config import Settings
from magi.events import EventBus
from magi.facilitator import certificate
from magi.facilitator.council import Council
from magi.facilitator.state import CouncilState
from magi.integrations.n8n import N8nClient
from magi.llm.base import LLMAdapter, LLMResult, PhaseContext
from magi.models import (
    AGENTS,
    ActionCall,
    Decision,
    Dossier,
    EscalationOption,
    Evidence,
    HumanRuling,
    Outcome,
    Param,
    Proposal,
    ScribeOutput,
    ToolRequest,
    VoteChoice,
    params_dict,
)
from magi.sim.feeds import ToolNotPermitted, tool_result
from magi.sim.scenario import Scenario
from magi.sim.world import World

TICK_S = 0.25
PRICE_PER_MTOK = {"in": 4.0, "out": 20.0}  # Claude Opus 5.5 list price, Oct 2026


class Incident:
    def __init__(self, scenario: Scenario, settings: Settings, adapters: dict[str, LLMAdapter],
                 n8n: N8nClient, store=None, speed: float | None = None, mode: str = "scripted",
                 tick_s: float = TICK_S, incident_id: str | None = None):
        self.id = incident_id or f"INC-{uuid.uuid4().hex[:4].upper()}"
        self.scenario = scenario
        self.settings = settings
        self.mode = mode
        self.n8n = n8n
        self.tick_s = tick_s
        self.speed = speed or scenario.speed
        self.paused = False
        world = World(scenario.world, scenario.dynamics, scenario.effects)
        self.state = CouncilState(incident_id=self.id, scenario=scenario, world=world)
        self.bus = EventBus(self.id, clock=lambda: self.state.sim_ts, store=store)
        self.agents = {a: Agent(a, adapters[a], settings.anonymize_peers) for a in AGENTS}
        self.scribe = adapters.get("SCRIBE") or adapters["MELCHIOR"]
        self.timeline = sorted(scenario.timeline, key=lambda t: t.t)
        self._released = 0
        self.dps = sorted(scenario.decision_points, key=lambda d: d.at)
        self._dp_index = 0
        self.council: Optional[Council] = None
        self.council_task: Optional[asyncio.Task] = None
        self._loop_task: Optional[asyncio.Task] = None
        self.closed = False
        self._decision_counter = 0
        self._confirms: dict[str, asyncio.Future] = {}
        self._ruling: Optional[asyncio.Future] = None
        self._reconvene = asyncio.Event()
        self.dossier: Optional[Dossier] = None
        self.metrics = {"pages": 0, "confirmations": 0, "calls": 0, "input_tokens": 0, "output_tokens": 0,
                        "llm_calls": 0, "llm_failures": 0}
        self._started_wall = time.monotonic()
        self._idle_since: Optional[float] = None
        self._auto_injected: set[str] = set()
        self._pending_assess: list[str] = []  # evidence that arrived between decision points

    # ================================================================ lifecycle
    def start(self) -> None:
        self.bus.emit("incident.opened", {
            "title": self.scenario.title, "company": self.scenario.company, "scenario_id": self.scenario.id,
            "services": self.scenario.services, "mode": self.mode, "speed": self.speed,
            "decision_points": [d.model_dump() for d in self.dps],
            "injections": [{"id": i.id, "label": i.label or i.id} for i in self.scenario.injections],
            "integrations": {"n8n": self.n8n.enabled, "phone": self.settings.phone_enabled},
            "world": self.state.world.snapshot(),
        })
        self._slack(f"🔴 {self.id} opened: {self.scenario.title}. MAGI council convened.", kind="opened")
        self._loop_task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        self.closed = True
        for t in (self.council_task, self._loop_task):
            if t and not t.done():
                t.cancel()

    async def wait_closed(self, timeout: float = 120.0) -> None:
        deadline = time.monotonic() + timeout
        while not self.closed and time.monotonic() < deadline:
            await asyncio.sleep(0.05)

    async def _loop(self) -> None:
        last_metrics = 0.0
        try:
            while not self.closed:
                await asyncio.sleep(self.tick_s)
                if not self.paused:
                    dt = self.tick_s * self.speed
                    self.state.sim_ts += dt
                    self.state.world.advance(dt)
                    if self.state.dp is not None:
                        self.state.registry.retier(self.state.world.state, self.state.dp.id)
                self._release_due()
                self._auto_inject()
                self._maybe_start_dp()
                now = time.monotonic()
                if now - last_metrics >= 1.0:
                    last_metrics = now
                    self.bus.emit("metrics.tick", self._metrics_view())
                await self._maybe_close()
        except asyncio.CancelledError:
            pass

    def _metrics_view(self) -> dict[str, Any]:
        w = self.state.world.state
        return {"services": w.get("services", {}), "clusters": w.get("clusters", {}),
                "assets": w.get("assets", {}), "flags": w.get("flags", {})}

    def _release_due(self) -> None:
        while self._released < len(self.timeline) and self.timeline[self._released].t <= self.state.sim_ts:
            item = self.timeline[self._released]
            self._released += 1
            self.add_evidence(item.to_evidence())

    def _auto_inject(self) -> None:
        for inj in self.scenario.injections:
            if inj.demo_auto_at is not None and inj.id not in self._auto_injected and self.state.sim_ts >= inj.demo_auto_at:
                self._auto_injected.add(inj.id)
                self.inject(inj.id)

    def _maybe_start_dp(self) -> None:
        if self.council_task and not self.council_task.done():
            return
        if self._dp_index >= len(self.dps):
            return
        dp = self.dps[self._dp_index]
        if self.state.sim_ts < dp.at:
            return
        self._dp_index += 1
        self.council = Council(self, dp)
        for eid in self._pending_assess:  # new info since the last council gets assessed first
            self.council.interrupts.put_nowait(eid)
        self._pending_assess.clear()
        self.council_task = asyncio.create_task(self._run_council(self.council))

    async def _run_council(self, council: Council) -> None:
        try:
            await council.run()
        except Exception as e:  # never let a council crash take the incident down silently
            self.bus.emit("council.error", {"decision_point": council.dp.id, "error": repr(e)[:500]})
            raise
        finally:
            self.bus.emit("council.finished", {"decision_point": council.dp.id,
                                               "outcome": council.outcome.value if council.outcome else None})

    async def _maybe_close(self) -> None:
        if self.closed or self._dp_index < len(self.dps):
            return
        if self.council_task and not self.council_task.done():
            self._idle_since = None
            return
        if self._idle_since is None:
            self._idle_since = self.state.sim_ts
            return
        if self.state.sim_ts - self._idle_since >= 20:
            await self.close()

    async def close(self) -> None:
        if self.closed:
            return
        cost = (self.metrics["input_tokens"] * PRICE_PER_MTOK["in"] + self.metrics["output_tokens"] * PRICE_PER_MTOK["out"]) / 1e6
        summary = {**self.metrics, "cost_usd": round(cost, 3), "wall_s": round(time.monotonic() - self._started_wall, 1),
                   "sim_s": round(self.state.sim_ts, 1),
                   "decisions": [d.model_dump(mode="json") for d in self.state.decisions]}
        self.bus.emit("incident.resolved", summary)
        record = self.record()
        resp = await self.n8n.close({"incident_id": self.id, "record_markdown": record, "summary": summary})
        self._slack(record, kind="record", via="n8n" if resp and "error" not in resp else "local")
        self.closed = True

    # ================================================================ evidence & tools
    def add_evidence(self, ev: Evidence, interrupt: bool = True) -> Evidence:
        self.state.evidence[ev.id] = ev
        self.bus.emit("evidence.released", {"evidence": ev.public_view(), "reliability": self.scenario.reliability(ev.source)})
        if interrupt and any(ev.visible(a) for a in AGENTS):
            if self.council and self.council_task and not self.council_task.done():
                self.council.interrupts.put_nowait(ev.id)
            elif self._dp_index > 0:
                self._pending_assess.append(ev.id)
        return ev

    def inject(self, injection_id: str | None = None, *, source: str = "operator", content: str = "",
               visible_to: list[str] | None = None, is_false: bool = False) -> Evidence:
        if injection_id:
            inj = next(i for i in self.scenario.injections if i.id == injection_id)
            ev = inj.to_evidence(sim_ts=self.state.sim_ts)
        else:
            ev = Evidence(id=self.state.next_evidence_id(), sim_ts=self.state.sim_ts, source=source,
                          visible_to=visible_to or list(AGENTS), content=content, is_false=is_false)
        return self.add_evidence(ev)

    async def run_tool(self, agent: str, req: ToolRequest) -> Optional[Evidence]:
        params = params_dict(req.params)
        self.bus.emit("tool.requested", {"tool": req.tool, "params": params, "reason": req.reason}, agent)
        via = "local"
        try:
            text = None
            if self.n8n.enabled:
                token = getattr(self.settings, f"agent_token_{agent.lower()}", "")
                resp = await self.n8n.tool({"incident_id": self.id, "agent": agent, "token": token,
                                            "tool": req.tool, "params": params})
                if resp and "error" not in resp:
                    text, via = str(resp.get("result") or resp.get("text") or resp), "n8n"
            if text is None:
                text = tool_result(self.scenario, self.state.world.state, agent, req.tool, params)
        except ToolNotPermitted as e:
            self.bus.emit("tool.denied", {"tool": req.tool, "reason": str(e)}, agent)
            return None
        ev = Evidence(id=self.state.next_evidence_id(), sim_ts=self.state.sim_ts, source=f"tool:{req.tool}",
                      visible_to=[agent], content=text, requested_by=agent)
        self.state.evidence[ev.id] = ev
        self.bus.emit("tool.result", {"tool": req.tool, "evidence": ev.public_view(), "via": via}, agent)
        return ev

    def account(self, res: LLMResult) -> None:
        self.metrics["llm_calls"] += 1
        self.metrics["input_tokens"] += res.input_tokens
        self.metrics["output_tokens"] += res.output_tokens
        if res.parsed is None:
            self.metrics["llm_failures"] += 1

    # ================================================================ decisions
    def new_decision(self, dp: str, round_: int, prop: Optional[Proposal], outcome: Outcome, rule: str,
                     choices: dict[str, VoteChoice], vetoes: list[str], decider: str = "COUNCIL",
                     ruled_by: str | None = None, actions: list[ActionCall] | None = None) -> Decision:
        self._decision_counter += 1
        d = Decision(id=f"D-{self._decision_counter}", decision_point=dp, round=round_,
                     proposal_ref=prop.ref if prop else None, proposal_hash=prop.hash if prop else None,
                     tier=prop.tier if prop else None, outcome=outcome, rule_applied=rule, votes=choices,
                     vetoes=vetoes, decider=decider, ruled_by=ruled_by,
                     actions=actions if actions is not None else (list(prop.draft.actions) if prop else []))
        self.state.decisions.append(d)
        self.bus.emit("decision.made", {"decision": d.model_dump(mode="json")})
        return d

    async def execute(self, d: Decision) -> None:
        d.certificate = certificate.sign(self.settings.magi_signing_key, d.id, d.proposal_hash or "", d.outcome.value)
        payload = {"incident_id": self.id, "decision": d.model_dump(mode="json"), "signature": d.certificate}
        self.bus.emit("action.executing", {"decision_id": d.id, "actions": [a.label() for a in d.actions],
                                           "certificate": d.certificate, "via": "n8n" if self.n8n.enabled else "local"})
        resp = await self.n8n.execute(payload)
        if resp is None or "error" in resp:
            if resp is not None:
                self.bus.emit("integration.fallback", {"step": "execute", "error": resp.get("error")})
            for a in d.actions:
                self.apply_action(d.id, a, via="local")
        label = ", ".join(a.label() for a in d.actions) or "no infrastructure actions"
        who = f"ruled by {d.ruled_by}" if d.decider == "HUMAN" else d.rule_applied
        self._slack(f"✅ Executed {label} ({who}). Decision {d.id}.", kind="executed")

    def apply_action(self, decision_id: str, a: ActionCall, via: str) -> list[str]:
        changes = self.state.world.apply(a)
        self.bus.emit("action.result", {"decision_id": decision_id, "action": a.label(), "changes": changes,
                                        "status": "ok", "via": via})
        return changes

    async def request_confirm(self, d: Decision, prop: Proposal) -> bool:
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._confirms[d.id] = fut
        self.metrics["confirmations"] += 1
        payload = {"incident_id": self.id, "decision_id": d.id, "proposal": prop.model_dump(mode="json"),
                   "votes": {k: v.value for k, v in d.votes.items()}, "timeout_s": self.settings.confirm_timeout_s,
                   "callback": f"{self.settings.public_backend_url}/confirm/{self.id}/{d.id}"}
        resp = await self.n8n.confirm(payload)
        via = "n8n" if resp and "error" not in resp else "local"
        self.bus.emit("confirm.requested", {"decision_id": d.id, "proposal_ref": prop.ref, "tier": prop.tier.value,
                                            "via": via, "timeout_s": self.settings.confirm_timeout_s})
        if via == "local":
            self._slack(f"🟠 Confirm T2 action for {self.id}: {prop.draft.title} (3/3 agents). Approve or deny.",
                        kind="confirm")
        try:
            approved, by = await asyncio.wait_for(fut, timeout=self.settings.confirm_timeout_s)
        except asyncio.TimeoutError:
            approved, by = False, "timeout"
        self.bus.emit("confirm.result", {"decision_id": d.id, "approved": approved, "by": by})
        if approved:
            d.decider, d.ruled_by = "COUNCIL", f"confirmed by {by}"
        return approved

    def confirm_result(self, decision_id: str, approved: bool, by: str) -> bool:
        fut = self._confirms.get(decision_id)
        if fut is None or fut.done():
            return False
        fut.set_result((approved, by))
        return True

    # ================================================================ escalation
    async def escalate(self, council: Council, d: Decision, reason: str, info_needed: list[str] | None = None) -> None:
        self.metrics["pages"] += 1
        dossier = await self.build_dossier(council, reason, info_needed or [])
        self.dossier = dossier
        self._ruling = asyncio.get_running_loop().create_future()
        self._reconvene.clear()
        self.bus.emit("escalation.started", {"dossier": dossier.public_view(), "decision_id": d.id})
        await self._dispatch_call(dossier)

        while True:
            reconvene = asyncio.create_task(self._reconvene.wait())
            done, _ = await asyncio.wait({self._ruling, reconvene}, return_when=asyncio.FIRST_COMPLETED)
            if self._ruling in done:
                reconvene.cancel()
                ruling: HumanRuling = self._ruling.result()
                await self._apply_ruling(council, dossier, ruling)
                return
            self._reconvene.clear()
            self.bus.emit("escalation.reconvening", {"decision_point": council.dp.id})
            outcome, decision, lead = await council.reconvene()
            council.outcome = outcome
            approved = outcome == Outcome.EXECUTE or (
                outcome == Outcome.CONFIRM and await self.request_confirm(decision, lead))
            if approved:
                self.bus.emit("escalation.resolved", {"by": "COUNCIL", "decision_id": decision.id})
                self._ruling.cancel()
                self.dossier = None
                await self.execute(decision)
                return
            dossier = await self.build_dossier(council, decision.rule_applied, [])
            dossier.confirm_code = self.dossier.confirm_code if self.dossier else dossier.confirm_code
            self.dossier = dossier
            self.bus.emit("escalation.updated", {"dossier": dossier.public_view(), "decision_id": decision.id})

    async def _dispatch_call(self, dossier: Dossier) -> None:
        self._slack(f"📞 {self.id} escalated to {self.settings.oncall_name}. Crux: {dossier.crux} "
                    f"Confirmation code: {dossier.confirm_code}", kind="escalation")
        if not self.settings.phone_enabled:
            self.bus.emit("call.status", {"status": "no_phone", "detail": "No phone configured: rule from the UI."})
            return
        self.metrics["calls"] += 1
        dyn = {
            "incident_id": self.id, "incident_title": dossier.title, "oncall_name": self.settings.oncall_name,
            "situation": dossier.situation, "crux": dossier.crux,
            "option_a": _opt(dossier, "A"), "option_b": _opt(dossier, "B"), "option_c": _opt(dossier, "C"),
            "positions": " ".join(f"{a.title()}: {p}" for a, p in dossier.positions.items()),
            "sealed_available": ", ".join(dossier.sealed_available) or "none",
        }
        resp = await self.n8n.escalate({"incident_id": self.id, "to_number": self.settings.oncall_phone,
                                        "confirm_code": dossier.confirm_code, "dynamic_variables": dyn,
                                        "agent_id": self.settings.elevenlabs_agent_id,
                                        "agent_phone_number_id": self.settings.elevenlabs_phone_number_id})
        if resp and "error" not in resp:
            self.bus.emit("call.status", {"status": "dialing", "conversation_id": resp.get("conversation_id")})
        else:
            self.bus.emit("call.status", {"status": "failed", "detail": (resp or {}).get("error", "n8n unavailable")})

    async def build_dossier(self, council: Council, reason: str, info_needed: list[str]) -> Dossier:
        props = self.state.registry.latest_for_dp(council.dp.id)
        lead = council.leading
        ordered = ([lead] if lead else []) + [p for p in props if not lead or p.id != lead.id]
        options: list[EscalationOption] = []
        for key, p in zip(("A", "B", "C"), ordered[:3]):
            supporters = [a for a in AGENTS if (pos := self.state.positions.get(a))
                          and pos.preferred_proposal_ref.partition("@")[0] == p.id]
            blocking = [k for k in self.state.critiques if k.decision_point == council.dp.id and k.kind == "objection"
                        and k.severity == "blocking" and k.target_ref.partition("@")[0] == p.id]
            risk = blocking[-1].text if blocking else (p.draft.risks[0] if p.draft.risks else p.tier_reasons[0])
            options.append(EscalationOption(key=key, proposal_ref=p.ref, summary=p.draft.title,
                                            supporters=supporters, main_risk=risk, tier=p.tier))
        positions = {}
        for a in AGENTS:
            v = council.last_votes.get(a)
            positions[a] = (v.reason if v else "no position") + (f" Would change if: {v.would_change_if}" if v and v.would_change_if else "")
        sealed = [e.id for e in self.state.evidence.values() if e.sealed and "human_ic" in e.visible_to]
        situation = council.dp.question
        crux = "The agents disagree: " + " / ".join(
            f"{a.title()} would change if {v.would_change_if}" for a, v in council.last_votes.items() if v.would_change_if)
        res = await self._scribe(council, options, positions, reason)
        if res is not None:
            situation, crux = res.situation, res.crux
            for opt, summ in zip(options, res.option_summaries):
                opt.summary = summ
        return Dossier(incident_id=self.id, decision_point=council.dp.id, title=self.scenario.title,
                       situation=situation, crux=crux, options=options, positions=positions, sealed_available=sealed,
                       confirm_code=f"{random.randint(100, 999)}", info_needed=info_needed, reason=reason)

    async def _scribe(self, council: Council, options, positions, reason) -> Optional[ScribeOutput]:
        lines = [prompts.context_block(self.state, "SCRIBE", anonymize=False), f"\nWHY ESCALATED: {reason}", "OPTIONS:"]
        for o in options:
            p = self.state.registry.get(o.proposal_ref)
            acts = "; ".join(a.label() for a in p.draft.actions) if p else ""
            lines.append(f"{o.key}) {o.proposal_ref} [{o.tier.value}] {o.summary} | {acts} | supporters {o.supporters} | main risk: {o.main_risk}")
        lines.append("POSITIONS:")
        lines += [f"{a}: {p}" for a, p in positions.items()]
        user = "\n".join(lines) + "\n\nTASK: " + prompts.TASKS["SCRIBE"]
        ctx = PhaseContext(scenario_id=self.scenario.id, decision_point=council.dp.id, agent="SCRIBE", phase="SCRIBE",
                           round=council.round)
        res = await self.scribe.structured(system=prompts.SCRIBE_SYSTEM, user=user, schema=ScribeOutput, ctx=ctx,
                                           max_tokens=1200)
        self.account(res)
        return res.parsed

    async def _apply_ruling(self, council: Council, dossier: Dossier, ruling: HumanRuling) -> None:
        opt = next((o for o in dossier.options if o.key == ruling.option_key), None)
        prop = self.state.registry.get(opt.proposal_ref) if opt else None
        actions = list(prop.draft.actions) if prop else []
        if ruling.conditions or ruling.custom_instruction:
            actions.append(ActionCall(action_id="comms.slack_update",
                                      params=[Param(name="text", value=f"IC condition: {ruling.conditions or ruling.custom_instruction}")]))
        rule = f"Human ruling: option {ruling.option_key}" + (f" with condition '{ruling.conditions}'" if ruling.conditions else "")
        self.bus.emit("human.ruling", {"ruling": ruling.model_dump(exclude={"confirm_code"}), "proposal_ref": opt.proposal_ref if opt else None})
        d = self.new_decision(council.dp.id, council.round, prop, Outcome.EXECUTE, rule,
                              {a: VoteChoice.ABSTAIN for a in AGENTS}, [], decider="HUMAN",
                              ruled_by=ruling.ruled_by, actions=actions)
        await self.execute(d)
        self.dossier = None

    # ---------------------------------------------------------------- human inputs (voice or UI)
    def check_code(self, code: str) -> bool:
        return bool(self.dossier) and hmac.compare_digest(self.dossier.confirm_code, (code or "").strip())

    def submit_ruling(self, ruling: HumanRuling) -> tuple[bool, str]:
        if self._ruling is None or self._ruling.done():
            return False, "No escalation is waiting for a ruling."
        if not self.check_code(ruling.confirm_code):
            return False, "Confirmation code does not match."
        self._ruling.set_result(ruling)
        return True, "Ruling accepted. Executing now and posting to Slack."

    def add_human_info(self, text: str, by: str = "IC", via: str = "ui") -> Evidence:
        ev = Evidence(id=self.state.next_evidence_id(), sim_ts=self.state.sim_ts, source="oncall_human",
                      visible_to=list(AGENTS) + ["human_ic"], content=f"{by} ({via}): {text}")
        self.bus.emit("human.info_added", {"evidence_id": ev.id, "text": text, "by": by, "via": via})
        self.add_evidence(ev, interrupt=True)
        if self._ruling is not None and not self._ruling.done():
            self._reconvene.set()
        return ev

    def unseal(self, evidence_id: str, code: str) -> tuple[bool, str]:
        ev = self.state.evidence.get(evidence_id)
        if ev is None or not ev.sealed:
            return False, f"{evidence_id} is not sealed evidence."
        if "human_ic" not in ev.visible_to:
            return False, "The incident commander is not entitled to this evidence."
        if not self.check_code(code):
            return False, "Confirmation code does not match."
        self.bus.emit("evidence.unsealed", {"evidence_id": evidence_id, "by": "IC"})
        return True, ev.content

    def detail(self, topic: str) -> str:
        """Answer a spoken question from non-sealed evidence, claims, and proposals. No LLM."""
        words = {w for w in re.findall(r"[a-z0-9\-\.]+", topic.lower()) if len(w) > 2}
        corpus: list[tuple[str, str]] = []
        for e in self.state.evidence.values():
            if not e.sealed and not e.is_false and not e.source.startswith("slack_rumor"):
                corpus.append((e.id, e.content))
        for c in self.state.claims:
            corpus.append((c.id, f"{c.author.title()} claims: {c.text} (confidence {c.confidence:.2f})"))
        for p in self.state.registry.all_versions():
            corpus.append((p.ref, f"{p.ref} {p.draft.title}: {p.draft.rationale}"))
        scored = sorted(((len(words & set(re.findall(r'[a-z0-9\-\.]+', t.lower()))), i, t) for i, t in corpus),
                        reverse=True)
        hits = [t for s, _, t in scored[:2] if s > 0]
        return " ".join(hits) if hits else "MAGI doesn't have that information."

    # ================================================================ slack echo & record
    def _slack(self, text: str, kind: str, via: str | None = None) -> None:
        self.bus.emit("slack.message", {"channel": "#incident", "text": text, "kind": kind,
                                        "via": via or ("n8n" if self.n8n.enabled else "local")})

    def record(self) -> str:
        def t(s: float) -> str:
            return f"T+{int(s // 60):02d}:{int(s % 60):02d}"

        lines = [f"*{self.id} · {self.scenario.title}* · pages: {self.metrics['pages']}"]
        for e in self.bus.events:
            p = e.payload
            if e.type == "proposal.created":
                pr = p["proposal"]
                lines.append(f"{t(e.sim_ts)} {e.agent} proposed {p['ref']} [{pr['tier']}]: {pr['draft']['title']}")
            elif e.type == "proposal.versioned":
                lines.append(f"{t(e.sim_ts)} {e.agent} amended {p['supersedes']} → {p['ref']}")
            elif e.type == "evidence.assessed":
                a = p["assessment"]
                if a["verdict"] != "ACCEPT":
                    lines.append(f"{t(e.sim_ts)} {e.agent} rated {a['evidence_id']} {a['verdict']} (credibility {a['credibility']:.2f})")
            elif e.type == "position.updated" and p["position"].get("changed"):
                pos = p["position"]
                lines.append(f"{t(e.sim_ts)} {e.agent} changed {p.get('from')} → {pos['preferred_proposal_ref']} "
                             f"({pos['change_cause']}{', FLAGGED' if 'conformity_risk' in p['flags'] else ''})")
            elif e.type == "decision.made":
                d = p["decision"]
                lines.append(f"{t(e.sim_ts)} {d['id']} {d['outcome']} {d.get('proposal_ref') or ''}: {d['rule_applied']}")
            elif e.type == "action.result":
                lines.append(f"{t(e.sim_ts)} executed {p['action']} via {p['via']}")
            elif e.type == "escalation.started":
                lines.append(f"{t(e.sim_ts)} escalated: {p['dossier']['crux']}")
            elif e.type == "human.ruling":
                r = p["ruling"]
                lines.append(f"{t(e.sim_ts)} ruling by {r['ruled_by']} via {r['via']}: option {r['option_key']} {r.get('conditions') or ''}")
        return "\n".join(lines)

    def snapshot(self) -> dict[str, Any]:
        return {"id": self.id, "scenario_id": self.scenario.id, "title": self.scenario.title, "mode": self.mode,
                "speed": self.speed, "paused": self.paused, "closed": self.closed, "sim_ts": self.state.sim_ts,
                "metrics": self.metrics, "world": self.state.world.snapshot(),
                "dossier": self.dossier.public_view() if self.dossier else None}


def _opt(d: Dossier, key: str) -> str:
    o = next((o for o in d.options if o.key == key), None)
    if o is None:
        return "not available"
    sup = ", ".join(s.title() for s in o.supporters) or "no agent"
    return f"{o.summary} Supported by {sup}. Main risk: {o.main_risk}"
