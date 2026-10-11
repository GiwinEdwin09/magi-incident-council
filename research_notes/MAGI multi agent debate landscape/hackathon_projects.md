# Hackathon projects resembling MAGI (multi-agent debate, councils, juries, consensus, negotiation)

Method note: Devpost blocks plain fetches, so project pages and Devpost's own search JSON (`devpost.com/software/search?query=...`) were pulled with curl. About 3,500 unique project hits came from roughly 1,000 search pages ("debate", "multi-agent debate", "AI council", "AI jury", "MAGI", "evangelion", "consensus agents", "negotiation agents", "AGNTCY", etc.). Devpost ranks search results by recency, so the sample leans toward 2026. Projects were opened and read individually. A "Winner" label below means Devpost showed a winner badge on 2026-10-10. "No prize shown" also covers events whose judging may not be finished. Dates are the first timestamp on each Devpost page, which is roughly the submission date.

## Q1. Which hackathon projects implemented multi-agent debate, AI councils, juries/courts/tribunals, MAGI clones, agent negotiation, or "agents disagree" systems?

### Takeaway
At least 4 Evangelion MAGI clones were submitted to 2026 hackathons: UCI AWS Cloud Hacks, Google Cloud Rapid Agent Hackathon, StormHacks, and GirlHacks. "AI council / tribunal / committee" projects are now a crowded genre on Devpost. Almost all of them hand the final decision to a central chair, judge or synthesizer, and very few measure themselves against a baseline. Two non-hackathon GitHub repos from mid-2026, `jamespud/MAGI-system` and `Adrian-Sandwich/magi-council`, are near-identical prior art to MAGI's design, and judges could find them.

### Cited Findings

