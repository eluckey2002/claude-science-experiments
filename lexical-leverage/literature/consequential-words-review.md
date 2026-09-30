# Consequential words: what has actually been measured

**Scope.** The question — *which individual words carry the most behavioural leverage when
working with agents?* — does not yet exist as a research object. Nobody has published a
ranked, per-word consequentiality index. What exists is four literatures that each measure a
slice of it, largely without citing each other. This document maps those slices, grades the
evidence, names the gaps, and gives a protocol for measuring leverage in a local harness.

Companion file: `consequential_words_evidence.csv` — one row per lexical lever with channel,
measured outcome, effect, evidence grade, and citation.

---

## 1. The four literatures

**(a) Prompt sensitivity / robustness.** Establishes that wording matters enormously, then
treats it as *noise to be averaged away* rather than as semantics to be understood. Format
choice alone moves accuracy by many points and format rankings correlate only weakly between
models (FormatSpread, arXiv:2310.11324); a single character-level perturbation costs ~5 points
on GSM8K; POSIX (arXiv:2410.02185) proposes an aggregate sensitivity index per model. This
literature gives you the **noise floor** — indispensable, because any claim that a specific
word matters must clear it.

**(b) Social and affective framing.** Politeness, emotion, persona, influence tactics. The
most publicised and the least trustworthy. Politeness results reverse across studies, models
and languages (arXiv:2402.14531 vs. 2510.04950 vs. 2604.16275 vs. 2512.12812). EmotionPrompt
(arXiv:2307.11760) and NegativePrompt (arXiv:2405.02814) report gains from *opposite* emotional
valences, which should be read as evidence about register sensitivity, not about emotion.
Persona openers show no reliable gain across 162 roles × 2,410 questions (arXiv:2311.10054).

**(c) Output-form constraints.** The largest reproducible practitioner-relevant effect in the
whole set. "Be concise" degrades factual reliability across most models tested, up to a ~20%
drop in hallucination resistance (Phare, arXiv:2505.11365). This is a system-prompt word that
almost every production deployment contains, chosen for cost and latency reasons, with a
measured factuality price.

**(d) Evidentiary and epistemic language.** Two distinct directions, and this is the part of
the user's intuition that the literature most clearly vindicates:

