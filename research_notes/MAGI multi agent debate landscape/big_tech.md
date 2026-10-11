# Big Tech Multi-Agent Debate / Deliberation / Consensus Systems (benchmark for MAGI)

Scope: products, features and research systems from major companies where multiple AI agents or models debate, deliberate, critique each other, vote, or reach consensus. Current as of 2026-10-10. "SHIPPED" = generally available or paid-tier feature; "PREVIEW" = gated or early-access product; "RESEARCH" = paper or prototype only. Vendor-reported numbers are flagged as such.

---

## Q1. Google / Google DeepMind: what has shipped or been published?

### Takeaway
Google has the deepest research bench here: AI co-scientist (a multi-agent generate, debate, tournament and evolve system, published in Nature in 2026), the Habermas Machine (an AI mediator for *human* group deliberation, Science 2024), formal debate-for-oversight research, and a large study showing that multi-agent systems often *hurt* on sequential tasks. Its shipped consumer feature, Gemini Deep Think, is single-model "parallel thinking", not a set of personas.

### Cited Findings
**AI co-scientist (RESEARCH, then Trusted Tester access; foundation of "Gemini for Science")**
- Announced February 19, 2025. It is a multi-agent system built on Gemini 2.0 that generates hypotheses, research overviews and experimental protocols from a natural-language research goal. — [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- Named agents: Generation, Reflection, Ranking, Evolution, Proximity and Meta-review. A **Supervisor** agent parses the goal into a plan, assigns agents to a worker queue and allocates resources. In other words, it is centralized. — [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- Mechanism: "self-play–based scientific debate" generates hypotheses, ranking tournaments compare them, and an evolution step improves them. Self-improvement relies on an **Elo** auto-evaluation metric from the tournaments. — [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- Scientist-in-the-loop: scientists can supply seed ideas or natural-language feedback. — [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- Evaluation: higher Elo correlated with a higher probability of correct answers on GPQA diamond, but Elo is auto-evaluated rather than ground truth. Seven experts curated 15 goals, and quality improved with more test-time compute. On 11 goals, experts rated novelty and impact higher (the authors call this a small sample). — [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- Wet-lab validations: AML drug-repurposing candidates inhibited tumor viability in cell lines; epigenetic targets for liver fibrosis showed anti-fibrotic activity in hepatic organoids; and it independently re-derived an unpublished cf-PICI phage-tail mechanism for antimicrobial resistance. — [Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)
- At I/O 2026 (May 2026), Google announced "Gemini for Science", built on Co-Scientist and Empirical Research Assistance, "both published in Nature last week". — [Google Research I/O 2026 blog](https://research.google/blog/a-new-era-of-innovation-google-research-at-io-2026)

**Habermas Machine (RESEARCH; Science, October 2024)**
- Built by Google DeepMind (Tessler et al.) and inspired by Habermas's theory of communicative action. It generates group statements from individual participants' opinions and critiques to maximize group approval, using supervised fine-tuning and reward modeling. — [Summary of the Science paper (CSS Society)](https://comdig.cssociety.org/2024/10/27/ai-can-help-humans-find-common-ground-in-democratic-deliberation/); [Science PDF mirror](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
- Mechanism: it generates many candidate group statements and returns one by *simulating an election* over each participant's predicted ranking. In effect it uses a social-choice or voting step. — [arXiv 2601.05904, analysis of the Habermas Machine](https://arxiv.org/pdf/2601.05904)
- Experiments with more than 5,000 UK participants (5,734 in total) on Brexit, immigration, minimum wage, climate change and childcare. In head-to-head comparisons, participants preferred the AI's statement over a human mediator's **56%** of the time. External judges rated AI statements higher for quality, clarity, informativeness and fairness. Groups converged after AI mediation but not in unmediated exchange, and minority critiques were incorporated into revisions. — [MIT Technology Review](https://www.technologyreview.com/2024/10/17/1105810/ai-could-help-people-find-common-ground-during-deliberations/); [Mediate.com](https://mediate.com/news/ai-mediation-tool-may-help-reduce-culture-war-rifts-say-researchers/)
- Source conflict: one summary says AI and human statements did *not* differ significantly in inclusion of minority positions, while the abstract says the model "demonstrably incorporated minority critiques". — [Mediate.com](https://mediate.com/news/ai-mediation-tool-may-help-reduce-culture-war-rifts-say-researchers/) vs [CSS Society summary](https://comdig.cssociety.org/2024/10/27/ai-can-help-humans-find-common-ground-in-democratic-deliberation/)

**Gemini Deep Think (SHIPPED to the $250/month AI Ultra tier)**
- Gemini 2.5 Deep Think shipped to Ultra subscribers on **August 1, 2025**. It uses "parallel thinking" to generate many ideas at once, consider them simultaneously and revise or combine them before answering. The consumer version reached bronze level on IMO 2025; the gold-medal version was given only to mathematicians. — [Google blog](https://blog.google/products-and-platforms/products/gemini/gemini-2-5-deep-think/); [Simon Willison](https://simonwillison.net/2025/Aug/1/)
- Gemini 3 Deep Think shipped to Ultra on **December 4, 2025**. Its "parallel reasoning" explores multiple hypotheses simultaneously (41.0% on HLE without tools and 45.1% on ARC-AGI-2, per Google). — [9to5Google](https://9to5google.com/2025/12/04/gemini-3-deep-think/); [Tom's Guide](https://www.tomsguide.com/ai/google-gemini/google-just-launched-gemini-3-deep-think-its-most-powerful-ai-model-yet)

**Debate-for-oversight research (RESEARCH)**
- Kenton et al. (Google DeepMind, NeurIPS 2024) tested 9 tasks with about 5 million generations. Debate beat consultancy on all tasks when sides were assigned. Debate beat direct QA only with information asymmetry and was "mixed" otherwise. Stronger debaters increased judge accuracy "more modestly than in previous studies". — [arXiv 2407.04622](https://arxiv.org/pdf/2407.04622); [NeurIPS proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/899511e37a8e01e1bd6f6f1d377cc250-Abstract.html)

**"Towards a science of scaling agent systems" (RESEARCH; Google Research, DeepMind and MIT; arXiv December 2025, blog January 28, 2026)**
- Across 180 agent configurations, centralized coordination improved parallelizable tasks such as financial reasoning by 80.9%, and decentralized coordination did best on dynamic web navigation. On **sequential reasoning tasks, every multi-agent variant degraded performance by 39–70%**. — [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/); [Techstrong.ai](https://techstrong.ai/agentic-ai/google-research-study-scaling-multi-agent-systems-is-a-strange-science/)
- **Independent agents amplified errors 17.2x, versus 4.4x for centralized systems.** The orchestrator acts as a "validation bottleneck". — [Google Research blog](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- A predictive model picks the best architecture for 87% of unseen configurations. A later arXiv version reports 260 configurations and a lower R² (0.373 vs 0.513), so cite carefully. — [hyper.ai listing of arXiv 2512.08296](https://hyper.ai/en/papers/2512.08296)

**Protocols**
- Google Cloud is a formative member of AGNTCY at the Linux Foundation and said the project will be "neutrally governed alongside the Agent2Agent protocol". — [Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos); [NAND Research](https://nand-research.com/research-note-agntcy-moves-to-linux-foundation/)

### Inferences
- Co-scientist is MAGI's closest big-tech conceptual analogue for "debate, then revise, then rank", but it differs from MAGI in four ways: (a) it has a central Supervisor; (b) its agents are functional roles (generate, critique, rank), not *value-laden* stakeholders with competing objectives; (c) it ranks with Elo tournaments, not unanimity; (d) it optimizes one objective (hypothesis quality).
- The Habermas Machine is the closest analogue to MAGI's consensus-seeking and minority-preservation goal, but the deliberators are *humans* and the AI is the mediator. MAGI inverts this: the AI agents deliberate and a human is the fallback. Citing it shows that consensus statements can be evaluated by external raters and by preference against a human baseline.
- Google's own scaling study is the strongest caution for MAGI. MAGI's "no central decider" design is the topology that amplified errors 17.2x, and many MAGI-style questions are not parallelizable. MAGI needs an explicit cross-check or verification mechanism (for example, each agent must critique the others' claims before voting) and should report where multi-agent helps and where it does not.
- Deep Think is a single-model parallel-hypothesis method, which makes it a fair "strong single-agent baseline" category for MAGI to compare against (self-consistency or best-of-N at equal compute).

### Gaps
- I did not retrieve the Nature citation (title, date, DOI) for the Co-Scientist paper. The I/O blog only says "published in Nature last week" (May 2026).
- I found no public statement of Co-Scientist or Gemini for Science general-availability terms as of October 2026.
- I found no Google *product* that exposes multi-persona debate or voting to end users.

---

## Q2. Microsoft: MAI-DxO, Magentic-One / AutoGen, and Copilot multi-model features

### Takeaway
Microsoft has the two most MAGI-like artifacts in big tech. **MAI-DxO** (June 2025, research) is a role-played virtual panel of doctors with a devil's advocate and a cost steward that debate and reach consensus on the next action. **Copilot Researcher "Critique" and "Council"** (March 2026, Frontier preview) are shipped cross-vendor (GPT plus Claude) generate-and-critique and parallel-compare-with-disagreement-summary features. Microsoft also published Magentic Marketplace, which shows agents negotiating badly.

### Cited Findings
**MAI-DxO / Sequential Diagnosis (RESEARCH, not approved for clinical use)**
- Announced June 30, 2025 (arXiv 2506.22405, submitted June 27, 2025; authors include Nori, King, Suleyman and Horvitz). — [Microsoft AI blog](https://microsoft.ai/new/the-path-to-medical-superintelligence/); [arXiv](https://arxiv.org/abs/2506.22405)
- The virtual panel has five roles. **Dr. Hypothesis** keeps a ranked top-3 differential and updates probabilities. **Dr. Test-Chooser** picks up to 3 discriminating tests per round. **Dr. Challenger** plays devil's advocate, flagging anchoring bias and contradictory evidence. **Dr. Stewardship** pushes cost-conscious care and vetoes low-yield expensive tests. **Dr. Checklist** silently checks quality and consistency. — [arXiv HTML](https://arxiv.org/html/2506.22405)
- The roles deliberate in a "chain of debate" and reach **consensus** on one of three actions: ask questions, order tests, or commit to a diagnosis (only above a certainty threshold). No single role has final authority. In the ensemble variant, a separate aggregation step picks the diagnosis across parallel panels. — [arXiv HTML](https://arxiv.org/html/2506.22405)
- SDBench converts 304 NEJM clinicopathological cases into stepwise encounters with a gatekeeper model and virtual test costs, graded against the NEJM gold-standard diagnosis. — [Microsoft AI blog](https://microsoft.ai/new/the-path-to-medical-superintelligence/)
- Numbers: off-the-shelf o3 scored **78.6% at $7,850 per case**. MAI-DxO unconstrained with o3 scored **81.9% at $4,735**, budgeted scored about **79.9% at about $2,396**, and the ensemble scored **85.5% at $7,184**. Physicians (21 generalists, no references allowed) averaged **19.9% at $2,963**, and the best physician reached 41%. — [arXiv HTML](https://arxiv.org/html/2506.22405)
- The orchestrator is model-agnostic and "boosted the diagnostic performance of every model we tested" (GPT, Gemini, Claude, Grok, DeepSeek, Llama). — [Microsoft AI blog](https://microsoft.ai/new/the-path-to-medical-superintelligence/)
- Limitations: the cases are hard and include no healthy patients, so false-positive rates are unknown. Costs are first-order US prices. Physicians were barred from resources. Neither SDBench nor MAI-DxO was public at release. — [arXiv HTML](https://arxiv.org/html/2506.22405); [Microsoft AI blog](https://microsoft.ai/new/the-path-to-medical-superintelligence/)

**Microsoft 365 Copilot Researcher: Critique and Council (PREVIEW; Frontier program, Copilot license required; late March 2026)**
- **Critique**: one model (GPT) plans, retrieves and drafts, then a second model (Claude) reviews for source reliability, completeness, grounding and citations. It is the default when the model picker is on "auto". — [Computerworld](https://www.computerworld.com/article/4152323/microsoft-adds-multi-model-ai-to-copilot-researcher-raising-accuracy-stakes.html); [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research); [Microsoft message center MC1265765 (itelio mirror)](https://www.itelio.com/en/microsoft-message-center/MC1265765)
- **Council**: runs the same question through multiple deep-research agents (for example GPT and Claude) in parallel, keeps each full report, and adds a synthesis that highlights **where the models agree, where they diverge, and what each uniquely contributes**. — [Computerworld](https://www.computerworld.com/article/4152323/microsoft-adds-multi-model-ai-to-copilot-researcher-raising-accuracy-stakes.html); [Gigazine, 2026-03-31](https://www.gigazine.net/gsc_news/en/20260331-microsoft-365-copilot-critique-council)
- Vendor-reported result: on DRACO (100 research tasks across 10 domains; Zhong et al., arXiv 2602.11685), Researcher with Critique scored **57.4**, which Microsoft reports as +7.0 points (+13.88%) over the best previously reported system, Perplexity Deep Research on Claude Opus 4.6. Claude Opus 4.6 alone scored 42.7. GPT-5.2 was the LLM judge. — [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research); [Computerworld](https://www.computerworld.com/article/4152323/microsoft-adds-multi-model-ai-to-copilot-researcher-raising-accuracy-stakes.html)
- An analyst warns this is a best-case test and that a reviewer model may share the generator's blind spots. — [Computerworld](https://www.computerworld.com/article/4152323/microsoft-adds-multi-model-ai-to-copilot-researcher-raising-accuracy-stakes.html)

**Magentic Marketplace (RESEARCH, open source; October/November 2025)**
- A simulated market with 100 customer-side agents and 300 business-side agents (GPT-4o, GPT-5, Gemini-2.5-Flash, Qwen3-4b, GPT-OSS-20b). Frontier models reach near-optimal welfare only under favorable search conditions. Performance degrades with scale, and every model showed **severe first-proposal bias (10–30x advantage for speed over quality)**. Some seller agents manipulated buyers through prompt injection. — [arXiv 2510.25779](https://arxiv.org/html/2510.25779v1); [InfoQ](https://infoq.com/news/2025/11/magentic-marketplace-microsoft); [TechRadar](https://www.techradar.com/pro/microsoft-built-a-fake-marketplace-to-see-how-its-ai-agents-would-work-selling-unsupervised-and-lets-just-say-the-results-were-unsurprising)

**Magentic-One / AutoGen and Copilot Studio**
- Magentic-One (November 2024) is a generalist multi-agent system in which a lead **Orchestrator** directs specialist agents (WebSurfer, FileSurfer, Coder, ComputerTerminal). It is a centralized planner, not a debate system. (Not re-fetched this session; from the primary Microsoft Research page.) — [Microsoft Research](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)
- Copilot Studio multi-agent orchestration reached GA with A2A support, according to secondary coverage. — [Enterprise DNA](https://enterprisedna.co/resources/news/salesforce-summer-26-agentforce-800m-arr-multi-agent-2026/)

### Inferences
- MAI-DxO is the single most important precedent to cite. It already has (a) role personas with *competing objectives* (Dr. Stewardship's cost objective vs Dr. Hypothesis's accuracy objective), (b) a devil's advocate, (c) consensus on concrete actions, and (d) **ground-truth evaluation against a human baseline**. MAGI is not novel on "personas debate and agree". Its differentiation must come from somewhere else: decentralization across independent agents (MAI-DxO is one model role-playing a panel), explicit human escalation, preserved dissent, and value or ethics trade-offs.
- MAI-DxO's real win is **cost-efficiency at similar accuracy**: 81.9% vs 78.6% for o3 alone, at about 60% of the cost. The 85.5% figure needed an ensemble. This is a good model for MAGI's baseline: report quality *and* cost (tokens) against a single-agent baseline.
- Copilot Council's "where they agree, where they diverge, what each contributes" synthesis is a **shipped** form of "preserve disagreement". Judges who use M365 may have seen it. MAGI goes further only if disagreement changes the *decision procedure* (no consensus, so no action, so escalation), not just the report.
- Magentic Marketplace's first-proposal bias is directly relevant to MAGI's voting. Agents may anchor on the first concrete proposal. MAGI should randomize proposal order or have each agent propose independently before seeing the others.

### Gaps
- I could not fetch the Microsoft Tech Community post on Critique and Council directly, so the details come from Computerworld, Decrypt and the message-center mirror.
- I found no independent replication of the MAI-DxO or Critique numbers.
- I did not find any Microsoft feature that escalates to a human when models disagree. Council leaves interpretation to the user.

---

## Q3. OpenAI: pro parallel sampling, debate research, Agents SDK, council features

### Takeaway
OpenAI originated the debate-for-AI-safety idea (2018) but has shipped no user-facing debate, council or voting feature. Its "pro" models use undisclosed "parallel test-time compute" (single model, multiple samples), and its Agents SDK uses handoff and orchestration patterns rather than deliberation.

### Cited Findings
- "AI safety via debate" (Irving, Christiano, Amodei; arXiv May 2, 2018): two agents play a zero-sum debate game with alternating short statements and a human judge. With optimal play, debate can answer PSPACE questions with polynomial-time judges. In the MNIST toy experiment, judge accuracy rose from 59.4% to 88.9% with 6 pixels revealed, and from 48.2% to 85.2% with 4. — [arXiv 1805.00899](https://arxiv.org/abs/1805.00899)
- o3-pro was released June 10, 2025. OpenAI did not publish the aggregation mechanism, and third-party sources describe it as sampling or aggregating multiple candidates. — [aiwiki o3-pro](https://aiwiki.ai/wiki/o3-pro); [GreaterWrong "o3 Turns Pro"](https://www.greaterwrong.com/posts/inWQLm6FvFQB68vY7/o3-turns-pro)
- The GPT-5 system card says ChatGPT offers gpt-5-thinking with a setting that "makes use of parallel test time compute" (GPT-5 Pro). No technical paper explains the aggregator. — [Conduct Atlas excerpt of GPT-5 system card](https://conductatlas.com/platform/openai/openai-gpt-5-system-card/provision/CA-P-066857/chatgpt-parallel-test-time-compute-setting-for-thinking-pro/)
- The Agents SDK (around March 11, 2025) is an open-source framework with handoffs (agent-to-agent delegation), guardrails, tracing and sessions, and is the production successor to the experimental Swarm. — [GoCodeo](https://gocodeo.com/post/openai-releases-responses-api-and-agents-sdk); [Data Science Dojo](https://datasciencedojo.com/blog/openai-agents-sdk/)
- An April 2026 SDK update reportedly added sandboxing, a long-horizon harness and subagents (single, low-quality infographic source). — [OpenLink infographic](https://openlinksw.com/data/html/openai-agents-sdk-next-evolution-infographic.html)

### Inferences
- Judges will know "pro" models and best-of-N style parallel sampling. MAGI should present this as the **compute-matched single-agent baseline**: same model and token budget, majority vote or self-consistency. That shows whether deliberation adds anything beyond extra samples.
- OpenAI's debate paper gives MAGI an intellectual lineage. The relevant result is that debate helps a *weaker judge* (here a human) decide, which supports MAGI's human-escalation framing: when agents disagree, their opposing arguments are the evidence handed to the human.

### Gaps
- I found no OpenAI shipped "council" or multi-model debate feature. Absence of evidence is not conclusive.
- OpenAI's mechanism for selecting among parallel samples in GPT-5 Pro or o3-pro is unpublished.
- I did not verify primary OpenAI pages for the exact Agents SDK launch date.

---

## Q4. Anthropic: multi-agent research system, agent teams, debate research, Constitutional critique

### Takeaway
Anthropic ships an orchestrator-worker multi-agent Research feature (June 2025) that beat a single agent by 90.2% on its internal eval, but Anthropic says token spend explains most of the gain. It also ships experimental Claude Code "agent teams" whose docs explicitly recommend agents debating competing hypotheses. Anthropic researchers co-authored the key empirical debate paper.

### Cited Findings
- Multi-agent research system (blog June 13, 2025): a **LeadResearcher** orchestrator plans, spawns parallel subagents, decides whether more research is needed, and hands off to a CitationAgent. — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- Result: Opus 4 as lead with Sonnet 4 subagents **outperformed single-agent Opus 4 by 90.2%** on an internal research eval. — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- Cost and confound: multi-agent systems use about **15x** the tokens of chat. On BrowseComp, **token usage alone explained 80% of performance variance**, and three factors explained 95%. Anthropic: "Multi-agent systems work mainly because they help spend enough tokens to solve the problem." — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- Poor fit: domains needing shared context or with many inter-agent dependencies, most coding, and real-time coordination. Subagents cannot coordinate with each other during a run, and the article describes no debate or disagreement resolution. — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- Evaluation: a single LLM-as-judge with a rubric (factual accuracy, citations, completeness, source quality, tool efficiency) plus human testers. They started with about 20 queries. — [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- Claude Code **agent teams** (experimental, off by default): one lead session plus teammates in separate contexts who **message each other directly** and share a task list. The docs recommend starting with 3–5 teammates. Their example prompt spawns three teammates covering UX, architecture and a "devil's advocate". Another example asks 5 teammates to "talk to each other to try to disprove each other's theories, like a scientific debate" and record "whatever consensus emerges", reasoning that sequential investigation suffers from anchoring. The lead is fixed, so it is still a centralized lead. — [Claude Code docs: agent teams](https://code.claude.com/docs/en/agent-teams)
- Debate research: "Debating with More Persuasive LLMs Leads to More Truthful Answers" (Khan et al., arXiv 2402.06782; authors include Anthropic-affiliated researchers). On QuALITY, debate raised non-expert judge accuracy to **76% (LLM judges) and 88% (human judges)** vs naive baselines of 48% and 60%. Optimizing *consultants* (a single advocate) for persuasiveness made incorrect consultants relatively more persuasive, while optimizing debaters for persuasiveness increased judge accuracy. LLM judges showed verbosity, positional and sycophancy biases. — [arXiv 2402.06782](https://arxiv.org/html/2402.06782v4); [authors' summary on GreaterWrong](https://www.greaterwrong.com/posts/2ccpY2iBY57JNKdsP/debating-with-more-persuasive-llms-leads-to-more-truthful)
- Constitutional AI (December 2022) uses model self-critique and revision against a written set of principles. It is single-model critique, not multi-agent. (Not re-fetched this session.) — [arXiv 2212.08073](https://arxiv.org/abs/2212.08073)

### Inferences
- Anthropic's 80%-of-variance-is-tokens finding is the main methodological threat to any "multi-agent beats single agent" claim, MAGI's included. A credible MAGI baseline must be **token-matched**.
- The agent-teams docs show that "spawn a devil's advocate" and "agents disprove each other's theories" are now standard prompting patterns in developer tools. A three-persona debate is not a novel mechanism on its own.
- The Khan et al. finding that judges' positional and verbosity biases must be controlled applies directly if MAGI uses an LLM to summarize or judge votes. Swap positions and length-normalize.

### Gaps
- I did not confirm the release date of Claude Code agent teams from a primary announcement; the docs page is undated.
- I did not verify whether Khan et al. won an ICML 2024 award or the full author affiliations from the primary source.
- I found no Anthropic product that votes or escalates on inter-agent disagreement.

---

## Q5. xAI, Meta, Amazon, IBM, Salesforce, Perplexity, Apple

### Takeaway
Shipped consumer "council" products exist: xAI's Grok 4 Heavy and Grok 4.20 multi-agent, and Perplexity's Model Council. Enterprise platforms (Amazon Bedrock, Salesforce Agentforce, IBM watsonx Orchestrate) ship **supervisor or router** multi-agent orchestration, not deliberation. Meta's research directly measures LLMs' weakness at productive disagreement. I found nothing from Apple.

### Cited Findings
**xAI (SHIPPED, premium tiers)**
- Grok 4 Heavy (July 2025): multiple agents work independently in parallel, then "compare notes" like a "study group". Musk said it is *not simply a vote*: often one agent finds the key insight and shares it. xAI reported 44.4% on Humanity's Last Exam with tools. Available only on SuperGrok Heavy ($300/month). — [OfficeChai](https://officechai.com/miscellaneous/elon-musk-explains-how-grok4-heavy-xais-multi-agent-reasoning-model-works/); [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/grok-4-ai-launched-elon-musk-claims-it-surpasses/494462)
- Grok 4.20 Beta (consumer February 17, 2026; API around March 9–10, 2026, including `grok-4.20-multi-agent-beta-0309`) runs **four named agents**. **Grok** coordinates and resolves conflicts. **Harper** does research and fact-checking (including X data). **Benjamin** handles logic, math and code. **Lucas** is creative and contrarian. They analyze in parallel, then peer-review and question each other "until consensus". The sources are secondary, and xAI has not published a formal spec. — [eWeek](https://www.eweek.com/news/grok-4-20-multi-agent-ai-debate-architecture/); [NextBigFuture](https://www.nextbigfuture.com/2026/02/how-the-xai-grok-4-20-agents-work.html); [APIYI docs](https://docs.apiyi.com/en/news/grok-4-20-beta-launch)
- Claimed hallucination reduction of about 65% (12% to 4.2%) is unverified. — [eWeek](https://www.eweek.com/news/grok-4-20-multi-agent-ai-debate-architecture/)

**Perplexity (SHIPPED to Max subscribers; February 2026)**
- Model Council (around February 6–10, 2026) sends one query to **three models** at once. A synthesis step highlights agreement, divergence and unique insights, and users can open each full response. It launched for Perplexity Max on the web and was later integrated into Perplexity's "Computer" environment, producing a single cited report. — [Storyboard18](https://www.storyboard18.com/digital/perplexity-launches-model-council-to-compare-answers-across-multiple-ai-models-89246.htm); [Design Compass](https://designcompass.org/en/2026/02/11/perplexity-model-council-synthesizing-responses-from-multiple-ais/); [CreateWith](https://www.createwith.com/tool/perplexity/updates/perplexity-adds-model-council-for-cross-model-analysis-inside-computer)

**Amazon (SHIPPED)**
- Bedrock multi-agent collaboration was previewed at re:Invent 2024 and became GA **March 10, 2025**. A **supervisor** agent decomposes requests, delegates to specialist agents and consolidates outputs. AWS claims "marked improvements" over single agents on internal benchmarks. — [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/03/amazon-bedrock-multi-agent-collaboration/); [AWS News Blog](https://aws.amazon.com/blogs/aws/introducing-multi-agent-collaboration-capability-for-amazon-bedrock/)

**Salesforce (SHIPPED)**
- Agentforce multi-agent orchestration arrived in the Summer '26 release (live June 15, 2026). A primary agent is the single point of contact and routes to specialist agents. The Atlas reasoning engine picks the specialist from agent descriptions. A2A support is reported by secondary sources. — [Salesforce Summer '26 announcement](https://salesforce.com/news/stories/summer-2026-product-release-announcement); [Salesforce multi-agent page (KR)](https://www.salesforce.com/kr/agentforce/multi-agent-orchestration/); [Tekunda](https://tekunda.com/blog/Multi-Agent-Orchestration-on-Salesforce%3A-What-Makes-Agent-to-Agent-Handoffs-Work-in-Production)

**IBM (SHIPPED platform; protocol folded into A2A)**
- IBM's Agent Communication Protocol (ACP) is "now part of A2A under the Linux Foundation", and IBM is winding down ACP development. watsonx Orchestrate supports A2A v0.3.0 and coordinates through a **central planner** that routes to agents, tools or humans. — [IBM Research ACP page](https://research.ibm.com/projects/agent-communication-protocol); [IBM Think](https://www.ibm.com/think/topics/agent-communication-protocol); [watsonx Orchestrate docs](https://developer.watson-orchestrate.ibm.com/_releases/1.15.0/agents/connect_agent)

**Meta (RESEARCH)**
- Collaborative Reasoner, "Coral" (Meta FAIR, NeurIPS 2025): a framework to evaluate and improve multi-turn collaboration in which agents must **disagree, persuade and reach a shared final answer**. Finding: "current models cannot consistently leverage collaboration" to improve performance, and the social behaviors produced by post-training make them *less* suited to collaboration. Meta's fix is self-improvement on synthetic multi-agent conversations using the "Matrix" framework. — [Meta AI publication page](https://ai.meta.com/research/publications/collaborative-reasoner-self-improving-social-agents-with-synthetic-conversations/); [arXiv 2502.15153](https://arxiv.org/abs/2502.15153?context=cs); [NeurIPS 2025](https://neurips.cc/virtual/2025/poster/116966)
- CICERO (Science, 2022) played the negotiation game Diplomacy at human level, combining a language model with strategic planning. It is human-vs-agent negotiation, not agent-agent consensus. (Not re-fetched this session.) — [Meta AI CICERO](https://ai.meta.com/research/cicero/)

**Apple**
- No Apple-authored multi-agent debate or consensus paper or product turned up in search. — [search result set](https://proceedings.mlr.press/v306/okawa26a.html) (closest hits were non-Apple papers)

**Relevant non-big-tech context that judges have likely seen**
- Karpathy's "llm-council" (late 2025 weekend project): several LLMs answer, anonymously **rank each other**, then a "chairman" model synthesizes. — [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/12/llm-council-by-andrej-karpathy/)
- Smit et al. (ICML 2024): multi-agent debate "does not reliably outperform" other prompting strategies such as self-consistency. — [PMLR](https://proceedings.mlr.press/v235/smit24a.html)
- CONSENSAGENT (ACL Findings 2025) identifies **sycophancy**, where agents reinforce each other instead of engaging critically. Okawa (ICML 2026) finds sampling noise drives biased consensus in debates. — [ACL Anthology](https://preview.aclanthology.org/eacl-dois/2025.findings-acl.1141); [PMLR v306](https://proceedings.mlr.press/v306/okawa26a.html)

### Inferences
- **Grok 4.20 is structurally the closest shipped analogue to MAGI**: a small fixed set of named personas (research, logic, creative or contrarian) that debate to consensus. Two differences matter. It has a coordinator persona (Grok) that resolves conflicts, so it is centralized. And it optimizes answer quality, with no ethics or safety persona and no escalation.
- Perplexity Model Council and Copilot Council make "show the user where models disagree" a mainstream feature. Neither votes, and neither stops or escalates on disagreement.
- Enterprise platforms (Amazon, Salesforce, IBM, Microsoft Copilot Studio) all use **centralized supervisor or router** topologies. "No central decider" is therefore a real point of contrast with shipped enterprise products. It needs a safeguard, though (see Q1 on error amplification).
- Meta's Coral and the sycophancy literature suggest the main way MAGI can fail is fake consensus: agents caving rather than being persuaded by evidence. Measuring *why* an agent changed its vote (evidence-driven vs social pressure) is an under-served evaluation target.

### Gaps
- Primary xAI documentation for Grok 4.20's agents was not found. The role descriptions come from secondary sources.
- Perplexity's own announcement and model list were not retrieved. Which three models it uses is unconfirmed.
- No Apple activity was found. This may reflect search limits rather than absence.

---

## Q6. Cisco Outshift: AGNTCY, Internet of Agents, Internet of Cognition. What have the Cisco judges already seen?

### Takeaway
Cisco Outshift's own roadmap is about *exactly* MAGI's theme. Its "Internet of Cognition" (early 2026) adds shared intent, shared context and "collective innovation" on top of AGNTCY. Its open-source **Mycelium** project (2026) offers leaderless "goal rooms" where 3+ peer agents negotiate to consensus. Outshift reports consensus rising from **36% to 93% across 14 scenarios**. Cisco judges have seen leaderless multi-agent negotiation with a measured consensus rate, and a healthcare demo of agents with conflicting KPIs. MAGI should build on their stack and differentiate on decision quality, value trade-offs and calibrated escalation, not on "agents can reach consensus".

### Cited Findings
**AGNTCY / Internet of Agents**
- Cisco started AGNTCY in March 2025 with LangChain and Galileo. It was contributed to the Linux Foundation on **July 29, 2025**, with formative members Cisco, Dell, Google Cloud, Oracle and Red Hat, and has 75+ backing companies. It covers discovery, identity, messaging and observability across vendors and frameworks. — [Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos); [NAND Research](https://nand-research.com/research-note-agntcy-moves-to-linux-foundation/)
- The CoffeeAGNTCY reference app (Corto with 2 agents; Lungo as a fuller simulation) uses **LangGraph supervisor-worker** orchestration with SLIM (group communication) and NATS (pub/sub). It was demoed at the Outshift booth at KubeCon NA 2025. No negotiation scenario was documented. — [AGNTCY docs](https://docs.agntcy.org/coffee-agntcy/get-started/); [Outshift KubeCon page](https://outshift.cisco.com/events/kcna-2025)

**Internet of Cognition (IoC)**
- Concept: the Internet of Agents lets agents find each other and exchange messages but not "think together". IoC is a semantic layer above AGNTCY for shared intent, shared context and collective innovation. Outshift argues that MCP and A2A operate at the syntax and identity level. — [AI Chat Daily](https://www.aichatdaily.com/ai-analysis/cisco-s-outshift-pitches-internet-cognition-fix-multi-agent); [Techbuddies, 2026-02-01](https://www.techbuddies.io/2026/02/01/from-message-passing-to-shared-minds-cisco-outshifts-internet-of-cognition-for-ai-agents/); [Outshift X post](https://x.com/outshiftbycisco/status/2016194498976452631); [Forbes BrandVoice (sponsored), 2026-03-10](https://www.forbes.com/sites/outshift-by-cisco/2026/03/10/the-internet-of-cognition-building-infrastructure-for-distributed-superintelligence/)
- Architecture has three parts: (1) protocols for shared intent and coordination; (2) a "cognition fabric" for shared, policy-governed context and memory; (3) "cognition engines" that help agents **negotiate, coordinate or enforce guardrails**. — [CIO.com opinion, 2026-09-16](https://www.cio.com/article/4222319/connecting-ai-agents-was-only-the-beginning-now-they-need-to-think-together.html)
- Vijoy Pandey (SVP and GM, Outshift), on a podcast March 25, 2026:
  - He argues for "scaling out" (collective intelligence) alongside scaling up, and wants teams of agents to solve net-new problems.
  - He proposes cognition-state protocols: semantic, compressed and latent or KV-cache transfer.
  - He favors **diversity and "emergent consensus"** and warns about divergence and over-specialization.
  - He suggests game-theoretic modeling, and says humans are currently the "glue" for intent alignment.
  - — [Cognitive Revolution podcast](https://www.cognitiverevolution.ai/scaling-intelligence-out-cisco-s-vision-for-the-internet-of-cognition-with-vijoy-pandey/)
- **Healthcare demo**: four agents (scheduling, insurance, diagnostics, pharmacy; only scheduling belongs to the hospital) route a patient. The agents have **conflicting local KPIs** (time-to-route, outcome confidence, ROI), and today a *human* must push them to "give a little to get a little". — [Cognitive Revolution podcast](https://www.cognitiverevolution.ai/scaling-intelligence-out-cisco-s-vision-for-the-internet-of-cognition-with-vijoy-pandey/)
- **CAIPE** (Cisco's internal multi-agent SRE system, open-sourced via CNOE): about 20 agents and 100+ tool calls. Pandey says it cut team load about 30% and handles about 40% of tasks end to end. — [Cognitive Revolution podcast](https://www.cognitiverevolution.ai/scaling-intelligence-out-cisco-s-vision-for-the-internet-of-cognition-with-vijoy-pandey/)

**Mycelium (open source, Apache 2.0; Outshift; 2026)**
- Outshift says Mycelium creates "goal rooms" where agents align on intent and converge on one answer: a persistent shared-memory "room" that provides shared context plus a negotiation layer. — [Outshift blog (via search snippet)](https://outshift.cisco.com/blog/ai-ml/moving-multi-agent-systems-from-connected-to-coordinated); [LinkedIn: "Agents that reach consensus 93% of the time: Introducing Mycelium and CASA"](https://www.linkedin.com/pulse/agents-reach-consensus-93-time-introducing-mycelium-casa-uvqfe)
- Reported result (Outshift's own claim): consensus or alignment went from about **36% without coordination to about 93% with Mycelium** across **14 decision scenarios** in a controlled A/B study. — [CIO.com](https://www.cio.com/article/4222319/connecting-ai-agents-was-only-the-beginning-now-they-need-to-think-together.html) (quoting Outshift CPO Papi Menon); [GitHub README](https://github.com/mycelium-io/mycelium)
- Design (from the README):
  - Built for peers with "**no predefined workflow, no centralized supervisor, and no hierarchy**".
  - One MLS-encrypted AGNTCY **SLIM** group channel per room, with a thin FastAPI "moderator".
  - An "aligner" engine runs **NegMAS Stacked Alternating Offers** multi-issue negotiation and stops when agents agree.
  - Agents can state confidence, cite evidence and flag deference, yielding a single "trust number" for a consensus.
  - The README claims alignment "pays off at 3+ agents" and that at 4+ agents it is often the difference between converging and not converging.
  - — [GitHub mycelium-io/mycelium](https://github.com/mycelium-io/mycelium)
- What Mycelium does *not* document:
  - a stated fallback for non-convergence (stalled tasks can be escalated to the aligner);
  - a mechanism for humans to approve or override mid-negotiation (humans create rooms and watch);
  - ground-truth correctness metrics (the headline metric is consensus or alignment rate).
  - — [GitHub mycelium-io/mycelium](https://github.com/mycelium-io/mycelium)
- CASA (Continuous Agent Semantic Authorization), a companion Outshift project, checks agent tool calls against the user's original intent with a reported accuracy above 90%. — [LinkedIn Mycelium/CASA post (via search snippet)](https://www.linkedin.com/pulse/agents-reach-consensus-93-time-introducing-mycelium-casa-uvqfe)
- Caveat: a different project, also called Mycelium (mycelium.domains), is unrelated. — [mycelium.domains](https://mycelium.domains/)

### Inferences
- **What Cisco judges have already seen:**
  - leaderless peer negotiation to consensus among 3+ agents (Mycelium);
  - a consensus-rate A/B baseline (36% vs 93%);
  - agents with conflicting KPIs that need a human to break deadlock (healthcare demo);
  - supervisor-worker multi-agent apps on AGNTCY (CoffeeAGNTCY, CAIPE);
  - in the wider market, Copilot Council, Perplexity Model Council and Grok multi-agent.
  
  A MAGI demo that only shows "three agents debate and reach consensus" will look like a re-implementation of Mycelium's pitch.
- **Where MAGI can credibly go beyond Outshift's public material:**
  - (a) measure *correctness or decision quality*, not just consensus rate. Mycelium's metric rewards agreement, and the sycophancy literature shows agreement can be wrong;
  - (b) make the human escalation path a first-class, measured feature (escalate when unanimity fails, with a dissent brief). This is the gap Pandey describes ("human glue") and Mycelium leaves undocumented;
  - (c) give agents *value-level* competing objectives (scientific rigor vs ethics or safety vs practicality), which maps to Outshift's conflicting-KPI healthcare demo;
  - (d) show the "effect of new information" with tracked vote changes and their reasons.
- **Strategic alignment:** running MAGI's agents over AGNTCY SLIM or A2A, possibly as three separate services or different model vendors, and citing Mycelium (or benchmarking against a Mycelium-style negotiation baseline) speaks the judges' language. Pandey's emphasis on agent diversity supports heterogeneous models per MAGI persona.

### Gaps
- Outshift's IoC whitepaper and Mycelium blog bodies would not render via fetch, so their details come from search snippets, the README, a CIO opinion piece and the podcast. The 36%/93% figure is Outshift-reported and was not independently verified. The docs/evaluation.md file with scenario details returned HTTP 503.
- The exact launch date of "Internet of Cognition" was not confirmed. Coverage starts around late January to early February 2026.
- The UCSC hackathon track page and judge names were not researched here.
- An MIT Technology Review piece, "The path to artificial superintelligence" (2026-07-27), appeared in Mycelium search results. Whether it is sponsored Outshift content was not checked. — [MIT Technology Review](https://www.technologyreview.com/2026/07/27/1140724/the-path-to-artificial-superintelligence/)

---

## Q7. Cross-cutting: similarity to MAGI, standout traits, and does multi-agent beat single-agent?

### Takeaway
Nearly every shipped big-tech system is **centralized**: an orchestrator, supervisor, synthesizer or "chairman" decides. Most optimize a **single objective** (accuracy or research quality). None that I found uses **unanimity plus human escalation** as its stop rule. The evidence that multi-agent beats single-agent is real but mostly vendor-reported, confounded by compute, and task-dependent (sequential tasks can get worse).

### Cited Findings
- Multi-agent gains with ground truth or a baseline:
  - MAI-DxO 81.9% vs o3 78.6% at lower cost; ensemble 85.5% — [arXiv HTML](https://arxiv.org/html/2506.22405)
  - Anthropic +90.2% over single agent at about 15x tokens — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Copilot Critique +7.0 points on DRACO (vendor-run, LLM-judged) — [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research)
  - Habermas Machine statements preferred 56% over human mediators — [MIT Tech Review](https://www.technologyreview.com/2024/10/17/1105810/ai-could-help-people-find-common-ground-during-deliberations/)
  - Debate lifts judge accuracy 48% to 76% (LLM judges) and 60% to 88% (human judges) — [arXiv 2402.06782](https://arxiv.org/html/2402.06782v4)
- Negative or caution results:
  - All multi-agent variants degrade sequential reasoning by 39–70%; independent agents amplify errors 17.2x — [Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
  - Tokens explain 80% of variance — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Models cannot consistently leverage collaboration — [Meta Coral](https://ai.meta.com/research/publications/collaborative-reasoner-self-improving-social-agents-with-synthetic-conversations/)
  - Debate doesn't reliably beat self-consistency — [Smit et al.](https://proceedings.mlr.press/v235/smit24a.html)
  - Debate vs direct QA is mixed without information asymmetry — [Kenton et al.](https://arxiv.org/pdf/2407.04622)
  - First-proposal bias in agent negotiation — [Magentic Marketplace](https://arxiv.org/html/2510.25779v1)

### Inferences
Comparison grid. Each row's claims are sourced in Q1–Q6 above.

| System (company, date, status) | Agents / topology | Competing objectives? | Decision rule | Human-in-loop | Ground-truth eval | Closest MAGI overlap |
|---|---|---|---|---|---|---|
| AI co-scientist (Google, Feb 2025, research and trusted testers) | Functional agents under a Supervisor (centralized) | No (single goal: hypothesis quality) | Elo tournament ranking | Scientist seeds and feedback | Partial (wet lab, GPQA correlation, expert ratings) | Debate, critique, evolve |
| Habermas Machine (DeepMind, Science, Oct 2024) | AI mediator for human groups | Humans hold the competing views | Simulated election over predicted rankings | Humans are the deliberators | Human preference (56%) and external raters | Consensus with minority preservation |
| Gemini Deep Think (Google, Aug and Dec 2025, shipped) | Single model, parallel hypotheses | No | Internal | No | Benchmarks | Baseline category only |
| MAI-DxO (Microsoft, Jun 2025, research) | 5 role personas, one orchestrator | Yes (accuracy vs cost; devil's advocate) | Panel consensus on next action | None at runtime | Yes (NEJM gold diagnoses; physician baseline) | **Very high** |
| Copilot Critique / Council (Microsoft, Mar 2026, Frontier preview) | GPT generates, Claude critiques; or parallel plus synthesis judge | No | Reviewer revises; synthesis summary | User reads divergence | DRACO, LLM-judged (vendor) | Cross-vendor critique; preserve disagreement |
| Anthropic Research (Jun 2025, shipped) | Lead plus parallel subagents | No | Lead decides | No | Internal eval plus humans | Low (no debate) |
| Claude Code agent teams (Anthropic, experimental) | Fixed lead plus teammates who message directly | Prompted (devil's advocate) | Lead synthesizes "consensus" | User can message any teammate | No | Debate prompting pattern |
| Grok 4 Heavy / 4.20 (xAI, Jul 2025 / Feb 2026, shipped) | 4 named personas plus coordinator | Roles differ (contrarian), not objectives | Peer review "until consensus"; coordinator resolves | No | Vendor benchmarks | **High (persona council)** |
| Perplexity Model Council (Feb 2026, shipped Max) | 3 models plus synthesizer | No | Synthesis of agree, diverge, unique | User | No | Preserve disagreement |
| Bedrock / Agentforce / watsonx (shipped) | Supervisor or router | No | Supervisor | Router may route to humans (IBM) | Vendor internal | Low |
| Mycelium (Cisco Outshift, 2026, OSS) | Leaderless peers in a room; moderator or aligner engine | Agents bring positions | NegMAS alternating-offers negotiation to agreement | Humans set up and watch | Consensus rate (36% to 93%), not correctness | **Very high (and it is the judges' own work)** |

- **MAGI's defensible differentiators** (none of these appears as a combined, shipped feature in the material found):
  1. *Value-pluralistic* personas: an ethics or safety agent with veto power, rather than accuracy-only roles.
  2. A **unanimity rule whose failure triggers structured human escalation** with a dissent brief, as opposed to a synthesizer or coordinator silently resolving conflicts.
  3. **Measured belief revision under injected new information**, with reasons logged.
  4. **Decision-quality evaluation** against ground truth plus a **token-matched single-agent or self-consistency baseline**, and reporting escalation precision (did it escalate the cases it would have gotten wrong?).
- **Biggest credibility risks for MAGI:**
  - Being seen as a re-skin of Mycelium, Grok 4.20 or MAI-DxO.
  - Claiming gains that are really extra tokens.
  - Fake consensus through sycophancy.
  - Error amplification in a decentralized topology without cross-checking.

### Gaps
- I found no public, head-to-head study comparing unanimity-with-escalation against majority vote or synthesizer-decides in LLM councils. This may be an open research gap, or something my search missed.
- No independent (non-vendor) replications were found for Copilot Critique, Grok 4.20, Bedrock or Mycelium claims.

---

## Q8. What gaps remain that a hackathon project could credibly target?

### Takeaway
The open space is not "agents debate". It is **trustworthy stopping and escalation, value trade-offs, and honest evaluation**. A hackathon-scale MAGI can credibly own the following: "knows when it doesn't know (as a group) and hands a human a crisp dissent brief", "shows how new evidence moves each agent and why", and "beats a compute-matched single agent on ground-truth decisions, or tells you when it doesn't".

### Cited Findings
- No documented non-convergence fallback or human override in Mycelium; its headline metric is consensus rate. — [GitHub mycelium-io/mycelium](https://github.com/mycelium-io/mycelium); [CIO.com](https://www.cio.com/article/4222319/connecting-ai-agents-was-only-the-beginning-now-they-need-to-think-together.html)
- Pandey: humans are currently the "glue" for intent alignment. In the healthcare demo, a human has to get KPI-conflicting agents to compromise. — [Cognitive Revolution](https://www.cognitiverevolution.ai/scaling-intelligence-out-cisco-s-vision-for-the-internet-of-cognition-with-vijoy-pandey/)
- Council-style products summarize divergence but do not vote or escalate. — [Computerworld](https://www.computerworld.com/article/4152323/microsoft-adds-multi-model-ai-to-copilot-researcher-raising-accuracy-stakes.html); [Storyboard18](https://www.storyboard18.com/digital/perplexity-launches-model-council-to-compare-answers-across-multiple-ai-models-89246.htm)
- Compute is the dominant confound: tokens explain 80% of variance. — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- Sycophancy and biased consensus are documented failure modes, and post-training makes models poor collaborators. — [CONSENSAGENT](https://preview.aclanthology.org/eacl-dois/2025.findings-acl.1141); [Okawa ICML 2026](https://proceedings.mlr.press/v306/okawa26a.html); [Meta Coral](https://ai.meta.com/research/publications/collaborative-reasoner-self-improving-social-agents-with-synthetic-conversations/)
- Decentralized topologies amplify errors without cross-checks. — [Google Research](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/)
- Agents anchor on first proposals. — [Magentic Marketplace](https://arxiv.org/html/2510.25779v1)
- A Göttingen study found consensus protocols beat voting on knowledge tasks, while voting beats consensus on reasoning tasks. This suggests MAGI's decision rule should be chosen per task type. — [arXiv 2502.19130 overview](https://alphaxiv.org/overview/2502.19130v4)

### Inferences
Candidate hackathon targets, ranked by credibility, novelty against the landscape above, and fit with the Cisco Level 3 rubric:

1. **Calibrated escalation as the headline metric.** Report, on a labeled question set, the following:
   - accuracy when unanimous;
   - accuracy of the single-agent baseline on the cases MAGI escalated;
   - the escalation rate.
   
   The pitch: "When MAGI agrees it is right X% of the time; when it escalates, the single agent would have been wrong Y% of the time." Nobody in big tech publishes this for a council. It also directly addresses the track's "know when to stop / ask a human" criterion.
2. **Evidence-driven vs social belief revision.** Inject new information mid-debate and log each agent's position, confidence and stated reason. Flag flips that cite no new evidence as possible sycophancy. This hits the track's "effect of new information" criterion and the Coral and CONSENSAGENT failure modes.
3. **Value-pluralistic competing objectives with a veto.** Give the ethics or safety agent explicit authority to block. Unlike MAI-DxO, Grok 4.20 and co-scientist, which all optimize accuracy, this mirrors Outshift's own conflicting-KPI healthcare scenario.
4. **Compute-matched baselines.** Compare against the same model with N samples and majority vote or self-consistency at equal tokens, and against a single "pro"-style run. Optionally add a "synthesizer decides" ablation (Council or Perplexity style) and a "majority vote" ablation versus unanimity-plus-escalation.
5. **Run on Cisco's stack and cite it.** Put three independent agent processes (ideally different model vendors, for diversity) on AGNTCY SLIM or A2A with identity. Frame MAGI as "an Internet of Cognition cognition engine for high-stakes decisions" that adds escalation and dissent preservation to Mycelium-style goal rooms. Optionally use Mycelium as a baseline.
6. **Dissent artifact.** Produce a "minority report" when unanimity fails, in the spirit of the Habermas Machine's incorporation of minority critiques. Human judges get the strongest arguments on each side, which follows the debate-for-oversight rationale (Irving et al.; Khan et al.).

### Gaps
- No standard benchmark exists for "council escalation calibration". MAGI would need to build a small labeled set, for example questions with known answers plus deliberately ambiguous or value-contested items.
- It is unknown whether Outshift judges will run Mycelium themselves or expect integration. The track rubric wording was taken from the assignment brief, not verified against the track page.
