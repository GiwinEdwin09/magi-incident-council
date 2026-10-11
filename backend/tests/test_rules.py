"""Decision rules, tiers, voting, attribution, certificates: the claims we make on stage."""

from magi.facilitator import certificate
from magi.facilitator.attribution import validate_cause
from magi.facilitator.proposals import ProposalRegistry
from magi.facilitator.tiers import classify, classify_draft, veto_owners
from magi.facilitator.voting import decide, pareto, schulze, tally
from magi.models import (ActionCall, ChangeCause, Outcome, Param, Position, ProposalDraft, Tier, VoteChoice,
                         VoteOutput)

WORLD = {
    "assets": {"db-7": {"serving": True, "suspicious": True, "forensics_captured": False},
               "web-1": {"serving": True, "suspicious": False}},
    "clusters": {"pay-db": {"replication_lag_s": 45, "write_rate_per_s": 27},
                 "ok-db": {"replication_lag_s": 0, "write_rate_per_s": 10}},
    "services": {"checkout-api": {"migration_since_previous": False}},
}


def act(aid: str, **params) -> ActionCall:
    return ActionCall(action_id=aid, params=[Param(name=k, value=str(v)) for k, v in params.items()])


def draft(*actions: ActionCall) -> ProposalDraft:
    return ProposalDraft(title="t", actions=list(actions))


def test_classify_is_live():
    assert classify(act("host.restart", host="db-7"), WORLD)[0] == Tier.T2
    assert classify(act("host.restart", host="web-1"), WORLD)[0] == Tier.T1
    captured = {**WORLD, "assets": {**WORLD["assets"], "db-7": {**WORLD["assets"]["db-7"], "forensics_captured": True}}}
    assert classify(act("host.restart", host="db-7"), captured)[0] == Tier.T1
    assert classify(act("db.failover", cluster="pay-db"), WORLD)[0] == Tier.T2
    assert classify(act("db.failover", cluster="ok-db"), WORLD)[0] == Tier.T1
    assert classify(act("db.failover", cluster="pay-db", when="lag<5s"), WORLD)[0] == Tier.T1
    assert classify(act("traffic.shed", service="x", percent=30), WORLD)[0] == Tier.T2
    assert classify(act("traffic.shed", service="x", percent=20), WORLD)[0] == Tier.T1
    assert classify(act("security.disable_control", control="waf", scope="global", minutes=10), WORLD)[0] == Tier.T2
    assert classify(act("db.wipe_and_resync", host="db-8"), WORLD)[0] == Tier.T2
    assert classify(act("hold", minutes=5), WORLD)[0] == Tier.T0
    assert classify(act("not.a.real.action"), WORLD)[0] == Tier.T2
    tier, reasons = classify_draft(draft(act("hold", minutes=1), act("host.restart", host="db-7")), WORLD)
    assert tier == Tier.T2 and any("suspicious" in r for r in reasons)


def test_veto_owners():
    assert veto_owners(draft(act("host.restart", host="db-7")), WORLD) == {"BALTHASAR"}
    assert veto_owners(draft(act("db.failover", cluster="pay-db")), WORLD) == {"CASPER"}
    assert veto_owners(draft(act("host.isolate_network", host="db-7")), WORLD) == {"MELCHIOR"}
    assert veto_owners(draft(act("deploy.rollback", service="checkout-api", to_version="1")), WORLD) == set()


def _prop(reg: ProposalRegistry, d: ProposalDraft):
    return reg.create(d, "MELCHIOR", 0, "DP1", WORLD)[0]


def _votes(prop, **choices):
    return {a: VoteOutput(proposal_ref=prop.ref, proposal_hash=prop.hash, choice=VoteChoice(c), reason="r",
                          position=Position(preferred_proposal_ref=prop.ref)) for a, c in choices.items()}


