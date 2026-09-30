# Why Small League's successor could not have detected a population effect

Recomputed from `studies/small-league-successor/CANDIDATE-SEALED-MATRIX.csv` — 96 candidates,
48 sealed-case columns, 2,304 candidate-case outcomes. No new runs; no data modified.

## The hypothesis I tested, and its failure

I proposed that the study's primary outcome — sealed pass count of one committed finalist per arm —
structurally discards what a population produces, and that a coverage-style measure over the arm's
whole output would reveal an effect the finalist measure had thrown away.

**It would not have.** Recomputing all five contrasts under three different outcome measures:

| Measure | What it asks |
|---|---|
| `finalist_sealed` | the study's own measure: the one committed finalist's pass count |
| `best_of_6` | the best candidate the arm produced, whether or not it was selected |
| `union_of_6` | how many sealed cases the arm's six candidates passed *between them* |

Taking each measure separately, **no contrast keeps the same non-zero sign across all four blocks**
— the criterion the study itself used to conclude that no factor had a positive effect. Swapping the
finalist measure for either population measure does not change that verdict. Union coverage differs
from the finalist count by at most one case anywhere in the dataset. The population measure finds
nothing because there is nothing at that resolution to find.

Within a single block the three measures often agree with each other — Task 4 block 2 gives
`state_GP_GG` = -1 under all three, and Task 5 block 2 gives `state_SP_SG` = +1 and `interaction`
= +1 under all three. That agreement is expected rather than informative: the three measures are
computed from the same six candidates and differ only in which of them they read, so they are
near-collinear. Cross-measure agreement inside one block is not replication; replication is
agreement across blocks, which is what the table above fails to show.

## What the data shows instead

The sealed banks are almost entirely non-discriminating.

| | Task 4 | Task 5 |
|---|---:|---:|
| Sealed cases | 24 | 24 |
| Passed or failed by **all 48** candidates | 14 | 20 |
| Vary across candidates at all | 10 | 4 |
| **Pass rate between 10% and 90%** | **2** | **2** |
| Distinct behaviours among 48 candidates | 8 | 8 |
| Distinct descriptor vectors among 48 candidates | 15 | 16 |
| Range of sealed pass counts | 8–17 | 19–23 |

Two cases per task carry essentially all the discriminating signal. In Task 4 those are case 10
(16 of 48 pass) and case 13 (39 of 48). In Task 5, case 13 (20 of 48) and case 21 (19 of 48).
Every other varying case is flipped by one or two candidates out of forty-eight.

So the reported contrasts of 0 and ±1 are not a small effect measured noisily. They are the readout
of about two binary cases per artifact. The 24-case bank has an effective width closer to 2.

**And the descriptor vectors already resolve roughly twice as much as the bank does** — 15–16
distinct `{boundary, dependency, semantic}` vectors versus 8 distinct sealed-bank behaviours over
the same 48 candidates. The population is visible in descriptor space and invisible in outcome
space. In one arm-block (Task 4, block 2, GP) all six candidates share a single bank signature:
six candidates, one measurable behaviour.

## What this means for a measurable population

The binding constraint is not the outcome measure, the finalist-selection step, or the block count.
It is that **the measurement surface has almost no resolution left.** No statistic computed on these
banks can separate the arms, because the candidates are not separable on these banks.

This also explains the study history rather than contradicting it. Pilot-002's headroom attempts 1
and 2 saturated outright — Haiku passing 24/24/24 — and W2 was stopped by its own stop rule. The
saturation problem was identified five days before the successor ran, correctly named as headroom,
and the successor then ran on banks with two discriminating cases each.

A population needs a fitness surface with room in it. Two axes worth noting:

1. **Case difficulty has to be calibrated against the candidate distribution, not the reference.**
   A case that the reference passes and every candidate also passes contributes nothing. The
   existing headroom check tests whether a bank is saturated *in aggregate*; per-case pass rates
   across the candidate pool are the finer instrument, and they are computable from data already
   collected.
2. ~~**The descriptor vector is the higher-resolution signal you already record.**~~
   **Retracted — see the next section.** The descriptor partition and the behaviour partition
   cross-cut rather than nest, so the count of 15–16 positions is not a finer reading of the same
   thing.

## Follow-up test: is the descriptor trustworthy? No.

The recommendation above was tested directly and fails. Taking every group of candidates that share
an identical `{boundary, dependency, semantic}` vector, and asking whether they behave identically
on the sealed bank:

| | Task 4 | Task 5 |
|---|---:|---:|
| Descriptor groups with more than one member | 13 | 14 |
| Groups whose members **differ** on the bank | **7** | **10** |
| P(same behaviour given same descriptor) | 0.60 | 0.32 |
| P(same descriptor given same behaviour) | 0.14 | 0.08 |
| Widest sealed-score spread inside one descriptor group | **9 cases** | 3 cases |

Descriptor groups pool both blocks within a task. That is legitimate here because the sealed bank
is identical within an artifact, so two candidates from different blocks are graded on the same
questions — but it means a group can span independent model draws.

