# Small League: why the nulls, and the durable fixes

Findings from a post-hoc analysis of `small-league-successor`, 2026-09-20. Every
load-bearing number here is registered in `claims.json` and re-derived by
`verify_claims.py` against a loop-lab checkout; run it before trusting any figure
below. Statements not so registered are marked *(argued)* and are the author's
inference, not a measurement.

```
python3 verify_claims.py claims.json --repo <loop-lab checkout>   # 32 pass, 0 fail, 1 argued
```

## The result being explained

The successor 2×2 ablation of specialized roles and portfolio retention closed as
"no factor showed a stable positive effect." The design and reporting were sound —
matched budgets, blind verifier, finalist committed before the sealed bank opened,
activation gate declared in advance and fired. The null is correctly stated. What
follows is why the comparison could not have found an effect even if one existed.

## Finding 1 — the sealed banks had almost no resolving power

Across the 48-candidate pool, **2 of 24 cases discriminate** on each task (pool
pass-rate in [0.10, 0.90]); 14 and 20 cases are passed or failed by all 48
candidates alike; the 48 candidates collapse to **8 distinct behaviours** each. A
24-case bank with 2 discriminating cases is a 2-case bank for the comparison. The
reported ±1 contrasts were the readout of those two cases.

## Finding 2 — the discriminating cases test validation, not search

Every discriminating case on both tasks declares outcome `INVALID_INPUT` —
exhaustive enumeration of malformed-input errors. Zero `SELECTED`, `NONE`,
`SCHEDULED` or `CYCLE` cases discriminate. Specialized roles and retained
portfolios are search machinery; whether they have a mechanism on
validation-error enumeration is **an open question** (registered as
`mechanism-question`), and the falsifying test is a 2×2 on a bank whose
discriminating cases test search quality. No position is warranted until that runs.

## Finding 3 — the descriptor is not an equivalence class

The `{boundary, dependency, semantic}` vector cross-cuts behaviour:
P(same behaviour | same descriptor) = 0.60 (Task 4), 0.32 (Task 5); the converse
0.14 and 0.08. One Task-4 descriptor group holds six candidates scoring 8 to 17.
Safe as a diversity coordinate; unsafe for any dedup/retention/selection rule.

## Finding 4 — the qualification proxy predicted nothing

This is the mechanism of the whole failure. The non-sealed diagnostic that
qualification used was saturated: **38 of 48** candidates scored a perfect
diagnostic rate on Task 4 (their sealed scores span 8–17), **45 of 48** on Task 5
(sealed 19–23). Spearman correlation between diagnostic rate and sealed pass count
is **+0.05** and **−0.03**. Qualification passed because the proxy called every
candidate equally good, and the proxy tracked nothing.

---

## The bug: `headroom-check.mjs` scores probes, not the pool

The gate scores a fixed set of ~6 planted candidates (reference, a thrower,
baseline, two pilot-001 finalists, a tiebreak defect) and passes when the strongest
sits below 24/24 and the baseline is above 0. Attempt 4 passed on **a repair pass
at 16/24, baseline 14/24, ceiling 24** — three points.

It never scores the pool of candidates the comparison will actually run on, so it
cannot see that those candidates cluster into 8 behaviours on 2 cases. The property
it checks (a probe below the ceiling) and the property the comparison needs (spread
across the candidate pool) are different, and the first does not imply the second.

**This is not "one word in a stop condition"** — a slogan used earlier and
retracted. `HEADROOM-CHECK.md` already split repair headroom from discovery
headroom; the concept was not missing. What is missing is that headroom was
operationalized over probes rather than over the candidate pool.

## The asymmetry behind it

loop-lab mutation-tests its *checks* rigorously — check-card garbage tests record
real mutations and red counts; `calibrate.mjs` runs six controls with known
dispositions before every run. It has **never mutation-tested a case bank.** That
asymmetry is the structural gap. The remedy is the discipline already owned,
pointed at the bank instead of the checks.

## The fixes

**Code — widen `headroom-check.mjs`.** Score the candidate pool through the gate,
count cases whose pool pass-rate lands in the discriminating band [0.10, 0.90], and
require a minimum. (Patch and negative tests ship alongside this document.) Under
this gate, **22 of 24 cases fail on each task** — because only 2 discriminate. A
weaker rule ("passed by ≥1 and failed by ≥1 candidate") fails 14 and 20; the band
threshold is what produces the 22 figure, and it is the one to use.

**Process — an authoring-time probe gate, inside the seal.** Before sealing,
require every case to be passed by at least one probe implementation and failed by
at least one, where the probes are deliberately-flawed variants spanning the quality
range candidates are expected to occupy — not a broken baseline against a perfect
reference. Runs before any model call; costs three or four hand-written probes.

**Discipline — read declarations before outputs when reviewing an experiment
cold.** Research brief before RESULTS.md; the repo rulebook before analyzing
anything it governs. Three of this analysis's own early errors came from critiquing
the study against an objective inferred from a machine summary instead of read from
`RESEARCH-BRIEF.md`. The `repo-rules-preflight` skill mechanizes the rulebook half.

## What is NOT claimed

- That any arm difference exists. Findings 1–4 establish the banks could not detect
  one; they say nothing about whether one is there.
- That the treatments are ineffective. Finding 2's mechanism question is open.
- That the successor violated its protocol. It did not; the gap is upstream, in a
  bank property no declared check covered.
