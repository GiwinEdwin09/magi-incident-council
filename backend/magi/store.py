"""Append-only SQLite event log.

Live incidents run in memory; this log is what survives a restart. Past incidents are read back
from it, and incidents a restart cut off are closed here with an `incident.ended` event.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path

TERMINAL = ("incident.resolved", "incident.ended")


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
            {"seq": r[0], "id": f"{incident_id}-{r[0]}", "incident_id": incident_id, "type": r[1], "ts": r[2],
             "sim_ts": r[3], "agent": r[4], "payload": json.loads(r[5])}
            for r in rows
        ]

    def incidents(self, limit: int = 50) -> list[dict]:
        """Newest first: id, title, mode, when it opened, and its status (running/resolved/stopped/interrupted)."""
        with self._lock:
            opened = self._conn.execute(
                "SELECT incident_id, ts, payload FROM events WHERE type='incident.opened' ORDER BY ts DESC LIMIT ?",
                (limit,),
            ).fetchall()
            ends = self._conn.execute(
                f"SELECT incident_id, type, payload FROM events WHERE type IN {TERMINAL} ORDER BY seq"
            ).fetchall()
        status: dict[str, str] = {}
        for iid, type_, payload in ends:
            status[iid] = "resolved" if type_ == "incident.resolved" else json.loads(payload).get("reason", "ended")
        out = []
        for iid, ts, payload in opened:
            p = json.loads(payload)
            out.append({"id": iid, "title": p.get("title", ""), "mode": p.get("mode", ""), "opened_at": ts,
                        "status": status.get(iid, "running")})
        return out

    def mark_interrupted(self, detail: str) -> list[str]:
        """Close every incident with no terminal event. Run at startup, when nothing is live in memory."""
        with self._lock:
            rows = self._conn.execute(
                f"""SELECT incident_id, MAX(seq), MAX(sim_ts) FROM events GROUP BY incident_id
                    HAVING SUM(type IN {TERMINAL}) = 0"""
            ).fetchall()
            for iid, seq, sim_ts in rows:
                self._conn.execute(
                    "INSERT INTO events VALUES (?,?,?,?,?,?,?)",
                    (iid, seq + 1, "incident.ended", datetime.now(timezone.utc).isoformat(), sim_ts or 0.0, None,
                     json.dumps({"reason": "interrupted", "detail": detail})),
                )
            self._conn.commit()
        return [r[0] for r in rows]
