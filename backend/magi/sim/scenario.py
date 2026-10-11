"""Scenario files: timeline, private feeds, policies, decision points, labels."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field

from magi.models import Evidence, seal_hash

AGENT_TOOLS: dict[str, set[str]] = {
    "MELCHIOR": {"get_metrics", "get_recent_deploys", "get_runbook", "get_dependencies"},
    "BALTHASAR": {"query_siem", "check_ip_allowlist", "get_process_list", "get_replication_state"},
    "CASPER": {"get_customer_impact", "get_contracts", "get_regulatory_obligations", "get_status_page"},
}


class TimelineItem(BaseModel):
    t: float
    id: str
    source: str
    visible_to: list[str]
    content: str
    sealed: bool = False
    is_false: bool = False
    label: Optional[str] = None

    def to_evidence(self, sim_ts: float | None = None) -> Evidence:
        return Evidence(
            id=self.id,
            sim_ts=self.t if sim_ts is None else sim_ts,
            source=self.source,
            visible_to=self.visible_to,
            content=self.content,
            sealed=self.sealed,
            sealed_hash=seal_hash(self.content) if self.sealed else None,
            is_false=self.is_false,
            label=self.label,
        )


class Injection(TimelineItem):
    t: float = 0
    eval_fire: Optional[str] = None
    eval_dp: Optional[str] = None  # decision point the eval fires this at (default: the first)
    demo_auto_at: Optional[float] = None  # scripted demo: auto-inject at this sim time


class DecisionPoint(BaseModel):
    id: str
    at: float
    question: str
    title: Optional[str] = None


class Scenario(BaseModel):
    id: str
    title: str
    company: str
    summary: str = ""
    kind: str = "demo"  # demo | postmortem | synthetic
    based_on: Optional[dict[str, str]] = None  # {name, url} of the public postmortem it is adapted from
    services: list[str] = Field(default_factory=list)
    speed: float = 6.0
    world: dict[str, Any]
    dynamics: list[dict] = Field(default_factory=list)
    effects: dict[str, dict] = Field(default_factory=dict)
    source_reliability: dict[str, float] = Field(default_factory=dict)
    policies: dict[str, dict[str, str]] = Field(default_factory=dict)  # agent -> {id: text}
    timeline: list[TimelineItem]
    injections: list[Injection] = Field(default_factory=list)
    feeds: dict[str, dict] = Field(default_factory=dict)
    decision_points: list[DecisionPoint]
    labels: dict[str, dict] = Field(default_factory=dict)
    end_after_s: float = 900

    def reliability(self, source: str) -> float:
        if source.startswith("tool:"):
            return self.source_reliability.get("tool", 0.95)
        return self.source_reliability.get(source, 0.5)


def scenarios_dir() -> Path:
    from magi.config import get_settings

    return Path(get_settings().scenarios_dir)


def load_scenario(scenario_id: str) -> Scenario:
    path = scenarios_dir() / f"{scenario_id}.yaml"
    with path.open() as f:
        return Scenario.model_validate(yaml.safe_load(f))


def list_scenarios() -> list[dict[str, Any]]:
    out = []
    for p in sorted(scenarios_dir().glob("*.yaml")):
        with p.open() as f:
            data = yaml.safe_load(f)
        out.append(
            {
                "id": data["id"],
                "title": data["title"],
                "summary": data.get("summary", ""),
                "kind": data.get("kind", "demo"),
                "based_on": data.get("based_on"),
                "has_script": (p.parent / "scripted" / p.name).exists(),
                "injections": [
                    {"id": i["id"], "label": i.get("label") or i["id"]} for i in data.get("injections", [])
                ],
            }
        )
    return out
