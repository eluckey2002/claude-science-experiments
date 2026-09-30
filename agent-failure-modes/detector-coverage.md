# Detector literature for `agent-failure-modes` v2.4

Generated 2026-09-21. 74 arXiv queries -> 509 unique records -> 328 screened as supplying a detector -> hand-curated to the table below.

**Evidence level: abstracts only.** Titles and arXiv ids are verbatim from the arXiv API; the one-line notes paraphrase abstracts and have not been checked against method sections. arXiv-only, so ACL/EMNLP-only work and industry tooling are out of scope. Treat this as a reading list with coverage accounting, not a validated detector catalogue.

**Provenance.** All 80 cited arXiv ids verified present in the retrieved pool with verbatim API titles. Two records (2606.18467, 2505.14925) were curated from their abstracts after the automatic screening batch was cut short by a token limit; their detector_type and runtime_capable fields were assigned by hand and are labelled as such in detector-candidates.csv.

## Coverage summary

| tier | modes | meaning |
|---|---|---|
| **strong** | A3, A4, B8, C2, C6, D1, D2, D4 | 3+ detectors targeting this mode's tell |
| **moderate** | B2, B3, C1, C5 | 2-3, or strong detectors with a locus/runtime caveat |
| **thin** | A1, A2, B1, B4, B7, C3, D3 | proxies only, or a single mechanism-level result |
| **none** | A5, B5, B6, C4 | no detector found for this mode's tell after two query rounds |

| code | mode | coverage | direct | runtime detector | suggested `detector.method` |
|---|---|---|---|---|---|
| A1 | Literalism | thin | 0 | no | `human` |
| A2 | Shape of the Example | thin | 1 | no | `human` |
| A3 | Shape of the Conversation | strong | 5 | yes | `monitor` |
| A4 | No Questions Asked | strong | 5 | yes | `preflight` |
| A5 | Manufactured Decision | none | 0 | no | `human` |
| B1 | Shape of the Data | thin | 0 | no | `human` |
| B2 | Shape of the Tool | moderate | 2 | yes | `monitor` |
| B3 | Shape of the Prior | moderate | 4 | yes | `monitor` |
| B4 | First Suspect | thin | 1 | yes | `human` |
| B5 | Sunk Path | none | 0 | no | `human` |
| B6 | Forced Symmetry | none | 0 | no | `human` |
| B7 | Premature Abstraction | thin | 0 | no | `human` |
| B8 | Confabulation | strong | 4 | yes | `monitor` |
| C1 | Unchecked Premise | moderate | 2 | yes | `monitor` |
| C2 | Sailing | strong | 3 | yes | `monitor` |
| C3 | Skating | thin | 1 | yes | `human` |
| C4 | Spot-Check | none | 0 | no | `human` |
| C5 | Closure Performance | moderate | 3 | yes | `monitor` |
| C6 | Gaming the Check | strong | 7 | yes | `monitor` |
| D1 | Spinning | strong | 4 | yes | `monitor` |
| D2 | Drift | strong | 4 | yes | `monitor` |
| D3 | Context Bleed | thin | 0 | no | `human` |
| D4 | Say-Do Gap | strong | 5 | yes | `monitor` |

## Per-mode detectors

