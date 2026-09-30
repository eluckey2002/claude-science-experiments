# Agent workflow benchmark report
_Generated 2026-09-20T20:52:26-05:00 by agentbench v1._
## Corpus
| source_project | suite | n_runs | n_cases | n_arms | n_splits | completion_rate | scored_runs |
|---|---|---|---|---|---|---|---|
| 2248-challenge | 2248-exact-greed | 384 | 16 | 3 | 1 | 1.00 | 384 |
| 2248-challenge | 2248-policy | 454 | 227 | 2 | 2 | 1.00 | 454 |
| 2248-challenge | 2248-search-depth | 416 | 208 | 2 | 1 | 1.00 | 416 |
| Adverserial Bot! | chat-archaeologist | 76 | 16 | 2 | 3 | 1.00 | 75 |
| Adverserial Bot! | coevolution-arena | 43 | 14 | 4 | 2 | 0.81 | 43 |
| Adverserial Bot! | evidence-escape-room | 12 | 1 | 2 | 1 | 0.75 | 9 |

## Arm summary
Score is the harness-owned primary metric for each suite; intervals are 95% cluster bootstrap over cases (repeats of a case resampled together).
| suite | split | arm | n_runs | n_cases | repeats_per_case | completion_rate | score_mean | score_ci_lo | score_ci_hi | success_rate | latency_s_mean | latency_s_p90 | cost_usd_mean | cost_usd_total | tool_calls_mean | tokens_out_mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2248-exact-greed | visible | RESULT-0036 | 128 | 16 | 8.000 | 1.000 | 0.234 | 0.062 | 0.438 | 0.234 |  |  |  |  |  |  |
| 2248-exact-greed | visible | RESULT-0037 | 128 | 16 | 8.000 | 1.000 | 0.250 | 0.070 | 0.453 | 0.250 |  |  |  |  |  |  |
| 2248-exact-greed | visible | RESULT-0038 | 128 | 16 | 8.000 | 1.000 | 0.250 | 0.070 | 0.453 | 0.250 |  |  |  |  |  |  |
| 2248-policy | holdout | handmade | 225 | 225 | 1.000 | 1.000 | 0.960 | 0.933 | 0.982 | 0.960 | 0.689 | 1.113 |  |  |  |  |
| 2248-policy | holdout | reference | 225 | 225 | 1.000 | 1.000 | 0.987 | 0.969 | 1.000 | 0.987 | 0.102 | 0.145 |  |  |  |  |
| 2248-policy | visible | handmade | 2 | 2 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.849 | 0.965 |  |  |  |  |
| 2248-policy | visible | reference | 2 | 2 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.138 | 0.152 |  |  |  |  |
| 2248-search-depth | visible | deep | 208 | 208 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |  |  |  |  |  |  |
| 2248-search-depth | visible | shallow | 208 | 208 | 1.000 | 1.000 | 0.899 | 0.856 | 0.938 | 0.899 |  |  |  |  |  |  |
| chat-archaeologist | holdout | lexical | 15 | 5 | 3.000 | 1.000 | 0.150 | 0.150 | 0.150 | 0.000 | 0.048 | 0.047 | 0.000 | 0.000 | 1.000 | 0.000 |
| chat-archaeologist | unknown | baseline | 1 | 1 | 1.000 | 1.000 |  |  |  |  | 5.739 | 5.739 | 0.000 | 0.000 | 1.000 | 535.000 |
| chat-archaeologist | visible | baseline | 30 | 10 | 3.000 | 1.000 | 0.533 | 0.425 | 0.655 | 0.200 | 4.939 | 7.536 | 0.000 | 0.010 | 0.800 | 618.833 |
| chat-archaeologist | visible | lexical | 30 | 10 | 3.000 | 1.000 | 0.300 | 0.180 | 0.420 | 0.000 | 0.035 | 0.048 | 0.000 | 0.000 | 1.000 | 0.000 |
| coevolution-arena | holdout | baseline-v0 | 6 | 6 | 1.000 | 1.000 | 0.667 | 0.333 | 1.000 | 0.667 | 16.359 | 20.122 |  |  | 1.167 | 343.667 |
| coevolution-arena | holdout | candidate-v0 | 6 | 6 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 21.521 | 35.669 |  |  | 1.333 | 405.333 |
| coevolution-arena | visible | baseline-v0 | 6 | 4 | 1.500 | 1.000 | 0.500 | 0.000 | 1.000 | 0.500 | 16.230 | 18.697 |  |  | 1.167 | 355.333 |
| coevolution-arena | visible | candidate-v0 | 6 | 4 | 1.500 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 23.967 | 32.472 |  |  | 1.500 | 473.000 |
| coevolution-arena | visible | candidate-v1-retry | 3 | 3 | 1.000 | 1.000 | 0.667 | 0.000 | 1.000 | 0.667 | 17.753 | 19.397 |  |  | 1.000 | 382.667 |
| coevolution-arena | visible | public-shakeout | 16 | 4 | 4.000 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 | 6.844 | 15.495 |  |  | 0.917 | 339.875 |
| evidence-escape-room | visible | baseline | 7 | 1 | 7.000 | 0.857 | 0.591 |  |  | 0.000 | 13.700 | 24.148 | 0.001 | 0.005 | 8.143 | 1346.143 |
| evidence-escape-room | visible | challenger | 5 | 1 | 5.000 | 0.600 | 0.612 |  |  | 0.000 | 12.638 | 22.048 | 0.001 | 0.003 | 9.800 | 1055.400 |

