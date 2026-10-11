# Open-source multi-agent debate, council, voting and consensus projects compared with MAGI

Scope note: the star and fork counts, creation dates and last-push dates below come from the GitHub REST API (`gh api repos/<owner>/<repo>`), queried 2026-10-10. "Last push" is the repo's `pushed_at`. It shows recent activity but does not prove meaningful development. Each repo link below was checked through the API and exists. Projects that are not on GitHub (pMAGI, LapiSteLLa, NAGI) are flagged as such.

MAGI reference design, for comparison: three agents (MELCHIOR for science and evidence, BALTHASAR for ethics and safety, CASPER for creative and practical concerns) start as the same base model with different prompts. They analyze independently and in parallel, see each other's positions, debate and revise, then vote on concrete, immutable proposal versions. A decision requires unanimity, and after three failed rounds the question goes to a human. Planned features: mid-debate evidence injection, per-agent tools, a comparison against a single-LLM baseline, a React retro UI over WebSockets, a FastAPI backend, and optional Cisco AGNTCY integration.

---

## Key Question 1: Which MAGI/Evangelion clones exist, and what exactly does each one do (models, personas, rounds, decision rule, UI)?

### Takeaway
There are at least a dozen MAGI-themed clones, and almost all are small. Only TomaszRewak/MAGI (163 stars) and lordpba/AI_Magi (27 stars) have any traction. Most clones either just synthesize three persona answers or run a simple 2-of-3 majority vote. Several features are rare across the field:
- **Unanimity.** TomaszRewak's "any NO blocks" rule is effectively unanimity. float1122 uses 3/3 unanimity only for "grave" operations.
- **Human arbitration.** Adrian-Sandwich/magi-council has it.
- **Multi-round revision.** atrix228, Git-Hacking, nlink-jp and Adrian-Sandwich have it.

No clone combines all three of these with immutable proposal versions, evidence injection and a single-LLM baseline harness.

### Cited Findings

