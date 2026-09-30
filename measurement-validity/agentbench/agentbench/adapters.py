"""Adapters: project-specific run dialects -> canonical RunRecord.

Each adapter is a pure reader. It never mutates the source tree, and it records
`source_path` on every record so any aggregate number can be traced back to the
file it came from.

Adding a new project means writing one function here; nothing downstream
changes.
"""

from __future__ import annotations

import glob
import json
import os
from typing import Any, Iterable

from .schema import CaseRecord, RunRecord


def _read_jsonl(path: str) -> list[dict]:
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _scalars(d: Any) -> dict[str, Any]:
    """Keep only scalar grade fields; lists/dicts go to `extra`."""
    if not isinstance(d, dict):
        return {}
    return {k: v for k, v in d.items() if isinstance(v, (int, float, bool))}


# --------------------------------------------------------------------------
# chat-archaeologist: retrieval/abstention agent, runs.jsonl schema v3
# --------------------------------------------------------------------------

def _migrate_chat_archaeologist(r: dict) -> dict:
    """Lift an older flat record (schema_version 1) into the v3 shape.

    v1 predates case registration: the run has a free-text query but no
    `case_id`, so it is tagged `unregistered:<run>` and lands in the `unknown`
    split, where it is reported but never used for arm comparison.
    """
    if r.get("schema_version", 3) >= 3:
        return r
    lat_ms = r.get("latency_ms")
    return {
        "schema_version": r.get("schema_version"),
        "run_id": r.get("run_id"),
        "timestamp": r.get("recorded_at"),
        "rung": r.get("kind"),
        "configuration": r.get("configuration") or r.get("mode"),
        "prompt_sha256": r.get("prompt_sha256"),
        "model_requested": r.get("model"),
        "model_returned": r.get("model"),
        "repeat_index": 1,
        "case_id": f"unregistered:{str(r.get('run_id'))[:8]}",
        "split": "unknown",
        "category": None,
        "query": r.get("query"),
        "expected_status": None,
        "answer": {
            "status": r.get("status"),
            "answer": r.get("answer"),
            "selected_source_ref": r.get("selected_source_ref"),
            "evidence": r.get("evidence") or [],
            "abstention_reason": r.get("abstention_reason"),
            "confidence": r.get("confidence"),
        },
        "grade": {},
        "usage": {**(r.get("usage") or {}),
                  "estimated_cost_usd": r.get("estimated_cost_usd")},
        "latency_seconds": (lat_ms / 1000.0) if isinstance(lat_ms, (int, float)) else None,
        "tool_events": r.get("tool_events") or [],
        "error": "; ".join(r.get("validation_errors") or []) or None,
        "corpus_manifest_sha256": None,
    }


def load_chat_archaeologist(root: str) -> tuple[list[RunRecord], list[CaseRecord]]:
    suite = "chat-archaeologist"
    cases: list[CaseRecord] = []
    for path in sorted(glob.glob(os.path.join(root, "private/evals/*_cases.jsonl"))):
        for c in _read_jsonl(path):
            cases.append(
                CaseRecord(
                    suite=suite,
                    case_id=c["id"],
                    split=c.get("split", "unknown"),
                    category=c.get("category"),
                    query=c.get("query"),
                    expected_status=c.get("expected_status"),
                    expected_answer=c.get("expected_answer"),
                    expected_source_refs=c.get("expected_source_refs") or [],
                    required_terms=c.get("required_terms") or [],
                    forbidden_terms=c.get("forbidden_terms") or [],
                    verified_by_owner=c.get("verified_by_owner"),
                    notes=c.get("notes"),
                )
            )

    run_paths = sorted(
        glob.glob(os.path.join(root, "artifacts/runs/*.jsonl"))
        + glob.glob(os.path.join(root, "data/runs/*.jsonl"))
    )
    seen: set[str] = set()
    runs: list[RunRecord] = []
    for path in run_paths:
        for r in _read_jsonl(path):
            r = _migrate_chat_archaeologist(r)
            rid = r.get("run_id")
            if rid in seen:
                continue
            seen.add(rid)
            grade = r.get("grade") or {}
            usage = r.get("usage") or {}
            answer = r.get("answer") or {}
            runs.append(
                RunRecord(
                    suite=suite,
                    source_project="Adverserial Bot!",
                    source_path=os.path.relpath(path, root),
                    run_id=rid,
                    case_id=r.get("case_id"),
                    arm=r.get("configuration") or "unspecified",
                    timestamp=r.get("timestamp"),
                    split=r.get("split", "unknown"),
                    repeat=r.get("repeat_index") or 1,
                    model=r.get("model_returned") or r.get("model_requested"),
                    reasoning_effort=r.get("reasoning_effort"),
                    status=answer.get("status"),
                    completed=not r.get("error"),
                    primary_score=grade.get("composite_score"),
                    primary_metric="composite_score",
                    correct=None,  # assigned by the regrader
                    latency_s=r.get("latency_seconds"),
                    cost_usd=usage.get("estimated_cost_usd"),
                    input_tokens=usage.get("input_tokens"),
                    output_tokens=usage.get("output_tokens"),
                    tool_calls=len(r.get("tool_events") or []),
                    error=r.get("error"),
                    input_digest=r.get("corpus_manifest_sha256"),
                    metrics=_scalars(grade),
                    extra={
                        "answer": answer,
                        "tool_events": r.get("tool_events") or [],
                        "recorded_reasons": grade.get("reasons") or [],
                        "expected_status": r.get("expected_status"),
                        "rung": r.get("rung"),
                    },
                )
            )
    return runs, cases