## Paired arm comparisons
Paired by case on the intersection both arms ran. `mean_diff` is arm_b − arm_a; `separated` means the 95% bootstrap CI excludes zero.
| suite | split | arm_a | arm_b | metric | n_shared_cases | n_cases_only_a | n_cases_only_b | mean_a | mean_b | mean_diff | diff_ci_lo | diff_ci_hi | n_cases_b_better | n_cases_a_better | n_cases_tied | wilcoxon_p | wilcoxon_note | separated | wilcoxon_n_nonzero | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2248-exact-greed | visible | RESULT-0036 | RESULT-0037 | primary_score | 16 | 0 | 0 | 0.234 | 0.250 | 0.016 | -0.023 | 0.063 | 2.000 | 2.000 | 12.000 |  | only 4 non-tied cases; test not run | False |  |  |
| 2248-exact-greed | visible | RESULT-0036 | RESULT-0038 | primary_score | 16 | 0 | 0 | 0.234 | 0.250 | 0.016 | -0.016 | 0.055 | 2.000 | 1.000 | 13.000 |  | only 3 non-tied cases; test not run | False |  |  |
| 2248-exact-greed | visible | RESULT-0037 | RESULT-0038 | primary_score | 16 | 0 | 0 | 0.250 | 0.250 | 0.000 | -0.031 | 0.031 | 2.000 | 2.000 | 12.000 |  | only 4 non-tied cases; test not run | False |  |  |
| 2248-policy | holdout | handmade | reference | primary_score | 225 | 0 | 0 | 0.960 | 0.987 | 0.027 | 0.009 | 0.049 | 6.000 | 0.000 | 219.000 | 0.031 |  | True | 6.000 |  |
| 2248-policy | visible | handmade | reference | primary_score | 2 | 0 | 0 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 2.000 |  | only 0 non-tied cases; test not run | False |  |  |
| 2248-search-depth | visible | deep | shallow | primary_score | 208 | 0 | 0 | 1.000 | 0.899 | -0.101 | -0.144 | -0.062 | 0.000 | 21.000 | 187.000 | 0.000 |  | True | 21.000 |  |
| chat-archaeologist | visible | baseline | lexical | primary_score | 10 | 0 | 0 | 0.533 | 0.300 | -0.233 | -0.360 | -0.065 | 2.000 | 8.000 | 0.000 | 0.076 |  | True | 10.000 |  |
| coevolution-arena | holdout | baseline-v0 | candidate-v0 | primary_score | 6 | 0 | 0 | 0.667 | 1.000 | 0.333 | 0.000 | 0.667 | 2.000 | 0.000 | 4.000 |  | only 2 non-tied cases; test not run | False |  |  |
| coevolution-arena | visible | baseline-v0 | candidate-v0 | primary_score | 4 | 0 | 0 | 0.500 | 1.000 | 0.500 | 0.000 | 1.000 | 2.000 | 0.000 | 2.000 |  | only 2 non-tied cases; test not run | False |  |  |
| coevolution-arena | visible | baseline-v0 | candidate-v1-retry | primary_score | 3 | 1 | 0 | 0.333 | 0.667 | 0.333 | 0.000 | 1.000 | 1.000 | 0.000 | 2.000 |  | only 1 non-tied cases; test not run | False |  |  |
| coevolution-arena | visible | baseline-v0 | public-shakeout | primary_score | 0 | 4 | 4 |  |  |  |  |  |  |  |  |  |  |  |  | insufficient shared cases for a paired comparison |
| coevolution-arena | visible | candidate-v0 | candidate-v1-retry | primary_score | 3 | 1 | 0 | 1.000 | 0.667 | -0.333 | -1.000 | 0.000 | 0.000 | 1.000 | 2.000 |  | only 1 non-tied cases; test not run | False |  |  |
| coevolution-arena | visible | candidate-v0 | public-shakeout | primary_score | 0 | 4 | 4 |  |  |  |  |  |  |  |  |  |  |  |  | insufficient shared cases for a paired comparison |
| coevolution-arena | visible | candidate-v1-retry | public-shakeout | primary_score | 0 | 3 | 4 |  |  |  |  |  |  |  |  |  |  |  |  | insufficient shared cases for a paired comparison |
| evidence-escape-room | visible | baseline | challenger | primary_score | 1 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | insufficient shared cases for a paired comparison |