**1. jason-chao/MAGI ("Multi-Agent Group Intelligence"; PyPI `magi-core`)**
- Repo stats: 2 stars, 0 forks, created 2026-02-10, last push 2026-04-15, Python, MIT. The description reads "A council of LLMs for hard decisions… blind peer review." — [GitHub](https://github.com/jason-chao/MAGI)
- **Mechanism.** The question goes to all configured models in parallel. Each returns structured JSON (answer, reasoning, confidence). A "Rapporteur", the most confident model, synthesizes the final report. An optional "Deliberative Round" lets agents read each other's Round 1 answers before finalizing. — [README](https://github.com/jason-chao/MAGI)
- **Eight decision modes:** Synthesis, Probability, VoteYesNo, VoteOptions, Majority, Consensus, Minority, and Compose (which generates content and ranks it through blind peer review). Vote modes tally the votes and declare a winner if the count passes a threshold. — [README](https://github.com/jason-chao/MAGI)
- **Anonymization.** During deliberation, peers appear under random pseudonyms (e.g., "Participant X7K2") to reduce brand bias. The final report is de-anonymized by default, and `--anonymous-report` keeps the pseudonyms. — [README](https://github.com/jason-chao/MAGI)
- **Models.** The default config lists `openai/gpt-5.4-nano`, `anthropic/claude-haiku-4-5`, and `gemini/gemini-2.5-flash-lite`. It supports fallback chains, a `min_models` quorum (abort if too few respond), and a language option. — [README](https://github.com/jason-chao/MAGI)
- **Author write-up.** Per Jason Chao, the highest-confidence model writes the synthesis and the lowest-confidence model writes the minority report. The write-up reports no benchmark. The procedures borrow from parliamentary committees, the European Court of Human Rights rapporteur model, Quaker consensus and Fishkin's deliberative polling. The Evangelion styling is described as cosmetic. The thesis: "The value is not the verdict. It is the record of the disagreement." There is a live demo at magi-council.org. — [jasontc.net write-up](https://jasontc.net/work/magi.html)
- **Differences from MAGI.** It gets diversity from different vendors rather than personas. It has at most two rounds and no unanimity-or-escalate loop. It has no human escalation, no proposal versioning and no tools. It is listed in the Karpathy-council ecosystem index. — [Awesome-LLM-Council-Projects](https://github.com/danielrosehill/Awesome-LLM-Council-Projects)

**2. lordpba/AI_Magi ("MAGI System v2.0")**
- Repo stats: 27 stars, 3 forks, created 2024-04-23, last push 2025-11-07, Python. GitHub detects no license, though the README says "Code: MIT License". — [GitHub](https://github.com/lordpba/AI_Magi)
- **Mechanism.** CrewAI agents represent Melchior (scientific/logical), Balthasar (ethical/emotional) and Casper (practical/social). "MAGI splits your question into three perspectives" and then a synthesis "merges all three analyses." There is no voting or debate. — [README](https://github.com/lordpba/AI_Magi)
- **Stack.** CrewAI, Gradio web UI (localhost:7862, deployable to Hugging Face Spaces) and LiteLLM. Providers are Groq (recommended), OpenAI or local Ollama, chosen as one provider and model for all three personas. Serper web search is optional. — [README](https://github.com/lordpba/AI_Magi)
- **Similarity to MAGI.** This is the closest to MAGI's "same model, different persona" starting point, and its persona split is nearly identical. It lacks MAGI's debate, voting, unanimity and escalation.

**3. TomaszRewak/MAGI**
- Repo stats: 163 stars, 24 forks, created 2023-05-11, last push 2024-04-01, Python. This is the most-starred MAGI clone found. — [GitHub](https://github.com/TomaszRewak/MAGI)
- **Model.** It runs on GPT-3.5, all three agents on the same model. The persona prompts are "You are a scientist… advance our technological progress" (MELCHIOR), "You are a mother… protect your children" (BALTHASAR) and "You are a woman… pursue love, dreams and desires" (CASPER). — [README](https://github.com/TomaszRewak/MAGI)
- **Flow.** It first classifies whether the question is yes/no. Each agent answers. Outputs are evaluated in this order:
  - error
  - info (not a yes/no question)
  - **no if at least one agent says no**
  - conditional if any agent gives a conditional yes
  - **yes only if all agents give an unconditional yes**

  This is effectively a unanimity/veto rule. There is a single round with no debate. — [README](https://github.com/TomaszRewak/MAGI)
- **UI.** A local web app (127.0.0.1:8050) with an Evangelion-style animated display (GIFs in the README). Users can click each subsystem to inspect its full reply and conditions. Its design was reused by Adrian-Sandwich/magi-council (below). — [README](https://github.com/TomaszRewak/MAGI); [magi-council README](https://github.com/Adrian-Sandwich/magi-council)

**4. atrix228/magi-system ("M.A.G.I. System — AI Tribunal for Android")**
- Repo stats: 0 stars, created and last pushed 2026-06-26. GitHub reports no language, which suggests the repo distributes an APK and the source may not be published. — [GitHub](https://github.com/atrix228/magi-system)
- **Three phases.** (1) Independent analysis, with reasoning streamed live in "thought boxes". (2) "Cross-Examination", where the brains review each other's arguments, "challenge inconsistencies, debate assumptions, and refine their positions." (3) "Voting & Verdict", with majority opinion plus dissent in an executive summary. — [README](https://github.com/atrix228/magi-system)
- **Features.** The user can assign a different model to each brain (GPT-4o, Claude, DeepSeek and others) through the "Evia API Router", which gives access to 100+ models. It also has a NERV terminal aesthetic, sci-fi sound effects and a synthesized voice verdict. It runs on Android 8.0+. — [README](https://github.com/atrix228/magi-system)

**5. float1122/magi-system (Claude Code skill; install instructions point to jangfolk/magi-system)**
- Repo stats: 9 stars, 4 forks, created 2026-07-01, last push 2026-07-01. — [GitHub](https://github.com/float1122/magi-system)
- **Structure.** Three persona cores run as parallel Claude Code subagents on the same base model:
  - MELCHIOR covers logic and performance.
  - BALTHASAR, the "Mother / Safety Core", covers user impact and rollback safety.
  - CASPER covers pragmatism and intuition.

  Each core fans out into 3–5 "judgment nodes" (10–20 in total) that self-verify. — [README](https://github.com/float1122/magi-system)
- **Tiered decision rule.** Regular decisions pass with a 2/3 majority. "Grave/irreversible ops" (file deletion, prod deploy, DB drop, force-push, auth/payment bypass, security disable) need 3/3 unanimity, and any core can VETO. Node states are OK, DELIBERATING and COMPROMISED, and only OK nodes vote. — [README](https://github.com/float1122/magi-system)
- **Orchestrator.** It "never judges". It decomposes the request, dispatches the cores, verifies one fact by hand and reports. Output is an ASCII-art status banner. — [README](https://github.com/float1122/magi-system)

**6. Git-Hacking/MAGI**
- Repo stats: 0 stars, created and last pushed 2026-08-24, JavaScript (Node). — [GitHub](https://github.com/Git-Hacking/MAGI)
- **Models.** Three different models via OpenRouter, one per unit, each with its own system prompt. — [README](https://github.com/Git-Hacking/MAGI)
- **Flow.** Round 1 is independent. In Round 2 each unit sees the other two. In the final round each unit gives a closing position and votes APPROVE or REJECT. Strict majority decides ("never a tie… no overrides"), and `ROUNDS = 2` is configurable. — [README](https://github.com/Git-Hacking/MAGI)
- **UI and experiments.** The browser UI is a "terminal / war-room" look with live streaming and a vote tally. The README suggests trying all three units on the *same* model to see "how much less interesting the disagreement gets". — [README](https://github.com/Git-Hacking/MAGI)

**7. Adrian-Sandwich/magi-council ("three AI heads that deliberate, vote and execute")**
- Repo stats: 0 stars, created 2026-08-07, last push 2026-09-25, Python. It has CI. — [GitHub](https://github.com/Adrian-Sandwich/magi-council)
- **Seats and output.** "The persona lives in the seat, the provider is swappable" (kimi, codex, claude, Ollama, any OpenAI-compatible API). Output includes a ruling, a minority report, "mind changes between rounds and human arbitration." — [README](https://github.com/Adrian-Sandwich/magi-council)
- **Memory and production mode.** A local Postgres knowledge graph ingests past sessions and decisions and injects them into each deliberation. In "production mode" the council approves a plan, an executor implements it on a branch, and the council reviews the diff. "On unanimous approval" it merges itself. — [README](https://github.com/Adrian-Sandwich/magi-council)
- **Heads and tools.** CLI/MCP heads can investigate the repo with tools and vote through MCP. API heads vote over an inlined journal but cannot run tools. With zero heads the system runs "degraded" and only the human can close decisions. — [README](https://github.com/Adrian-Sandwich/magi-council)
- **Operations.** Seats that fail three times are quarantined. The system tracks token and cost usage per seat. The UI is a MAGI-style web app "based on TomaszRewak/MAGI". Docs are partly in Spanish. — [README](https://github.com/Adrian-Sandwich/magi-council)

**8. nlink-jp/magi-system (Japanese; archived 2026-07-31)**
- Repo stats: 0 stars, created 2026-03-16, archived. It is a terminal tool running local LLMs through LM Studio (default `qwen/qwen3-30b-a3b-2507`). — [GitHub](https://github.com/nlink-jp/magi-system)
- **Personas.** Each has a priority order: MELCHIOR (scientific evidence, then logic, then reproducibility), BALTHASAR (ethics, then human emotion, then social impact), CASPER (feasibility, then cost, then risk). Each persona also tracks an emotional state toward the others (favorable, neutral or negative), which changes its speaking style. — [README](https://github.com/nlink-jp/magi-system)
- **Mechanics designed against convergence-by-default:**
  - Random stance assignment (promoter, skeptic, alternative-proposer).
  - A facilitator.
  - The next speaker is chosen by a "Maximum Disagreement" score.
  - A novelty check: if bigram similarity is above 0.7, the speaker is told to bring a new perspective.
  - Discussion phases: problem definition, issue exploration, solution design, consensus.
  - An issue-coverage check at turn 8.
  - Facilitator warnings at the midpoint and at 75% of turns.

  Convergence requires coverage passed, MIN_TURNS elapsed, threshold votes and recent agreement. A final LLM report is saved to Markdown. — [README](https://github.com/nlink-jp/magi-system)

**9. pMAGI (NISHIO Hirokazu), not a GitHub repo found**
- The tool asks "several virtual personas with different ideologies" to answer the same question, for example "Synthetic Technocracy", "Digital Democracy" and an Altman-ideology supporter. It is hosted at magi-nishio.vercel.app (Next.js). — [Scrapbox pMAGI 2024-02-04](https://scrapbox.io/nishio-en/pMAGI-2024-02-04)
- Decision rule: "This system does not use majority voting by ballot." Consensus is when "all three respondents are in the same direction", and "weak consensus" is when some are neutral. Each answer starts with STRONG YES, Yes, Neutral, No or STRONG NO. — [Scrapbox](https://scrapbox.io/nishio-en/pMAGI-2024-02-04)
- Outputs were precomputed by the author because of AI cost. No multi-round deliberation is described, and the source code's availability is not stated. — [Scrapbox](https://scrapbox.io/nishio-en/pMAGI-2024-02-04)

**10. LapiSteLLa ("an AI assistant guided by the three wise men"), an AWS PartyRock app rather than a repo**
- It is a PartyRock brainstorming app modeled on MAGI (AWS community post, March 2024 per the search snippet). Melchior and Balthasar run at high temperature with abstract, unrestricted prompts "to shake up ideas". Casper runs at low temperature with a restricted prompt and refers to the other two to produce realistic improvements. It is ideation, not voting. — [AWS Builder post](https://community.aws/content/2dM7DAtTPhnzUxrgaCu6Xd1RWA4/lapistella-an-ai-assistant-guided-by-the-three-wise-men?lang=en) (now redirects to builder.aws.com; the full page was not fetched)

**11. NAGI system (Koki Tanaka, NAIST, Dec 2022), a Hugging Face demo rather than a repo**
- It uses three different *non-chat* models: BERT as Melchior, GPT-2 as Casper and mT5 as Balthasar. Each says approve or deny, and the majority decides. The models were not trained for approve/deny, so "denial" was frequently returned (a bias). — [GIGAZINE (EN)](https://gigazine.net/gsc_news/en/20221221-nagi-system)

**12. Long tail (0-star, description-only; verified to exist, READMEs not reviewed in depth)**
- UrabeMikotoX1145/magi-vote: "DeepSeek API, Melchior/Balthasar/Casper majority" (Chinese), created 2026-09-18. — [GitHub](https://github.com/UrabeMikotoX1145/magi-vote)
- revkahoptimum106/MAGI-System: "Simulate three AI units debating yes/no questions and deliver a majority vote verdict", last push 2026-10-10. — [GitHub](https://github.com/revkahoptimum106/MAGI-System)
- Ssysshy/MAGI (TypeScript, "charge your question"). — [GitHub](https://github.com/Ssysshy/MAGI)

**13. UI asset: mdrbx/nerv-ui (not a council, but relevant to the retro UI)**
- Repo stats: 92 stars, MIT, created 2026-03-08, last push 2026-10-04. It is a typed React/TypeScript "command-center" component library: an npm package `@mdrbx/nerv-ui` with 48 components, 18 live examples and a coding-agent skill. Its sample prompt advises using "original labels". — [GitHub](https://github.com/mdrbx/nerv-ui)

### Inferences
- **Decision rules.** The MAGI clones split into three camps:
  - (a) Synthesis only: lordpba, LapiSteLLa, jason-chao's Synthesis mode.
  - (b) Majority vote: atrix228, Git-Hacking, NAGI, magi-vote, float1122 for regular decisions.
  - (c) Unanimity or veto: TomaszRewak's "any NO" rule, float1122 for grave operations, Adrian-Sandwich's merge gate, pMAGI's "same direction" consensus.

  MAGI belongs in camp (c), but differs because it *iterates* toward unanimity over revisable proposals rather than taking a single snapshot.
- Adrian-Sandwich/magi-council is the closest functional match: per-seat personas, swappable providers, tools on some heads, mind changes across rounds, unanimity for merges and human arbitration. It is a local developer tool tied to code execution and has no traction (0 stars). MAGI can present itself as a general-purpose, demo-quality version of these ideas.
- nlink-jp's anti-convergence mechanics (Maximum-Disagreement speaker selection, novelty check, coverage gate) are directly reusable ideas against premature unanimity in MAGI.
- **Same model vs. different models.** TomaszRewak, lordpba, float1122 and pMAGI use one model with personas. jason-chao, atrix228, Git-Hacking and NAGI use different models. Git-Hacking claims, without data, that same-model councils disagree less. No clone measures this, so MAGI could fill that gap.

### Gaps
- No public source code for pMAGI was found. Whether it is open-source is unknown.
- The atrix228/magi-system repo appears to ship only an APK, so whether source is available is unverified.
- The full LapiSteLLa page (builder.aws.com) was not fetched. The details come from a search snippet. Exact models and date are unconfirmed.
- I found no AWS "Lapistella" GitHub repo. PartyRock apps are shareable or remixable but are not standard open-source repos.
- I did not exhaustively crawl GitHub. More 0–5-star MAGI clones likely exist. Searches for "magi evangelion llm" and "magi system llm" returned nothing, while "melchior balthasar casper" surfaced most of the ones listed.

---

## Key Question 2: What AI council, multi-model council and LLM-as-a-jury tools exist (Karpathy's llm-council and its notable forks)?

### Takeaway
Karpathy's llm-council (25.3k stars, Nov 2025) set the de facto "council" pattern:
1. Independent answers.
2. Anonymized peer ranking.
3. Chairman synthesis.

It also uses the same FastAPI + React stack MAGI plans to use. Hundreds of forks and Claude Code "skills" followed. The only fork found with a rigorous evaluation (andybhall/llm-council-governance) found that **Deliberate→Vote beat chairman synthesis and beat the best single model by 9.2 points**. An independent June 2026 analysis found that councils exhibit **groupthink**, dropping about 75% of good single-model ideas.

### Cited Findings

**karpathy/llm-council**
- Repo stats: 25,338 stars, 4,409 forks, created and last pushed 2025-11-22. It is unmaintained by design: "I'm not going to support it in any way… Code is ephemeral now." — [GitHub](https://github.com/karpathy/llm-council)
- **Mechanism.**
  - Stage 1: first opinions from all LLMs, shown in tabs.
  - Stage 2: each LLM sees the others' responses, "anonymized so that the LLM can't play favorites", and ranks them for accuracy and insight.
  - Stage 3: a Chairman LLM compiles the final answer.

  The default council is GPT-5.1, Gemini 3 Pro, Claude Sonnet 4.5 and Grok 4 via OpenRouter, with Gemini 3 Pro as chairman. — [README](https://github.com/karpathy/llm-council)
- **Tech stack.** FastAPI backend (async httpx), React + Vite frontend, conversations stored as JSON files. — [README](https://github.com/karpathy/llm-council)
- **Reception.** Commentators described it as trending within an hour and called it "99% vibe coded". Some argued the idea itself was not new. — [Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/12/llm-council-by-andrej-karpathy/)
- The HN submission of the repo got 4 points and 0 comments (2025-11-23). Most discussion apparently happened elsewhere. — [HN Algolia API result, item 46021989](https://news.ycombinator.com/item?id=46021989)

**andybhall/llm-council-governance (evaluation fork)**
- Repo stats: 21 stars, created 2025-12-22, last push 2026-01-04. It compares seven governance structures on MMLU-Pro Math with four 7–9B models (Llama 3.1 8B, Mistral 7B, Gemma 2 9B, Qwen 2.5 7B). — [GitHub](https://github.com/andybhall/llm-council-governance)
- **Results (1,004 valid trials).** The baseline is the best individual model, Qwen 2.5 7B, at 71.7%.

  | Structure | Accuracy | vs. baseline |
  |---|---|---|
  | Deliberate→Vote | 80.9% | +9.2pp |
  | Majority Vote | 76.8% | +5.1pp |
  | Deliberate→Synthesize | 75.4% | +3.7pp |
  | Agenda Setter + Veto | 74.1% | +2.4pp |
  | Rank→Synthesize (Karpathy-style) | 70.7% | −1.0pp |
  | Weighted Majority | 69.0% | −2.7pp |
  | Self-Consistency (one model sampled 9×) | 68.9% | −2.8pp |

  — [README](https://github.com/andybhall/llm-council-governance)
- **Authors' interpretation.** "Sampling the same model multiple times doesn't add the diversity that different models provide", and "having a chairman synthesize answers works better after deliberation than after ranking." — [README](https://github.com/andybhall/llm-council-governance)

**Groupthink critique**
- Rohit Krishnan ("LLM councils show groupthink", Strange Loop Canon, 2026-06-15) evaluated 16 open-ended tasks (8 strategy, 8 writing):
  - A blended council kept only about a quarter of the good single-model ideas.
  - A peer-review council kept rare ideas at about the same rate (24% vs. 22%).
  - Peer review acted as a "consensus detector", favoring shared ideas.
  - A best-answer picker kept about 37%.

  The author recommends model diversity and an explicit protocol that extracts and ranks each model's best ideas before synthesis. — [Strange Loop Canon](https://www.strangeloopcanon.com/p/llm-councils-show-groupthink)

**Notable forks and derivatives**
- **DmitryBMsk/llm-council-plus.** 131 stars, last push 2026-09-08. A React/FastAPI app with OpenRouter or Ollama. Modes are `chat_only`, `chat_ranking` (anonymized peer rankings) and `full` (with chairman synthesis). It adds streaming with cancellation and partial-result recovery, persistent conversations, attachments, admin settings and provider-reported usage tracking. — [GitHub](https://github.com/DmitryBMsk/llm-council-plus)
- **aiwithremy/claude-skills-llm-council.** 2,445 stars, created 2026-04-25, by Ole Lehmann. A Claude skill where *one model* spins up "5 different advisors who each think about it from a fundamentally different angle", peer-review each other, and a chairman synthesizes "where the advisors agree, where they clash". It is positioned for decisions, not factual questions. — [GitHub](https://github.com/aiwithremy/claude-skills-llm-council)
- **a1exsun/dsh-council.** 159 stars, created 2026-08-30. A DeepSeek Harness plugin: 2–8 independent answerers, 1–8 reviewers comparing anonymous answers, and one arbiter. Output includes confidence notes, consensus, disagreements, blind spots, model identities and average rankings. — [GitHub](https://github.com/a1exsun/dsh-council)
- **Other council-style tools** (descriptions only; READMEs not reviewed):
  - TorpedoD/claude-council (21 stars): "peer review, forced debate, dual-chairman synthesis with dissent preservation". — [GitHub](https://github.com/TorpedoD/claude-council)
  - amgadelgamal/claude-council (22 stars): parallel Claude subagents "debate, anonymously peer-review, and synthesize". — [GitHub](https://github.com/amgadelgamal/claude-council)
  - kvsdileep/model-council (33 stars): "Four frontier models. A structured debate. One synthesized verdict." — [GitHub](https://github.com/kvsdileep/model-council)
  - sanky369/open-model-council (13 stars): open-source version of Perplexity's model council. — [GitHub](https://github.com/sanky369/open-model-council)
  - amiable-dev/llm-council (44 stars, active 2026-10-09). — [GitHub](https://github.com/amiable-dev/llm-council)
- **Ecosystem index.** danielrosehill/Awesome-LLM-Council-Projects lists 20+ council derivatives, including jason-chao/MAGI, llm-council-plus, OpenCouncil and council-of-high-intelligence. — [GitHub](https://github.com/danielrosehill/Awesome-LLM-Council-Projects)

**LLM-as-a-jury and judge protocols**
- **haizelabs/verdict.** 348 stars, last push 2025-11-05. "Inference-time scaling for LLMs-as-a-judge". It composes judge protocols, for example 3 hierarchically verified judges plus a max vote, or three pairs of LLMs debating with the outcomes aggregated into a verdict. — [GitHub](https://github.com/haizelabs/verdict)
- **yusufipk/opencode-safeguard.** 5 stars, 2026-09-19. An "LLM jury for OpenCode V2 permission asks: allow, deny or escalate, with a visible verdict under every tool call". This is a rare example of a jury that escalates to a human. — [GitHub](https://github.com/yusufipk/opencode-safeguard)
- **Two more small jury repos:**
  - NasLabBgu/jury-deliberation (4 stars): multi-LLM jury deliberation simulation. — [GitHub](https://github.com/NasLabBgu/jury-deliberation)
  - ajsai47/llm-jury: "don't vote, verify", a small-model council plus a verifier. — [GitHub](https://github.com/ajsai47/llm-jury)

### Inferences
- Karpathy's repo is MAGI's most direct competitor in judges' minds. It shares MAGI's stack (FastAPI + React), uses anonymized peer review and has huge mindshare. Differences:
  - Karpathy uses a chairman (a single point of authority), single-shot ranking, no persona objectives, no voting on a concrete proposal, no iteration toward agreement and no human escalation.
  - MAGI's "no chairman: unanimity or escalate" design is a clear philosophical contrast.
- The andybhall results support MAGI's "deliberate, then vote" structure over chairman synthesis. They also warn that self-consistency (the same model sampled repeatedly) underperforms. That bears on MAGI's same-base-model plan: persona prompts may not supply enough diversity unless MAGI measures it.
- The groupthink finding is a direct risk for a unanimity-seeking system. MAGI should show that unanimity does not just mean "everyone converged on the bland shared idea". That could mean tracking dropped minority ideas, or rewarding a dissenter who flips others with evidence.

### Gaps
- No substantive Hacker News or Reddit threads on llm-council were found. The repo's HN post had 0 comments.
- Several other HN posts exist but were not read: "I run a 9-model LLM council to write a financial newsletter. What breaks" (Aug 2026), and a Show HN for abhishekgandhi-neo/llm_council (Feb 2026).
- The PoLL / "Replacing Judges with Juries" paper's official code was not checked.
- The andybhall results use small 7–9B models on math only. Whether they transfer to frontier models or to open-ended ethical questions is untested.

---

## Key Question 3: How do multi-agent frameworks and research codebases implement debate and consensus (AutoGen, CAMEL, ChatEval, MetaGPT, CrewAI, LangGraph, OpenAI Agents SDK/Swarm, DSPy, AgentVerse, TradingAgents, Agent Laboratory, co-scientist reimplementations, AGNTCY coffeeAgntcy, MAD, Du et al., ReConcile, MALLM)?

### Takeaway
General frameworks (AutoGen/MAF, CrewAI, LangGraph, OpenAI Agents SDK, CAMEL, DSPy) give you primitives for building a debate, such as group chat, handoffs, graphs and parallelization. None ships a first-class unanimity/escalation protocol, and CrewAI's `consensual` process is still a `# TODO`. The richest debate mechanics are in research code:
- MALLM: seven decision protocols plus a harness.
- ReConcile: confidence-weighted voting across different models.
- MAD: devil, angel and judge.
- Du et al.: rounds of mutual critique.

The richest *applied* debate is TradingAgents: bull/bear researchers and a risk team, with a manager approving or rejecting. AGNTCY's coffeeAgntcy documents a "Decentralized Consensus Agents" pattern but has not implemented it.

### Cited Findings

**Microsoft AutoGen → Microsoft Agent Framework**
- AutoGen has 61,345 stars, last push 2026-04-15. It is in **maintenance mode**: "will not receive new features". New users are pointed to Microsoft Agent Framework (MAF) 1.0, with "cross-runtime interoperability via A2A and MCP". — [GitHub](https://github.com/microsoft/autogen)
- **AutoGen's "Multi-Agent Debate" design pattern doc:**
  - Solver agents are connected in a sparse topology (per arXiv 2406.11776) and exchange and refine responses for a fixed number of rounds.
  - An aggregator agent "uses majority voting to aggregate the final responses".
  - The demo is on GSM8K and uses the publish/subscribe topic API.

  — [AutoGen docs notebook](https://github.com/microsoft/autogen/blob/main/python/docs/src/user-guide/core-user-guide/design-patterns/multi-agent-debate.ipynb)

**CrewAI**
- 59,546 stars, last push 2026-10-10. Processes are `sequential` and `hierarchical`, where a manager is automatically assigned to coordinate, delegate and validate. The source enum contains `# TODO: consensual = 'consensual'`, so there is no built-in consensus or vote process. — [README](https://github.com/crewAIInc/crewAI); [process.py](https://github.com/crewAIInc/crewAI/blob/main/lib/crewai/src/crewai/process.py)
- lordpba/AI_Magi (KQ1) is built on CrewAI and only synthesizes. — [GitHub](https://github.com/lordpba/AI_Magi)

**LangGraph**
- 43,029 stars, last push 2026-10-11. It is a general graph and state framework, "Build resilient agents." — [GitHub](https://github.com/langchain-ai/langgraph)
- TradingAgents (with LangGraph checkpoint resume) and conradry's co-scientist reimplementation are built on it. — [TradingAgents README](https://github.com/TauricResearch/TradingAgents); [open-coscientist-agents](https://github.com/conradry/open-coscientist-agents)
- Community debate templates exist. For example, NishantkSingh0/Multi-Agent-Debates-LangGraph (11 stars) has an LLM-Scientist debate an LLM-Philosopher, with the winner decided by an LLM-Judge. — [GitHub](https://github.com/NishantkSingh0/Multi-Agent-Debates-LangGraph)

**OpenAI Swarm → OpenAI Agents SDK**
- Swarm has 22,049 stars. It is "experimental, educational" and "now replaced by the OpenAI Agents SDK". Its primitives are Agents and **handoffs**. — [GitHub](https://github.com/openai/swarm)
- The Agents SDK has 29,954 stars, last push 2026-10-08. Its `examples/agent_patterns` include `parallelization.py`, `llm_as_a_judge.py`, `agents_as_tools*.py`, several `human_in_the_loop*.py` files, `routing.py` and guardrails. There is no debate or vote example. — [GitHub examples](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns)

**CAMEL**
- 17,853 stars, last push 2026-10-05. It provides role-playing "Agent Societies" and a "Workforce" module. It is a framework, not a debate protocol. — [GitHub](https://github.com/camel-ai/camel)

**MetaGPT**
- 70,796 stars, last push 2026-01-21. It is an SOP-based "AI software company". It ships `examples/debate.py` and `debate_simple.py` (a two-role "SpeakAloud" quarrel, 2023), but debate is a toy example rather than a core primitive. — [GitHub](https://github.com/FoundationAgents/MetaGPT); [debate.py](https://github.com/FoundationAgents/MetaGPT/blob/main/examples/debate.py)

**DSPy**
- 38,584 stars. It has a `MultiChainComparison` module (compares multiple reasoning attempts) and is used to optimize prompts and programs, not to orchestrate agents. — [GitHub](https://github.com/stanfordnlp/dspy); [MultiChainComparison docs](https://github.com/stanfordnlp/dspy/blob/main/docs/docs/api/modules/MultiChainComparison.md)

**AgentVerse and ChatEval**
- AgentVerse has 5,156 stars, last push 2024-09-09. It offers "task-solving" (agents assembled as an automatic multi-agent system) and "simulation" frameworks, and the code was being refactored. — [GitHub](https://github.com/OpenBMB/AgentVerse)
- ChatEval (thunlp, 343 stars, last push 2024-10-19) is a "multi-agent referee team" whose persona-assigned LLMs "autonomously debate" to judge text quality. It is built on AgentVerse and has a FastChat arena demo. — [GitHub](https://github.com/thunlp/ChatEval); [arXiv 2308.07201](https://arxiv.org/abs/2308.07201)

**TradingAgents (TauricResearch)**
- 110,520 stars, 21,282 forks, last push 2026-10-03, v0.6.0 in Oct 2026. It is by far the most-starred debate-centric open-source project in this survey. — [GitHub](https://github.com/TauricResearch/TradingAgents)
- **Pipeline:**
  1. Analysts (fundamental, sentiment, technical and others) work in parallel with their own tools.
  2. Bull and bear researchers hold "structured debates".
  3. A Trader agent proposes.
  4. The risk management team evaluates.
  5. The Portfolio Manager "approves/rejects the transaction proposal".

  Config includes `max_debate_rounds` and `max_risk_rounds`. A "quick" model serves analysts and debaters, while a "deep" model serves the managers, and each can use a different provider. — [README](https://github.com/TauricResearch/TradingAgents)
- **Memory and reflection.** A persistent decision log settles past decisions against realized returns and generates reflections that later runs read. — [README](https://github.com/TauricResearch/TradingAgents)

**Agent Laboratory**
- 5,897 stars, last push 2025-08-20. It runs research in three phases (literature review, experimentation, report writing) with specialized agents and tools (arXiv, Hugging Face, Python, LaTeX). A "Co-Pilot mode" adds human involvement. It is not a debate or vote system. — [GitHub](https://github.com/SamuelSchmidgall/AgentLaboratory)

**Google AI co-scientist reimplementations** (the original is not open-source)
- **conradry/open-coscientist-agents** (69 stars, last push 2025-07-22). Built on LangGraph and GPT Researcher, with Reflection, Evolution, Meta-Review and Supervisor agents. It runs an Elo-rated "Tournament-Style Hypothesis Competition" with debate transcripts, a Streamlit dashboard and a tournament viewer. — [GitHub](https://github.com/conradry/open-coscientist-agents)
- **Kaimen-Inc/Co-Scientist** (270 stars, last push 2026-08-03):
  - Supervisor, Generation ("simulated scientific debate"), Reflection, Ranking ("Elo tournament with simulated debates between hypotheses"), Evolution, Proximity (clustering for dedup and pairings) and Meta-review agents.
  - Ships cross-model bench results.
  - Cites Gottweis et al., *Nature*, 2026.

  — [GitHub](https://github.com/Kaimen-Inc/Co-Scientist)
- **The-Swarm-Corporation/AI-CoScientist** (131 stars): a minimal implementation on the Swarms framework. — [GitHub](https://github.com/The-Swarm-Corporation/AI-CoScientist)

**AGNTCY coffeeAgntcy (the Cisco hackathon track's reference app)**
- 111 stars, 52 forks, last push 2026-10-09. It demonstrates SLIM (request-reply, unicast and group communication), NATS pub/sub, A2A, MCP, the Observe SDK and the Directory. Its "Lungo" demo shows group communication among farms, a shipper and an accountant. — [GitHub](https://github.com/agntcy/coffeeAgntcy)
- **"Decentralized Consensus Agents" pattern doc:**
  - North America, Europe and APAC demand agents exchange "Belief Update"s.
  - A "Consensus Merge Agent" produces a converged number.
  - It must handle "oscillation and gaming… through caps, dampening, voting rules, or human tie-breaks" with "explicit stopping rules".
  - The Workflow section says it "will describe how this pattern is realized once a concrete layout exists".

  — [pattern doc](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/api/agentic_workflows/docs/workflows/decentralized_consensus_agents.md)
- In `starting_workflows.json`, the "Decentralized Consensus Agents" entry has `"use_case": "---"` and an empty `starting_topology` (`nodes: [], edges: []`), so it is **not implemented**. The same file lists other unimplemented patterns such as "Approval Gate Agent" (Governance, Policy & Human Oversight). — [starting_workflows.json](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/api/agentic_workflows/starting_workflows.json)
- **Related AGNTCY repos:** agntcy/slim (Rust, 228 stars, active 2026-10-10) and agntcy/app-sdk (21 stars, "used by coffeeAGNTCY to demonstrate AGNTCY interoperability patterns"). — [slim](https://github.com/agntcy/slim); [app-sdk](https://github.com/agntcy/app-sdk)

**Research debate codebases**
- **Du et al., "Improving Factuality and Reasoning… through Multiagent Debate"** (ICML 2024). composable-models/llm_multiagent_debate has 552 stars, last push 2025-04-24. It covers arithmetic, GSM, biographies and MMLU tasks. — [GitHub](https://github.com/composable-models/llm_multiagent_debate)
- **MAD (Liang et al.).** Skytliang/Multi-Agents-Debate has 615 stars, GPL-3.0, last push 2025-12-16. Agents argue "tit for tat" (an affirmative "devil" and a negative "angel"). A judge manages the debate and picks the final solution, to counter "Degeneration-of-Thought" in self-reflection. — [GitHub](https://github.com/Skytliang/Multi-Agents-Debate); [arXiv 2305.19118](https://arxiv.org/abs/2305.19118)
- **ReConcile (Chen, Saha, Bansal).** dinobby/ReConcile has 207 stars, last push 2023-10-03. A "round table conference among diverse LLM agents" (ChatGPT, PaLM/Bard, Claude):
  - Multi-round discussion.
  - "Learning to convince" through human-explanation demonstrations.
  - A **confidence-weighted voting** mechanism.

  It reports gains of up to 11.4% over prior baselines and beats GPT-4 on three datasets. — [GitHub](https://github.com/dinobby/ReConcile); [arXiv 2309.13007](https://arxiv.org/abs/2309.13007)
- **MALLM (Göttingen).** 67 stars, active 2026-10-10, EMNLP 2025 demo.
  - It is built from agents, discussion paradigms (`collective_refinement`, `debate`, `memory`, `relay`, `report`) and decision protocols (`approval_voting`, `consensus`, `consensus_voting`, `cumulative_voting`, `judge`, `ranked_voting`, `simple_voting`).
  - The default config uses `decision_protocol: hybrid_consensus`, `max_turns: 10` and `debate_rounds: 2`.
  - It has a built-in loader for 20+ datasets (MMLU-Pro, GPQA, StrategyQA, ETHICS, MoCaMoral, SimpleEthicalQuestions and others) and a `mallm-evaluate` script.

  — [GitHub](https://github.com/Multi-Agent-LLMs/mallm); [repo tree](https://github.com/Multi-Agent-LLMs/mallm/tree/main/mallm/decision_protocols)
- **"Voting or Consensus? Decision-Making in Multi-Agent Debate"** (Kaesberg et al., ACL Findings 2025, built on MALLM):
  - Voting protocols improve reasoning tasks by 13.2%, and consensus protocols improve knowledge tasks by 2.8%.
  - More agents helps, while **more discussion rounds before voting reduce performance**.
  - The proposed All-Agents Drafting and Collective Improvement methods add up to 3.3% and 7.4%.

  — [arXiv 2502.19130](https://arxiv.org/html/2502.19130v4)
- **instadeepai/DebateLLM.** 62 stars. A library of debate protocols (Society of Minds, Medprompt, ChatEval, SPP and others) for Q&A truthfulness. Its finding: "no single debate or prompting strategy consistently outperforms others across all scenarios." — [GitHub](https://github.com/instadeepai/DebateLLM)
- **togethercomputer/MoA (Mixture-of-Agents).** 2,982 stars. Layers of proposer LLMs feed an aggregator, scoring 65.1% on AlpacaEval 2.0 with open-source models versus GPT-4o's 57.5%. It is aggregation, not debate or voting. — [GitHub](https://github.com/togethercomputer/MoA)
- **zjunlp/MachineSoM.** 121 stars, ACL 2024. "Exploring Collaboration Mechanisms for LLM Agents: A Social Psychology View." — [GitHub](https://github.com/zjunlp/MachineSoM)
- **Newer protocol variants** (descriptions only):
  - jonathansantilli/freemad (20 stars): a "Consensus-Free Multi-Agent Debate" orchestrator with transcripts and a dashboard. — [GitHub](https://github.com/jonathansantilli/freemad)
  - magnus919/hermes-council (54 stars): an expert-agent debate "in structured rounds, producing visible transcripts". — [GitHub](https://github.com/magnus919/hermes-council)

### Inferences
- For implementation, MAGI does not need a heavy framework. AutoGen is in maintenance mode, CrewAI has no consensus process, and the Agents SDK has no debate pattern. A plain FastAPI + asyncio state machine (as in Karpathy's council) is the fastest hackathon path. LangGraph is the best fit if MAGI wants checkpointing or resume, as TradingAgents does.
- MALLM is the best ready-made **evaluation harness** for MAGI's "baseline vs. single LLM" claim. It already includes ethics datasets and a range of decision protocols, MAGI's unanimity rule could be plugged in as a protocol, and Kaesberg et al. give published baselines to compare against.
- The finding that more rounds before voting reduce performance cautions against MAGI's three-round loop. MAGI should measure whether rounds 2–3 help.
- TradingAgents is the strongest precedent for **competing objectives plus tools**: bull vs. bear, a risk team, tool-using analysts and an approve/reject gate. It is domain-locked to trading, however, and has no unanimity or human-escalation rule.
- AGNTCY's unimplemented "Decentralized Consensus Agents" pattern, along with the unimplemented "Approval Gate Agent", is an open slot in the Cisco reference library. A MAGI build on SLIM group communication or A2A could be presented as the first concrete implementation of that pattern. This fits the Cisco "Collective Intelligence" track.

### Gaps
- I did not find an official LangGraph "debate" template in langchain-ai repos, only community examples. This was not exhaustively searched.
- CAMEL's and AgentVerse's specific decision-making modules (for example AgentVerse's "horizontal/vertical decision-making" from its paper) were not verified in the current code.
- Agent Laboratory's internal agent roles (PhD, Postdoc and so on) were not verified from the README.
- Microsoft Agent Framework's own debate or group-chat patterns were not examined.
- The Google co-scientist's original code is not public. Fidelity of the reimplementations to the *Nature* paper was not assessed.

---

## Key Question 4: Comparison catalog — how does each project compare with MAGI (similarities, what stands out, limitations)?

### Takeaway
Across the 25 entries below, the MAGI features that are **common** in the field are parallel independent first answers, seeing others' answers, a single revision round and majority or chairman aggregation. The features that are **rare** are unanimity or veto, more than two rounds, persona objectives that genuinely conflict, per-agent tools and human escalation. The features that are **absent everywhere** are immutable versioned proposals, mid-debate evidence injection by the user, and a built-in single-LLM baseline comparison in the UI.

### Cited Findings
(Stars and dates are from the GitHub API on 2026-10-10. Mechanism details are from each repo's README as cited in KQ1–KQ3.)

| # | Project | Stars / last push | Models vs. personas | Rounds and decision rule | Standout features | Limitations vs. MAGI |
|---|---|---|---|---|---|---|
| 1 | [karpathy/llm-council](https://github.com/karpathy/llm-council) | 25,338 / 2025-11-22 | 4 different vendors; no personas | 1 answer + 1 anonymized ranking; **chairman** synthesizes | Same FastAPI+React stack as MAGI; anonymized peer review; huge mindshare | No vote, no iteration, no persona objectives, no human escalation; unmaintained |
| 2 | [andybhall/llm-council-governance](https://github.com/andybhall/llm-council-governance) | 21 / 2026-01-04 | 4 small open models | 7 structures incl. Deliberate→Vote, Agenda-Setter+Veto | **Only rigorous evaluation harness** among council forks (MMLU-Pro Math, 1,004 trials) | Math only; no UI; no personas |
| 3 | [DmitryBMsk/llm-council-plus](https://github.com/DmitryBMsk/llm-council-plus) | 131 / 2026-09-08 | OpenRouter/Ollama models | Karpathy 3-stage, selectable modes | Production hardening: streaming with cancel, persistence, usage tracking | Same chairman model; no debate |
| 4 | [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council) | 2,445 / 2026-04-26 | **One model, 5 advisor personas** | Peer review → chairman | Shows persona-on-one-model demand; decision-focused | Skill prompt, not an app; no vote; no escalation |
| 5 | [a1exsun/dsh-council](https://github.com/a1exsun/dsh-council) | 159 / 2026-09-08 | 2–8 models; per-role model choice | Answer → anonymous review → arbiter | Inspectable consensus, disagreements, blind spots | Arbiter decides; DSH plugin only |
| 6 | [jason-chao/MAGI](https://github.com/jason-chao/MAGI) | 2 / 2026-04-15 | GPT/Claude/Gemini (different vendors) | Round 1 + optional deliberative round; 8 methods (vote, consensus, minority, etc.) | Confidence-scored JSON; rapporteur and minority report; pseudonymous deliberation; PyPI package; governance-theory grounding | ≤2 rounds; no unanimity loop; no human escalation; no tools; low traction |
| 7 | [TomaszRewak/MAGI](https://github.com/TomaszRewak/MAGI) | 163 / 2024-04-01 | GPT-3.5 ×3 with scientist/mother/woman prompts | Single round; **any "no" means no; yes only if all unconditional yes** (de facto unanimity) | Iconic Evangelion UI; conditional-yes state | No debate or revision; GPT-3.5; stale |
| 8 | [lordpba/AI_Magi](https://github.com/lordpba/AI_Magi) | 27 / 2025-11-07 | One provider/model; science, ethics and practical personas | Single pass → synthesis | CrewAI + Gradio; optional web search; HF Spaces deploy | No vote, no debate |
| 9 | [atrix228/magi-system](https://github.com/atrix228/magi-system) | 0 / 2026-06-26 | Per-brain model choice (100+ models via router) | Independent → cross-examination → majority vote with dissent | Android app; live reasoning streams; voice verdict; NERV UI | Source apparently not published; majority, not unanimity |
| 10 | [float1122/magi-system](https://github.com/float1122/magi-system) | 9 / 2026-07-01 | Claude subagents, 3 persona cores | 2/3 majority; **3/3 unanimity + veto for grave ops** | Tiered rule by stakes; 10–20 self-verifying judgment nodes; orchestrator verifies one fact | Coding-decision skill only; no multi-round revision; no human loop |
| 11 | [Git-Hacking/MAGI](https://github.com/Git-Hacking/MAGI) | 0 / 2026-08-24 | 3 different OpenRouter models | Round 1 → Round 2 (see others) → final APPROVE/REJECT; majority | Live streaming war-room UI; suggests same-model vs. different-model experiment | Majority; no escalation; no eval |
| 12 | [Adrian-Sandwich/magi-council](https://github.com/Adrian-Sandwich/magi-council) | 0 / 2026-09-25 | Persona per seat, swappable providers (CLI/MCP heads with tools; API heads without) | Multi-round, mind changes tracked; ruling + minority report; **human arbitration; unanimous approval to auto-merge** | Memory graph; executes plans; per-seat cost metrics; seat quarantine | Developer-ops tool; heavy setup (Postgres); no traction; docs partly Spanish |
| 13 | [nlink-jp/magi-system](https://github.com/nlink-jp/magi-system) | 0 / archived 2026-07-31 | Local LLM ×3 personas with priorities and emotions | Up to MAX_TURNS; convergence-vote threshold plus coverage gate | **Anti-groupthink mechanics**: max-disagreement speaker selection, novelty check, coverage check, facilitator warnings | Archived; Japanese only; TUI |
| 14 | pMAGI ([Scrapbox](https://scrapbox.io/nishio-en/pMAGI-2024-02-04)) | n/a (web app) | Ideological personas | STRONG YES…STRONG NO; consensus if all same direction, weak if some neutral; **explicitly no majority vote** | Graded-stance consensus | Single pass; precomputed outputs; code availability unknown |
| 15 | [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | 110,520 / 2026-10-03 | Role agents; quick vs. deep model tiers, per-tier provider | Bull/bear debate (`max_debate_rounds`) → trader → risk debate → PM approve/reject | **Tools per agent**, competing objectives, persistent memory with outcome reflection | Trading-only; manager decides, no unanimity; no human escalation |
| 16 | [microsoft/autogen](https://github.com/microsoft/autogen) | 61,345 / 2026-04-15 | Any | Debate pattern: N rounds over sparse topology → majority vote | Pub/sub topology; reference debate doc | Maintenance mode; math benchmark demo only |
| 17 | [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 59,546 / 2026-10-10 | Role-playing agents | Sequential or hierarchical (manager); consensual = TODO | Easy persona agents (used by lordpba/AI_Magi) | No consensus or vote primitive |
| 18 | [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | 29,954 / 2026-10-08 | Any | Handoffs, parallelization, LLM-as-judge, human-in-the-loop examples | Built-in human-in-the-loop and guardrail patterns | No debate or vote pattern |
| 19 | [Multi-Agent-LLMs/mallm](https://github.com/Multi-Agent-LLMs/mallm) | 67 / 2026-10-10 | Configurable personas and agents | 7 decision protocols (consensus, approval, ranked, cumulative, simple voting, judge…), 5 discussion paradigms | **Evaluation harness** with ethics datasets; companion "Voting or Consensus?" findings | Research CLI; no UI; no tools; no human loop |
| 20 | [dinobby/ReConcile](https://github.com/dinobby/ReConcile) | 207 / 2023-10-03 | **Different vendors** (ChatGPT, PaLM, Claude) | Multi-round; **confidence-weighted vote** | "Convincing" explanations; up to +11.4% | Stale; benchmark-only; Claude via cookies hack |
| 21 | [Skytliang/Multi-Agents-Debate](https://github.com/Skytliang/Multi-Agents-Debate) (MAD) | 615 / 2025-12-16 | Same model; affirmative "devil" vs. negative "angel" | Tit-for-tat rounds; **judge** decides | Counters Degeneration-of-Thought | 2 debaters + judge; no vote; research code |
| 22 | [composable-models/llm_multiagent_debate](https://github.com/composable-models/llm_multiagent_debate) (Du et al.) | 552 / 2025-04-24 | Multiple instances of same model | N agents × R rounds of mutual critique → final answers | Canonical "society of minds" debate baseline | Benchmark scripts only |
| 23 | [thunlp/ChatEval](https://github.com/thunlp/ChatEval) | 343 / 2024-10-19 | Persona referees | Debate → judgment on which text is better | Persona diversity improves alignment with human eval | Evaluation use case only; stale |
| 24 | [Kaimen-Inc/Co-Scientist](https://github.com/Kaimen-Inc/Co-Scientist) / [conradry/open-coscientist-agents](https://github.com/conradry/open-coscientist-agents) | 270 / 2026-08-03; 69 / 2025-07-22 | Role agents | **Elo tournament via pairwise simulated debates**; evolution of hypotheses | Ranking many candidate proposals; Streamlit tournament viewer (conradry) | Science-hypothesis domain; no unanimity or human escalation |
| 25 | [agntcy/coffeeAgntcy](https://github.com/agntcy/coffeeAgntcy) | 111 / 2026-10-09 | Supply-chain agents over SLIM/NATS/A2A/MCP | "Decentralized Consensus Agents" pattern: belief updates → merge agent, with caps, dampening, votes or human tie-breaks | Cisco track's own reference; interop and observability | **Consensus pattern documented but not implemented** (empty topology) |

Also relevant, but not in the table:
- [haizelabs/verdict](https://github.com/haizelabs/verdict) (judge or jury protocol composition, 348 stars).
- [togethercomputer/MoA](https://github.com/togethercomputer/MoA) (layered aggregation, 2,982 stars).
- [instadeepai/DebateLLM](https://github.com/instadeepai/DebateLLM) (protocol benchmark, 62 stars).
- [yusufipk/opencode-safeguard](https://github.com/yusufipk/opencode-safeguard) (a jury that can "escalate").
- [mdrbx/nerv-ui](https://github.com/mdrbx/nerv-ui) (React NERV-style UI kit, 92 stars).

### Inferences
- **Scale tiers.** One project has mass adoption with debate as a core mechanism (TradingAgents, 110k stars). One has mass adoption with a council (llm-council, 25k). General frameworks sit at 17k–71k. Every MAGI-branded clone has 163 stars or fewer, and most have 0. The Evangelion MAGI concept is crowded with hobby projects, but **no clone has become the reference implementation**, so the niche is still open for a polished, evaluated version.
- **The three most common critiques MAGI can answer:**
  - "Same model = no real diversity" (andybhall's self-consistency result; Git-Hacking's suggested experiment).
  - "Councils converge to bland consensus" (Krishnan's groupthink study).
  - "The chairman is a single point of failure" (Karpathy, dsh-council's arbiter, the TradingAgents PM).

  MAGI's unanimity-or-escalate rule addresses the third. MAGI should explicitly instrument the first two, for example by toggling same-model vs. different-model agents and by tracking minority ideas through rounds.

### Gaps
- Star counts for Hugging Face, PartyRock and Vercel-hosted projects (NAGI, LapiSteLLa, pMAGI) are not available.
- The table summarizes READMEs. I did not run any of these systems or verify claimed behavior in their code, except where noted (CrewAI enum, MALLM protocol files, AutoGen doc, coffeeAgntcy JSON).

---

## Key Question 5: What does none of these projects do that MAGI could add?

### Takeaway
The surveyed projects leave a clear set of open features:
- Voting on **immutable, versioned concrete proposals**, where agents amend by submitting a new version rather than editing in place.
- **User-injected evidence mid-debate** that agents must respond to.
- An **iterate-until-unanimous loop with a hard round cap and human escalation** as the primary decision rule, not a special case.
- **Per-persona tool scopes** tied to competing objectives.
- A **built-in single-LLM baseline comparison** shown alongside the council.
- A **concrete implementation of AGNTCY's unimplemented "Decentralized Consensus" pattern**.

Each feature has partial precedents, cited below, but no single project combines them.

### Cited Findings
- **Immutable proposal versions.** No project surveyed votes on versioned proposal objects:
  - Karpathy ranks free-text answers. — [llm-council](https://github.com/karpathy/llm-council)
  - jason-chao votes yes/no or on user-defined options. — [MAGI](https://github.com/jason-chao/MAGI)
  - Git-Hacking votes APPROVE/REJECT on the question itself. — [Git-Hacking/MAGI](https://github.com/Git-Hacking/MAGI)
  - Closest precedents: andybhall's "Agenda Setter + Veto", where a chairman proposes and the council votes ACCEPT/VETO. — [llm-council-governance](https://github.com/andybhall/llm-council-governance) TradingAgents' trader "transaction proposal", which the PM approves or rejects. — [TradingAgents](https://github.com/TauricResearch/TradingAgents)
  - The co-scientist reimplementations rank hypotheses via an Elo tournament and evolve them, but do not version them for a vote. — [Kaimen-Inc/Co-Scientist](https://github.com/Kaimen-Inc/Co-Scientist)
- **Mid-debate evidence injection.** No surveyed project lets the *user* inject new evidence partway through a debate:
  - nlink-jp's facilitator intervenes automatically on coverage gaps. — [nlink-jp/magi-system](https://github.com/nlink-jp/magi-system)
  - Adrian-Sandwich injects prior *memory* at the start. — [magi-council](https://github.com/Adrian-Sandwich/magi-council)
  - coffeeAgntcy's pattern describes peers exchanging "belief updates and evidence" (unimplemented). — [coffeeAgntcy pattern doc](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/api/agentic_workflows/docs/workflows/decentralized_consensus_agents.md)
- **Unanimity with escalation after N failed rounds.**
  - Human arbitration exists in Adrian-Sandwich/magi-council. — [README](https://github.com/Adrian-Sandwich/magi-council)
  - "Escalate" exists as a jury verdict in opencode-safeguard. — [GitHub](https://github.com/yusufipk/opencode-safeguard)
  - coffeeAgntcy mentions "human tie-breaks" in principle. — [pattern doc](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/api/agentic_workflows/docs/workflows/decentralized_consensus_agents.md)
  - Unanimity appears only as single-shot (TomaszRewak) or stakes-tiered (float1122). — [TomaszRewak/MAGI](https://github.com/TomaszRewak/MAGI); [float1122/magi-system](https://github.com/float1122/magi-system)
  - No project found makes "unanimity within 3 rounds, else human" the core contract.
- **Per-agent tools aligned with objectives.**
  - TradingAgents analysts each have their own tools. — [README](https://github.com/TauricResearch/TradingAgents)
  - Adrian-Sandwich lets only MCP/CLI heads run tools. — [README](https://github.com/Adrian-Sandwich/magi-council)
  - lordpba offers optional web search for everyone. — [README](https://github.com/lordpba/AI_Magi)
  - No MAGI clone gives the scientist evidence tools, the ethicist safety or policy tools, and the creative agent ideation tools.
- **Baseline comparison.**
  - Only andybhall measures council vs. best single model, offline. — [llm-council-governance](https://github.com/andybhall/llm-council-governance)
  - MALLM provides offline evaluation. — [mallm](https://github.com/Multi-Agent-LLMs/mallm)
  - jason-chao explicitly reports no benchmark. — [jasontc.net](https://jasontc.net/work/magi.html)
  - No user-facing app shows a single-LLM answer next to the council result.
- **Anti-groupthink instrumentation.** Councils drop about 75% of good single-model ideas. — [Strange Loop Canon](https://www.strangeloopcanon.com/p/llm-councils-show-groupthink) Only nlink-jp actively counters convergence, using novelty and maximum-disagreement rules. — [nlink-jp/magi-system](https://github.com/nlink-jp/magi-system)
- **Protocol choice evidence.** More rounds before voting reduces accuracy, and voting suits reasoning while consensus suits knowledge tasks. — [arXiv 2502.19130](https://arxiv.org/html/2502.19130v4) Deliberate→Vote was the best structure tested. — [llm-council-governance](https://github.com/andybhall/llm-council-governance)
- **AGNTCY.** coffeeAgntcy has no implemented consensus or approval-gate workflow; both entries have empty topologies. — [starting_workflows.json](https://github.com/agntcy/coffeeAgntcy/blob/main/coffeeAGNTCY/coffee_agents/lungo/api/agentic_workflows/starting_workflows.json)

### Inferences
- **Immutable proposals + version history.** Each round's vote is over hashed proposal versions (e.g., P1.0, then P1.1 amended by BALTHASAR). The UI can show exactly *which version* each agent rejected and why. This fixes the "vote on vague prose" problem common to llm-council-style tools.
- **Evidence injection as a first-class event.** The user drops a fact or document mid-debate. Each agent must state whether and how it changes its position, and the "mind change" is logged (Adrian-Sandwich already tracks mind changes, but not around injected evidence). This makes a strong live demo moment.
- **Escalation packet.** When three rounds fail, MAGI hands the human a structured dossier: the final proposal versions, each agent's blocking objection, what evidence would flip each agent, and a minority report (borrowing jason-chao's minority report idea).
- **Same-model vs. different-model toggle + single-LLM baseline panel.** This directly tests the self-consistency critique and Git-Hacking's suggested experiment. MAGI could reuse MALLM datasets (ETHICS, MoCaMoral, SimpleEthicalQuestions) or andybhall's harness design for a small offline eval to quote in the pitch.
- **Groupthink metrics.** Track per-round "unique ideas surviving" (Krishnan's method) and flag "suspicious unanimity", for example unanimity reached in round 1 with no objections, using nlink-jp-style novelty checks.
- **AGNTCY angle.** Implement MAGI's three agents as A2A agents over SLIM group communication, with Observe SDK traces. MAGI can then be pitched as the first working reference for coffeeAgntcy's "Decentralized Consensus Agents" plus "Approval Gate Agent" (human oversight) patterns. This maps directly to the Cisco track.
- **Retro UI.** TomaszRewak's design is the visual reference that most clones reuse. mdrbx/nerv-ui offers ready React components, but its own guidance to use "original labels" suggests keeping a homage rather than copying trademarked assets.
- **Positioning sentence for judges:** "Karpathy's council has a chairman; MAGI has no chairman: three agents with conflicting mandates must unanimously ratify a specific, versioned proposal, or the human decides."

### Gaps
- I cannot rule out closed-source or unindexed projects that already implement versioned-proposal voting or user evidence injection. The search covered GitHub repo search, two curated lists and web search, not exhaustive code search.
- No published evidence was found on whether *persona diversity on one base model* matches *model diversity* for ethical or open-ended questions. andybhall's self-consistency result covers same-model sampling *without* personas, on math only.
- Licensing and trademark implications of Evangelion-themed UIs were not researched. The projects themselves include fan disclaimers, e.g. float1122 and lordpba.