#### A. Evangelion MAGI clones at hackathons (closest analogues)
1. **MAGI**, UCI AWS Cloud Hacks 2026, Apr 2026, no prize shown. Team: Timmy Phan, Brian Lien, Kenneth Aiden Yandell. It is a "council of 3 independent LLMs, inspired by Neon Genesis Evangelion" built on Amazon Bedrock multi-agent collaboration. A background Supervisor delegates each prompt to three persona sub-agents. In the "Code Architect" preset these are Big-O optimizer, clean-code defender and security attacker. The team mixed model families (Claude 3.5 Sonnet v2, Mistral Large 2, Nova Pro, Command R+) "so the agents wouldn't suffer from shared underlying biases". It streams deliberation over Lambda SSE to React, and the Supervisor "synthesiz[es] their arguments and deliver[s] a final consensus verdict". — [Devpost: MAGI](https://devpost.com/software/magi-lxb0ne)
   - *Gaps MAGI can exploit:* a central Supervisor decides, with no rounds, voting, revision, unanimity, human escalation or baseline.
2. **magi-system**, Google Cloud Rapid Agent Hackathon, Jun 2026, no prize shown, solo (Praveen Sharma). Melchior covers data/efficiency, Balthasar empathy/psychological safety, and Caspar speed/pragmatism, all on Gemini 3.1 Flash Lite. The write-up frames the problem as "When AI agents disagree, how do we programmatically break the tie without hallucinating?" Clashes trigger a Meta-Auditor that uses an Arize Phoenix MCP tool to read OpenTelemetry traces. It treats "Processing Density (Tokens Per Second)" as a confidence proxy to pick a winner. Stack: FastAPI, React/Vite, Render and Vercel. — [Devpost: magi-system](https://devpost.com/software/magi-system)
   - *Gaps:* the tie-break uses throughput as a stand-in for correctness, which is a weak proxy. It has a central auditor and no negotiation or human escalation.
3. **TriBunal**, StormHacks 2026, Oct 4 2026, no prize shown (results may be pending), solo (Soyoung Lee). The write-up says it was inspired by "sci-fi stories where three supercomputers vote on every decision" and by the triple bottom line. Three Gemini judges, Business (quality), Environment (carbon budget) and Tech & Ethics (proportionality), vote on how an AI job should run. Majority rule plus a Python "constitution" maps the votes to FULL, DOWNGRADE, CACHE or BLOCK. A secretary agent writes a "win-win plan", and each judge speaks in its own ElevenLabs voice. There are two UI skins, a "Terminal" TUI and "Otter" mode. — [Devpost: TriBunal](https://devpost.com/software/eco-governai)
   - *Gaps:* one-shot majority vote with no debate, revision or human hand-off.
4. **Oracle Grove**, GirlHacks 2026, Oct 2026, no prize shown. Three storybook animals, Quill (logic), Ember (risk) and Willow (feelings), advise on a two-option decision. "Glowing roots" merge where they agree, and every page ends with "This choice is yours." It shows a 988 crisis page when needed. Stack: Gemini, ElevenLabs, React/GSAP. — [Devpost: Oracle Grove](https://devpost.com/software/oracle-grove-yic5n8)
   - *Notable:* the agreement visualization is a polished UI idea. *Gap:* the agents never interact.

#### B. Multi-model councils and deliberation engines
5. **MOD – Mixture of Dulus**, OpenAI Build Week, Jul 2026, no prize shown. It puts 3–5 frontier models (Claude, GPT, Gemini, Kimi, DeepSeek) into one conversation as tool-using agents. Each sees the others' last messages and can message any other member asynchronously through a mailbox ("AgentChat"). It explicitly criticizes ensembles that "fan a prompt out to N models, run them in total isolation, average or vote". By rounds 3–5 the agents "either converge on a real answer or fork". — [Devpost: MOD](https://devpost.com/software/mod-mixture-of-dulus)
6. **Council Tower Pipeline – AI Deliberation Engine**, DeveloperWeek New York 2026, May 2026, **Winner of the Tower Pipeline Challenge: Data-to-AI**. Four agents (Financial Analyst, Contrarian, Compliance Validator, Summarizer) run a 5-phase protocol: ANALYSIS → CHALLENGE (the Contrarian attacks) → VALIDATION (each agent must say whether it changed position and confidence) → LOCK (hard 0.0–1.0 confidence) → SUMMARY. — [Devpost: Council Tower Pipeline](https://devpost.com/software/council-tower-pipeline-ai-deliberation-engine)
7. **FactNews / "Consensus"**, HackEurope, Feb 2026, no prize shown. A council of LLMs (OpenAI, Anthropic, Gemini, Grok, DeepSeek via OpenRouter and Cerebras) with RAG over 20+ outlets identifies consensus and "highlight[s] contested facts" in the news. A judge model writes the synthesis. — [Devpost: Consensus](https://devpost.com/software/consensus-tdv0el)
8. **syro**, Dublin Hacx, Oct 2026, no prize shown. Questions go to a swarm of local models running on volunteers' laptops. Each round, answers are embedded and peer-scored: +1.0 for being closest to others, +0.5 for being furthest (a "new angle"), and strikes for copies or junk. A larger verifier model grades the answers anonymously ("Agreeing isn't being right"). Payouts go through Stripe Connect. — [Devpost: syro](https://devpost.com/software/syro)
9. **TheAgora ("AI Democracy")**, Hugging Face Agents & MCP Hackathon (mcp-server-track), 2025, no prize info. Models propose, see each other's proposals (attributed or anonymous), rebut, then vote. Consensus comes from majority, confidence- or role-weighting, or a moderator, and "disagreements are logged explicitly". Models: Claude for ethics, GPT-4o for creativity, Mistral for technical analysis, SambaNova for facts. — [HF Space README](https://huggingface.co/spaces/Agents-MCP-Hackathon/TheAgora/blob/main/README.md)
10. **Consilium MCP Server**, Hugging Face Agents & MCP Hackathon (mcp-server-track and agent-demo-track), 2025, prize status unverified (the collection page shows a 🏆 emoji with no explanation). It shows a "visual roundtable" with speech bubbles and also runs as an MCP server. Models are Mistral Large, DeepSeek-R1, Llama-3.3-70B and QwQ-32B. A research agent pulls from Web, Wikipedia, arXiv, GitHub and SEC EDGAR. Roles, protocol and communication strategy are configurable, and so is the number of rounds. — [HF Space README](https://huggingface.co/spaces/Agents-MCP-Hackathon/consilium_mcp/raw/main/README.md); [HF collection](https://huggingface.co/collections/Agents-MCP-Hackathon/consilium-68461d2bbe1c5539087b7b0f)
11. **AXIOM – Cognitive Blind Spot Engine**, Build the Future with AI Moonshot Hackathon, Jul 2026, **Winner: Top 100 Finalist Award**. Two four-agent "rooms" debate a claim: a VC matrix and an epistemic matrix with Historian, Contrarian, Scientist and Philosopher. Each agent has a "locked, enforced persona", and the result is a weighted "Blind Spot Score". — [Devpost: AXIOM](https://devpost.com/software/axiom-the-cognitive-stress-test-engine)

#### C. Courts, juries, tribunals
12. **Split Decision**, Global AI Hackathon Series with Qwen Cloud, Jul 2026, **Winner: Blog Post Award and Top 10 Honorable Mention**, solo (Tarik Moody). Nine AI justices are each committed to a judicial philosophy (Textualist, Originalist, Pragmatist and others). They cast **secret ballots**, argue in rounds, and file a verdict **with dissents** on real Supreme Court cases. **Self-grading against the real Court across 4 arms:** one model asked directly, nine judges voting silently, full deliberation, and a control of nine neutral analysts with no philosophies. It has also filed public predictions on three undecided cases. The motivation is stated directly: "Nobody I asked could show me numbers", and agents "start agreeing with each other, fast". It also has a pixel-art courtroom replay, a podcast made by two AI journalist agents, and a live bench running on the deployed server. Models: Qwen3.7-plus/max. — [Devpost: Split Decision](https://devpost.com/software/split-decision)
13. **JURO – AI Tribunal for Denied Health Insurance Claims**, Jun 2026, **Winner: Second Runner-Up (Vitalitics 2026 LUMA Pitch Competition)** and **Winner: Membership (Hack Begin Impact Creation)**, solo (Priyanshu R). Four agents share one room: Advocate, Scrutinizer (argues the insurer's side), Evidence (finds the resolving statute) and Adjudicator (recommends). **"A human always delivers the final ruling."** The record is a SHA-256 hash-chained, tamper-evident audit trail, and the system auto-generates an appeal letter citing ERISA/ACA. Built with the Anthropic Band SDK, a LangGraph state machine and Deepgram voice. — [Devpost: JURO](https://devpost.com/software/juro); [Devpost: JURO (LUMA entry)](https://devpost.com/software/juro-an-ai-tribunal-for-denied-health-insurance-claims-boi6tg)
14. **Devil's Advocate**, Pixel Forge AI Hackathon, Aug 2026, no prize shown. Two agents are assigned opposite sides and write blind openings, then quote-based rebuttals, then cross-examination. Open clash lasts 0–6 rounds and continues **"only while a referee rules the disagreement still live"**, so stopping is an explicit decision. The judge scores both sides from 0–100 and names "the question neither side settled". The user can then challenge, and the judge is told the user's argument "carries no authority from you having started the debate". — [Devpost: Devil's Advocate](https://devpost.com/software/devil-s-advocate-ovw6lc)
15. **Devil's Advocate and Jury**, Elasticsearch Agent Builder Hackathon, Feb 2026, no prize shown. A proponent and a devil's advocate may argue only from documents retrieved from Elasticsearch. A Jury agent re-fetches every citation and penalizes misquoted or invented ones (a "no-hallucination contract"). — [Devpost](https://devpost.com/software/devil-s-advocate-and-jury)
16. **Gavel – The Disagreement Engine**, Qloo Agentic Hackathon, Oct 2026, no prize shown. Two advocate agents argue group-dining options from Qloo taste-graph evidence. The **judge is fully deterministic** ("vetoes and decisions are rules, not vibes"). UI elements include a tug-of-war meter, evidence board and verdict card. — [Devpost: Gavel](https://devpost.com/software/fauxpas)
17. **Small Claims Court**, CloudHacks 2026 Singapore, Sep 2026, **Winner: People's Choice**. A comedic petty-grievance court with three judge personas, voiced rulings, a PDF court order with QR code, and an appeal to a "Lord Chief Justice". — [Devpost](https://devpost.com/software/small-claims-court)
18. **DAOCouncil**, ETHGlobal "Agentic Ethereum" (exact date not on the fetched page; believed to be early 2025, unverified), **Winner: Autonome Best Social Agent** and **3rd place, Coinbase Developer Platform AgentKit pool prize**. AI jurors with distinct personas read DAO debates, "update their stance as the debate progresses", render verdicts and vote. The goal is to reduce token-whale dominance. — [ETHGlobal showcase](https://ethglobal.com/showcase/daocouncil-8d9k4)
19. **Deb8: Clash of the Models**, Meta Llama 3 Hackathon, May 2024, **Winner: 2nd Place**. It uses debate as an *evaluation* method. Models debate in Karl Popper format across 10 topics × 10 categories and are scored with the FLASK metric, with GPT-4 as a benchmark judge. — [Devpost: Deb8](https://devpost.com/software/deb8-clash-of-the-models)

#### D. Investment committees and forecasting
20. **The Committee – Explainable AI Paper-Trading Lab**, OpenAI Build Week, Jul 2026, no prize shown. Five agents (Quant, Risk, Macro, Sentiment, Contrarian) debate in 2 rounds, and a Chairman records the decision. A trade opens only after weighted agreement, a positive Chairman verdict, no Risk veto and capacity checks. Extras include "War Room transcripts", a counterfactual "Decision Integrity Lab" and a cryptographic proof ledger, and "a documented hold" is treated as a valid outcome. — [Devpost](https://devpost.com/software/the-committee-explainable-ai-paper-trading-lab)
21. **VerdictX – Institutional AI Investment Committee**, OpenAI Build Week, Jul 2026, no prize shown. Six analysts (Bull, Bear, Quant, Macro, Risk, Chair) research live data, challenge each other, "update their confidence in real time", and vote one at a time. The Chair writes the memo. — [Devpost](https://devpost.com/software/verdictx-institutional-ai-investment-committee)
22. **ProphETF**, Hack Knight Fall 2026, Oct 2026, no prize shown (judging likely pending). A 5-agent panel (Growth, Value/risk, Macro, Skeptic, Fit checker) votes on stocks and on "beat the S&P next week?". The team **back-tested the panel on 8 past weeks (80 decisions): "right 50% of the time, no better than a coin flip, and the site says so next to every vote."** It asks clarifying questions instead of guessing. — [Devpost: ProphETF](https://devpost.com/software/prophetf)
23. **AI Forecasting Track / OracleFlow**, Uncommon Hacks 2026, May 2026, **Winner: Agents for Prediction Markets (Sigma Lab)**. A three-call debate (outside view, inside view, reconciler) turns the *amount of disagreement* into a confidence signal that drives extremization. Calibration uses Platt scaling fitted on 1,393 resolved Kalshi markets. — [Devpost](https://devpost.com/software/ai-forecasting-track)
24. **J^2**, First Visions: Danta, Sep 2025, **Winner: First Prize ($1,000 + credits)**. Six debate agents (Macro, Equity, Risk, Quant, Sentiment, Fact-Checker) cross-reference each other's arguments. An orchestrator produces a consensus recommendation and executes compliant trades, with a 3D agent visualization. — [Devpost: J^2](https://devpost.com/software/j-2)

#### E. Negotiation with private information (closest to the "competing objectives" brief)
25. **unsaid**, DivHacks 2026, Sep 2026, **Winner: Capital One sponsor challenge (Best Use of Nessie)**. Each friend gets a personal agent in iMessage, and "the agents do the arguing" over budget, diet and commute. **Private information is designed in:** "Each agent sees only its own person". The orchestrator pools only the lowest budget, combined dietary needs and the overlapping time window, and "Nobody finds out whose budget set the ceiling." The output is an iMessage poll that humans vote on. — [Devpost: unsaid](https://devpost.com/software/unsaid-zm8w5v)

#### F. Other notable entries (shorter)
- **The AI Council**, uOttaHack 8, Jan 2026. Eleven agents govern a medieval kingdom, and a Sovereign agent makes the final call. It has an autonomous mode and a "Manual / Intervention Mode" where a human can pause or steer. Built with Solace Agent Mesh, AWS WebSocket API and React. — [Devpost](https://devpost.com/software/the-ai-council)
- **GhostTrace**, NextGenHacks, Jun 2026, **Winner: Top 9 Finalists**. Attacker, Skeptic and Arbiter agents work on cyber incident response, and confidence comes from rulings on each claim (SUSTAINED, NEEDS_MORE_EVIDENCE and so on). — [Devpost](https://devpost.com/software/ghosttrace-jh5ws8)
- **BLUEPRINT: AI Property Due Diligence**, Google Cloud Rapid Agent Hackathon, Jun 2026, **Winner: Elastic 2nd Place**. Seven data agents feed an Optimist vs Pessimist debate before the final risk score. — [Devpost](https://devpost.com/software/blueprint-ai-property-due-diligence)
- **Decision Room**, Amazon Nova AI Hackathon, Mar 2026, **Winner: Bonus Blog Post Prize**. A stakeholder panel questions the user, then holds a "closed-door deliberation" that reports a "consensus gap" metric. — [Devpost](https://devpost.com/software/decision-room)
- **Jury**, AI Builders Hackathon, Sep 2026. Five investigators build "a cited, versioned record of the beliefs your idea depends on". It criticizes "AI advisor panel" tools that "dressed one model up as five people and called the agreement consensus." — [Devpost](https://devpost.com/software/jury-abiehq)
- **BoardSeat.dev**, Life After Code, Oct 2026. A five-seat AI board (CEO, CTO, CFO, CS and a Chair) reviews every GitLab merge request, and "every verdict ships with a bet you can check later." — [Devpost](https://devpost.com/software/boardseat-dev)
- **Counterfactual Financial Oracle**, CodeFest Dec 2025, **Winner: General Build track**. Gemini (optimist) and DeepSeek (critic) debate "with convergence detection" over a Monte Carlo simulation of 10,000 scenarios. — [Devpost](https://devpost.com/software/counterfactual-financial-oracle)
- **Consensus (audio)**, AI Hackfest, Apr 2026, **Winner: Best Beginner Hack**. Five personas plus a moderator, with ElevenLabs voices. — [Devpost](https://devpost.com/software/consensus-psj7lf)
- **VERDICT AI**, 2026 Startup Week Buildathon, Feb 2026, **Winner: Best use of Lovable**. A multi-agent courtroom for witness prep. — [Devpost](https://devpost.com/software/verdict-ai)
- **DebateHub**, UB Hacking Fall 2024, Nov 2024. The classic pro, con and rubric-judge setup. — [Devpost](https://devpost.com/software/debatehub)
- **AI Agents Hackathon (Kitchener, Oct 28 2023)** had a dedicated **"Best AI vs AI Debate"** prize. Winner-badged entries included **AiDebate**, a comedic Biden vs Trump debate. Other submissions included "Con Sense Us" ("Two AI agents that debate a topic to reach Consensus") and "AI-AI Debate" (a "consensus-proposing arbiter"). — [Hackathon page](https://ai-agents-hackathon.devpost.com/); [Gallery](https://ai-agents-hackathon.devpost.com/project-gallery)

#### G. Non-hackathon MAGI clones that judges could find (prior-art risk)
- **jamespud/MAGI-system** (GitHub, created 2026-07-13, last push 2026-10-10). Melchior is "the scientist", Balthasar "the protector" and Casper "the innovator". Each "investigate[s] the question under a distinct objective function and evidence standard, then vote, debate, reflect, and re-vote toward a consensus". The principle is "LLM = semantics, code = rules": deterministic Go counts votes and handles the evidence gate, consensus, loop limits and timeouts. The Commander LLM "is deliberately *not* a 'god agent'". This is nearly MAGI's exact role split. — [GitHub](https://github.com/jamespud/MAGI-system)
- **Adrian-Sandwich/magi-council** (GitHub, created 2026-08-07). Three heads "deliberate on your questions and vote on decisions, with a ruling, **minority report, mind changes between rounds and human arbitration**". It has a memory graph and a production mode in which "on unanimous approval — it merges itself". The UI is based on TomaszRewak/MAGI. — [GitHub](https://github.com/Adrian-Sandwich/magi-council)
- Other clones: hirakujira/MAGI-System (GPT, Claude and Gemini as one model per unit; APPROVE/REJECT/ABSTAIN), 07JP27/MagiSystem (C#, majority rule), atrix228/magi-system (Android "AI tribunal" with cross-examination), anotheroom1/magi, TomaszRewak/MAGI (the UI reference). — [hirakujira](https://github.com/hirakujira/MAGI-System), [07JP27](https://github.com/07JP27/MagiSystem/), [atrix228](https://github.com/atrix228/magi-system), [anotheroom1](https://github.com/anotheroom1/magi), [TomaszRewak](https://github.com/TomaszRewak/MAGI) (descriptions taken from search snippets; READMEs not individually verified)
- Karpathy's **llm-council** (Nov 2025, not a hackathon) popularized the pattern of models answering, then anonymously reviewing and ranking each other, then a Chairman LLM synthesizing. — [Analytics Vidhya write-up](https://www.analyticsvidhya.com/blog/2025/12/llm-council-by-andrej-karpathy/)

### Inferences
- MAGI's Evangelion branding is **not novel at hackathons**: there were at least 4 MAGI-inspired submissions in 2026 alone. Differentiation has to come from mechanism (unanimity, versioned proposals, escalation, evidence injection) and from measurement, not from the theme.
- The near-identical repos, jamespud/MAGI-system (scientist/protector/innovator, deterministic vote counting) and magi-council (minority report, human arbitration, unanimity), mean MAGI should be ready for a judge asking "how is this different?". A safe answer is measured baselines, AGNTCY-native distributed agents, and live evidence injection with belief-change tracking.

### Gaps
- Devpost's search JSON ranks by recency, so 2023–2025 coverage is thinner even with deep pagination.
- lablab.ai: no debate or council *winner* was found. Its recent-winners list shows multi-agent trading and due-diligence apps such as "Deflow" and "HealthVet" ([lablab recent winners](https://lablab.ai/apps/recent-winners)), but these were not opened.
- MLH was not searched as a separate platform. Many of the events above (UB Hacking, HackDavis, StormHacks, DivHacks) are typical MLH-style student hackathons, but MLH membership was not checked.
- Prize status for October 2026 events (StormHacks, GirlHacks, Qloo, Dublin Hacx, Hack Knight, Life After Code) may still be pending.

## Q2. Which projects won prizes, and what did judges reward?

### Takeaway
In this sample, debate and council projects mostly win **sponsor-track, finalist, blog-post or people's-choice prizes, not grand prizes**. The clearest wins either (a) measured themselves against ground truth or real-world data (Split Decision, OracleFlow, Deb8), (b) tied the debate to a concrete high-stakes user problem with a human making the final call (JURO), or (c) made heavy, creative use of a sponsor's platform (Council Tower, BLUEPRINT, DAOCouncil, unsaid, the AGNTCY winners).

### Cited Findings
- **Split Decision**: Blog Post Award and Top 10 Honorable Mention. Its write-up centers on numbers, comparing single model vs silent vote vs full deliberation vs a neutral control against real Supreme Court outcomes, plus pre-registered predictions and a listenable or replayable demo. — [Devpost](https://devpost.com/software/split-decision)
- **JURO**: Second Runner-Up (Vitalitics LUMA Pitch Competition) and the Membership prize (Hack Begin). The pitch leads with statistics: 19% of US claims denied, under 1% appealed, 67–80% of appeals succeed. It adds a human-delivered binding ruling and a tamper-evident record. — [Devpost](https://devpost.com/software/juro-an-ai-tribunal-for-denied-health-insurance-claims-boi6tg)
- **OracleFlow / AI Forecasting Track**: won the Sigma Lab "Agents for Prediction Markets" prize with debate-derived confidence calibrated on 1,393 resolved markets. — [Devpost](https://devpost.com/software/ai-forecasting-track)
- **Deb8**: 2nd Place at the Meta Llama 3 Hackathon (May 2024) for "a novel and rigorous evaluation framework" using debate. — [Devpost](https://devpost.com/software/deb8-clash-of-the-models)
- **J^2**: First Prize at First Visions: Danta (Sep 2025), a 6-agent trading debate with compliance automation. — [Devpost](https://devpost.com/software/j-2)
- **Sponsor-track wins:**
  - Council Tower Pipeline: Tower challenge. — [Devpost](https://devpost.com/software/council-tower-pipeline-ai-deliberation-engine)
  - BLUEPRINT: Elastic 2nd. — [Devpost](https://devpost.com/software/blueprint-ai-property-due-diligence)
  - DAOCouncil: Autonome Best Social Agent and CDP AgentKit 3rd. — [ETHGlobal](https://ethglobal.com/showcase/daocouncil-8d9k4)
  - unsaid: Capital One Nessie. — [Devpost](https://devpost.com/software/unsaid-zm8w5v)
  - VERDICT AI: Best use of Lovable. — [Devpost](https://devpost.com/software/verdict-ai)
- **Finalist, novelty and crowd prizes:**
  - AXIOM: Top 100 Finalist. — [Devpost](https://devpost.com/software/axiom-the-cognitive-stress-test-engine)
  - GhostTrace: Top 9 Finalists. — [Devpost](https://devpost.com/software/ghosttrace-jh5ws8)
  - Small Claims Court: People's Choice. — [Devpost](https://devpost.com/software/small-claims-court)
  - Consensus (audio): Best Beginner Hack. — [Devpost](https://devpost.com/software/consensus-psj7lf)
  - Decision Room: Bonus Blog Post Prize. — [Devpost](https://devpost.com/software/decision-room)
- Several of the most MAGI-like entries (MAGI at UCI, magi-system, MOD, The Committee, VerdictX, Devil's Advocate) showed no prize badge on 2026-10-10. — [MAGI](https://devpost.com/software/magi-lxb0ne), [magi-system](https://devpost.com/software/magi-system), [MOD](https://devpost.com/software/mod-mixture-of-dulus), [The Committee](https://devpost.com/software/the-committee-explainable-ai-paper-trading-lab), [VerdictX](https://devpost.com/software/verdictx-institutional-ai-investment-committee), [Devil's Advocate](https://devpost.com/software/devil-s-advocate-ovw6lc)

### Inferences
- "Agents debating" on its own no longer wins. Visible persona debates with a synthesized verdict are common, and several polished examples went without prizes. What sets the winners apart is **evidence that the debate helps** (an accuracy delta or calibration) or **a sharp real-world stake with a human in charge**.
- Two blog-post awards (Split Decision, Decision Room) suggest a strong write-up about *what was learned from measuring the agents* is itself rewarded.
- For a Cisco/AGNTCY track, sponsor-tech depth matters: every SanD Hacks Multi-Agent Systems winner used AGNTCY components (see Q3).

### Gaps
- Judges' written rationales were not available. Reasons for winning are inferred from what each write-up emphasizes.

## Q3. Past Cisco Outshift / AGNTCY / Internet of Agents / Internet of Cognition hackathons and challenges, and any "When AI Agents Disagree" results

### Takeaway
The clearest precedent is **SanD Hacks 2026** (UCSD, Jan 31–Feb 1 2026). Its **"Multi-Agent Systems Challenge"** had 4 winners, each receiving a $150 Cisco store gift card per person plus a badge and certificate. All four winners were built on AGNTCY and CoffeeAGNTCY/Lungo components, and **none dealt with disagreement or debate**. No public "When AI Agents Disagree" challenge or results page was found. Outshift's own 2026 research, however, measures exactly the failure modes MAGI targets.

### Cited Findings
- SanD Hacks 2026 (CSES @ UCSD, 26 hours, about 90 participants) listed a "Multi-Agent Systems Challenge – 4 winners – $150 Cisco store gift card (per person) and eligible to a badge and certificate". The general judging criteria were Idea, Demo, Technical Complexity and Completion. — [SanD Hacks 2026](https://sand-hacks-2026.devpost.com/)
- The four winners of that challenge:
  - **Lungo+**: a competitive coffee marketplace on AGNTCY. A Scout agent probes farms in parallel with adaptive timeouts. A Market agent runs multi-round RFQ auctions weighted on price 40%, delivery 25%, quality 20% and performance 15%. It adds shared memory with a "Semantic Translator" between agent vocabularies and a playable "GameView". Built with LangGraph and ClickHouse. — [Devpost](https://devpost.com/software/lungo)
  - **Travel AGNTCY**: travel planning over the AGNTCY A2A protocol, NATS transport and agntcy-app-sdk, with OpenTelemetry, Grafana and ClickHouse observability. — [Devpost](https://devpost.com/software/travel-agyntc)
  - **Agntcity**: a multi-agent newsletter summarizing Moltbook agent chatter, built with AGNTCY, LangGraph and NATS. — [Devpost](https://devpost.com/software/agntcity)
  - **Execution-Aware Shipping Agent for CoffeeAGNTCY**: adds shipment caps and customs delays to the Lungo group-chat demo. — [Devpost](https://devpost.com/software/execution-aware-shipping-agent-for-coffeeagntcy)
- Devpost's hackathon search for "cisco" returns only older Cisco events (Meraki, DevNet, Spark, House of Hacking 2023). There are no Outshift or AGNTCY-branded hackathons on Devpost. — [Devpost hackathon search results, e.g. Cisco House of Hacking](https://cisco-house-of-hacking.devpost.com/)
- Outshift's AGNTCY activity in 2025–2026 consisted of an AGNTCY Summit 2025 and an AGNTCY Hands-on Lab in June 2026, which was a workshop and not a competition. — [Outshift AGNTCY Summit](https://outshift.cisco.com/events/agntcy-summit-2025); [Outshift Hands-on Lab](https://outshift.cisco.com/events/agntcy-handsonlab-june-2026)
- **Outshift's Mycelium results:** Vijoy Pandey's post of Jun 25 2026 reports that across 14 decision scenarios, "consensus jumped from 36% to 93%" with Mycelium goal rooms and a Cognition Engine that mediates structured negotiation ("agents propose, counter, and converge through a protocol rather than free-chatting"). On the five hardest scenarios, unstructured chat reached zero decisions. In the 22% of unstructured runs where agents "invented steps", Mycelium brought that to zero. These are company-reported figures. — [Outshift blog: connected to coordinated](https://outshift.cisco.com/blog/ai-ml/moving-multi-agent-systems-from-connected-to-coordinated)
- **Outshift's research on cognitive failures** (Sep 15 2026; Carofiglio, Ameur, Feltin et al.) found that "roughly half of debate sessions" in a decentralized multi-agent debate contain at least one cognitive failure. Debate accuracy measured 0.99 with no failure, 0.81 with two failure categories and 0.16 with three. "Verification collapse alone costs 87 accuracy points and leaves the five agents in unanimous agreement on a wrong answer 75% of the time." The authors describe agents that "agree for the wrong reasons". — [Outshift blog: cognitive challenges](https://outshift.cisco.com/blog/ai-ml/cognitive-challenges-in-multi-agent-systems)
- A CIO.com opinion piece (Ferrazzi and Smith, Sep 16 2026) frames the Internet of Cognition problem as agents that "interpret the same goal differently or optimize for competing objectives". It quotes Outshift's Papi Menon: "Agents don't align and they kind of tend to diverge." It mentions no hackathon. — [CIO](https://www.cio.com/article/4222319/connecting-ai-agents-was-only-the-beginning-now-they-need-to-think-together.html)
- The only hackathon write-up found that uses the phrase "When AI agents disagree" is the magi-system Devpost entry. — [Devpost: magi-system](https://devpost.com/software/magi-system)

### Inferences
- **Opportunity:** the previous Cisco multi-agent challenge winners were integration and plumbing demos (supply chain, travel, newsletter). A MAGI built *on AGNTCY* (A2A/SLIM messaging between independently running agents, plus agent identity and directory) that tackles disagreement directly would be new for this sponsor.
- **Pitch hook:** Outshift's own research says unstructured agents reach consensus 36% of the time and that unanimous wrong answers occur when verification collapses. MAGI's unanimity rule plus escalation could be framed as a direct answer to that research. It should *demonstrate* that it catches "agreement for the wrong reasons", for example with a planted-false-evidence test, rather than treating unanimity as success.

### Gaps
- No winners list, rules or results were found for any "When AI Agents Disagree" or "Build a Collective Intelligence" challenge before UCSC 2026. Searches of Outshift, Devpost and the web returned nothing.
- It is unknown whether Cisco ran similar challenges at other 2025–2026 hackathons (for example Cal Hacks, LA Hacks, HackDavis) that are not indexed under "AGNTCY" on Devpost.

## Q4. Patterns: which domains are common, overdone or rare?

### Takeaway
The overdone formats are the **two-agent pro/con plus judge** setup, **courtroom/jury** metaphors, **investment committees**, and **startup-idea validation panels**. Nearly all projects use a **central chair, judge, moderator or synthesizer** to decide. Rare elements are private information, baseline measurement, true unanimity, versioned proposals, live evidence injection, and principled stopping or escalation.

### Cited Findings
- **Pro/con plus judge, repeated since 2023:**
  - [DebateHub (2024)](https://devpost.com/software/debatehub)
  - [Devil's Advocate (2026)](https://devpost.com/software/devil-s-advocate-ovw6lc)
  - [Devil's Advocate and Jury (2026)](https://devpost.com/software/devil-s-advocate-and-jury)
  - [Gavel (2026)](https://devpost.com/software/fauxpas)
  - [BLUEPRINT (2026)](https://devpost.com/software/blueprint-ai-property-due-diligence)
  - [Counterfactual Financial Oracle (2025)](https://devpost.com/software/counterfactual-financial-oracle)
  - [GhostTrace (2026)](https://devpost.com/software/ghosttrace-jh5ws8)
  - The 2023 Kitchener hackathon had a dedicated "Best AI vs AI Debate" prize. — [AI Agents Hackathon 2023](https://ai-agents-hackathon.devpost.com/)
- **Courtroom/tribunal metaphors:**
  - [Split Decision](https://devpost.com/software/split-decision)
  - [JURO](https://devpost.com/software/juro)
  - [Small Claims Court](https://devpost.com/software/small-claims-court)
  - [VERDICT AI](https://devpost.com/software/verdict-ai)
  - [DAOCouncil](https://ethglobal.com/showcase/daocouncil-8d9k4)
  - [Jury](https://devpost.com/software/jury-abiehq)
  - [TriBunal](https://devpost.com/software/eco-governai)
  - Devpost search also shows Venture Jury, Genie Jury, Veritas.ai and the OMINI "AI courtrooms" (names and taglines only; not opened).
- **Investment committees and trading:**
  - [The Committee](https://devpost.com/software/the-committee-explainable-ai-paper-trading-lab)
  - [VerdictX](https://devpost.com/software/verdictx-institutional-ai-investment-committee)
  - [J^2](https://devpost.com/software/j-2)
  - [ProphETF](https://devpost.com/software/prophetf)
  - Devpost search also shows "Origin – Black-Box Arena" (Gemini hedge-fund agents debate), "bull-vs-bear" and an "AI powered investment discovery platform" (taglines only).
- **Startup or idea stress-testing:**
  - [AXIOM](https://devpost.com/software/axiom-the-cognitive-stress-test-engine)
  - [Jury](https://devpost.com/software/jury-abiehq)
  - [BoardSeat.dev](https://devpost.com/software/boardseat-dev)
  - [Decision Room](https://devpost.com/software/decision-room)
- **Medical/health:** JURO for insurance appeals; MedConsensus ("specialist AIs debate diagnoses"; tagline only, not opened); Bodify, a "council of AI specialists" health planner (winner badge seen in search JSON; not opened). — [JURO](https://devpost.com/software/juro); [Devpost search JSON, query "A2A agents debate"/"council"]
- **Central decider pattern:**
  - Supervisor (MAGI at UCI). — [MAGI](https://devpost.com/software/magi-lxb0ne)
  - Meta-Auditor. — [magi-system](https://devpost.com/software/magi-system)
  - Sovereign. — [The AI Council](https://devpost.com/software/the-ai-council)
  - Chairperson or Chairman. — [VerdictX](https://devpost.com/software/verdictx-institutional-ai-investment-committee); [The Committee](https://devpost.com/software/the-committee-explainable-ai-paper-trading-lab)
  - Summarizer. — [Council Tower](https://devpost.com/software/council-tower-pipeline-ai-deliberation-engine)
  - Adjudicator. — [JURO](https://devpost.com/software/juro)
  - Judge model. — [FactNews](https://devpost.com/software/consensus-tdv0el)
- **Majority vote rather than unanimity:**
  - [TriBunal](https://devpost.com/software/eco-governai)
  - [TheAgora](https://huggingface.co/spaces/Agents-MCP-Hackathon/TheAgora/blob/main/README.md)
  - The only unanimity rule found is in the non-hackathon magi-council ("on unanimous approval — it merges itself"). — [magi-council](https://github.com/Adrian-Sandwich/magi-council)
- **Rare domain examples:**
  - Constitutional law with ground truth. — [Split Decision](https://devpost.com/software/split-decision)
  - Carbon-aware AI routing. — [TriBunal](https://devpost.com/software/eco-governai)
  - Cybersecurity incident response. — [GhostTrace](https://devpost.com/software/ghosttrace-jh5ws8)
  - DAO governance. — [DAOCouncil](https://ethglobal.com/showcase/daocouncil-8d9k4)
  - Group social planning with private constraints. — [unsaid](https://devpost.com/software/unsaid-zm8w5v)
  - News consensus and contested facts. — [FactNews](https://devpost.com/software/consensus-tdv0el)

### Inferences
- Choosing a courtroom or investment-committee demo domain would put MAGI in the most crowded lanes. Good alternatives: open-ended policy or safety trade-offs (fits MAGI's science/ethics/practical split), incident response, and resource-allocation decisions with competing objectives and checkable outcomes.
- Using a central synthesizer would break the Level 3 "no central decider" requirement, and most competitors use one. MAGI's unanimity among peers plus human escalation is a real structural difference if the orchestrator only enforces protocol rules and never picks a winner. This is the same "LLM = semantics, code = rules" stance as jamespud/MAGI-system.

### Gaps
- Domain counts are qualitative. No systematic tally across all ~3,500 search hits was made.

## Q5. What did no project do that MAGI could do?

### Takeaway
No hackathon project found combines **(1) a controlled baseline comparison, (2) mid-debate evidence injection with tracked belief change, (3) unanimity on versioned concrete proposals with a round cap and human escalation, (4) private or asymmetric information, and (5) manipulation or sycophancy-resistance tests**. Each item appears at most in isolation: Split Decision has the baseline, unsaid has private information, JURO and magi-council have the human ruling, and Devil's Advocate has referee-ruled stopping.

### Cited Findings
- **Baseline comparison is rare.** Only Split Decision runs explicit arms: single model vs silent vote vs deliberation vs a neutral control. ProphETF back-tested its panel and disclosed coin-flip accuracy, and OracleFlow calibrated against resolved markets. — [Split Decision](https://devpost.com/software/split-decision); [ProphETF](https://devpost.com/software/prophetf); [OracleFlow](https://devpost.com/software/ai-forecasting-track)
- **Mid-debate evidence injection:** the closest features are The AI Council's "Manual / Intervention Mode" (pause or steer) and Devil's Advocate's post-verdict user "Challenge". Neither measures how positions shift in response to *new evidence*. — [The AI Council](https://devpost.com/software/the-ai-council); [Devil's Advocate](https://devpost.com/software/devil-s-advocate-ovw6lc)
- **Stopping and escalation:**
  - Devil's Advocate continues only "while a referee rules the disagreement still live". — [Devil's Advocate](https://devpost.com/software/devil-s-advocate-ovw6lc)
  - JURO always has a human deliver the ruling. — [JURO](https://devpost.com/software/juro)
  - Council Tower uses a fixed 5-phase protocol with a LOCK step. — [Council Tower](https://devpost.com/software/council-tower-pipeline-ai-deliberation-engine)
  - MOD may "fork" instead of converging. — [MOD](https://devpost.com/software/mod-mixture-of-dulus)
  - None found escalates to a human *only after N failed unanimity rounds*. magi-council has "human arbitration" but is not a hackathon project. — [magi-council](https://github.com/Adrian-Sandwich/magi-council)
- **Preserving disagreement:**
  - Split Decision files dissents. — [Split Decision](https://devpost.com/software/split-decision)
  - TheAgora logs disagreements. — [TheAgora](https://huggingface.co/spaces/Agents-MCP-Hackathon/TheAgora/blob/main/README.md)
  - The Committee exposes "dissent". — [The Committee](https://devpost.com/software/the-committee-explainable-ai-paper-trading-lab)
  - FactNews highlights "contested facts". — [FactNews](https://devpost.com/software/consensus-tdv0el)
  - magi-council keeps a "minority report". — [magi-council](https://github.com/Adrian-Sandwich/magi-council)
  - None reports a structured "irreducible disagreement" outcome as a first-class deliverable alongside the human hand-off.
- **Versioned proposals:** the only versioning found is Jury's "cited, versioned record of the beliefs your idea depends on". No project has agents vote on numbered proposal versions (v1 → v2 → v3) with diffs. — [Jury](https://devpost.com/software/jury-abiehq)
- **Private information and competing objectives:** only unsaid isolates each agent's private constraints ("Each agent sees only its own person"). — [unsaid](https://devpost.com/software/unsaid-zm8w5v)
- **Manipulation or sycophancy resistance:**
  - Devil's Advocate tells the judge the user's argument "carries no authority" from having started the debate. — [Devil's Advocate](https://devpost.com/software/devil-s-advocate-ovw6lc)
  - Devil's Advocate and Jury penalizes fabricated citations. — [Devil's Advocate and Jury](https://devpost.com/software/devil-s-advocate-and-jury)
  - syro rewards correctness over popularity ("Agreeing isn't being right"). — [syro](https://devpost.com/software/syro)
  - No project tests whether agents hold their position against a planted bad-faith agent, false evidence, or social pressure. Outshift's research shows unanimous wrong answers in 75% of verification-collapse cases. — [Outshift cognitive challenges](https://outshift.cisco.com/blog/ai-ml/cognitive-challenges-in-multi-agent-systems)
- **Model diversity:** some projects mix model families to avoid shared bias, notably MAGI at UCI (Claude, Mistral, Nova, Command R+) and MOD (Claude, GPT, Gemini, Kimi, DeepSeek). None measures whether diversity changes outcomes. — [MAGI](https://devpost.com/software/magi-lxb0ne); [MOD](https://devpost.com/software/mod-mixture-of-dulus)
- **Per-agent tools that differ by role:** some projects give agents tools or retrieval (MOD tool access, BLUEPRINT per-source FunctionTools, Consilium's research agent), but no debate project gives each *perspective* its own toolset tied to its objective. Evidence tools for the scientist, risk and policy lookups for the ethicist, and cost or feasibility tools for the pragmatist would be new. — [MOD](https://devpost.com/software/mod-mixture-of-dulus); [BLUEPRINT](https://devpost.com/software/blueprint-ai-property-due-diligence); [Consilium](https://huggingface.co/spaces/Agents-MCP-Hackathon/consilium_mcp/raw/main/README.md)
- **AGNTCY-native debate:** no debate or council project built on AGNTCY was found. The AGNTCY winners were coordination and marketplace demos. — [SanD Hacks winners: Lungo+](https://devpost.com/software/lungo), [Travel AGNTCY](https://devpost.com/software/travel-agyntc), [Agntcity](https://devpost.com/software/agntcity)

### Inferences
Gaps MAGI could exploit, ranked by expected judging impact for the Cisco Level 3 brief:
1. **A measured baseline with a control arm**, as in Split Decision. Compare a single LLM, three agents voting independently with no debate, and full MAGI deliberation on a small labeled question set or checkable decisions. Report the accuracy or quality delta *and* the cost and latency delta honestly, as ProphETF did.
2. **An "inject new evidence" button with a belief-change trace**: per-agent position and confidence before and after, the proposal version bump, and whether the injection broke or created unanimity. No project shows this.
3. **A false-consensus or manipulation stress test**: inject planted false evidence or a sycophantic pressure message and show that MAGI's agents verify it before agreeing. This addresses Outshift's own "agree for the wrong reasons" finding directly.
4. **Unanimity, round cap, escalation and preserved disagreement as a first-class output**: show the unresolved crux, each agent's last position and the proposal diff history. That differs clearly from chair-decides projects and from majority-vote MAGI clones.
5. **Asymmetric or private information per agent** (as in unsaid) to make the "competing objectives" real rather than persona-deep.
6. **AGNTCY-native distribution**: each MAGI unit as a separately addressable agent with identity and directory entries communicating over A2A/SLIM. This is new among debate projects and fits the sponsor's stack.

### Gaps
- A missing project in this sample does not prove no hackathon project has a given feature. Devpost descriptions are self-reported, and many projects were seen only as taglines.
- Hugging Face Spaces and ETHGlobal were sampled lightly: TheAgora, Consilium and the DAOCouncil family. The ETHGlobal showcase also has AI-DAO-President, Minerva, AutoVote and DAAO (governance-voting agents), seen only via search snippets. — [ETHGlobal AI-DAO-President](https://ethglobal.com/showcase/ai-dao-president-bm0ib); [Minerva](https://ethglobal.com/showcase/minerva-bhi46); [AutoVote](https://ethglobal.com/showcase/autovote-ieaxr)