- *Input side.* Confident framing of a false premise — "I'm sure that…", "My teacher told
  me…" — raises hallucination risk by up to ~15% relative to hedged framing of the same
  statement (Phare's graded Unsure / Confident / Very Confident ladder).
- *Output side.* Hedges in generated text are not neutral downstream. Every LLM judge tested,
  GPT-4o included, is non-robust to epistemic markers (EMBER, arXiv:2410.20774); the mapping
  from marker to actual accuracy is unstable (arXiv:2505.24778); and humans over-rely on
  overconfident model phrasing across five languages (arXiv:2507.06306).

In an agent pipeline these compose: an agent that hedges honestly is scored down by the judge
in the loop, and an agent that asserts confidently is over-trusted by the human at the end.

---

## 2. "Simple" — the specification-word class

The intuition is right and the literature supports it *as a class*, not yet per word.

"Simple", "clean", "efficient", "robust", "production-ready" are underspecified non-functional
requirements. They read as constraints but function as **silent delegations**: each transfers
an unmade design decision to the model, which resolves it invisibly and then reports success.
The Orchid benchmark (arXiv:2604.21505, 1,304 tasks, vagueness as one of four ambiguity types)
finds that requirement ambiguity consistently degrades performance, that **the most advanced
models degrade most**, that the same ambiguous requirement yields functionally divergent
implementations, and that models largely fail to detect or resolve the ambiguity on their own.
Clarifying-question rates are low across code LLMs (arXiv:2406.00215; 2504.16331; 2607.00711).

Two adjacent findings sharpen this for agents specifically:

- **Urgency is measurably harmful in code generation.** Operationalising Yukl & Falbe's
  influence tactics across five models on LiveCodeBench and SWE-bench Verified, framings
  emphasising urgency were associated with reduced correctness *and* reduced security
  (arXiv:2608.11513).
- **Constraint decay.** As structural requirements accumulate, agent assertion pass rates fall
  27.28 points on average from baseline to fully-specified, and convention-heavy frameworks
  fare far worse than explicit ones (arXiv:2605.06445). Adding precision to fight vagueness has
  its own cost curve.

So the practical shape is a trade-off, not a rule: vagueness costs correctness and hides
divergence; specification load costs constraint adherence. Neither end is free.

---

## 3. "Novelty" — measured as an axis, not as an instruction

Novelty appears in the literature as an *evaluation dimension*, not as a prompt word whose
presence shifts behaviour. The strongest result is the trade-off: with 100+ NLP researchers
doing blind review, LLM-generated ideas were judged **more novel** than expert ideas (p<0.05)
while slightly weaker on feasibility, and LLM self-evaluation of novelty failed
(arXiv:2409.04109). Creativity metrics themselves are inconsistent across domains and a metric
that discriminates creativity in one domain fails in another (arXiv:2508.05470).

The operational reading for anyone running a search or evolutionary loop: "novelty" is cheap to
increase, expensive to validate, and the model cannot grade its own. Putting it in an objective
function without an external validity check buys distance from the prior rather than quality —
which is the same failure shape as an agent reporting success against a vague adjective.

---

## 4. What is genuinely unmeasured

1. **Per-word leverage rankings.** No study ranks individual lexemes by behavioural effect
   size. POSIX gives per-*model* sensitivity; nothing gives per-*word* consequentiality.
2. **"Simple" and its family in isolation.** Studied only inside an aggregate "vagueness"
   category, never as individual adjectives with individual effect sizes.
3. **Agent-trace outcomes.** Almost everything above measures answer accuracy or pass rate.
   Nothing systematically measures how a word changes *decisions*: whether the agent asks a
   clarifying question, how many tools it calls, how many files it touches, whether it writes
   tests, whether it abstains, how far scope drifts.
4. **Long-horizon propagation.** Whether a single word in turn 1 still shapes behaviour at turn
   40. Multi-agent sycophancy propagation (arXiv:2604.02668) is the only early probe.
5. **Channel placement.** Whether the same word in a system prompt, a skill file, a task brief,
   or a tool description carries different weight. Unstudied.

Gaps 1–3 are directly addressable in a local harness. That is the design below.

---

## 5. Protocol: measuring lexical leverage

The single methodological requirement — and the thing practitioner A/B tests almost always
omit — is a **paraphrase control arm**. Without it, an observed effect cannot be distinguished
from ordinary prompt-sensitivity noise, and literature (a) shows that noise is large.

**Design.** For each candidate word *w*:

1. **Treatment arm.** A base task prompt with *w* inserted at a fixed position, and a matched
   variant with *w* removed or replaced by a neutral counterpart ("simple" → ∅, and "simple" →
   "working"). Hold token count as close as possible; log it.
2. **Control arm.** N semantics-preserving paraphrases of the *same* base prompt that do not
   touch *w*. This arm measures the noise floor for this task and model.
3. **Replication.** k runs per cell at fixed temperature and fixed model version; report
   intervals, never point estimates. Model version and decoding params are part of the unit of
   analysis — politeness results already demonstrate that effects do not port across versions.

**Outcome metrics — decision-level, not just accuracy.** This is where a local harness beats
the published work:

- clarifying-question rate (did it ask, or did it guess?)
- tool-call count and tool-call mix
- files touched, diff size, lines deleted
- test-written rate; test-passed rate
- abstention / refusal rate
- scope drift: work done outside the stated target
- retries and self-corrections
- for judged tasks: judge score *and* the hedge density of the output, scored separately

**Effect size.** Define leverage as a z-score against the control arm:
`leverage(w) = |mean(treatment) − mean(base)| / sd(paraphrase control)`.
A word earns attention only when leverage > ~2, i.e. its effect exceeds what rephrasing the
prompt does anyway. Report leverage per outcome metric — a word can be inert for accuracy and
large for scope drift, which is precisely the case for the specification-word class.

**Starter word set** (ordered by expected leverage, from the evidence above):
`concise` / `briefly` · `simple` · `robust` / `production-ready` · `ASAP` / `urgent` ·
`novel` · `just` · `quick` · `comprehensive` · `obviously` / `I'm sure` (input-side
evidentiary) · `verify` / `confirm` / `proven` (output-side evidentiary) ·
`please` (as a low-expected-leverage negative control).

**Confounds to log explicitly:** token-count delta, position in prompt, channel (system vs.
user vs. tool description vs. skill file), model version, temperature, and whether the word
appears in a reasoning-visible or reasoning-hidden configuration.

---

## 6. Bottom line

- Evidentiary language is the best-supported part of the intuition, in both directions: confident
  framing of premises corrupts factuality (~15%), and hedging in output corrupts downstream
  judging and human reliance.
- "Be concise" is the highest-leverage word in most production system prompts, at up to a ~20%
  factuality cost, and is almost always chosen for reasons unrelated to accuracy.
- "Simple" belongs to a class whose measured harm is real but only ever measured in aggregate —
  it degrades most in the strongest models, and models do not flag it.
- "Novelty" is an axis the model cannot self-grade; treat it as requiring an external check.
- Politeness, emotion, and persona are the loudest results and the weakest evidence. Do not
  port any of them across models, versions, or languages without re-measuring.
- Every claim above must clear a paraphrase noise floor before it counts as a word effect.
