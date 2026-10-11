"""Decision certificates: n8n executes only actions carrying a valid HMAC."""

from __future__ import annotations

import hashlib
import hmac


def _message(decision_id: str, proposal_hash: str, outcome: str) -> bytes:
    return f"{decision_id}|{proposal_hash}|{outcome}".encode()


def sign(key: str, decision_id: str, proposal_hash: str, outcome: str) -> str:
    mac = hmac.new(key.encode(), _message(decision_id, proposal_hash, outcome), hashlib.sha256)
    return "hmac-sha256:" + mac.hexdigest()


def verify(key: str, signature: str, decision_id: str, proposal_hash: str, outcome: str) -> bool:
    return hmac.compare_digest(sign(key, decision_id, proposal_hash, outcome), signature or "")