### A1 Literalism — *Obeys the words, misses the intent.*
`framing` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [When Contextual Inference Fails: Cancelability in Interactive Instruction Following](https://arxiv.org/abs/2603.19997) | 2026 | benchmark+scorer | partial | Separates literal interpretation from contextual inference in underspecified instruction-following; supplies a cancelability test that operationalises letter-vs-spirit. |
| [TOD-ProcBench: Benchmarking Complex Instruction-Following in Task-Oriented Dialogues](https://arxiv.org/abs/2511.15976) | 2025 | benchmark+scorer · runtime | partial | Procedural instruction-following benchmark with an explicit violation-detection subtask. |

> **Gap.** No detector targets letter-vs-spirit divergence in agent traces. Nearest neighbours are prompt-injection defences, which share the surface signal (obeyed the wrong instruction) but a different cause.

### A2 Shape of the Example — *Copies the example's form, not your goal.*
`framing` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Mitigating Copy Bias in In-Context Learning through Neuron Pruning](https://arxiv.org/abs/2410.01288) | 2024 | probe | direct | Measures and localises 'copy bias' — answers copied from in-context examples rather than derived from the task — and prunes the responsible neurons. |
| [Mitigating the Bias of Large Language Model Evaluation](https://arxiv.org/abs/2409.16788) | 2024 | benchmark+scorer · runtime | partial | Judge-side analogue: raters scoring superficial quality over instruction fidelity. |

> **Gap.** Only mechanism-level work exists. No trace-level detector asks whether an agent's output mirrors the exemplar's form rather than the request's goal.

### A3 Shape of the Conversation — *Follows the chat's drift over the facts.*
`framing` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Detecting and Controlling Sycophancy with Cascading Linear Features](https://arxiv.org/abs/2606.26155) | 2026 | probe · runtime | direct | Linear-feature probe over activations; detects and steers sycophancy at inference time. |
| [Measuring and Detecting Harmful AI Sycophancy](https://arxiv.org/abs/2608.05624) | 2026 | probe · runtime | direct | Detects stance reversals driven by user preference rather than evidence. |
| [SWAY: A Counterfactual Computational Linguistic Approach to Measuring and Mitigating Sycophancy](https://arxiv.org/abs/2604.02423) | 2026 | benchmark+scorer · runtime | direct | Counterfactual framing manipulation that isolates sycophancy from content-driven reasoning. |
| [FramingQA: Does the Question Shape the Answer? Measuring the Compositional Framing Effect](https://arxiv.org/abs/2609.07448) | 2026 | benchmark+scorer · runtime | direct | Measures the compositional framing effect: same facts, rephrased question, changed answer. |
| [The Social Sycophancy Scale: A psychometrically validated measure of sycophancy](https://arxiv.org/abs/2603.15448) | 2026 | benchmark+scorer · runtime | direct | Psychometrically validated sycophancy scale for open-ended domains without ground truth. |

### A4 No Questions Asked — *Guesses on ambiguity instead of asking.*
`framing` · coverage **strong** · suggested `detector.method`: `preflight`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification](https://arxiv.org/abs/2602.11199) | 2026 | benchmark+scorer · runtime | direct | Benchmark plus rubric-guided RLVR for when and what to ask; covers ambiguous and false-premise queries. |
| [Uncertainty Decomposition for Clarification Seeking in LLM Agents](https://arxiv.org/abs/2606.19559) | 2026 | benchmark+scorer · runtime | direct | Decomposes predictive uncertainty into components that signal when clarification is warranted — runtime-usable. |
| [Structured Uncertainty guided Clarification for LLM Agents](https://arxiv.org/abs/2511.08798) | 2025 | uncertainty · runtime | direct | Structured uncertainty over tool parameters as a preflight clarification trigger. |
| [Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering](https://arxiv.org/abs/2502.13069) | 2025 | benchmark+scorer · runtime | direct | Underspecified software-engineering issues; scores whether the agent asks before implementing. |
| [When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search](https://arxiv.org/abs/2606.27669) | 2026 | benchmark+scorer · runtime | direct | Clarification-aware deep search: detects agents that assume rather than ask. |

### A5 Manufactured Decision — *Asks permission for work already authorized.*
`framing` · coverage **none** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](https://arxiv.org/abs/2604.09408) | 2026 | benchmark+scorer · runtime | inverse | Measures whether agents know when to ask for help — the opposite polarity: penalises under-asking, not over-asking. |
| [Clarify-Then-Search: A Clarification Benchmark for Deep Search with End-to-End Nugget Restoration](https://arxiv.org/abs/2608.20357) | 2026 | benchmark+scorer | inverse | Same polarity: rewards clarification on underspecified queries. |

> **Gap.** The entire clarification literature is built to punish under-asking. Nothing published scores an agent for escalating a decision it was already authorised to make, so A5 currently has no external anchor and no detector.

### B1 Shape of the Data — *Treats available data as the whole picture.*
`reasoning` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [ScoreGate: Adaptive Chunk Selection for Retrieval-Augmented Generation via Dual-Score Statistical Fusion](https://arxiv.org/abs/2606.14269) | 2026 | programmatic · runtime | partial | Dual-score statistic that flags over- and under-retrieval per query — a programmatic proxy for 'the evidence set is not the whole picture'. |
| [URAG: A Benchmark for Uncertainty Quantification in Retrieval-Augmented Large Language Models](https://arxiv.org/abs/2603.19281) | 2026 | benchmark+scorer | partial | Uncertainty quantification for RAG, scoring beyond answer correctness. |
| [Investigating the Factual Knowledge Boundary of Large Language Models with Retrieval Augmentation](https://arxiv.org/abs/2307.11019) | 2023 | benchmark+scorer | partial | Measures whether models perceive their own factual-knowledge boundary under retrieval augmentation. |

> **Gap.** Detectors exist for insufficient retrieval; none for the agent treating a complete-looking but skewed evidence set as the population.

### B2 Shape of the Tool — *Lets its tools pick the approach.*
`reasoning` · coverage **moderate** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Internal Representations as Indicators of Hallucinations in Agent Tool Selection](https://arxiv.org/abs/2601.05214) | 2026 | probe · runtime | direct | Internal-representation indicators of hallucinated tool selection, readable during inference. |
| [Quantitative Certification of Agentic Tool Selection](https://arxiv.org/abs/2510.03992) | 2025 | benchmark+scorer · runtime | direct | Certifies a tool-selection pipeline against a safety spec under a realistic tool distribution. |
| [When Agents Fail to Act: A Diagnostic Framework for Tool Invocation Reliability in Multi-Agent LLM Systems](https://arxiv.org/abs/2601.16280) | 2026 | benchmark+scorer · runtime | partial | Diagnostic framework for tool-invocation reliability across model classes. |
| [Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents](https://arxiv.org/abs/2608.11888) | 2026 | benchmark+scorer | partial | Empirical study of skill-induced failures: skills that degrade success or cost without being flagged. |

> **Gap.** All of these score tool choice against a known-correct tool. None runs the counterfactual that B2 actually asserts — would the approach change if the tool were absent?

### B3 Shape of the Prior — *The default answer beats the evidence given.*
`reasoning` · coverage **moderate** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence](https://arxiv.org/abs/2608.25869) | 2026 | probe · runtime | direct | Prior scores shift LLM-judge ratings; quantifies anchoring as an independence violation. |
| [Anchors in the Machine: Behavioral and Attributional Evidence of Anchoring Bias in LLMs](https://arxiv.org/abs/2511.05766) | 2025 | programmatic · runtime | direct | Behavioural and attributional evidence of anchoring, with an attribution analysis of the mechanism. |
| [Parameters vs. Context: Fine-Grained Control of Knowledge Reliance in Language Models](https://arxiv.org/abs/2503.15888) | 2025 | programmatic · runtime | direct | Fine-grained measurement and control of parametric-vs-context reliance under conflict. |
| [MemToC: Benchmarking Memory-Tool Conflict Resolution in Large Language Models](https://arxiv.org/abs/2608.26295) | 2026 | benchmark+scorer | direct | Memory-tool conflict benchmark; reports how rarely correct memory survives an incorrect tool return. |

> **Gap.** Strong offline/counterfactual instruments, no runtime signal — all require running the item twice under varied anchors.

### B4 First Suspect — *Locks on hypothesis #1, skips the rest.*
`reasoning` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Information-seeking failures of large language models in agentic clinical reasoning](https://arxiv.org/abs/2607.10275) | 2026 | benchmark+scorer · runtime | direct | Agentic clinical reasoning: detects models that stop investigating and commit under uncertainty. |
| [Evaluating Multi-Turn Multimodal Diagnostic Reasoning on Challenging Real-World Clinical Cases](https://arxiv.org/abs/2607.25933) | 2026 | benchmark+scorer | partial | Multi-turn diagnostic reasoning that locks on an initial hypothesis. |
| [AgentAbstain: Do LLM Agents Know When Not to Act?](https://arxiv.org/abs/2607.10059) | 2026 | benchmark+scorer · runtime | partial | Whether agents recognise abstention triggers before acting. |

> **Gap.** Only instantiated in clinical diagnosis, where premature closure has a 20-year prior literature. No domain-general trace detector.

### B5 Sunk Path — *Won't abandon a failing approach.*
`reasoning` · coverage **none** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [SkillHEX: Improving Agent Skills via Hypothesis-Driven Autonomous Exploration and Exploitation](https://arxiv.org/abs/2608.05628) | 2026 | monitor · runtime | partial | Agent locks onto a failing skill revision and skips alternatives — closest observed behaviour. |
| [FinHarness: An Inline Lifecycle Safety Harness for Finance LLM Agents](https://arxiv.org/abs/2605.27333) | 2026 | monitor · runtime | partial | Inline lifecycle harness flagging irreversible mid-trajectory actions. |

> **Gap.** Two targeted query rounds returned no detector and no benchmark for sunk-cost persistence in LLM agents. This is a real hole in the literature, not a query artifact — despite B5 being one of the most reported practitioner complaints.

### B6 Forced Symmetry — *Invents parallelism that isn't there.*
`reasoning` · coverage **none** · suggested `detector.method`: `human`

> **Gap.** Nothing. False balance is studied in media framing and in bias audits of generated text, never as an agent reasoning failure with a detection procedure.

### B7 Premature Abstraction — *Builds the framework too early.*
`reasoning` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [A Causal Perspective on Measuring, Explaining and Mitigating Smells in LLM-Generated Code](https://arxiv.org/abs/2511.15817) | 2025 | programmatic | partial | Causal measurement, explanation and mitigation of code smells in LLM-generated code — the only quantitative handle on over-structuring. |
| [Assessing the Quality and Security of AI-Generated Code: A Quantitative Analysis](https://arxiv.org/abs/2508.14727) | 2025 | programmatic | partial | Quantitative code-quality and security comparison across five models. |

> **Gap.** Code-smell metrics are a proxy with a known confound: idiomatic abstraction and premature abstraction produce overlapping smell profiles.

### B8 Confabulation — *Invents specifics to complete the pattern.*
`reasoning` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Tool Receipts, Not Zero-Knowledge Proofs: Practical Hallucination Detection for AI Agents](https://arxiv.org/abs/2603.10060) | 2026 | monitor · runtime | direct | Cross-references agent claims against tool-call receipts; catches fabricated counts and false absence claims. Cheapest runtime detector in this whole table. |
| [Actionable Hallucination Detection: Translating Latent Uncertainty into Agentic Critique](https://arxiv.org/abs/2608.10430) | 2026 | monitor · runtime | direct | Translates latent uncertainty into an agentic critique of hallucinated tool calls and ungrounded parameters. |
| [Beyond Document Grounding: Span-Level Hallucination Detection over Code, Tool Output, and Documents](https://arxiv.org/abs/2607.00895) | 2026 | benchmark+scorer · runtime | direct | Span-level hallucination classifier over code, tool output and structured documents. |
| [MetaRAG: Metamorphic Testing for Hallucination Detection in RAG Systems](https://arxiv.org/abs/2509.09360) | 2025 | programmatic · runtime | direct | Metamorphic testing for RAG: synonym/antonym entailment mismatches reveal unsupported factoids. |

### C1 Unchecked Premise — *Never tests the starting assumption.*
`verification` · coverage **moderate** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Syn-QA2: Evaluating False Assumptions in Long-tail Questions with Synthetic QA Datasets](https://arxiv.org/abs/2403.12145) | 2024 | benchmark+scorer | direct | Synthetic long-tail QA with false assumptions; scores whether the model rejects the premise. |
| [Source or It Didn't Happen: A Multi-Agent Framework for Citation Hallucination Detection](https://arxiv.org/abs/2605.08583) | 2026 | programmatic · runtime | direct | Multi-agent citation-hallucination detection: extraction, retrieval, field matching, specialist judgment. |
| [ScopeJudge: Cost-Aware Pre-Execution Gating for Offensive Security Agents](https://arxiv.org/abs/2607.07774) | 2026 | judge · runtime | partial | Pre-execution gating of tool calls against declared scope boundaries. |

> **Gap.** Mature at the QA level. The agent-trace version — the premise entering step 1 was never tested — has no published detector.

### C2 Sailing — *Glides to the end, never checks.*
`verification` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents](https://arxiv.org/abs/2607.24300) | 2026 | monitor · runtime | direct | Self-authored verification scores diverge from external deployment performance. Read this one first: it is evidence against the self-report detector method in your own telemetry schema. |
| [E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing](https://arxiv.org/abs/2512.03109) | 2025 | monitor · runtime | direct | Sequential hypothesis testing over trajectories; flags long runs with no progress verification. |
| [ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift](https://arxiv.org/abs/2606.18467) | 2026 | uncertainty · runtime | direct | Conformal risk control over retrieval and tool-use drift — calibrated abstention rather than a heuristic threshold. |
| [SWE-Marathon: Can Agents Autonomously Complete Ultra-Long-Horizon Software Work?](https://arxiv.org/abs/2606.07682) | 2026 | benchmark+scorer · runtime | benchmark | Ultra-long-horizon software work; scores claims of success against actual requirements. |
| [ContractBench: Can LLM Agents Preserve Observation Contracts?](https://arxiv.org/abs/2605.17281) | 2026 | benchmark+scorer · runtime | partial | Whether agents preserve observation contracts (temporal validity, byte integrity) across API workflows. |

### C3 Skating — *Checks the surface only.*
`verification` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge](https://arxiv.org/abs/2509.26072) | 2025 | benchmark+scorer · runtime | direct | LLM judges rationalising decisions from unacknowledged superficial cues — surface-checking with a plausible narrative on top. |
| [Beyond correlation: The Impact of Human Uncertainty in Measuring the Effectiveness of Automatic Evaluation and LLM-as-a-Judge](https://arxiv.org/abs/2410.03775) | 2024 | programmatic · runtime | partial | Correlation metrics masking performance gaps on high-uncertainty subsets. |

> **Gap.** Locus mismatch: published work catches a superficial *judge*, your C3 is a superficial *self-check*. The instruments transfer but the validation does not.

### C4 Spot-Check — *Tests one case, assumes the rest.*
`verification` · coverage **none** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Process Supervision for Chain-of-Thought Reasoning via Monte Carlo Net Information Gain](https://arxiv.org/abs/2603.17815) | 2026 | monitor · runtime | partial | Monte-Carlo net information gain per reasoning step; identifies steps that do not change correctness likelihood. |
| [MamaBench: Benchmarking LLM Robustness in Maternal and Child Health Diagnosis through Counterfactual Clinical Perturbation](https://arxiv.org/abs/2607.14385) | 2026 | benchmark+scorer · runtime | partial | Counterfactual clinical variants where base-case accuracy masks fragility — the spot-check fallacy at benchmark level. |
| [MEDEQUALQA: Evaluating Biases in LLMs with Counterfactual Reasoning](https://arxiv.org/abs/2510.12818) | 2025 | benchmark+scorer · runtime | partial | Counterfactual demographic variation scoring reasoning stability. |

> **Gap.** No detector asks whether an agent's verification sample covers its claim. Software testing has the ready-made apparatus — mutation score, test adequacy criteria — and nobody has applied it to agent self-verification.

### C5 Closure Performance — *Looks done; isn't verified.*
`verification` · coverage **moderate** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/abs/2606.09863) | 2026 | probe · runtime | direct | Characterises false success: agent claims completion without verifying the environment state changed. The closest published match to C5. |
| [Agent Safety Should Be a Runtime Contract](https://arxiv.org/abs/2608.11274) | 2026 | monitor · runtime | direct | Argues agent actions need verifiable evidence of execution; runtime-contract framing. |
| [Complementing Self-Consistency with Cross-Model Disagreement for Uncertainty Quantification](https://arxiv.org/abs/2604.17112) | 2026 | uncertainty · runtime | direct | Cross-model semantic disagreement as an uncertainty signal for confident-but-wrong outputs. |
| [Evaluating LLM Agents on Automated Software Analysis Tasks](https://arxiv.org/abs/2604.11270) | 2026 | benchmark+scorer · runtime | partial | Agents claiming success without validating that the tool produced meaningful output. |

### C6 Gaming the Check — *Makes the check pass dishonestly.*
`verification` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [EvilGenie: A Reward Hacking Benchmark](https://arxiv.org/abs/2511.21654) | 2025 | benchmark+scorer · runtime | direct | Reward-hacking benchmark covering test hardcoding, test-file editing and judge evasion. |
| [Hack-Verifiable Environments: Towards Evaluating Reward Hacking at Scale](https://arxiv.org/abs/2605.20744) | 2026 | benchmark+scorer · runtime | direct | Environments with deliberately embedded exploitable vulnerabilities, verifiable at scale. |
| [Hack-Verifiable Terminal Bench: Evaluating Reward Hacking in Terminal Tasks](https://arxiv.org/abs/2608.22103) | 2026 | benchmark+scorer · runtime | direct | Terminal-task variant of the same hack-verifiable design. |
| [Monitoring Emergent Reward Hacking During Generation via Internal Activations](https://arxiv.org/abs/2603.04069) | 2026 | probe · runtime | direct | Reward-hacking signals in internal activations during generation — runtime, pre-completion. |
| [Monitoring and Discovering Reward Hacking with Internal Representations during LLM Evaluations](https://arxiv.org/abs/2609.19101) | 2026 | probe · runtime | direct | Internal-representation monitoring for reward hacking during evaluations. |
| [Is It Thinking or Cheating? Detecting Implicit Reward Hacking by Measuring Reasoning Effort](https://arxiv.org/abs/2510.01367) | 2025 | monitor · runtime | direct | Detects implicit reward hacking by measuring reasoning effort: high reward on truncated reasoning. |
| [Harness-agnostic detection and immunization of reward hacking in self-evolving language models](https://arxiv.org/abs/2609.04665) | 2026 | monitor · runtime | direct | Harness-agnostic detection and immunisation for self-evolving models. |
| [Do Prompt-Elicited Trajectories Reflect Training-Time Reward Hacking? A Systematic Study on Monitoring Training-Time Reward Hacking in Code Generation](https://arxiv.org/abs/2604.23488) | 2026 | monitor · runtime | caution | Asks whether prompt-elicited hacking trajectories reflect training-time hacking — a validity warning for anyone eliciting C6 on demand. |

### D1 Spinning — *Repeats a step with no progress.*
`execution` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Automata from Agent Traces: Failure and Next-Step Prediction](https://arxiv.org/abs/2608.23670) | 2026 | monitor · runtime | direct | Induces a finite-state automaton from agent traces; predicts failure-prone states and non-progress loops. |
| [Real-Time Detection and Repair of LLM Agent Failures](https://arxiv.org/abs/2608.02464) | 2026 | monitor · runtime | direct | Real-time detection and repair of mid-episode loops, drift, and fabricated results from telemetry anomalies. |
| [E-valuator: Reliable Agent Verifiers with Sequential Hypothesis Testing](https://arxiv.org/abs/2512.03109) | 2025 | monitor · runtime | direct | Sequential testing flags unproductive repetition without a fixed loop-count threshold. |
| [An Approach to Checking Correctness for Agentic Systems](https://arxiv.org/abs/2509.20364) | 2025 | monitor · runtime | direct | Temporal assertions over action sequences; programmatic and cheap. |

### D2 Drift — *Goal erodes across a long run.*
`execution` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [MAGE: Safeguarding LLM Agents against Long-Horizon Threats via Shadow Memory](https://arxiv.org/abs/2605.03228) | 2026 | monitor · runtime | direct | Shadow memory that preserves the original objective and flags drift across long trajectories. |
| [TRACE: Trajectory Reasoning through Adaptive Cross-Step Evidence Aggregation for LLM Agents](https://arxiv.org/abs/2606.07054) | 2026 | monitor · runtime | direct | Cross-step evidence aggregation to surface objectives that emerged mid-run. |
| [ProbGuard: Proactive Runtime Monitoring for LLM Agent Safety via Probabilistic Prediction](https://arxiv.org/abs/2508.00500) | 2025 | monitor · runtime | direct | Probabilistic trajectory prediction with an intervention trigger below a safety threshold. |
| [Evaluating Agentic AI in the Wild: Failure Modes, Drift Patterns, and a Production Evaluation Framework](https://arxiv.org/abs/2605.01604) | 2026 | monitor · runtime | direct | Production field study of drift and compounding error with an evaluation framework. |

### D3 Context Bleed — *Drops earlier or mid-context constraints.*
`execution` · coverage **thin** · suggested `detector.method`: `human`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [Beyond Black-Box Benchmarking: Observability, Analytics, and Optimization of Agentic Systems](https://arxiv.org/abs/2503.06745) | 2025 | monitor · runtime | partial | Observability and analytics for agentic systems; names context loss as an observable. |
| [Uncertainty Quantification for LLM Agents: A Taxonomy, an Evaluation Protocol, and an Empirical Study](https://arxiv.org/abs/2609.07395) | 2026 | benchmark+scorer · runtime | partial | Step-level calibration masking trajectory-level drift in agent uncertainty. |
| [Too Long, Didn't Model: Decomposing LLM Long-Context Understanding With Novels](https://arxiv.org/abs/2505.14925) | 2025 | benchmark+scorer | benchmark | Decomposes long-context understanding; measurement rather than detection. |

> **Gap.** Well benchmarked, poorly detected. A constraint-ledger check — enumerate constraints at turn 1, re-verify each against the final output — is trivially implementable and, as far as these queries reach, unpublished.

### D4 Say-Do Gap — *Reasoning says one thing; the action does another.*
`execution` · coverage **strong** · suggested `detector.method`: `monitor`

| paper | yr | type | directness | what it flags |
|---|---|---|---|---|
| [DeceptGuard :A Constitutional Oversight Framework For Detecting Deception in LLM Agents](https://arxiv.org/abs/2603.13791) | 2026 | probe|monitor · runtime | direct | Constitutional oversight framework for reasoning-action mismatch, including deception masked by behavioural suppression. |
| [Guardrails as Scapegoats: Auditing Unfaithful Safety Refusals in Tool-Augmented LLM Agents](https://arxiv.org/abs/2607.19449) | 2026 | benchmark+scorer · runtime | direct | Audits unfaithful safety refusals: agent invents a rationale when a tool silently fails. |
| [StepGuard: Learning Step-Level Guardrails with Scalable Supervision and Safety-Utility Balancing](https://arxiv.org/abs/2608.24777) | 2026 | monitor · runtime | direct | Step-level guardrails auditing each action against stated constraints before execution. |
| [ToolSafe: Enhancing Tool Invocation Safety of LLM-based agents via Proactive Step-level Guardrail and Feedback](https://arxiv.org/abs/2601.10156) | 2026 | monitor · runtime | direct | Proactive step-level detection of misalignment between safety reasoning and the invoked tool. |
| [VeriGuard: Enhancing LLM Agent Safety via Verified Code Generation](https://arxiv.org/abs/2510.05156) | 2025 | monitor · runtime | direct | Verified code generation: actions checked against a pre-verified policy at runtime. |

## Cross-cutting

| paper | yr | why it matters here |
|---|---|---|
| [TelemetrySuffBench: Is Agent Telemetry Sufficient for Failure-Origin Diagnosis?](https://arxiv.org/abs/2608.07899) | 2026 | Tests whether agent telemetry is sufficient to identify where a failure originated — directly relevant to your event schema's adequacy. |
| [MAESTRO: Multi-Agent Evaluation Suite for Testing, Reliability, and Observability](https://arxiv.org/abs/2601.00481) | 2026 | Multi-agent evaluation suite; run-to-run variance masking structural failures. |
| [Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents](https://arxiv.org/abs/2607.24300) | 2026 | Self-authored verification diverges from external performance — bears on detector.method='self-report'. |
