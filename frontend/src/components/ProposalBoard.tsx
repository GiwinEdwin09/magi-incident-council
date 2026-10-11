import { useState } from "react";
import { useStore } from "../lib/store";
import type { AgentName, Proposal } from "../lib/types";
import { AGENTS, actionLabel } from "../lib/types";
import { AGENT_META, AgentTag, RefChip, SectionTitle, TierBadge, VoteLight, useHighlighted } from "./ui";

function ScoreBar({ agent, score }: { agent: AgentName; score?: number }) {
  const m = AGENT_META[agent];
  return (
    <div className="flex items-center gap-1.5" title={`${agent}'s score on its own mandate`}>
      <span className={`w-3 font-mono text-[11px] font-bold ${m.text}`}>{m.short}</span>
      <div className="h-2 w-20 bg-panel-2">
        <div className="h-2" style={{ width: `${(score ?? 0) * 10}%`, background: m.color }} />
      </div>
      <span className="w-4 font-mono text-[11px] text-dim">{score ?? "–"}</span>
    </div>
  );
}

function ProposalCard({ id }: { id: string }) {
  const pv = useStore((s) => s.view.proposals[id]);
  const leading = useStore((s) => s.view.leading);
  const positions = useStore((s) => s.view.agents);
  const hl = useHighlighted(id);
  const [showHistory, setShowHistory] = useState(false);
  if (!pv) return null;
  const latest: Proposal = pv.versions[pv.versions.length - 1];
  const ref = `${latest.id}@${latest.version}`;
  const isLeading = leading?.split("@")[0] === id;
  const supporters = AGENTS.filter((a) => positions[a].position?.preferred_proposal_ref.split("@")[0] === id);
  const ballots = Object.entries(pv.votes);

  return (
    <li className={`border px-2.5 py-2 ${isLeading ? "border-amber" : hl ? "border-amber/60" : "border-line"} ${hl ? "bg-amber/10" : "bg-panel"}`}>
      <div className="flex flex-wrap items-center gap-2">
        <RefChip id={ref} />
        <TierBadge tier={latest.tier} reasons={latest.tier_reasons} />
        {isLeading && <span className="display bg-amber px-1.5 text-[11px] font-bold text-black">ON BALLOT</span>}
        <span className="ml-auto text-[12px] text-dim">
          by <AgentTag agent={latest.author} />{latest.co_authors.length > 0 && <> + {latest.co_authors.map((c) => <AgentTag key={c} agent={c} />)}</>}
        </span>
      </div>
      <div className="mt-1 font-semibold leading-snug">{latest.draft.title}</div>
      <ul className="mt-1 font-mono text-[12px] text-dim">
        {latest.draft.actions.map((a, i) => <li key={i}>→ {actionLabel(a)}</li>)}
      </ul>
      {latest.draft.rationale && <p className="mt-1 text-[13px] leading-snug">{latest.draft.rationale}</p>}
      <p className="mt-1 text-[12px] text-dim" title={latest.tier_reasons.join("\n")}>Why {latest.tier}: {latest.tier_reasons.filter((r) => !r.includes("T0")).join(" · ") || latest.tier_reasons[0]}</p>

      <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
        <div className="space-y-0.5">{AGENTS.map((a) => <ScoreBar key={a} agent={a} score={pv.scores[a]?.score} />)}</div>
        <div className="text-right text-[12px]">
          <div className="text-dim">Preferred by</div>
          <div className="flex justify-end gap-1">{supporters.length ? supporters.map((a) => <AgentTag key={a} agent={a} />) : <span className="text-dim">none</span>}</div>
        </div>
      </div>

      {ballots.length > 0 && (
        <div className="mt-2 space-y-1 border-t border-line pt-1">
          {ballots.map(([b, votes]) => (
            <div key={b} className="flex flex-wrap items-center gap-2 text-[12px]">
              <span className="font-mono text-dim">vote on {b}</span>
              {AGENTS.map((a) => <span key={a} className="flex items-center gap-1"><span className={`font-mono text-[11px] ${AGENT_META[a].text}`}>{AGENT_META[a].short}</span><VoteLight choice={votes[a]} size="sm" /></span>)}
            </div>
          ))}
        </div>
      )}

      {pv.versions.length > 1 && (
        <button onClick={() => setShowHistory(!showHistory)} className="mt-1 text-[12px] text-amber underline">
          {showHistory ? "Hide" : "Show"} {pv.versions.length - 1} earlier version{pv.versions.length > 2 ? "s" : ""}
        </button>
      )}
      {showHistory && (
        <ol className="mt-1 space-y-1">
          {pv.versions.slice(0, -1).reverse().map((ver) => (
            <li key={ver.version} className="border-l border-line-strong pl-2 text-[12px] text-dim">
              <span className="font-mono">{ver.id}@{ver.version}</span> {ver.draft.title} by {ver.author}: {ver.draft.actions.map(actionLabel).join("; ")}
            </li>
          ))}
        </ol>
      )}
    </li>
  );
}

export function ProposalBoard() {
  const order = useStore((s) => s.view.proposalOrder);
  const proposals = useStore((s) => s.view.proposals);
  const dp = useStore((s) => s.view.dp?.id);
  const [showOld, setShowOld] = useState(false);
  const current = order.filter((id) => proposals[id]?.dp === dp);
  const older = order.filter((id) => proposals[id]?.dp !== dp);

  return (
    <div className="frame flex min-h-0 flex-col">
      <SectionTitle right={<span className="text-[12px] text-dim">bars = each agent's score on its own mandate</span>}>
        Proposals{dp ? ` · ${dp}` : ""}
      </SectionTitle>
      <ul className="min-h-0 flex-1 space-y-2 overflow-y-auto p-2">
        {current.map((id) => <ProposalCard key={id} id={id} />)}
        {current.length === 0 && <li className="p-2 text-dim">No proposals yet. Agents propose independently before seeing each other's plans.</li>}
        {older.length > 0 && (
          <li>
            <button onClick={() => setShowOld(!showOld)} className="text-[12px] text-amber underline">
              {showOld ? "Hide" : "Show"} {older.length} proposal{older.length > 1 ? "s" : ""} from earlier decision points
            </button>
          </li>
        )}
        {showOld && older.map((id) => <ProposalCard key={id} id={id} />)}
      </ul>
    </div>
  );
}
