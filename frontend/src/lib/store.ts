import { create } from "zustand";
import { initialView, reduce, type View } from "./reducer";
import type { MagiEvent } from "./types";

type Store = {
  view: View;
  lastSeq: number;
  connected: boolean;
  incidentId?: string;
  highlight?: string;
  connect: (incidentId: string) => void;
  disconnect: () => void;
  setHighlight: (ref?: string) => void;
};

let socket: WebSocket | null = null;
let retry: number | undefined;

export const useStore = create<Store>((set, get) => ({
  view: initialView(),
  lastSeq: 0,
  connected: false,
  connect: (incidentId) => {
    get().disconnect();
    set({ view: initialView(), lastSeq: 0, incidentId, connected: false });
    if (location.hash !== `#${incidentId}`) history.replaceState(null, "", `#${incidentId}`);
    const open = () => {
      const proto = location.protocol === "https:" ? "wss" : "ws";
      const ws = new WebSocket(`${proto}://${location.host}/ws/incidents/${incidentId}?since=${get().lastSeq}`);
      socket = ws;
      ws.onopen = () => set({ connected: true });
      ws.onmessage = (msg) => {
        const e = JSON.parse(msg.data) as MagiEvent;
        if (e.type === "error") {
          // Unknown incident (e.g. a stale link): stop reconnecting and go back to standby.
          get().disconnect();
          set({ incidentId: undefined });
          history.replaceState(null, "", location.pathname);
          return;
        }
        if (!e.seq || e.seq <= get().lastSeq) return;
        set((s) => ({ view: reduce(s.view, e), lastSeq: e.seq }));
      };
      ws.onclose = () => {
        set({ connected: false });
        if (socket === ws && get().incidentId === incidentId) retry = window.setTimeout(open, 1000);
      };
    };
    open();
  },
  disconnect: () => {
    window.clearTimeout(retry);
    const ws = socket;
    socket = null;
    ws?.close();
    set({ connected: false });
  },
  setHighlight: (ref) => set({ highlight: ref }),
}));
