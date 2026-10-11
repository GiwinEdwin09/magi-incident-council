import { useState } from "react";
import { useStore } from "../lib/store";
import type { AgentName } from "../lib/types";
import { simTime } from "../lib/types";
import { AGENT_META, AgentTag, RefChip, SectionTitle, Visibility, useHighlighted } from "./ui";

function EvidenceCard({ id }: { id: string }) {
  const item = useStore((s) => s.view.evidence[id]);
  const hl = useHighlighted(id);
  if (!item) return null;
  const { ev, assessments } = item;
  const isTool = ev.source.startsWith("tool:");
  const rumor = ev.source === "slack_rumor";
  const human = ev.source === "oncall_human";
  const rejected = Object.values(assessments).filter((a) => a && a.verdict !== "ACCEPT").length;
  return (
    <li className={`border-l-2 px-2 py-1.5 ${hl ? "bg-amber/15 border-amber" : rumor ? "border-alarm" : human ? "border-ink" : isTool ? "border-t1" : "border-line-strong"}`}>
      <div className="flex items-center gap-2 text-[12px]">
        <RefChip id={ev.id} />
        <span className={`font-mono ${rumor ? "text-alarm" : "text-dim"}`}>{ev.source}</span>
        <span className="font-mono text-dim">{simTime(ev.sim_ts)}</span>
        <span className="ml-auto"><Visibility visibleTo={ev.visible_to} /></span>
      </div>
      <p className={`mt-1 text-[13px] leading-snug ${ev.sealed ? "font-mono text-balthasar" : ""}`}>
        {ev.sealed ? `🔒 Sealed evidence (${ev.sealed_hash}). Only BALTHASAR and the incident commander can read it.` : ev.content}
      </p>
      {Object.keys(assessments).length > 0 && (
        <div className="mt-1 flex flex-wrap gap-2">
          {(Object.entries(assessments) as [AgentName, NonNullable<(typeof assessments)[AgentName]>][]).map(([a, as]) => (
            <span key={a} title={as.reason} className="flex items-center gap-1 font-mono text-[11px]">
              <span className={AGENT_META[a].text}>{AGENT_META[a].short}</span>
              <span className={as.verdict === "ACCEPT" ? "text-ok" : as.verdict === "REJECT" ? "text-alarm" : "text-balthasar"}>
                {as.verdict} {as.credibility.toFixed(2)}
              </span>
            </span>
          ))}
          {rejected >= 2 && <span className="bg-alarm px-1 font-mono text-[10px] text-white">REJECTED BY COUNCIL</span>}
        </div>
      )}
    </li>
  );
}

export function EvidencePanel() {
  const order = useStore((s) => s.view.evidenceOrder);
  const claims = useStore((s) => s.view.claims);
  const dp = useStore((s) => s.view.dp?.id);
  const [showTools, setShowTools] = useState(true);
  const evidence = useStore((s) => s.view.evidence);
  const list = [...order].reverse().filter((id) => showTools || !evidence[id]?.ev.source.startsWith("tool:"));
  const dpClaims = claims.filter((c) => !dp || c.decision_point === dp);

  return (
    <div className="frame flex min-h-0 flex-col">
      <SectionTitle right={
        <label className="flex items-center gap-1 text-[12px] text-dim">
          <input type="checkbox" checked={showTools} onChange={(e) => setShowTools(e.target.checked)} /> tool results
        </label>
      }>Evidence ({order.length})</SectionTitle>
      <p className="px-3 pt-1 text-[11px] text-dim">Colored letters show which agents can see each item. Agents only ever see their own.</p>
      <ul className="min-h-0 flex-1 space-y-1 overflow-y-auto p-2">
        {list.map((id) => <EvidenceCard key={id} id={id} />)}
        {list.length === 0 && <li className="p-2 text-dim">No evidence yet.</li>}
      </ul>
      <SectionTitle>Published claims ({dpClaims.length})</SectionTitle>
      <ul className="max-h-[32%] space-y-1 overflow-y-auto p-2">
        {dpClaims.map((c) => (
          <li key={c.id} className="text-[13px] leading-snug">
            <span className="font-mono text-[11px] text-dim">{c.id}</span> <AgentTag agent={c.author} />{" "}
            {c.text}
            <span className="ml-1 font-mono text-[11px] text-dim">conf {c.confidence.toFixed(2)}</span>
            {c.evidence_ids.map((e) => <RefChip key={e} id={e} />)}
            {c.sealed_ref && <span className="ml-1 font-mono text-[11px] text-balthasar">🔒 {c.sealed_ref}</span>}
          </li>
        ))}
        {dpClaims.length === 0 && <li className="text-dim">No claims yet.</li>}
      </ul>
    </div>
  );
}
