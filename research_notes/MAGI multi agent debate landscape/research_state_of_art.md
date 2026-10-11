# Academic State of the Art: Multi-Agent LLM Debate, Deliberation, Negotiation and Consensus (for MAGI)

Scope note: These notes cover research through October 2026. Sources marked "(abstract only)" were checked only at the arXiv abstract level, so their details were not verified against the full text. Items marked "(not re-verified this session)" are well-known papers cited from prior knowledge. Their arXiv IDs and venues are standard, but no specific numbers are quoted for them. Many 2026 items are unreviewed arXiv preprints, and the notes say so wherever that applies.

---

## Q1. Does multi-agent debate beat simpler baselines (single LLM, self-consistency, majority vote)?

### Takeaway
Vanilla debate among copies of the same model usually does **not** beat a compute-matched majority vote or self-consistency, and most of the reported "debate gains" come from ensembling. NeurIPS 2025 work proves that homogeneous debate is a martingale, meaning it does not raise expected correctness. Debate starts to beat voting only when something breaks that symmetry: different models, diverse starting hypotheses, calibrated confidence, a correctly-arguing dissenter, or information asymmetry. For MAGI this means one LLM is too weak a baseline. Judges who know the literature will ask for **majority vote of N samples at the same token budget** and an **"independent analysis + vote, no debate"** ablation.

