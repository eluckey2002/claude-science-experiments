# Pre-registration — "simple" ablation, multi-task (Orchid-HEval sample)

**Registered:** 2026-09-26, before any model call for this run.
**Relationship to prior work:** independent of `simple-ablation-task01-preregistration.md` (artifact `2e6c3e56-4a5d-4b6e-9b96-4c928dd6a40d`), which stays frozen and unedited, shelved as a possible later side-check. This is a new registration, not a revision.
**Question (unchanged from task01):** does telling a model to "keep it simple" cause silent, incompatible run-to-run decisions on things the prompt never specified, even though each run looks fine and reports success on its own.

This record is frozen. Changing the task sample, the arms, or the disagreement metric after this point is a new record, not an edit to this one.

## Frozen task bank

30 tasks drawn from Orchid-HEval (SII-YDD/Orchid on Hugging Face, config `Orchid-HEval`, file `Orchid-HEval/data.jsonl`, 164 tasks total), via `random.Random(20260926).sample(names, 30)`, sorted back to dataset order:

`HumanEval/3`, `HumanEval/4`, `HumanEval/9`, `HumanEval/11`, `HumanEval/13`, `HumanEval/18`, `HumanEval/29`, `HumanEval/31`, `HumanEval/32`, `HumanEval/41`, `HumanEval/47`, `HumanEval/49`, `HumanEval/51`, `HumanEval/57`, `HumanEval/58`, `HumanEval/61`, `HumanEval/63`, `HumanEval/64`, `HumanEval/79`, `HumanEval/82`, `HumanEval/86`, `HumanEval/88`, `HumanEval/95`, `HumanEval/104`, `HumanEval/115`, `HumanEval/126`, `HumanEval/129`, `HumanEval/134`, `HumanEval/139`, `HumanEval/150`.

All 30 signatures were checked before registration and classify cleanly under the fuzzer typing rule below (see Controls, C5). If a task's clean `prompt` or `test_case` field is missing or malformed at run time, it is dropped and replaced by the next unused name in the same seeded sample order (drawing one extra name now as standby: re-running the sample with `k=31` and taking the 31st).

## Design — four arms

For each sampled task, take its clean `prompt` field (the original HumanEval description, functionally complete) as the base. Four arms:

- **A — vague:** base prompt + `"\n\nKeep it simple."` appended verbatim, no other change.
- **B — absent:** base prompt, unmodified. Baseline.
- **C — operationalized:** base prompt + `"\n\nConstraints: standard library only, at most one helper function, no CLI or __main__ block."` — a generic, task-agnostic reading of "simple" (structural, not a line-count, since task difficulty varies too much across the sample for one length cap to be fair to all of them).
- **D — calibration:** the task's own `Vagueness_prompt` field, verbatim, unmodified. This is Orchid's own published ambiguity manipulation (deletes a functional detail from the spec). It is a scale reference, not a hypothesis about "simple" — see P3.

k = 5 completions per (task, arm): 30 × 4 × 5 = **600 completions total**.

**Model:** `host.reasoning_model()`, resolved and written into the run log before analysis; a mid-run change invalidates the record. **Temperature:** fixed default, also snapshotted into the run log.

## Correctness oracle

Each task's own `test_case` field (input/output/relation triples, inherited from HumanEval) — pass/fail only. No LLM judge anywhere on this path.

## Disagreement measurement — type-directed fuzzing (replaces hand-built probes)

Task01 used 10 hand-picked probe inputs written specifically for the duration parser. That doesn't scale to 30 arbitrary tasks without 30 rounds of manual probe design — the exact cost that moving to an existing benchmark was meant to avoid. Instead:

1. For each of the 30 tasks, generate `n_probe = 20` random inputs matching the function's parameters, typed by this frozen rule: `int` → random integer in a task-appropriate range; `float` → random float; `str` → random ASCII string, varying length including empty; `List[int]`/`List[float]` → random-length list (including empty and length-1) of random numbers; `List[str]` → random-length list of random strings; untyped `list`/bare parameters → infer element type from the shapes already present in that task's own `test_case` inputs; `bool`, `Tuple[...]`, `Optional[...]` → generated explicitly per their declared shape. A task whose signature doesn't classify under this rule is dropped per the fallback above.
2. The 20 fuzzed inputs are frozen per task before any model call and never shown to the model.
3. All 5 reps × 4 arms = 20 completions for a given task are executed against that task's same 20 fuzzed inputs. Each run's 20-slot output/exception vector is its fingerprint — read off by execution, never by inspecting code, same principle as task01.
4. Disagreement per (task, arm) = mean pairwise fraction of differing slots among the 5 same-arm reps.
5. Primary aggregate = mean disagreement across the 30 tasks.

