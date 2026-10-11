"""End-to-end council behavior and the need-to-know guarantees."""

from __future__ import annotations

from magi.agents import prompts
from magi.facilitator.council import Council
from magi.facilitator.state import CouncilState
from magi.llm.base import LLMResult
from magi.models import AGENTS, ClaimDraft, HumanRuling, ProposalDraft, ProposeOutput
from magi.sim.scenario import load_scenario
from magi.sim.world import World

from tests.conftest import run_scenario


def _state_with_all_evidence(scenario_id: str) -> CouncilState:
    sc = load_scenario(scenario_id)
    st = CouncilState(incident_id="INC-T", scenario=sc, world=World(sc.world))
    for item in sc.timeline:
        ev = item.to_evidence()
        st.evidence[ev.id] = ev
    for inj in sc.injections:
        st.evidence[inj.id] = inj.to_evidence()
    st.dp = sc.decision_points[0]
    return st


def test_need_to_know_prompts_only_contain_visible_evidence():
    for sid in ("s1_friday_deploy", "s2_ghost_process"):
        st = _state_with_all_evidence(sid)
        for agent in AGENTS:
            text = prompts.system_prompt(agent, st) + prompts.context_block(st, agent, anonymize=True)
            for ev in st.evidence.values():
                if ev.visible(agent):
                    assert ev.content in text, (sid, agent, ev.id)
                else:
                    assert ev.content not in text, f"{agent} saw {ev.id} in {sid}"


def test_sealed_never_leaks_outside_entitled_viewers():
    st = _state_with_all_evidence("s2_ghost_process")
    sealed = st.evidence["S-1"]
    assert sealed.sealed and "BALTHASAR" in sealed.visible_to
    for agent in ("MELCHIOR", "CASPER"):
        assert sealed.content not in prompts.context_block(st, agent, anonymize=True)
    assert sealed.content not in str(sealed.public_view())
    assert sealed.content not in prompts.context_block(st, "SCRIBE", anonymize=False)


async def test_claims_that_quote_sealed_text_are_redacted():
    class FakeInc:
        pass

    st = _state_with_all_evidence("s2_ghost_process")
    inc = FakeInc()
    inc.state, inc.settings = st, None
    events = []
    inc.bus = type("B", (), {"emit": lambda self, t, p=None, a=None: events.append((t, p))})()
    council = Council(inc, st.dp)
    leaked = st.evidence["S-1"].content
    out = ProposeOutput(assessment="a", key_claims=[ClaimDraft(text=f"Intel says: {leaked}", evidence_ids=["S-1"])],
                        proposal=ProposalDraft(title="x", actions=[]))
    council._publish_claims("BALTHASAR", out)
    claim = st.claims[-1]
    assert leaked not in claim.text and "[sealed S-1]" in claim.text and claim.sealed_ref == "S-1"


async def test_s1_auto_executes_without_paging():
    inc = await run_scenario("s1_friday_deploy")
    assert inc.closed
    decisions = inc.state.decisions
    assert [d.outcome.value for d in decisions] == ["EXECUTE"]
    assert decisions[0].votes == {"MELCHIOR": "ACCEPT", "BALTHASAR": "ACCEPT", "CASPER": "ACCEPT"}
    assert inc.metrics["pages"] == 0
    assert inc.state.world.state["services"]["checkout-api"]["version"] == "2.30"


def _rule_b(inc):
    if inc.dossier and inc._ruling and not inc._ruling.done():
        ok, _ = inc.submit_ruling(HumanRuling(option_key="B", ruled_by="Alex", confirm_code=inc.dossier.confirm_code))
        assert ok


async def test_s2_interim_containment_then_escalation_and_ruling():
    inc = await run_scenario("s2_ghost_process", on_tick=_rule_b)
    outcomes = [(d.decision_point, d.outcome.value, d.decider) for d in inc.state.decisions]
    assert outcomes[0] == ("DP1", "EXECUTE", "COUNCIL")  # reversible containment passes without a page
    assert ("DP2", "ESCALATE", "COUNCIL") in outcomes
    assert outcomes[-1] == ("DP2", "EXECUTE", "HUMAN")
    assert inc.metrics["pages"] == 1
    w = inc.state.world.state
    assert w["assets"]["db-7"]["forensics_captured"] and w["assets"]["db-7"]["isolated"]
    assert w["clusters"]["pay-db"]["primary"] == "db-8" and w["flags"]["lost_writes"] > 0


async def test_s2_rumor_is_rejected_after_tool_verification():
    def inject(inc):
        if inc.state.dp and inc.state.dp.id == "DP2" and "E-13" not in inc.state.evidence:
            inc.inject("E-13")
        _rule_b(inc)

    inc = await run_scenario("s2_ghost_process", on_tick=inject)
    a = inc.state.assessments[("BALTHASAR", "E-13")]
    assert a.verdict == "REJECT" and a.credibility < 0.2
    tools = [e.payload["tool"] for e in inc.bus.events if e.type == "tool.result" and e.agent == "BALTHASAR"]
    assert "check_ip_allowlist" in tools


async def test_s2_evidence_between_decision_points_is_assessed_by_next_council():
    def inject_between(inc):
        dp1_done = any(d.decision_point == "DP1" for d in inc.state.decisions)
        if dp1_done and inc.state.dp and inc.state.dp.id == "DP1" and "E-13" not in inc.state.evidence:
            inc.inject("E-13")
        _rule_b(inc)

    inc = await run_scenario("s2_ghost_process", on_tick=inject_between)
    assert inc.state.evidence["E-13"].sim_ts < 150  # arrived before DP2 opened
    assert inc.state.assessments[("BALTHASAR", "E-13")].verdict == "REJECT"
    assert ("MELCHIOR", "E-12") in inc.state.assessments  # timeline evidence between councils too


async def test_s2_human_info_reopens_deliberation():
    def add_info(inc):
        if inc.dossier and inc._ruling and not inc._ruling.done() and not any(
                e.type == "human.info_added" for e in inc.bus.events):
            inc.add_human_info("I approve discarding the in-flight writes.")
        for d, f in list(inc._confirms.items()):
            if not f.done():
                inc.confirm_result(d, True, "Alex")

    inc = await run_scenario("s2_ghost_process", on_tick=add_info)
    last = inc.state.decisions[-1]
    assert last.outcome.value == "CONFIRM" and last.proposal_ref == "P-5@1"
    changes = [e for e in inc.bus.events if e.type == "position.updated" and e.payload["position"]["changed"]
               and e.payload["decision_point"] == "DP2"]
    assert changes and all(e.payload["position"]["change_cause"] == "NEW_EVIDENCE" for e in changes)
    assert not any("conformity_risk" in e.payload["flags"] for e in changes)


async def test_failures_move_toward_the_human_never_toward_action():
    class Broken:
        name = "broken"

        async def structured(self, **kw):
            return LLMResult(None, "timeout")

    adapters = {a: Broken() for a in (*AGENTS, "SCRIBE")}

    def rule_or_stop(inc):
        if inc.dossier and inc._ruling and not inc._ruling.done():
            inc._ruling.cancel()

    inc = await run_scenario("s1_friday_deploy", adapters=adapters, on_tick=rule_or_stop, timeout_s=5)
    assert inc.state.decisions and inc.state.decisions[0].outcome.value == "ESCALATE"
    assert not any(e.type == "action.result" for e in inc.bus.events)
