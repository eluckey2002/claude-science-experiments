# Measurement validity

**Question.** Can the instruments we use to compare agents tell a real difference from a grader quirk, noise, or a test too easy to separate anyone?

**Where it stands.** Six instrument failures have been found across three projects (a grader rewarding the wrong arm, unrepeatable scores, a test bank that could not separate candidates, a proxy that did not predict the sealed score, descriptors that did not match behaviour, too few cases to rate). Two are fully diagnosed and guarded in loop-lab's scar ledger; the rest are measured but not yet explained. A central register of instrument failures (with a denominator, cause, prevention and whether it was caught before or after spend) is planned for this program and is not built yet.

## Contents

- `agentbench/` : scorekeeping harness (case, arm, repeat, split) and its tests
- `agentbench-runs/` : canonical run table, reports and figures from the six suites; `2248_result_ledger.csv` is the 2248-challenge RESULT-00xx ledger, not a list of work done here
- `small-league/` : sealed-bank resolution analysis, claims manifest and its checker

## Experiments

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 2026-09-20 | Built agentbench v1 across four run-record dialects | Built + tested | 131 runs, 31 cases; 14 unit tests | All tests pass; canonical CSV, report and figure produced end to end |
| 2026-09-20 | Extended agentbench v2 with 2248-ledger adapters | Built + tested | 1,385 runs across six suites | Three new adapters; corpus, README, tests and figure updated |
| 2026-09-20 | Chat-archaeologist grader regrade | Ran (re-analysis) | 75 runs; 10 visible + 5 holdout cases | Recorded grader ranked the always-hedging lexical arm above baseline (0.475 vs 0.339) although baseline got status right 28/30 and lexical 0/45. Regrading against case definitions reverses the ranking |
| 2026-09-20 | Grader ranking-inversion detector | Built + tested | 14 tests | ranking_inverted flag added and confirmed on the chat-archaeologist case |
| 2026-09-20 | Adversarial-coevolution-arena replication | Ran (re-analysis) | 5 studies; 27 executions in study-001 | Candidate beats baseline on sentinel (1.00 vs 0.00) and generation-1 (1.00 vs 0.33); both pass 4/4 on transfer. Replicates the study's own no-transfer result |
| 2026-09-20 | Evidence-escape-room comparability check | Ran (re-analysis) | 12 runs, 1 case | Not comparable: single case, 3 of 12 runs errored |
| 2026-09-20 | Arena public-shakeout stability check | Ran (re-analysis) | Repeats of one identical case | Different score on every repeat (full 0-1 range): a measurement problem, not a quality result |
| 2026-09-20 | 2248 reference vs handmade policy (RESULT-0026) | Ran (re-analysis) | 450 cells, paired on 225 boards | Reference 0.987 vs handmade 0.960 (diff +0.027, CI 0.009-0.049); 6 wins, 219 ties, 0 losses |
| 2026-09-20 | 2248 deep vs shallow search | Ran (re-analysis) | 208 boards, both depths | Deep solves 208/208 vs 187/208 (diff 0.101, CI 0.063-0.144) at 3.7x the states expanded |
| 2026-09-20 | 2248 ranking stability across seed samples (RESULT-0021) | Ran (re-analysis) | 6,360 measurements, 53 candidates | Spearman rho 0.9995 between halves; registered claim holds |
| 2026-09-20 | 2248 exact-greed fresh-seed replication (RESULT-0036/37/38) | Ran (re-analysis) | 3 batches x 16 design points | Win rate replicates (0.234/0.250/0.250); exactComplete not comparable across batches |
| 2026-09-21 | Independent recomputation of Small League successor contrasts | Ran (re-analysis) | 96 candidates, 2,304 outcomes, 5 contrasts x 4 blocks | No contrast keeps a consistent non-zero sign across all four blocks under any measure |
| 2026-09-21 | Sealed-bank resolution analysis | Ran (re-analysis) | 48 candidates x 24 cases, Tasks 4 and 5 | 14/24 and 20/24 cases identical for every candidate; only 2 discriminating cases per task; effective bank width about 2 |
| 2026-09-21 | Descriptor equivalence-class test | Ran (re-analysis) | 13 and 14 multi-member descriptor groups | P(same behaviour / same descriptor) = 0.60 / 0.32; descriptors and behaviours cross-cut |
| 2026-09-21 | What the discriminating cases test | Ran (re-analysis) | 4 discriminating cases | All four are malformed-input validation cases |
| 2026-09-21 | Constant-policy gameability probe | Ran | 24 expected outputs per bank | Best constant policy scores 1/24; banks are not gameable |
| 2026-09-21 | Qualification proxy vs sealed score | Ran (re-analysis) | 48 candidates per task | Spearman +0.050 (Task 4), -0.029 (Task 5): proxy carries no rank information |
| 2026-09-21 | Comparison band vs full pool re-check | Ran (re-analysis) | Band covers 46 of 48 | Same two discriminating cases either way |
| 2026-09-21 | Authoring-gate '22 of 24' recomputation | Ran (re-analysis) | 24 candidates per task | Holds only under the band threshold; plain rule gives 14 and 20 |
| 2026-09-21 | Resolution-screen mutation study (loop-lab PR #20) | Ran | Broken screen variants + 4 successor banks | Caught every broken variant; flagged all four banks as unable to discriminate; adopted as a warning |
| 2026-09-21 | Selector follow-up study (loop-lab PR #21) | Stopped before run | 0 model calls | Closed because banks lack resolution; 8 reopening conditions written down |
| 2026-09-21 | FINDINGS.md claim check | Ran | 33 claims | All 33 verify; checker exits 0 |
| 2026-09-21 | measure-preflight skill build and validation | Built + tested | Real pool + 3 hand fixtures | Reproduces every number above; later corrected (criterion C2) |
| 2026-09-21 | Runner cold-review defect audit | Audit | 27 files, ~9,000 lines JS; 12 logged failures | All 12 share one root cause: nothing ties a run's actual conditions to its declared protocol |
| 2026-09-21 | Random-mutation control wording check | Audit | 256 seeds | 162/256 'met or exceeded'; one README says 'beat 63.3%' (ties folded into wins) |
| 2026-09-21 | 2248 experiment ledger census | Audit | 16 records on main | 3 supported, 7 inconclusive, 1 falsified, 2 unverified, 1 map-corpus inconclusive, 1 closed; one empty stub |
| 2026-09-21 | Git branch and worktree audits (2248 and loop-lab) | Audit | ~65 branches | Six unpushed 2248 branches carrying records past RESULT-0038 found; user pushed them |
| 2026-09-21 | Scar ledger audit and update (PR #24) | Audit + change | 13 -> 15 scars | Merged after auditor corrections |
