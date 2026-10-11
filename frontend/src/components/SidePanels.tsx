import { useEffect, useRef } from "react";
import { useStore } from "../lib/store";
import { simTime } from "../lib/types";
import { SectionTitle } from "./ui";

export function SlackPanel() {
  const slack = useStore((s) => s.view.slack);
  const box = useRef<HTMLUListElement>(null);
  useEffect(() => {
    if (box.current) box.current.scrollTop = box.current.scrollHeight;
  }, [slack.length]);
  return (
    <div className="frame flex min-h-0 flex-col">
      <SectionTitle right={<span className="text-[11px] text-dim">{!slack.length ? "" : slack[0].via === "n8n" ? "via n8n" : "local echo (n8n not configured)"}</span>}>
        #incident
      </SectionTitle>
      <ul ref={box} className="min-h-0 flex-1 space-y-1.5 overflow-y-auto p-2 text-[13px]">
        {slack.filter((m) => m.kind !== "record").map((m) => (
          <li key={m.seq} className="leading-snug">
            <span className="mr-1 font-mono text-[11px] text-dim">{simTime(m.sim_ts)}</span>
            <span className="font-semibold text-amber">MAGI</span> {m.text}
          </li>
        ))}
        {slack.length === 0 && <li className="text-dim">No messages.</li>}
      </ul>
    </div>
  );
}

function Stat({ label, value, bad }: { label: string; value: string; bad?: boolean }) {
  return (
    <div className="border border-line px-2 py-1">
      <div className="text-[11px] text-dim">{label}</div>
      <div className={`font-mono text-[15px] font-semibold ${bad ? "text-alarm" : "text-ink"}`}>{value}</div>
    </div>
  );
}

export function WorldPanel() {
  const world = useStore((s) => s.view.world);
  const resolved = useStore((s) => s.view.resolved);
  const decisions = useStore((s) => s.view.decisions);
  if (!world) return null;
  const services = Object.entries(world.services ?? {}) as [string, any][];
  const clusters = Object.entries(world.clusters ?? {}) as [string, any][];
  const flags = world.flags ?? {};
  const pages = decisions.filter((d) => d.outcome === "ESCALATE").length;
  return (
    <div className="frame">
      <SectionTitle>Live system (simulated)</SectionTitle>
      <div className="grid grid-cols-2 gap-1.5 p-2 xl:grid-cols-3">
        {services.map(([name, s]) => (
          <Stat key={name} label={`${name} p99`} value={`${Math.round(s.latency_p99_ms)} ms`} bad={s.latency_p99_ms > (s.slo_p99_ms ?? 800)} />
        ))}
        {services.map(([name, s]) => (
          <Stat key={`${name}-e`} label={`${name} errors`} value={`${(s.error_rate * 100).toFixed(1)}%`} bad={s.error_rate > 0.02} />
        ))}
        {clusters.map(([name, c]) => (
          <Stat key={name} label={`${name} lag`} value={`${Number(c.replication_lag_s).toFixed(0)} s`} bad={c.replication_lag_s > 5} />
        ))}
        {"exfil_mb" in flags && <Stat label="Data sent out" value={`${Math.round(flags.exfil_mb)} MB`} bad />}
        {"lost_writes" in flags && <Stat label="Lost writes" value={`${Math.round(flags.lost_writes)}`} bad={flags.lost_writes > 0} />}
        <Stat label="Humans paged" value={String(pages)} bad={pages > 0} />
        {resolved && <Stat label="LLM calls / tokens" value={`${resolved.llm_calls} / ${Math.round((resolved.input_tokens + resolved.output_tokens) / 1000)}k${resolved.cost_usd != null ? ` / $${resolved.cost_usd}` : ""}`} />}
      </div>
    </div>
  );
}
