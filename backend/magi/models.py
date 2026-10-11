"""The MAGI data contract.

Everything the agents produce, everything the Facilitator records, and every
payload the frontend renders is defined here. LLM output schemas avoid numeric
range constraints and free-form dicts so they stay compatible with structured
outputs on any provider; ranges are clamped in code instead.
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field

AGENTS: tuple[str, ...] = ("MELCHIOR", "BALTHASAR", "CASPER")
AgentName = Literal["MELCHIOR", "BALTHASAR", "CASPER"]


class Tier(str, Enum):
    T0 = "T0"
    T1 = "T1"
    T2 = "T2"


class ChangeCause(str, Enum):
    NEW_EVIDENCE = "NEW_EVIDENCE"
    NEW_ARGUMENT = "NEW_ARGUMENT"
    OWN_ERROR = "OWN_ERROR"
    PEER_AGREEMENT_ONLY = "PEER_AGREEMENT_ONLY"
    NO_CHANGE = "NO_CHANGE"


class VoteChoice(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    ABSTAIN = "ABSTAIN"


class Outcome(str, Enum):
    EXECUTE = "EXECUTE"
    CONFIRM = "CONFIRM"
    NEXT_ROUND = "NEXT_ROUND"
    ESCALATE = "ESCALATE"
    INSUFFICIENT_INFO = "INSUFFICIENT_INFO"
    HOLD = "HOLD"


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


# ---------------------------------------------------------------- primitives


class Param(BaseModel):
    name: str
    value: str


def params_dict(params: list[Param]) -> dict[str, str]:
    return {p.name: p.value for p in params}


class ActionCall(BaseModel):
    action_id: str
    params: list[Param] = Field(default_factory=list)

    @property
    def p(self) -> dict[str, str]:
        return params_dict(self.params)

    def label(self) -> str:
        args = ", ".join(f"{p.name}={p.value}" for p in self.params)
        return f"{self.action_id}({args})"


class ToolRequest(BaseModel):
    tool: str
    params: list[Param] = Field(default_factory=list)
    reason: str = ""


# ---------------------------------------------------------------- evidence


class Evidence(BaseModel):
    id: str
    sim_ts: float
    source: str
    visible_to: list[str]
    content: str
    sealed: bool = False
    sealed_hash: Optional[str] = None
    is_false: bool = False  # eval ground truth only; never rendered into prompts
    label: Optional[str] = None
    requested_by: Optional[str] = None

    def visible(self, viewer: str) -> bool:
        return viewer in self.visible_to

    def public_view(self) -> dict:
        """Payload safe for the UI/event log: sealed content is never included."""
        data = self.model_dump(exclude={"is_false"})
        if self.sealed:
            data["content"] = f"[SEALED {self.sealed_hash}]"
        return data


def seal_hash(content: str) -> str:
    return "sha256:" + hashlib.sha256(content.encode()).hexdigest()[:12]


class ClaimDraft(BaseModel):
    text: str
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float = 0.5


class Claim(ClaimDraft):
    id: str
    author: str
    round: int = 0
    decision_point: str = ""
    sealed_ref: Optional[str] = None


# ---------------------------------------------------------------- proposals


class ProposalDraft(BaseModel):
    title: str
    actions: list[ActionCall]
    rationale: str = ""
    expected_outcome: str = ""
    risks: list[str] = Field(default_factory=list)


def draft_hash(draft: ProposalDraft) -> str:
    blob = json.dumps(draft.model_dump(), sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(blob.encode()).hexdigest()[:16]


def canonical_actions(draft: ProposalDraft) -> str:
    acts = sorted((a.action_id, sorted(a.p.items())) for a in draft.actions)
    return json.dumps(acts, separators=(",", ":"))


class Proposal(BaseModel):
    id: str
    version: int
    hash: str
    author: str
    co_authors: list[str] = Field(default_factory=list)
    supersedes: Optional[str] = None
    draft: ProposalDraft
    tier: Tier
    tier_reasons: list[str]
    created_round: int
    decision_point: str

    @property
    def ref(self) -> str:
        return f"{self.id}@{self.version}"


# ---------------------------------------------------------------- agent outputs


class ProposeOutput(BaseModel):
    assessment: str
    key_claims: list[ClaimDraft] = Field(default_factory=list)
    proposal: ProposalDraft
    confidence: float = 0.5
    insufficient_info: bool = False
    info_needed: list[str] = Field(default_factory=list)
    tool_requests: list[ToolRequest] = Field(default_factory=list)


class ProposalScore(BaseModel):
    proposal_ref: str
    score: int
    reason: str = ""


class ScoreOutput(BaseModel):
    scores: list[ProposalScore]
    ranking: list[str]


class Objection(BaseModel):
    proposal_ref: str
    text: str
    severity: Literal["blocking", "major", "minor"]
    cites_policy: Optional[str] = None
    would_accept_if: str = ""


class ClaimChallenge(BaseModel):
    claim_id: str
    challenge: str
    requested_evidence: str = ""


class Position(BaseModel):
    preferred_proposal_ref: str
    confidence: float = 0.5
    changed: bool = False
    change_cause: ChangeCause = ChangeCause.NO_CHANGE
    cited_ids: list[str] = Field(default_factory=list)


class CritiqueOutput(BaseModel):
    objections: list[Objection] = Field(default_factory=list)
    challenges: list[ClaimChallenge] = Field(default_factory=list)
    amendment: Optional[ProposalDraft] = None
    amends_ref: Optional[str] = None
    position: Position
    tool_requests: list[ToolRequest] = Field(default_factory=list)


class DissentOutput(BaseModel):
    target_ref: str
    strongest_case_against: str
    failure_scenario: str


class VoteOutput(BaseModel):
    proposal_ref: str
    proposal_hash: str
    choice: VoteChoice
    reason: str
    blocking_objection: Optional[str] = None
    would_change_if: str = ""
    position: Position


class EvidenceAssessment(BaseModel):
    evidence_id: str
    source_reliability: float = 0.5
    plausibility: float = 0.5
    corroborating_ids: list[str] = Field(default_factory=list)
    contradicting_ids: list[str] = Field(default_factory=list)
    credibility: float = 0.5
    verdict: Literal["ACCEPT", "DOUBT", "REJECT"]
    reason: str
    verification: Optional[ToolRequest] = None


class ScribeOutput(BaseModel):
    """Escalation summary. The scribe has no vote and no mandate."""

    situation: str
    crux: str
    option_summaries: list[str]


# ---------------------------------------------------------------- decisions


class Decision(BaseModel):
    id: str
    decision_point: str
    round: int
    proposal_ref: Optional[str] = None
    proposal_hash: Optional[str] = None
    tier: Optional[Tier] = None
    outcome: Outcome
    rule_applied: str
    votes: dict[str, VoteChoice] = Field(default_factory=dict)
    vetoes: list[str] = Field(default_factory=list)
    decider: Literal["COUNCIL", "HUMAN"] = "COUNCIL"
    ruled_by: Optional[str] = None
    actions: list[ActionCall] = Field(default_factory=list)
    certificate: Optional[str] = None


class EscalationOption(BaseModel):
    key: Literal["A", "B", "C"]
    proposal_ref: str
    summary: str
    supporters: list[str]
    main_risk: str
    tier: Tier


class Dossier(BaseModel):
    incident_id: str
    decision_point: str
    title: str
    situation: str
    crux: str
    options: list[EscalationOption]
    positions: dict[str, str]
    sealed_available: list[str]
    confirm_code: str
    info_needed: list[str] = Field(default_factory=list)
    reason: str = ""

    def public_view(self) -> dict:
        return self.model_dump(exclude={"confirm_code"})


class HumanRuling(BaseModel):
    option_key: Literal["A", "B", "C", "CUSTOM"]
    conditions: str = ""
    custom_instruction: str = ""
    ruled_by: str = "on-call"
    via: Literal["voice", "slack", "ui"] = "ui"
    confirm_code: str = ""
