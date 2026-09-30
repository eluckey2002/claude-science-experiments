"""Aggregation and arm comparison.

Two statistical choices matter here and are deliberate:

1. Repeats of the same case are *not* independent observations. Every interval
   is a cluster bootstrap that resamples cases, not runs — resampling runs would
   understate uncertainty roughly by the repeat factor.
2. Arms are compared *paired by case* on the intersection of cases both arms
   ran. Comparing marginal means across arms that ran different case sets
   measures the case mix, not the arm.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

RNG_SEED = 20260920


def to_frame(runs) -> pd.DataFrame:
    df = pd.DataFrame([r.flat() for r in runs])
    if df.empty:
        return df
    for col in ("primary_score", "latency_s", "cost_usd", "input_tokens",
                "output_tokens", "tool_calls"):
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _cluster_bootstrap_ci(df: pd.DataFrame, value: str, cluster: str = "case_id",
                          n_boot: int = 5000, alpha: float = 0.05) -> tuple[float, float]:
    """95% CI for the mean of `value`, resampling whole clusters."""
    sub = df[[cluster, value]].dropna()
    if sub.empty:
        return (np.nan, np.nan)
    groups = [g[value].to_numpy() for _, g in sub.groupby(cluster)]
    if len(groups) < 2:
        return (np.nan, np.nan)
    rng = np.random.default_rng(RNG_SEED)
    idx = rng.integers(0, len(groups), size=(n_boot, len(groups)))
    means = np.array([np.concatenate([groups[i] for i in row]).mean() for row in idx])
    return (float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))


def arm_summary(df: pd.DataFrame, metric: str = "primary_score") -> pd.DataFrame:
    """One row per (suite, split, arm)."""
    rows = []
    for (suite, split, arm), g in df.groupby(["suite", "split", "arm"], dropna=False):
        lo, hi = _cluster_bootstrap_ci(g, metric)
        rows.append({
            "suite": suite,
            "split": split,
            "arm": arm,
            "n_runs": len(g),
            "n_cases": g["case_id"].nunique(),
            "repeats_per_case": round(len(g) / max(g["case_id"].nunique(), 1), 2),
            "completion_rate": g["completed"].mean() if "completed" in g else np.nan,
            "score_mean": g[metric].mean(),
            "score_ci_lo": lo,
            "score_ci_hi": hi,
            "success_rate": g["correct"].astype("float").mean() if g["correct"].notna().any() else np.nan,
            "latency_s_mean": g["latency_s"].mean(),
            "latency_s_p90": g["latency_s"].quantile(0.90) if g["latency_s"].notna().any() else np.nan,
            "cost_usd_mean": g["cost_usd"].mean(),
            "cost_usd_total": g["cost_usd"].sum(min_count=1),
            "tool_calls_mean": g["tool_calls"].mean(),
            "tokens_out_mean": g["output_tokens"].mean(),
        })
    out = pd.DataFrame(rows)
    return out.sort_values(["suite", "split", "arm"]).reset_index(drop=True)


def stability(df: pd.DataFrame, metric: str = "primary_score") -> pd.DataFrame:
    """Run-to-run variability within (case, arm) — the flakiness of the workflow."""
    rows = []
    for (suite, arm), g in df.groupby(["suite", "arm"], dropna=False):
        per = g.groupby("case_id")[metric].agg(["count", "mean", "std", "min", "max"])
        per = per[per["count"] > 1]
        if per.empty:
            rows.append({"suite": suite, "arm": arm, "n_cases_with_repeats": 0,
                         "mean_within_case_sd": np.nan, "frac_cases_unstable": np.nan,
                         "max_within_case_range": np.nan})
            continue
        rng_ = (per["max"] - per["min"])
        rows.append({
            "suite": suite,
            "arm": arm,
            "n_cases_with_repeats": int(len(per)),
            "mean_within_case_sd": float(per["std"].mean()),
            "frac_cases_unstable": float((rng_ > 1e-9).mean()),
            "max_within_case_range": float(rng_.max()),
        })
    return pd.DataFrame(rows).sort_values(["suite", "arm"]).reset_index(drop=True)


def paired_compare(df: pd.DataFrame, suite: str, split: str, arm_a: str, arm_b: str,
                   metric: str = "primary_score", n_boot: int = 10000) -> dict:
    """Paired arm comparison on the case intersection. Positive diff favours arm_b."""
    sub = df[(df["suite"] == suite) & (df["split"] == split)]
    a = sub[sub["arm"] == arm_a].groupby("case_id")[metric].mean()
    b = sub[sub["arm"] == arm_b].groupby("case_id")[metric].mean()
    shared = sorted(set(a.index) & set(b.index))
    result = {
        "suite": suite, "split": split, "arm_a": arm_a, "arm_b": arm_b,
        "metric": metric, "n_shared_cases": len(shared),
        "n_cases_only_a": len(set(a.index) - set(b.index)),
        "n_cases_only_b": len(set(b.index) - set(a.index)),
    }
    if len(shared) < 2:
        result["note"] = "insufficient shared cases for a paired comparison"
        return result
    av, bv = a.loc[shared].to_numpy(), b.loc[shared].to_numpy()
    d = bv - av
    rng = np.random.default_rng(RNG_SEED)
    boot = rng.choice(d, size=(n_boot, len(d)), replace=True).mean(axis=1)
    result.update({
        "mean_a": float(av.mean()),
        "mean_b": float(bv.mean()),
        "mean_diff": float(d.mean()),
        "diff_ci_lo": float(np.quantile(boot, 0.025)),
        "diff_ci_hi": float(np.quantile(boot, 0.975)),
        "n_cases_b_better": int((d > 0).sum()),
        "n_cases_a_better": int((d < 0).sum()),
        "n_cases_tied": int((d == 0).sum()),
    })
    # Wilcoxon signed-rank on the case-level differences (non-parametric, paired).
    try:
        from scipy.stats import wilcoxon
        nz = d[d != 0]
        if len(nz) >= 5:
            stat, p = wilcoxon(nz)
            result["wilcoxon_p"] = float(p)
            result["wilcoxon_n_nonzero"] = int(len(nz))
        else:
            result["wilcoxon_p"] = None
            result["wilcoxon_note"] = f"only {len(nz)} non-tied cases; test not run"
    except Exception as exc:
        result["wilcoxon_error"] = str(exc)
    ci_excludes_zero = result["diff_ci_lo"] > 0 or result["diff_ci_hi"] < 0
    result["separated"] = bool(ci_excludes_zero)
    return result


def all_pairwise(df: pd.DataFrame, metric: str = "primary_score") -> pd.DataFrame:
    rows = []
    for (suite, split), g in df.groupby(["suite", "split"]):
        arms = sorted(g["arm"].dropna().unique())
        for i, a in enumerate(arms):
            for b in arms[i + 1:]:
                rows.append(paired_compare(df, suite, split, a, b, metric=metric))
    return pd.DataFrame(rows)


def grader_rank_agreement(df: pd.DataFrame, recorded_col: str = "metric.composite_score",
                          harness_col: str = "primary_score") -> pd.DataFrame:
    """Do the source grader and the harness grader rank the arms the same way?

    Correlation alone is not the question — a benchmark only misleads when the
    two graders disagree about *which arm wins*. This reports the rank
    correlation and, more importantly, flags ordering inversions.
    """
    if recorded_col not in df.columns:
        return pd.DataFrame()
    rows = []
    for (suite, split), g in df.groupby(["suite", "split"]):
        sub = g[[recorded_col, harness_col, "arm", "case_id"]].dropna(
            subset=[recorded_col, harness_col])
        if sub.empty or sub["arm"].nunique() < 1:
            continue
        try:
            from scipy.stats import spearmanr
            rho = float(spearmanr(sub[recorded_col], sub[harness_col]).statistic)
        except Exception:
            rho = float("nan")
        per_arm = sub.groupby("arm")[[recorded_col, harness_col]].mean()
        inverted = False
        best_recorded = per_arm[recorded_col].idxmax()
        best_harness = per_arm[harness_col].idxmax()
        if per_arm.shape[0] > 1:
            inverted = best_recorded != best_harness
        rows.append({
            "suite": suite,
            "split": split,
            "n_runs": len(sub),
            "n_arms": int(per_arm.shape[0]),
            "spearman_rho": rho,
            "mean_abs_delta": float((sub[recorded_col] - sub[harness_col]).abs().mean()),
            "best_arm_recorded_grader": best_recorded,
            "best_arm_harness_grader": best_harness,
            "ranking_inverted": inverted,
        })
    return pd.DataFrame(rows)


def split_sample_rank_agreement(records: list[dict]) -> pd.DataFrame:
    """Does candidate *ranking* hold across two disjoint seed samples?

    The registered claim in a measurement receipt of this shape is about rank
    stability, so the statistic is a rank correlation between the two samples'
    per-candidate means — not a difference of means.
    """
    rows = []
    for rec in records:
        m = pd.DataFrame(rec["measurements"])
        if not {"candidateName", "sample", "score"} <= set(m.columns):
            continue
        piv = m.pivot_table(index="candidateName", columns="sample",
                            values="score", aggfunc="mean")
        samples = list(piv.columns)
        if len(samples) < 2:
            continue
        a, b = piv[samples[0]].to_numpy(), piv[samples[1]].to_numpy()
        try:
            from scipy.stats import spearmanr, pearsonr
            rho = float(spearmanr(a, b).statistic)
            r = float(pearsonr(a, b).statistic)
        except Exception:
            rho = r = float("nan")
        # Per-candidate within-sample spread, to say whether a single seed
        # could stand in for the sample mean.
        sd = m.groupby(["candidateName", "sample"])["score"].std().mean()
        spread = float(piv.max(axis=1).max() - piv.min(axis=1).min())
        rows.append({
            "experiment": rec["experiment"],
            "metric": rec["metric"],
            "n_candidates": int(piv.shape[0]),
            "n_measurements": rec["n_measurements"],
            "samples": "/".join(str(s) for s in samples),
            "spearman_rank_rho": rho,
            "pearson_r": r,
            "mean_within_sample_sd": float(sd),
            "between_candidate_spread": spread,
            "sd_to_spread_ratio": float(sd / spread) if spread else float("nan"),
        })
    return pd.DataFrame(rows)


def case_difficulty(df: pd.DataFrame, metric: str = "primary_score") -> pd.DataFrame:
    """Per-case mean across arms — which cases the workflow fails on."""
    g = df.groupby(["suite", "split", "case_id"]).agg(
        n_runs=("run_id", "count"),
        n_arms=("arm", "nunique"),
        score_mean=(metric, "mean"),
        score_min=(metric, "min"),
        score_max=(metric, "max"),
        success_rate=("correct", lambda s: s.astype("float").mean()),
    ).reset_index()
    return g.sort_values(["suite", "score_mean"]).reset_index(drop=True)
