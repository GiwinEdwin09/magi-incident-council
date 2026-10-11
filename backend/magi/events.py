"""Event bus. Every state change is an event: stored append-only, then broadcast.

The UI, the decision record, eval metrics and replay all read the same log.
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from pydantic import BaseModel


class MagiEvent(BaseModel):
    seq: int
    id: str
    incident_id: str
    type: str
    ts: str
    sim_ts: float
    agent: Optional[str] = None
    payload: dict[str, Any]


class EventBus:
    def __init__(self, incident_id: str, clock: Callable[[], float], store=None):
        self.incident_id = incident_id
        self.clock = clock
        self.store = store
        self.events: list[MagiEvent] = []
        self._subscribers: set[asyncio.Queue] = set()

    def emit(self, type_: str, payload: dict[str, Any] | None = None, agent: str | None = None) -> MagiEvent:
        event = MagiEvent(
            seq=len(self.events) + 1,
            id=uuid.uuid4().hex[:12],
            incident_id=self.incident_id,
            type=type_,
            ts=datetime.now(timezone.utc).isoformat(),
            sim_ts=round(self.clock(), 2),
            agent=agent,
            payload=payload or {},
        )
        self.events.append(event)
        if self.store is not None:
            self.store.append(event)
        for q in list(self._subscribers):
            q.put_nowait(event)
        return event

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self._subscribers.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self._subscribers.discard(q)

    def since(self, seq: int) -> list[MagiEvent]:
        return [e for e in self.events if e.seq > seq]