## Run-to-run stability
Variation across repeats of the same (case, arm). A workflow that scores differently on identical input is a measurement problem before it is a quality problem.
| suite | arm | n_cases_with_repeats | mean_within_case_sd | frac_cases_unstable | max_within_case_range |
|---|---|---|---|---|---|
| 2248-exact-greed | RESULT-0036 | 16 | 0.078 | 0.188 | 1.000 |
| 2248-exact-greed | RESULT-0037 | 16 | 0.083 | 0.188 | 1.000 |
| 2248-exact-greed | RESULT-0038 | 16 | 0.102 | 0.250 | 1.000 |
| 2248-policy | handmade | 0 |  |  |  |
| 2248-policy | reference | 0 |  |  |  |
| 2248-search-depth | deep | 0 |  |  |  |
| 2248-search-depth | shallow | 0 |  |  |  |
| chat-archaeologist | baseline | 10 | 0.022 | 0.200 | 0.267 |
| chat-archaeologist | lexical | 15 | 0.000 | 0.000 | 0.000 |
| coevolution-arena | baseline-v0 | 2 | 0.000 | 0.000 | 0.000 |
| coevolution-arena | candidate-v0 | 2 | 0.000 | 0.000 | 0.000 |
| coevolution-arena | candidate-v1-retry | 0 |  |  |  |
| coevolution-arena | public-shakeout | 4 | 0.577 | 1.000 | 1.000 |
| evidence-escape-room | baseline | 1 | 0.094 | 1.000 | 0.210 |
| evidence-escape-room | challenger | 1 | 0.160 | 1.000 | 0.300 |

## Grader ranking agreement
Whether the source grader and the harness grader pick the same winning arm. An inversion means the benchmark's conclusion depends on which grader is used.
| suite | split | n_runs | n_arms | spearman_rho | mean_abs_delta | best_arm_recorded_grader | best_arm_harness_grader | ranking_inverted |
|---|---|---|---|---|---|---|---|---|
| chat-archaeologist | holdout | 15 | 1 |  | 0.190 | lexical | lexical | False |
| chat-archaeologist | visible | 60 | 2 | 0.485 | 0.193 | lexical | baseline | True |

## Grader agreement
The harness recomputes grades from the case definitions alone and compares them with the score the source runner recorded.
- **chat-archaeologist**: regraded 75 runs; 75 comparable to a recorded score; mean |Δ| = 0.193, max |Δ| = 0.525; 1 case definitions missing.

## Split-sample reliability
For measurement receipts that score candidates under two disjoint seed samples, the registered claim is about rank stability, so the statistic is a rank correlation between the samples — not a difference of means. `sd_to_spread_ratio` is the within-sample noise against the spread between candidates: small means one seed can stand in for the sample.
| experiment | metric | n_candidates | n_measurements | samples | spearman_rank_rho | pearson_r | mean_within_sample_sd | between_candidate_spread | sd_to_spread_ratio |
|---|---|---|---|---|---|---|---|---|---|
| RESULT-0021 | terminal achievable score before target stopping | 53 | 6360 | a/b | 1.000 | 0.999 | 6689.087 | 219384.667 | 0.030 |

