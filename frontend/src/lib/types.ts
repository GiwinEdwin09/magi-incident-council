export const AGENTS = ["MELCHIOR", "BALTHASAR", "CASPER"] as const;
export type AgentName = (typeof AGENTS)[number];
export type Tier = "T0" | "T1" | "T2";
export type VoteChoice = "ACCEPT" | "REJECT" | "ABSTAIN";

export type MagiEvent = {
  seq: number;
  id: string;
  incident_id: string;
  type: string;
  ts: string;
  sim_ts: number;
  agent?: AgentName | null;
  payload: Record<string, any>;
};

export type Param = { name: string; value: string };
export type ActionCall = { action_id: string; params: Param[] };

export type Evidence = {
  id: string;
  sim_ts: number;
  source: string;
  visible_to: string[];
  content: string;
  sealed: boolean;
  sealed_hash?: string | null;
  label?: string | null;
  requested_by?: string | null;
};

export type Assessment = {
  evidence_id: string;
  credibility: number;
  verdict: "ACCEPT" | "DOUBT" | "REJECT";
  reason: string;
  source_reliability: number;
};

export type Claim = {
  id: string;
  author: AgentName;
  text: string;
  evidence_ids: string[];
  confidence: number;
  sealed_ref?: string | null;
  decision_point: string;
};

export type ProposalDraft = {
  title: string;
  actions: ActionCall[];
  rationale: string;
  expected_outcome: string;
  risks: string[];
};

export type Proposal = {
  id: string;
  version: number;
  hash: string;
  author: AgentName;
  co_authors: string[];
  supersedes?: string | null;
  draft: ProposalDraft;
  tier: Tier;
  tier_reasons: string[];
  created_round: number;
  decision_point: string;
};

export type Position = {
  preferred_proposal_ref: string;
  confidence: number;
  changed: boolean;
  change_cause: string;
  cited_ids: string[];
};

export type Decision = {
  id: string;
  decision_point: string;
  round: number;
  proposal_ref?: string | null;
  tier?: Tier | null;
  outcome: "EXECUTE" | "CONFIRM" | "NEXT_ROUND" | "ESCALATE" | "INSUFFICIENT_INFO" | "HOLD";
  rule_applied: string;
  votes: Record<string, VoteChoice>;
  vetoes: string[];
  decider: "COUNCIL" | "HUMAN";
  ruled_by?: string | null;
  actions: ActionCall[];
  certificate?: string | null;
};

export type EscalationOption = {
  key: "A" | "B" | "C";
  proposal_ref: string;
  summary: string;
  supporters: AgentName[];
  main_risk: string;
  tier: Tier;
};

export type Dossier = {
  incident_id: string;
  decision_point: string;
  title: string;
  situation: string;
  crux: string;
  options: EscalationOption[];
  positions: Record<string, string>;
  sealed_available: string[];
  info_needed: string[];
  reason: string;
};

export type EvalRate = { mean: number | null; lo?: number | null; hi?: number | null; n: number };

export type EvalCondition = {
  name: string;
  runs: number;
  decision_points: number;
  harmful_rate: EvalRate;
  harmful_unchecked_rate: EvalRate;
  acceptable_rate: EvalRate;
  best_rate: EvalRate;
  escalation_accuracy: EvalRate;
  escalation_precision: number | null;
  escalation_recall: number | null;
  false_evidence_rejection: EvalRate;
  pages_per_dp: number | null;
  initial_disagreement: EvalRate;
  flips: Record<string, number>;
  tokens_per_dp: number;
  llm_calls_per_dp: number;
  wall_s_per_dp: number;
  errors: number;
};

export type EvalSummary = {
  run: string;
  config: { started?: string; models?: Record<string, string>; runs?: number };
  conditions: Record<string, EvalCondition>;
  hypotheses: { id: string; text: string; vs: string; council: number | null; baseline: number | null; verdict: string }[];
  decision_points: {
    scenario: string;
    decision_point: string;
    kind: string | null;
    should_escalate?: boolean;
    results: Record<string, { outcomes: string[]; harmful: number; best: number; escalated: number; runs: number; actions: string[] }>;
  }[];
};

export type IncidentSummary = {
  id: string;
  title: string;
  mode: string;
  opened_at: string;
  status: "running" | "resolved" | "stopped" | "interrupted" | string;
};

export type ScenarioInfo = {
  id: string;
  title: string;
  summary: string;
  kind?: "demo" | "postmortem" | "synthetic";
  based_on?: { name: string; url: string } | null;
  has_script?: boolean;
  injections: { id: string; label: string }[];
};

export type AppConfig = {
  mode: string;
  has_api_key: boolean;
  n8n: boolean;
  phone: boolean;
  oncall_name: string;
  models: Record<string, string>;
};

export const actionLabel = (a: ActionCall) =>
  `${a.action_id}(${a.params.map((p) => `${p.name}=${p.value}`).join(", ")})`;

export const simTime = (s: number) => {
  const m = Math.floor(s / 60);
  const sec = Math.floor(s % 60);
  return `T+${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;
};

export const pid = (ref: string) => ref.split("@")[0];
