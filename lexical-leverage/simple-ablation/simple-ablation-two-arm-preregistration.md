# Pre-registration — "simple" ablation, two arms (Orchid-HEval sample) — v4

**Registered:** 2026-09-26, before any model call for this run. v2 applied the findings of two independent reviews of v1 (Reviewers C and D, `independent-reviews-two-arm.md`); v3 applied a delta review of v2 (one new main finding, one new minor, two consistency notes, one carried-over partial); v4 applies the second delta review's three wording-level minors (`delta-review-two-arm-v2-v3.md`), which returned zero main findings — the review loop's stopping rule. v4's edits are unreviewed wording changes to C7, the INCONCLUSIVE labels, and this preamble. No model call was made against any version.
**Relationship to prior work:** supersedes the four-arm registration `simple-ablation-orchid-preregistration.md` (artifact `4f67aa29-681c-420d-a68e-2441d58ed819`, version `f6685cb7-e5df-40eb-9c65-4169edf5b358`), which was reviewed independently twice ([independent reviews](independent-reviews-orchid-preregistration.md), artifact `e199789e-e8ff-4a10-86b4-e45c35ad70cb`) and found not fundable as written. That record stays frozen and unedited; no model call was ever made against it. This is a new, reduced record, not a revision.

**Question:** does appending "Keep it simple." to a function-level coding task make the model's run-to-run behaviour less consistent than the same task with nothing appended — in particular on inputs the task's own reference solution does not handle (the instrument's proxy for "unspecified"; see Reference fingerprint)?

This record is frozen. Changing the task sample, the arms, the fuzz inputs, the equality rule, or the decision thresholds after this point is a new record.

## What was cut, and why

The four-arm design tried to answer three questions at once (does "simple" add divergence; does operationalizing it remove divergence; how big is that against Orchid's own ambiguity manipulation). The reviews found that the operationalized arm constrained code *structure* while the instrument reads code *behaviour*, that the calibration ratio is undefined when its denominator nears zero, and that the three-way ordering rule let SUPPORTED fire when "simple" did nothing. Cutting to two arms removes all three problems and halves the spend. The other two questions become follow-ups, run only if this one comes out positive.

## Frozen task bank

Same 30 tasks as the superseded record, drawn from Orchid-HEval (SII-YDD/Orchid on Hugging Face, config `Orchid-HEval`, file `Orchid-HEval/data.jsonl`, 164 tasks) via `random.Random(20260926).sample(names, 30)`, sorted to dataset order:

`HumanEval/3`, `HumanEval/4`, `HumanEval/9`, `HumanEval/11`, `HumanEval/13`, `HumanEval/18`, `HumanEval/29`, `HumanEval/31`, `HumanEval/32`, `HumanEval/41`, `HumanEval/47`, `HumanEval/49`, `HumanEval/51`, `HumanEval/57`, `HumanEval/58`, `HumanEval/61`, `HumanEval/63`, `HumanEval/64`, `HumanEval/79`, `HumanEval/82`, `HumanEval/86`, `HumanEval/88`, `HumanEval/95`, `HumanEval/104`, `HumanEval/115`, `HumanEval/126`, `HumanEval/129`, `HumanEval/134`, `HumanEval/139`, `HumanEval/150`.

If a task's `prompt`, `test_case`, or `solution` field is missing or malformed at run time, or its signature fails the fuzzer typing rule, it is dropped and replaced by the next unused name in the same seeded order (re-run the sample with a larger draw count and take the 31st, 32nd, … names in order). The 164-name list in dataset order is snapshotted as a companion artifact at registration, so standbys do not depend on the hosted file's row order staying fixed.

## Design — two arms

For each task, the base is its clean `prompt` field with the entry point renamed to `solve` **everywhere it appears** — the `def` line and every doctest example in the docstring — so no trace of the original HumanEval function name remains. Renaming is applied identically to both arms before any model call.

- **A — vague:** base + `"\n\nKeep it simple."` appended verbatim.
- **B — absent:** base, unmodified.

k = 5 completions per (task, arm): 30 × 2 × 5 = **300 completions**.

**Model:** `host.reasoning_model()`, resolved once before the first call and written into the run log; a mid-run change invalidates the record.
**Sampling:** `thinking={"type": "disabled"}`, `temperature=1.0`, passed explicitly on every call. (The host forces temperature to 1 while thinking is active, so disabling thinking is what makes the temperature value ours.) Run-to-run divergence is the phenomenon under study; temperature 1.0 is the model's full sampling distribution and is the reference condition. Any other value is a different experiment.
**Call order:** control C6's 25 calls (arm B, the five C2 tasks, 5 reps) run first as a block in fixed task-then-rep order. The remaining 275 (task, arm, rep) triples are shuffled with `random.Random(20260926)` and run in that interleaved order. Timestamps logged. Because the five C6 tasks are the only ones whose arm-B completions precede their arm-A completions, the primary analysis is also recomputed with those five tasks excluded. **The all-30-task number governs the SUPPORTED / FALSIFIED / INCONCLUSIVE call.** The 25-task number is a sensitivity check: if it moves the point estimate by more than δ/2 = 0.025 or flips the classification, the run is reported as **INCONCLUSIVE-DUE-TO-ORDER-CONFOUND**, a distinct label, the same rule shape as the extraction-noise check.

## Correctness oracle

Each task's own `test_case` field, pass/fail only. No LLM judge anywhere on the measurement path.

## Disagreement instrument — type-directed fuzzing with fixed edge slots

For each task, 20 probe inputs, frozen before any model call and never shown to the model:

- **Slots 1–6, deterministic edge probes**, chosen by parameter type: empty value (`""`, `[]`, `0`, `0.0`), a singleton / length-1 value, a negative or below-range value, an oversized value (string of 200 chars, list of 200 elements, int 10**6), a whitespace-only string or all-equal list where the type allows, and one boundary value taken from the task's own `test_case` inputs (its smallest or largest). Where a type has fewer than six natural edges, the remaining slots fall to the random pool.
- **Slots 7–20, random in-domain probes**, generated with `random.Random(int(hashlib.sha256(task_name.encode()).hexdigest(), 16))` — a process-invariant seed; Python's built-in `hash()` is salted per process and must not be used — under this rule: `int` → uniform in [−100, 100]; `float` → uniform in [−100.0, 100.0] rounded to 3 decimals; `str` → printable ASCII, length uniform in [0, 30]; `List[int]`/`List[float]` → length uniform in [0, 12] of the above; `List[str]` → length uniform in [0, 8] of the above strings; `bool`, `Tuple[...]`, `Optional[...]` → per declared shape; untyped parameters → element type inferred from the task's own `test_case` inputs.

The full 30 × 20 probe set is generated once, saved as a companion artifact with its SHA-256 recorded here at freeze time, and loaded from that file at run time — the frozen inputs are data, not a formula.

Each of the 10 completions for a task (5 reps × 2 arms) is executed against those same 20 probes, each call under a **2-second timeout**. The 20-slot output/exception vector is the run's fingerprint.

**Slot equality (frozen):** two slots agree if both returned values and `a == b` (floats and floats inside lists compared with `math.isclose(rel_tol=1e-6, abs_tol=1e-9)`), or both raised and the exception **types** match (messages ignored; a timeout is its own type `ProbeTimeout`). Any other combination is a disagreement.

**Reference fingerprint:** each task's canonical `solution` field is run on the same 20 probes. Slots where the reference returns cleanly are **reference-valid** slots; slots where it raises are **reference-invalid** slots. This is the canonical author's behaviour on out-of-domain inputs, not a reading of the spec — the labels say so deliberately, and secondary analysis 1 is worded to match. Control C8 checks how well this proxy agrees with independently written implementations on the five C2 tasks. The canonical solution also serves as the reference implementation for controls C1 and C7, replacing the 30 hand-written implementations the superseded record required.

**Disagreement per (task, arm)** = mean over the 10 same-arm rep pairs of the fraction of the 20 slots that disagree.

## Extraction rule

The model is asked for exactly one fenced ` ```python ` block. Extraction takes the **first** fenced Python block. The block is executed in a fresh namespace; if that raises, or no callable named `solve` exists afterwards, the rep is an **extraction failure**. Extraction failures are recorded, kept in n, and given a fingerprint of 20 `ExtractionFailure` slots — so two extraction failures **agree** with each other and disagree with every executed rep. Extraction-failure rate is reported per arm as its own number.

## Primary analysis

**Contrast:** for each task, Δ = disagreement(A) − disagreement(B). Statistic = mean Δ over the 30 tasks.
**Interval:** bootstrap resampling **tasks** with replacement, 2000 resamples, **90%** interval on mean Δ.
**Permutation test:** within each task, shuffle the A/B labels among its 10 completions preserving the 5/5 split (C(10,5) = 252 labelings per task), recompute mean Δ; 5000 permutations; report the one-sided p for the observed mean Δ.
**Smallest effect of interest:** δ = **0.05** (one probe slot in twenty).

- **SUPPORTED** — the 90% interval lies entirely above 0 and the point estimate is ≥ δ; permutation p < 0.05.
- **FALSIFIED (below δ)** — the 90% interval lies entirely inside [−δ, +δ]. This is an equivalence claim — any effect is smaller than one slot in twenty — not a claim that the effect is exactly zero; an interval above 0 but inside δ is reported with that wording.
- **INCONCLUSIVE** — anything else.

The interval was raised from 80% to 90% on review.

**Precision feasibility (replaces an unstated power assumption).** A 90% interval on a mean over 30 tasks has half-width ≈ 1.645 · SD(Δ)/√30 ≈ 0.30 · SD(Δ). The design can land on either side of δ = 0.05 only if SD(Δ) across tasks is ≲ 0.17. Control C6 yields five per-task disagreement(B) values and their within-task spread; before the 275 remaining calls are spent, SD(Δ) is projected from them as √2 · SD(disagreement(B)) (the conservative independent-arms case) and the projected half-width is written into the run log. **If the projected half-width exceeds 0.05, the run does not proceed under this record** — a new record raises δ or the task count. INCONCLUSIVE remains the expected modal outcome at 30 tasks; the gate ensures it is a possible outcome rather than a certain one.

## Secondary analyses (pre-registered, descriptive)

1. Mean Δ restricted to **reference-invalid** slots and, separately, to **reference-valid** slots, with the per-task count of reference-invalid slots reported alongside (tasks with fewer than 3 such slots contribute little and are flagged). The hypothesis predicts the effect lives in the reference-invalid slots — inputs the canonical author's code does not handle. An effect confined to reference-valid slots is a correctness story and is reported as such. The interpretive weight this carries is bounded by C8's agreement rate.
2. Mean Δ with extraction failures excluded, alongside the primary (which includes them). If excluding failures moves the point estimate of mean Δ by more than δ/2 = 0.025, or flips the classification, the run is reported as **INCONCLUSIVE-DUE-TO-EXTRACTION-NOISE**, a distinct label. The per-arm extraction-failure rates are also compared directly (task-level 90% bootstrap interval on the A − B rate difference) and reported as a formatting effect of the appended sentence, separate from behavioural divergence.
3. Per-arm pass rate on the official `test_case` oracle: fraction of reps passing, averaged over tasks, with a task-level 90% bootstrap interval on the A − B difference. Reported, not thresholded.

## Consuming decision

- **SUPPORTED** → next registration is the two follow-ups this record cut, in order: (i) a paraphrase control — k rephrasings of arm B that never touch "simple" — to separate the word from prompt rephrasing in general; (ii) only if the word survives that, an operationalized arm redefined on the behavioural axis the fuzzer reads.
- **FALSIFIED** → "simple" is dropped as a test case for single-shot function-level tasks. The null is not generalized to other specification words or to agentic settings.
- **INCONCLUSIVE** → apply the diagnosis below; no automatic scale-up.
- **Any INCONCLUSIVE-DUE-TO-\* label** (ORDER-CONFOUND, EXTRACTION-NOISE, MEMORIZATION) is terminal: reported as-is with its cause, bypassing the floor/ceiling diagnosis, which applies only to plain INCONCLUSIVE.

**Diagnosis before any scale-up.** Bands are numeric: **floor** = mean disagreement below 0.05 in both arms; **ceiling** = above 0.80 in both arms; **mid-range** = everything else. If floor, run the memorization diagnostic. If it fires → **INCONCLUSIVE-DUE-TO-MEMORIZATION**, a distinct label; there is no clean redraw pool within Orchid, so this is reported as a limitation of public benchmarks, not fixed by redrawing. If it clears → floor effect, the instrument is not sensitive enough for these tasks; fix the instrument (probe design) before adding n. If ceiling → temperature-1 sampling noise dominates; report as ceiling, do not lower temperature within this record. Only mid-range arm means with an interval straddling δ justify a new record with more tasks.

**Memorization diagnostic:** per task, mean `difflib.SequenceMatcher` ratio (whitespace-normalized) between each of the 10 completions and the canonical `solution`. Fires if ≥ 20 of 30 tasks have mean ratio ≥ the **calibration bar**, where the bar is the 90th percentile of the ratio between the canonical `solution` and the independently hand-written implementations from control C2 (so "one obvious way to write it" is not mistaken for memorization). C2 gives exactly 10 such comparisons, so this bar is the second-highest of ten draws and is treated as provisional in any report that relies on it; if fewer than 10 are available the bar defaults to 0.85.

## Controls — run in the order C7, C1, C2, C3, C4, C5, C8 before any model call; C6 is then the first 25 of the 300 calls and gates the other 275; any failure stops the run

- **C1 — determinism:** run each task's canonical `solution` against its 20 probes twice; fingerprints identical.
- **C2 — positive control:** for 5 pre-named tasks (`HumanEval/3`, `HumanEval/11`, `HumanEval/29`, `HumanEval/57`, `HumanEval/104`), hand-write two correct implementations that differ on exactly one edge case, one task each from: empty input, singleton, negative/below-range, oversized, whitespace-only or all-equal. The probes must separate the pair for **all 5** tasks — the deterministic edge slots make this a requirement, not a hope.
- **C3 — oracle non-interference:** both C2 implementations pass all official `test_case` entries for their task.
- **C4 — type coverage:** the coded fuzzer classifies all 30 signatures and generates 20 probes for each, executed, not inspected.
- **C5 — rename integrity:** for each of the 60 prompts (30 tasks × 2 arms), the original function name appears zero times and `solve` appears at least once.
- **C6 — baseline gate:** arm B only, 5 tasks (the C2 tasks), 5 reps = 25 calls, run first as a block (see Call order). Gate statistic = the mean of the five per-task disagreement(B) values. It must exceed 0.02; if it does not, stop — the instrument cannot see anything at this temperature on these tasks, and the remaining 275 calls are not spent. These 25 completions are kept and count toward the main run. C6 also supplies the SD estimate for the precision-feasibility gate in the Primary analysis.
- **C7 — reference timeout audit:** run the canonical `solution` against all 600 probes once with timing. Any probe on which it needs more than 0.5 s (a quarter of the run-time budget) or times out is replaced: a random slot (7–20) takes the next draw from that slot's generator; a deterministic edge slot is handled by kind: the oversized slot and the whitespace-only / all-equal slot halve their length (200 → 100 → 50; 10**6 → 10**5 → 10**4) until they clear; the empty, singleton, negative/below-range, and test_case-boundary slots have no magnitude to shrink and are left as they are — the timeout is logged, the task is flagged, and that slot is excluded from the reference-valid / reference-invalid split for that task. The replaced probe set is what gets frozen. This keeps a slow-but-correct reference from turning a slot "reference-invalid" for a runtime reason. Runs before C1.
- **C8 — reference-validity proxy check:** for the five C2 tasks, compare which slots raise under the canonical `solution` against which slots raise under each of the two hand-written C2 implementations. Report the slot-level agreement rate (5 tasks × 20 slots × 2 implementations = 200 slot comparisons). This is reported, not gated: it bounds how much interpretive weight secondary analysis 1 can carry.

## Scope

**Can claim:** whether the two words "keep it simple", appended to a clean function spec, measurably change run-to-run behavioural consistency on fuzzed inputs, and whether any change concentrates on inputs the reference solution does not handle (the proxy for unspecified behaviour), for a single reasoning-tier model, single-shot, at temperature 1, on 30 HumanEval-derived tasks — and whether that change, if present, lives in reference-invalid slots or in reference-valid ones (correctness).

**Cannot claim:** that the effect is due to the word rather than to any appended text (paraphrase control is the follow-up); anything about operationalizing "simple"; anything about other specification words, other channels (system prompt, tool description, repo rule), other models, or agentic / multi-turn / tool-using settings. "Each run reports success" from the original framing is proxied by the oracle, not measured.
