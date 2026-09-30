# agentbench

An offline benchmark harness for agent workflows. It reads run records your
agents already write, normalizes them into one schema, regrades them against
their case definitions, and compares arms with statistics that respect how the
runs were actually collected.

It does not execute agents. Everything it computes is deterministic and
reproducible from the record files.

## Why

Across the two source trees this was built on, the same four concepts — case,
arm, repeat, split — were spelled four different ways, so no result from one
project could be compared with any other, and each project re-implemented its
own grader. `agentbench` puts one vocabulary and one scorer in front of all of
them.

## Install / run

Requires `pandas`, `numpy`, `scipy`. No other dependencies.

```bash
python -m agentbench --config bench.config.json --out out/
python -m pytest            # 14 tests over the scoring and aggregation logic
```

`bench.config.json`:

```json
{
  "sources": {
    "chat-archaeologist":   "/path/to/chat-archaeologist",
    "evidence-escape-room": "/path/to/evidence-escape-room",
    "coevolution-arena":    "/path/to/adversarial-coevolution-arena"
  },
  "regrade_suites": ["chat-archaeologist"],
  "ledger_root": "/path/to/2248-challenge"
}
```

Paths are read-only; the harness never writes into a source tree.

## Canonical schema

`agentbench/schema.py`. One `RunRecord` per execution:

| field | meaning |
|---|---|
| `suite` | benchmark suite, usually one per project |
| `case_id` | the unit of work |
| `arm` | the thing being compared (configuration / strategy / policy) |
| `repeat` | which re-run of this (case, arm) |
| `split` | `visible` / `holdout` / `unknown` |
| `primary_score` | normalized 0–1 quality score |
| `correct` | binary task success where the suite defines one |
| `latency_s`, `cost_usd`, `input_tokens`, `output_tokens`, `tool_calls` | operational cost |
| `metrics.*` | every scalar grade field the source recorded, kept verbatim |
| `extra` | anything that does not map onto a canonical field — nothing is discarded |

`source_path` is stamped on every record, so any aggregate traces back to the
file it came from.

## Adapters

`agentbench/adapters.py` — one function per project dialect. Adding a project
means writing one function; nothing downstream changes.

- `chat-archaeologist` — `runs.jsonl` schema v3, plus a migration that lifts
  older flat v1 records into the v3 shape. v1 records predate case
  registration, so they land in the `unknown` split and are reported but never
  scored.
- `evidence-escape-room` — one JSON per run; `strategy` is the arm; repeats are
  derived by ordering runs within (case, arm).
- `coevolution-arena` — study summaries with per-execution records; `sentinel`
  and `transfer` phases map to the `holdout` split.
- `2248-policy` — `confirmation.json` / `qualification.json` cells, where
  `policy` is the arm and each cell is one (policy, level, seed) execution with
  a binary `targetReached` outcome. The qualification smoke test runs on
  different seeds than the confirmation, so the two are held in separate
  splits rather than pooled.
- `2248-search-depth` — `corpus.json` rows that carry a `shallow`/`deep` search
  pair. Each row is one board searched both ways, so the arms are paired by
  construction; the outcome is whether a standing resolved at all, and the
  cost is expanded states where the receipt records it.
- `2248-exact-greed` — the RESULT-0036/0037/0038 family. These re-run the same
  (level, percentile) design points on *fresh seeds*, so they are replications,
  not repeats: the arm is the experiment and cases pair on the design point,
  never on the seed.
- `split_sample_measurements` + `aggregate.split_sample_rank_agreement` —
  `measurement.json` receipts score candidates under two disjoint seed
  samples. That registered claim is about rank *stability*, so the statistic is
  a rank correlation between samples, not a difference of means.
- `load_ledger_claims` — the remaining `RESULT-00xx` material is
  claim-verification bookkeeping (closure status, disposition, preregistration)
  rather than arm comparison, so it is inventoried and never folded into the
  arm statistics. The repo's own `tools/verify-experiments.js` gate enforces
  protocol-to-report compliance; the harness does not duplicate it.

## Scoring

`agentbench/scoring.py` recomputes grades from the case definitions alone —
deterministic string matching, no model calls. The point is not to replace a
project's grader but to have a second, independent one: where they disagree,
one is wrong, and grader drift is what silently invalidates a benchmark.

Composite weights are explicit in `WEIGHTS` and documented in the report.
Scoring rules that the test suite pins:

- A hedge is a *correct* abstention only when the case has nothing to find.
- Committing on an unfindable case is an overclaim.
- Right status with the wrong source is not a success.
- A forbidden claim voids the run (composite 0).

## Statistics

`agentbench/aggregate.py`. Two choices matter:

1. **Repeats are not independent.** Every interval is a cluster bootstrap that
   resamples *cases*, not runs. Resampling runs would understate uncertainty by
   roughly the repeat factor. A test asserts the clustered interval is wider
   than the naive run-level one.
2. **Arms are compared paired by case**, on the intersection both arms ran.
   Comparing marginal means across arms with different case sets measures the
   case mix, not the arm. Paired bootstrap CI plus a Wilcoxon signed-rank test
   on the case-level differences; the test is skipped and the reason recorded
   when there are too few non-tied cases.

`grader_rank_agreement` checks whether the source grader and the harness grader
pick the same *winning arm* — correlation is not the question; an ordering
inversion means the benchmark's conclusion depends on which grader was used.

`stability` reports variation across repeats of an identical (case, arm). A
workflow that scores differently on identical input is a measurement problem
before it is a quality problem.

## Outputs

Written to `--out`:

| file | contents |
|---|---|
| `benchmark_report.md` | the rendered report |
| `runs_canonical.csv` | every run in the canonical schema — the join table for any further analysis |
| `arm_summary.csv` | per (suite, split, arm) score, CI, success rate, latency, cost |
| `pairwise_comparisons.csv` | paired arm comparisons with CIs and Wilcoxon p |
| `grader_rank_agreement.csv` | source vs harness grader, with inversion flag |
| `stability.csv` | run-to-run variability |
| `case_difficulty.csv` | per-case scores — which cases the workflow fails |
| `case_definitions.csv` | the registered cases |
| `experiment_ledger.csv` | 2248-challenge claim inventory |
| `split_sample_reliability.csv` | rank stability across disjoint seed samples |
| `grader_agreement.json` | regrade coverage and delta vs recorded scores |

The report's "Coverage and limits" section is generated, not written by hand:
arms with too few cases, pairs with no shared cases, missing cost fields, and
grader inversions are each emitted as an explicit caveat.

## Extending

- **New project**: add a loader to `adapters.ADAPTERS`.
- **New metric**: add it to `metrics` in the adapter; it becomes a
  `metric.<name>` column automatically.
- **Different scoring**: edit `scoring.WEIGHTS` or `regrade_run`; the tests
  pin the behaviour that should not change silently.
- **Live runner**: write canonical `RunRecord`s directly and skip the adapter
  layer — everything downstream already works.