### Cited Findings
**Early positive results (2023-2024)**
- Du et al., "Improving Factuality and Reasoning in Language Models through Multiagent Debate" (ICML 2024; arXiv 2305.14325). Multiple instances propose answers, read each other's answers over several rounds, and converge. They report gains on arithmetic, GSM8K, chess, biographies and MMLU. Their baselines included single-agent reflection and a multi-agent majority vote (not re-verified this session) — [arXiv 2305.14325](https://arxiv.org/abs/2305.14325)
- Liang et al., "Encouraging Divergent Thinking in LLMs through Multi-Agent Debate" (EMNLP 2024; arXiv 2305.19118). Introduces "Degeneration-of-Thought": once a model is confident, self-reflection stops producing new ideas. MAD uses affirmative and negative debaters plus a judge, a "tit-for-tat" disagreement level, and an adaptive break. Evaluated on counter-intuitive arithmetic (CIAR) and commonsense MT. The abstract notes that a judge may not be fair when the debaters are different LLMs (not re-verified this session) — [arXiv 2305.19118](https://arxiv.org/abs/2305.19118)
- ChatEval (Chan et al., ICLR 2024; arXiv 2308.07201). A multi-agent referee team for evaluating text. It reports that diverse role prompts are essential, and that giving every agent the same role description degrades performance (not re-verified this session) — [arXiv 2308.07201](https://arxiv.org/abs/2308.07201)
- ReConcile (Chen, Saha, Bansal; ACL 2024; arXiv 2309.13007). A "round table" of **different model families**. Each round shares grouped answers, explanations, each agent's confidence, and human "convincing" demonstrations, and the final answer is a **confidence-weighted vote**. It reports up to 11.4% over prior single- and multi-agent baselines, beats GPT-4 on 3 datasets, and gets +8% on MATH from mixing agents. Its component analysis attributes much of the gain to **model diversity** — [arXiv 2309.13007](https://arxiv.org/abs/2309.13007)
- Hegazy (arXiv 2410.12853, 2024). A diverse panel of medium models (Gemini-Pro, Mixtral 8x7B, PaLM 2-M) reached **91% on GSM-8K after 4 rounds**, beating GPT-4. Three Gemini-Pro copies reached only **82%**. The panel also reports **94% on ASDiv** — [arXiv 2410.12853](https://arxiv.org/abs/2410.12853)
- Khan et al., "Debating with More Persuasive LLMs Leads to More Truthful Answers" (ICML 2024; arXiv 2402.06782). Debate between expert models with hidden text helps non-expert judges, human and LLM, find the truth on QuALITY. This is debate as **scalable oversight**: the goal is to inform a judge, not for the debaters to reach consensus (not re-verified this session) — [arXiv 2402.06782](https://arxiv.org/abs/2402.06782)

**Skeptical and corrective results (2023-2026)**
- Smit et al., "Should we be going MAD?" (arXiv 2311.17371; v3 Jul 2024; also published at ICML 2024 per my recollection, while the arXiv page lists no venue). MAD "does not reliably outperform" self-consistency or ensembling over multiple reasoning paths. With tuning, especially of the **agent agreement level**, Multi-Persona can beat all non-debate protocols. MAD is more hyperparameter-sensitive than other methods — [arXiv 2311.17371](https://arxiv.org/abs/2311.17371)
- Wang et al., "Rethinking the Bounds of LLM Reasoning: Are Multi-Agent Discussions the Key?" (ACL 2024; arXiv 2402.18272). A single agent with a strong prompt (demonstrations) roughly matches multi-agent discussion. Discussion helps mainly when no demonstrations are given (not re-verified this session) — [arXiv 2402.18272](https://arxiv.org/abs/2402.18272)
- Zhang et al., "Stop Overvaluing Multi-Agent Debate" (position paper; arXiv 2502.08788). Evaluated 5 MAD methods × 9 benchmarks × 4 models. MAD "often fail[s] to outperform" CoT and Self-Consistency despite using more compute. **Model heterogeneity** is a "universal antidote" that consistently improves MAD frameworks. The abstract gives no numbers for this — [arXiv 2502.08788](https://arxiv.org/abs/2502.08788)
- **Choi, Zhu & Li, "Debate or Vote: Which Yields Better Decisions in Multi-Agent LLMs?" (NeurIPS 2025 Spotlight; arXiv 2508.17536).** The third author appears as "Sharon Li" in the paper and as "Yixuan Li" on arXiv; this is the same person — [arXiv HTML v2](https://arxiv.org/html/2508.17536v2); [NeurIPS poster](https://neurips.cc/virtual/2025/poster/116557)
  - Setup: 7 benchmarks (Arithmetics, GSM8K, MMLU Pro-Medicine, MMLU Formal Logic, HellaSwag, CommonsenseQA, HH-RLHF). Qwen2.5-7B and Llama3.1-8B, plus a Qwen2.5-32B check. 5 agents, 2/3/5 rounds.
  - Qwen2.5-7B averages: single 0.7205, **majority vote 0.7691**, Decentralized MAD 0.7377, Sparse MAD 0.7330, Centralized MAD 0.6551. Llama3.1-8B: single 0.6203, **majority vote 0.7242**, best MAD 0.6990.
  - Theory: beliefs are modeled with a Dirichlet-Compound-Multinomial. Under homogeneous fully connected agents, debate is a **martingale**, so expected belief in the correct answer does not change. Majority voting's error probability decays exponentially in N even when the correct answer's probability is below 0.5. Empirically, mean agent accuracy stays flat across rounds.
  - Interventions (Qwen-7B, T=5):
    - Vanilla MAD scores 0.7084.
    - **MAD-Oracle** locks correct answers using ground truth, so it is impractical. It reaches 0.8289.
    - **MAD-Conformist** keeps an answer if it matches the prior-round majority. It reaches 0.7524.
    - **MAD-Follower** adopts the majority with probability 0.3. It reaches 0.7577.
    - Both practical variants still trail plain majority vote (0.7691).
  - Persona-diverse agents: on MMLU Pro-Medicine, Decentralized MAD (0.8419) beat majority vote (0.8235). On GSM8K, majority vote (0.9367) still won. Evidence that personas help is limited.
  - Recommendations: start from simple ensembling, and if you debate, protect correct answers across rounds.
- **Zhu, Zhang, Chi, Stafford, Collier, Vlachos, "Demystifying Multi-Agent Debate: The Role of Confidence and Diversity" (arXiv 2601.19921; Jan 2026, v3 Jun 2026; no venue listed; abstract only).** Under homogeneous agents and uniform updates, debate preserves expected correctness. They add two ingredients drawn from human deliberation research:
  - **Diversity-aware initialisation**: pick a diverse pool of initial candidate answers so the correct hypothesis is more likely to be present. In theory this raises the prior probability of success.
  - **Confidence-modulated debate**: agents state calibrated confidence and condition their updates on others' confidence. In theory this lets debate drift systematically toward the correct hypothesis.
  - Result: across 6 reasoning QA benchmarks, both methods beat vanilla MAD **and** majority vote. The abstract gives no numbers — [arXiv 2601.19921](https://arxiv.org/abs/2601.19921)
- Kaesberg, Becker, Wahle, Ruas, Gipp, "Voting or Consensus? Decision-Making in Multi-Agent Debate" (ACL Findings 2025; arXiv 2502.19130). Compares 7 decision protocols with everything else held fixed.
  - **Voting protocols do +13.2% better on reasoning tasks** and **consensus protocols do +2.8% better on knowledge tasks**.
  - **More agents help, and more discussion rounds before voting hurt.**
  - Two diversity methods: All-Agents Drafting (up to +3.3%) and Collective Improvement (up to +7.4%) — [arXiv 2502.19130](https://arxiv.org/abs/2502.19130)
- Hu et al., "Multi-Agent Debate for LLM Judges with Adaptive Stability Detection" (NeurIPS 2025; arXiv 2510.12697). Claims that debate beats majority vote for LLM-as-judge tasks. It adds adaptive stopping by modeling consensus with a time-varying Beta-Binomial mixture plus a Kolmogorov-Smirnov test (abstract/summary only) — [NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/42475c537936b2394b5015e871765056-Abstract-Conference.html)
- Bertalanič & Fortuna, "The Cost of Consensus: Isolated Self-Correction Prevails Over Unguided Homogeneous MAD" (arXiv 2605.00914; Apr 2026; listed for the ACM Conference on AI and Agentic Systems). Setup: 10 same-model agents, 3 rounds, 7-8B models, GSM-Hard and MMLU-Hard.
  - Debate uses **2.1-3.4× more tokens** than isolated self-correction (up to 28,631 tokens per problem) for **equal or lower accuracy**.
  - "Isolated self-correction consistently offers a more favorable cost-accuracy tradeoff" — [arXiv 2605.00914](https://arxiv.org/abs/2605.00914)
- Wu, Li & Li, "Can LLM Agents Really Debate?" (arXiv 2511.07784; Nov 2025 preprint). Controlled study on Knight-Knave-Spy puzzles. **Intrinsic reasoning strength and group diversity** dominate outcomes, while order and confidence visibility give limited gains. Majority pressure suppresses independent correction. Effective teams overturn an incorrect consensus, and validity-aligned reasoning predicts improvement — [arXiv 2511.07784](https://arxiv.org/abs/2511.07784)
- Free-MAD (Cui et al.; arXiv 2509.11035; ACL Findings 2026). Combines anti-conformity prompts (find flaws in others' outputs) with **trajectory-level scoring** in place of a last-round vote. Later-round opinion shifts are down-weighted by a factor f=(k+1)^-1. The authors claim gains on 8 benchmarks with a single debate round and better robustness to attacks — [arXiv 2509.11035](https://arxiv.org/abs/2509.11035); [ACL Anthology](https://aclanthology.org/2026.findings-acl.1600/)

### Inferences
- MAGI's planned design (one model, three persona prompts, unanimity) is the configuration the literature finds **least likely** to beat voting on accuracy. Choi et al.'s martingale result applies almost directly. MAGI should therefore not pitch "debate improves accuracy". Its strengths lie elsewhere:
  - calibrated abstention and escalation
  - evidence handling
  - resistance to manipulation
  - transparent, auditable disagreement

  Or MAGI should add the symmetry-breakers the literature validates: heterogeneous models, diversity-aware initialization, confidence-modulated updates, and a designated dissenter.
- The baseline set needed for credibility (the 24h build cost of each is small):
  - B1: single LLM with CoT.
  - B2: self-consistency, i.e. majority vote of k samples from the same model, **token-matched** to MAGI.
  - B3: "MAGI round 0 only", meaning the three personas answer independently and then vote with no debate. This isolates the effect of debate (Choi et al.'s decomposition).
  - B4: a single LLM asked to role-play all three perspectives in one prompt, which tests Wang et al.'s claim.
- If MAGI can use two or three different providers (for example Claude, GPT and Gemini, or an open-weights model), that is the strongest single lever for real disagreement and accuracy gains (Zhang 2025; Hegazy 2024; ReConcile).
- Cap rounds at 2-3 and stop early on stability (Kaesberg: more rounds hurt). MAGI's existing 3-round cap is consistent with the literature.

### Gaps
- No full-text numbers were obtained for Zhu et al. 2026 (2601.19921), so effect sizes are unknown.
- Du et al.'s and Liang et al.'s exact table numbers were not re-verified this session.
- I found no study testing debate on **open-ended, value-laden decisions** with ground truth (MAGI's natural domain). Most accuracy evidence comes from math and MCQ.

---

## Q2. Failure modes (sycophancy/conformity, confident-wrong persuasion, degeneration, bland compromise, persona non-diversity, correlated errors) and mitigations that work

### Takeaway
The dominant failure is **conformity**: agents abandon correct answers under peer pressure. It is measurable and large: 57-77% of conformity flips are correct→wrong, and modal adoption reaches up to 85.5%. It appears even in base models without RLHF. Contributing factors:
- Even vacuous "reasoning-like" text persuades.
- Personas on one model add only marginal diversity.
- Frontier models share errors (60% agreement when both are wrong).

Mitigations with evidence:
- heterogeneous models
- **anonymizing** peer responses
- a single **structured dissenter**
- calibrated **confidence**
- trajectory-level (not final-round) aggregation
- sparse or regulated communication

### Cited Findings
**Conformity and sycophancy**
- Wynn, Satija, Hadfield, "Talk Isn't Always Cheap" (ICML 2025 MAS workshop; arXiv 2509.05396). Debate can reduce accuracy over time even when stronger models outnumber weaker ones. Models switch correct→incorrect in response to peer reasoning and "favor agreement over challenging flawed reasoning". The disagreement rate falls across rounds, and that fall correlates with degradation — [arXiv 2509.05396](https://arxiv.org/abs/2509.05396)
- Hao et al., "Not All Flips Are Conformity: Decomposing Stance Convergence in Multi-Agent LLM Debate" (arXiv 2606.00820; May 2026 preprint). Splits the flip rate into spontaneous instability, stance-induced conformity, and reasoning-induced persuasion, using counterfactual controls.
  - **37%** of agent-question observations changed under self-reflection alone (MMLU-Pro).
  - Strict conformity was **29%**, and **57-77% of conformity flips were correct→wrong**.
  - **Vacuous reasoning** led **20-39%** of resistant agents to adopt errors.
  - Harmful conformity is predictable from Round-0 features (AUC 0.79). A targeted intervention cut it by 13.6 pp.
  - Caveat: without correctness labels, reducing peer adoption did **not** improve accuracy, because the intervention cannot tell harmful influence from beneficial influence — [arXiv 2606.00820](https://arxiv.org/abs/2606.00820)
- Kumarappan & Mujoo, "Not Just RLHF: Why Alignment Alone Won't Fix Multi-Agent Sycophancy" (arXiv 2605.12991; 2026 preprint).
  - Across 4 model families, **base models show the same (higher) yield** to peer pressure as Instruct models.
  - Activation patching localizes the effect to mid-layer attention, and pressure suppresses clean-reasoning features.
  - Channel framing × consensus strength gives a **47.5 pp yield gap** at majority consensus.
  - **A single correctly-arguing dissenter cuts yield by 54-73 pp.**
  - The best prompt-only defense fails on out-of-scope attack variants — [arXiv 2605.12991](https://arxiv.org/abs/2605.12991)
- Bertalanič & Fortuna (arXiv 2605.00914) name three pathways:
  - sycophantic conformity, with modal adoption up to **85.5%**
  - contextual fragility, where peer rationales destabilize correct reasoning in up to **70.0%** of cases
  - consensus collapse, where plurality discards correct answers already in the pool, giving an **oracle gap up to 32.3 pp**

  Conformity is already high with 2 peers and grows with exposure, and it grows *with* more initial diversity (temperature) — [arXiv 2605.00914](https://arxiv.org/abs/2605.00914)
- Choi, Zhu, Li, "When Identity Skews Debate: Anonymization for Bias-Reduced Multi-Agent Reasoning" (ACL 2026 Main; arXiv 2510.07517).
  - Models debate as an identity-weighted Bayesian update and defines an **Identity Bias Coefficient (IBC)**.
  - Identity bias is widespread, and **sycophancy is far more common than self-bias**.
  - **Response anonymization** (removing "self" and "peer" labels) reduces the bias.
  - Earlier versions also defined Conformity and Obstinacy metrics. The abstract gives no numbers — [arXiv 2510.07517](https://arxiv.org/abs/2510.07517)
- Estornell & Liu, "Multi-LLM Debate: Framework, Principals, and Interventions" (NeurIPS 2024; **Yang Liu is at UC Santa Cruz**, a useful local hook). When models have similar capabilities or responses, debate converges to the majority. If the majority shares a misconception from common training data, you get an **echo chamber**. Proposed interventions: **diversity-pruning** (maximize the entropy of responses), **quality-pruning**, and **misconception-refutation**. They improve 4 benchmarks — [NeurIPS 2024 PDF](https://proceedings.nips.cc/paper_files/paper/2024/file/32e07a110c6c6acf1afbf2bf82b614ad-Paper-Conference.pdf); [poster](https://neurips.cc/virtual/2024/poster/93363)
- Qian, "What Does Multi-Agent Debate Actually Change?" (arXiv 2609.08016; Sep-Oct 2026 preprint). Ran 2-3 member committees on 50 GlobalOpinionQA questions.
  - Tone dominates *stated* agreement: 70.7-96.3% strong agreement under friendly instructions versus 9.5-19.3% under hostile ones.
  - The **selected option stays the same in over 90%** of initial-vs-final comparisons.
  - Expressed disagreement ≠ actual position revision — [arXiv 2609.08016](https://arxiv.org/abs/2609.08016)

**Persuasion by confident or adversarial agents**
- Amayuelas et al., "MultiAgent Collaboration Attack" (arXiv 2406.14711, 2024). An adversary in a debate network sways the others, and **persuasive ability is the main determinant** of how far. The paper offers metrics for system accuracy and agreement, and prompt-based mitigation is only partially explored — [arXiv 2406.14711](https://arxiv.org/abs/2406.14711)
- MAD-Spear (Cui & Du; arXiv 2507.13038). Compromising a small subset of agents to emit multiple plausible-but-wrong answers exploits conformity and degrades consensus across 5 benchmarks — [arXiv 2507.13038](https://arxiv.org/abs/2507.13038)
- Nilayam et al., "Heterogeneous LLM Debate Under Adversarial Peers" (arXiv 2606.19826; 2026 preprint).
  - An **honest heterogeneous peer** cut honest agents' harmful-revision rate from **89% to 35%** (Llama-3.1-70B, MATH-hard). An adversarial peer pushed it back to **90%**.
  - With a same-family adversary already present, adding an honest heterogeneous peer cut flips on initially-correct items from **31% to 6%**.
  - The **end-of-debate flip rate** reveals damage that the conditional revision rate masks — [arXiv 2606.19826](https://arxiv.org/abs/2606.19826)

**Degeneration and bland compromise**
- Degeneration-of-Thought: self-reflection stalls once a model is confident, which motivated forced divergent debate with "tit-for-tat" (Liang et al.) — [arXiv 2305.19118](https://arxiv.org/abs/2305.19118)
- HiddenBench and its successor show "premature convergence on shared evidence while critical distributed facts remain unexplored" — [arXiv 2505.11556](https://arxiv.org/abs/2505.11556v2)
- The Habermas Machine's own analysis is evidence *against* the bland-compromise worry, at least for its design. Text embeddings showed that winning statements "incorporated dissenting voices while respecting the majority position" — [Tessler et al., Science 2024](https://doi.org/10.1126/science.adq2852)

**Persona non-diversity and same-model correlated errors**
- Kim, Garg, Peng, Garg, "Correlated Errors in Large Language Models" (ICML 2025; arXiv 2506.07962). Across 350+ LLMs, models agree **60% of the time when both are wrong**, against roughly 33% expected by chance. **Larger, more accurate models are more correlated**, even across providers — [arXiv 2506.07962](https://arxiv.org/abs/2506.07962); [PMLR](https://proceedings.mlr.press/v267/kim25e.html)
- The ICLR 2025 "Diverse Multi-Agent Debate" work argues that persona-assigned agents still use the same reasoning methods (a "fixed mental set"). It recommends **different reasoning methods per agent**, not just different roles — [ICLR 2025 poster](https://iclr.cc/virtual/2025/poster/28079)
- The 2026 systematic review of 141 MAD studies finds the field defaults to "static fully connected topologies, verbatim exchange, short-term memory and voting resolution" by convention, not by comparison. Most debates use the same base model — [Motger et al., arXiv 2607.26212](https://arxiv.org/abs/2607.26212)

**Other structural mitigations**
- DEAR (arXiv 2608.03648, 2026 preprint). Regulates "debate relationships", meaning who references whom, via RL to mitigate blind conformity. It argues that individual confidence and perplexity signals can worsen conformity (abstract only; no numbers) — [arXiv 2608.03648](https://arxiv.org/abs/2608.03648)
- Choi et al. 2025: Sparse MAD performs comparably to Decentralized MAD, and Centralized (hub) MAD is worst — [arXiv 2508.17536](https://arxiv.org/html/2508.17536v2)
- MAST taxonomy, Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2503.13657). 14 failure modes in 3 categories: specification, inter-agent misalignment, and verification (not re-verified this session) — [arXiv 2503.13657](https://arxiv.org/abs/2503.13657)

### Inferences
- **Anonymize inside the prompts, keep names in the UI.** Agents should read peers as "Analysis A / B" with the perspective tag, *without* a self/peer marker. MAGI keeps its themed UI and gets the ACL 2026 mitigation.
- **Mandatory change-of-mind justification.** Every position change must name its cause from a fixed enum:
  - `NEW_EVIDENCE` (cite id)
  - `NEW_ARGUMENT` (quote it)
  - `FOUND_ERROR_IN_OWN_REASONING`
  - `PEER_AGREEMENT_ONLY`

  Flag flips with no new argument as "possible conformity". This is a cheap, label-free proxy for Hao et al.'s decomposition. Hao et al. warn that suppressing adoption without labels does not raise accuracy, so this should be **flag and display**, not block.
- **Structured dissent.** Before any vote, BALTHASAR (or a rotating agent) must produce the strongest case against the leading proposal. One correct dissenter cuts yield by 54-73 pp (Kumarappan & Mujoo 2026).
- **Trajectory-aware final decision (Free-MAD).** If an agent abandons a high-confidence round-0 answer without a cited reason, count its round-0 answer, not its final one.
- **Run a self-reflection control.** Re-ask each agent once with its own answer only, without peers. The difference between that flip rate and the debate flip rate estimates **social influence**, which is a demonstrable metric.
- **Same-model personas will look diverse but err together** (Kim et al. 2025). Give each agent a different *reasoning method*, for example:
  - MELCHIOR: formal/quantitative decomposition
  - BALTHASAR: failure-mode / pre-mortem analysis
  - CASPER: analogy and implementation-path reasoning

  Also consider at least one different model family.

### Gaps
- A search summary reported a 2026 preprint in which persona-only diversity on identical models sits only slightly above a no-diversity baseline, with model-level differentiation as the main driver. I could not pin down which paper this is, so treat it as unverified. Choi et al. 2025's mixed persona results (above) are the verified evidence on this point.
- An LLM + linear-programming negotiation agent ("ASTRA", 2025) reportedly reaches Pareto-optimal multi-issue outcomes. It appeared only in a search summary, and no primary source was fetched.
- No numbers were obtained for anonymization's effect size (ACL 2026 abstract has none).
- I found no work specifically measuring "bland compromise" (semantic dilution of proposals over rounds) in LLM-agent negotiation. That is a possible measurement contribution.

---

## Q3. Negotiation and consensus mechanisms beyond majority/unanimity

### Takeaway
The strongest validated "consensus without a central decider" mechanism is the **Habermas Machine** (Science 2024):
- generate many candidate group statements
- score them with per-person preference models
- pick a winner by a **clone-independent social choice rule (Schulze)**
- iterate with private critiques

It beat human mediators (56% vs 44%) with N=5,734. LLM negotiation benchmarks show agents are manipulable (feigned desperation gives +20% payoff) and rarely Pareto-optimal (about 44-55%). MAGI's "immutable proposal versions + unanimity" maps naturally onto a Habermas-style generate → rank → aggregate → critique → revise loop. Adding a ranking rule and a Pareto filter before the unanimity vote would make MAGI's mechanism substantively grounded.

### Cited Findings
- **Habermas Machine.** Tessler, Bakker, Jarrett, … Parkes, Botvinick, Summerfield, "AI can help humans find common ground in democratic deliberation", *Science* 386, eadq2852 (18 Oct 2024), DOI 10.1126/science.adq2852 — [DOI](https://doi.org/10.1126/science.adq2852); [PDF mirror](https://www.rivista.ai/wp-content/uploads/2024/10/science.adq2852.pdf)
  - Architecture: two fine-tuned Chinchilla models. A generator proposes candidate group statements, and a **personalized reward model** predicts each member's ranking.
  - Aggregation: rankings are combined "using a social choice function with the 'independence of clones' property, ensuring that very similar candidate statements do not split the vote", namely the **Schulze method**.
  - Procedure: private opinions → candidate statements → participants rank → winner returned → participants write **private critiques** → revised candidates → re-rank → final preference between initial and revised. This is "caucus mediation".
  - N = **5,734** participants. HM statements were preferred **56% vs 44%** over human mediators (predicted p=0.575, CI 0.535-0.614) and rated more informative, clear and unbiased.
  - Groups were left **less divided**, while simply sharing opinions did not have that effect. Winning statements incorporated minority critiques while respecting the majority.
  - The result was replicated in a demographically representative virtual citizens' assembly.
  - Caveats from commentary: opinion shifts were modest, entrenched issues moved little, and critics ask whether the system "deliberates" or merely aggregates — [Knight Columbia commentary](https://knightcolumbia.org/content/can-ai-mediation-improve-democratic-deliberation)
- Generative Social Choice (Fish et al., arXiv 2309.01291; cited as ref 11 by the Habermas paper). An LLM generates candidate statements and queries agents' preferences, aiming for proportional representation guarantees (not re-verified this session) — [arXiv 2309.01291](https://arxiv.org/abs/2309.01291)
- Social choice with LLMs:
  - "An Electoral Approach to Diversify LLM-based Multi-Agent Collective Decision-Making" applies electoral rules to LLM agent groups — [arXiv 2410.15168](https://arxiv.org/abs/2410.15168)
  - "Evaluating Agents using Social Choice Theory" ranks agents by aggregating preferences with Borda, approval and other rules — [arXiv 2312.03121](https://arxiv.org/abs/2312.03121)
  - "LLM Voting: Human Choices and AI Collective Decision Making" — [arXiv 2402.01766](https://arxiv.org/abs/2402.01766). Findings not verified this session.
  - A March 2026 preprint, "Social Choice with Text: Collective Decision Making in the LLM Era" (Grandi, Bredereck, Delemazure, Endriss, Maly, Mattei, Maudet, Nardi, Szufa; HAL hal-05548117), exists per a bibliography entry. Its content is unverified — [bib](https://staff.fnwi.uva.nl/u.endriss/pubs/bib/GrandiEtAl2026.bib)
- Decision protocol matters: across 7 protocols, voting beats consensus on reasoning (+13.2%) and consensus beats voting on knowledge (+2.8%) — [Kaesberg et al., arXiv 2502.19130](https://arxiv.org/abs/2502.19130). Under injected misinformation, "consensus is more stable than voting under peer pressure" — [Becker et al., arXiv 2606.16710](https://arxiv.org/abs/2606.16710)
- **NegotiationArena** (Bianchi, Chia, Yuksekgonul, Tagliabue, Jurafsky, Zou; ICML 2024, PMLR 235:3935-3951; arXiv 2402.05863). Covers ultimatum, trading and buy/sell scenarios. GPT-4 was the best negotiator overall. **Feigning desperation raised payoffs by about 20%** against GPT-4, and agents showed anchoring bias and other irrationalities — [PMLR](https://proceedings.mlr.press/v235/bianchi24a.html); [arXiv](https://arxiv.org/abs/2402.05863)
- **LLM-Deliberation / scorable negotiation** (Abdelnabi, Gomaa, Sivaprasad, Schönherr, Fritz; arXiv 2309.17234; NeurIPS 2024 D&B per common citation, while the arXiv page lists no venue).
  - Multi-agent, multi-issue, semantically rich negotiation games with greedy and adversarial players.
  - "GPT-3.5 and small models mostly fail", and GPT-4 and Llama-3-70B still underperform — [arXiv 2309.17234](https://arxiv.org/abs/2309.17234)
  - A 2025 reproducibility study uses **Pareto-front membership** as the deal-quality metric and calls model comparison "ambiguous" — [arXiv 2502.16242](https://arxiv.org/abs/2502.16242)
- "Game-theoretic LLM: Agent Workflow for Negotiation Games" reports **Pareto-optimal outcome rates of roughly 44-55%** plus envy-freeness — [arXiv 2411.05990](https://arxiv.org/abs/2411.05990)
- "Strategic Tradeoffs Between Humans and AI in Multi-Agent Bargaining" supplies a linear-programming formulation of the Pareto-optimal surplus as a performance benchmark — [arXiv 2509.09071](https://arxiv.org/abs/2509.09071)
- "Are LLMs Effective Negotiators?" is a systematic evaluation of negotiation dialogue — [arXiv 2402.13550](https://arxiv.org/abs/2402.13550)
- Pluralistic alignment (Sorensen et al., ICML 2024, arXiv 2402.05070) defines **Overton-pluralistic** outputs that present the spectrum of reasonable answers instead of forcing one. This framework fits "preserve disagreement" outcomes (not re-verified this session) — [arXiv 2402.05070](https://arxiv.org/abs/2402.05070)

### Inferences
- **Habermas-style proposal selection for MAGI (about 2-3 hours to build):**
  1. Each agent drafts a proposal, or MAGI generates k=3-6 candidates.
  2. **Each agent ranks all live proposals** with a short reason.
  3. Aggregate with **Schulze** (about 30 lines of code), or Borda as a fallback, to pick the proposal that goes to the immutable-version **unanimity** vote.
  4. On a NO vote, the agent must write a **critique**. The next version must address the critiques, and versions stay immutable and diffable.

  This is a decentralized mechanism with a cited pedigree. Note that it is still a mechanism and not a "central decider", which is exactly what Level 3 asks for.
- **Pareto filter.** Each agent scores every proposal on its own axis (MELCHIOR: evidential soundness; BALTHASAR: risk/safety; CASPER: feasibility/cost). Remove Pareto-dominated proposals before ranking. Show the 3-axis Pareto plot in the UI as a concrete visualization of "real negotiation".
- **Make "no consensus" a first-class output.** When unanimity fails after the round cap, emit an Overton-style "minority report":
  - each agent's position and confidence
  - the **crux** (the specific claim that, if resolved, would flip the decision)
  - what evidence would resolve it

  Then escalate to the human. This is better grounded than forcing a compromise.
- Negotiation benchmarks show agents are manipulable by emotional framing (NegotiationArena). A demo where one agent uses "desperation" or "authority" framing, and MAGI's flip-justification check flags it, is a direct, citable robustness test.

### Gaps
- No full text of the 2026 "Social Choice with Text" survey was obtained.
- I found no LLM study comparing Schulze, Borda and approval specifically for **agent-internal** proposal selection with ground truth.
- Deliberative-polling-with-LLM-moderator studies (e.g., Stanford Deliberative Democracy Lab) were not researched in this pass.

---

## Q4. How to evaluate "collective intelligence": metrics and usable ground-truth benchmarks

### Takeaway
Credible evaluation in 2025-2026 goes well beyond final accuracy. It includes:
- **compute-matched baselines**
- **flip analysis** (correct→wrong vs wrong→correct)
- **oracle gap** (the right answer was present but lost)
- decomposition of belief change into **evidence vs social pressure**, using counterfactual controls
- **identity bias**
- **robustness to misinformation and adversarial peers**
- **selective accuracy and abstention** metrics

Several datasets with ground truth are small enough for a hackathon: ClashEval, HiddenBench, AbstentionBench, GPQA-Diamond and MMLU-Pro subsets, and GlobalOpinionQA for no-ground-truth opinion dynamics.

### Cited Findings
**Metrics with precedent**
- **Harmful-revision rate and end-of-debate flip rate.** The conditional revision rate can hide damage that the end-of-debate flip rate shows — [Nilayam et al., arXiv 2606.19826](https://arxiv.org/abs/2606.19826)
- **Three-source flip decomposition**, using these controls:
  - a self-reflection-only control, which measures spontaneous instability
  - a stance-only exposure, which measures conformity
  - a vacuous vs reasoning-like rationale, which measures persuasion by form

  Harmful conformity is predictable from Round 0 (AUC 0.79) — [Hao et al., arXiv 2606.00820](https://arxiv.org/abs/2606.00820)
- **Oracle gap**: plurality discarding correct answers already in the pool, up to 32.3 pp. **Token cost ratio** versus self-correction: 2.1-3.4× — [Bertalanič & Fortuna, arXiv 2605.00914](https://arxiv.org/abs/2605.00914)
- **Identity Bias Coefficient**, plus Conformity and Obstinacy under disagreement — [Choi et al., arXiv 2510.07517](https://arxiv.org/abs/2510.07517)
- **Stated vs revealed position change**: self-reported agreement versus selected-option change. Selected options stay the same in over 90% of cases even when agents "disagree" — [Qian, arXiv 2609.08016](https://arxiv.org/abs/2609.08016)
- **Martingale check**: plot mean agent accuracy per round. A flat line means debate is adding nothing beyond voting — [Choi et al., arXiv 2508.17536](https://arxiv.org/html/2508.17536v2)
- **Yield under pressure**: correct→incorrect under simulated disagreement, and the effect of one dissenter — [Kumarappan & Mujoo, arXiv 2605.12991](https://arxiv.org/abs/2605.12991)
- **Adversary metrics**: system accuracy and agreement under an adversarial agent — [Amayuelas et al., arXiv 2406.14711](https://arxiv.org/abs/2406.14711)
- **Abstain accuracy**: multi-LLM COOPERATE/COMPETE probing raised abstain accuracy **by up to 19.3%** over the strongest baseline across 3 LLMs and 4 QA tasks — [Feng et al., ACL 2024, arXiv 2402.00367](https://arxiv.org/abs/2402.00367)
- **Adaptive stopping metric**: a stability test on the consensus distribution (Beta-Binomial + KS) instead of fixed rounds — [Hu et al., NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/42475c537936b2394b5015e871765056-Abstract-Conference.html)

**Ground-truth datasets suitable for a 24h build**
- **ClashEval** (Wu, Wu, Zou; NeurIPS 2024 D&B; arXiv 2404.10198). Over 1,200 questions in 6 domains (drug dosages, Olympic records, locations, …). Retrieved documents are perturbed from subtle to blatant.
  - LLMs **adopt incorrect retrieved content over 60% of the time**, overriding correct priors.
  - Less plausible errors are adopted less often.
  - Lower initial confidence (token probabilities) predicts adoption.
  - This is the ideal dataset for MAGI's "inject evidence / challenge credibility" feature — [arXiv 2404.10198](https://arxiv.org/abs/2404.10198)
- **HiddenBench / "Systematic Failures in Collective Reasoning under Distributed Information in Multi-Agent LLMs"** (Li, Naito, Shirado; ICML 2026; arXiv 2505.11556). Built on the Hidden Profile paradigm, with 65 tasks and 15 models.
  - Multi-agent groups with distributed information reach **30.1%** accuracy, versus **80.7%** for a single agent with full information.
  - The gap persists across prompting strategies, depths and group sizes, and **worsens with scale**.
  - The failure comes from not reasoning about what others might know, which causes premature convergence on shared evidence.
  - The dataset is on Hugging Face — [arXiv](https://arxiv.org/abs/2505.11556v2); [ICML 2026](https://icml.cc/virtual/2026/poster/62206); [dataset](https://huggingface.co/datasets/YuxuanLi1225/HiddenBench)
- **AbstentionBench** (Kirichenko, Ibrahim, Chaudhuri, Bell, FAIR at Meta; NeurIPS 2025; arXiv 2506.09038). 20 datasets covering unknown answers, underspecification, false premises, subjective questions and outdated info.
  - Abstention is unsolved, and scale barely helps.
  - **Reasoning fine-tuning degrades abstention by 24% on average.**
  - System prompts help only partially.
  - Code is at facebookresearch/AbstentionBench — [arXiv 2506.09038](https://arxiv.org/abs/2506.09038)
- Misinformation in benign multi-agent systems (Becker, Wahle, Ruas, Gipp; arXiv 2606.16710; 2026 preprint). Intent-based misinformation injected into a subset of agents persists through debate, though debate reduces degradation versus a single agent. Consensus is more stable than voting, and majorities often steer misinformed agents back — [arXiv 2606.16710](https://arxiv.org/abs/2606.16710)
- Reasoning sets used in the debate literature:
  - GSM8K, MMLU subsets, CommonsenseQA, HellaSwag ([Choi et al.](https://arxiv.org/html/2508.17536v2))
  - MMLU-Pro and GPQA-Diamond ([Hao et al.](https://arxiv.org/abs/2606.00820))
  - GSM-Hard and MMLU-Hard ([Bertalanič & Fortuna](https://arxiv.org/abs/2605.00914))
  - Knight-Knave-Spy puzzles with verifiable steps ([Wu et al.](https://arxiv.org/abs/2511.07784))
- No-ground-truth opinion dynamics: GlobalOpinionQA, 50 questions in Qian 2026 — [arXiv 2609.08016](https://arxiv.org/abs/2609.08016)

### Inferences
**Minimal, defensible MAGI evaluation (fits in about 4-6 hours of compute and analysis, roughly 100-150 items total)**
1. **Accuracy vs cost**: 40-60 items from GPQA-Diamond or MMLU-Pro. Compare MAGI with B1-B4 (see Q1) and report tokens, $ and latency per item. Use bootstrap 95% CIs, since at this n a 3-5 pt difference is noise.
2. **Evidence effect (MAGI's headline)**: 30 ClashEval items, in three variants: (a) correct evidence, (b) subtly wrong evidence, (c) blatantly wrong evidence. Measure:
   - **acceptance of true evidence** (sensitivity)
   - **rejection of false evidence** (specificity)

   Compare single LLM vs MAGI. A win here is directly citable against "over 60% adoption".
3. **Social-pressure vs evidence decomposition**: for each flip, use the self-reflection control plus the cause tags. Report the % of flips that are evidence-driven vs peer-only, and the correct→wrong rate.
4. **Abstention and escalation**: 20 AbstentionBench items (false-premise/underspecified) plus 20 answerable items. Report abstention precision and recall, plus a **risk-coverage curve**: accuracy on committed answers vs % escalated. Compare against a single LLM thresholded on verbalized confidence at the same coverage.
5. **Manipulation resistance**: replace one agent with a saboteur (MAD-Spear style: confident, plausible, wrong). Measure the accuracy drop and harmful-revision rate with and without anonymization and flip-justification.
6. **Distributed information**: 10-15 HiddenBench tasks with information sharded across MELCHIOR, BALTHASAR and CASPER. Compare vanilla debate with a "disclose what others likely don't know" protocol, using single agent + full info as the ceiling.

### Gaps
- No standard metric exists for "quality of preserved disagreement" (e.g., crux identification accuracy). MAGI would have to define one.
- ClashEval and HiddenBench have not, to my knowledge, been run through a *debate* system with an explicit credibility-challenge step. That is an opportunity, but it also means no published comparison point.
- The exact HiddenBench task format and prompt templates were not inspected. Check the HF dataset card before building on it.

---

## Q5. What is genuinely under-explored that a hackathon demo could show convincingly (plus consolidated MAGI recommendations)

### Takeaway
Accuracy-via-debate is crowded and mostly negative for homogeneous agents. The open, demo-able space is:
1. **Evidence-vs-pressure attribution**: showing *why* each agent changed its mind, and that MAGI changes for evidence but not for pressure.
2. **Credibility-challenged evidence injection**: true vs perturbed evidence mid-debate.
3. **Private and distributed information**: hidden-profile tasks, where LLM groups fail badly.
4. **Calibrated "don't converge"**: INSUFFICIENT_INFORMATION and human escalation, evaluated as selective prediction.
5. **Manipulation resistance** against a planted persuasive agent.

Each has 2025-2026 papers documenting the *problem* but few working *systems* that combine detection, mechanism and evaluation in one loop.

### Cited Findings
- Even the best 2026 conformity intervention could not improve accuracy without labels, because it cannot tell harmful from beneficial influence. This is a stated open problem that a mechanism tying flips to explicit, checkable evidence could address — [Hao et al., arXiv 2606.00820](https://arxiv.org/abs/2606.00820)
- The strongest prompt-level sycophancy defense fails on attack variants outside its design. The authors call for **structured dissent at the pipeline level** — [Kumarappan & Mujoo, arXiv 2605.12991](https://arxiv.org/abs/2605.12991)
- Multi-agent LLMs with distributed information perform far below a single agent with full information (30.1% vs 80.7%). The cause is failing to reason about what others know but haven't said — [HiddenBench / ICML 2026](https://arxiv.org/abs/2505.11556v2)
- Misinformation persists in benign multi-agent debate when only some agents are exposed — [Becker et al., arXiv 2606.16710](https://arxiv.org/abs/2606.16710). LLMs adopt wrong retrieved evidence over 60% of the time — [ClashEval](https://arxiv.org/abs/2404.10198)
- Abstention is unsolved, and reasoning training makes it worse (−24%) — [AbstentionBench](https://arxiv.org/abs/2506.09038). Multi-LLM collaboration improves abstention (up to +19.3%) — [Feng et al. ACL 2024](https://arxiv.org/abs/2402.00367)
- An adaptive stopping rule already beats fixed-round debate for judges — [Hu et al. NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/42475c537936b2394b5015e871765056-Abstract-Conference.html). The MACI controller (arXiv 2510.04488) uses a cross-family judge as a stop signal and recommends **periodic human audits** — [arXiv 2510.04488](https://arxiv.org/pdf/2510.04488v1)
- The field has converged on default designs (fully connected, verbatim exchange, voting) without comparison, and calls for cost-aware benchmarking — [Motger et al., arXiv 2607.26212](https://arxiv.org/abs/2607.26212)
- Heterogeneity is both an attack surface and a defense — [Nilayam et al., arXiv 2606.19826](https://arxiv.org/abs/2606.19826)
- Human-AI deliberation precedent: the Habermas Machine. Iterative critique plus a clone-independent social choice rule beat human mediators and kept minority views — [Science 2024](https://doi.org/10.1126/science.adq2852)

### Inferences

#### Positioning sentence for judges
"MAGI is not another 'debate improves accuracy' system. The 2025-26 literature shows that homogeneous debate is a martingale. MAGI is a **deliberation protocol whose outputs are auditable**:
- every change of mind is attributed to evidence or to pressure
- injected evidence is credibility-tested
- consensus requires unanimity over immutable proposals chosen by a clone-independent vote
- when consensus would be unjustified, MAGI abstains or escalates with an explicit crux."

#### Prioritized build list for 24 hours (P0 = must, P1 = strong, P2 = if time)
- **P0: Baselines.** B1 single CoT, B2 token-matched self-consistency vote, B3 MAGI round-0 + vote (no debate). Cite Choi et al. 2025 and Zhang et al. 2025.
- **P0: Anonymized cross-reading.** Peers appear as "Analysis A/B (perspective: safety)" without self/peer identity. Cite Choi et al. ACL 2026.
- **P0: Structured agent output (JSON).**
  - `position`, `confidence` (0-100), `key_claims[]`, `evidence_used[]`
  - `what_would_change_my_mind`
  - on revision: `change_cause` ∈ {NEW_EVIDENCE, NEW_ARGUMENT, OWN_ERROR, PEER_AGREEMENT_ONLY} plus a quote

  This enables the flip analysis and a "conformity flag" in the UI.
- **P0: Evidence injection with credibility check.** Injected evidence is first assessed by each agent: source, plausibility versus priors, internal consistency, and a credibility score. Each agent then states whether it updates. Evaluate on ClashEval true / subtle-false / blatant-false variants.
- **P0: Stop and escalate rules.**
  - Stop early if a round has no position changes and no new `key_claims`.
  - After a max of 3 rounds, if not unanimous: output a minority report plus the crux and ESCALATE.
  - Output INSUFFICIENT_INFORMATION if ≥2 agents give confidence below a threshold **and** list missing information. Do this rather than letting them converge.
- **P1: Designated dissent.** Before each vote, one agent (rotating, or BALTHASAR) must steelman the strongest objection. Cite Kumarappan & Mujoo 2026 and Estornell & Liu NeurIPS 2024 (misconception-refutation; UCSC co-author).
- **P1: Habermas-style proposal selection.** Agents rank all proposal versions, the winner is chosen by Schulze (Borda as fallback), and an optional Pareto filter on the 3 persona axes runs first. A NO vote requires a critique that the next immutable version must address.
- **P1: Confidence-modulated updates.** Show peers' confidences, instruct agents to weigh by confidence *and* argument quality, and use a confidence-weighted tally for factual questions. Cite ReConcile and Zhu et al. 2026.
- **P1: Self-reflection control.** One extra call per agent re-asks with only its own prior answer. Debate flips minus self-flips gives the "social influence" metric.
- **P1: Saboteur mode.** A toggle swaps one agent's prompt for a confident-wrong persuader (MAD-Spear style). The demo shows MAGI flagging peer-only flips and holding. Report harmful-revision rate on and off.
- **P2: Heterogeneous model option.** Run CASPER on a different provider or open-weights model. This is the most robust accuracy lever per Zhang et al. 2025, Hegazy 2024 and Nilayam et al. 2026. If allowed, show same-model vs mixed-model in the eval table.
- **P2: Private information mode.** Shard evidence across agents on 10 HiddenBench tasks. Add a "disclose facts others likely lack" step and compare against vanilla sharing.
- **P2: Trajectory-aware decision (Free-MAD).** Score answers across all rounds rather than only the last. Revert unexplained abandonment of high-confidence round-0 answers.

#### Demo narrative (about 3 minutes)
1. Show a question where a single LLM is confidently wrong.
2. Show MAGI agents disagreeing for real, with heterogeneous reasoning.
3. Inject **false** evidence: MAGI agents challenge it, while the single LLM adopts it (ClashEval-style).
4. Inject **true** evidence: the agents update, and the UI shows "NEW_EVIDENCE" flip tags.
5. Saboteur toggle: the planted agent pushes, MAGI flags "PEER_AGREEMENT_ONLY" flips, and the vote holds.
6. Show an unanswerable or underspecified question: MAGI returns INSUFFICIENT_INFORMATION with the missing facts listed.
7. End on one table with a risk-coverage chart: MAGI vs B1/B2/B3 on accuracy, true-evidence acceptance, false-evidence rejection, harmful-flip rate, abstention precision, and tokens/latency.

#### Honest framing
- Say up front that, on pure accuracy with one model, MAGI may tie majority vote. This is the expected outcome per Choi et al., and saying so signals literature fluency.
- Claim wins only on the dimensions measured.
- Report CIs.

### Gaps
- No published system found that combines flip-cause attribution, credibility-tested evidence injection and selective escalation. That makes the opportunity look genuine, but my search was not exhaustive for October 2026 preprints.
- The best abstention or confidence threshold for MAGI's INSUFFICIENT_INFORMATION is task-dependent, and no source gives a transferable value. Tune it on a small held-out set.
- Whether hackathon judges (Cisco Cloud track) weight accuracy over process transparency is unknown. The Level 3 criteria as described favor process: disagreement, mechanism, new information, baseline, and stopping/escalation.
