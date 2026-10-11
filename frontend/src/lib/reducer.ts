// The UI is a pure function of the event log: replaying the same events gives the same screen.
import type {
  AgentName,
  Assessment,
  Claim,
  Decision,
  Dossier,
  Evidence,
  MagiEvent,
  Position,
  Proposal,
  Tier,
  VoteChoice,
} from "./types";
import { AGENTS, actionLabel, pid } from "./types";

export type AgentView = {
  status: string;
  position?: Position;
  flags: string[];
  vote?: { ballot: string; choice: VoteChoice; reason: string; would_change_if: string; blocking_objection?: string | null };
  assessment?: string;
  confidence?: number;
  error?: string;
};

export type Tone = "info" | "ok" | "warn" | "alarm" | "human";

export type LogEntry = {
  seq: number;
  sim_ts: number;
  agent?: AgentName | null;
  kind: string;
  text: string;
  tone: Tone;
  refs: string[];
  dp?: string;
};

export type ProposalView = {
  versions: Proposal[];
  scores: Partial<Record<AgentName, { score: number; reason: string }>>;
  votes: Record<string, Partial<Record<AgentName, VoteChoice>>>; // by ballot ref
  dp: string;
};

export type View = {
  incidentId?: string;
  title: string;
  company: string;
  scenarioId?: string;
  mode: string;
  speed: number;
  paused: boolean;
  integrations: { n8n: boolean; phone: boolean };
  injections: { id: string; label: string }[];
  injected: string[];
  decisionPoints: { id: string; title?: string; question: string; at: number }[];
  simTs: number;
  evidence: Record<string, { ev: Evidence; reliability: number; assessments: Partial<Record<AgentName, Assessment>> }>;
  evidenceOrder: string[];
  claims: Claim[];
  proposals: Record<string, ProposalView>;
  proposalOrder: string[];
  leading?: string;
  leadingInfo?: { pareto_kept: string[]; dropped: string[]; schulze: { wins: Record<string, number> } };
  agents: Record<AgentName, AgentView>;
  log: LogEntry[];
  decisions: Decision[];
  dp?: { id: string; title?: string; question: string };
  round: number;
  confirm: { decision_id: string; proposal_ref: string; tier: Tier; via: string; timeout_s: number; at: number } | null;
  escalation: {
    dossier: Dossier;
    decision_id: string;
    call: string;
    callDetail?: string;
    activity: string[];
    reconvening: boolean;
  } | null;
  slack: { seq: number; text: string; kind: string; via: string; sim_ts: number }[];
  world?: Record<string, any>;
  resolved?: Record<string, any>;
  errors: string[];
};

const emptyAgent = (): AgentView => ({ status: "IDLE", flags: [] });

export const initialView = (): View => ({
  title: "",
  company: "",
  mode: "",
  speed: 1,
  paused: false,
  integrations: { n8n: false, phone: false },
  injections: [],
  injected: [],
  decisionPoints: [],
  simTs: 0,
  evidence: {},
  evidenceOrder: [],
  claims: [],
  proposals: {},
  proposalOrder: [],
  agents: { MELCHIOR: emptyAgent(), BALTHASAR: emptyAgent(), CASPER: emptyAgent() },
  log: [],
  decisions: [],
  round: 0,
  confirm: null,
  escalation: null,
  slack: [],
  errors: [],
});

const short = (s: string, n = 220) => (s.length > n ? s.slice(0, n - 1) + "…" : s);