The worst case is stark: in Task 4, descriptor `(3, 1, 3)` holds six candidates scoring
**8, 15, 15, 17, 17, 17** out of 24. The weakest candidate in the entire task-4 pool shares a
descriptor with three of the strongest. In Task 5, descriptor `(4, 4, 1)` holds eight candidates
with five distinct behaviours, scoring 19 to 22.

Both conditional probabilities are low, which is the decisive detail. The descriptor is not a
coarsening of behaviour and behaviour is not a coarsening of the descriptor — **the two partitions
cross-cut.** So "15–16 descriptor positions versus 8 bank behaviours" does not mean the descriptor
sees more; it means the two measures disagree about which candidates are alike. Spearman
correlations between each descriptor component and sealed pass count are weak throughout
(|rho| <= 0.33, and three of six are below 0.11).

This is precisely the case the study's own `PORTFOLIO-GEOMETRY-AUDIT` declined to claim. That audit
found 8 aggregate-vector collision groups with none holding more than one exact behaviour — on the
predecessor's *admitted-challenge* evidence — and explicitly made "no claim aggregate vectors
suffice for future or unseen artifacts." On the successor's sealed banks, they do not. The audit's
caveat was correct and is now tested.

Practical consequence: the descriptor is safe as a *diversity coordinate* (it is allowed to be
orthogonal to quality) but unsafe as an *equivalence class*. Any rule that treats equal descriptors
as interchangeable candidates can discard a 17-case candidate in favour of an 8-case one. The
successor's corrected retention rule already avoids this by falling back to byte-distinctness; this
analysis quantifies why that correction mattered.

## What the study actually measured

The degenerate-baseline probe was run next — the Arm R question applied to a measure rather than a
policy: can the bank be passed without doing the task?

**It cannot.** All 24 expected outputs are distinct in both banks, so the best input-ignoring
constant policy scores 1 of 24. The banks are not gameable, and the second failure class does not
apply to them. That worry is removed.

The probe surfaced something sharper. Classifying every case by the outcome its expected output
declares:

| Task 4 | n | informative | discriminating |
|---|---:|---:|---:|
| `SELECTED` | 16 | 5 | **0** |
| `NONE` | 2 | 1 | **0** |
| `INVALID_INPUT` | 6 | 4 | **2** |

| Task 5 | n | informative | discriminating |
|---|---:|---:|---:|
| `SCHEDULED` | 9 | 0 | **0** |
| `CYCLE` | 3 | 0 | **0** |
| `INVALID_INPUT` | 12 | 4 | **2** |

**Every case that separates candidates is a malformed-input validation case.** All four of them:

| Case | Outcome | Error objects required | Families | Pass rate |
|---|---|---:|---|---:|
| `task4-case-10` | `INVALID_INPUT` | 7 | boundary+dependency | 0.33 |
| `task4-case-13` | `INVALID_INPUT` | 10 | boundary+dependency | 0.81 |
| `task5-case-13` | `INVALID_INPUT` | 1 | boundary | 0.42 |
| `task5-case-21` | `INVALID_INPUT` | 4 | boundary+dependency | 0.40 |

The six non-`INVALID_INPUT` cases that vary at all do so at a pass rate of 0.979 — 47 of 48 — which
is one broken candidate failing, not a comparison. Every `SCHEDULED` and `CYCLE` case in Task 5 is
passed or failed by all 48 candidates alike.

So the study is named as an ablation of specialized roles and portfolio retention on a next-task
selector and a release-wave planner. **What it measured is exhaustive enumeration of validation
errors on malformed input** — path and code, every field, exactly. Selection quality, wave
planning, dependency reasoning and cycle detection contributed no comparative signal at all.

The `semantic` family is the clearest casualty. It appears in 17 of Task 4's 24 cases and 8 of
Task 5's, and it is present in none of the four discriminating cases; in Task 5 all eight semantic
cases carry zero information. The three-family design does not predict discriminating power.

This is the study's own scar class, instantiated on its newest run. `meaningful-distinctness-omitted`
records the transition `goal-to-measurement`, with the bypass path "proxy outcomes pass while the
stated goal remains unmeasured." That is exactly what happened here, a month after the scar was
written, and the scar's `owner_disposition` is still `OPEN`.

## Caveats

- This is a re-analysis of one study's recorded outcomes. It says the successor's banks could not
  detect an arm difference; it says nothing about whether such a difference exists.
- `union_of_6` and `best_of_6` are my constructions, not pre-registered measures. They are reported
  here as a sensitivity analysis on the study's conclusion, not as replacement outcomes.
- The per-case pass rates pool all four arms and both generations within a task (n=48). Pooling is
  what makes a case's discriminating power visible; it is not an arm comparison.
- Descriptor-vector counts are of the `vector` field as recorded. I did not verify that two equal
  vectors imply equal behaviour — the study's own retrospective found 3 of 4 equal-vector groups
  later diverged, which cuts in the same direction as the finding above.
- Nothing here was verified by re-executing the runner.
