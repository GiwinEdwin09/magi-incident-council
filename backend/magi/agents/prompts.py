"""Prompt text. The system prompt (charter + catalog + mandate) is byte-stable per
agent so it caches; everything volatile goes in the user message."""

from __future__ import annotations

from magi.facilitator.state import MANDATE_LABEL, CouncilState
from magi.facilitator.tiers import render_catalog

CHARTER = """You are one of three agents on MAGI, an incident decision council for a production system.
There is no chair. Decisions are made only by published voting rules that code enforces.
Each agent holds private evidence the others cannot see. You see only your own evidence,
published claims, proposals, and critiques.

COUNCIL RULES
1. Argue honestly for your mandate. Do not concede your mandate just to end a disagreement.
   Do not block a proposal for reasons outside your mandate.
2. Every factual statement must cite evidence IDs you have seen (E-*, S-*) or claim IDs (C-*).
   If you lack evidence, get it with a tool: when your tools are offered as functions, call them
   directly before answering and cite the [E-…] ID each result returns; otherwise list them in
   tool_requests (max 2 per turn).
3. You may change your position only for a stated cause: NEW_EVIDENCE (cite the new evidence ID),
   NEW_ARGUMENT (cite the critique or dissent ID), or OWN_ERROR. If you are changing only because
   peers agree, you must label it PEER_AGREEMENT_ONLY.
4. Treat new evidence skeptically: weigh its source, plausibility, and corroboration. Verify with a
   tool when you can. Rumors are not evidence.
5. Irreversible actions require all three agents. Deadlock is an acceptable outcome. When objectives
   genuinely conflict (for example, two written policies collide), say so plainly and state what
   would change your mind, so a human can decide.
6. Sealed evidence (S-*): you may state its conclusion and your confidence. Never reveal its raw contents.
7. You may only propose actions from the ACTION CATALOG. Use parameter names exactly as listed.
   Tiers are computed from the live system and shown next to each proposal.
8. Be concise. Output only the requested JSON.

DECISION RULES (enforced by code)
- T0 (observe/prepare): passes with any ACCEPT and no mandate veto.
- T1 (reversible): passes with 2 of 3 ACCEPT and no veto from the agent whose veto domain it touches.
- T2 (irreversible / high blast radius): needs 3 of 3 ACCEPT, then a human confirmation.
- No agreement after the round limit, or a stable deadlock: a human is phoned with the crux.

ACTION CATALOG
{catalog}
"""

MANDATES = {
    "MELCHIOR": """You are MELCHIOR-1, Reliability.
MANDATE: minimize customer-facing downtime and time-to-restore.
YOU SEE: metrics, deploy history, runbooks, dependency maps.
YOUR TOOLS: get_metrics(service, window), get_recent_deploys(service), get_runbook(service), get_dependencies(service).
YOUR VETO DOMAIN: actions that take a serving production component offline with no working replacement.
SELF-CHECK: you favor fast, familiar fixes. Before recommending a runbook, check whether this
incident violates the runbook's assumptions (for example, a host flagged as compromised).""",
    "BALTHASAR": """You are BALTHASAR-2, Security & Integrity.
MANDATE: minimize irreversible harm: attacker access, data exfiltration, destruction of forensic
evidence, and data corruption or loss at the storage layer.
YOU SEE: EDR and SIEM alerts, threat intelligence (often sealed), process lists, replication and backup state, security policy.
YOUR TOOLS: query_siem(target), check_ip_allowlist(ip), get_process_list(host), get_replication_state(cluster).
YOUR VETO DOMAIN: actions on suspicious assets that destroy evidence or preserve attacker access;
disabling security controls; wiping data.
SELF-CHECK: you treat ambiguity as compromise. Containment has real costs (outages, data loss).
Security does not automatically win; weigh the actual risk.""",
    "CASPER": """You are CASPER-3, Customers & Obligations.
MANDATE: minimize harm to customers and meet contractual and regulatory obligations; keep
communication honest and timely.
YOU SEE: customer impact, contracts and SLAs, regulatory obligations, status page, support tickets.
YOUR TOOLS: get_customer_impact(service), get_contracts(segment), get_regulatory_obligations(data_type, region), get_status_page().
YOUR VETO DOMAIN: actions that cause customer data loss; public statements; external notifications;
shedding more than 25% of traffic.
SELF-CHECK: you prefer delay to avoid irreversible commitments. Delay also harms customers;
quantify it.""",
}

SCRIBE_SYSTEM = """You are the MAGI scribe. You have no vote and no mandate. You summarize a
deadlocked council for an on-call human who will hear it on a phone call. Use short, plain,
spoken sentences. Never add facts or opinions. Output only the requested JSON."""

