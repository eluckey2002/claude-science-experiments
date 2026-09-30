# Review log — task01 pre-registration

**Reviews:** `simple-ablation-task01-preregistration.md`, artifact `2e6c3e56-4a5d-4b6e-9b96-4c928dd6a40d`, version `5a84650f-c1ed-4aee-97f5-90629cb0ecfa`.
**Status:** findings only — not yet applied. The registration is frozen as written; if these are folded in, that happens as a new version before any model call runs, or as a superseding v2 record if a model call has already run by then (per this project's own chain-offer-v2 convention).

## Main findings

**M1 — pseudo-replication in the CI.** P1's bootstrap treats all 45 within-arm pairs (from k=10 runs) as independent observations. They aren't — all 45 are built from the same 10 draws, so the CI comes out tighter than the data supports. Fix: bootstrap by resampling the 10 runs per arm (with replacement) and rebuild the pairwise statistic each draw; add a permutation test that shuffles the 20 arm-A/arm-C labels to build a null directly.

**M2 — no consuming decision.** The registration states what run 01 can and cannot prove, but never states what action each outcome triggers. This project's own house convention (the 2248 registered-protocol format) always names "the consuming decision" — what happens next isn't optional detail, it's part of the registration. As written, SUPPORTED, FALSIFIED, and INCONCLUSIVE could all land and nothing downstream would be committed to move. Needs one line per outcome: SUPPORTED -> write the paraphrase-controlled confirmation registration; FALSIFIED -> drop "simple" as a test case, do not generalize the null to other specification words; INCONCLUSIVE -> [undecided — rerun at higher n, try a different task, or stop here; this choice itself needs making, not just the trigger].

## Minor findings

- No floor/ceiling invalidation rule: if arm A saturates at 10/10 disagreement or arm C bottoms at 0/10, the ordering can't be read, and nothing in the doc currently treats that as invalidating.
- Code-extraction and execution-failure handling (how a completion becomes a tested function, what an extraction failure counts as) isn't pre-registered — undisclosed flexibility in the analysis pipeline.
- P1's phrasing ("raise disagreement... without lowering correctness") presupposes disagreement is a cost; the Scope section hedges this but the prediction's own wording doesn't.
- "Resolved at run time via host.reasoning_model()" isn't yet paired with a rule to snapshot the resolved model string + temperature into the run log, or to invalidate the record on a mid-run change.
