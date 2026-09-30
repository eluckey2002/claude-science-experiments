# Trigger-rate evaluation: `repo-rules-preflight` description

**Question.** Does the published description reliably cause the skill to be
consulted on requests that need it, and left alone on requests that do not?

## Method

Proxy harness, not the product's selection code. A judge model is shown a
catalog of 18 skills (the target plus 17 real distractors drawn from this
workspace's live catalog, in fixed shuffled order) and one user request, and
asked which skills it would consult. The target's description is the only text
that varies between arms; catalog order, distractor descriptions, queries and
repeat count are held fixed.

- Judge model: `claude-sonnet-5` (not the session model — a Sonnet-class judge was used
  for cost; absolute rates may differ from what an Opus-class selector does)
- Eval set: 50 queries, 25 should-trigger / 25 should-not, written in the
  register of real requests (lowercase, typos, file paths, partial context)
- Negatives are near-misses by construction: they share vocabulary with the
  skill (rules, repo, run, benchmark, evidence) but are owned by another skill
- 3 repeats per query per arm; per-query verdict is the majority of surviving
  repeats
- 10 of 300 calls returned empty (`stop_reason=max_tokens`) and were excluded;
  queries 29 and 30 lost too many calls in one arm and were dropped from the
  paired comparison, leaving n=48

## Arms

| arm | independent variable vs. previous | chars |
|---|---|---|
| v1_published | — (baseline, as published) | 669 |
| v2_exclusion | adds an exclusion clause: not for summarising a rules file | 818 |
| v3_exclusion_orient | v2 plus an orientation / complementarity clause | 1084 |
| v4_trimmed (shipped) | v3 with one redundant trigger clause removed to fit the registry's 1024-char cap | 1016 |

v2 was measured only in the n=20 pilot and dropped: its clause is contained in v3.

## Results (n=48 queries, 3 repeats, complete cases)

| arm | recall (should-trigger) | false-trigger (should-not) | accuracy |
|---|---|---|---|
| v1_published | 0.797 | 0.040 | 0.875 |
| v3_exclusion_orient | 0.868 | 0.000 | 0.938 |
| v4_trimmed (shipped) | 0.882 | 0.000 | 0.938 |

Paired over queries: v3 better on 3, worse on 0, discordant 3, exact
binomial p=0.25. Accuracy delta +0.062, 95% CI
[+0.000, +0.146] (query-level bootstrap, 10k resamples).

**Verdict: within noise.** The direction is favourable and no query regressed,
but with 3 discordant queries the test cannot reject chance — p=0.25 is the
floor for 3 discordant observations, so zero regressions would need >=6
discordant queries before p<0.05 is even reachable (2*0.5^5 = 0.0625; 2*0.5^6 = 0.031). The CI's lower bound sits
at zero: the evidence rules out a meaningful regression, not the null.

Within-query repeat variance was zero on almost every query in every arm — the
judge is highly consistent given the same catalog. The uncertainty here is
between-query (50 queries is a small sample of request space), not sampling.

## What changed, per query

v3 fixed three v1 failures: a "get oriented in this project first" request, a
"change the scoring weights and tell me the benchmark cost" request, and one
keyword-bait negative ("read AGENTS.md and turn it into an onboarding page")
that v1 triggered on and v3 correctly declined.

Residual misses under v3 are all should-trigger requests lost to a competing
skill (`loop-run-card` on "preregister a protocol before I run" and "sanity
check this win-rate claim") or to no selection at all ("a new play session file
showed up, what do I do with it"). Two of those are arguably correct behaviour
by the judge: loading the run-design skill is not wrong, and the real product
allows loading both. The metric scores a query as a miss whenever the target is
absent, even when a sensible companion was chosen — so measured recall is a
lower bound on useful behaviour.

## Limitations

1. Proxy construct. This is not the product's skill-selection path; only
   between-arm differences on an identical catalog are interpretable.
2. Judge is Sonnet-class, the session is Opus-class.
3. Eval-set authorship bias: the same agent wrote the description and the
   queries. The negatives were chosen to be adversarial to the description, but
   an independently authored set would be stronger evidence.
4. Distractor catalog is 18 skills; the live catalog is 51. A fuller catalog
   would raise competition and likely lower absolute recall for every arm.

## Shipped variant

The registry caps `description` at 1024 characters, so v3 (1084) could not be
published. v4 removes one redundant trigger clause to reach 1016 and was then
measured as its own arm on the same 50 queries rather than shipped untested:
it agrees with v3 on every single query (0 discordant of 48), with recall
0.882 vs 0.868 — the same per-query verdicts, one extra surviving repeat.
v4 is what is published; v3 is retained in `variants.json` for reference.
