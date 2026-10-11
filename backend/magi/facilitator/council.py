"""The Facilitator's council state machine for one decision point.

The Facilitator never decides. It routes messages, enforces visibility, computes
tiers, counts votes, applies the published rules, and builds the escalation
dossier. Every failure (timeout, refusal, parse error) becomes an ABSTAIN, so
failures move toward the human, never toward action.
"""

from __future__ import annotations

import asyncio
import difflib
import time
from typing import TYPE_CHECKING, Any, Optional

from magi.facilitator.attribution import validate_cause
from magi.facilitator.proposals import diff_drafts
from magi.facilitator.state import Critique
from magi.facilitator.voting import decide, pareto, schulze, tally
from magi.models import (
    AGENTS,
    Param,
    ToolRequest,
    ChangeCause,
    Claim,
    CritiqueOutput,
    Decision,
    DissentOutput,
    EvidenceAssessment,
    Outcome,
    Position,
    Proposal,
    ProposeOutput,
    ScoreOutput,
    Tier,
    VoteChoice,
    VoteOutput,
    clamp01,
)
from magi.sim.scenario import AGENT_TOOLS, DecisionPoint

if TYPE_CHECKING:
    from magi.incident import Incident


TOOL_PHASES = {"PROPOSE", "CRITIQUE", "ASSESS"}


