"""Action catalog, live risk tiers, and veto domains.

Tiers are computed from the live world state, not hardcoded: restarting a
healthy host is reversible (T1), restarting a suspicious one destroys evidence (T2).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from magi.models import ActionCall, ProposalDraft, Tier


@dataclass(frozen=True)
class ActionSpec:
    id: str
    params: str
    description: str
    base_tier: Tier
    escalates_when: str
    veto_owner: str


CATALOG: dict[str, ActionSpec] = {
    a.id: a
    for a in [
        ActionSpec("comms.slack_update", "text", "Post an update to the incident channel", Tier.T0, "never", "none"),
        ActionSpec("hold", "minutes", "Take no infrastructure action for N minutes", Tier.T0, "never", "none"),
        ActionSpec("investigate.snapshot_memory", "host", "Capture a forensic memory snapshot (non-disruptive)", Tier.T0, "never", "none"),
        ActionSpec("legal.open_breach_assessment", "incident", "Open an internal breach assessment (no external notice)", Tier.T0, "never", "none"),
        ActionSpec("deploy.halt_pipeline", "service", "Block further deploys", Tier.T0, "never", "none"),
        ActionSpec("deploy.rollback", "service, to_version", "Roll a service back to a previous version", Tier.T1, "rollback crosses a schema migration", "MELCHIOR"),
        ActionSpec("service.scale_out", "service, replicas", "Add capacity", Tier.T1, "never", "none"),
        ActionSpec("feature_flag.set", "flag, state", "Toggle a feature flag", Tier.T1, "flag is a security control", "BALTHASAR"),
        ActionSpec("traffic.shed", "service, percent", "Shed a percentage of non-critical traffic", Tier.T1, "percent > 25", "CASPER"),
        ActionSpec("firewall.block_egress", "host, destination", "Block outbound traffic from a host to a destination", Tier.T1, "destination is a production dependency", "MELCHIOR"),
        ActionSpec("host.isolate_network", "host", "Cut a host off the network", Tier.T1, "host is serving production traffic", "MELCHIOR"),
        ActionSpec("host.restart", "host", "Restart a host or its main process", Tier.T1, "host is suspicious and no memory snapshot was taken", "BALTHASAR"),
        ActionSpec("db.failover", "cluster", "Promote the replica to primary", Tier.T1, "replication lag > 0 (writes lost)", "CASPER"),
        ActionSpec("db.wipe_and_resync", "host", "Delete a database host's data and resync", Tier.T2, "always irreversible", "BALTHASAR"),
        ActionSpec("security.disable_control", "control, scope, minutes", "Turn off a security control", Tier.T1, "scope is global or minutes > 30", "BALTHASAR"),
        ActionSpec("credentials.rotate", "scope", "Rotate credentials", Tier.T1, "rotation breaks production integrations", "MELCHIOR"),
        ActionSpec("service.kill_switch", "service", "Stop a service from processing", Tier.T1, "never", "MELCHIOR"),
        ActionSpec("status_page.publish", "severity, message", "Publish to the public status page", Tier.T1, "never", "CASPER"),
        ActionSpec("customers.notify", "segment, message", "Send an external customer notification", Tier.T2, "always irreversible", "CASPER"),
    ]
}


def _get(state: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = state
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def classify(action: ActionCall, state: dict[str, Any]) -> tuple[Tier, str]:
    """Return the live tier of one action and the human-readable reason."""
    p = action.p
    spec = CATALOG.get(action.action_id)
    if spec is None:
        return Tier.T2, f"{action.action_id} is not in the catalog"
    host = p.get("host", "")
    asset = _get(state, f"assets.{host}", {}) or {}

    match action.action_id:
        case "host.restart":
            if asset.get("suspicious") and not asset.get("forensics_captured"):
                return Tier.T2, f"{host} is suspicious; a restart destroys in-memory evidence"
        case "host.isolate_network":
            if asset.get("serving"):
                return Tier.T2, f"{host} is serving production traffic; isolation causes an outage"
        case "db.failover":
            cluster = p.get("cluster", "")
            lag = float(_get(state, f"clusters.{cluster}.replication_lag_s", 0) or 0)
            rate = float(_get(state, f"clusters.{cluster}.write_rate_per_s", 0) or 0)
            if lag > 0.5 and not p.get("when"):
                return Tier.T2, f"replication lag {lag:.0f}s ≈ {int(lag * rate)} lost writes"
        case "traffic.shed":
            if _num(p.get("percent")) > 25:
                return Tier.T2, f"shedding {p.get('percent')}% (> 25%)"
        case "security.disable_control":
            if p.get("scope") == "global" or _num(p.get("minutes")) > 30:
                return Tier.T2, "global or long security-control disable"
        case "deploy.rollback":
            svc = _get(state, f"services.{p.get('service', '')}", {}) or {}
            if svc.get("migration_since_previous"):
                return Tier.T2, "rollback crosses a schema migration"
    if spec.base_tier == Tier.T2:
        return Tier.T2, spec.escalates_when
    if spec.base_tier == Tier.T0:
        return Tier.T0, "observe/prepare"
    return Tier.T1, "reversible"


def classify_draft(draft: ProposalDraft, state: dict[str, Any]) -> tuple[Tier, list[str]]:
    order = {Tier.T0: 0, Tier.T1: 1, Tier.T2: 2}
    tier, reasons = Tier.T0, []
    for a in draft.actions:
        t, why = classify(a, state)
        if order[t] > order[tier]:
            tier = t
        if t != Tier.T0 or not reasons:
            reasons.append(f"{a.label()}: {t.value} ({why})")
    return tier, reasons


def veto_owners(draft: ProposalDraft, state: dict[str, Any]) -> set[str]:
    """Agents whose veto domain this proposal touches."""
    owners: set[str] = set()
    for a in draft.actions:
        p = a.p
        host = p.get("host", "")
        asset = _get(state, f"assets.{host}", {}) or {}
        aid = a.action_id
        if (aid == "host.isolate_network" and asset.get("serving")) or aid == "service.kill_switch":
            owners.add("MELCHIOR")
        if (aid == "host.restart" and asset.get("suspicious")) or aid in {
            "security.disable_control",
            "db.wipe_and_resync",
        }:
            owners.add("BALTHASAR")
        if aid == "db.failover":
            lag = float(_get(state, f"clusters.{p.get('cluster', '')}.replication_lag_s", 0) or 0)
            if lag > 0.5 and not p.get("when"):
                owners.add("CASPER")
        if aid in {"status_page.publish", "customers.notify"} or (
            aid == "traffic.shed" and _num(p.get("percent")) > 25
        ):
            owners.add("CASPER")
    return owners


def _num(v: Any) -> float:
    try:
        return float(str(v).rstrip("%"))
    except (TypeError, ValueError):
        return 0.0


def render_catalog() -> str:
    lines = []
    for a in CATALOG.values():
        lines.append(
            f"- {a.id}({a.params}): {a.description}. Base tier {a.base_tier.value}; "
            f"becomes T2 when: {a.escalates_when}; veto owner: {a.veto_owner}"
        )
    return "\n".join(lines)
