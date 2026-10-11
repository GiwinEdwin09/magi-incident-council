import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { useStore } from "../lib/store";
import { actionLabel } from "../lib/types";
import { AgentTag, SectionTitle, VoteLight } from "./ui";

export function RecordView() {
  const incidentId = useStore((s) => s.incidentId);
  const decisions = useStore((s) => s.view.decisions);
  const lastSeq = useStore((s) => s.lastSeq);
  const [md, setMd] = useState("");

  useEffect(() => {
    if (incidentId) api.record(incidentId).then((r) => setMd(r.markdown)).catch(() => undefined);
  }, [incidentId, lastSeq]);

  if (!incidentId) return <p className="p-6 text-dim">Start an incident to build a decision record.</p>;

  return (
    <div className="grid min-h-0 flex-1 gap-3 overflow-y-auto p-3 lg:grid-cols-2">
      <div className="frame">
        <SectionTitle>Decisions</SectionTitle>
        <ol className="space-y-3 p-3">
          {decisions.map((d) => (
            <li key={d.id} className="border-l-2 border-amber pl-3">
              <div className="flex flex-wrap items-center gap-2">
                <span className="display text-[16px] font-bold">{d.id} · {d.outcome}</span>
                <span className="font-mono text-[12px] text-dim">{d.decision_point} round {d.round} · {d.decider}{d.ruled_by ? ` (${d.ruled_by})` : ""}</span>
              </div>
              <p className="text-[13px]">{d.rule_applied}</p>
              {d.decider === "COUNCIL" && (
                <div className="mt-1 flex flex-wrap gap-3">
                  {Object.entries(d.votes).map(([a, c]) => <span key={a} className="flex items-center gap-1"><AgentTag agent={a} /><VoteLight choice={c} size="sm" /></span>)}
                </div>
              )}
              {d.actions.length > 0 && <ul className="mt-1 font-mono text-[12px] text-dim">{d.actions.map((a, i) => <li key={i}>→ {actionLabel(a)}</li>)}</ul>}
              {d.certificate && <p className="mt-1 break-all font-mono text-[11px] text-dim">certificate {d.certificate}</p>}
            </li>
          ))}
        </ol>
      </div>
      <div className="frame">
        <SectionTitle>Postmortem draft (posted to Slack on close)</SectionTitle>
        <pre className="whitespace-pre-wrap p-3 font-mono text-[12.5px] leading-relaxed">{md}</pre>
      </div>
    </div>
  );
}
