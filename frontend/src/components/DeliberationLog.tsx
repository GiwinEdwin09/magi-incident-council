import { useEffect, useRef, useState } from "react";
import type { Tone } from "../lib/reducer";
import { useStore } from "../lib/store";
import { simTime } from "../lib/types";
import { AgentTag, RefChip, SectionTitle } from "./ui";

const FILTERS: Record<string, { label: string; kinds?: string[] }> = {
  all: { label: "All" },
  arguments: { label: "Objections & dissent", kinds: ["objection", "challenge", "dissent"] },
  changes: { label: "Changes of mind", kinds: ["change"] },
  votes: { label: "Votes & decisions", kinds: ["vote", "decision", "confirm", "escalate", "human", "execute"] },
  evidence: { label: "Evidence & tools", kinds: ["evidence", "assess", "tool", "interrupt"] },
};

const TONE: Record<Tone, string> = {
  info: "border-transparent",
  ok: "border-ok",
  warn: "border-balthasar",
  alarm: "border-alarm bg-alarm/10",
  human: "border-ink bg-ink/5",
};

export function DeliberationLog() {
  const log = useStore((s) => s.view.log);
  const [filter, setFilter] = useState("all");
  const [follow, setFollow] = useState(true);
  const box = useRef<HTMLDivElement>(null);
  const kinds = FILTERS[filter].kinds;
  const rows = kinds ? log.filter((r) => kinds.includes(r.kind)) : log;

  useEffect(() => {
    if (follow && box.current) box.current.scrollTop = box.current.scrollHeight;
  }, [rows.length, follow]);

  return (
    <div className="frame flex min-h-0 flex-col">
      <SectionTitle right={
        <div className="flex flex-wrap items-center gap-1">
          {Object.entries(FILTERS).map(([id, f]) => (
            <button key={id} onClick={() => setFilter(id)}
              className={`border px-1.5 py-0.5 text-[11px] ${filter === id ? "border-amber text-amber" : "border-line text-dim hover:text-ink"}`}>
              {f.label}
            </button>
          ))}
          <label className="ml-2 flex items-center gap-1 text-[11px] text-dim">
            <input type="checkbox" checked={follow} onChange={(e) => setFollow(e.target.checked)} /> follow
          </label>
        </div>
      }>Deliberation log</SectionTitle>
      <div ref={box} className="min-h-0 flex-1 overflow-y-auto px-2 py-1 font-mono text-[12.5px] leading-snug" role="log" aria-live="polite">
        {rows.map((r) => (
          <div key={`${r.seq}-${r.kind}-${r.text.length}`} className={`grid grid-cols-[64px_96px_1fr] gap-2 border-l-2 py-0.5 pl-2 ${TONE[r.tone]}`}>
            <span className="text-dim">{simTime(r.sim_ts)}</span>
            <AgentTag agent={r.agent} />
            <span className="font-sans text-[13px]">
              {r.text}
              {r.refs.filter((x) => /^(E|S|P|C)-/.test(x)).slice(0, 4).map((x) => <RefChip key={x} id={x} />)}
            </span>
          </div>
        ))}
        {rows.length === 0 && <div className="p-2 text-dim">Nothing yet. Start an incident above.</div>}
      </div>
    </div>
  );
}
