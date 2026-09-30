# Cold audit — simple-ablation-orchid-preregistration.md (v2)

Run by FRESH_EYES_AUDITOR, no shared context with the design conversation, no network access.
Reviews artifact `4f67aa29-681c-420d-a68e-2441d58ed819`, version `f6685cb7-e5df-40eb-9c65-4169edf5b358`.

**Post-audit verification note:** the audit's one "flagged but provisional" risk (fuzzer typing rule not covering HumanEval/95, /115, /129) was checked directly against the real Orchid-HEval file after this audit completed. Confirmed real, not provisional: `check_dict_case(dict)`, `max_fill(grid, capacity)`, `minPath(grid, k)` all use dict/nested-list parameters the frozen typing rule never defines a generation strategy for. This promotes that item from "flagged risk" to a seventh blocking defect.

---

# Audit: `simple-ablation-orchid-preregistration.md`

**Scope note (read before the findings):** I have no network access, so I could not verify the document's claims about the external dataset (`SII-YDD/Orchid` on Hugging Face, its `Orchid-HEval` config/field names, the 164-task count, or the existence of `Vagueness_prompt`/`solution` fields). Those are flagged separately below rather than assumed correct. Everything else below is an internal-consistency check of the document as written, in the order the audit brief asked for.

I found **six blocking defects** and one flagged-but-unverifiable internal-consistency risk that is severe enough to sit alongside them. I also found five non-blocking improvements.

---

## Blocking defects

**B1 — The renamed-entry-point mitigation is not specified precisely enough for two implementers to do the same thing, and as written it doesn't deliver what it claims.**

Location: "Memorization diagnostic" section, "Primary mitigation" paragraph.

> "every arm, for every task, uses a neutral, renamed entry point (e.g. `below_zero` → `solve`) instead of the original HumanEval function name, and the docstring is otherwise left intact. This strips the single strongest retrieval cue"

Three unresolved questions, each with two defensible readings:
- *Mechanism*: nothing states how the rename is actually applied to the "clean `prompt` field" defined in the Design section (string-substitute the function name token, regenerate the signature line, or append an instruction telling the model what to call the function). The Design section's "base prompt" is defined *before* this mitigation appears and is never revised to say it's the renamed version.
- *Naming scheme*: "e.g." leaves open whether every task uses the same literal name (`solve`) or a per-task name. This affects reproducibility of which exact prompt was shown.
- *Self-contradiction*: many HumanEval-style docstrings include doctest examples that call the function by its original name (e.g., `>>> below_zero([1, 2, -4, 5])`). If "the docstring is otherwise left intact," the old name survives inside the doctest examples even while the `def` line shows the new name — which directly undercuts the claim that this "strips the single strongest retrieval cue," since the cue is still present in the docstring body. Two implementers could reasonably rename only the signature (leaving the old name inside the docstring, per the literal instruction) or rename everywhere (violating "otherwise left intact") — producing two different prompts and, downstream, two different memorization-similarity readings.

**B2 — The floor/ceiling decision rule has no numeric thresholds, so the corrective action isn't determined by the document.**

Location: "Consuming decision" section, "Floor/ceiling invalidation rule."

> "if disagreement sits near 0 for all arms across most tasks, run the memorization diagnostic... If disagreement sits near max for all arms, sampling noise at the registered temperature is dominating... Only a real, plausible-but-borderline spread justifies scaling up tasks or reps."

"Near 0," "most tasks," and "near max" are never given numeric definitions anywhere in the document. Whether a given result triggers the memorization branch, the "fix the instrument" branch, the "lower temperature" branch, or the "scale up" branch is a judgment call — two implementers looking at the same 30×4 result table could pick different branches and therefore take different next actions from an identical dataset.

**B3 — The P2 parity threshold is ambiguous between an absolute and a relative reading.**

Location: "Predictions" section, P2.

> "Parity holds if no arm's mean differs from another's by more than 1/5"

