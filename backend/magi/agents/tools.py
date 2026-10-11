"""Native tool definitions for each agent's data tools.

Only an agent's own tools are ever offered to it (need-to-know). Every call still runs through
Incident.run_tool, which enforces entitlement, routes through n8n, records the result as private
evidence, and emits events, exactly like structured tool_requests.
"""

from __future__ import annotations

from magi.sim.scenario import AGENT_TOOLS

# name -> (description, {param: description})
TOOL_SPECS: dict[str, tuple[str, dict[str, str]]] = {
    "get_metrics": ("Current latency, error rate and version for a service.", {"service": "Service name, e.g. payments-api", "window": "Time window, e.g. 15m"}),
    "get_recent_deploys": ("Recent deploys for a service.", {"service": "Service name"}),
    "get_runbook": ("The runbook for a service, including its assumptions.", {"service": "Service name"}),
    "get_dependencies": ("What a service depends on and what is a production dependency.", {"service": "Service name"}),
    "query_siem": ("Security events and traffic for a host or IP.", {"target": "Host or IP"}),
    "check_ip_allowlist": ("Whether an IP belongs to a sanctioned party (e.g. an active pentest).", {"ip": "IPv4 address"}),
    "get_process_list": ("Processes running on a host.", {"host": "Host name, e.g. db-7"}),
    "get_replication_state": ("Replication lag and catch-up rate for a database cluster.", {"cluster": "Cluster name, e.g. pay-db"}),
    "get_customer_impact": ("Customers and writes affected, and what a failover would discard.", {"service": "Service name"}),
    "get_contracts": ("Contract and SLA terms for a customer segment.", {"segment": "Customer segment, e.g. enterprise"}),
    "get_regulatory_obligations": ("Regulatory obligations for a data type in a region.", {"data_type": "e.g. personal data, cardholder data", "region": "e.g. eu"}),
    "get_status_page": ("Current public status page state.", {}),
}


def openai_tools(agent: str) -> list[dict]:
    """Responses API function tools (strict) for this agent only."""
    tools = []
    for name in sorted(AGENT_TOOLS.get(agent, set())):
        desc, params = TOOL_SPECS[name]
        tools.append({
            "type": "function",
            "name": name,
            "description": desc,
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {p: {"type": "string", "description": d} for p, d in params.items()},
                "required": list(params),
                "additionalProperties": False,
            },
        })
    return tools
