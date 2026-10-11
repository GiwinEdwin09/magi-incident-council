"""Pareto filtering, Schulze ranking, and the risk-tiered decision rule.

Pure functions. No LLM is involved in deciding anything.
"""

from __future__ import annotations

from typing import Any

from magi.facilitator.tiers import veto_owners
from magi.models import AGENTS, Outcome, Proposal, Tier, VoteChoice, VoteOutput


def pareto(refs: list[str], scores: dict[str, tuple[float, float, float]]) -> list[str]:
    """Drop proposals another proposal beats or ties on every mandate axis (and beats on one)."""

    def dominated(r: str) -> bool:
        return any(
            all(scores[o][i] >= scores[r][i] for i in range(3)) and scores[o] != scores[r]
            for o in refs
            if o != r
        )

    keep = [r for r in refs if not dominated(r)]
    return keep or list(refs)


def schulze(cands: list[str], rankings: list[list[str]]) -> tuple[str, dict[str, Any]]:
    """Schulze winner over ranked ballots. Ties break toward the earliest candidate."""
    if len(cands) == 1:
        return cands[0], {"pairwise": {}, "wins": {cands[0]: 0}}
    d = {(a, b): 0 for a in cands for b in cands if a != b}
    for r in rankings:
        pos = {c: (r.index(c) if c in r else len(r)) for c in cands}
        for a in cands:
            for b in cands:
                if a != b and pos[a] < pos[b]:
                    d[(a, b)] += 1
    p = {(a, b): (d[(a, b)] if d[(a, b)] > d[(b, a)] else 0) for (a, b) in d}
    for i in cands:
        for j in cands:
            if i == j:
                continue
            for k in cands:
                if i != k and j != k:
                    p[(j, k)] = max(p[(j, k)], min(p[(j, i)], p[(i, k)]))
    wins = {a: sum(p[(a, b)] > p[(b, a)] for b in cands if a != b) for a in cands}
    winner = max(cands, key=lambda a: (wins[a], -cands.index(a)))
    pairwise = {f"{a}>{b}": d[(a, b)] for (a, b) in d}
    return winner, {"pairwise": pairwise, "wins": wins}


def tally(proposal: Proposal, votes: dict[str, VoteOutput | None]) -> dict[str, VoteChoice]:
    """A vote counts only if it names this exact version and hash; anything else is ABSTAIN."""
    out: dict[str, VoteChoice] = {}
    for agent in AGENTS:
        v = votes.get(agent)
        valid = v is not None and v.proposal_ref == proposal.ref and v.proposal_hash == proposal.hash
        out[agent] = v.choice if valid else VoteChoice.ABSTAIN
    return out


def decide(
    proposal: Proposal,
    choices: dict[str, VoteChoice],
    state: dict[str, Any],
    round_: int,
    max_rounds: int,
    stable: bool,
) -> tuple[Outcome, str, list[str]]:
    accepts = sum(c == VoteChoice.ACCEPT for c in choices.values())
    rejects = {a for a, c in choices.items() if c == VoteChoice.REJECT}
    vetoes = sorted(rejects & veto_owners(proposal.draft, state))

    if proposal.tier == Tier.T0 and not vetoes and accepts >= 1:
        return Outcome.EXECUTE, f"T0: {accepts}/3 ACCEPT, no mandate veto", vetoes
    if proposal.tier == Tier.T1 and accepts >= 2 and not vetoes:
        return Outcome.EXECUTE, f"T1: {accepts}/3 ACCEPT, no veto", vetoes
    if proposal.tier == Tier.T2 and accepts == 3:
        return Outcome.CONFIRM, "T2: 3/3 ACCEPT, human confirmation required", vetoes
    detail = f"{proposal.tier.value}: {accepts}/3 ACCEPT" + (f", veto by {', '.join(vetoes)}" if vetoes else "")
    if stable:
        return Outcome.ESCALATE, detail + "; positions stable (deadlock)", vetoes
    if round_ >= max_rounds:
        return Outcome.ESCALATE, detail + f"; max rounds ({max_rounds}) reached", vetoes
    return Outcome.NEXT_ROUND, detail, vetoes
