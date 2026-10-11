import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { useStore } from "../lib/store";
import type { AppConfig, IncidentSummary, ScenarioInfo } from "../lib/types";
import { simTime } from "../lib/types";

export function TopBar({ tab, setTab }: { tab: string; setTab: (t: string) => void }) {
  const view = useStore((s) => s.view);
  const connected = useStore((s) => s.connected);
  const incidentId = useStore((s) => s.incidentId);
  const connect = useStore((s) => s.connect);
  const [scenarios, setScenarios] = useState<ScenarioInfo[]>([]);
  const [config, setConfig] = useState<AppConfig | null>(null);
  const [scenario, setScenario] = useState("s2_ghost_process");
  const [mode, setMode] = useState("scripted");
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<IncidentSummary[]>([]);
  const finished = !!view.resolved || !!view.ended;

  useEffect(() => {
    api.scenarios().then(setScenarios).catch((e) => setError(String(e)));
    api.config().then((c) => {
      setConfig(c);
      setMode(c.mode === "live" ? "live" : "scripted");
    }).catch(() => setError("Backend not reachable on :8787. Start it with: cd backend && uv run uvicorn magi.main:app --port 8787"));
    // A refresh, or a link with #INC-XXXX, reopens that incident (live or from the saved log).
    const fromUrl = () => decodeURIComponent(location.hash.slice(1));
    if (fromUrl()) connect(fromUrl());
    const onHash = () => fromUrl() && fromUrl() !== useStore.getState().incidentId && connect(fromUrl());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, [connect]);

  const refreshHistory = () => api.incidents().then(setHistory).catch(() => undefined);
  useEffect(() => {
    refreshHistory();
  }, [incidentId, finished]);

  const start = async () => {
    setError(null);
    try {
      const { incident_id } = await api.start(scenario, { mode });
      connect(incident_id);
      setTab("control");
    } catch (e) {
      setError(String((e as Error).message));
    }
  };

  const ctl = (action: "pause" | "resume" | "speed", speed?: number) =>
    incidentId && api.control(incidentId, action, speed).catch((e) => setError(String(e)));

  const inject = (id: string) => incidentId && api.inject(incidentId, { injection_id: id }).catch((e) => setError(String(e)));

  const alarm = !!view.escalation && !finished;
  const status = view.resolved ? "RESOLVED" : view.ended ? view.ended.reason.toUpperCase() : view.escalation ? "ESCALATED" : view.dp ? "DELIBERATING" : incidentId ? "MONITORING" : "STANDBY";

  return (
    <header className="border-b border-line bg-panel">
      <div className={`h-1 ${alarm ? "hazard" : "bg-amber"}`} />
      <div className="flex flex-wrap items-center gap-x-5 gap-y-2 px-4 py-2">
        <div className="flex items-baseline gap-3">
          <span className="display text-3xl font-bold leading-none text-amber">MAGI</span>
          <span className="display text-[13px] text-dim">Incident council</span>
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className={`display px-2 py-0.5 text-[13px] font-bold ${alarm ? "pulse-alarm bg-alarm text-white" : view.resolved ? "bg-ok text-black" : view.ended ? "bg-panel-2 text-dim" : "bg-panel-2 text-amber"}`}>
              {status}
            </span>
            {view.incidentId && <span className="font-mono text-[13px] text-dim">{view.incidentId}</span>}
            <span className="truncate text-[15px] font-semibold">{view.title || "No incident running"}</span>
          </div>
          {view.company && <div className="text-[12px] text-dim">{view.company} · {view.mode} mode{view.mode === "scripted" ? " (deterministic agents, no API calls)" : ""}</div>}
        </div>

        <div className="flex items-center gap-3 font-mono text-[13px]">
          <span title="Simulated incident clock">{simTime(view.simTs)}</span>
          <span className="text-dim">×{view.speed}{view.paused ? " PAUSED" : ""}</span>
          <span className={connected ? "text-ok" : "text-dim"} title="Event stream">{connected ? "● live" : "○ offline"}</span>
          {config && (
            <span className="text-dim" title="Integrations: local fallback is used when not configured">
              n8n:{config.n8n ? <b className="text-ok">on</b> : "local"} · phone:{config.phone ? <b className="text-ok">on</b> : "UI"}
            </span>
          )}
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2 border-t border-line px-4 py-2">
        <nav className="mr-3 flex" aria-label="Views">
          {[["control", "Control room"], ["record", "Decision record"]].map(([id, label]) => (
            <button key={id} onClick={() => setTab(id)}
              className={`display border px-3 py-1 text-[13px] ${tab === id ? "border-amber bg-amber text-black" : "border-line text-dim hover:text-ink"}`}>
              {label}
            </button>
          ))}
        </nav>

        <label className="flex items-center gap-2 text-[13px] text-dim">
          Scenario
          <select value={scenario} onChange={(e) => setScenario(e.target.value)}
            className="border border-line bg-panel-2 px-2 py-1 text-ink">
            {scenarios.map((s) => <option key={s.id} value={s.id}>{s.title}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-2 text-[13px] text-dim">
          Agents
          <select value={mode} onChange={(e) => setMode(e.target.value)} className="border border-line bg-panel-2 px-2 py-1 text-ink">
            <option value="scripted">Scripted (offline)</option>
            <option value="live" disabled={!config?.has_api_key}>Live LLM{config?.has_api_key ? "" : " (needs API key)"}</option>
            <option value="record" disabled={!config?.has_api_key}>Live + record</option>
            <option value="replay">Replay recording</option>
          </select>
        </label>
        <button onClick={start} className="display bg-amber px-4 py-1 text-[14px] font-bold text-black hover:brightness-110">
          ▶ Start incident
        </button>

        <label className="flex items-center gap-2 text-[13px] text-dim">
          History
          <select value={history.some((h) => h.id === incidentId) ? incidentId : ""} onFocus={refreshHistory}
            onChange={(e) => e.target.value && connect(e.target.value)}
            className="max-w-56 border border-line bg-panel-2 px-2 py-1 text-ink">
            <option value="">{history.length ? "Open a past incident…" : "No incidents yet"}</option>
            {history.map((h) => (
              <option key={h.id} value={h.id}>
                {h.id} · {h.status} · {new Date(h.opened_at).toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })} · {h.title}
              </option>
            ))}
          </select>
        </label>

        {incidentId && !finished && (
          <>
            <span className="mx-1 h-5 w-px bg-line" />
            <button onClick={() => ctl(view.paused ? "resume" : "pause")} className="border border-line px-2 py-1 text-[13px] hover:border-amber">
              {view.paused ? "Resume clock" : "Pause clock"}
            </button>
            {[6, 15, 30].map((s) => (
              <button key={s} onClick={() => ctl("speed", s)}
                className={`border px-2 py-1 font-mono text-[12px] ${view.speed === s ? "border-amber text-amber" : "border-line text-dim hover:text-ink"}`}>
                ×{s}
              </button>
            ))}
            {view.injections.length > 0 && <span className="mx-1 h-5 w-px bg-line" />}
            {view.injections.map((i) => (
              <button key={i.id} disabled={view.injected.includes(i.id)} onClick={() => inject(i.id)}
                className="border border-alarm px-2 py-1 text-[13px] text-alarm hover:bg-alarm hover:text-white disabled:opacity-40">
                Inject: {i.label}
              </button>
            ))}
          </>
        )}
        {error && <span role="alert" className="ml-2 text-[13px] text-alarm">{error}</span>}
      </div>
    </header>
  );
}
