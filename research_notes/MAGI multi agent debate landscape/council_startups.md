# Startups and Products in Multi-Model Consensus, AI Councils, AI Debate, and Simulated Stakeholders (benchmark for MAGI)

Research date: 2026-10-10. Scope: general-purpose decision support and answer quality. Domain-specific negotiation, procurement, energy and trading companies are excluded because another researcher covers them. Most claims about performance or traction come from vendors and are flagged as self-reported. Where sources conflict, the conflict is noted.

---

## Q1. Which products are built on multi-model consensus or cross-checking ("ask many models")?

### Takeaway
There are three tiers of "ask many models and reconcile" products. The first is small startups that sell consensus as the whole product: Sup AI, Suprmind and CollectivIQ. The second is incumbents that shipped it as a premium feature in 2025-2026: Perplexity Model Council, Microsoft 365 Copilot Researcher Critique/Council, and xAI Grok 4 Heavy. The third is side-by-side chat aggregators that show answers next to each other without reconciling them: ChatHub, Poe and TypingMind. A large open-source scene sits underneath all three, including Karpathy's llm-council and at least five projects literally named MAGI.

### Cited Findings

**Sup AI (startup; sup.ai / Product Hunt)**
- Sup AI runs a query through many LLMs in parallel and "synthesizes answers by measuring confidence on every segment." Its premise: "Every LLM hallucinates. They just don't hallucinate the same things." Reported model count is 339 — [FeedBagel](https://feedbagel.com/post/sup-ai-ensemble-system-using-339-llms-to-reduce-hallucinations-scores-5215-on-hu). Another review says 337 active models — [PopularAITools](https://popularaitools.ai/tools/sup-ai/).
- It claims 52.15% on Humanity's Last Exam (HLE). Promotional coverage says this beats any single model by 7.41 points. The figure is self-reported and I did not find an independent replication — [FeedBagel](https://feedbagel.com/post/sup-ai-ensemble-system-using-339-llms-to-reduce-hallucinations-scores-5215-on-hu); [PopularAITools](https://popularaitools.ai/tools/sup-ai/).
- One review says it downweights high-entropy segments, which are likely hallucinations. It can also use web search or code execution to verify results during synthesis — [PopularAITools](https://popularaitools.ai/tools/sup-ai/).
- A directory listing shows it was added on 2025-09-17 — [ToolMage](https://www.toolmage.com/ko/tool/sup-ai/). Its Product Hunt page is https://www.producthunt.com/products/sup-ai — [FeedBagel](https://feedbagel.com/post/sup-ai-ensemble-system-using-339-llms-to-reduce-hallucinations-scores-5215-on-hu).
- **Status flag:** when I fetched https://sup.ai on 2026-10-10, the page showed only "Sup AI / Sign in / Coming soon." The product may have moved, be relaunching, or have paused — [sup.ai](https://sup.ai).
- Founder: secondary coverage says Ken Mueller, a 20-year-old Stanford CS student. FeedBagel only names Mueller as the article's author, and a search turned up no corroboration. Treat this as unverified — [PopularAITools](https://popularaitools.ai/tools/sup-ai/); [FeedBagel](https://feedbagel.com/post/sup-ai-ensemble-system-using-339-llms-to-reduce-hallucinations-scores-5215-on-hu).

**Suprmind (startup; suprmind.ai)**
- Five frontier models share one conversation: GPT, Claude, Gemini, Grok and Perplexity Sonar. The company says they were chosen because their "training data, reasoning patterns, and tool access differ" — [Suprmind platform page](https://suprmind.ai/hub/platform/).
- It has six modes:
  - Sequential: each AI reads all prior answers.
  - Super Mind: five answer in parallel, then a synthesis layer merges them with "consensus mapping and divergence flags."
  - Debate: models argue assigned positions.
  - Red Team: attacks a plan "from six angles."
  - Research Symphony.
  - First Principles.
  
  An "Adjudicator" produces a "Disagreement/Correction Index." The company says disagreement is "surfaced, tracked, indexed" rather than smoothed over — [Suprmind platform page](https://suprmind.ai/hub/platform/).
- Pricing: Spark $19/mo, Pro $45/mo, Frontier $95/mo, Enterprise custom, plus a 7-day free trial — [Suprmind platform page](https://suprmind.ai/hub/platform/).
- Self-reported traction: an internal study of 1,324 production turns over 45 days found 3,484 "unique insights," 949 of them "critical-severity." The page does not describe any human-escalation feature. The founding year and founders are not stated, and the only named person is the page author, Radomir Basta — [Suprmind platform page](https://suprmind.ai/hub/platform/).
- Its guidance is to log disagreement rather than automatically take the majority answer — [Suprmind via search summary](https://suprmind.ai/hub/?p=3065).

**CollectivIQ (startup; Boston)**
- Launched on 2026-03-04 as a "World's First AI Consensus Platform." It queries ChatGPT, Claude, Gemini, Grok and up to about 10 other LLMs, then returns "a single annotated response" that shows agreement and disagreement. CEO: John Davie — [Buyers Edge Platform press release](https://buyersedgeplatform.com/blog/collectiviq-launches-worlds-first-ai-consensus-platform/); [Pulse2 interview](https://pulse2.com/collectiviq-profile-john-davie-interview/).
- It is described as a Boston spinout. It was built after employees reported biased or wrong AI answers ending up in official presentations — [Pulse2 interview](https://pulse2.com/collectiviq-profile-john-davie-interview/).
- Claimed scores are 53.3% on HLE (text-only) and 96.4% on GPQA Diamond, from an "independent evaluation conducted by Ten Point Data." I could not verify that evaluation — [TechEdgeAI](https://techedgeai.com/collectiviq-ai-consensus-platform-claims-higher-accuracy-than-frontier-models/).
- An April 2026 update added model selection, file RAG, image generation, projects, and a "Triager" intent router — [IT Brief UK](https://itbrief.co.uk/story/collectiviq-adds-model-choice-image-tools-for-teams).
- **Conflict:** one blog says CollectivIQ was founded by "former Google DeepMind researchers Priya Mehta and James Chen." It also claims 73% fewer hallucinations at $0.08 per query. This conflicts with the press coverage naming John Davie as CEO of a Boston spinout. The blog looks unreliable, possibly AI-generated, so do not use those claims — [DigitalApplied](https://www.digitalapplied.com/blog/collectiviq-multi-model-ai-consensus-enterprise-platform) vs [Pulse2](https://pulse2.com/collectiviq-profile-john-davie-interview/).
- I found no funding or pricing disclosed.

**Perplexity Model Council (incumbent feature)**
- Announced 2026-02-05. The user picks three models and they answer in parallel. A separate synthesizer model highlights agreement, divergence, and each model's unique insight. It was Max-only at launch ($200/mo). It was later integrated into Perplexity's "Computer" environment to produce cited reports with a consensus/disagreement breakdown — [Perplexity blog](https://hub-prod.perplexity.ai/hub/blog/introducing-model-council); [Storyboard18](https://www.storyboard18.com/digital/perplexity-launches-model-council-to-compare-answers-across-multiple-ai-models-89246.htm); [CreateWith](https://www.createwith.com/tool/perplexity/updates/perplexity-adds-model-council-for-cross-model-analysis-inside-computer).

**Microsoft 365 Copilot Researcher: Critique and Council (incumbent feature, late March 2026)**
- Critique: a GPT model plans, retrieves and drafts, then Claude reviews the draft for accuracy, completeness and citations. It is the default when the model picker is set to auto — [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research); [Constellation Research](https://www.constellationr.com/insights/news/microsoft-365-copilots-researcher-agent-goes-multi-model).
- Council: sources disagree on how it works. Constellation describes side-by-side comparisons. Decrypt describes models working in parallel while a third judge finds the discrepancies — [Constellation Research](https://www.constellationr.com/insights/news/microsoft-365-copilots-researcher-agent-goes-multi-model); [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research).
- Microsoft's self-reported results are on the DRACO benchmark: "+13.8%" over rival tools, or "+7.0 points" over the previous best system — [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research); [TechStrong](https://techstrong.ai/features/microsoft-unveils-multi-model-critique-and-agentic-ai-to-boost-copilot-adoption/).

**xAI Grok 4 Heavy (incumbent; July 9, 2025)**
- Parallel agents "compare their work... like a study group." Musk said it is not a simple majority vote, because often only one agent finds the key insight. It sold at $300/mo through SuperGrok Heavy — [OfficeChai](https://officechai.com/miscellaneous/elon-musk-explains-how-grok4-heavy-xais-multi-agent-reasoning-model-works/); [AI-TLDR](https://ai-tldr.dev/models/grok-4-heavy/).
- A less established source says Grok 4.20 uses four agents that analyze separately and then debate, with "Heavy mode" scaling to 16 agents — [Basenor](https://www.basenor.com/blogs/news/grok-4-20-is-live-whats-new-and-why-its-getting-faster).

**Side-by-side aggregators (no reconciliation)**
- ChatHub began as an open-source Chrome extension and is now a web, desktop and mobile app. Pro is listed at $14.99/mo billed annually (third-party listing) — [ToolJunction](https://www.tooljunction.io/ai-tools/chathub).
- Poe (Quora) has a multi-bot chat that sends one prompt to several models side by side, with a free tier — [ToolsForHumans](https://www.toolsforhumans.ai/ai-tools/poe).
- TypingMind's "multi-model responses" sends one prompt to several models and keeps a separate thread per model. You bring your own API keys — [TypingMind docs](https://docs.typingmind.com/manage-and-connect-ai-models/activate-multi-model-responses).

**Yupp (startup; shut down)**
- Raised a $33M seed led by a16z crypto (Chris Dixon). Users compared answers from about 800 models and were paid for preference feedback. It shut down less than a year after launch, as reported on 2026-03-31 — [TechCrunch](https://techcrunch.com/2026/03/31/yupp-ai-shuts-down-raising-33m-from-a16z-cryptos-chris-dixon/); [The Block](https://www.theblock.co/post/358094/a16zcrypto-33-million-usd-seed-round-yupp-ai-model-evaluation).
- Failory argues the post-training data market moved to expert-labeled datasets rather than broad consumer feedback — [Failory](https://newsletter.failory.com/p/paid-to-use-ai).

**Triall (small tool)**
- Three LLMs answer in parallel, blind peer-review and stress-test each other, then give an "evidence-tagged verdict with confidence scores." One listing says it is a Google Colab rather than SaaS — [FutureTools](https://futuretools.io/tools/triall-usp6to); [FutureTools alt](https://www.futuretools.io/tools/triall).

**Open-source "LLM council" reference designs**
- Karpathy's llm-council was posted around 2025-11-22. It sends queries through OpenRouter to several models, which anonymously rank each other's answers, and then a "Chairman" LLM writes the final answer. Karpathy described it as "vibe coded as a fun Saturday hack" and said it is unsupported — [Language Log via Harvard TagTeam](https://tagteam.harvard.edu/hub_feeds/1937/feed_items/16984216); [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/12/llm-council-by-andrej-karpathy/).
- It had about 23.4k GitHub stars and about 4.2k forks as of 2026-07-30 — [Star History](https://www.star-history.com/karpathy/llm-council).
- Derivatives include a Java/Spring port, the Python package "Consilium" (openadapt-consilium), and coding-agent extensions — [Medium explainer](https://medium.com/@nisarg.nargund/andrej-karpathys-llm-council-fully-explained-5251bdc9a95f); [PyPI Consilium](https://pypi.org/project/openadapt-consilium/0.4.1/).

### Inferences
- The minimum feature set is now: parallel answers from different model families, a synthesis with agreement and disagreement highlighted, and optional anonymized peer ranking. A weekend hack can build it, and Perplexity, Microsoft and xAI all ship it. MAGI cannot stand out on "multiple models agree" alone.
- Accuracy claims cluster around HLE at roughly 50%: Sup 52.15%, CollectivIQ 53.3%, and Grok 4 Heavy 44.4% with tools (50.7% on the text-only subset). All are self-reported. "Beats single models on HLE" is becoming the standard marketing line, and judges may be skeptical of it.

### Gaps
- Sup AI: no funding, founding date, current pricing, or confirmed current status found. The homepage said "Coming soon" on 2026-10-10.
- Suprmind and CollectivIQ: funding and founding year not found.
- I did not verify how Poe and ChatHub multi-bot features stand in 2026, or how many people use them.
- Consensus.app is a likely name confusion. It is generally known as an AI search engine over academic papers, not a multi-model consensus product, but I did not research it in this session.

---

## Q2. Which AI debate, argument and deliberation products exist?

### Takeaway
Deliberation tools aggregate human opinions; AI mainly clusters and summarizes them. Examples are Polis, Talk to the City, Remesh and Harmonica. AI-vs-AI or AI-vs-user debate products are mostly consumer apps or open-source projects, such as Dissent, DebateAI and Turncoat. I found no funded startup whose core product is AI agents debating to reach a binding group decision.

### Cited Findings
- **Talk to the City** (AI Objectives Institute, nonprofit, open source): LLMs extract arguments from large volumes of public input and arrange them into clusters and subclusters that users can explore as an opinion map. It can ingest Polis results — [AOI page archive](https://gwern.net/doc/www/ai.objectives.institute/fa46182a810da5bfde418b21016574027d1dd94f.html). Reported deployments include Taiwan's moda, Chatham House "Recursive Public" (1,000 participants), Tokyo election polling, and UNFCCC. These come from a secondary wiki and are unverified — [LongtermWiki](https://www.longtermwiki.com/wiki/E2717).
- **Polis** (open source): participants submit short statements and vote agree, disagree or pass. Algorithms cluster voters and surface "bridging consensus" — [LongtermWiki](https://www.longtermwiki.com/wiki/E2717).
- **Remesh** (commercial): an enterprise market and employee research platform. In 2026 it focused on "Remy," an AI that "plans, builds, recruits, probes, and analyzes a study from a single conversation" — [Remesh 2026 review](https://www.remesh.ai/resources/from-question-to-defensible-decision-2026-at-remesh-so-far). One secondary wiki claims Culture Amp acquired Remesh in 2023. I could not verify this, and Remesh's 2026 site presents it as an independent product — [LongtermWiki](https://www.longtermwiki.com/wiki/E2717).
- **Harmonica** (open source, AI facilitation): started as 1:1 AI interviews. Version 0.4 (2026-06-12) became "a runtime for facilitation": multiplayer sessions, chained multi-step workflows, and a public MCP server so agents can create and run sessions. Metagov used it to gather input from more than 50 governance experts — [Harmonica 0.4 update](https://opencollective.com/harmonica/updates/harmonica-0-4-a-runtime-for-facilitation).
- A 2025 panel on AI-powered deliberation (mySociety TICTeC) listed Remesh, GoVocal, Talk to the City and Harmonica as the existing tools — [TICTeC](https://tictec.mysociety.org/event/ai-powered-deliberation-opportunities-and-risks/).
- **Dissent: AI Debate** (consumer app): eight AI personalities with different debate styles, plus AI judges that score on logic, rhetoric and scholarly merit. It challenges the user rather than steelmanning — [MWM listing](https://mwm.ai/apps/dissent-ai-debate/6761025160).
- **DebateAI**: a platform where users debate an AI opponent to challenge their beliefs — [G2](https://www.g2.com/products/debateai/discuss).
- **Turncoat** (open source): two LLMs each argue for and against a motion in a four-speech format, using the user's own API keys — [Streamlit forum](https://discuss.streamlit.io/t/ai-models-debate-turncoat-style/120750).
- I found no funded startup whose core product is steelmanning — [search summary across sources above; see Gemini competition project](https://ai.google.dev/competition/projects/ai-debate?hl=pt-br).

### Inferences
- MAGI fits between these two groups. Deliberation tools have legitimacy mechanisms, such as Polis' bridging consensus, but the participants are humans. Debate apps have AI participants but no decision output. MAGI's "agents debate, revise, vote unanimously, escalate to a human" adds a decision protocol that consumer debate apps lack.
- Polis' "bridging consensus" (agreement across clusters that otherwise disagree) is a well-tested mechanism MAGI could borrow. For example, a proposal could pass only if it wins approval from agents with opposing objectives, which is what MAGI's unanimity rule already does.

### Gaps
- No funding or traction figures for Dissent, DebateAI or Harmonica.
- Remesh's ownership status (independent or acquired) is unverified.

---

## Q3. Which products use synthetic personas, simulated stakeholders, or AI "boards of advisors"?

### Takeaway
This is the most heavily funded cluster. Simile has raised about $300M at a $2B valuation, and Aaru has a $1B headline valuation. Both simulate populations of AI agents to predict human reactions rather than to decide. Consumer "AI board of advisors" apps (Boardroom AI, Kin, Thinkers, AdviseMe) are closest to MAGI's form, with several personas that can vote. They are small, unfunded or undisclosed, and appear to be personas on one model.

### Cited Findings

**Simulated populations (well-funded)**
- **Simile** (Joon Sung Park, co-author of the 2023 "Generative Agents" paper):
  - $100M Series A in February 2026, reportedly led by Index Ventures, with Bain Capital Ventures, A* and Hanabi. Fei-Fei Li and Andrej Karpathy also invested — [iTiger](https://www.itiger.com/news/1115874123).
  - $200M Series B at a $2B valuation in July 2026, led by Greenoaks — [RuntimeWire](https://runtimewire.com/article/simile-raises-200m-series-b-2b-valuation); [Seedtable](https://seedtable.com/companies/simile/funding-rounds/series-b-2026-07).
  - Pitch: test decisions against populations of AI agents before real customers see them. Early customer: CVS Health — [Implicator](https://www.implicator.ai/the-stanford-team-that-invented-generative-agents-wants-to-kill-the-focus-group.md); [RuntimeWire](https://runtimewire.com/article/simile-raises-200m-series-b-2b-valuation).
- **Aaru** (NYC):
  - Founded 2024 by Cam Fink and Ned Koh; some sources also name John Kessler — [NeuronFeed](https://neuronfeed.com/startups/aaru); [Semafor](https://www.semafor.com/article/09/20/2024/ai-startup-aaru-uses-chatbots-instead-of-humans-for-political-polls).
  - Its product, Lumen, simulates large numbers of agents built from census, personality and behavioral data — [Semafor](https://www.semafor.com/article/09/20/2024/ai-startup-aaru-uses-chatbots-instead-of-humans-for-political-polls); [Fortune](https://fortune.com/2026/06/17/aaru-cofounder-ned-koh-ai-startup-sales-pitch-do-not-trust-us/).
  - Predicted the June 2024 NY Democratic primary within 371 votes — [Semafor](https://www.semafor.com/article/09/20/2024/ai-startup-aaru-uses-chatbots-instead-of-humans-for-political-polls).
  - Its simulation of the 2025 NYC mayoral primary came within 2,000 votes — [Fortune](https://fortune.com/2026/06/17/aaru-cofounder-ned-koh-ai-startup-sales-pitch-do-not-trust-us/).
  - Series A in December 2025, reportedly led by Redpoint at a $1B "headline" valuation with a lower blended valuation. The round was reported as over $50M and ARR as under $10M, all from anonymous sources — [TechCrunch](https://techcrunch.com/2025/12/05/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation).
  - Earlier backers include Accenture Ventures (March 2025), Felicis, General Catalyst and A*. Customers include Accenture, EY, IPG and political campaigns — [TechCrunch via search summary](https://techcrunch.com/2025/12/05/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation).
  - Co-founder Koh reportedly tells clients "Do not trust us. Do not trust our model" — [Fortune](https://fortune.com/2026/06/17/aaru-cofounder-ned-koh-ai-startup-sales-pitch-do-not-trust-us/).
- **Artificial Societies** (London, YC W25):
  - Founded 2024 by James He and Patrick Sharpe. About $5.3M raised: a Point72 Ventures-led seed, plus a pre-seed led by Kindred Capital with YC participating — [Unite.ai](https://www.unite.ai/?p=264519); [Silicon Canals](https://siliconcanals.com/yc-backed-artificial-societies-bags-e4-5m/).
  - Simulates "societies" of AI personas reacting to messaging. Claims more than 15,000 users and more than 100,000 simulations (self-reported) — [Unite.ai](https://www.unite.ai/?p=264519).
- **Electric Twin** (London):
  - Raised a £7M round led by Atomico plus a previously undisclosed £3M pre-seed, about $14M in total, reported February 2026. Angels include Marc Andreessen and Cal Henderson — [UKTech News](https://www.uktech.news/ai/ai-startup-building-synthetic-audiences-to-model-human-thought-raises-10m-20260212); [Pulse2](https://pulse2.com/electric-twin-synthetic-audience-ai-platform-secures-14-million-in-funding).
  - Founders are Alex Cooper (CEO) and Dr Ben Warner. Claims more than 40,000 population evaluations across 155 countries — [UKTech News](https://www.uktech.news/ai/ai-startup-building-synthetic-audiences-to-model-human-thought-raises-10m-20260212).
- **Synthetic Users** (syntheticusers.com):
  - AI-persona user interviews, positioned as a step before real interviews — [Synthetic Users FAQ](https://syntheticusers.com/faqs).
  - Self-reported claim of 85% overlap with insights from human interviews — [Adviso review](https://www.adviso.ca/en/blog/test-bench-ux-and-cx-research-driven-by-artificial-intelligence-ai-1).
  - Pro plan at $49/mo per G2 — [G2](https://ai.g2.com/marketplace/tools/syntheticusers).
  - CEO Kwame Ferreira; co-founder Hugo Alves — [Synthetic Users team](https://www.syntheticusers.com/team).
  - Founding date conflicts: CB Insights says 2013, while the company says it began experimenting with LLMs in 2019 — [CB Insights](https://www.cbinsights.com/compare/ballpark-vs-synthetic-users).

**AI "board of advisors" consumer apps (closest in form to MAGI)**
- **Boardroom AI** (iOS): pick 2 to 9 board members from 25 AI business personalities, hold meetings, call votes on decisions, get automatic minutes, and run separate boards per goal — [AppFollow listing](https://apps.appfollow.io/ios/boardroomai-app/6755253237?country=us).
- **Kin: Personal AI Advisors**: five advisors with shared on-device memory, aimed at personal and career coaching — [App Store](https://apps.apple.com/us/app/-/id6473448146).
- **Thinkers**: unlimited custom AI advisor personas — [App Store](https://apps.apple.com/py/app/thinkers-your-ai-advisors/id6743700517?l=en-GB).
- **AdviseMe**: a group chat with several AI personas, including ones modeled on public figures — [Product Hunt](https://www.producthunt.com/p/advise-me/adviseme).
- **AI Board Advisor: 24/7**: video-call sessions with AI board members who learn the business from uploaded documents, from $49/mo (marketing claim) — [Product Hunt](https://www.producthunt.com/products/ai-boardai-board-advisor-24-7).
- **AI Agent Rooms**: up to eight personas plus a moderator that synthesizes the discussion — [The Prompt Index](https://thepromptindex.com/agent-rooms/).
- **mamf**: a Rust CLI council of CFO, CTO and CMO advisors. Experimental; its docs build had failed — [docs.rs](https://docs.rs/mamf).
- A practitioner guide describes an AI board as personas that "debate your decision, critique each other blind, and vote." It warns that one shared chat makes advisors converge, and admits "it's one model playing seven disciplined lenses" — [The Solo Creators](https://thesolocreators.com/learn/ai-board-of-advisors/).

### Inferences
- Investors are paying for simulating many humans (prediction, market research), not for a few AIs reaching a verdict. Simile and Aaru together account for several hundred million dollars. I found no disclosed VC funding for any council or advisor-board app.
- Persona-board apps have voting but apparently lack model diversity and human escalation. Consensus apps have model diversity but lack competing value-laden objectives. MAGI combines both.
- Aaru's "Do not trust us" stance shows that even the best-funded simulation companies sell with humility about accuracy. MAGI's explicit escalation to a human can be presented the same way: as calibrated deference rather than a weakness.

### Gaps
- No funding, users or founding dates for Boardroom AI, Kin, Thinkers, AdviseMe or AI Board Advisor.
- Not confirmed whether these apps use one underlying model or several.
- No independent accuracy validation for Simile, Artificial Societies, Electric Twin or Synthetic Users.

---

## Q4. Which enterprise decision-intelligence products use multiple agents (red team/blue team, investment-committee-style)?

### Takeaway
I found little evidence of funded general-purpose enterprise startups built around adversarial multi-agent deliberation. The clearest commercial examples are Suprmind's Red Team and Debate modes, Microsoft's Critique (a drafter and reviewer pair), and CollectivIQ's enterprise pitch. The rest are hackathon projects or prompting guides.

### Cited Findings
- **Suprmind Red Team mode** "attacks a plan from six angles." The company recommends using it before launches, investments, leadership presentations and fundraising, with specific metrics as input — [Suprmind platform](https://suprmind.ai/hub/platform/); [Suprmind Red Team](https://suprmind.ai/hub/modes/red-team-mode/).
- **RedTeam** (lablab.ai, Milan AI Week hackathon project): multi-agent "adversarial decision intelligence." Users upload a business plan or market-entry proposal, and the agents find flaws for internal decision-makers. It is a hackathon project, not a funded company — [lablab.ai](https://lablab.ai/ai-hackathons/milan-ai-week-hackathon/umarell/redteam-adversarial-decision-intelligence-agent).
- Founders already prompt chatbots to play roles such as "penetration tester," "ruthless competitor" or "regulatory enforcer" to pull apart business ideas — [Arabian Post](https://thearabianpost.com/entrepreneurs-turn-to-harsh-ai-red-teamers-to-stress‑test-ideas/).
- **CollectivIQ** pitches enterprise teams on fewer hallucinations, provenance for each answer, and less vendor lock-in — [Pulse2](https://pulse2.com/collectiviq-profile-john-davie-interview/).
- **Microsoft Critique**: one model drafts and a model from another company reviews, inside enterprise M365 — [Constellation Research](https://www.constellationr.com/insights/news/microsoft-365-copilots-researcher-agent-goes-multi-model).
- A broad search for 2026 multi-agent "decision intelligence" startup rounds found only adjacent companies: Antares Labs (real estate decision support), Gravity (agentic BI), Canyon Code (multi-agent observability) and Synapse Analytics (credit-policy decisioning). None is described as debate or consensus based — [Gravity tracker](https://gravity.fast/blog/ai-agent-funding-tracker-q3-2026/); [NeuronFeed seed list](https://neuronfeed.com/funded/seed/2026).

### Inferences
- "Red team your plan" is a growing pattern, but it is sold as a mode inside a multi-model chat (Suprmind) or as a prompt technique, not as a governed decision workflow with sign-off. That fits the Cisco Cloud enterprise angle: an auditable, policy-aware council for operational decisions such as change approvals or incident response.

### Gaps
- I did not find investment-committee simulators for general use. Finance-specific tools were out of scope.
- No enterprise customer counts for Suprmind or CollectivIQ.

---

## Q5. How similar is each product to MAGI, and what makes each stand out or fall short?

### Takeaway
The closest analogues are open-source projects, not companies:
- Jason Chao's **MAGI council** (magi-council.org): three different models, eight decision methods including yes/no votes, and a minority report.
- **lordpba/AI_Magi**: personas named Melchior, Balthasar and Casper for logic, ethics and practicality, nearly the same as the planned MAGI roles.

Among companies, **Suprmind** is closest, with multiple models, Debate and Red Team modes, and a disagreement index. None of the sources describe unanimity voting on concrete proposals combined with escalation to a human when unresolved.

### Cited Findings

**Similarity matrix** (High, Med or Low similarity to MAGI: 3 agents with competing objectives, debate and revision, unanimous vote on proposals, human escalation)

| Product | Type / status | Agents | Personas or different models | Aggregation | Human escalation | Similarity | Stands out | Weakness | Source |
|---|---|---|---|---|---|---|---|---|---|
| MAGI council (Jason Chao), magi-council.org | Open source, 2026; PyPI `magi-core` | 3 (GPT-5, Claude, Gemini by default) | Different models | 8 methods: VoteYesNo, VoteOptions, Majority, Consensus, Probability, Synthesis, Minority, Compose. Blind peer review in round 2. Highest-confidence model writes the synthesis, lowest writes the minority report | Not described; only fallback chains to keep quorum | **High** (same name, same 3-agent voting idea) | "The value is not the verdict. It is the record of the disagreement." | No competing value objectives; no human loop | [jasontc.net](https://jasontc.net/work/magi.html) |
| lordpba/AI_Magi | Open source (Gradio) | 3 | Personas: Melchior = logic, Balthasar = ethics, Casper = practicality; any model via LiteLLM | Synthesis | Not described | **High** (near-identical roles) | Matches MAGI's role split | Hobby project; synthesis rather than vote | [GitHub](https://github.com/lordpba/AI_Magi) |
| Other MAGI clones | OSS: Claude Code plugin (ohta-rh), Android "AI tribunal" (atrix228), pMAGI (nishio), NAGI system (2022) | 3 | Mixed | Tribunal votes; pMAGI uses strong or weak consensus | Not described | High in concept | Shows the Evangelion framing is widely used | Name crowding | [Search summary sources: skillselion](https://skillselion.com/skills/ohta-rh/magi-system/plugins/magi); [gitblind](https://gitblind.noratr.app/atrix228/magi-system); [nishio](https://scrapbox.io/nishio-en/pMAGI-2024-02-04); [Gigazine](https://gigazine.net/gsc_news/en/20221221-nagi-system) |
| Suprmind | Startup, paid ($19–95/mo) | 5 | Different models; assigned positions in Debate mode | Synthesis with consensus map, divergence flags, Disagreement/Correction Index | Not described | **Med-High** | 6 modes incl. Red Team; treats disagreement as a feature | No formal vote or escalation; self-reported metrics | [Suprmind](https://suprmind.ai/hub/platform/) |
| Karpathy llm-council | OSS hack, Nov 2025; about 23.4k stars | N (configurable) | Different models | Anonymous peer ranking, then Chairman synthesis | No | Med | Most-copied reference design | Unsupported; no personas or votes | [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/12/llm-council-by-andrej-karpathy/); [Star History](https://www.star-history.com/karpathy/llm-council) |
| Perplexity Model Council | Incumbent feature, Feb 2026; $200/mo Max | 3 + synthesizer | Different models | Synthesizer shows agreement, divergence and unique insights | No | Med | Distribution, citations, search grounding | Answers questions, does not decide; expensive tier | [Perplexity](https://hub-prod.perplexity.ai/hub/blog/introducing-model-council) |
| MS Copilot Critique / Council | Incumbent, Mar 2026 | 2 (+ judge in Council) | Different models (GPT + Claude) | Reviewer critique; parallel models plus judge | Not described | Med | Enterprise distribution; DRACO claims | Research reports, not decisions | [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research) |
| Grok 4 Heavy | Incumbent, Jul 2025; $300/mo | Several, later reportedly 4 to 16 | Same model, parallel agents | "Study group" sharing of insights, not majority vote | No | Low-Med | About 10x test-time compute | Opaque; slow; costly | [OfficeChai](https://officechai.com/miscellaneous/elon-musk-explains-how-grok4-heavy-xais-multi-agent-reasoning-model-works/) |
| Sup AI | Startup; site "Coming soon" Oct 2026 | 337–339 | Different models | Confidence (entropy) weighting by segment | No | Low-Med | Scale; HLE 52.15% (self-reported) | Status unclear; black box | [FeedBagel](https://feedbagel.com/post/sup-ai-ensemble-system-using-339-llms-to-reduce-hallucinations-scores-5215-on-hu); [sup.ai](https://sup.ai) |
| CollectivIQ | Startup, Boston, Mar 2026 | 4 to 10+ | Different models | Annotated synthesis with agreement and disagreement | Not described | Med | Enterprise; provenance; HLE 53.3% claim | Unverified benchmarks | [Pulse2](https://pulse2.com/collectiviq-profile-john-davie-interview/); [TechEdgeAI](https://techedgeai.com/collectiviq-ai-consensus-platform-claims-higher-accuracy-than-frontier-models/) |
| Triall | Small tool / Colab | 3 | Different models | Blind peer review, then verdict with confidence | No | Med | Evidence-tagged verdict | May not be hosted SaaS | [FutureTools](https://futuretools.io/tools/triall-usp6to) |
| Boardroom AI | iOS app | 2–9 of 25 personas | Personas | Votes on decisions; minutes | Not described (user is the chair) | **Med-High** (votes plus personas) | Board metaphor; votes; minutes | Business personas only; likely one model | [AppFollow](https://apps.appfollow.io/ios/boardroomai-app/6755253237?country=us) |
| Kin | Consumer app | 5 advisors | Personas | Advice; shared memory | No | Med | On-device memory | Coaching, not decisions | [App Store](https://apps.apple.com/us/app/-/id6473448146) |
| ChatHub / Poe / TypingMind | Aggregators | N | Different models | None (side by side) | User judges | Low | Cheap and easy | No reconciliation | [ToolJunction](https://www.tooljunction.io/ai-tools/chathub); [TypingMind docs](https://docs.typingmind.com/manage-and-connect-ai-models/activate-multi-model-responses) |
| Aaru / Simile / Artificial Societies / Electric Twin / Synthetic Users | Funded startups | Thousands of simulated people | Personas from data | Aggregate predicted reactions | Human analyst consumes output | Low (different job: predict, not decide) | Funding; data moats; election accuracy (Aaru) | Validity questions | See Q3 citations |
| Polis / Talk to the City / Remesh / Harmonica | Civic and enterprise deliberation | Humans (AI clusters) | n/a | Bridging consensus, clustering | Humans are the deciders | Low-Med | Legitimacy; tested at scale | AI is not a voter | See Q2 citations |
| Dissent / DebateAI / Turncoat | Debate apps / OSS | 2 to 8 AI personas | Personas or models | AI judges score | No | Low-Med | Training critical thinking | No decision output | See Q2 citations |

- The Solo Creators guide stresses independence: separate fresh chats per persona, because shared context makes advisors converge — [The Solo Creators](https://thesolocreators.com/learn/ai-board-of-advisors/).
- LLM juries can share blind spots, and diversity across model families helps — [Evidently AI](https://evidentlyai.com/blog/llm-judges-jury).
- Arize Phoenix's "LLM Jury" gives each juror a trust weight and records each juror's label for auditing — [Arize docs](https://www.arize.com/docs/phoenix/evaluation/server-evals/code-evaluators/llm-jury.md).

### Inferences
- **Name-collision risk:** "MAGI" is already used by an active open-source library with a public demo (magi-council.org, `magi-core` on PyPI), by a Claude Code plugin, and by several GitHub projects. One of them (AI_Magi) uses the same logic, ethics and practicality split. The hackathon team should cite these as prior art and state clearly how they differ, rather than claim novelty for the three-agent Evangelion council.
- MAGI's real differences from all of the above:
  1. Competing objective functions per agent (science, ethics/safety, creative/practical), not just different models or flavor personas.
  2. Unanimity on concrete proposals, not answer synthesis.
  3. A revise-and-revote loop.
  4. Explicit escalation to a human with a structured handoff.

  None of the cataloged sources describe all four.
- Combining model diversity with persona diversity (each MAGI core running a different provider's model and a different value objective) would address both known failure modes: persona boards that converge because they share one model, and multi-model councils that lack value pluralism.

### Gaps
- Not checked whether Suprmind's Debate mode or Boardroom AI's votes include any deadlock or escalation handling beyond what their pages describe.
- No license details for magi-council or AI_Magi.

---

## Q6. Market signals: is "ask multiple AIs" a viable business or a commodity feature?

### Takeaway
As a standalone consumer answer engine, it is turning into a commodity feature. Perplexity (February 2026), Microsoft (March 2026) and xAI (July 2025) bundled it into premium tiers. Karpathy's free weekend hack has about 23k stars. A well-funded model-comparison startup, Yupp ($33M), shut down in March 2026. The money is in (a) simulating populations (Simile, Aaru) and (b) enterprise trust and provenance positioning (CollectivIQ, Microsoft Critique). That suggests a council's value has to come from governance, auditability and decision workflow, not from accuracy alone.

### Cited Findings
- Yupp raised $33M (a16z crypto) and shut down less than a year after launch (TechCrunch, 2026-03-31) — [TechCrunch](https://techcrunch.com/2026/03/31/yupp-ai-shuts-down-raising-33m-from-a16z-cryptos-chris-dixon/).
- Perplexity Model Council launched 2026-02-05 on the $200/mo Max tier — [Perplexity](https://hub-prod.perplexity.ai/hub/blog/introducing-model-council); [Storyboard18](https://www.storyboard18.com/digital/perplexity-launches-model-council-to-compare-answers-across-multiple-ai-models-89246.htm).
- Microsoft Critique became the default Researcher mode under auto model selection (March 2026) — [Constellation Research](https://www.constellationr.com/insights/news/microsoft-365-copilots-researcher-agent-goes-multi-model).
- Grok 4 Heavy is multi-agent at $300/mo — [AI-TLDR](https://ai-tldr.dev/models/grok-4-heavy/).
- Karpathy's llm-council had about 23.4k stars by July 2026 — [Star History](https://www.star-history.com/karpathy/llm-council).
- Simile: $100M Series A (February 2026) and $200M Series B at $2B (July 2026) — [iTiger](https://www.itiger.com/news/1115874123); [RuntimeWire](https://runtimewire.com/article/simile-raises-200m-series-b-2b-valuation).
- Aaru: $1B headline valuation Series A (December 2025); ARR reportedly under $10M — [TechCrunch](https://techcrunch.com/2025/12/05/ai-synthetic-research-startup-aaru-raised-a-series-a-at-a-1b-headline-valuation).
- Electric Twin about $14M (February 2026); Artificial Societies about $5.3M — [Pulse2](https://pulse2.com/electric-twin-synthetic-audience-ai-platform-secures-14-million-in-funding); [Unite.ai](https://www.unite.ai/?p=264519).
- An outside commentator says CollectivIQ "must demonstrate that the added complexity delivers measurably better outcomes than simply using the best available single model" — [TechBuzz](https://www.techbuzz.ai/articles/collectiviq-aggregates-10-ai-models-to-beat-hallucinations).
- Infrastructure investors describe customers adopting multi-model strategies. Baseten raised a $1.5B Series F on 2026-06-22. This is a market-context claim from an aggregator blog — [Medium (MetaLLM)](https://metallm.medium.com/top-ai-aggregators-in-2026-the-ultimate-guide-to-multi-model-platforms-that-actually-change-how-164c6ae62b91).

### Inferences
- The consumer "ask multiple AIs" wedge is squeezed from above by incumbents bundling it and from below by free open source. Standalone consensus startups (Sup, Suprmind, CollectivIQ) have no disclosed VC rounds in my sources, and Sup's homepage now says "Coming soon." Both point to a hard standalone business.
- For a hackathon pitch, MAGI should present itself as decision governance (who decided what, why, with what dissent, and when a human was pulled in) rather than "a more accurate chatbot." That fits enterprise and Cisco Cloud themes such as auditable change approval, incident triage and policy decisions.

### Gaps
- No revenue or user figures for Suprmind, CollectivIQ, Boardroom AI or Kin.
- Could not confirm whether Sup AI has shut down or is relaunching.

---

## Q7. What does nobody offer that MAGI could add?

### Takeaway
Across about 25 products, none of the sources describe this full combination: agents with competing value objectives (including an ethics/safety agent that can veto), different underlying models, iterative debate with position revision, a unanimous vote on concrete proposals, and a structured human-escalation path with a measured escalation policy. These are the features to build and demo.

### Cited Findings (evidence of the gap)
- Suprmind, the closest commercial product, describes no human-escalation feature — [Suprmind](https://suprmind.ai/hub/platform/).
- MAGI council (Jason Chao) covers voting and minority reports, but its only failure handling is fallback chains to keep quorum. It has no human escalation — [jasontc.net](https://jasontc.net/work/magi.html).
- Perplexity Model Council and Microsoft Council produce syntheses and discrepancy findings for research answers, not decisions on proposals — [Perplexity](https://hub-prod.perplexity.ai/hub/blog/introducing-model-council); [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research).
- Persona-board apps (Boardroom AI) support votes and minutes, but their personas are business-function roles, not competing objectives such as safety versus creativity — [AppFollow](https://apps.appfollow.io/ios/boardroomai-app/6755253237?country=us).
- Suprmind and the LLM-jury literature recommend logging disagreement rather than forcing a majority — [Suprmind](https://suprmind.ai/hub/?p=3065); [Arize](https://www.arize.com/docs/phoenix/evaluation/server-evals/code-evaluators/llm-jury.md).
- All accuracy claims found (Sup, CollectivIQ, Grok Heavy, Microsoft) are self-reported benchmark scores. None reports decision-quality or escalation metrics — [FeedBagel](https://feedbagel.com/post/sup-ai-ensemble-system-using-339-llms-to-reduce-hallucinations-scores-5215-on-hu); [TechEdgeAI](https://techedgeai.com/collectiviq-ai-consensus-platform-claims-higher-accuracy-than-frontier-models/); [AI-TLDR](https://ai-tldr.dev/models/grok-4-heavy/); [Decrypt](https://decrypt.co/362805/microsoft-gpt-claude-work-together-ai-research).

### Inferences (candidate MAGI differentiators)
1. **Human escalation as a first-class output.** When unanimity fails after N rounds, produce an "escalation brief": each core's final position, its reasons for rejecting, what evidence would change its vote, and the minimal question for the human. Nothing in the catalog does this.
2. **Value-pluralist objectives, not just model pluralism.** Scientific, ethical/safety and creative/practical cores with explicit, competing scoring rubrics. An optional safety veto mirrors real governance, such as an IRB or change-advisory board.
3. **Hybrid diversity.** Assign each core a different provider's model as well as a different persona. This guards against single-model persona convergence, which The Solo Creators warns about, and against shared blind spots, which Evidently warns about.
4. **Proposal-level voting with revision history.** Vote on concrete, editable proposals and track how positions moved across rounds (a "position drift" timeline). The closest prior art is magi-council's VoteYesNo/VoteOptions plus minority report.
5. **Escalation calibration as the evaluation metric.** Measure whether escalated cases really are the hard or ambiguous ones, and whether unanimous decisions are more accurate than single-model answers on a labeled set. This avoids the crowded "HLE score" claim.
6. **Enterprise and Cisco Cloud fit.** An auditable decision log (who voted what and why), policy hooks, and a Webex or Slack human-in-the-loop handoff. This pitches MAGI as decision governance infrastructure, a space the funded companies (simulation and research) are not in.
7. **Prior-art honesty.** Acknowledge magi-council.org, AI_Magi and Karpathy's llm-council in the pitch, and show the escalation and competing-objectives delta. Judges who search "MAGI LLM" will find these projects.

### Gaps
- I could not check every small consumer app's internal mechanics, so "nobody offers X" means "not described in any source found." A hidden feature in an app such as Boardroom AI or Suprmind Enterprise may exist.
- No user research found on whether people want an AI system to escalate to them, or prefer a single answer.
