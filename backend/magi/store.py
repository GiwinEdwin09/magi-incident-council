"""Append-only SQLite event log."""

from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path


class EventStore:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._lock = threading.Lock()
        with self._lock:
            self._conn.execute(
                """CREATE TABLE IF NOT EXISTS events (
                    incident_id TEXT, seq INTEGER, type TEXT, ts TEXT, sim_ts REAL,
                    agent TEXT, payload TEXT, PRIMARY KEY (incident_id, seq))"""
            )
            self._conn.commit()

    def append(self, event) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO events VALUES (?,?,?,?,?,?,?)",
                (
                    event.incident_id,
                    event.seq,
                    event.type,
                    event.ts,
                    event.sim_ts,
                    event.agent,
                    json.dumps(event.payload, default=str),
                ),
            )
            self._conn.commit()

    def load(self, incident_id: str) -> list[dict]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT seq, type, ts, sim_ts, agent, payload FROM events WHERE incident_id=? ORDER BY seq",
                (incident_id,),
            ).fetchall()
        return [
            {"seq": r[0], "type": r[1], "ts": r[2], "sim_ts": r[3], "agent": r[4], "payload": json.loads(r[5])}
            for r in rows
        ]
