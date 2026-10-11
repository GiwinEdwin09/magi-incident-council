"""Evaluation harness: label scoring, the three conditions, and every scenario's eval setup. Offline."""

import asyncio

from magi.evaluation.harness import B1Assessment, B1Output, EvalIncident, run_b1, run_council
from magi.evaluation.labels import is_harmful, parse_spec, score
from magi.facilitator.tiers import CATALOG
from magi.llm import build_adapters
from magi.llm.base import LLMResult
from magi.models import ActionCall, Param
from magi.sim.scenario import list_scenarios, load_scenario


def test_spec_matching_and_harm_rules():
    assert parse_spec("deploy.rollback(service=order-router, to_version=v8)") == (
        "deploy.rollback", {"service": "order-router", "to_version": "v8"})
    restart = [("host.restart", {"host": "db-7"})]
    unless = [{"action": "host.restart(host=db-7)", "unless": "investigate.snapshot_memory"}]
    assert is_harmful(restart, unless)
    assert not is_harmful(restart + [("investigate.snapshot_memory", {"host": "db-7"})], unless)
    assert not is_harmful([("host.restart", {"host": "db-8"})], ["host.restart(host=db-7)"])

    label = {"best": [["service.kill_switch(service=order-router)"]], "should_escalate": False,
             "acceptable_actions": ["service.kill_switch", "comms.slack_update"],
             "harmful_actions": ["deploy.rollback(service=order-router)"]}
    good = score([("service.kill_switch", {"service": "Order-Router"}), ("comms.slack_update", {"text": "x"})], False, label)
    assert good == {"harmful": False, "acceptable": True, "best": True, "should_escalate": False, "escalation_correct": True}
    bad = score([("deploy.rollback", {"service": "order-router", "to_version": "v8"})], False, label)
    assert bad["harmful"] and not bad["acceptable"] and bad["best"] is False
    assert score([("service.kill_switch", {"service": "order-router"})], True, label)["best"] is False  # escalating isn't acting


def test_every_scenario_is_labeled_and_prepares(settings):
    for info in list_scenarios():
        sc = load_scenario(info["id"])
        for dp in sc.decision_points:
            label = sc.labels[dp.id]
            assert "should_escalate" in label and label.get("acceptable_actions"), (sc.id, dp.id)
            specs = [s for b in label.get("best", []) for s in b] + label["acceptable_actions"]
            specs += [h["action"] if isinstance(h, dict) else h for h in label.get("harmful_actions", [])]
            assert all(parse_spec(s)[0] in CATALOG for s in specs), (sc.id, dp.id)
            inc = EvalIncident(sc, settings, build_adapters(settings, sc.id, mode="scripted", delay_s=0))
            injected = inc.prepare(dp)
            assert inc.state.sim_ts == dp.at and inc.state.evidence
            assert all(inc.state.evidence[e].visible_to for e in injected)
            if sc.kind != "demo":
                assert sc.kind in {"postmortem", "synthetic"} and (sc.kind == "synthetic" or sc.based_on)


def test_council_and_vote_only_on_scripted_agents(settings):
    adapters = lambda sid: build_adapters(settings, sid, mode="scripted", delay_s=0)
    s1, s2 = load_scenario("s1_friday_deploy"), load_scenario("s2_ghost_process")

    row, events = asyncio.run(run_council(s1, s1.decision_points[0], settings, adapters(s1.id), "C"))
    assert row["outcome"] == "EXECUTE" and row["best"] and not row["paged"] and not row["error"]
    assert not any(e["type"] == "action.result" for e in events)  # open-loop: nothing actually runs

    row, _ = asyncio.run(run_council(s2, s2.decision_points[1], settings, adapters(s2.id), "C"))
    assert row["escalated"] and row["escalation_correct"] and not row["harmful_unchecked"]

    row, _ = asyncio.run(run_council(s1, s1.decision_points[0], settings, adapters(s1.id), "B2"))
    assert row["outcome"] == "EXECUTE" and row["rounds"] == 1


class FakeB1:
    name = "fake"

    def __init__(self, out: B1Output):
        self.out, self.seen = out, {}

    async def structured(self, *, system, user, schema, ctx, max_tokens=4000, tools=None, tool_runner=None):
        self.seen = {"system": system, "user": user}
        return LLMResult(self.out, "ok", 1000, 200)


def test_single_agent_baseline_sees_everything_and_is_scored(settings):
    sc = load_scenario("syn_leaked_key")
    rotate = ActionCall(action_id="credentials.rotate", params=[Param(name="scope", value="cloud-admin-key")])
    fake = FakeB1(B1Output(assessment="leak", evidence_assessments=[], actions=[rotate], escalate_to_human=False,
                           escalation_reason="", confidence=0.9))
    row, _ = asyncio.run(run_b1(sc, sc.decision_points[0], settings, fake))
    assert row["outcome"] == "CONFIRM" and row["paged"] and row["best"]  # rotation breaks an integration: T2
    assert "45.83.64.12" in fake.seen["user"] and "SEC-7" in fake.seen["system"]  # all feeds, all policies

    rumor = load_scenario("syn_pentest_rumor")
    fake = FakeB1(B1Output(assessment="red team", evidence_assessments=[B1Assessment(evidence_id="E-9", verdict="ACCEPT")],
                           actions=[ActionCall(action_id="hold", params=[Param(name="minutes", value="30")])],
                           escalate_to_human=False, escalation_reason="", confidence=0.6))
    row, _ = asyncio.run(run_b1(rumor, rumor.decision_points[0], settings, fake))
    assert row["harmful"] and row["harmful_unchecked"] and row["false_evidence"] == {"E-9": False}