## Hardest cases
| suite | split | case_id | n_runs | n_arms | score_mean | score_min | score_max | success_rate |
|---|---|---|---|---|---|---|---|---|
| 2248-exact-greed | visible | L10:p0.25 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L10:p0.5 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L31:p0.25 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L31:p0.5 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L53:p0.25 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L53:p0.5 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L53:p0.75 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L54:p0.25 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L54:p0.5 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L54:p0.75 | 24 | 3 | 0.000 | 0.000 | 0.000 | 0.000 |
| 2248-exact-greed | visible | L54:p1 | 24 | 3 | 0.083 | 0.000 | 1.000 | 0.083 |
| 2248-exact-greed | visible | L31:p0.75 | 24 | 3 | 0.250 | 0.000 | 1.000 | 0.250 |
| 2248-exact-greed | visible | L10:p0.75 | 24 | 3 | 0.667 | 0.000 | 1.000 | 0.667 |
| 2248-exact-greed | visible | L31:p1 | 24 | 3 | 0.958 | 0.000 | 1.000 | 0.958 |
| 2248-exact-greed | visible | L53:p1 | 24 | 3 | 0.958 | 0.000 | 1.000 | 0.958 |

## Experiment ledger (2248-challenge)
Claim-verification records rather than arm comparisons: reported as an inventory, excluded from the statistics above.
| experiment | ledger_artifacts | closure_status | primary_outcome | n_claims | n_claims_pass | n_deviations | corpus_verdict | corpus_reportable | preregistered | claim |
|---|---|---|---|---|---|---|---|---|---|---|
| RESULT-0020 |  |  |  |  |  |  |  |  |  |  |
| RESULT-0021 | measurement |  |  |  |  |  |  |  |  | structural candidate ranking is stable across two disjoint seed samples and single-seed reliability is sufficient for candidate differentiation |
| RESULT-0022 |  |  |  |  |  |  |  |  |  |  |
| RESULT-0023 |  |  |  |  |  |  |  |  |  |  |
| RESULT-0024 |  |  |  |  |  |  |  |  |  |  |
| RESULT-0026 | confirmation,qualification |  |  |  |  |  |  |  |  |  |
| RESULT-0029 | corpus |  |  |  |  |  | INCONCLUSIVE | True | True |  |
| RESULT-0030 | corpus |  |  |  |  |  |  | True | True |  |
| RESULT-0031 | corpus |  |  |  |  |  |  | True | True |  |
| RESULT-0032 | corpus |  |  |  |  |  |  | True | True |  |
| RESULT-0033 | corpus |  |  |  |  |  |  | True | True |  |
| RESULT-0034 | corpus |  |  |  |  |  |  | True | True |  |
| RESULT-0035 | closure,corpus | CLOSED | MAP_CORPUS_INCONCLUSIVE | 9.00 | 9.00 | 0.00 |  | True | True |  |
| RESULT-0036 | closure,corpus | UNVERIFIED |  | 13.00 | 5.00 | 1.00 |  | True | True |  |
| RESULT-0037 | closure,corpus,qualification | UNVERIFIED |  | 12.00 | 5.00 | 1.00 |  | True | True |  |
| RESULT-0038 | closure,corpus,qualification | CLOSED | INCONCLUSIVE | 12.00 | 12.00 | 0.00 |  | True | True |  |

## Coverage and limits
- chat-archaeologist/visible: the source grader and the harness grader pick different winning arms (lexical vs baseline) — the arm ranking is grader-dependent, so neither number should be quoted without naming its grader.
- 2248-policy/visible/handmade: only 2 case(s) — arm estimates here are descriptive, not inferential.
- 2248-policy/visible/reference: only 2 case(s) — arm estimates here are descriptive, not inferential.
- chat-archaeologist/unknown/baseline: only 1 case(s) — arm estimates here are descriptive, not inferential.
- coevolution-arena/visible/baseline-v0: only 4 case(s) — arm estimates here are descriptive, not inferential.
- coevolution-arena/visible/candidate-v0: only 4 case(s) — arm estimates here are descriptive, not inferential.
- coevolution-arena/visible/candidate-v1-retry: only 3 case(s) — arm estimates here are descriptive, not inferential.
- coevolution-arena/visible/public-shakeout: only 4 case(s) — arm estimates here are descriptive, not inferential.
- evidence-escape-room/visible/baseline: only 1 case(s) — arm estimates here are descriptive, not inferential.
- evidence-escape-room/visible/challenger: only 1 case(s) — arm estimates here are descriptive, not inferential.
- coevolution-arena/visible: baseline-v0 vs public-shakeout has 0 shared case(s) — not comparable.
- coevolution-arena/visible: candidate-v0 vs public-shakeout has 0 shared case(s) — not comparable.
- coevolution-arena/visible: candidate-v1-retry vs public-shakeout has 0 shared case(s) — not comparable.
- evidence-escape-room/visible: baseline vs challenger has 1 shared case(s) — not comparable.
- 1297 of 1385 runs carry no cost field.
