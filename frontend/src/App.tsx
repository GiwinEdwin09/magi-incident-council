import { useState } from "react";
import { AgentCores } from "./components/AgentCores";
import { DeliberationLog } from "./components/DeliberationLog";
import { EscalationPanel } from "./components/EscalationPanel";
import { EvalView } from "./components/EvalView";
import { EvidencePanel } from "./components/EvidencePanel";
import { ProposalBoard } from "./components/ProposalBoard";
import { RecordView } from "./components/RecordView";
import { SlackPanel, WorldPanel } from "./components/SidePanels";
import { TopBar } from "./components/TopBar";
import { VerdictPanel } from "./components/VerdictPanel";

export default function App() {
  const [tab, setTab] = useState("control");
  return (
    <div className="scanlines flex h-full flex-col">
      <TopBar tab={tab} setTab={setTab} />
      {tab === "eval" ? (
        <EvalView />
      ) : tab === "record" ? (
        <RecordView />
      ) : (
        <main className="grid min-h-0 flex-1 gap-3 p-3 lg:grid-cols-[minmax(260px,1fr)_minmax(0,2.2fr)_minmax(300px,1.2fr)] lg:overflow-hidden">
          <div className="flex min-h-[420px] flex-col gap-3 lg:min-h-0">
            <EvidencePanel />
          </div>
          <div className="flex min-h-0 flex-col gap-3 lg:overflow-y-auto lg:pr-1">
            <AgentCores />
            <VerdictPanel />
            <div className="flex min-h-[340px] flex-1 flex-col"><DeliberationLog /></div>
          </div>
          <div className="flex min-h-0 flex-col gap-3">
            <div className="flex min-h-[360px] flex-[3] flex-col lg:min-h-0"><ProposalBoard /></div>
            <WorldPanel />
            <div className="flex min-h-[160px] flex-[1] flex-col lg:min-h-0"><SlackPanel /></div>
          </div>
        </main>
      )}
      <EscalationPanel />
    </div>
  );
}