**M1 fix (pseudo-replication):** the bootstrap CI on the primary aggregate resamples the 30 **tasks** (with replacement), not the within-arm run-pairs and not the individual reps — tasks are the true independent unit now. A permutation test (shuffle the four arm labels among each task's 20 completions, recompute the aggregate, repeat many times) supplies the null distribution directly.

## Predictions

**P1 — primary scatter ordering.** SUPPORTED if disagreement(A) ≥ disagreement(B) > disagreement(C) and the task-level bootstrap CI (2000 resamples, 80% interval — still pilot-sized at 30 tasks) on disagreement(A) − disagreement(C) excludes 0, corroborated by the permutation test. FALSIFIED if the reverse ordering holds with the equivalent CI excluding 0. INCONCLUSIVE otherwise. This prediction states only that disagreement moves; it does not presuppose that movement is a cost (see Scope).

**P2 — correctness parity.** Mean task-pass-rate per arm (aggregated over the 30 tasks). Parity holds if no arm's mean differs from another's by more than 1/5; parity failing is reported as a separate, stronger finding, not folded into P1.

**P3 — calibration comparison (descriptive, not a pass/fail test).** Report disagreement(A) / disagreement(D) as the size of the "simple" effect relative to Orchid's own validated ambiguity manipulation on the same 30 tasks. This contextualizes P1's result; it does not itself get a SUPPORTED/FALSIFIED label, since D isn't a hypothesis about "simple."

## Consuming decision — what each outcome triggers

- **P1 SUPPORTED** → write a paraphrase-controlled confirmation (k rephrasings of arm B that never touch "simple") before treating the word itself, rather than prompt rephrasing in general, as the cause.
- **P1 FALSIFIED** → drop "simple" as a test case for function-level tasks of this shape; do not generalize the null to other specification words (robust, concise, production-ready, etc.) without testing them separately.
- **P1 INCONCLUSIVE** → apply the floor/ceiling rule below before deciding whether to add tasks/reps or redesign.

**Floor/ceiling invalidation rule:** if disagreement sits near 0 for all arms across most tasks, run the memorization diagnostic (below) before concluding anything. If it implicates memorization, that is a **memorization floor**, not an instrument problem — see its own action below, distinct from the fuzzer-is-broken branch. If the diagnostic clears the tasks of memorization, then it is a genuine floor effect (fuzzed inputs or tasks too easy to expose any ambiguity) — fix the instrument, don't add n. If disagreement sits near max for all arms, sampling noise at the registered temperature is dominating — lower the temperature, don't add n. Only a real, plausible-but-borderline spread justifies scaling up tasks or reps.

**Memorization diagnostic (new, closes an internal-validity gap found in review):** HumanEval is one of the most reproduced coding benchmarks in existence, so a model may retrieve a memorized canonical solution regardless of arm wording — producing the same near-zero-disagreement symptom as a genuine floor effect, but for a reason unrelated to "simple." Each Orchid row ships the dataset's own canonical `solution` field for exactly this check. For every task, compute `difflib.SequenceMatcher` similarity (on whitespace-normalized code) between each of the 20 completions and that task's `solution` field, then take the per-task mean.

**Primary mitigation (applied before this diagnostic is ever needed):** every arm, for every task, uses a neutral, renamed entry point (e.g. `below_zero` → `solve`) instead of the original HumanEval function name, and the docstring is otherwise left intact. This strips the single strongest retrieval cue — the exact name that's been quoted across blogs, repos, and leaderboards — without changing task complexity, signature simplicity, or the fuzzer's applicability. All arms and the calibration arm get the same renamed entry point, so this is not a confound between arms.

**If memorization is still flagged after renaming** — 20 or more of the 30 tasks show mean similarity ≥ 0.85 to the canonical `solution` — there is no clean redraw pool within Orchid: the less-reproduced split (Orchid-BCB-Expand, BigCodeBench-based) requires pandas/numpy/matplotlib and non-scalar return types (e.g. `matplotlib.figure.Figure`), which is incompatible with both the stdlib-only operationalized arm and the type-directed fuzzer. In that case the honest outcome is to report the run as INCONCLUSIVE-DUE-TO-MEMORIZATION, a distinct label from ordinary INCONCLUSIVE, and treat it as a limitation of testing on any public, widely-reproduced benchmark rather than something this registration can fix by redrawing. Below the 0.85/20-task bar, memorization is not presumed to explain the result and the ordinary floor-effect branch applies.

## Controls — run before any of the 600 model calls

- **C1 — fuzzer/grader determinism:** for each of the 30 tasks, run one fixed correct hand-written implementation against its own 20 fuzzed inputs twice. Expect identical fingerprints both times.
- **C2 — positive control:** for 5 of the 30 tasks, hand-write two implementations differing on one plausible edge case (e.g., empty-input handling). Expect the 20 random fuzz inputs to catch the difference for at least 4 of the 5 tasks (fuzzing is random, so 100% isn't required, but a real difference should usually surface).
- **C3 — oracle non-interference:** both C2 implementations for each of the 5 tasks must still pass all of that task's official `test_case` entries despite disagreeing elsewhere.
- **C4 — calibration-arm sanity:** for the same 5 spot-checked tasks, confirm `Vagueness_prompt` differs from the clean `prompt` only by the documented deletion/alteration, not by any other accidental spec change.
- **C5 — fuzzer type coverage:** confirm all 30 sampled signatures classify under the typing rule above (checked at registration time — 100% coverage on `int`, `str`, `list`/`List[int]`/`List[float]`/`List[str]` — re-verify once the fuzzer is actually coded, since the check here was structural, not executed).

Any C1–C5 failure stops the run before a single model call is spent.

## Extraction and execution rule

The model is instructed to return exactly one fenced ` ```python ` block containing the completed function. Extraction pattern: first such fenced block in the response. If no fenced block is found, or the extracted code raises `SyntaxError`/`ImportError` before any of the 20 fuzz probes can run, that rep's fingerprint is recorded as all-slots-error — folded into the disagreement calculation as maximally divergent from every other outcome, never dropped from n.

## Scope — what this run can and cannot claim

**Can:** whether "simple," in this one generic operationalization, produces measurable, above-floor divergence across a real sample of function-level coding tasks — and how that divergence sizes up against Orchid's own validated ambiguity effect on the same tasks.

**Cannot:** claims about other specification words (robust, concise, production-ready, ...) without testing them separately; claims about channels other than a direct task-brief instruction (system prompt, tool description, repo rule file); claims about agentic, multi-turn, or tool-using settings — this is single-shot function-level generation only, same limitation task01 already carried.
