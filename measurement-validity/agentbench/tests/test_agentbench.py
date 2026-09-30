"""Tests for the scoring and aggregation logic.

These are the invariants that must not silently change: a hedge is only correct
when the case has nothing to find, a forbidden claim voids a run, repeats are
not counted as independent cases, and arms are compared on shared cases only.
"""

import numpy as np
import pytest

from agentbench import aggregate, scoring
from agentbench.schema import CaseRecord, RunRecord


def mk_run(case_id="c1", arm="a", repeat=1, status="found", selected=None,
           evidence=None, text="", suite="s", split="visible"):
    return RunRecord(
        suite=suite, source_project="p", source_path="x", run_id=f"{case_id}-{arm}-{repeat}",
        case_id=case_id, arm=arm, repeat=repeat, split=split,
        extra={"answer": {"status": status, "answer": text,
                          "selected_source_ref": selected,
                          "evidence": evidence or []},
               "tool_events": [{"returned_source_refs": [selected]}] if selected else []},
    )


def mk_case(case_id="c1", expected="found", refs=("ref-1",), required=(), forbidden=(),
            suite="s", split="visible"):
    return CaseRecord(suite=suite, case_id=case_id, split=split, expected_status=expected,
                      expected_source_refs=list(refs), required_terms=list(required),
                      forbidden_terms=list(forbidden))


def test_correct_answer_with_right_source_is_success():
    g = scoring.regrade_run(mk_run(status="found", selected="ref-1"), mk_case())
    assert g["regrade.status_correct"] == 1.0
    assert g["regrade.retrieval_top1"] == 1.0
    assert g["regrade.success"] == 1.0


def test_right_status_wrong_source_is_not_success():
    g = scoring.regrade_run(mk_run(status="found", selected="ref-9"), mk_case())
    assert g["regrade.status_correct"] == 1.0
    assert g["regrade.retrieval_top1"] == 0.0
    assert g["regrade.success"] == 0.0


def test_hedging_on_a_findable_case_is_not_a_correct_abstention():
    """The failure mode the harness exists to catch."""
    g = scoring.regrade_run(mk_run(status="possible_match", selected="ref-1"), mk_case())
    assert g["regrade.hedged"] == 1.0
    assert g["regrade.abstention_correct"] == 0.0
    assert g["regrade.success"] == 0.0


def test_hedging_on_an_unfindable_case_is_correct():
    g = scoring.regrade_run(mk_run(status="not_found", selected=None),
                            mk_case(expected="not_found", refs=()))
    assert g["regrade.abstention_correct"] == 1.0
    assert g["regrade.success"] == 1.0


def test_committing_on_an_unfindable_case_is_an_overclaim():
    g = scoring.regrade_run(mk_run(status="found", selected="ref-1"),
                            mk_case(expected="not_found", refs=()))
    assert g["regrade.overclaim"] == 1.0
    assert g["regrade.success"] == 0.0


def test_forbidden_term_voids_the_run():
    run = mk_run(status="found", selected="ref-1", text="The producer can verify itself.")
    g = scoring.regrade_run(run, mk_case(forbidden=("producer can verify itself",)))
    assert g["regrade.forbidden_claim"] == 1.0
    assert g["regrade.composite"] == 0.0
    assert g["regrade.success"] == 0.0


def test_required_term_coverage_is_fractional():
    run = mk_run(status="found", selected="ref-1", text="independent verification only")
    g = scoring.regrade_run(run, mk_case(required=("independent verification", "fresh verifier")))
    assert g["regrade.required_term_coverage"] == pytest.approx(0.5)


def test_ungraded_when_no_case_definition():
    runs = [mk_run(case_id="unregistered:x")]
    rep = scoring.apply_regrade(runs, [], "s")
    assert rep["n_missing_case_definition"] == 1
    assert runs[0].primary_score is None
    assert runs[0].correct is None


def _frame(rows):
    return aggregate.to_frame(rows)


def test_repeats_do_not_inflate_case_count():
    runs = [mk_run(case_id="c1", repeat=i) for i in (1, 2, 3)]
    for r in runs:
        r.primary_score = 0.5
    s = aggregate.arm_summary(_frame(runs))
    assert s.loc[0, "n_runs"] == 3
    assert s.loc[0, "n_cases"] == 1
    assert s.loc[0, "repeats_per_case"] == 3.0


def test_cluster_bootstrap_ci_is_wider_than_naive_run_level():
    """Resampling cases must not be narrower than pretending runs are independent."""
    rng = np.random.default_rng(0)
    runs = []
    for c in range(8):
        base = rng.uniform(0, 1)
        for rep in range(5):
            r = mk_run(case_id=f"c{c}", repeat=rep)
            r.primary_score = base  # perfectly correlated within case
            runs.append(r)
    df = _frame(runs)
    lo, hi = aggregate._cluster_bootstrap_ci(df, "primary_score")
    naive = df["primary_score"]
    naive_halfwidth = 1.96 * naive.std(ddof=1) / np.sqrt(len(naive))
    assert (hi - lo) / 2 > naive_halfwidth


def test_paired_compare_uses_only_shared_cases():
    runs = []
    for c in ("c1", "c2", "c3"):
        r = mk_run(case_id=c, arm="a"); r.primary_score = 0.2; runs.append(r)
    for c in ("c1", "c2", "c9"):
        r = mk_run(case_id=c, arm="b"); r.primary_score = 0.8; runs.append(r)
    res = aggregate.paired_compare(_frame(runs), "s", "visible", "a", "b")
    assert res["n_shared_cases"] == 2
    assert res["n_cases_only_a"] == 1
    assert res["n_cases_only_b"] == 1
    assert res["mean_diff"] == pytest.approx(0.6)
    assert res["separated"] is True


def test_paired_compare_refuses_single_case():
    runs = [mk_run(case_id="c1", arm="a"), mk_run(case_id="c1", arm="b")]
    for r in runs:
        r.primary_score = 0.5
    res = aggregate.paired_compare(_frame(runs), "s", "visible", "a", "b")
    assert "note" in res
    assert "mean_diff" not in res


def test_grader_inversion_is_detected():
    runs = []
    for c in ("c1", "c2"):
        a = mk_run(case_id=c, arm="a"); a.primary_score = 0.9; a.metrics = {"composite_score": 0.1}
        b = mk_run(case_id=c, arm="b"); b.primary_score = 0.1; b.metrics = {"composite_score": 0.9}
        runs += [a, b]
    out = aggregate.grader_rank_agreement(_frame(runs))
    assert bool(out.loc[0, "ranking_inverted"]) is True
    assert out.loc[0, "best_arm_recorded_grader"] == "b"
    assert out.loc[0, "best_arm_harness_grader"] == "a"


def test_stability_flags_nondeterminism():
    stable = [mk_run(case_id="c1", arm="steady", repeat=i) for i in (1, 2, 3)]
    for r in stable:
        r.primary_score = 0.5
    flaky = [mk_run(case_id="c2", arm="flaky", repeat=i) for i in (1, 2, 3)]
    for r, v in zip(flaky, (0.0, 0.5, 1.0)):
        r.primary_score = v
    out = aggregate.stability(_frame(stable + flaky)).set_index("arm")
    assert out.loc["steady", "frac_cases_unstable"] == 0.0
    assert out.loc["flaky", "frac_cases_unstable"] == 1.0
    assert out.loc["flaky", "max_within_case_range"] == pytest.approx(1.0)