export function reduce(v: View, e: MagiEvent): View {
  const p = e.payload;
  const agent = e.agent ?? undefined;
  const log = (kind: string, text: string, tone: Tone = "info", refs: string[] = []) => {
    v.log = [...v.log, { seq: e.seq, sim_ts: e.sim_ts, agent: e.agent, kind, text, tone, refs, dp: p.decision_point }];
  };
  const setAgent = (a: AgentName, patch: Partial<AgentView>) => {
    v.agents = { ...v.agents, [a]: { ...v.agents[a], ...patch } };
  };
  v = { ...v, simTs: Math.max(v.simTs, e.sim_ts) };

  switch (e.type) {
    case "incident.opened":
      v.incidentId = e.incident_id;
      v.title = p.title;
      v.company = p.company;
      v.scenarioId = p.scenario_id;
      v.mode = p.mode;
      v.speed = p.speed;
      v.integrations = p.integrations;
      v.injections = p.injections ?? [];
      v.decisionPoints = p.decision_points ?? [];
      v.world = p.world;
      log("incident", `Incident opened: ${p.title}`, "alarm");
      break;

    case "incident.control":
      v.speed = p.speed;
      v.paused = p.paused;
      break;

    case "evidence.released": {
      const ev: Evidence = p.evidence;
      v.evidence = { ...v.evidence, [ev.id]: { ev, reliability: p.reliability, assessments: {} } };
      v.evidenceOrder = [...v.evidenceOrder.filter((x) => x !== ev.id), ev.id];
      if (v.injections.some((i) => i.id === ev.id)) v.injected = [...v.injected, ev.id];
      if (ev.source === "oncall_human") log("human", `Human added: ${ev.content}`, "human", [ev.id]);
      else if (e.sim_ts > 1.5) log("evidence", `New evidence ${ev.id} from ${ev.source}`, ev.source === "slack_rumor" ? "warn" : "info", [ev.id]);
      break;
    }

    case "tool.requested":
      log("tool", `requests ${p.tool}(${Object.entries(p.params ?? {}).map(([k, val]) => `${k}=${val}`).join(", ")}): ${p.reason}`, "info");
      break;

    case "tool.result": {
      const ev: Evidence = p.evidence;
      v.evidence = { ...v.evidence, [ev.id]: { ev, reliability: 0.95, assessments: {} } };
      v.evidenceOrder = [...v.evidenceOrder, ev.id];
      log("tool", `${p.tool} → ${ev.id} via ${p.via}: ${short(ev.content, 160)}`, "info", [ev.id]);
      break;
    }

    case "tool.denied":
      log("tool", `tool ${p.tool} denied: ${p.reason}`, "warn");
      break;

    case "agent.status":
      if (agent) setAgent(agent, { status: p.status, error: p.status === "ABSTAIN" ? v.agents[agent].error : undefined });
      break;

    case "agent.error":
      if (agent) {
        setAgent(agent, { error: `${p.phase}: ${p.status}` });
        log("error", `${p.phase} failed (${p.status}); counted as ABSTAIN`, "warn");
      }
      break;

    case "council.started":
      v.dp = { id: p.decision_point, title: p.title, question: p.question };
      v.round = 0;
      v.leading = undefined;
      for (const a of AGENTS) setAgent(a, { position: undefined, vote: undefined, flags: [] });
      log("council", `Council convened on ${p.decision_point}: ${p.question}`, "info");
      break;

    case "assessment.posted":
      if (agent) setAgent(agent, { assessment: p.assessment, confidence: p.confidence });
      log("assess", p.assessment, "info");
      break;

    case "claim.published":
      v.claims = [...v.claims, p.claim];
      break;

    case "proposal.created":
    case "proposal.versioned": {
      const prop: Proposal = p.proposal;
      const cur = v.proposals[prop.id] ?? { versions: [], scores: {}, votes: {}, dp: prop.decision_point };
      v.proposals = { ...v.proposals, [prop.id]: { ...cur, versions: [...cur.versions, prop] } };
      if (!v.proposalOrder.includes(prop.id)) v.proposalOrder = [...v.proposalOrder, prop.id];
      if (e.type === "proposal.created")
        log("propose", `proposes ${p.ref} [${prop.tier}]: ${prop.draft.title} — ${prop.draft.actions.map(actionLabel).join("; ")}`, "info", [p.ref]);
      else
        log("amend", `amends ${p.supersedes} → ${p.ref} [${prop.tier}]: ${(p.diff ?? []).join("  ")}`, "info", [p.ref]);
      break;
    }

    case "proposal.merged": {
      const prop: Proposal = p.proposal;
      const cur = v.proposals[prop.id];
      if (cur) {
        const versions = cur.versions.map((x) => (x.version === prop.version ? { ...x, co_authors: prop.co_authors } : x));
        v.proposals = { ...v.proposals, [prop.id]: { ...cur, versions } };
      }
      log("propose", `independently proposed the same actions as ${p.ref}; merged as co-author`, "ok", [p.ref]);
      break;
    }

    case "proposal.scored":
      if (agent) {
        const next = { ...v.proposals };
        for (const s of p.scores ?? []) {
          const id = pid(s.proposal_ref);
          if (next[id]) next[id] = { ...next[id], scores: { ...next[id].scores, [agent]: { score: s.score, reason: s.reason } } };
        }
        v.proposals = next;
        log("score", `ranks ${(p.ranking ?? []).join(" > ")}`, "info");
      }
      break;

    case "proposal.leading":
      v.leading = p.ref;
      v.leadingInfo = { pareto_kept: p.pareto_kept, dropped: p.dropped, schulze: p.schulze };
      break;

    case "round.started":
      v.round = p.round;
      log("round", `Round ${p.round}${p.full ? "" : " (single proposal: straight to dissent and vote)"}`, "info");
      break;

    case "critique.posted": {
      const k = p.critique;
      const tone: Tone = k.severity === "blocking" ? "alarm" : k.kind === "challenge" ? "warn" : "info";
      const pol = k.cites_policy ? ` [policy ${k.cites_policy}]` : "";
      const label = k.kind === "challenge" ? `challenges claim ${k.target_ref}` : `${k.severity} objection to ${k.target_ref}${pol}`;
      log(k.kind, `${label}: ${k.text}${k.would_accept_if ? ` — would accept if: ${k.would_accept_if}` : ""}`, tone, [k.target_ref, k.id]);
      break;
    }

    case "dissent.posted":
      log("dissent", `DISSENT on ${p.critique.target_ref}: ${p.critique.text} Failure scenario: ${p.failure_scenario}`, "warn", [p.critique.target_ref]);
      break;

    case "position.updated":
      if (agent) {
        setAgent(agent, { position: p.position, flags: p.flags ?? [] });
        if (p.position.changed) {
          const flagged = (p.flags ?? []).includes("conformity_risk");
          log(
            "change",
            `changed position ${p.from ?? "—"} → ${p.position.preferred_proposal_ref} (cause: ${p.position.change_cause}${p.position.cited_ids?.length ? `, cites ${p.position.cited_ids.join(", ")}` : ""})${flagged ? " ⚠ possible conformity" : ""}`,
            flagged ? "warn" : "ok",
            p.position.cited_ids ?? [],
          );
        }
      }
      break;

    case "vote.cast":
      if (agent) {
        setAgent(agent, { vote: { ballot: p.ballot, choice: p.choice, reason: p.reason, would_change_if: p.would_change_if, blocking_objection: p.blocking_objection } });
        const id = pid(p.ballot);
        const cur = v.proposals[id];
        if (cur) {
          const votes = { ...cur.votes, [p.ballot]: { ...(cur.votes[p.ballot] ?? {}), [agent]: p.choice } };
          v.proposals = { ...v.proposals, [id]: { ...cur, votes } };
        }
        log("vote", `${p.choice} on ${p.ballot}: ${p.reason}`, p.choice === "ACCEPT" ? "ok" : p.choice === "REJECT" ? "alarm" : "warn", [p.ballot]);
      }
      break;

    case "evidence.assessed": {
      const a: Assessment = p.assessment;
      const cur = v.evidence[a.evidence_id];
      if (cur && agent) v.evidence = { ...v.evidence, [a.evidence_id]: { ...cur, assessments: { ...cur.assessments, [agent]: a } } };
      log("assess", `rates ${a.evidence_id} ${a.verdict} (credibility ${a.credibility.toFixed(2)}): ${a.reason}`, a.verdict === "ACCEPT" ? "info" : "warn", [a.evidence_id]);
      break;
    }

    case "council.interrupted":
      log("interrupt", `New evidence ${p.evidence_id}: every agent who can see it must assess it before continuing`, "warn", [p.evidence_id]);
      break;

    case "decision.made": {
      const d: Decision = p.decision;
      v.decisions = [...v.decisions, d];
      const tone: Tone = d.outcome === "EXECUTE" ? "ok" : d.outcome === "ESCALATE" ? "alarm" : d.decider === "HUMAN" ? "human" : "warn";
      log("decision", `${d.id} ${d.outcome}${d.proposal_ref ? ` ${d.proposal_ref}` : ""} — ${d.rule_applied}`, tone, d.proposal_ref ? [d.proposal_ref] : []);
      break;
    }

    case "action.executing":
      log("execute", `Executing via ${p.via}: ${p.actions.join("; ") || "no infrastructure actions"}`, "ok");
      break;

    case "action.result":
      log("execute", `✓ ${p.action}${p.changes?.length ? ` → ${p.changes.join(", ")}` : ""}`, "ok");
      break;

    case "action.rejected":
      log("execute", `Rejected action: ${p.reason}`, "alarm");
      break;

    case "confirm.requested":
      v.confirm = { decision_id: p.decision_id, proposal_ref: p.proposal_ref, tier: p.tier, via: p.via, timeout_s: p.timeout_s, at: Date.now() };
      log("confirm", `All three agents accept irreversible ${p.proposal_ref}. Waiting for a human tap (${p.via === "n8n" ? "Slack" : "this screen"}).`, "warn", [p.proposal_ref]);
      break;

    case "confirm.result":
      v.confirm = null;
      log("confirm", `${p.approved ? "Approved" : "Denied"} by ${p.by}`, p.approved ? "ok" : "alarm");
      break;

    case "escalation.started":
      v.escalation = { dossier: p.dossier, decision_id: p.decision_id, call: "starting", activity: [], reconvening: false };
      log("escalate", `ESCALATED to a human. Crux: ${p.dossier.crux}`, "alarm");
      break;

    case "escalation.updated":
      if (v.escalation) v.escalation = { ...v.escalation, dossier: p.dossier, reconvening: false };
      log("escalate", `Still deadlocked after new information. Updated crux: ${p.dossier.crux}`, "alarm");
      break;

    case "escalation.reconvening":
      if (v.escalation) v.escalation = { ...v.escalation, reconvening: true };
      log("council", "Human added information: the council re-deliberates", "human");
      break;

    case "escalation.resolved":
      v.escalation = null;
      log("council", "The council resolved the deadlock with the new information", "ok");
      break;

    case "call.status":
      if (v.escalation) v.escalation = { ...v.escalation, call: p.status, callDetail: p.detail };
      if (p.status !== "no_phone") log("call", `Call ${p.status}${p.detail ? `: ${p.detail}` : ""}`, "human");
      break;

    case "call.tool":
      if (v.escalation) v.escalation = { ...v.escalation, activity: [...v.escalation.activity, JSON.stringify(p.request)] };
      break;

    case "evidence.unsealed":
      log("human", `${p.evidence_id} unsealed by the incident commander`, "human", [p.evidence_id]);
      break;

    case "human.ruling":
      v.escalation = null;
      log("human", `RULING by ${p.ruling.ruled_by} via ${p.ruling.via}: option ${p.ruling.option_key}${p.ruling.conditions ? ` — condition: ${p.ruling.conditions}` : ""}`, "human", p.proposal_ref ? [p.proposal_ref] : []);
      break;

    case "slack.message":
      v.slack = [...v.slack, { seq: e.seq, text: p.text, kind: p.kind, via: p.via, sim_ts: e.sim_ts }];
      break;

    case "metrics.tick":
      v.world = p;
      break;

    case "council.error":
      v.errors = [...v.errors, p.error];
      log("error", `Council error: ${p.error}`, "alarm");
      break;

    case "incident.resolved":
      v.resolved = p;
      log("incident", `Incident resolved. Pages: ${p.pages}, LLM calls: ${p.llm_calls}, est. cost $${p.cost_usd}`, "ok");
      break;
  }
  return v;
}
