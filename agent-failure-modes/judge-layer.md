# The LLM-judge layer in the detector survey

Slice of the same 509-record arXiv pool behind `detector-coverage`. 43 records mention LLM-as-judge; 24 were screened as judge-type detectors; 9 carry it in the title. Abstract-level evidence only.

## 1. Judge-as-detector

Overwhelmingly multi-agent verification and step-level error attribution rather than single-judge scoring.

| paper | yr | modes | what it flags |
|---|---|---|---|
| [Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning](https://arxiv.org/abs/2609.04194v1) | 2026 | C2, C3, B8 | LLM judges confabulating step importance from legible text without actual functional grounding |
| [A Tri-Agent Framework for Evaluating and Aligning Question Clarification Capabilities of Large Language Models](https://arxiv.org/abs/2609.02054v1) | 2026 | A4, C1, C3 | LLM fails to ask clarifying questions on ambiguous user input |
| [EDGE: Error Dependency Graph-Guided Multi-Error Attribution in Multi-Agent LLM Systems](https://arxiv.org/abs/2609.01360v1) | 2026 | D4, B4, C2 | Multi-error misattribution via LLM-judge without dependency validation |
| [ScopeJudge: Cost-Aware Pre-Execution Gating for Offensive Security Agents](https://arxiv.org/abs/2607.07774v2) | 2026 | C1, A4, B2 | Tool calls violating user-declared scope boundaries in offensive security tasks |
| [MedGuards: Multi-Agent System for Reliable Medical Error Detection and Correction](https://arxiv.org/abs/2606.25651v2) | 2026 | C2, C3, B8 | Medical errors in LLM text; multi-agent consensus + confidence scoring |
| [Zero-source LLM Hallucination Detection with Human-like Criteria Probing](https://arxiv.org/abs/2606.12900v1) | 2026 | B8, C2, C3 | Factually incorrect or unfaithful LLM outputs via criteria-based scoring |
| [ComplexConstraints and Beyond: Expert Rubrics for RLVR](https://arxiv.org/abs/2606.09118v3) | 2026 | C3, C2, B1 | Rubric-based evaluation surface pass/fail; misses semantic correctness gaps |
| [Capability Advertisement as a Market for Lemons: A Trust Layer for Heterogeneous Agent Networks](https://arxiv.org/abs/2606.03034v1) | 2026 | C5, B8, A1 | Agent capability claims unvalidated against actual performance; confident-wrong assertions |
| [Agentic CLEAR: Automating Multi-Level Evaluation of LLM Agents](https://arxiv.org/abs/2605.22608v1) | 2026 | C2, C3, D4 | Agent behavior misalignment via multi-level trace and action analysis |
| [OptArgus: A Multi-Agent System to Detect Hallucinations in LLM-based Optimization Modeling](https://arxiv.org/abs/2605.11738v1) | 2026 | C1, B8, C2 | Structural inconsistency between problem, model, solver despite matching objective value |
| [Rewarding the Scientific Process: Process-Level Reward Modeling for Agentic Data Analysis](https://arxiv.org/abs/2604.24198v2) | 2026 | C2, B8, D4 | Silent errors and logical flaws in agent execution without exception feedback |
| [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](https://arxiv.org/abs/2604.23581v1) | 2026 | C2, B1, D4 | Intermediate step failures masked by end-to-end checks; root cause misattribution via dependency tracking |
| [GSAR: Typed Grounding for Hallucination Detection and Recovery in Multi-Agent LLMs](https://arxiv.org/abs/2604.23366v1) | 2026 | C2, B1, B8 | Ungrounded or contradicted claims in multi-agent LLM outputs; missing evidence linkage |
| [MARCH: Multi-Agent Reinforced Self-Check for LLM Hallucination](https://arxiv.org/abs/2603.24579v1) | 2026 | B8, C1, C2 | Hallucinated claims in LLM outputs via multi-agent factual verification |
| [Constitutional Black-Box Monitoring for Scheming in LLM Agents](https://arxiv.org/abs/2603.00829v2) | 2026 | C2, C3, B1 | Scheming in LLM-agent trajectories via prompted classifier on I/O only |
| [Tool-MAD: A Multi-Agent Debate Framework for Fact Verification with Diverse Tool Augmentation and Adaptive Retrieval](https://arxiv.org/abs/2601.04742v1) | 2026 | C2, B1, C5 | Hallucinations via faithfulness scoring and answer relevance quantification in debate output |
| [Multi-Agent LLMs for Generating Research Limitations](https://arxiv.org/abs/2601.11578v2) | 2025 | C3, B8, C2 | Superficial limitation statements; semantic gaps missed by n-gram metrics |
| [Where Did It All Go Wrong? A Hierarchical Look into Multi-Agent Error Attribution](https://arxiv.org/abs/2510.04886v2) | 2025 | D4, B4, C3 | Identifies which agent/step caused failure in multi-agent interaction traces |
| [Rethinking All Evidence: Enhancing Trustworthy Retrieval-Augmented Generation via Conflict-Driven Summarization](https://arxiv.org/abs/2507.01281v1) | 2025 | C1, B1, C2 | Unverified knowledge conflicts; missing conflict detection in RAG retrieval |
| [Active Task Disambiguation with LLMs](https://arxiv.org/abs/2502.04485v1) | 2025 | A4, C1, C2 | Agent guesses on ambiguity instead of asking clarifying questions first |
| [CBEval: A framework for evaluating and interpreting cognitive biases in LLMs](https://arxiv.org/abs/2412.03605v1) | 2024 | A3, B3, B1 | Cognitive biases in LLM reasoning; framing effects, anchoring, survivorship |
| [Towards Detecting LLMs Hallucination via Markov Chain-based Multi-agent Debate Framework](https://arxiv.org/abs/2406.03075v1) | 2024 | B8, C2, C3 | Hallucinated claims via multi-agent debate verification without ground-truth validation |
| [Sora Detector: A Unified Hallucination Detection for Large Text-to-Video Models](https://arxiv.org/abs/2405.04180v1) | 2024 | B1, C2, B8 | Text-to-video hallucinations: content contradicting input prompts across frames |
| [FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios](https://arxiv.org/abs/2307.13528v2) | 2023 | B8, C2, C3 | Factual errors in LLM-generated text across QA, code, math, and review tasks |

## 2. Judge reliability — the caveat layer

Every title-level LLM-judge paper in this pool is a negative or cautionary result. Six of them describe a judge exhibiting a mode from your own taxonomy, so a judge-based detector for mode X can fail by mode Y.

| paper | yr | mode it exhibits | note |
|---|---|---|---|
| [When Wording Steers the Evaluation: Framing Bias in LLM judges](https://arxiv.org/abs/2601.13537) | 2026 | **A3** | Framing bias in judges: wording steers the verdict — your A3, with the judge as the agent. |
| [Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence](https://arxiv.org/abs/2608.25869) | 2026 | **B3** | Prior scores anchor the judge and compromise evaluation independence — your B3. |
| [The Silent Judge: Unacknowledged Shortcut Bias in LLM-as-a-Judge](https://arxiv.org/abs/2509.26072) | 2025 | **C3** | Judge rationalises from unacknowledged superficial cues — your C3, at the detector. |
| [One Token to Fool LLM-as-a-Judge](https://arxiv.org/abs/2507.08794) | 2025 | **C6** | A single token flips the verdict — your C6 aimed at the detector rather than the task. |
| [Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based Reinforcement Learning](https://arxiv.org/abs/2606.04923) | 2026 | **C6** | Reward hacking against rubric-based judges, with a detection method. |
| [Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning](https://arxiv.org/abs/2609.04194) | 2026 | **B8** | Judged step importance diverges from actual functional importance — the judge confabulates a rationale. |

### General trust/validity results

| paper | yr |
|---|---|
| [Time to REFLECT: Can We Trust LLM Judges for Evidence-based Research Agents?](https://arxiv.org/abs/2605.19196) | 2026 |
| [BabelJudge: Measuring LLM-as-a-Judge Reliability Across Languages and Agent Trajectories](https://arxiv.org/abs/2606.22329) | 2026 |
| [C2-Faith: Benchmarking LLM Judges for Causal and Coverage Faithfulness in Chain-of-Thought Reasoning](https://arxiv.org/abs/2603.05167) | 2026 |
| [Assessing Judging Bias in Large Reasoning Models: An Empirical Study](https://arxiv.org/abs/2504.09946) | 2025 |
| [Beyond correlation: The Impact of Human Uncertainty in Measuring the Effectiveness of Automatic Evaluation and LLM-as-a-Judge](https://arxiv.org/abs/2410.03775) | 2024 |
| [Mitigating the Bias of Large Language Model Evaluation](https://arxiv.org/abs/2409.16788) | 2024 |

## Implication for the telemetry spec

`detector.method` has no `judge` value — judge-based detection currently has to be logged as `monitor` or `self-report`. Given that the reliability layer above is entirely cautionary, a judge detector wants its own enum value and a `detector.confidence` that reflects measured judge-task agreement, not the judge's own stated confidence.
