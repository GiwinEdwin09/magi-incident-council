import { useState } from "react";
import { api } from "../lib/api";
import { useStore } from "../lib/store";
import { AgentTag, RefChip, TierBadge } from "./ui";

const CALL_TEXT: Record<string, string> = {
  starting: "Preparing the call",
  dialing: "Dialing the on-call engineer…",
  ringing: "Ringing…",
  in_progress: "On the call",
  ended: "Call ended",
  failed: "Call failed: rule here instead",
  no_phone: "No phone configured: rule here",
};

export function EscalationPanel() {
  const esc = useStore((s) => s.view.escalation);
  const incidentId = useStore((s) => s.incidentId);
  const slack = useStore((s) => s.view.slack);
  const [code, setCode] = useState("");
  const [conditions, setConditions] = useState("");
  const [info, setInfo] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  const [unsealed, setUnsealed] = useState<Record<string, string>>({});
  const [collapsed, setCollapsed] = useState(false);
  if (!esc || !incidentId) return null;
  const d = esc.dossier;
  const codeHint = [...slack].reverse().find((m) => m.kind === "escalation");
  const localCode = codeHint?.via === "local" ? codeHint.text.match(/Confirmation code: (\d{3})/)?.[1] : undefined;

  const rule = async (key: string) => {
    setMsg(null);
    try {
      const r = await api.ruling(incidentId, { option_key: key, conditions, ruled_by: "on-call (UI)", confirm_code: code });
      setMsg(r.message);
    } catch (e) {
      setMsg((e as Error).message);
    }
  };
  const addInfo = async (text: string) => {
    if (!text.trim()) return;
    await api.info(incidentId, text.trim(), "on-call").catch((e) => setMsg(String(e)));
    setInfo("");
  };
  const unseal = async (id: string) => {
    try {
      const r = await api.unseal(incidentId, id, code);
      setUnsealed((u) => ({ ...u, [id]: r.content }));
    } catch (e) {
      setMsg((e as Error).message);
    }
  };

  if (collapsed) {
    return (
      <button onClick={() => setCollapsed(false)} className="pulse-alarm fixed bottom-4 right-4 z-30 bg-alarm px-4 py-3 display font-bold text-white">
        ⚠ Human decision needed: open
      </button>
    );
  }

  return (
    <div className="fixed inset-0 z-30 flex items-start justify-center overflow-y-auto bg-black/70 p-4" role="dialog" aria-modal="true" aria-label="Escalation">
      <div className="w-full max-w-4xl border-2 border-alarm bg-panel">
        <div className="hazard h-2" />
        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-line px-4 py-2">
          <div>
            <div className="display text-2xl font-bold text-alarm">Escalated · human decision required</div>
            <div className="text-[13px] text-dim">{d.reason}</div>
          </div>
          <div className="flex items-center gap-3">
            <span className={`display px-2 py-1 text-[14px] ${esc.call === "dialing" || esc.call === "in_progress" ? "pulse-alarm bg-alarm text-white" : "bg-panel-2 text-ink"}`}>
              📞 {CALL_TEXT[esc.call] ?? esc.call}
            </span>
            <button onClick={() => setCollapsed(true)} className="border border-line px-2 py-1 text-[12px] text-dim hover:text-ink">Minimize</button>
          </div>
        </div>

        <div className="space-y-4 p-4">
          {esc.reconvening && <div className="border border-ink bg-ink/10 px-3 py-2 text-[14px]">New information received. The council is re-deliberating…</div>}
          <div>
            <div className="display text-[13px] text-dim">Situation</div>
            <p className="text-[15px]">{d.situation}</p>
          </div>
          <div className="border-l-4 border-amber bg-panel-2 px-3 py-2">
            <div className="display text-[13px] text-amber">The decision you need to make</div>
            <p className="text-[19px] font-semibold leading-snug">{d.crux}</p>
          </div>

          <div className="grid gap-3 md:grid-cols-3">
            {d.options.map((o) => (
              <div key={o.key} className="flex flex-col border border-line bg-panel-2 p-3">
                <div className="flex items-center gap-2">
                  <span className="display text-3xl font-bold text-amber">{o.key}</span>
                  <RefChip id={o.proposal_ref} />
                  <TierBadge tier={o.tier} />
                </div>
                <p className="mt-1 flex-1 text-[14px] leading-snug">{o.summary}</p>
                <p className="mt-1 text-[12px] text-dim">Main risk: {o.main_risk}</p>
                <p className="mt-1 text-[12px]">Backed by: {o.supporters.length ? o.supporters.map((a) => <AgentTag key={a} agent={a} />) : <span className="text-dim">no agent</span>}</p>
                <button onClick={() => rule(o.key)} className="display mt-2 bg-amber py-1.5 font-bold text-black hover:brightness-110">
                  Rule option {o.key}
                </button>
              </div>
            ))}
          </div>

          <div className="grid gap-3 md:grid-cols-2">
            <div className="space-y-2">
              <label className="block text-[13px]">
                <span className="text-dim">Confirmation code (posted to Slack{localCode ? `; local echo in #incident shows ${localCode}` : ""})</span>
                <input value={code} onChange={(e) => setCode(e.target.value)} inputMode="numeric" maxLength={3}
                  className="mt-1 block w-28 border border-line bg-bg px-2 py-1 font-mono text-lg tracking-widest" placeholder="000" />
              </label>
              <label className="block text-[13px]">
                <span className="text-dim">Condition attached to your ruling (optional)</span>
                <input value={conditions} onChange={(e) => setConditions(e.target.value)} placeholder="e.g. if lag isn't under 5s in 6 minutes, do A"
                  className="mt-1 block w-full border border-line bg-bg px-2 py-1" />
              </label>
              {d.sealed_available.map((id) => (
                <div key={id} className="text-[13px]">
                  <button onClick={() => unseal(id)} className="border border-balthasar px-2 py-1 text-balthasar hover:bg-balthasar hover:text-black">
                    🔒 Unseal {id} (needs code)
                  </button>
                  {unsealed[id] && <p className="mt-1 border-l-2 border-balthasar pl-2 text-[13px]">{unsealed[id]}</p>}
                </div>
              ))}
            </div>
            <div className="space-y-2">
              <div className="text-[13px] text-dim">Add information instead (the agents re-deliberate with it)</div>
              <textarea value={info} onChange={(e) => setInfo(e.target.value)} rows={3}
                className="block w-full border border-line bg-bg px-2 py-1" placeholder="e.g. I approve discarding the in-flight writes; finance will reconcile." />
              <div className="flex flex-wrap gap-2">
                <button onClick={() => addInfo(info)} className="border border-ink px-3 py-1 text-[13px] hover:bg-ink hover:text-black">Send to council</button>
                <button onClick={() => addInfo("I approve discarding the in-flight writes; finance will reconcile from processor logs.")}
                  className="border border-line px-3 py-1 text-[12px] text-dim hover:text-ink">Preset: approve the write loss</button>
              </div>
            </div>
          </div>

          <div>
            <div className="display text-[13px] text-dim">Where the agents stand</div>
            <ul className="mt-1 space-y-1 text-[13px]">
              {Object.entries(d.positions).map(([a, p]) => <li key={a}><AgentTag agent={a} /> {p}</li>)}
            </ul>
          </div>
          {codeHint && <p className="font-mono text-[12px] text-dim">Slack: {codeHint.text}</p>}
          {msg && <p role="status" className="text-[14px] text-amber">{msg}</p>}
        </div>
      </div>
    </div>
  );
}
