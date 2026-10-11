import { useState } from "react";
import { api } from "../lib/api";
import { useStore } from "../lib/store";
import { actionLabel } from "../lib/types";
import { AgentTag, RefChip, TierBadge, VoteLight } from "./ui";

const OUTCOME_STYLE: Record<string, string> = {
  EXECUTE: "bg-ok text-black",
  CONFIRM: "bg-amber text-black",
  NEXT_ROUND: "bg-panel-2 text-amber border border-amber",
  ESCALATE: "bg-alarm text-white",
  INSUFFICIENT_INFO: "bg-alarm text-white",
  HOLD: "bg-panel-2 text-dim",
};

function ConfirmCard() {
  const confirm = useStore((s) => s.view.confirm);
  const incidentId = useStore((s) => s.incidentId);
  const [busy, setBusy] = useState(false);
  if (!confirm || !incidentId) return null;
  const act = async (approved: boolean) => {
    setBusy(true);
    await api.confirm(incidentId, confirm.decision_id, approved, "on-call (UI)").catch(() => undefined);
    setBusy(false);
  };
  return (
    <div className="pulse-alarm mt-3 border-2 border-amber bg-panel-2 p-3" role="alertdialog" aria-label="Confirm irreversible action">
      <div className="display text-[15px] font-bold text-amber">Human confirmation required</div>
      <p className="mt-1 text-[13px]">
        All three agents accept <RefChip id={confirm.proposal_ref} />, an irreversible ({confirm.tier}) action. It will not run without a human.
        {confirm.via === "n8n" ? " The request is also in Slack." : ""} No answer in {confirm.timeout_s}s counts as deny.
      </p>
      <div className="mt-2 flex gap-2">
        <button disabled={busy} onClick={() => act(true)} className="display bg-ok px-4 py-1.5 font-bold text-black">Approve</button>
        <button disabled={busy} onClick={() => act(false)} className="display bg-alarm px-4 py-1.5 font-bold text-white">Deny</button>
      </div>
    </div>
  );
}

export function VerdictPanel() {
  const v = useStore((s) => s.view);
  const lead = v.leading ? v.proposals[v.leading.split("@")[0]] : undefined;
  const leadVersion = lead?.versions[lead.versions.length - 1];
  const last = v.decisions[v.decisions.length - 1];
  const votes = leadVersion ? lead?.votes[`${leadVersion.id}@${leadVersion.version}`] ?? {} : {};

  return (
    <section className="frame p-3" aria-label="Current decision">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <div className="display text-[13px] text-dim">
          {v.dp ? `Decision point ${v.dp.id}${v.dp.title ? ` · ${v.dp.title}` : ""} · round ${v.round || "—"}` : "Waiting for the first decision point"}
        </div>
        {last && (
          <div className={`display px-2 py-0.5 text-[14px] font-bold ${OUTCOME_STYLE[last.outcome] ?? ""}`}>
            {last.id} · {last.outcome.replace("_", " ")}{last.decider === "HUMAN" ? " · HUMAN" : ""}
          </div>
        )}
      </div>
      {v.dp && <p className="mt-1 text-[15px] font-medium">{v.dp.question}</p>}

      {leadVersion && (
        <div className="mt-3 border-l-4 border-amber bg-panel-2 px-3 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className="display text-[13px] text-amber">On the ballot</span>
            <RefChip id={`${leadVersion.id}@${leadVersion.version}`} />
            <TierBadge tier={leadVersion.tier} reasons={leadVersion.tier_reasons} />
            <span className="font-semibold">{leadVersion.draft.title}</span>
          </div>
          <ul className="mt-1 flex flex-wrap gap-x-4 font-mono text-[12px] text-dim">
            {leadVersion.draft.actions.map((a, i) => <li key={i}>→ {actionLabel(a)}</li>)}
          </ul>
          <div className="mt-2 flex flex-wrap gap-3">
            {(["MELCHIOR", "BALTHASAR", "CASPER"] as const).map((a) => (
              <span key={a} className="flex items-center gap-1.5"><AgentTag agent={a} /> <VoteLight choice={votes[a]} size="sm" /></span>
            ))}
          </div>
          {v.leadingInfo && Object.keys(v.leadingInfo.schulze?.wins ?? {}).length > 1 && (
            <p className="mt-2 text-[12px] text-dim" title="Each agent ranks proposals; the Schulze method picks the one that wins the most head-to-head matchups. Proposals worse on every mandate are dropped first (Pareto filter).">
              Chosen by ranked vote (Schulze){v.leadingInfo.dropped.length ? `; dropped as dominated: ${v.leadingInfo.dropped.join(", ")}` : ""}.
              {new Set(Object.values(v.leadingInfo.schulze.wins)).size === 1 ? " Rankings form a cycle (genuine three-way disagreement); tie broken toward the earliest proposal." : ""}
            </p>
          )}
        </div>
      )}

      {last && (
        <p className="mt-2 text-[13px]">
          <span className="text-dim">Rule applied: </span>{last.rule_applied}
          {last.outcome === "EXECUTE" && last.proposal_ref && <> · <span className="text-dim">executed</span> <RefChip id={last.proposal_ref} /></>}
        </p>
      )}
      <ConfirmCard />
    </section>
  );
}
