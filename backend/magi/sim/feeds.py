"""Tool data at the current sim time. In production n8n would route these to Datadog, Splunk, CRM."""

from __future__ import annotations

from typing import Any

from magi.sim.scenario import AGENT_TOOLS, Scenario
from magi.sim.world import render_template


class ToolNotPermitted(Exception):
    pass


def tool_result(scenario: Scenario, state: dict[str, Any], agent: str, tool: str, params: dict[str, str]) -> str:
    if tool not in AGENT_TOOLS.get(agent, set()):
        raise ToolNotPermitted(f"{agent} is not entitled to {tool}")
    feed = scenario.feeds.get(tool)
    if feed is None:
        return f"{tool}: no data available for this incident."
    text = feed.get("default", f"{tool}: no matching record.")
    by = feed.get("by_param")
    if by:
        key = params.get(by, "")
        text = (feed.get("values") or {}).get(key, text)
    return render_template(str(text), state)
