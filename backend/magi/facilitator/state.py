"""Shared council state for one incident. Owned by the Facilitator; agents only ever
see views of it filtered by visibility."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from magi.facilitator.proposals import ProposalRegistry
from magi.models import Claim, Decision, EvidenceAssessment, Evidence, Position
from magi.sim.scenario import DecisionPoint, Scenario
from magi.sim.world import World

MANDATE_LABEL = {"MELCHIOR": "reliability", "BALTHASAR": "security", "CASPER": "customers"}


@dataclass
class Critique:
    id: str
    author: str
    round: int
    decision_point: str
    target_ref: str
    text: str
    severity: str
    cites_policy: Optional[str] = None
    would_accept_if: str = ""
    kind: str = "objection"  # objection | challenge | dissent


@dataclass
class CouncilState:
    incident_id: str
    scenario: Scenario
    world: World
    evidence: dict[str, Evidence] = field(default_factory=dict)
    claims: list[Claim] = field(default_factory=list)
    registry: ProposalRegistry = field(default_factory=ProposalRegistry)
    critiques: list[Critique] = field(default_factory=list)
    positions: dict[str, Position] = field(default_factory=dict)
    assessments: dict[tuple[str, str], EvidenceAssessment] = field(default_factory=dict)
    decisions: list[Decision] = field(default_factory=list)
    sim_ts: float = 0.0
    dp: Optional[DecisionPoint] = None
    _ev_counter: int = 100
    _claim_counter: int = 0
    _critique_counter: int = 0

    def visible_evidence(self, viewer: str) -> list[Evidence]:
        return [e for e in self.evidence.values() if e.visible(viewer)]

    def next_evidence_id(self) -> str:
        self._ev_counter += 1
        return f"E-{self._ev_counter}"

    def next_claim_id(self) -> str:
        self._claim_counter += 1
        return f"C-{self._claim_counter}"

    def next_critique_id(self) -> str:
        self._critique_counter += 1
        return f"K-{self._critique_counter}"

    def sealed_contents(self) -> dict[str, str]:
        return {e.id: e.content for e in self.evidence.values() if e.sealed}