def test_decide_tiers_and_vetoes():
    reg = ProposalRegistry()
    t1 = _prop(reg, draft(act("deploy.rollback", service="checkout-api", to_version="1")))
    ch = tally(t1, _votes(t1, MELCHIOR="ACCEPT", BALTHASAR="ACCEPT", CASPER="REJECT"))
    assert decide(t1, ch, WORLD, 1, 3, False)[0] == Outcome.EXECUTE

    vetoed = _prop(reg, draft(act("host.restart", host="web-1"), act("status_page.publish", severity="x", message="y")))
    ch = tally(vetoed, _votes(vetoed, MELCHIOR="ACCEPT", BALTHASAR="ACCEPT", CASPER="REJECT"))
    out, rule, vetoes = decide(vetoed, ch, WORLD, 1, 3, False)
    assert out == Outcome.NEXT_ROUND and vetoes == ["CASPER"]

    t2 = _prop(reg, draft(act("db.failover", cluster="pay-db")))
    ch = tally(t2, _votes(t2, MELCHIOR="ACCEPT", BALTHASAR="ACCEPT", CASPER="ACCEPT"))
    assert decide(t2, ch, WORLD, 1, 3, False)[0] == Outcome.CONFIRM
    ch = tally(t2, _votes(t2, MELCHIOR="ACCEPT", BALTHASAR="ACCEPT", CASPER="ABSTAIN"))
    assert decide(t2, ch, WORLD, 1, 3, False)[0] == Outcome.NEXT_ROUND
    assert decide(t2, ch, WORLD, 2, 3, True)[0] == Outcome.ESCALATE
    assert decide(t2, ch, WORLD, 3, 3, False)[0] == Outcome.ESCALATE


def test_vote_on_wrong_version_or_hash_is_abstain():
    reg = ProposalRegistry()
    p = _prop(reg, draft(act("db.failover", cluster="pay-db")))
    votes = _votes(p, MELCHIOR="ACCEPT", BALTHASAR="ACCEPT", CASPER="ACCEPT")
    votes["CASPER"] = votes["CASPER"].model_copy(update={"proposal_hash": "sha256:forged"})
    ch = tally(p, votes)
    assert ch["CASPER"] == VoteChoice.ABSTAIN
    assert decide(p, ch, WORLD, 1, 3, False)[0] != Outcome.CONFIRM


def test_registry_merges_and_versions():
    reg = ProposalRegistry()
    a, merged_a = reg.create(draft(act("hold", minutes=1)), "MELCHIOR", 0, "DP1", WORLD)
    b, merged_b = reg.create(draft(act("hold", minutes=1)), "CASPER", 0, "DP1", WORLD)
    assert not merged_a and merged_b and a is b and b.co_authors == ["CASPER"]
    v2 = reg.amend(a.ref, ProposalDraft(title="t2", actions=[act("hold", minutes=2)]), "BALTHASAR", 1, WORLD)
    assert v2.ref == "P-1@2" and v2.supersedes == "P-1@1" and v2.hash != a.hash
    assert reg.get("P-1@1").draft.actions[0].p["minutes"] == "1"  # old versions never mutate
    assert reg.latest("P-1").version == 2


def test_schulze_condorcet_and_cycle():
    winner, _ = schulze(["A", "B", "C"], [["A", "B", "C"], ["B", "A", "C"], ["A", "C", "B"]])
    assert winner == "A"
    cycle = [["A", "B", "C"], ["B", "C", "A"], ["C", "A", "B"]]
    assert schulze(["A", "B", "C"], cycle)[0] == "A"  # tie breaks toward earliest
    assert schulze(["X"], [["X"]])[0] == "X"


def test_pareto():
    scores = {"A": (5, 5, 5), "B": (4, 5, 5), "C": (9, 1, 1)}
    assert pareto(["A", "B", "C"], scores) == ["A", "C"]
    assert pareto(["A"], {"A": (1, 1, 1)}) == ["A"]


def test_change_cause_validator():
    pos = Position(preferred_proposal_ref="P-2@1", changed=True, change_cause=ChangeCause.NEW_EVIDENCE, cited_ids=["E-1"])
    out, flags = validate_cause(pos, released_since_last={"E-9"}, round_argument_ids=set())
    assert out.change_cause == ChangeCause.PEER_AGREEMENT_ONLY and "cause_unsupported" in flags
    out, flags = validate_cause(pos, released_since_last={"E-1"}, round_argument_ids=set())
    assert out.change_cause == ChangeCause.NEW_EVIDENCE and flags == []
    arg = Position(preferred_proposal_ref="P-2@1", changed=True, change_cause=ChangeCause.NEW_ARGUMENT, cited_ids=["K-3"])
    assert validate_cause(arg, set(), {"K-3"})[1] == []
    silent = Position(preferred_proposal_ref="P-2@1", changed=True, change_cause=ChangeCause.NO_CHANGE)
    assert "cause_missing" in validate_cause(silent, set(), set())[1]


def test_certificate():
    sig = certificate.sign("k", "D-1", "sha256:abc", "EXECUTE")
    assert certificate.verify("k", sig, "D-1", "sha256:abc", "EXECUTE")
    assert not certificate.verify("k", sig, "D-1", "sha256:abc", "CONFIRM")
    assert not certificate.verify("other", sig, "D-1", "sha256:abc", "EXECUTE")
