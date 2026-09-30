# Experiments and tests, 20-29 Sept 2026

Compiled from the 15 earlier sessions in this project. Status key: **Ran** = we executed it with model calls or code; **Ran (re-analysis)** = we re-computed results from your repos' existing run data; **Audit** = checked documents, code or git state; **Built** = tool or harness; **Designed, not run** = protocol exists, no calls made; **Stopped** = started and halted.

Literature reviews (the ~15 published word-effect studies, the CMB-0.1 paper) are not listed as our experiments.


## Benchmark harness (agentbench)

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-20 | Built agentbench v1 across four run-record dialects | Built + tested | 131 runs, 31 cases; 14 unit tests | All tests pass; canonical CSV, report and figure produced end to end |
| 09-20 | Extended agentbench v2 with 2248-ledger adapters | Built + tested | 1,385 runs across six suites | Three new adapters; corpus, README, tests and figure updated |
| 09-20 | Chat-archaeologist grader regrade | Ran (re-analysis) | 75 runs; 10 visible + 5 holdout cases | Recorded grader ranked the always-hedging lexical arm above baseline (0.475 vs 0.339) although baseline got status right 28/30 and lexical 0/45. Regrading against case definitions reverses the ranking |
| 09-20 | Grader ranking-inversion detector | Built + tested | 14 tests | ranking_inverted flag added and confirmed on the chat-archaeologist case |
| 09-20 | Adversarial-coevolution-arena replication | Ran (re-analysis) | 5 studies; 27 executions in study-001 | Candidate beats baseline on sentinel (1.00 vs 0.00) and generation-1 (1.00 vs 0.33); both pass 4/4 on transfer. Replicates the study's own no-transfer result |
| 09-20 | Evidence-escape-room comparability check | Ran (re-analysis) | 12 runs, 1 case | Not comparable: single case, 3 of 12 runs errored |
| 09-20 | Arena public-shakeout stability check | Ran (re-analysis) | Repeats of one identical case | Different score on every repeat (full 0-1 range): a measurement problem, not a quality result |
| 09-20 | 2248 reference vs handmade policy (RESULT-0026) | Ran (re-analysis) | 450 cells, paired on 225 boards | Reference 0.987 vs handmade 0.960 (diff +0.027, CI 0.009-0.049); 6 wins, 219 ties, 0 losses |
| 09-20 | 2248 deep vs shallow search | Ran (re-analysis) | 208 boards, both depths | Deep solves 208/208 vs 187/208 (diff 0.101, CI 0.063-0.144) at 3.7x the states expanded |
| 09-20 | 2248 ranking stability across seed samples (RESULT-0021) | Ran (re-analysis) | 6,360 measurements, 53 candidates | Spearman rho 0.9995 between halves; registered claim holds |
| 09-20 | 2248 exact-greed fresh-seed replication (RESULT-0036/37/38) | Ran (re-analysis) | 3 batches x 16 design points | Win rate replicates (0.234/0.250/0.250); exactComplete not comparable across batches |

## Skill trigger evaluation

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-20 | repo-rules-preflight description trigger eval, n=20 | Ran | 20 queries x 3 repeats | Unresolved: 2 discordant queries (p=0.50) |
| 09-20 | repo-rules-preflight description trigger eval, n=50 | Ran | 50 queries x 3 repeats | Reworded description 45/48 vs original 42/48: fixed 3, broke none; within noise at this n. Judge repeat variance near zero |