# --------------------------------------------------------------------------
# evidence-escape-room: instruction-variant study, one run JSON per execution
# --------------------------------------------------------------------------

def load_escape_room(root: str) -> tuple[list[RunRecord], list[CaseRecord]]:
    suite = "evidence-escape-room"
    runs: list[RunRecord] = []
    for path in sorted(glob.glob(os.path.join(root, "runs/*.json"))):
        r = json.load(open(path))
        grade = r.get("grade") or {}
        usage = r.get("usage") or {}
        total = grade.get("total_score")
        runs.append(
            RunRecord(
                suite=suite,
                source_project="Adverserial Bot!",
                source_path=os.path.relpath(path, root),
                run_id=r.get("run_id"),
                case_id=r.get("case_id"),
                arm=r.get("strategy") or "unspecified",
                arm_label=r.get("strategy_label"),
                timestamp=r.get("created_at"),
                split="visible",
                model=r.get("model_requested"),
                status=r.get("status"),
                completed=r.get("status") == "completed",
                primary_score=(total / 100.0) if isinstance(total, (int, float)) else None,
                primary_metric="total_score/100",
                correct=(grade.get("verdict") == "pass") if grade else None,
                latency_s=r.get("latency_seconds"),
                cost_usd=usage.get("estimated_cost_usd"),
                input_tokens=usage.get("input_tokens"),
                output_tokens=usage.get("output_tokens"),
                tool_calls=len(r.get("events") or []) or None,
                error=r.get("error"),
                metrics=_scalars(grade),
                extra={
                    "verdict": grade.get("verdict"),
                    "missing_evidence_roles": grade.get("missing_evidence_roles"),
                    "inspected_ids": r.get("inspected_ids"),
                },
            )
        )
    # repeats: same (case, arm) executed more than once
    counters: dict[tuple[str, str], int] = {}
    for rec in sorted(runs, key=lambda x: x.timestamp or ""):
        key = (rec.case_id, rec.arm)
        counters[key] = counters.get(key, 0) + 1
        rec.repeat = counters[key]
    return runs, []


# --------------------------------------------------------------------------
# adversarial-coevolution-arena: study summaries with per-execution records
# --------------------------------------------------------------------------

_ARENA_HOLDOUT_PHASES = {"sentinel", "transfer"}