class Council:
    def __init__(self, inc: "Incident", dp: DecisionPoint):
        self.inc = inc
        self.dp = dp
        self.state = inc.state
        self.settings = inc.settings
        self.interrupts: asyncio.Queue[str] = asyncio.Queue()
        self.rankings: dict[str, list[str]] = {}  # agent -> proposal ids, best first
        self.scores: dict[str, dict[str, int]] = {}  # proposal id -> agent -> score
        self.last_seen: dict[str, set[str]] = {}
        self.round = 0
        self.started = time.monotonic()
        self.leading: Optional[Proposal] = None
        self.last_votes: dict[str, VoteOutput] = {}
        self.outcome: Optional[Outcome] = None

    # ================================================================ helpers
    def emit(self, type_: str, payload: dict[str, Any] | None = None, agent: str | None = None) -> None:
        payload = dict(payload or {})
        payload.setdefault("decision_point", self.dp.id)
        self.inc.bus.emit(type_, payload, agent)

    def status(self, agent: str, status: str) -> None:
        self.emit("agent.status", {"status": status, "round": self.round}, agent)

    async def _call_all(self, phase: str, schema, agents: list[str] | None = None, **kw) -> dict[str, Any]:
        agents = agents or list(AGENTS)
        for a in agents:
            self.status(a, phase)

        async def one(a: str):
            runner = self._tool_runner(a) if phase in TOOL_PHASES else None
            res, _ = await self.inc.agents[a].call(self.state, phase, schema, self.round, tool_runner=runner, **kw)
            self.inc.account(res)
            if res.parsed is None:
                self.emit("agent.error", {"phase": phase, "status": res.status, "detail": res.detail}, a)
                self.status(a, "ABSTAIN")
            else:
                self.status(a, "IDLE")
            return a, res.parsed

        pairs = await asyncio.gather(*(one(a) for a in agents))
        return dict(pairs)

    def _tool_runner(self, agent: str):
        """Native tool calls run through the same path as tool_requests: entitlement, n8n, evidence, events."""

        async def run(name: str, args: dict) -> str:
            req = ToolRequest(tool=name, params=[Param(name=k, value=str(v)) for k, v in args.items()],
                              reason="native tool call")
            ev = await self.inc.run_tool(agent, req)
            return f"[{ev.id}] {ev.content}" if ev else f"{name} is not available to {agent}."

        return run

    def _resolve(self, ref: str | None) -> Optional[Proposal]:
        if not ref:
            return None
        p = self.state.registry.get(ref) or self.state.registry.resolve_latest(ref)
        if p is None or p.decision_point != self.dp.id:
            return None
        return p

    def _released_since(self, agent: str) -> set[str]:
        now = {e.id for e in self.state.visible_evidence(agent)}
        return now - self.last_seen.get(agent, set())

    def _argument_ids(self) -> set[str]:
        return {k.id for k in self.state.critiques if k.decision_point == self.dp.id and k.round >= self.round - 1}

    def _set_position(self, agent: str, pos: Position, phase: str) -> bool:
        target = self._resolve(pos.preferred_proposal_ref)
        if target is None:
            return False
        target = self.state.registry.latest(target.id) or target  # positions follow a proposal's newest version
        prev = self.state.positions.get(agent)
        prev_id = prev.preferred_proposal_ref.partition("@")[0] if prev else None
        # "changed" is computed from the record, never taken from the model's own claim
        actually_changed = prev is not None and prev_id != target.id
        pos = pos.model_copy(update={"preferred_proposal_ref": target.ref, "confidence": clamp01(pos.confidence),
                                     "changed": actually_changed})
        if not pos.changed:
            pos = pos.model_copy(update={"change_cause": ChangeCause.NO_CHANGE})
        pos, flags = validate_cause(pos, self._released_since(agent), self._argument_ids())
        self.state.positions[agent] = pos
        self.last_seen[agent] = {e.id for e in self.state.visible_evidence(agent)}
        self.emit("position.updated", {"position": pos.model_dump(mode="json"), "flags": flags, "phase": phase,
                                       "from": prev.preferred_proposal_ref if prev else None}, agent)
        return pos.changed

    # ================================================================ phases
    async def _run_tools(self, agent: str, requests) -> None:
        for req in (requests or [])[:2]:
            await self.inc.run_tool(agent, req)

    def _publish_claims(self, agent: str, out: ProposeOutput) -> None:
        sealed = self.state.sealed_contents()
        for cd in out.key_claims[:3]:
            text = cd.text
            sealed_ref = next((eid for eid in cd.evidence_ids if eid in sealed), None)
            for sid, content in sealed.items():
                m = difflib.SequenceMatcher(None, text.lower(), content.lower()).find_longest_match()
                if m.size >= 24:  # code-level guard: never let sealed text leak through a claim
                    text = text[: m.a] + f"[sealed {sid}]" + text[m.a + m.size :]
                    sealed_ref = sid
            claim = Claim(id=self.state.next_claim_id(), author=agent, text=text,
                          evidence_ids=[e for e in cd.evidence_ids if e in self.state.evidence],
                          confidence=clamp01(cd.confidence), round=self.round,
                          decision_point=self.dp.id, sealed_ref=sealed_ref)
            self.state.claims.append(claim)
            self.emit("claim.published", {"claim": claim.model_dump(mode="json")}, agent)

    def _register(self, agent: str, draft) -> Optional[Proposal]:
        draft.actions = [a for a in draft.actions if a.action_id]
        if not draft.actions:
            return None
        prop, merged = self.state.registry.create(draft, agent, self.round, self.dp.id, self.state.world.state)
        if merged:
            self.emit("proposal.merged", {"proposal": prop.model_dump(mode="json"), "ref": prop.ref}, agent)
        else:
            self.emit("proposal.created", {"proposal": prop.model_dump(mode="json"), "ref": prop.ref}, agent)
        return prop

    async def propose(self) -> dict[str, ProposeOutput]:
        outs = await self._call_all("PROPOSE", ProposeOutput)
        for agent in AGENTS:  # fixed order => deterministic proposal ids
            out = outs.get(agent)
            if out is None:
                continue
            self.emit("assessment.posted", {"assessment": out.assessment, "confidence": clamp01(out.confidence),
                                            "insufficient_info": out.insufficient_info,
                                            "info_needed": out.info_needed}, agent)
            self._publish_claims(agent, out)
            prop = self._register(agent, out.proposal)
            if prop is not None:
                self._set_position(agent, Position(preferred_proposal_ref=prop.ref, confidence=out.confidence), "PROPOSE")
        await asyncio.gather(*(self._run_tools(a, o.tool_requests) for a, o in outs.items() if o))
        return {a: o for a, o in outs.items() if o}

    async def score(self, props: list[Proposal]) -> None:
        refs = ", ".join(p.ref for p in props)
        outs = await self._call_all("SCORE", ScoreOutput, fmt={"refs": refs})
        for agent, out in outs.items():
            if out is None:
                continue
            ranking = []
            for r in out.ranking:
                p = self._resolve(r)
                if p and p.id not in ranking:
                    ranking.append(p.id)
            for p in props:
                if p.id not in ranking:
                    ranking.append(p.id)
            self.rankings[agent] = ranking
            for s in out.scores:
                p = self._resolve(s.proposal_ref)
                if p:
                    self.scores.setdefault(p.id, {})[agent] = max(0, min(10, s.score))
            self.emit("proposal.scored", {"scores": [s.model_dump() for s in out.scores], "ranking": ranking}, agent)

    def compute_leading(self) -> Proposal:
        props = self.state.registry.latest_for_dp(self.dp.id)
        ids = [p.id for p in props]
        if len(ids) == 1:
            self.leading = props[0]
            return props[0]
        triples = {pid: tuple(float(self.scores.get(pid, {}).get(a, 5)) for a in AGENTS) for pid in ids}
        kept = pareto(ids, triples)
        ballots = []
        for agent in AGENTS:
            ranking = [pid for pid in self.rankings.get(agent, ids) if pid in kept]
            ranking += [pid for pid in kept if pid not in ranking]
            pos = self.state.positions.get(agent)
            if pos:
                pref = pos.preferred_proposal_ref.partition("@")[0]
                if pref in ranking:
                    ranking.remove(pref)
                    ranking.insert(0, pref)
            ballots.append(ranking)
        winner, detail = schulze(kept, ballots)
        lead = self.state.registry.latest(winner)
        assert lead is not None
        self.leading = lead
        self.emit("proposal.leading", {"ref": lead.ref, "pareto_kept": kept,
                                       "dropped": [i for i in ids if i not in kept], "schulze": detail})
        return lead

    async def critique(self) -> bool:
        lead = self.leading
        outs = await self._call_all("CRITIQUE", CritiqueOutput, fmt={"leading": lead.ref if lead else ""},
                                    leading_ref=lead.ref if lead else None)
        any_change = False
        for agent in AGENTS:
            out: Optional[CritiqueOutput] = outs.get(agent)
            if out is None:
                continue
            for ob in out.objections:
                p = self._resolve(ob.proposal_ref)
                if p is None:
                    continue
                k = Critique(id=self.state.next_critique_id(), author=agent, round=self.round, decision_point=self.dp.id,
                             target_ref=p.ref, text=ob.text, severity=ob.severity, cites_policy=ob.cites_policy,
                             would_accept_if=ob.would_accept_if)
                self.state.critiques.append(k)
                self.emit("critique.posted", {"critique": k.__dict__}, agent)
            for ch in out.challenges:
                k = Critique(id=self.state.next_critique_id(), author=agent, round=self.round, decision_point=self.dp.id,
                             target_ref=ch.claim_id, text=ch.challenge, severity="challenge", kind="challenge",
                             would_accept_if=ch.requested_evidence)
                self.state.critiques.append(k)
                self.emit("critique.posted", {"critique": k.__dict__}, agent)
            if out.amendment is not None:
                base = self._resolve(out.amends_ref or out.position.preferred_proposal_ref)
                if base is not None:
                    new = self.state.registry.amend(base.ref, out.amendment, agent, self.round, self.state.world.state)
                    if new is not None:
                        any_change = True
                        self.emit("proposal.versioned", {"proposal": new.model_dump(mode="json"), "ref": new.ref,
                                                         "supersedes": base.ref,
                                                         "diff": diff_drafts(base.draft, new.draft)}, agent)
            if self._set_position(agent, out.position, "CRITIQUE"):
                any_change = True
        await asyncio.gather(*(self._run_tools(a, o.tool_requests) for a, o in outs.items() if o))
        return any_change

    async def dissent(self) -> None:
        lead = self.leading
        if lead is None:
            return
        opposed = [a for a in AGENTS
                   if (pos := self.state.positions.get(a)) and pos.preferred_proposal_ref.partition("@")[0] != lead.id]
        agent = opposed[0] if opposed else AGENTS[(self.round - 1) % 3]
        outs = await self._call_all("DISSENT", DissentOutput, agents=[agent], fmt={"leading": lead.ref},
                                    leading_ref=lead.ref)
        out = outs.get(agent)
        if out is None:
            return
        k = Critique(id=self.state.next_critique_id(), author=agent, round=self.round, decision_point=self.dp.id,
                     target_ref=lead.ref, text=out.strongest_case_against, severity="dissent", kind="dissent",
                     would_accept_if=out.failure_scenario)
        self.state.critiques.append(k)
        self.emit("dissent.posted", {"critique": k.__dict__, "failure_scenario": out.failure_scenario}, agent)

    async def vote(self, prop: Proposal) -> dict[str, VoteChoice]:
        outs = await self._call_all("VOTE", VoteOutput,
                                    fmt={"ballot": prop.ref, "hash": prop.hash, "tier": prop.tier.value},
                                    ballot_ref=prop.ref, ballot_hash=prop.hash, leading_ref=prop.ref)
        self.last_votes = {a: o for a, o in outs.items() if o is not None}
        choices = tally(prop, outs)
        for agent in AGENTS:
            out = outs.get(agent)
            self.emit("vote.cast", {"ballot": prop.ref, "choice": choices[agent].value,
                                    "reason": out.reason if out else "no valid vote (abstain)",
                                    "blocking_objection": out.blocking_objection if out else None,
                                    "would_change_if": out.would_change_if if out else ""}, agent)
            if out is not None:
                self._set_position(agent, out.position, "VOTE")
        return choices

    async def assess(self, evidence_id: str) -> None:
        ev = self.state.evidence.get(evidence_id)
        if ev is None:
            return
        viewers = [a for a in AGENTS if ev.visible(a)]
        if not viewers:
            return
        rel = self.state.scenario.reliability(ev.source)
        fmt = {"target": ev.id, "source": ev.source, "reliability": f"{rel:.2f}"}
        outs = await self._call_all("ASSESS", EvidenceAssessment, agents=viewers, fmt=fmt, target_evidence=ev.id)
        verify: list[tuple[str, Any]] = []
        for agent in viewers:
            out = outs.get(agent)
            if out is None:
                continue
            self._record_assessment(agent, ev.id, out)
            if out.verification and out.verification.tool in AGENT_TOOLS.get(agent, set()):
                verify.append((agent, out.verification))
        for agent, req in verify:
            await self.inc.run_tool(agent, req)
            res = await self._call_all("ASSESS", EvidenceAssessment, agents=[agent], fmt=fmt, target_evidence=ev.id)
            if res.get(agent) is not None:
                self._record_assessment(agent, ev.id, res[agent])

    def _record_assessment(self, agent: str, evidence_id: str, out: EvidenceAssessment) -> None:
        out = out.model_copy(update={"evidence_id": evidence_id, "credibility": clamp01(out.credibility),
                                     "source_reliability": clamp01(out.source_reliability),
                                     "plausibility": clamp01(out.plausibility)})
        self.state.assessments[(agent, evidence_id)] = out
        self.emit("evidence.assessed", {"assessment": out.model_dump(mode="json")}, agent)

    async def drain_interrupts(self) -> None:
        while not self.interrupts.empty():
            eid = self.interrupts.get_nowait()
            self.emit("council.interrupted", {"evidence_id": eid})
            await self.assess(eid)

    # ================================================================ main loop
    def _policy_block(self, prop: Proposal, choices: dict[str, VoteChoice]) -> Optional[Critique]:
        for k in self.state.critiques:
            if (k.decision_point == self.dp.id and k.kind == "objection" and k.severity == "blocking" and k.cites_policy
                    and k.target_ref.partition("@")[0] == prop.id and choices.get(k.author) == VoteChoice.REJECT):
                return k
        return None

    async def run_round(self, *, full: bool) -> tuple[Outcome, Decision, Proposal]:
        before = {a: (p.preferred_proposal_ref.partition("@")[0] if (p := self.state.positions.get(a)) else None)
                  for a in AGENTS}
        versions_before = len(self.state.registry.all_versions())
        self.emit("round.started", {"round": self.round, "full": full})
        await self.drain_interrupts()
        if full:
            self.compute_leading()
            await self.critique()
            await self.drain_interrupts()
        lead = self.compute_leading()
        await self.dissent()
        await self.drain_interrupts()
        lead = self.state.registry.latest(lead.id) or lead
        choices = await self.vote(lead)
        after = {a: (p.preferred_proposal_ref.partition("@")[0] if (p := self.state.positions.get(a)) else None)
                 for a in AGENTS}
        no_new_versions = len(self.state.registry.all_versions()) == versions_before
        stable = self.round > 1 and no_new_versions and before == after
        outcome, rule, vetoes = decide(lead, choices, self.state.world.state, self.round,
                                       self.settings.max_rounds, stable)
        if outcome == Outcome.NEXT_ROUND:
            block = self._policy_block(lead, choices)
            if block is not None and self.round >= 2:
                outcome, rule = Outcome.ESCALATE, rule + f"; blocking objection cites policy {block.cites_policy} (irreconcilable)"
            elif time.monotonic() - self.started > self.settings.decision_time_budget_s:
                outcome, rule = Outcome.ESCALATE, rule + "; decision time budget exceeded"
        decision = self.inc.new_decision(self.dp.id, self.round, lead, outcome, rule, choices, vetoes)
        return outcome, decision, lead

    async def run(self) -> None:
        self.state.dp = self.dp
        self.state.positions.clear()  # positions are per decision point; history stays in the event log
        self.emit("council.started", {"question": self.dp.question, "title": self.dp.title})
        await self.drain_interrupts()  # evidence that arrived since the last council is assessed first
        outs = await self.propose()
        insufficient = [a for a, o in outs.items() if o.insufficient_info]
        if len(insufficient) >= 2:
            self.emit("council.gathering", {"agents": insufficient})
            outs = await self.propose()
            insufficient = [a for a, o in outs.items() if o.insufficient_info]
            if len(insufficient) >= 2:
                needed = sorted({n for o in outs.values() for n in o.info_needed})
                decision = self.inc.new_decision(self.dp.id, 0, None, Outcome.INSUFFICIENT_INFO,
                                                 "≥2 agents report insufficient information after one regather", {}, [])
                await self.inc.escalate(self, decision, reason="insufficient information", info_needed=needed)
                return
        props = self.state.registry.latest_for_dp(self.dp.id)
        if not props:
            decision = self.inc.new_decision(self.dp.id, 0, None, Outcome.ESCALATE, "no valid proposals", {}, [])
            await self.inc.escalate(self, decision, reason="no valid proposals")
            return
        if len(props) > 1:
            await self.score(props)

        for r in range(1, self.settings.max_rounds + 1):
            self.round = r
            full = not (r == 1 and len(props) == 1)
            outcome, decision, lead = await self.run_round(full=full)
            self.outcome = outcome
            if outcome == Outcome.EXECUTE:
                await self.inc.execute(decision)
                return
            if outcome == Outcome.CONFIRM:
                if await self.inc.request_confirm(decision, lead):
                    await self.inc.execute(decision)
                    return
                await self.inc.escalate(self, decision, reason="T2 confirmation denied or timed out")
                return
            if outcome == Outcome.ESCALATE:
                await self.inc.escalate(self, decision, reason=decision.rule_applied)
                return
        # Unreachable: decide() escalates at max rounds.

    async def reconvene(self) -> tuple[Outcome, Decision, Proposal]:
        """New human information arrived during escalation: one more full round."""
        self.round += 1
        self.started = time.monotonic()
        return await self.run_round(full=True)