## Small League and loop-lab audit

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-21 | Independent recomputation of Small League successor contrasts | Ran (re-analysis) | 96 candidates, 2,304 outcomes, 5 contrasts x 4 blocks | No contrast keeps a consistent non-zero sign across all four blocks under any measure |
| 09-21 | Sealed-bank resolution analysis | Ran (re-analysis) | 48 candidates x 24 cases, Tasks 4 and 5 | 14/24 and 20/24 cases identical for every candidate; only 2 discriminating cases per task; effective bank width about 2 |
| 09-21 | Descriptor equivalence-class test | Ran (re-analysis) | 13 and 14 multi-member descriptor groups | P(same behaviour | same descriptor) = 0.60 / 0.32; descriptors and behaviours cross-cut |
| 09-21 | What the discriminating cases test | Ran (re-analysis) | 4 discriminating cases | All four are malformed-input validation cases |
| 09-21 | Constant-policy gameability probe | Ran | 24 expected outputs per bank | Best constant policy scores 1/24; banks are not gameable |
| 09-21 | Qualification proxy vs sealed score | Ran (re-analysis) | 48 candidates per task | Spearman +0.050 (Task 4), -0.029 (Task 5): proxy carries no rank information |
| 09-21 | Comparison band vs full pool re-check | Ran (re-analysis) | Band covers 46 of 48 | Same two discriminating cases either way |
| 09-21 | Authoring-gate '22 of 24' recomputation | Ran (re-analysis) | 24 candidates per task | Holds only under the band threshold; plain rule gives 14 and 20 |
| 09-21 | Resolution-screen mutation study (loop-lab PR #20) | Ran | Broken screen variants + 4 successor banks | Caught every broken variant; flagged all four banks as unable to discriminate; adopted as a warning |
| 09-21 | Selector follow-up study (loop-lab PR #21) | Stopped before run | 0 model calls | Closed because banks lack resolution; 8 reopening conditions written down |
| 09-21 | FINDINGS.md claim check | Ran | 33 claims | All 33 verify; checker exits 0 |
| 09-21 | measure-preflight skill build and validation | Built + tested | Real pool + 3 hand fixtures | Reproduces every number above; later corrected (criterion C2) |
| 09-21 | Runner cold-review defect audit | Audit | 27 files, ~9,000 lines JS; 12 logged failures | All 12 share one root cause: nothing ties a run's actual conditions to its declared protocol |
| 09-21 | Random-mutation control wording check | Audit | 256 seeds | 162/256 'met or exceeded'; one README says 'beat 63.3%' (ties folded into wins) |
| 09-21 | 2248 experiment ledger census | Audit | 16 records on main | 3 supported, 7 inconclusive, 1 falsified, 2 unverified, 1 map-corpus inconclusive, 1 closed; one empty stub |
| 09-21 | Git branch and worktree audits (2248 and loop-lab) | Audit | ~65 branches | Six unpushed 2248 branches carrying records past RESULT-0038 found; user pushed them |
| 09-21 | Scar ledger audit and update (PR #24) | Audit + change | 13 -> 15 scars | Merged after auditor corrections |

## Agent failure-modes taxonomy

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-21 | Fresh-eyes audit of the lexicon (v2.2) | Audit | 23 modes; 11 citations checked | Ten blocking defects, incl. confusable clusters with identical facets and 4 citation defects |
| 09-21 | Counter-audit of proposed new codes | Audit | 10 proposed codes | About three net additions survive; 'computation error' rejected |
| 09-21 | Inter-rater agreement pilot | Ran | 18 trace windows from 7 sessions | 17/18 agreement, kappa 0.486; only 1 window held a codable failure, so the pilot sets up the method rather than measuring the scheme |
| 09-21 | Detector-coverage literature survey | Ran | 74 queries -> 509 records -> 327 screened | 12 of 23 modes have something wireable to a runtime detector; 11 have none |
| 09-21 | Prevention-shortlist filter and CLAUDE.md rule drafts | Built | 10 rules; v1 then v2 (938 words) | v2 has trigger + reframe + rationale; not yet tried on real traces |

## Word-impact ('simple') study

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-22 | Duration-parser task (task 01) | Designed, not run | 3 arms x 10 reps planned | Spec, probes and pre-registration written and audited; shelved because one task cannot support a claim about a word |
| 09-26 | Four-arm Orchid pre-registration | Designed, not run | 30 tasks x 4 arms x 5 reps = 600 calls | Two independent reviewers: 'not fundable as written; fixable before first model call' |
| 09-26 | Two-arm Orchid pre-registration | Designed, not run | 30 tasks x 2 arms x 5 reps = 300 calls | Round-1 reviewers: not fundable yet; fuzz probes seeded with Python's non-deterministic hash() |
| 09-26 | Orchid dataset structure check | Ran | Sample rows vs 164 tasks | Prompt + hidden tests usable as the base for the arms |
| 09-26 | Sonnet vs Haiku cost estimate | Ran | 30 completions | About $0.15-0.20 Sonnet vs $0.07-0.10 Haiku |

## Web-design 'modern' word

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-26 | Coffee-shop landing page pilot | Ran | 2 arms x 3 runs = 6 pages | Without the word, runs disagreed on font, width, radius, header; with 'modern', all three agreed |
| 09-26 | Cross-model extension | Ran | 4 models x 2 arms x 3 runs = 24 pages (~$2.60) | Body font moved from serif (Georgia, 8/12) to sans-serif in 12/12 'modern' runs on all four models |
| 09-26 | Word-screen cost model, re-priced on measured tokens | Ran | 24 pages; extrapolated | Ten words across Sonnet/Opus/Fable about $6,900 list ($3,400 batch) |
| 09-26 | Thin vs thick brief, Bitcoin app | Ran | 2 x 3 x 5 = 30 pages, Sonnet 5 (~$7) | Brief choice already matched the thick spec's defaults, so the manipulation had little room to act |
| 09-27 | Thin vs thick brief, v2 (four conditions) | Ran | 4 conditions x 5 pages | Thin: blur 0/5 without 'modern', 5/5 with it. Thick: 0/5 both ways; the style guide suppresses the word |
| 09-28 | Design fingerprint extraction pipeline | Built + tested | 14 regex-parsed properties | Used to score all pages above |
| 09-28 | Vendor design-claim audit (Anthropic release pages) | Ran | 5 primary pages | Explicit design claims in Opus 4.5, narrowing afterwards, none by Opus 5.5 |
| 09-27 | Coherence test and recipe-dictionary test | Designed, not run | 10 pages; ~$6 for 10 descriptors | Waiting on go-ahead |
| 09-26 | GitHub rule-file collector smoke test | Stopped | 2 attempts | Stopped by user; collection moved to Claude Code on your machine |

## Multi-agent skill setup

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-26 | Fresh-eyes audits of corpus-librarian skill, rounds 1-3 | Ran | 3 sub-agent audits | Rounds 1-2 found real defects, fixed; round 3 was a false positive from a depth-capped auditor |
| 09-26 | Auditor prompt and relay-gate patches | Built | 1 profile edit, 1 skill publish | Live; depth-capped claims now reported as unverifiable |

## Image-description words

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-28 | Stimulus set for 'describe in one word' study | Built | 26 images (11 originals, 11 light, 4 off-centre) | 260-call pilot proposed; waiting on model choice |

## Critic-evaluator loop

| Date | Experiment | Status | Scale | Result |
|---|---|---|---|---|
| 09-29 | Judge calibration | Ran | 12 seeded flaws x 2 documents x 2 judges | Both judges 12/12 on seeded doc, 0/12 on original |
| 09-29 | Rereading vs outside-information critic loop | Stopped | 6 cells, 3 rounds planned | Round 1 done for 5 of 6 cells; round 2 never graded, so no arm comparison yet |
| 09-29 | JEV router vs Codex baseline benchmark | Designed, not run | ~20 Codex tasks proposed | Design only |

## Open items

**Needs a decision from you**
1. Image-description pilot: 260 calls on one model; pick the model (Sonnet proposed).
2. Coherence test and recipe-dictionary test for 'modern': go-ahead to write the protocol and run (~$6 for the dictionary).
3. Critic-evaluator loop: whether to score the 5 completed round-1 cells in a fresh session (and fill the missing sixth).

**Can wait**
1. Two-arm Orchid pre-registration: fix the hash() seeding, then a second review round before any calls.
2. CLAUDE.md rule set v2: small pilot in one repo against real traces.
3. Inter-rater agreement: re-run on a sample that contains enough codable failures to measure kappa.
4. JEV router vs Codex benchmark: build the frozen task set.

**On your side (Claude Code)**
1. Rule-file collector runs from your machine; the kit is written.
