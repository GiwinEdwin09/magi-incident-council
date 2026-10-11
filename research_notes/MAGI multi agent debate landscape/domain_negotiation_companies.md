# Domain-Specific AI Agents That Negotiate or Decide Collectively (Commercial Landscape for a MAGI Pivot)

Research date: 2026-10-10. Scope: companies and products that use autonomous AI agents to negotiate, or to make collective decisions across competing objectives, in a specific domain. General-purpose "ask several AIs" council apps are out of scope (another researcher covers them). Vendor claims are labeled as such. Funding dates come from press releases or secondary databases; where sources disagree, I note it.

## 1. Procurement and supply-chain negotiation agents (Pactum, Keelvar, Fairmarkit, Zip, Arkestro, Levelpath, Didero, Lio, nnamu, commodity/coffee)

### Takeaway
This is the most crowded and best-funded category, with well over $400M raised across the named vendors. Nearly every product, though, is a single buyer-side agent negotiating against a mostly human supplier. The objective function comes from buyer-set policy and limits. The agents do not reconcile competing internal objectives among themselves. Agent-to-agent (bot vs. bot) supplier negotiation is still mostly described as a future direction.

### Cited Findings
**Pactum (Estonia/US): the reference company for autonomous supplier negotiation**
- Series C of $54M led by Insight Partners brought total funding to just over $109M. A secondary database dates it to June 2025, and the Estonian World snippet gives no date. — [Estonian World](https://estonianworld.com/?p=79946); [VCBacked](https://www.vcbacked.co/company/pactum); [Asymmetrix](https://asymmetrixintelligence.substack.com/p/insight-partners-54m-investment-in)
- Earlier rounds: $20M Series B (July 2024, led by Karma Ventures, with Maersk investing; $55M total at the time), $11M Series A (2021, Atomico) and a $3M seed (2020). — [SupplyChain247](https://www.supplychain247.com/article/pactum-ai-raises-20-million-funding-maersk); [Maritime Executive](https://maritime-executive.com/corporate/pactum-raises-11m-series-a-and-enters-global-deployment-phase); [Tech.eu](https://tech.eu/brief/pactum-seed/)
- Pactum is reported to serve more than 50 global enterprises, including Walmart and Maersk. Its largest single autonomous deal was reportedly worth nearly $100M. — [Estonian World](https://estonianworld.com/?p=79946)
- The Walmart pilot (Walmart Canada, early 2021, three months, 89 suppliers of goods-not-for-resale such as shopping carts) closed deals with 64% of suppliers, against a 20% target. Deals took an average of 11 days, with 1.5% average savings and payment terms extended to 35 days. — [Talk Business & Politics](https://talkbusiness.net/2023/06/the-supply-side-generative-ai-or-chatgpt-next-holy-grail-for-retailers-suppliers/)
- Pactum's own January 2023 release reported 68% of approached suppliers closing deals and 3% average savings for Walmart. These numbers measure broader use after expansion and differ from the pilot figures. In the same release, 83% of suppliers called the bot easy to use. — [BusinessWire / Pactum](https://www.businesswire.com/news/home/20230111005148/en/Pactums-Autonomous-Negotiation-Technology-on-Display-at-the-National-Retail-Federations-2023-Retail-Big-Show)
- Bloomberg-sourced reporting says about 75% of Walmart suppliers preferred negotiating with the bot over a human. — [Engadget](https://www.engadget.com/walmarts-suppliers-would-rather-negotiate-with-ai-than-a-human-162131831.html); [PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2023/walmart-finds-75-percent-vendors-prefer-negotiating-with-chatbot/partial/)
- How it works: a buyer-side agent decides whether a request is negotiable, then opens a text chat with the supplier to trade terms such as price and payment terms. It can run thousands of negotiations at once. The CEO has described bot-to-bot negotiation as a possible future, not a shipped product. — [Grocery Dive](https://www.grocerydive.com/news/the-startup-thats-automating-supplier-negotiations-for-walmart/591407/); [HumanProgress](https://humanprogress.org/contract-negotiation-bots-could-soon-be-on-both-sides-of-the-table/)
- The 2026 product lineup includes a Negotiation Suite (price, payment terms, lead time, within buyer-defined limits), Automated Tactical Sourcing "with buyer oversight", a Requisition Alignment Agent and Supplier Campaigns. Pactum showcased these at World Procurement Congress, May 2026. — [Procurement Magazine](https://procurementmag.com/news/pactum-transforms-procurement-with-its-agentic-ai-platform); [agentcommunity.org](https://agentcommunity.org/m/pactum); [Pactum WPC page](https://pactum.com/world-procurement-congress-london)
- A third-party site reports, from company claims, that Pactum is deploying agents on more than $529M of supplier contracts for Fortune Global 2000 companies. — [SAMsearch](https://samsearch.co/government-contracting-news/pactum-utilizes-ai-agents-to-revolutionize-supplier-negotiations-for-major-corporations-120405)

**Lio (Munich, formerly askLio)**
- Raised a $30M Series A led by a16z on March 5, 2026, bringing total funding to $33M. Its agents triage requests, analyze quotes, compare suppliers, negotiate, onboard vendors and execute purchases end to end. — [TechCrunch](https://techcrunch.com/2026/03/05/lio-ai-series-a-a16z-30m-raise-automate-enterprise-procurement/); [Pulse 2.0](https://pulse2.com/lio-30-million-raised-for-agentic-ai-enterprise-procurement-platform)

**Didero (New York)**
- Raised a $30M Series A on February 12, 2026, co-led by Chemistry and Headline, with M12 (Microsoft) participating. Total funding is about $37M. Its agents sit inside email and ERP to handle supplier communications, order tracking and exception management for manufacturers and distributors. — [SiliconANGLE](https://siliconangle.com/2026/02/12/didero-raises-30m-series-expand-agentic-ai-enterprise-procurement/); [Digital Commerce 360](https://www.digitalcommerce360.com/2026/02/20/didero-30-million-funding-ai-procurement/)

**Arkestro (predictive procurement, game theory)**
- Raised $36M on May 14, 2025, led by Altira Group and Aramco Ventures, with NEA, KDT and Activant participating. One aggregator puts total funding at about $78M. — [StreetInsider / PRNewswire](https://www.streetinsider.com/PRNewswire/Arkestro+Secures+%2436M+in+Strategic+Investment+to+Accelerate+Predictive+Procurement+Innovation/24794849.html); [Supply Chain Digital](https://supplychaindigital.com/news/arkestro-to-accelerate-predictive-procurement-innovation)
- Arkestro combines AI, behavioral science and game theory, which it calls "Negotiation Science, Supplier Science, Process Science". It claims an average 18.8% savings per $1M of spend (vendor claim). Reviewers note friction on the supplier side. — [Supply Chain Digital](https://supplychaindigital.com/news/arkestro-to-accelerate-predictive-procurement-innovation); [rfp.wiki](https://www.rfp.wiki/vendors/arkestro)

**Keelvar (Cork, Ireland): sourcing optimization and "Autonomous Sourcing" bots**
- Raised a $24M Series B in May 2022, led by 83North, for $43M total, and an $18M Series A in June 2020. — [BusinessWire](https://www.businesswire.com/news/home/20220516005111/en/Keelvar-Raises-$24M-to-Usher-in-Next-Generation-of-Intelligent-Sourcing-Technology); [TechCrunch](https://techcrunch.com/2020/06/04/sourcing-software-provider-keelvar-raises-18m-from-elephant-and-mosaic)

**Levelpath**
- Raised more than $55M in a Series B (June/July 2025) led by Battery Ventures, with Redpoint, Benchmark and others, for about $100M total. The money is earmarked for "autonomous AI agents for enterprise procurement". — [Goodwin](https://www.goodwinlaw.com/en/news-and-events/news/2025/07/announcements-technology-goodwin-represents-levelpath-on-its-over); [Levelpath newsroom](https://www.levelpath.com/company/newsroom)

**Fairmarkit (Boston): tail-spend sourcing**
- Raised a $30M Series B in December 2020. A $35.6M Series C led by OMERS Growth Equity appears in a secondary dossier with an unclear date, and total funding there is listed as about $77.5M. Fairmarkit now markets a "suite of AI agents managing demand to award". — [BusinessWire](https://www.businesswire.com/news/home/20201210005088/en/Fairmarkit-raises-%2430M-Series-B-to-Expand-AI-Powered-Procurement-Platform-for-the-Fortune-500-and-Beyond); [Clay dossier](https://www.clay.com/dossier/fairmarkit-funding)

**Zip (San Francisco): intake-to-procure orchestration**
- In June 2025 Zip launched 50+ AI agents across procurement, finance, legal, IT and security, including Renewal Assist, DORA Assessment and Adverse Media. It calls the category "agentic procurement orchestration". — [BusinessWire](https://www.businesswire.com/news/home/20250610972074/en/Zip-Unveils-Suite-of-50-AI-Agents-to-Automate-High-Impact-Tasks-Across-Finance-Legal-Procurement-IT-and-Security); [Procurement Magazine](https://procurementmag.com/news/zips-50-ai-agents-transform-procurement-automation)
- Zip later added "Superagents" that reason, plan and coordinate many task-level agents inside Zip, with governance and audit trails. This is a hierarchical orchestrator, not peer negotiation. — [Zip blog](https://zip.com/blog/what-are-zip-superagents)

**nnamu (Munich; acquired by Beroe)**
- A game-theory AI negotiation agent. Beroe acquired it on March 17, 2025 and set up the subsidiary "Beroe X nnamu GmbH". It is trained on 2,000+ negotiations worth more than €400B (a later Beroe guide says 3,000+, so the sources disagree). It claims more than 12% savings on office supplies for one mobility company. — [Enterprise Times](https://www.enterprisetimes.co.uk/2025/03/21/beroe-brings-game-theory-to-procurement-with-nnamu-acquisition/); [Beroe](https://www.beroeinc.com/resource-centre/news/beroe-acquires-nnamu-turbocharge-procurement-negotiations-game-theory-and-ai/)

**Commodity and coffee-adjacent**
- **Helios**: an AI platform for ag-commodity procurement teams and traders. It has a $4.7M seed and claims price and climate-risk prediction for 75 ag commodities across 90 countries. Its multi-agent product, Helios Horizon, answers procurement questions in minutes. — [AgFunderNews](https://agfundernews.com/helios-taps-ai-agents-for-ag-insights-at-worst-time-for-procurement-pros)
- **Sourcerer**: agents that source suppliers, negotiate terms, compute landed cost and arrange freight. It acts as the supplier or distributor itself rather than selling SaaS, and so takes on supplier-failure risk. — [Runtime Wire](https://runtimewire.com/article/startup-spotlight-sourcerer-wants-to-turn-ai-procurement-into-a-supplier-not-saa)
- Nestlé's head of commodity research says coffee risk is driven mostly by short-term weather shocks (frost and drought in Brazil). Cocoa faces structural supply problems. Nestlé runs Monte Carlo simulations on price risk. — [Vesper podcast notes](https://vespertool.com/blog/new-strong-source-podcast-with-corinna-olearo-head-of-commodity-research-price-risk-management-at-nestle-on-riding-the-commodity-rollercoaster/)

**Academic evidence on agent-vs-agent negotiation**
- MIT Sloan ran an international competition with more than 180,000 negotiations between prompt-engineered LLM agents, across chair purchase, rental and job-offer scenarios. Warmth was associated with better outcomes and dominance helped claim value. Chain-of-thought, prompt injection and strategic concealment showed dynamics that classic negotiation theory does not explain. An earlier version reported a warmth/value-claiming trade-off, so the findings shifted between versions. — [arXiv 2503.06416](https://arxiv.org/abs/2503.06416v1); [MIT Sloan](https://mitsloan.mit.edu/ideas-made-to-matter/surprising-power-warmth-ai-negotiations)

### Inferences
- Every procurement product found uses one buyer agent (or an orchestrated swarm of task agents) facing a counterparty. "Competing objectives" are collapsed into buyer-configured policy: target price, walk-away, acceptable trade-offs. None of the reviewed sources describes internal agents (for example cost vs. sustainability vs. supply continuity) negotiating a joint buyer position among themselves, or preserving dissent for a human. That is a plausible white space, but my searches cannot prove no one does it.
- The Walmart pilot numbers (64% deal rate vs. a 20% target, 1.5% savings, 11-day average, payment terms to 35 days) give MAGI realistic magnitudes and a credible baseline framing ("vs. single-agent buyer bot").
- Commodity and coffee procurement has forecasting and analytics players (Helios) but no clear agentic negotiation player turned up. A coffee-procurement MAGI is less directly crowded than generic indirect-spend negotiation.
- The MIT finding that prompt injection and strategic concealment matter in agent-vs-agent bargaining suggests a MAGI demo could show resistance to manipulation by a supplier agent. That is a differentiator the established vendors don't publicize.

### Gaps
- Exact date of Pactum's $54M Series C is not confirmed by a primary source. A "71% of client negotiations fully automated" figure appeared in a search summary, but I could not tie it to a specific source.
- The launch date of Keelvar's "Autonomous Sourcing" product, and whether it raised funding after 2022, were not found.
- Fairmarkit's Series C date and lead investor are only from a secondary dossier with inconsistent dates.
- No confirmed production case was found of a buyer agent negotiating against a supplier-side AI agent in procurement. Pactum frames it as future and Luminance claims it for legal contracts (see section 4).

## 2. Energy and grid: VPP orchestration and autonomous energy trading

### Takeaway
Autonomous energy-trading and VPP agents exist commercially: Tesla Autobidder (established) plus a wave of small 2025-2026 startups. They are single-optimizer systems with human-set multi-objective parameters. They are not negotiating agent committees. Multi-objective trade-offs (revenue vs. battery state-of-charge vs. risk) are encoded as operator parameters, which is the clearest structural analog to MAGI's competing objectives.

### Cited Findings
- **Tesla Autobidder** is a real-time trading and control platform for battery assets. It is part of Tesla's "Autonomous Control" suite and runs at Hornsdale Power Reserve in South Australia. It works at every scale, from aggregated residential batteries to 100 MW utility installations. — [Tesla Autobidder](https://www.tesla.com/support/energy/tesla-software/autobidder)
- Tesla says Autobidder trades using a numerical optimization model "based on the parameters set and adjusted by a human operator". Its March 2026 submission to the Australian Energy Regulator (AER) says operators set price thresholds, state-of-charge limits and multi-objective priorities. — [Tesla Autobidder](https://www.tesla.com/support/energy/tesla-software/autobidder); [Tesla submission to AER, 31 Mar 2026](https://www.aer.gov.au/system/files/2026-06/Tesla%20-%20Submission%20to%20the%20Rebidding%20and%20Technical%20Parameters%20Guideline%20Review%20Consultation%20Paper%20-%2031%20March%202026.pdf)
- A 2026 analytical framework on risks of multi-agent systems deployed across organizational boundaries cites autonomous market-bidding systems such as Autobidder as existing examples. — [arXiv 2608.26626](https://arxiv.org/pdf/2608.26626)
- **Shatterdome Energy** raised a $3.5M pre-seed in May 2026, led by Crucible Capital with Transpose Platform and Entrepreneurs First. Its autonomous system ingests real-time grid data, decides when to produce, store or sell, and executes trades programmatically. It claims 200 MWh moved within three months and a 1.5 GW asset pipeline (company claims). — [BusinessWire](https://www.businesswire.com/news/home/20260521179921/en/Shatterdome-Energy-Raises-%243.5-Million-in-Pre-Seed-Funding); [DCD](https://www.datacenterdynamics.com/en/news/shatterdome-raises-35m-to-build-ai-platform-for-power-market-trading/)
- **Capalo AI** (Helsinki) raised a €3.8M seed in March 2025, led by VentureFriends and PROfounders. Its "Zeus VPP" aggregates distributed batteries into one virtual battery and trades stored energy and capacity across electricity markets. — [AIN](https://en.ain.ua/2025/03/19/capalo-ai-raises-eur38m)
- **GreenVoltis** (Stockholm) is listed as an AI-native VPP aggregation and multi-market optimization platform. — [Caplight profile](https://www.caplight.com/company/greenvoltis). Caution: a search summary credited GreenVoltis with "$16M Series A led by BlackRock and Fin Capital". That text matches a site-wide banner about Caplight's own funding, which also appeared on Caplight's Arkestro page. The GreenVoltis funding figure is likely a misattribution and should not be used.
- Smart-grid VC funding reached $373M across 14 deals in Q1 2026, vs. $346M across 18 deals in Q1 2025 (Mercom). — [Mercom](https://www.mercomindia.com/shatterdome-energy-raises-3-5m-pre-seed-funding)

### Inferences
- Energy has real numbers (prices, state of charge, MW) and real competing objectives (revenue, battery degradation, grid reliability, carbon). Yet the commercial pattern is one optimizer with human-set weights. A MAGI demo in which a reliability agent, a cost/revenue agent and a sustainability agent negotiate a bid would differ structurally. But energy-market judges would expect hard real-time optimization, and an LLM debate is slow and hard to justify there.
- Energy is less natural than procurement for a Cisco AGNTCY track, given the coffee reference app.

### Gaps
- I found no source on Octopus Energy's Kraken platform or its VPP agent architecture.
- No commercial energy product was found that uses several LLM agents debating or voting. All products found are optimization-based.

## 3. Finance: multi-agent investment committees and AI hedge funds with agent debate

### Takeaway
The bull/bear/risk debate pattern has already been productized (Boosted.ai's Alfa Prime), open-sourced (TradingAgents) and cloned in many hackathon entries. It is the most saturated "agents debate" pattern in a vertical. Notably, Boosted.ai already treats convergence vs. sustained disagreement as a signal, which overlaps with MAGI's "preserve disagreement" idea.

### Cited Findings
- **Boosted.ai "Alfa Prime"** is a multi-model AI investment committee that combines signal monitoring, research agents and structured debate between independent AI models. Bull, bear and moderator views draw on filings, transcripts and research. A moderator evaluates where the models agree or disagree, and why. Rapid convergence is said to signal a more strongly supported thesis, and sustained disagreement highlights uncertainty. It claims to find higher-quality opportunities at about twice the rate of the baseline analyst workflow (self-reported). It is initially limited to select institutional partners. Positioning: "AI committee debates, challenges, recommends; people direct and decide." — [TechIntelPro](https://techintelpro.com/news/ai/agentic-ai/boostedai-introduces-multi-model-ai-investment-committee); [01net](https://www.01net.it/boosted-ai-introduces-a-multi-model-ai-investment-committee-for-select-institutional-partners/)
- **TradingAgents** (UCLA, MIT and Tauric Research; ICML 2025) has seven roles: four analysts (fundamentals, sentiment, news, technicals), bull and bear researchers in an adversarial debate, a trader, a risk-management team and a fund manager. It reports gains in cumulative return, Sharpe ratio and max drawdown over baselines. These are self-reported backtests that have been questioned for lack of live-capital validation. The code is open source. — [arXiv 2412.20138](https://arxiv.org/abs/2412.20138v6); [Hugging Face Papers](https://huggingface.co/papers/2412.20138)
- **Debate-Verdict** (Product Hunt launch) runs a Bull vs. Bear vs. independent Judge debate. The judge checks claims against SEC EDGAR and Yahoo Finance data. — [Product Hunt](https://www.producthunt.com/products/debate-verdict/makers)
- Hackathon clones of the same pattern include **Quorum**, a ten-agent committee in which bull and bear must rebut each other, the Risk Officer has a compliance gate and deadlocks escalate to a Chief Risk Officer. **Senatus AI** has a BearAnalyst that files an "AVOID motion" and a human chair with final authority. — [lablab.ai Quorum](https://lablab.ai/ai-hackathons/band-of-agents-hackathon/dem-ai/quorum-a-self-assembling-ai-investment-committee); [lablab.ai Senatus](https://lablab.ai/submissions/t43aig9ya8j9yw9p9x4fvh1x)

### Inferences
- A MAGI finance pivot would look derivative of TradingAgents and Boosted.ai, and of several hackathon submissions with nearly identical escalate-to-human designs. Judges who know the space may see it as a clone.
- Boosted.ai's "convergence = confidence, persistent disagreement = uncertainty" framing is the closest commercial analog to MAGI's "preserve disagreement" principle. MAGI should present that as an established idea it applies to a new domain, not as a novel invention.

### Gaps
- Funding and traction for Boosted.ai's Alfa Prime specifically, and the exact launch date, were not confirmed (the press appears to be 2026).
- I found no credit-committee multi-agent product (lending approval via agent debate) in the searches run.
- No live-capital, independently audited performance was found for any debate-based trading system.

## 4. Healthcare, legal, IT/network change approval, security (SOC) and emergency response

### Takeaway
- **Healthcare:** multi-agent panels exist (Hippocratic AI's constellation, Microsoft/Stanford tumor board work, hospital pilots), but they are cooperative specialist panels checking a primary agent, not agents with competing objectives.
- **Legal:** this is the one domain with a commercial claim of true agent-to-agent negotiation (Luminance). AI mock-jury startups simulate group deliberation.
- **Network change approval:** Cisco's own Swisscom/Outshift work is a multi-agent validator built on a digital twin.
- **SOC:** startups orchestrate multiple agents, but none was found that uses consensus voting.
- **Emergency response:** no commercial multi-agent product was found, only hackathon projects and academic work.

### Cited Findings
**Healthcare**
- **Hippocratic AI's Polaris** is a "constellation" with a primary conversational LLM agent plus several specialist agents that supply task-specific context and safety checks. — [arXiv 2403.13313](https://arxiv.org/html/2403.13313v1)
- Polaris 3.0 uses 22 specialized models (4.2T parameters total) and claims 99.38% clinical accuracy, vs. 98.75% for 2.0 and 96.79% for 1.0 (company claims). The company says single-model prototypes plateaued at about 80% because of inconsistency, and that "treating safety as a system" fixed it. — [Hippocratic AI Polaris 3](https://hippocraticai.com/polaris-3/); [Hippocratic AI engineering blog](https://hippocraticai.com/building-ai-for-healthcare-conversations-part-2/)
- **Microsoft Research and Stanford** built a multi-agent system for the Stanford Thoracic Tumor Board, with a deployed automated chart-summarization tool. — [Microsoft Research](https://www.microsoft.com/en-us/research/?p=1169017)
- A **Tampa General** myelodysplastic-syndromes virtual tumor board (SOHO 2025) uses moderator, diagnostic, prognostic, treatment and clinical-trial agents. On 30 generated cases it outperformed general-purpose LLMs, which the presenter called early evidence. — [VJHemOnc](https://www.vjhemonc.com/video/r8db3p6tdoa-evaluating-ai-driven-virtual-tumor-boards-in-mds/)
- **ML6** (consultancy) built a multi-agent "AI-based tumor board" for the International Leukemia/Lymphoma Tumor Board. — [ML6](https://www.ml6.eu/en/blog/the-ai-based-tumor-board-a-multi-agent-approach-to-finding-cancer-treatments-with-ai)
- Hackathon tumor boards are common, for example OncoBoard.ai (seven agents, human gates) and the Autonomous Oncology Board (pathologist, researcher and oncologist agents). — [lablab.ai OncoBoard](https://lablab.ai/ai-hackathons/milan-ai-week-hackathon/oncoboard-ai/oncoboardai); [lablab.ai AOB](https://lablab.ai/ai-hackathons/amd-developer/syntroph/autonomous-oncology-board-aob)

**Legal**
- **Luminance** ("Autopilot", now "Autonomous Negotiation"): in November 2023 it demonstrated its AI negotiating an NDA with another AI, with no human involved until signature. — [CNBC](https://www.cnbc.com/2023/11/07/ai-negotiates-legal-contract-without-humans-involved-for-first-time.html)
- Luminance markets itself as "the legal industry's only 100% AI autonomous contract negotiation tool" (vendor claim). A 2026 upgrade shows "the why behind every decision", retains negotiation history and institutional memory, and opens the tool to non-lawyers while Legal keeps governance. — [Luminance press](https://www.luminance.com/press/luminance-enhances-the-legal-industrys-only-100-ai-autonomous-contract-negotiation-tool-to-show-the-why-behind-every-decision-and-opens-it-to-the-entire-enterprise/); [Luminance Autonomous Negotiation](https://www.luminance.com/autonomous-negotiation/)
- **Courtroom** (New York) came out of stealth in June 2026 with a pre-seed led by Neo and Precursor Ventures (plus Rel Labs, Relativity's investment arm). It simulates AI juries and judges, claims more than 90% accuracy (unverified) and says AmLaw 100 firms and Fortune 1000 companies use it. — [BusinessWire](https://www.businesswire.com/news/home/20260611125975/en/); [Pulse 2.0](https://pulse2.com/courtroom-emerges-from-stealth-with-pre-seed-funding-to-bring-ai-jury-and-judge-simulations-to-litigation-teams/)
- **Viewpoints.ai** simulates jurors matched to a venue's jury pool, including group deliberations among simulated jurors, and produces verdict and damages distributions. It is based on research by Stanford media psychologists. — [Legal Technology Hub](https://www.legaltechnologyhub.com/vendors/viewpoints-ai/)
- A 2026 UNT Dallas Law Review study found that GPT-4, Claude and Gemini repeatedly failed to replicate real juror reasoning, while fine-tuning on actual mock-juror data improved alignment. — [UNT Dallas Law Review](https://onthecusp.untdallas.edu/docs/2026/michaelscottisnotajuror.pdf)

**IT/network change approval (Cisco's own territory)**
- **Swisscom and Cisco Outshift:** after a config error that passed lab tests caused a production outage, they built a multi-agent validation pipeline with a Network Digital Twin and an "Agentic Network Validator". Cisco says the system reproduced and would have prevented the exact outage within four months (Cisco-authored case study). — [Outshift case study](https://outshift.cisco.com/case-studies/swisscom-agentic-ai-network-reliability); [Outshift blog](https://outshift.cisco.com/blog/swisscom-oushift-network-change-management)
- The **Aether** paper (2026; authors include Carofiglio of Cisco and Gysi of Swisscom) describes five specialized NetOps agents that cover change validation from intent analysis to verification. It reports 100% error detection, 92-96% diagnostic coverage and 6-7 minute runs, on synthetic scenarios plus past ISP incidents. — [arXiv 2604.18233](https://arxiv.org/pdf/2604.18233); [Cisco Live BRKNWT-2502](https://www.ciscolive.com/c/dam/r/ciscolive/global-event/docs/2025/pdf/BRKNWT-2502.pdf)

**Security operations (SOC)**
- **Mate Security** reportedly raised a $35M Series A in 2026 (dated July 2026 by Seedtable). It claims more than 500% growth since Q3 2025 and lets "agents close the loop" while people keep material decisions. — [Seedtable](https://seedtable.com/companies/mate-security/funding-rounds/series-a-2026-07)
- **7AI** is described as focused on multi-agent orchestration for triage, enrichment and investigation. Dropzone AI, Prophet Security and Reach Security are listed as triage-agent companies. — [Intezer roundup](https://intezer.com/top-15-ai-soc-platforms-in-2026/); [UnderDefense](https://underdefense.com/blog/ai-soc-analyst/)
- **CrowdStrike** announced coordinated multi-agent investigation across endpoint, identity, SaaS, cloud and network on September 2, 2026 (incumbent). — [CrowdStrike](https://www.crowdstrike.com/en-us/press-releases/crowdstrike-unveils-next-evolution-of-the-agentic-soc/)
- The verification practice described is human sampling (Tier-2 reviewing 10-20% of AI verdicts weekly), not agent consensus. — [UnderDefense](https://underdefense.com/blog/ai-soc-analyst/)

**Emergency and disaster response**
- No commercial startup was found. Hackathon projects include CrisisMind (rescue, medical, food and shelter agents plus a commander) and Mission Control (five agents using USGS, OSM and weather feeds). — [lablab.ai CrisisMind](https://lablab.ai/ai-hackathons/band-of-agents-hackathon/crisismind-ai/crisismind-multi-agent-disaster-response-system); [lablab.ai Mission Control](https://lablab.ai/ai-hackathons/amd-developer-hackathon-act-ii/shikigamis/mission-control-earthquake-response)
- Academic work: a University of Wollongong decentralized multi-agent system for allocating rescue resources across concurrent emergencies (AAMAS 2016 demo). — [UOW](https://ro.uow.edu.au/eispapers/6507); [AAMAS 2016](https://ifaamas.csc.liv.ac.uk/Proceedings/aamas2016/pdfs/p1482.pdf)

### Inferences
- Healthcare panels are cooperative: agents check each other toward one shared goal. MAGI's genuinely competing objectives would be a conceptual difference, but clinical validation and safety make healthcare a poor hackathon fit, and tumor-board hackathon entries are already common.
- Luminance is the strongest commercial precedent for true agent-to-agent negotiation with auditability ("show the why"). MAGI could cite it as validation that explainable agent negotiation is commercially valued.
- The Swisscom case shows that Cisco Outshift already invests in multi-agent change validation, which aligns with the judges. But its agents are cooperative pipeline stages (intent, then twin, then verification), not stakeholders with competing objectives. A MAGI framing of "availability vs. security vs. change-velocity agents negotiating a change window" would extend Cisco's own work rather than duplicate it. There is a risk it reads as derivative of Cisco's internal project.
- Multi-agent disaster response is a recurring hackathon trope with no commercial anchor. It would likely score as unoriginal.

### Gaps
- No funded startup was found that runs virtual tumor boards or multi-specialist panels as its core product (most work is academic, big-tech or hackathon). Microsoft MAI-DxO was named in the brief but not re-verified here.
- I found no SOC product that uses explicit multi-agent voting or consensus on verdicts.
- No AI contract-negotiation competitor to Luminance was researched in depth.
- No commercial logistics-dispatch agent-negotiation product was found in the searches run.

## 5. Agent-to-agent commerce and negotiation protocols (A2A/AP2, Fetch.ai, Olas, Cisco AGNTCY coffee reference app)

### Takeaway
The plumbing for agents negotiating on behalf of different principals is being standardized (Google AP2 on A2A/MCP, Olas, Fetch.ai), and Cisco's own CoffeeAGNTCY reference app already models a coffee supply chain with a supervisor broadcasting to farm agents, auction style. These provide transport, identity and payment mandates, not the deliberation logic among agents with competing objectives. That is the layer MAGI could occupy.

### Cited Findings
- **Google AP2** (Agent Payments Protocol) was launched on September 16, 2025 as an open protocol that can extend A2A and MCP. More than 60 organizations backed it at launch, including Mastercard, AmEx, PayPal, Coinbase, Etsy and Salesforce. — [TechCrunch](https://techcrunch.com/2025/09/16/google-launches-new-protocol-for-agent-driven-purchases); [The Paypers](https://thepaypers.com/payments/news/google-launches-agent-payments-protocol-ap2)
- AP2 relies on cryptographically signed "mandates". The Intent Mandate holds the user's instruction and constraints such as budget caps. The Cart Mandate locks items, price and terms. The Payment Mandate signals agent involvement to the payment network. In the human-not-present flow, the agent negotiates autonomously within Intent Mandate constraints. — [RisingWave explainer](https://risingwave.com/blog/agent-payments-protocol-ap2-explained/); [ArthurChiao guide](https://arthurchiao.art/blog/ap2-illustrated-guide/)
- One secondary source claims Google donated AP2 to the FIDO Alliance in April 2026. This is unverified. — [RisingWave](https://risingwave.com/blog/agent-payments-protocol-ap2-explained/)
- **Fetch.ai** "Autonomous Economic Agents" negotiate and transact peer to peer. The documented supply-chain work is an academic prototype: the Cambridge "A2SC" system covers procurement, transport monitoring, negotiation and inventory, built on Fetch.ai's framework. A collaboration with Festo is mentioned. — [Fetch.ai blog](https://fetch.ai/blog/fetch-ai-pioneering-autonomous-supply-chains); [Sheffield PITCH-IN](https://pitch-in.sites.sheffield.ac.uk/projects/demonstrating-feasibility-of-autonomous-supply-chains-with-iot)
- **Olas (Autonolas, Valory)** raised $13.8M in February 2025, led by 1kx, to launch Pearl, an "agent app store". It supports "decentralized multi-operator consensus agents", where one agent service runs across instances held by different operators that reach consensus. Its Mech Marketplace lets agents hire each other. It claims more than 3.5M agent transactions across nine chains. — [SiliconANGLE](https://siliconangle.com/2025/02/05/olas-raises-13-8m-launch-decentralized-app-store-ai-agents/); [The Block](https://www.theblock.co/post/338713/olas-raises-13-8-million-to-launch-pearl-an-app-store-for-autonomous-ai-agents-in-crypto)
- **Cisco Outshift's CoffeeAGNTCY** is an open-source multi-agent reference app for a "fictional global coffee enterprise". It shows MCP, A2A and AGNTCY components working together.
  - "Corto" is a simple A2A sommelier demo. "Lungo" is a full multi-agent supply-chain simulation.
  - In Lungo, a supervisor agent talks to farm agents. An "auction supervisor" sends the same request to multiple farm agents and waits for all responses, over NATS or SLIM transports.
  - Identity badges are verified (Ory Hydra) before a farm handles an order.
  - Sources: [Outshift blog](https://outshift.cisco.com/blog/multi-agentic-systems-agntcy-application-sdk-reference-application); [AGNTCY docs: get started](https://docs.agntcy.org/coffee-agntcy/get-started/); [SLIM docs](https://docs.agntcy.org/coffee-agntcy/slim-coffee-agntcy/); [Identity docs](https://docs.agntcy.org/coffee-agntcy/identity-coffee-agntcy/)
- **Lungo+** (a community Devpost project) extends Lungo with a scout agent that queries farms in parallel and a market agent that runs competitive bidding. — [Devpost Lungo+](https://devpost.com/software/lungo)

### Inferences
- CoffeeAGNTCY's Lungo already has farm-side agents and a central auction supervisor. A MAGI coffee pivot could sit on the buyer side as a decentralized committee that replaces the single supervisor: cost, sustainability/risk and delivery agents with private data, negotiating which farm bids to accept and re-planning when a farm agent fails. That reuses the judges' own reference architecture while demonstrating the Level-3 criterion of "no central decider", which Lungo's supervisor does not meet.
- Lungo+ shows other hackathon teams are already extending CoffeeAGNTCY with bidding. A coffee pivot will not be unique on domain alone. Its differentiation has to come from internal multi-objective deliberation, preserved dissent and a measured baseline.
- AP2's Intent Mandate (constraints a human pre-authorizes) is a natural formalism for MAGI's "when to escalate to a human": escalate when the negotiated outcome would exceed the mandate's bounds.

### Gaps
- I did not verify whether Cisco has a newer CoffeeAGNTCY release that already includes multi-objective buyer deliberation. The current docs reviewed show supervisor-to-farm patterns only.
- I found no production deployment data for Fetch.ai supply-chain negotiation.
- The AP2-to-FIDO governance change is unverified.

## 6. Synthesis: similarity to MAGI, what makes incumbents stand out, and where a MAGI pivot would be novel vs. crowded

### Takeaway
Crowded areas:
- Buyer-vs-supplier autonomous negotiation (Pactum and seven or more funded rivals).
- Bull/bear investment-committee debate (Boosted.ai, TradingAgents, many hackathon clones).
- Specialist medical panels.
- Multi-agent disaster-response demos.

Comparatively open:
- Intra-organization negotiation among agents that each own a competing objective and private data.
- No central decider.
- Explicitly preserved dissent and evidence-triggered human escalation.
- A measured baseline comparison.

That combination maps cleanly onto Cisco's own CoffeeAGNTCY supply-chain scenario.

### Cited Findings
- Incumbents stand out on real deployment data and ROI claims: Pactum/Walmart (64% deal rate, 1.5% savings in the pilot; 68%/3% later), Arkestro (18.8% savings claim), nnamu (12%+ savings claim), Polaris (99.38% accuracy claim), Boosted.ai (about 2x the baseline analyst hit rate). — [Talk Business](https://talkbusiness.net/2023/06/the-supply-side-generative-ai-or-chatgpt-next-holy-grail-for-retailers-suppliers/); [BusinessWire/Pactum](https://www.businesswire.com/news/home/20230111005148/en/Pactums-Autonomous-Negotiation-Technology-on-Display-at-the-National-Retail-Federations-2023-Retail-Big-Show); [Supply Chain Digital](https://supplychaindigital.com/news/arkestro-to-accelerate-predictive-procurement-innovation); [Enterprise Times](https://www.enterprisetimes.co.uk/2025/03/21/beroe-brings-game-theory-to-procurement-with-nnamu-acquisition/); [Hippocratic AI](https://hippocraticai.com/polaris-3/); [TechIntelPro](https://techintelpro.com/news/ai/agentic-ai/boostedai-introduces-multi-model-ai-investment-committee)
- Human approval gates and auditability are standard selling points:
  - Pactum agents operate within buyer-defined limits, with buyer oversight. — [agentcommunity.org](https://agentcommunity.org/m/pactum)
  - Luminance shows "the why" behind each decision, and Legal keeps governance. — [Luminance](https://www.luminance.com/press/luminance-enhances-the-legal-industrys-only-100-ai-autonomous-contract-negotiation-tool-to-show-the-why-behind-every-decision-and-opens-it-to-the-entire-enterprise/)
  - Zip Superagents provide governance and audit trails. — [Zip](https://zip.com/blog/what-are-zip-superagents)
  - Boosted.ai: "people direct and decide". — [01net](https://www.01net.it/boosted-ai-introduces-a-multi-model-ai-investment-committee-for-select-institutional-partners/)
  - Tesla Autobidder works within operator-set multi-objective priorities. — [Tesla AER submission](https://www.aer.gov.au/system/files/2026-06/Tesla%20-%20Submission%20to%20the%20Rebidding%20and%20Technical%20Parameters%20Guideline%20Review%20Consultation%20Paper%20-%2031%20March%202026.pdf)
- The documented architectures nearly always have a central decider: Zip Superagents (orchestrator), Polaris (primary agent), TradingAgents (fund manager), Quorum (Chief Risk Officer) and CoffeeAGNTCY Lungo (auction supervisor). — [Zip](https://zip.com/blog/what-are-zip-superagents); [arXiv 2403.13313](https://arxiv.org/html/2403.13313v1); [arXiv 2412.20138](https://arxiv.org/abs/2412.20138v6); [lablab.ai Quorum](https://lablab.ai/ai-hackathons/band-of-agents-hackathon/dem-ai/quorum-a-self-assembling-ai-investment-committee); [AGNTCY docs](https://docs.agntcy.org/coffee-agntcy/slim-coffee-agntcy/)
- The exception is Olas, whose "multi-operator consensus agents" are decentralized at the infrastructure and blockchain level. That decentralization is about operators reaching consensus on the same agent's state, not about competing objectives. — [SiliconANGLE](https://siliconangle.com/2025/02/05/olas-raises-13-8m-launch-decentralized-app-store-ai-agents/)

### Catalog table (one row per company or product)

| # | Company / product | Domain | URL | Funding / traction (as found) | How agents negotiate or decide | Similarity to MAGI |
|---|---|---|---|---|---|---|
| 1 | Pactum | Procurement | pactum.com | ~$109M total; $54M Series C (Insight; date likely 2025); Walmart, Maersk, 50+ enterprises | One buyer agent chats with suppliers within buyer limits; escalates | Medium: negotiation, single objective |
| 2 | Lio | Procurement | lio.ai (assumed) | $30M Series A, a16z, Mar 2026 | End-to-end agent workforce, including negotiation | Low-medium |
| 3 | Didero | Procurement / supply chain | didero.ai (assumed) | $30M Series A, Feb 2026 (M12) | Agents in email/ERP for supplier comms and exceptions | Low; useful for "supplier fails" scenario |
| 4 | Arkestro | Procurement | arkestro.com | $36M, May 2025 (Aramco Ventures) | Game theory and behavioral pricing; simulated negotiations | Medium: game theory |
| 5 | Keelvar | Sourcing | keelvar.com | $43M total (2022) | Sourcing optimization and autonomous sourcing bots | Low-medium |
| 6 | Levelpath | Procurement | levelpath.com | ~$100M total; $55M Series B, 2025 | Autonomous procurement agents | Low |
| 7 | Fairmarkit | Tail-spend sourcing | fairmarkit.com | $30M Series B, 2020; Series C reported | "AI agents managing demand to award" | Low |
| 8 | Zip | Intake-to-procure | ziphq.com | 50+ agents, Jun 2025; Superagents | Hierarchical orchestrator | Low (central decider) |
| 9 | nnamu (Beroe) | Negotiation strategy | beroeinc.com | Acquired Mar 2025 | Game-theory negotiation agent | Medium |
| 10 | Helios | Ag commodities (coffee-relevant) | (see AgFunder) | $4.7M seed | Multi-agent Q&A, price and climate risk | Low; data partner archetype |
| 11 | Sourcerer | Physical-goods sourcing | (see Runtime Wire) | Early stage | Agents source, negotiate, arrange freight | Medium |
| 12 | Luminance | Legal contracts | luminance.com | 1,000+ customers (vendor) | Claims 100% agent-to-agent NDA negotiation with "why" trail | High on agent-vs-agent and audit |
| 13 | Courtroom | Litigation | (see BusinessWire) | Pre-seed, Jun 2026 | Simulated jury and judge | Medium: deliberation |
| 14 | Viewpoints.ai | Litigation | viewpoints.ai (assumed) | n/a | Simulated jury group deliberations; verdict distributions | Medium-high: group deliberation |
| 15 | Tesla Autobidder | Energy trading | tesla.com | Hornsdale, utility scale | Optimizer with operator-set multi-objective priorities | Low-medium |
| 16 | Shatterdome Energy | Power trading | (see BusinessWire) | $3.5M pre-seed, May 2026 | Autonomous produce/store/sell trading | Low |
| 17 | Capalo AI | VPP | capalo.ai (assumed) | €3.8M seed, Mar 2025 | VPP aggregation and market trading | Low |
| 18 | Boosted.ai Alfa Prime | Investing | boosted.ai | Limited institutional rollout | Bull/bear/moderator multi-model debate; disagreement as signal | High (closest debate analog) |
| 19 | TradingAgents (Tauric Research) | Trading (open source) | github.com/TauricResearch | ICML 2025 paper | Bull/bear debate, risk team, fund manager | High; crowded |
| 20 | Debate-Verdict | Investing | Product Hunt | Small launch | Bull vs. Bear vs. Judge, verified against EDGAR | High; crowded |
| 21 | Hippocratic AI Polaris | Healthcare | hippocraticai.com | 22-model constellation | Primary agent plus specialist safety agents | Medium (cooperative) |
| 22 | Microsoft/Stanford tumor board | Healthcare | microsoft.com/research | Deployed summarization | Specialist agents | Medium (cooperative) |
| 23 | Cisco Outshift + Swisscom | Network change validation | outshift.cisco.com | Case study; Aether paper | Five cooperative NetOps agents plus digital twin | Medium; judge-aligned |
| 24 | Mate Security / 7AI / Prophet / Dropzone | SOC | (various) | Mate: $35M Series A, 2026 | Multi-agent triage orchestration; human sampling | Low (no consensus found) |
| 25 | Google AP2 (on A2A) | Agent commerce protocol | (see TechCrunch) | 60+ partners at launch | Mandates bound agent negotiation | Infrastructure / escalation formalism |
| 26 | Fetch.ai | Agent economy | fetch.ai | Academic supply-chain prototype | Peer-to-peer autonomous economic agents | Medium (decentralized) |
| 27 | Olas / Pearl | Agent economy | olas.network | $13.8M, Feb 2025 | Multi-operator consensus agents; Mech Marketplace | Medium (decentralized infrastructure) |
| 28 | Cisco CoffeeAGNTCY (Lungo) | Reference app, coffee supply chain | docs.agntcy.org | Open source | Supervisor/auction broadcast to farm agents | Very high: the pivot's substrate |

URLs marked "(assumed)" are guessed domains, not verified in this session. Use the cited source links above instead.

### Inferences: where a MAGI pivot is crowded vs. novel
- **Crowded (avoid as the headline):**
  - Buyer-agent-vs-supplier price negotiation (Pactum, Lio, Didero, Arkestro, Keelvar, Levelpath, Fairmarkit, Zip, nnamu).
  - Bull/bear/risk investment debate (Boosted.ai, TradingAgents, Debate-Verdict, Quorum, Senatus).
  - Specialist medical panels (Hippocratic, Microsoft/Stanford, many hackathon tumor boards).
  - Multi-agent disaster response (many hackathon projects).
- **Comparatively novel (based on what the searches found):**
  1. **Intra-buyer multi-objective negotiation.** A cost agent, a sustainability/risk agent and a delivery agent, each holding private data (price ladders; farm certifications and climate risk; lead times and inventory), negotiate the buyer's position before or while bidding. Commercial tools instead encode these trade-offs as static human-configured policy.
  2. **No central decider.** Most documented systems have an orchestrator, a fund manager, a primary agent or an auction supervisor. MAGI's vote and revise loop without a supervisor directly contrasts with CoffeeAGNTCY Lungo's auction supervisor.
  3. **Preserved disagreement as a product output.** Boosted.ai is the only commercial precedent found that treats disagreement as signal. MAGI can ship a dissent memo plus escalation to a human when objectives cannot be reconciled within mandate bounds, in the style of AP2's Intent Mandate.
  4. **New information mid-negotiation.** A farm agent fails or a frost shock hits Brazil (the shock type Nestlé cites). MAGI would show each agent's position and the vote shifting in response. Incumbents market exception handling (Didero) but don't show deliberative belief updates.
  5. **Measured baseline.** Run the same synthetic scenarios against a single-agent weighted-sum optimizer (the industry pattern) and against MAGI. Report cost, constraint violations, risk exposure, rounds to convergence and escalation rate. Incumbents report ROI but not head-to-head comparisons between architectures.
- **Strategic fit:**
  - Grounding MAGI in CoffeeAGNTCY's farm agents (reusing Lungo's A2A/SLIM transport and identity badges) aligns with Cisco Outshift judges and their reference architecture.
  - The differentiation must come from the decision layer (decentralized, competing objectives, dissent, baseline), because Lungo+ and similar community extensions already add bidding.
  - Network change approval (availability vs. security vs. velocity) is a strong second option because of Cisco's Swisscom investment, but it risks looking like a re-skin of Cisco's own Aether work.
- **What a hackathon MAGI could credibly demonstrate that incumbents don't publicize:**
  - Peer voting with no supervisor.
  - Per-agent private information.
  - A logged trace of position revisions after a mid-run shock.
  - Explicit stopping rules (convergence, max rounds, or impasse leading to human escalation).
  - Quantified comparison against a single-agent baseline.
  - Robustness to manipulation by a supplier agent. MIT's competition found prompt injection and strategic concealment matter in agent-vs-agent bargaining.

### Gaps
- Proving a negative is not possible: I found no commercial product doing intra-organization multi-objective agent negotiation with preserved dissent, but private or stealth products may exist.
- Combined funding totals are approximate, since several rounds come from secondary databases with inconsistent dates.
- Product URLs for several startups (Lio, Didero, Capalo, Viewpoints.ai, Helios) were not verified directly.
- I did not research credit-committee agents, logistics-dispatch negotiation vendors or Octopus Kraken in depth because of the tool-call budget.
