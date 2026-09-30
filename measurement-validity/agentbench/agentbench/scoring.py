"""Independent regrading.

The point of regrading is not to replace the project's own grader but to have a
*second, harness-owned* grader computed from the case definitions alone. Where
the two disagree, one of them is wrong — and grader drift is the failure mode
that silently invalidates a benchmark over time.

Scoring here is deterministic and string-based: no model is called, so the
harness produces the same numbers on every machine and every replay.
"""

from __future__ import annotations

from typing import Any

from .schema import CaseRecord, RunRecord

# A status is "committed" when the agent asserts something about the corpus.
COMMITTED = {"found", "contradicted"}
# ...and "hedged" when it declines to commit.
HEDGED = {"not_found", "possible_match", "insufficient_evidence", None}

# Composite weights. Explicit and documented so the number is interpretable;
# change them here and every report follows.
WEIGHTS = {
    "status_correct": 0.35,
    "retrieval_top1": 0.30,
    "required_term_coverage": 0.20,
    "evidence_grounded": 0.15,
}


def _norm(s: Any) -> str:
    return " ".join(str(s or "").lower().split())


def _answer_text(answer: dict) -> str:
    parts = [answer.get("answer") or "", answer.get("abstention_reason") or ""]
    for ev in answer.get("evidence") or []:
        if isinstance(ev, dict):
            parts.append(ev.get("quote") or "")
    return _norm(" ".join(parts))


def _retrieved_refs(tool_events: list[dict]) -> list[str]:
    refs: list[str] = []
    for ev in tool_events or []:
        if not isinstance(ev, dict):
            continue
        for ref in ev.get("returned_source_refs") or []:
            if ref not in refs:
                refs.append(ref)
    return refs


def regrade_run(run: RunRecord, case: CaseRecord | None) -> dict[str, Any]:
    """Recompute grades for one chat-archaeologist run from its case."""
    answer = run.extra.get("answer") or {}
    status = answer.get("status")
    expected = (case.expected_status if case else None) or run.extra.get("expected_status")
    text = _answer_text(answer)
    exp_refs = list(case.expected_source_refs) if case else []
    retrieved = _retrieved_refs(run.extra.get("tool_events") or [])
    selected = answer.get("selected_source_ref")

    status_correct = bool(status == expected)
    committed = status in COMMITTED
    should_commit = expected in COMMITTED
    # Correct abstention: hedged exactly when the case has nothing to find.
    abstention_correct = bool(committed == should_commit)

    if exp_refs:
        top1 = float(selected in exp_refs)
        top3 = float(any(r in exp_refs for r in retrieved[:3]))
        recall = float(any(r in exp_refs for r in retrieved))
    else:
        # No gold reference (a not_found case): retrieval is scored as
        # "correctly selected nothing".
        top1 = float(selected in (None, ""))
        top3 = top1
        recall = top1

    req = [t for t in (case.required_terms if case else [])]
    hits = [t for t in req if _norm(t) in text]
    req_cov = (len(hits) / len(req)) if req else (1.0 if status_correct else 0.0)

    forb = [t for t in (case.forbidden_terms if case else []) if _norm(t) in text]

    evidence = [e for e in (answer.get("evidence") or []) if isinstance(e, dict)]
    if evidence:
        grounded = sum(
            1 for e in evidence if e.get("source_ref") in retrieved or e.get("quote")
        )
        grounded_frac = grounded / len(evidence)
    else:
        grounded_frac = 1.0 if not committed else 0.0

    composite = (
        WEIGHTS["status_correct"] * status_correct
        + WEIGHTS["retrieval_top1"] * top1
        + WEIGHTS["required_term_coverage"] * req_cov
        + WEIGHTS["evidence_grounded"] * grounded_frac
    )
    if forb:
        composite = 0.0  # a forbidden claim voids the run

    # Strict task success: said the right thing AND pointed at the right source.
    if should_commit:
        success = bool(status_correct and top1 == 1.0 and not forb)
    else:
        success = bool(status_correct and not forb)

    return {
        "regrade.status_correct": float(status_correct),
        "regrade.abstention_correct": float(abstention_correct),
        "regrade.retrieval_top1": top1,
        "regrade.retrieval_top3": top3,
        "regrade.retrieval_recall": recall,
        "regrade.required_term_coverage": req_cov,
        "regrade.forbidden_claim": float(bool(forb)),
        "regrade.evidence_grounded": grounded_frac,
        "regrade.hedged": float(not committed),
        "regrade.overclaim": float(committed and not should_commit),
        "regrade.composite": composite,
        "regrade.success": float(success),
        "_forbidden_hits": forb,
        "_expected_status": expected,
        "_observed_status": status,
    }


def apply_regrade(runs: list[RunRecord], cases: list[CaseRecord], suite: str) -> dict[str, Any]:
    """Regrade every run of `suite` in place; return a grader-agreement report."""
    by_case = {c.case_id: c for c in cases if c.suite == suite}
    deltas: list[float] = []
    missing_case: list[str] = []
    n = 0
    for run in runs:
        if run.suite != suite:
            continue
        case = by_case.get(run.case_id)
        if case is None:
            # No registered case definition: nothing to grade against. The run
            # keeps whatever the source recorded and is excluded from scoring.
            missing_case.append(run.case_id)
            run.metrics["regrade.ungraded"] = 1.0
            run.primary_score = None
            run.correct = None
            continue
        g = regrade_run(run, case)
        n += 1
        recorded = run.metrics.get("composite_score")
        if isinstance(recorded, (int, float)):
            deltas.append(abs(recorded - g["regrade.composite"]))
        run.metrics.update({k: v for k, v in g.items() if not k.startswith("_")})
        run.extra["regrade_detail"] = {k: v for k, v in g.items() if k.startswith("_")}
        run.correct = bool(g["regrade.success"])
        # Trust the harness-owned score as primary; keep the source score in metrics.
        run.primary_score = g["regrade.composite"]
        run.primary_metric = "regrade.composite"
    return {
        "suite": suite,
        "n_regraded": n,
        "n_missing_case_definition": len(set(missing_case)),
        "missing_case_ids": sorted(set(missing_case)),
        "mean_abs_delta_vs_recorded": (sum(deltas) / len(deltas)) if deltas else None,
        "max_abs_delta_vs_recorded": max(deltas) if deltas else None,
        "n_compared": len(deltas),
        "weights": dict(WEIGHTS),
    }
