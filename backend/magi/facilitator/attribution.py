"""Change-of-mind attribution: every position change must name a supported cause."""

from __future__ import annotations

from magi.models import ChangeCause, Position


def validate_cause(
    pos: Position, released_since_last: set[str], round_argument_ids: set[str]
) -> tuple[Position, list[str]]:
    flags: list[str] = []
    cited = set(pos.cited_ids)
    if pos.changed and pos.change_cause == ChangeCause.NEW_EVIDENCE and not (cited & released_since_last):
        pos = pos.model_copy(update={"change_cause": ChangeCause.PEER_AGREEMENT_ONLY})
        flags.append("cause_unsupported")
    elif pos.changed and pos.change_cause == ChangeCause.NEW_ARGUMENT and not (cited & round_argument_ids):
        pos = pos.model_copy(update={"change_cause": ChangeCause.PEER_AGREEMENT_ONLY})
        flags.append("cause_unsupported")
    if pos.changed and pos.change_cause == ChangeCause.NO_CHANGE:
        pos = pos.model_copy(update={"change_cause": ChangeCause.PEER_AGREEMENT_ONLY})
        flags.append("cause_missing")
    if pos.change_cause == ChangeCause.PEER_AGREEMENT_ONLY:
        flags.append("conformity_risk")
    return pos, flags