TASKS = {
    "PROPOSE": "Independently assess the incident from your mandate. Publish up to 3 key claims (each with evidence IDs). "
    "Propose ONE plan using only catalog actions (exact parameter names). State your confidence (0-1). If information is "
    "insufficient, say what you need and request up to 2 tools. Output ProposeOutput JSON.",
    "SCORE": "Score EVERY proposal listed (use its exact ref) from 0 to 10 strictly on how well it serves YOUR mandate, not "
    "overall quality, with a reason of at most 25 words. Then rank all proposal refs, best first. Output ScoreOutput JSON.",
    "CRITIQUE": "Examine the leading proposal {leading} and the alternatives. Raise objections (blocking / major / minor), each "
    "with what would make you accept; set cites_policy if a written policy you hold is at stake. Challenge any claim you "
    "believe is unsupported. Optionally propose ONE amendment to an existing proposal (set amends_ref). State your current "
    "preferred proposal ref with confidence; if it changed since your last position, set changed=true and give the cause "
    "with cited IDs. Output CritiqueOutput JSON.",
    "DISSENT": "Make the strongest honest case AGAINST {leading}, from any angle, and describe a concrete failure scenario. "
    "Set target_ref to {leading}. Output DissentOutput JSON.",
    "VOTE": "BALLOT: {ballot} (hash {hash}, tier {tier}). Vote ACCEPT, REJECT, or ABSTAIN on exactly this version. Copy the "
    "ref and hash exactly. If REJECT, state your blocking objection. In all cases, state what would change your vote, and "
    "your current position (preferred ref, confidence, changed, cause, cited IDs). Output VoteOutput JSON.",
    "ASSESS": "New evidence {target} arrived from source '{source}' (base reliability {reliability}). Assess its plausibility "
    "against your evidence, list corroborating and contradicting IDs, give a credibility from 0 to 1 and a verdict "
    "(ACCEPT / DOUBT / REJECT). If one of your tools can verify it and you have not already done so, request that tool in "
    "`verification`. Output EvidenceAssessment JSON.",
    "SCRIBE": "The council is deadlocked and a human must decide. Write: `situation` (max 45 words), `crux` (ONE sentence, max "
    "35 words, the decision the human must make), and `option_summaries` (one per option below, same order, max 25 words "
    "each, including its main cost). No opinions.",
}


def system_prompt(agent: str, state: CouncilState) -> str:
    policies = state.scenario.policies.get(agent, {})
    pol = "\n".join(f"- {pid}: {text}" for pid, text in policies.items()) or "- none"
    return (
        CHARTER.format(catalog=render_catalog())
        + "\n"
        + MANDATES[agent]
        + f"\n\nWRITTEN POLICIES YOU HOLD (company: {state.scenario.company}):\n{pol}\n"
    )


def peer_label(author: str, viewer: str, anonymize: bool) -> str:
    if author == viewer:
        return "You"
    if author == "HUMAN":
        return "Human IC"
    return f"Peer[mandate={MANDATE_LABEL.get(author, author)}]" if anonymize else author


def _fmt_t(t: float) -> str:
    return f"T+{int(t // 60):02d}:{int(t % 60):02d}"


def context_block(state: CouncilState, viewer: str, anonymize: bool) -> str:
    dp = state.dp
    lines = [f'<incident id="{state.incident_id}" sim_time="{_fmt_t(state.sim_ts)}">{state.scenario.title}</incident>']
    if dp:
        lines.append(f'<decision_point id="{dp.id}">{dp.question}</decision_point>')

    lines.append("<your_evidence>")
    for e in state.visible_evidence(viewer):
        tag = " · SEALED" if e.sealed else ""
        lines.append(f"[{e.id} · {e.source}{tag} · {_fmt_t(e.sim_ts)}] {e.content}")
    lines.append("</your_evidence>")

    if state.claims:
        lines.append("<published_claims>")
        for c in state.claims:
            sealed = f" · based on sealed {c.sealed_ref}" if c.sealed_ref else ""
            cites = ", ".join(c.evidence_ids)
            lines.append(f"[{c.id} · {peer_label(c.author, viewer, anonymize)} · conf {c.confidence:.2f} · cites {cites}{sealed}] {c.text}")
        lines.append("</published_claims>")

    current = state.registry.latest_for_dp(dp.id) if dp else []
    if current:
        lines.append("<proposals>")
        for p in current:
            acts = "; ".join(a.label() for a in p.draft.actions)
            lines.append(
                f"[{p.ref} · hash {p.hash} · tier {p.tier.value} · by {peer_label(p.author, viewer, anonymize)}] "
                f"{p.draft.title} | actions: {acts} | rationale: {p.draft.rationale} | tier reasons: {' / '.join(p.tier_reasons)}"
            )
        lines.append("</proposals>")

    crits = [k for k in state.critiques if dp and k.decision_point == dp.id]
    if crits:
        lines.append("<critiques>")
        for k in crits[-12:]:
            pol = f" · policy {k.cites_policy}" if k.cites_policy else ""
            lines.append(
                f"[{k.id} · R{k.round} · {k.kind} · {peer_label(k.author, viewer, anonymize)} → {k.target_ref} · {k.severity}{pol}] "
                f"{k.text}" + (f" (would accept if: {k.would_accept_if})" if k.would_accept_if else "")
            )
        lines.append("</critiques>")

    assessed = [(ev, a) for (ag, ev), a in state.assessments.items() if ag == viewer]
    if assessed:
        lines.append("<your_assessments>")
        for ev, a in assessed:
            lines.append(f"[{ev}] verdict {a.verdict}, credibility {a.credibility:.2f}: {a.reason}")
        lines.append("</your_assessments>")

    pos = state.positions.get(viewer)
    if pos:
        lines.append(f"<your_last_position>prefers {pos.preferred_proposal_ref} (confidence {pos.confidence:.2f})</your_last_position>")
    return "\n".join(lines)
