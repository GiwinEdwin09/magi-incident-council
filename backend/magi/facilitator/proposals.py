"""Immutable, versioned proposal registry."""

from __future__ import annotations

import difflib
from typing import Any, Optional

from magi.facilitator.tiers import classify_draft
from magi.models import Proposal, ProposalDraft, canonical_actions, draft_hash


class ProposalRegistry:
    def __init__(self) -> None:
        self._versions: dict[str, list[Proposal]] = {}
        self._counter = 0

    # ------------------------------------------------------------ lookups
    def get(self, ref: str) -> Optional[Proposal]:
        if "@" not in ref:
            return self.latest(ref)
        pid, _, ver = ref.partition("@")
        versions = self._versions.get(pid, [])
        try:
            v = int(ver)
        except ValueError:
            return None
        return versions[v - 1] if 0 < v <= len(versions) else None

    def latest(self, pid: str) -> Optional[Proposal]:
        versions = self._versions.get(pid.partition("@")[0])
        return versions[-1] if versions else None

    def resolve_latest(self, ref: str) -> Optional[Proposal]:
        """Any ref (old version or bare id) resolves to that proposal's newest version."""
        return self.latest(ref.partition("@")[0])

    def latest_for_dp(self, dp: str) -> list[Proposal]:
        return [v[-1] for v in self._versions.values() if v[-1].decision_point == dp]

    def all_versions(self) -> list[Proposal]:
        return [p for v in self._versions.values() for p in v]

    # ------------------------------------------------------------ mutations
    def _find_same_actions(self, draft: ProposalDraft, dp: str) -> Optional[Proposal]:
        key = canonical_actions(draft)
        for p in self.latest_for_dp(dp):
            if canonical_actions(p.draft) == key:
                return p
        return None

    def create(
        self, draft: ProposalDraft, author: str, round_: int, dp: str, state: dict[str, Any]
    ) -> tuple[Proposal, bool]:
        """Register a new proposal. Identical action sets merge (author becomes co-author)."""
        existing = self._find_same_actions(draft, dp)
        if existing is not None:
            if author != existing.author and author not in existing.co_authors:
                existing.co_authors.append(author)
            return existing, True
        self._counter += 1
        tier, reasons = classify_draft(draft, state)
        prop = Proposal(
            id=f"P-{self._counter}",
            version=1,
            hash=draft_hash(draft),
            author=author,
            draft=draft,
            tier=tier,
            tier_reasons=reasons,
            created_round=round_,
            decision_point=dp,
        )
        self._versions[prop.id] = [prop]
        return prop, False

    def amend(
        self, ref: str, draft: ProposalDraft, author: str, round_: int, state: dict[str, Any]
    ) -> Optional[Proposal]:
        base = self.resolve_latest(ref)
        if base is None:
            return None
        if canonical_actions(draft) == canonical_actions(base.draft) and draft.title == base.draft.title:
            return None
        tier, reasons = classify_draft(draft, state)
        prop = Proposal(
            id=base.id,
            version=base.version + 1,
            hash=draft_hash(draft),
            author=author,
            co_authors=[],
            supersedes=base.ref,
            draft=draft,
            tier=tier,
            tier_reasons=reasons,
            created_round=round_,
            decision_point=base.decision_point,
        )
        self._versions[base.id].append(prop)
        return prop

    def retier(self, state: dict[str, Any], dp: str) -> list[Proposal]:
        """World changed: recompute tiers of the live versions in place (tiers are live)."""
        changed = []
        for p in self.latest_for_dp(dp):
            tier, reasons = classify_draft(p.draft, state)
            if tier != p.tier:
                p.tier, p.tier_reasons = tier, reasons
                changed.append(p)
        return changed


def diff_drafts(old: ProposalDraft, new: ProposalDraft) -> list[str]:
    a = [f"title: {old.title}"] + [x.label() for x in old.actions]
    b = [f"title: {new.title}"] + [x.label() for x in new.actions]
    return [line for line in difflib.ndiff(a, b) if line[:1] in "+-"]
