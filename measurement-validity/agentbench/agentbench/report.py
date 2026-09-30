"""Markdown report rendering."""

from __future__ import annotations

import datetime as _dt

import pandas as pd


def _md(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    """Render a DataFrame as a GitHub markdown table (no external dependency)."""
    if df is None or df.empty:
        return "_(none)_\n"
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else floatfmt.format(v))
        else:
            d[c] = d[c].map(lambda v: "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v))
    cols = list(d.columns)
    lines = ["| " + " | ".join(cols) + " |",
             "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, row in d.iterrows():
        lines.append("| " + " | ".join(str(row[c]).replace("|", "\\|") for c in cols) + " |")
    return "\n".join(lines) + "\n"


def render(bundle: dict) -> str:
    runs = bundle["runs"]
    L = []
    L.append("# Agent workflow benchmark report\n")
    L.append(f"_Generated {_dt.datetime.now().astimezone().isoformat(timespec='seconds')} "
             f"by agentbench v{bundle['schema_version']}._\n")

    L.append("## Corpus\n")
    L.append(_md(bundle["corpus"], "{:.2f}"))

    L.append("\n## Arm summary\n")
    L.append("Score is the harness-owned primary metric for each suite; intervals are "
             "95% cluster bootstrap over cases (repeats of a case resampled together).\n")
    L.append(_md(bundle["arms"]))

    L.append("\n## Paired arm comparisons\n")
    L.append("Paired by case on the intersection both arms ran. `mean_diff` is "
             "arm_b − arm_a; `separated` means the 95% bootstrap CI excludes zero.\n")
    L.append(_md(bundle["pairwise"]))

    L.append("\n## Run-to-run stability\n")
    L.append("Variation across repeats of the same (case, arm). A workflow that scores "
             "differently on identical input is a measurement problem before it is a "
             "quality problem.\n")
    L.append(_md(bundle["stability"]))

    if bundle.get("grader_ranks") is not None and not bundle["grader_ranks"].empty:
        L.append("\n## Grader ranking agreement\n")
        L.append("Whether the source grader and the harness grader pick the same winning "
                 "arm. An inversion means the benchmark's conclusion depends on which "
                 "grader is used.\n")
        L.append(_md(bundle["grader_ranks"]))

    if bundle.get("regrade") is not None:
        L.append("\n## Grader agreement\n")
        L.append("The harness recomputes grades from the case definitions alone and "
                 "compares them with the score the source runner recorded.\n")
        for r in bundle["regrade"]:
            L.append(f"- **{r['suite']}**: regraded {r['n_regraded']} runs; "
                     f"{r['n_compared']} comparable to a recorded score; "
                     f"mean |Δ| = {r['mean_abs_delta_vs_recorded']:.3f}, "
                     f"max |Δ| = {r['max_abs_delta_vs_recorded']:.3f}; "
                     f"{r['n_missing_case_definition']} case definitions missing.\n")

    if bundle.get("reliability") is not None and not bundle["reliability"].empty:
        L.append("\n## Split-sample reliability\n")
        L.append("For measurement receipts that score candidates under two disjoint seed "
                 "samples, the registered claim is about rank stability, so the statistic "
                 "is a rank correlation between the samples — not a difference of means. "
                 "`sd_to_spread_ratio` is the within-sample noise against the spread "
                 "between candidates: small means one seed can stand in for the sample.\n")
        L.append(_md(bundle["reliability"]))

    L.append("\n## Hardest cases\n")
    L.append(_md(bundle["cases"].head(15)))

    if bundle.get("ledger") is not None and not bundle["ledger"].empty:
        L.append("\n## Experiment ledger (2248-challenge)\n")
        L.append("Claim-verification records rather than arm comparisons: reported as "
                 "an inventory, excluded from the statistics above.\n")
        L.append(_md(bundle["ledger"], "{:.2f}"))

    L.append("\n## Coverage and limits\n")
    for line in bundle["limits"]:
        L.append(f"- {line}\n")
    return "".join(L)
