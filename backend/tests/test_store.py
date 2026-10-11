"""The event log is what survives a restart: past incidents list, replay and close correctly."""

from magi.events import EventBus
from magi.incident import build_record
from magi.store import EventStore


def _bus(store: EventStore, incident_id: str) -> EventBus:
    return EventBus(incident_id, clock=lambda: 12.0, store=store)


def test_history_status_and_restart(tmp_path):
    store = EventStore(str(tmp_path / "magi.sqlite"))
    done = _bus(store, "INC-DONE")
    done.emit("incident.opened", {"title": "Finished", "mode": "scripted"})
    done.emit("incident.resolved", {"pages": 1})
    cut = _bus(store, "INC-CUT")
    cut.emit("incident.opened", {"title": "Cut off", "mode": "live"})
    cut.emit("decision.made", {"decision": {"id": "D-1", "outcome": "ESCALATE", "proposal_ref": "P-1@1",
                                            "rule_applied": "deadlock"}})
    stopped = _bus(store, "INC-STOP")
    stopped.emit("incident.opened", {"title": "Stopped", "mode": "scripted"})
    stopped.emit("incident.ended", {"reason": "stopped"})

    assert {i["id"]: i["status"] for i in store.incidents()} == {
        "INC-DONE": "resolved", "INC-CUT": "running", "INC-STOP": "stopped"}

    # A restart reopens the same file: only the open incident gets closed, and only once.
    restarted = EventStore(str(tmp_path / "magi.sqlite"))
    assert restarted.mark_interrupted("server restarted") == ["INC-CUT"]
    assert restarted.mark_interrupted("server restarted") == []
    assert {i["id"]: i["status"] for i in restarted.incidents()}["INC-CUT"] == "interrupted"

    events = restarted.load("INC-CUT")
    assert [e["seq"] for e in events] == [1, 2, 3]
    assert events[-1]["type"] == "incident.ended" and events[-1]["sim_ts"] == 12.0
    record = build_record("INC-CUT", "Cut off", "n/a", events)
    assert "D-1 ESCALATE P-1@1: deadlock" in record
    assert record.endswith("incident interrupted: server restarted")