def load_arena(root: str) -> tuple[list[RunRecord], list[CaseRecord]]:
    suite = "coevolution-arena"
    runs: list[RunRecord] = []
    for path in sorted(glob.glob(os.path.join(root, ".arena/*/summary.json"))):
        study = json.load(open(path))
        study_id = os.path.basename(os.path.dirname(path))
        for i, e in enumerate(study.get("executions") or []):
            phase = e.get("phase")
            tok = e.get("tokenUsage") or {}
            oracle = e.get("oracle")
            expected = e.get("expectedAction")
            action = e.get("action")
            correct = None
            if isinstance(oracle, dict):
                for key in ("pass", "passed", "ok", "accepted"):
                    if isinstance(oracle.get(key), bool):
                        correct = oracle[key]
                        break
                if correct is None and isinstance(oracle.get("verdict"), str):
                    correct = oracle["verdict"].lower() in {"pass", "accept", "accepted"}
            if correct is None and expected is not None:
                correct = action == expected
            wall = e.get("wallTimeMs")
            runs.append(
                RunRecord(
                    suite=suite,
                    source_project="Adverserial Bot!",
                    source_path=os.path.relpath(path, root),
                    run_id=f"{study_id}:{i:03d}",
                    case_id=e.get("caseId") or "unspecified",
                    arm=e.get("strategy") or study.get("kind") or "unspecified",
                    timestamp=None,
                    split="holdout" if phase in _ARENA_HOLDOUT_PHASES else "visible",
                    model=e.get("model") or study.get("model"),
                    reasoning_effort=e.get("reasoning") or study.get("reasoning"),
                    status=("ok" if e.get("exitStatus") == 0 else "error"),
                    completed=e.get("exitStatus") == 0 and not e.get("error"),
                    primary_score=(1.0 if correct else 0.0) if correct is not None else None,
                    primary_metric="oracle_pass",
                    correct=correct,
                    latency_s=(wall / 1000.0) if isinstance(wall, (int, float)) else None,
                    cost_usd=None,
                    input_tokens=tok.get("input_tokens") or tok.get("inputTokens"),
                    output_tokens=tok.get("output_tokens") or tok.get("outputTokens"),
                    tool_calls=(len(e["toolUse"]) if isinstance(e.get("toolUse"), list) else None),
                    error=(str(e.get("error")) if e.get("error") else None),
                    input_digest=(e.get("inputManifest") or {}).get("manifestHash")
                    or e.get("inputManifestHash"),
                    metrics={},
                    extra={
                        "study": study_id,
                        "study_kind": study.get("kind"),
                        "phase": phase,
                        "action": action,
                        "expected_action": expected,
                        "study_verdict": study.get("studyVerdict"),
                        "parse_error": e.get("parseError"),
                    },
                )
            )
    counters: dict[tuple[str, str, str], int] = {}
    for rec in runs:
        key = (rec.case_id, rec.arm, rec.extra.get("phase") or "")
        counters[key] = counters.get(key, 0) + 1
        rec.repeat = counters[key]
    return runs, []


# --------------------------------------------------------------------------
# 2248-challenge: evidence-ledger experiments (claims, not arm comparisons)
# --------------------------------------------------------------------------

def _exp_id(path: str) -> str:
    return os.path.basename(os.path.dirname(path))


def load_2248_policy(root: str) -> tuple[list[RunRecord], list[CaseRecord]]:
    """Policy confirmation/qualification cells: `policy` is the arm.

    One cell is one (policy, level, seed) execution with a binary outcome
    (`targetReached`), so this is a clean two-arm comparison paired on the
    (level, seed) board.
    """
    suite = "2248-policy"
    runs: list[RunRecord] = []
    for kind in ("qualification", "confirmation"):
        for path in sorted(glob.glob(os.path.join(root, f"experiments/RESULT-*/{kind}.json"))):
            try:
                d = json.load(open(path))
            except Exception:
                continue
            cells = d.get("cells") or []
            if not cells:
                continue
            eid = _exp_id(path)
            # `qualification` is the smoke test before the confirmation run:
            # different seeds and a different reportable standing, so it is
            # held separately rather than pooled with the confirmation.
            split = "visible" if kind == "qualification" else "holdout"
            counters: dict[tuple, int] = {}
            for i, c in enumerate(cells):
                case = f"L{c.get('level')}:s{c.get('seed')}"
                arm = c.get("policy") or "unspecified"
                counters[(case, arm)] = counters.get((case, arm), 0) + 1
                reached = c.get("targetReached")
                rt = c.get("chooserRuntimeMs")
                runs.append(RunRecord(
                    suite=suite,
                    source_project="2248-challenge",
                    source_path=os.path.relpath(path, root),
                    run_id=f"{eid}:{kind}:{i:04d}",
                    case_id=case,
                    arm=arm,
                    split=split,
                    repeat=counters[(case, arm)],
                    model=c.get("policyId"),
                    status=c.get("terminationReason"),
                    completed=True,
                    primary_score=(1.0 if reached else 0.0) if reached is not None else None,
                    primary_metric="target_reached",
                    correct=bool(reached) if reached is not None else None,
                    latency_s=(rt / 1000.0) if isinstance(rt, (int, float)) else None,
                    metrics={k: v for k, v in c.items()
                             if k in ("score", "movesToTarget", "movesUsed",
                                      "moveBudget", "target", "level")
                             and isinstance(v, (int, float, bool))},
                    extra={"experiment": eid, "receipt": kind,
                           "reportable": d.get("reportable")},
                ))
    return runs, []