Since pass rate is a proportion in [0,1], "differs... by more than 1/5" is defensible as either an absolute difference (>0.2 percentage-point gap) or a relative difference (>20% of the compared arm's rate). These produce different parity verdicts whenever pass rates are low (e.g., a gap of 0.10 vs. 0.30 pass rate is a 0.20 absolute difference — exactly at the boundary — but a 200% relative difference, clearly failing parity under the relative reading).

**B4 — Extraction-failure handling is defined for the disagreement metric but never defined for the correctness metric (P2).**

Location: "Extraction and execution rule" section, cross-referenced against "Predictions" P2.

> "If no fenced block is found, or the extracted code raises `SyntaxError`/`ImportError` before any of the 20 fuzz probes can run, that rep's fingerprint is recorded as all-slots-error — folded into the disagreement calculation as maximally divergent from every other outcome, never dropped from n."

This rule only says what happens to the *disagreement* fingerprint. P2 ("Mean task-pass-rate per arm") never states whether an extraction failure counts as a failed test (0, included in the denominator) or is excluded from the denominator entirely. The two readings give different pass rates and could flip a parity verdict.

**B5 — The standby-task replacement is not reproducible as specified.**

Location: "Frozen task bank" section.

> "30 tasks drawn from Orchid-HEval... via `random.Random(20260926).sample(names, 30)`, sorted back to dataset order" ... "it is dropped and replaced by the next unused name in the same seeded sample order (drawing one extra name now as standby: re-running the sample with `k=31` and taking the 31st)."

The primary 30 tasks are safe because they're spelled out explicitly in the document — an implementer never needs to re-run the sampling code to get them. But the standby (31st) task is *not* enumerated anywhere, so if a task needs replacing, the implementer must actually execute `random.Random(20260926).sample(names, 31)`, and `names` — the ordered list fed into `.sample()` — is never defined (dataset file order? lexicographic task-ID order? numeric order?). Since `random.sample`'s output for the same seed depends on input order, two implementers with different `names` orderings get different 31st tasks, and thus a different backup task enters the run with no way to detect the divergence afterward.

**B6 — The permutation test's "corroboration" criterion and iteration count are unspecified.**

Location: "Disagreement measurement" (M1 fix) and "Predictions" P1.

> "A permutation test (shuffle the four arm labels among each task's 20 completions, recompute the aggregate, repeat many times) supplies the null distribution directly." ... "SUPPORTED if disagreement(A) ≥ disagreement(B) > disagreement(C) and the task-level bootstrap CI... excludes 0, corroborated by the permutation test."

The bootstrap gets a precise spec ("2000 resamples, 80% interval"). The permutation test gets neither an iteration count ("repeat many times") nor a decision rule for what "corroborated by" means (e.g., observed statistic outside the 90th percentile of the null? p < 0.05? just same-sign?). Since "corroborated by the permutation test" is one of the three conjunctive conditions for SUPPORTED, the verdict is partly gated on a check the document never specifies how to compute.

---

## Flagged risk (cannot fully verify without network access, but material)

**The fuzzer's typing rule may not cover several of the 30 sampled tasks, contradicting the document's own pre-registration claim.**

Location: "Frozen task bank" ("All 30 signatures were checked before registration and classify cleanly under the fuzzer typing rule below") and "Disagreement measurement," point 1 (the typing rule: `int`, `float`, `str`, `List[int]`/`List[float]`, `List[str]`, untyped/bare lists, `bool`, `Tuple[...]`, `Optional[...]`).

Based on the standard, widely-published HumanEval task set (which I could not cross-check against the live Orchid file), at least two of the sampled tasks appear to use parameter shapes the typing rule never defines a generation strategy for: a dictionary-typed parameter (HumanEval/95, `check_dict_case`) and nested `List[List[int]]` grid parameters (HumanEval/115 `max_fill`, HumanEval/129 `minPath`). Neither `dict` nor nested lists appear in the frozen typing rule's enumerated cases. If this recollection is accurate for Orchid's copies of these tasks, the claim "All 30 signatures... classify cleanly" is false as written, which would force the drop/standby fallback for multiple tasks at once — a case the document has no mechanism for (see B5, and also: only one standby name is ever drawn, so a second simultaneous drop has no defined replacement at all). **This is provisional** — I could not open the actual Hugging Face file to confirm Orchid's exact signatures for these three tasks — but it's concrete enough that it should be checked against the real file before the run, not waved through on the strength of the pre-registration's own "checked at registration time" claim.

Related smaller gap in the same area: C5's coverage checklist —

> "checked at registration time — 100% coverage on `int`, `str`, `list`/`List[int]`/`List[float]`/`List[str]`"

— omits `float`, `bool`, `Tuple[...]`, and `Optional[...]` even though the typing rule two sections earlier defines generation strategies for all four. This is at minimum a copy-paste omission in the control's own checklist, separate from the dict/nested-list question above.

---

## Non-blocking improvements

1. **"Primary aggregate" is defined without an arm.** "Disagreement per (task, arm) = mean pairwise fraction..." followed by "Primary aggregate = mean disagreement across the 30 tasks" reads, taken literally, like a single number averaged over all task×arm cells — but P1 needs `disagreement(A)`, `disagreement(B)`, `disagreement(C)` separately. The intended per-arm aggregation is inferable from context but should be stated explicitly.
2. **"the reverse ordering" (P1, FALSIFIED branch) is never spelled out.** The intended reversal of `A ≥ B > C` is presumably `C ≥ B > A`, but the document doesn't say so, and the asymmetric `≥`/`>` in the original makes the "reverse" less than obvious.
3. **C2/C3/C4's "5 of the 30 tasks"** for the positive-control and calibration-sanity spot checks is never pinned to specific task IDs, leaving the selection to implementer discretion (probably harmless for a sanity check, but not reproducible as stated).
4. **Only one standby task is ever drawn.** If more than one of the 30 sampled tasks needs to be dropped at run time, there is no second replacement and no general rule for drawing further standbys.
5. **The memorization diagnostic doesn't say whether the canonical `solution` field also gets the entry-point rename before the `SequenceMatcher` comparison.** If the canonical solution keeps its original function name while completions use the renamed one, the name mismatch alone will deflate every similarity score by a small, uncontrolled amount, which affects how meaningful the 0.85 threshold actually is.

---

## Verdict

Not clear to run as written. Six items (B1–B6) meet the "two implementers, two different executions or two different verdicts" or "promised-but-uncomputable check" bar, and the fuzzer-coverage claim needs a direct check against the real Orchid file before trusting the "all 30 classify cleanly" assertion — several of these (B2 the floor/ceiling branch, B5/B6 affecting whether P1 reaches SUPPORTED, and the coverage question affecting which 30 tasks actually run) sit on the critical path that determines what the 600 completions are even testing.

Per the house convention on your prior task01 review, I'm delivering this as a standalone review document rather than editing the pre-registration in place — since no model call has been spent on this record yet, folding the fixes back in as a same-file revision (rather than a superseding v2) looks like it would be in scope for you to approve directly, rather than requiring the v2 fork rule that applied to task01.

**Deviations:** none in scope reduction — I did not audit the external dataset itself (no network access), which is called out inline above wherever it's load-bearing; every other check requested was performed against the document's full text.