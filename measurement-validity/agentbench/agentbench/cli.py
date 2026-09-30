"""agentbench pipeline: ingest -> regrade -> aggregate -> report.

    python -m agentbench --config bench.config.json --out out/

The config names where each source tree lives, so the same harness runs on
another machine by editing paths only.
"""

from __future__ import annotations

import argparse
import json
import os

import pandas as pd

from . import adapters, aggregate, report, scoring
from .schema import SCHEMA_VERSION


def build(config: dict) -> dict:
    sources = config["sources"]
    runs, cases = adapters.load_all(sources)

    regrade_reports = []
    for suite in config.get("regrade_suites", []):
        regrade_reports.append(scoring.apply_regrade(runs, cases, suite))

    df = aggregate.to_frame(runs)
    cases_df = pd.DataFrame([c.flat() for c in cases])

    corpus = (
        df.groupby(["source_project", "suite"])
        .agg(n_runs=("run_id", "count"), n_cases=("case_id", "nunique"),
             n_arms=("arm", "nunique"), n_splits=("split", "nunique"),
             completion_rate=("completed", "mean"),
             scored_runs=("primary_score", "count"))
        .reset_index()
    )

    reliability_df = pd.DataFrame()
    if config.get("measurement_root"):
        recs = adapters.split_sample_measurements(config["measurement_root"])
        if recs:
            reliability_df = aggregate.split_sample_rank_agreement(recs)

    ledger_df = pd.DataFrame()
    if config.get("ledger_root"):
        ledger = adapters.load_ledger_claims(config["ledger_root"])
        if ledger:
            ledger_df = pd.DataFrame(ledger)
            keep = ["experiment", "ledger_artifacts", "closure_status", "primary_outcome",
                    "n_claims", "n_claims_pass", "n_deviations", "corpus_verdict",
                    "corpus_reportable", "preregistered", "claim"]
            ledger_df = ledger_df[[c for c in keep if c in ledger_df.columns]]

    arms = aggregate.arm_summary(df)
    pairwise = aggregate.all_pairwise(df)
    stab = aggregate.stability(df)
    case_diff = aggregate.case_difficulty(df)
    grader_ranks = aggregate.grader_rank_agreement(df)

    limits = []
    for _, r in grader_ranks.iterrows():
        if r.get("ranking_inverted"):
            limits.append(
                f"{r['suite']}/{r['split']}: the source grader and the harness grader "
                f"pick different winning arms ({r['best_arm_recorded_grader']} vs "
                f"{r['best_arm_harness_grader']}) — the arm ranking is grader-dependent, "
                "so neither number should be quoted without naming its grader."
            )
    for _, r in arms.iterrows():
        if r["n_cases"] < 5:
            limits.append(
                f"{r['suite']}/{r['split']}/{r['arm']}: only {int(r['n_cases'])} case(s) — "
                "arm estimates here are descriptive, not inferential."
            )
    for _, r in pairwise.iterrows():
        if r.get("n_shared_cases", 0) < 2:
            limits.append(
                f"{r['suite']}/{r['split']}: {r['arm_a']} vs {r['arm_b']} has "
                f"{int(r.get('n_shared_cases', 0))} shared case(s) — not comparable."
            )
    if df["cost_usd"].fillna(0).sum() == 0:
        limits.append("No non-zero cost recorded in any source; cost columns are unusable.")
    n_nocost = int(df["cost_usd"].isna().sum())
    if n_nocost:
        limits.append(f"{n_nocost} of {len(df)} runs carry no cost field.")
    if not limits:
        limits.append("No coverage warnings triggered.")

    return {
        "schema_version": SCHEMA_VERSION,
        "runs": df,
        "cases": case_diff,
        "case_definitions": cases_df,
        "corpus": corpus,
        "arms": arms,
        "pairwise": pairwise,
        "stability": stab,
        "grader_ranks": grader_ranks,
        "reliability": reliability_df,
        "regrade": regrade_reports or None,
        "ledger": ledger_df,
        "limits": limits,
    }


def write(bundle: dict, outdir: str) -> list[str]:
    os.makedirs(outdir, exist_ok=True)
    written = []
    tables = {
        "runs_canonical.csv": bundle["runs"],
        "arm_summary.csv": bundle["arms"],
        "pairwise_comparisons.csv": bundle["pairwise"],
        "stability.csv": bundle["stability"],
        "grader_rank_agreement.csv": bundle.get("grader_ranks"),
        "split_sample_reliability.csv": bundle.get("reliability"),
        "case_difficulty.csv": bundle["cases"],
        "case_definitions.csv": bundle["case_definitions"],
        "experiment_ledger.csv": bundle["ledger"],
    }
    for name, tbl in tables.items():
        if tbl is None or (hasattr(tbl, "empty") and tbl.empty):
            continue
        path = os.path.join(outdir, name)
        tbl.to_csv(path, index=False)
        written.append(path)
    rp = os.path.join(outdir, "benchmark_report.md")
    with open(rp, "w") as fh:
        fh.write(report.render(bundle))
    written.append(rp)
    if bundle.get("regrade"):
        gp = os.path.join(outdir, "grader_agreement.json")
        with open(gp, "w") as fh:
            json.dump(bundle["regrade"], fh, indent=2)
        written.append(gp)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agentbench")
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default="out")
    args = ap.parse_args(argv)
    config = json.load(open(args.config))
    bundle = build(config)
    for p in write(bundle, args.out):
        print(p)
    return bundle


if __name__ == "__main__":
    main()