_SEARCH_UNRESOLVED = {"UNKNOWN", None}


def load_2248_search(root: str) -> tuple[list[RunRecord], list[CaseRecord]]:
    """Corpus rows carrying a `shallow` vs `deep` search pair: depth is the arm.

    Each row is one board searched both ways, so the arms are paired by
    construction. The outcome is whether the search resolved a standing at all
    (anything other than UNKNOWN); the cost is expanded states, where the
    receipt records it.
    """
    suite = "2248-search-depth"
    runs: list[RunRecord] = []
    for path in sorted(glob.glob(os.path.join(root, "experiments/RESULT-*/corpus.json"))):
        try:
            d = json.load(open(path))
        except Exception:
            continue
        rows = d.get("rows") or []
        eid = _exp_id(path)
        for i, r in enumerate(rows):
            if not all(isinstance(r.get(s), dict) and "standing" in r[s]
                       for s in ("shallow", "deep")):
                continue
            cost = r.get("deterministicCost") or {}
            for side in ("shallow", "deep"):
                v = r[side]
                standing = v.get("standing")
                resolved = standing not in _SEARCH_UNRESOLVED
                expanded = cost.get(f"{side}ExpandedStates")
                runs.append(RunRecord(
                    suite=suite,
                    source_project="2248-challenge",
                    source_path=os.path.relpath(path, root),
                    run_id=f"{eid}:{i:03d}:{side}",
                    # The board is only meaningful within its experiment.
                    case_id=f"{eid}:L{r.get('level')}:s{r.get('seed')}",
                    arm=side,
                    split="visible",
                    status=standing,
                    completed=True,
                    primary_score=1.0 if resolved else 0.0,
                    primary_metric="standing_resolved",
                    correct=resolved,
                    metrics={"expanded_states": expanded} if isinstance(expanded, (int, float)) else {},
                    input_digest=v.get("puzzleIdentity") or r.get("puzzleIdentity"),
                    extra={"experiment": eid, "dimensions": r.get("dimensions"),
                           "bin": r.get(f"{side}Bin"), "standing": standing,
                           "descriptors": v.get("descriptors")},
                ))
    return runs, []


def load_2248_exact(root: str) -> tuple[list[RunRecord], list[CaseRecord]]:
    """The exact-greed-ratio replication family (RESULT-0036/0037/0038).

    These three experiments re-run the same (level, percentile) design points
    on *fresh seeds*, so they are replications, not repeats: the arm is the
    experiment and cases pair on the design point, never on the seed.
    """
    suite = "2248-exact-greed"
    runs: list[RunRecord] = []
    for path in sorted(glob.glob(os.path.join(root, "experiments/RESULT-*/corpus.json"))):
        try:
            d = json.load(open(path))
        except Exception:
            continue
        rows = d.get("rows") or []
        if not rows or "win" not in rows[0]:
            continue
        eid = _exp_id(path)
        counters: dict[str, int] = {}
        for i, r in enumerate(rows):
            case = f"L{r.get('level')}:p{r.get('percentile')}"
            counters[case] = counters.get(case, 0) + 1
            win = r.get("win")
            obs = r.get("denominatorObservations") or []
            timeouts = sorted({o.get("timeoutMs") for o in obs
                               if isinstance(o, dict) and o.get("timeoutMs") is not None})
            desc = r.get("descriptors") or {}
            runs.append(RunRecord(
                suite=suite,
                source_project="2248-challenge",
                source_path=os.path.relpath(path, root),
                run_id=f"{eid}:{i:03d}",
                case_id=case,
                arm=eid,
                split="visible",
                repeat=counters[case],
                status=r.get("terminal"),
                completed=True,
                primary_score=(1.0 if win else 0.0) if win is not None else None,
                primary_metric="win",
                correct=bool(win) if win is not None else None,
                metrics={
                    "score": r.get("score"),
                    "moves": r.get("moves"),
                    "exact_complete": float(bool(r.get("exactComplete"))),
                    "half_score_move": desc.get("halfScoreMove"),
                    "greed_ratio": desc.get("greedRatio"),
                    "oracle_timeout_ms": timeouts[-1] if timeouts else None,
                },
                extra={"experiment": eid, "seed": r.get("seed"),
                       "percentile": r.get("percentile"),
                       "denominator": r.get("denominator")},
            ))
    return runs, []


