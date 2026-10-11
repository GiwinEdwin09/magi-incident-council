import type { ReactNode } from "react";
import type { AgentName, Tier, VoteChoice } from "../lib/types";
import { useStore } from "../lib/store";

export const AGENT_META: Record<AgentName, { num: string; role: string; short: string; color: string; text: string; border: string; bg: string }> = {
  MELCHIOR: { num: "1", role: "Reliability", short: "M", color: "var(--color-melchior)", text: "text-melchior", border: "border-melchior", bg: "bg-melchior" },
  BALTHASAR: { num: "2", role: "Security & Integrity", short: "B", color: "var(--color-balthasar)", text: "text-balthasar", border: "border-balthasar", bg: "bg-balthasar" },
  CASPER: { num: "3", role: "Customers & Obligations", short: "C", color: "var(--color-casper)", text: "text-casper", border: "border-casper", bg: "bg-casper" },
};

export function SectionTitle({ children, right }: { children: ReactNode; right?: ReactNode }) {
  return (
    <div className="flex items-center justify-between border-b border-line px-3 py-1.5">
      <h2 className="display text-[15px] font-semibold text-amber">{children}</h2>
      {right}
    </div>
  );
}

const TIER_INFO: Record<Tier, { label: string; cls: string; help: string }> = {
  T0: { label: "T0 · prepare", cls: "border-t0 text-t0", help: "Observe/prepare. Passes with any ACCEPT and no mandate veto." },
  T1: { label: "T1 · reversible", cls: "border-t1 text-t1", help: "Reversible. Passes with 2 of 3 ACCEPT and no veto from the affected mandate." },
  T2: { label: "T2 · irreversible", cls: "border-t2 text-t2", help: "Irreversible or high blast radius. Needs 3 of 3 ACCEPT plus a human confirmation." },
};

export function TierBadge({ tier, reasons }: { tier: Tier; reasons?: string[] }) {
  const t = TIER_INFO[tier];
  const title = [t.help, ...(reasons ?? [])].join("\n");
  return (
    <span title={title} className={`inline-flex shrink-0 items-center border px-1.5 py-px font-mono text-[11px] font-semibold ${t.cls}`}>
      {t.label}
    </span>
  );
}

export function AgentTag({ agent, full = false }: { agent?: string | null; full?: boolean }) {
  if (!agent || !(agent in AGENT_META)) return <span className="font-mono text-[12px] text-dim">{agent ?? "SYSTEM"}</span>;
  const m = AGENT_META[agent as AgentName];
  return (
    <span className={`display shrink-0 text-[13px] font-semibold ${m.text}`}>
      {full ? `${agent}-${m.num}` : agent}
    </span>
  );
}

const VOTE: Record<VoteChoice, { cls: string; kanji: string }> = {
  ACCEPT: { cls: "bg-ok text-black", kanji: "承認" },
  REJECT: { cls: "bg-alarm text-white", kanji: "否決" },
  ABSTAIN: { cls: "bg-abstain text-white", kanji: "保留" },
};

export function VoteLight({ choice, size = "md" }: { choice?: VoteChoice; size?: "sm" | "md" }) {
  if (!choice) return <span className="font-mono text-[12px] text-dim">no vote</span>;
  const v = VOTE[choice];
  return (
    <span key={choice} className={`stamp inline-flex items-baseline gap-1.5 px-2 py-0.5 font-mono font-semibold ${v.cls} ${size === "sm" ? "text-[11px]" : "text-[13px]"}`}>
      {choice}
      <span className="text-[10px] opacity-80">{v.kanji}</span>
    </span>
  );
}

// Clickable reference chip: hovering highlights the matching evidence/proposal elsewhere on screen.
export function RefChip({ id }: { id: string }) {
  const setHighlight = useStore((s) => s.setHighlight);
  const highlight = useStore((s) => s.highlight);
  const active = highlight && (highlight === id || highlight.split("@")[0] === id.split("@")[0]);
  return (
    <button
      type="button"
      onMouseEnter={() => setHighlight(id)}
      onMouseLeave={() => setHighlight(undefined)}
      onFocus={() => setHighlight(id)}
      onBlur={() => setHighlight(undefined)}
      className={`mx-0.5 inline border px-1 font-mono text-[11px] ${active ? "border-amber bg-amber text-black" : "border-line-strong text-dim hover:text-ink"}`}
    >
      {id}
    </button>
  );
}

export function useHighlighted(id: string): boolean {
  const h = useStore((s) => s.highlight);
  if (!h) return false;
  return h === id || h.split("@")[0] === id.split("@")[0];
}

export function Visibility({ visibleTo }: { visibleTo: string[] }) {
  return (
    <span className="flex gap-0.5" title={`Visible to: ${visibleTo.join(", ")}`}>
      {(["MELCHIOR", "BALTHASAR", "CASPER"] as AgentName[]).map((a) => (
        <span
          key={a}
          className={`w-4 text-center font-mono text-[10px] font-bold ${visibleTo.includes(a) ? `${AGENT_META[a].bg} text-black` : "bg-panel-2 text-line-strong"}`}
        >
          {AGENT_META[a].short}
        </span>
      ))}
      {visibleTo.includes("human_ic") && <span className="bg-ink px-0.5 font-mono text-[10px] font-bold text-black">IC</span>}
    </span>
  );
}
