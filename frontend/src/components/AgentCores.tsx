import { useStore } from "../lib/store";
import type { AgentName } from "../lib/types";
import { AGENTS } from "../lib/types";
import { AGENT_META, RefChip, VoteLight } from "./ui";

const ACTIVE = new Set(["PROPOSE", "SCORE", "CRITIQUE", "DISSENT", "VOTE", "ASSESS"]);
const STATUS_TEXT: Record<string, string> = {
  PROPOSE: "Proposing",
  SCORE: "Scoring",
  CRITIQUE: "Critiquing",
  DISSENT: "Arguing against",
  VOTE: "Voting",
  ASSESS: "Assessing evidence",
  IDLE: "Waiting",
  ABSTAIN: "Failed: abstains",
};

function Core({ name }: { name: AgentName }) {
  const a = useStore((s) => s.view.agents[name]);
  const m = AGENT_META[name];
  const busy = ACTIVE.has(a.status);
  const vote = a.vote;
  const conformity = a.flags.includes("conformity_risk");

  return (
    <section className="frame flex min-w-0 flex-col" style={{ borderTop: `3px solid ${m.color}` }} aria-label={`${name} status`}>
      <div className="flex items-start justify-between gap-2 px-3 pt-2">
        <div>
          <div className={`display text-[22px] font-bold leading-none ${m.text}`}>{name}·{m.num}</div>
          <div className="text-[12px] text-dim">{m.role}</div>
        </div>
        <div className="text-right">
          <div className={`display text-[13px] font-semibold ${busy ? "text-amber" : a.status === "ABSTAIN" ? "text-alarm" : "text-dim"}`}>
            {busy && <span className="blink">■ </span>}
            {STATUS_TEXT[a.status] ?? a.status}
          </div>
          {a.error && <div className="font-mono text-[11px] text-alarm">{a.error}</div>}
        </div>
      </div>

      <div className="mt-2 grid grid-cols-[auto_1fr] items-center gap-x-3 gap-y-1 px-3 text-[13px]">
        <span className="text-dim">Prefers</span>
        <span className="flex items-center gap-1">
          {a.position ? <RefChip id={a.position.preferred_proposal_ref} /> : <span className="text-dim">—</span>}
          {a.position && <span className="font-mono text-[12px] text-dim">conf {a.position.confidence.toFixed(2)}</span>}
          {a.position?.changed && (
            <span className={`ml-1 px-1 font-mono text-[10px] ${conformity ? "bg-balthasar text-black" : "bg-ok text-black"}`}
              title={conformity ? "Changed position without a supported reason (possible conformity)" : "Changed position for a stated, supported reason"}>
              {conformity ? "⚠ CONFORMITY?" : `↻ ${a.position.change_cause}`}
            </span>
          )}
        </span>
        <span className="text-dim">Vote</span>
        <span className="flex items-center gap-2">
          <VoteLight choice={vote?.choice} />
          {vote && <span className="font-mono text-[11px] text-dim">on {vote.ballot}</span>}
        </span>
      </div>

      <div className="mt-2 flex-1 border-t border-line px-3 py-2 text-[13px] leading-snug">
        {vote ? (
          <>
            <p className="line-clamp-3" title={vote.reason}>{vote.reason}</p>
            {vote.blocking_objection && <p className="mt-1 text-alarm">Blocks: {vote.blocking_objection}</p>}
            {vote.would_change_if && <p className="mt-1 line-clamp-2 text-dim" title={vote.would_change_if}>Would change if: {vote.would_change_if}</p>}
          </>
        ) : a.assessment ? (
          <p className="line-clamp-4 text-dim" title={a.assessment}>{a.assessment}</p>
        ) : (
          <p className="text-dim">No assessment yet.</p>
        )}
      </div>
    </section>
  );
}

export function AgentCores() {
  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
      {AGENTS.map((a) => <Core key={a} name={a} />)}
    </div>
  );
}
