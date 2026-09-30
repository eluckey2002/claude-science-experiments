# Pre-registration — "simple" three-arm ablation, task 01 (duration parser)

**Registered:** 2026-09-26, before any model call for this run.
**Frozen task definition:** `simple-ablation-task01.md`, artifact `86c2cca5-588f-489a-8943-6da21f38b040`, version `4c3b757c-ed71-4ab3-8f92-5e3978c44750`. Arm wording, oracle, and probes are frozen as written there; this record does not restate them and does not change them.
**Status:** pilot / instrumentation run, not a confirmation run. Its job is to find out whether the decision-fingerprint measurement is sensitive at all, not to certify a claim about the word "simple."

This record is frozen. If the task, the probes, or the arms change, that is a new run and a new record — not an edit to this one.

## Question and consuming decision

Does an unoperationalized quality adjective ("keep it simple") raise run-to-run disagreement on the silent decisions a coding prompt leaves open, without lowering how often the code is functionally correct?

This run can decide only whether the fingerprint-disagreement instrument is sensitive enough to see anything on one small task. It cannot decide whether the word "simple" caused any observed A-vs-B gap (see Scope) and it authorizes no claim about "simple" outside this task shape.

## Design

Three arms (A vague / B absent / C operationalized), exact wording frozen in the task file. Fixed model and fixed sampling temperature for all reps, resolved at run time via `host.reasoning_model()` and recorded in the run log (not hardcoded here, since literal model ids drift). k = 10 independent completions per arm, 30 model calls total. Each completion is executed, never read, against the 5 oracle cases and the 10 contested probes from the task file.

## Controls — run before any of the 30 model calls

### C1 — grader determinism (clean baseline)
Run one fixed hand-written correct `parse_duration` against the 10 probes twice.
**Expected:** identical fingerprint both times (0/10 disagreement).
**Failure meaning:** the grader itself is a noise source; stop, the instrument isn't ready.

### C2 — positive control (known divergence is detectable)
Two hand-written implementations that differ only on D6 (bare number) and D7 (invalid input) — one raises on invalid input and treats a bare number as an error, the other returns `None` and treats a bare number as seconds.
**Expected:** fingerprint diff is nonzero and lands exactly on the D6/D7 probe slots, 0 elsewhere.
**Failure meaning:** the metric can't detect a difference that's known to exist; stop.

### C3 — oracle non-interference
Both C2 implementations pass all 5 CORE oracle cases despite disagreeing on contested behavior.
**Expected:** 5/5 pass for both.
**Failure meaning:** the oracle is silently deciding contested behavior; it needs to shrink.

Any C1–C3 failure stops the run before a single model call is spent.

## Predictions, classified before any arm is run

### P1 — primary: scatter ordering
Mean pairwise disagreement (over all 45 within-arm pairs) computed per arm.
- **SUPPORTED:** point estimates satisfy disagreement(A) ≥ disagreement(B) > disagreement(C), and the bootstrap CI (2000 resamples, 80% interval — widened from the usual 90/95% because n=10/arm is a pilot-sized sample) on disagreement(A) − disagreement(C) excludes 0.
- **FALSIFIED:** the reverse ordering holds with the equivalent CI on disagreement(C) − disagreement(A) excluding 0.
- **INCONCLUSIVE:** anything else, including CIs that overlap 0 or an ordering that doesn't match either bar. Given n=10/arm, INCONCLUSIVE is the modal expected outcome for a pilot — it is not itself evidence against the hypothesis.

### P2 — secondary: correctness parity
Core pass rate (0–5) per arm.
- **Parity holds** if no arm's mean core pass rate differs from another's by more than 1/5.
- **Parity fails** — reported as a separate, stronger finding, not folded into P1 — if any arm's mean drops by more than 1/5 relative to another.

## Stopping rule

1. Run C1–C3. Any failure stops here; fix the grader, do not spend model calls, do not edit this record — write a new one.
2. If C1–C3 pass, run all 30 completions in one pass. No interim looks, no dropping or re-rolling a rep that "looks wrong."
3. Classify P1 and P2 exactly as defined above. No threshold changes after seeing the numbers.
4. Report the result once. A second pilot on this same task is a new registered record, not a rerun of this one.

## Scope — what this run can and cannot claim

**Can:** whether the fingerprint/disagreement instrument is sensitive on this one task, this one model, this one temperature, n=10/arm — i.e., whether it's worth building the full runner around.

**Cannot:**
- Attribute an A-vs-B gap to the word "simple" specifically. Rephrasing alone moves LLM output; that requires a paraphrase-control arm (k rephrasings of arm B that never touch the adjective) to establish a noise floor, which this run does not include.
- Generalize beyond one small, isolated function-writing task. Per the task file's own limit, this may just describe short functions, not the user's actual agent workflows.
- Certify a population-level effect. n=10/arm is a sensitivity check, not a powered confirmation.