def split_sample_measurements(root: str) -> list[dict]:
    """Measurement receipts that score candidates under two disjoint seed samples.

    RESULT-0021's registered claim is that the *ranking* of candidates is
    stable across two disjoint seed samples. That is a reliability question,
    not an arm comparison, so it is returned as its own record rather than as
    RunRecords.
    """
    out: list[dict] = []
    for path in sorted(glob.glob(os.path.join(root, "experiments/RESULT-*/measurement.json"))):
        try:
            d = json.load(open(path))
        except Exception:
            continue
        ms = d.get("measurements") or []
        if not ms:
            continue
        out.append({
            "experiment": _exp_id(path),
            "claim": (d.get("claim") or "")[:200] or None,
            "metric": d.get("metric"),
            "n_measurements": len(ms),
            "n_candidates": len({m.get("candidateName") for m in ms}),
            "samples": sorted({m.get("sample") for m in ms}),
            "measurements": ms,
        })
    return out


def load_ledger_claims(root: str) -> list[dict]:
    """Index the RESULT-00xx experiment ledger.

    These records assert *claims* with a registered protocol and a closure
    status rather than comparing arms, so they are reported as an experiment
    inventory, not folded into the arm statistics.
    """
    out: list[dict] = []
    for exp_dir in sorted(glob.glob(os.path.join(root, "experiments/RESULT-*"))):
        if not os.path.isdir(exp_dir):
            continue
        rec: dict[str, Any] = {
            "experiment": os.path.basename(exp_dir),
            "source_project": "2248-challenge",
            "files": sorted(os.path.basename(p) for p in glob.glob(os.path.join(exp_dir, "*"))),
        }
        artifact_kinds = []
        for name in ("closure", "corpus", "measurement", "confirmation", "qualification"):
            path = os.path.join(exp_dir, f"{name}.json")
            if not os.path.exists(path):
                continue
            try:
                d = json.load(open(path))
            except Exception as exc:  # malformed ledger file
                rec[f"{name}_error"] = str(exc)
                continue
            if not isinstance(d, dict):
                continue
            artifact_kinds.append(name)

            # `result` in these files is the experiment id, not a verdict.
            if name == "closure":
                rec["closure_status"] = d.get("closure_status")
                rec["primary_outcome"] = d.get("primary_outcome")
                claims = d.get("claims") or []
                rec["n_claims"] = len(claims)
                rec["n_claims_pass"] = sum(
                    1 for c in claims if isinstance(c, dict) and str(c.get("status")).upper() == "PASS")
                rec["n_deviations"] = len(d.get("deviations") or [])
            elif name == "corpus":
                rec["corpus_reportable"] = d.get("reportable")
                dec = d.get("decision")
                rec["corpus_verdict"] = dec.get("verdict") if isinstance(dec, dict) else None
                rec["proof_standing"] = (d.get("proofStanding") or "")[:120] or None
                reg = d.get("registration") or {}
                rec["preregistered"] = (not reg.get("exploratory")) if reg else None
            elif name == "measurement":
                rec["claim"] = (d.get("claim") or "")[:160] or None
                rec["metric"] = d.get("metric")
            else:  # confirmation / qualification
                rec[f"{name}_reportable"] = d.get("reportable")
        rec["ledger_artifacts"] = ",".join(artifact_kinds) or None
        rec.pop("files", None)
        out.append(rec)
    return out


ADAPTERS = {
    "chat-archaeologist": load_chat_archaeologist,
    "evidence-escape-room": load_escape_room,
    "coevolution-arena": load_arena,
    "2248-policy": load_2248_policy,
    "2248-search-depth": load_2248_search,
    "2248-exact-greed": load_2248_exact,
}


def load_all(sources: dict[str, str]) -> tuple[list[RunRecord], list[CaseRecord]]:
    """sources: {adapter_name: root_path} -> (runs, cases)."""
    runs: list[RunRecord] = []
    cases: list[CaseRecord] = []
    for name, root in sources.items():
        if name not in ADAPTERS:
            raise KeyError(f"no adapter named {name!r}; have {sorted(ADAPTERS)}")
        if not os.path.isdir(root):
            raise FileNotFoundError(f"{name}: {root}")
        r, c = ADAPTERS[name](root)
        runs.extend(r)
        cases.extend(c)
    return runs, cases
