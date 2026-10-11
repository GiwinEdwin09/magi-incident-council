import type { AppConfig, IncidentSummary, ScenarioInfo } from "./types";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(path, {
    ...init,
    headers: { "content-type": "application/json", ...(init?.headers ?? {}) },
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(body?.detail ?? `${r.status} ${r.statusText}`);
  return body as T;
}

const post = <T>(path: string, body: unknown) => req<T>(path, { method: "POST", body: JSON.stringify(body) });

export const api = {
  config: () => req<AppConfig>("/api/config"),
  scenarios: () => req<ScenarioInfo[]>("/api/scenarios"),
  incidents: () => req<IncidentSummary[]>("/api/incidents"),
  start: (id: string, body: { speed?: number; mode?: string }) =>
    post<{ incident_id: string }>(`/api/scenarios/${id}/start`, body),
  inject: (incident: string, body: { injection_id?: string; content?: string; source?: string }) =>
    post<{ evidence_id: string }>(`/api/incidents/${incident}/inject`, body),
  control: (incident: string, action: "pause" | "resume" | "speed" | "stop", speed?: number) =>
    post(`/api/incidents/${incident}/control`, { action, speed }),
  ruling: (incident: string, body: { option_key: string; conditions?: string; ruled_by: string; confirm_code: string }) =>
    post<{ message: string }>(`/api/incidents/${incident}/ruling`, { ...body, via: "ui" }),
  info: (incident: string, text: string, by: string) => post(`/api/incidents/${incident}/info`, { text, by }),
  unseal: (incident: string, evidence_id: string, code: string) =>
    post<{ content: string }>(`/api/incidents/${incident}/unseal`, { evidence_id, code }),
  confirm: (incident: string, decision: string, approved: boolean, by: string) =>
    post(`/api/incidents/${incident}/confirm/${decision}`, { approved, by }),
  record: (incident: string) => req<{ markdown: string }>(`/api/incidents/${incident}/record`),
};
