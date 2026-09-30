# Agent rule files (CLAUDE.md / AGENTS.md) — literature the detector survey missed

The 509-record pool behind `detector-coverage` contains **zero** records mentioning CLAUDE.md or AGENTS.md: none of those 74 queries reached this literature. Seven targeted queries returned 39 records, 30 relevant. Abstract-level evidence only.

This is a distinct detector family. Everything in `detector-coverage` inspects a *trace*; most of this work inspects the *rule file* — a preflight artifact check rather than a runtime monitor.

## Findings

| paper | yr | kind | finding |
|---|---|---|---|
| [Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and Persistent Configuration for Coding Agents](https://arxiv.org/abs/2604.11088) | 2026 | empirical | 679 rule files / 25,532 rules from GitHub, 5,000+ Claude Code runs on SWE-bench Verified. Rule files give +13.8pp — but gains are largely content-independent: random, shuffled, mismatched-domain and unconverted-format files all match curated ones, which the authors attribute to context priming. Rule polarity is the one content effect that survives: every individually beneficial rule is a negative constraint, every individually harmful one a positive directive. Individually harmful rules do not accumulate damage in ensemble — pass rates stay stable from 0 to 50 rules. Stated principle: constrain what agents must not do rather than prescribing what they should. |
| [Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding](https://arxiv.org/abs/2608.11095) | 2026 | empirical | 247,694 instruction lifetimes across 1,867 repositories: files grow +226% over their lifetime, +4.9 net instructions per commit, older instructions progressively less likely to be deleted (log-hazard -0.032/commit). Traced to deletion cost — once an instruction's rationale is gone, removing it safely costs O(2^|D|). The fix is measured, not proposed: prompt comments encoding the latent reasoning cut excess instructions by 99.3% (+211.3% growth down to +1.4%) and improve real-world agentic instruction-following by up to 23.1% on WildIFEval. |
| [Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories](https://arxiv.org/abs/2607.27250) | 2026 | empirical | Controlled two-agent ablation (Claude Code + Codex, 3 repos, 17 tasks, 288 gold-test-evaluated runs). Context strategy does not measurably move correctness — equivalence-bounded to <=10-15pp; a manipulation probe found the real AGENTS.md never converted a near-miss to a pass. Also supplies a reconciliation for the contradictory prior literature: borderline task difficulty is agent-specific (Spearman rho=0.75), so single-agent studies sample from different agents' informative bands. |
| [When "Do Not" Is Not Deny: Security Rules in CLAUDE.md vs Built-In Controls](https://arxiv.org/abs/2608.23550) | 2026 | empirical | 481 public CLAUDE.md files. Only ~4-16% of extracted security rules had a matching Claude Code built-in control; 4.4% under the strictest matching standard (95% CI 2.6-6.7%). Quantifies the gap between an interpreted 'do not' and an enforced deny. |
| [Configuration Smells in AGENTS.md Files: Common Mistakes in Configuring Coding Agents](https://arxiv.org/abs/2606.15828) | 2026 | detector | First smell catalog for coding-agent config files: six smells with automated detection heuristics, prevalence measured on 100 popular repos. The only runnable linter in this set. |
| [Context Rot in AI-Assisted Software Development: Repurposing Documentation Consistency for AI Configuration Artifacts](https://arxiv.org/abs/2606.09090) | 2026 | roadmap | Names 'context rot' — config drifting stale as code evolves — and argues decades of documentation-consistency tooling transfers directly to detecting it. Research roadmap, no tool released. |
| [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](https://arxiv.org/abs/2606.20512) | 2026 | method | Argues how guidance is produced is the decisive variable; probe-and-refine tuning patches a repository's guidance file via synthetic bug-fix probes with no agent loop during tuning. |
| [PACT: Can Enterprise AI Assistants Be Trusted Under Pressure?](https://arxiv.org/abs/2609.18605) | 2026 | benchmark | PACT: rule-following under pressure. 12 regulated enterprise domains, 48 multi-turn scenarios, each pairing a standing rule against a rule-violating shortcut, with pressure applied by a persistent user or hurried manager. |
| [Structural Quality Gaps in Practitioner AI Governance Prompts: An Empirical Study Using a Five-Principle Evaluation Framework](https://arxiv.org/abs/2604.21090) | 2026 | audit | Five-principle structural-completeness framework applied to 34 public AGENTS.md governance files; 37% of file-model pairs score below threshold, with data classification and assessment rubrics most often missing. |
| [Operationalizing Ethics for AI Agents: How Developers Encode Values into Repository Context Files](https://arxiv.org/abs/2605.05584) | 2026 | survey | Developers already encode fairness, accessibility, sustainability, tone and privacy rules into repository context files — a developer-authored governance layer. |
| [An Exploratory Study of Agent Plans for Agentic AI Coding Tools in Open-Source Software](https://arxiv.org/abs/2608.04661) | 2026 | survey | Agent Plans as a distinct task-oriented artifact: 36,710 repositories screened, 85 plan files found in 10 repos. |
| [What's Inside a GitHub Repository? An Empirical Study on the Contents of 10K Projects](https://arxiv.org/abs/2605.16701) | 2026 | prevalence | 10,000 GitHub repositories over ten years; AGENTS.md and CLAUDE.md appear as emerging standard content. |

## What is deflationary

Content curation does not earn its keep. The +13.8pp in 2604.11088 survives randomising, shuffling, and swapping the domain of the rule file, so it is a priming effect rather than a knowledge-transfer effect, and effort spent hand-authoring rule *content* is buying something other than what it appears to buy. Positive directives ("follow code style") are the individually harmful class. A rulebook full of prescriptions is the configuration this study argues against.

## What is actionable

1. **Polarity.** Prefer negative constraints to positive directives. This is the one content effect that survived randomisation, and it is stated as a design principle by the authors.

2. **Annotate the rationale.** Prompt comments removed 99.3% of excess instructions and lifted instruction-following by up to 23.1% (2608.11095). The mechanism is deletion cost: a rule whose reason is recorded can be retired safely, a rule whose reason is lost cannot.

3. **Move security rules to enforced controls.** Only 4.4% of security rules in 481 public CLAUDE.md files had a matching built-in control under strict matching (2608.23550). Prose for conventions, deny rules for boundaries.

4. **Lint the file.** 2606.15828 ships six configuration smells with automated detection heuristics — the only runnable tool in this set.

## What is genuinely missing

Every study here measures either task correctness or rule-file quality. **None measures whether an agent complied with the rulebook on a given run.** PACT (2609.18605) is the closest, and it scores rule-following on purpose-built scenarios rather than auditing a real trace against a real repository's rules. A compliance detector — enumerate the standing rules, check the trace against each — has no published instrument.

## On the apparent contradiction

2604.11088 reports +13.8pp; 2607.27250 reports a null bounded to <=10-15pp. The ablation paper supplies its own reconciliation: borderline task difficulty is agent-specific (Spearman rho=0.75), so studies drawing tasks from one agent's informative band will disagree with studies drawing from another's. Cite both, and read the null as bounded rather than absent.
