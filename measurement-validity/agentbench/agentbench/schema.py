"""Canonical run-record schema.

Every adapter normalizes a project-specific record into a RunRecord. The
canonical vocabulary is deliberately small: a *case* is the unit of work, an
*arm* is the thing being compared, a *repeat* distinguishes re-runs of the same
(case, arm), and a *split* separates visible from held-out cases.

Anything a source dialect carries that does not map onto a canonical field is
preserved verbatim under `extra`, so no information is lost by normalizing.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

SCHEMA_VERSION = 1

# Ordered canonical columns. Aggregation and reporting only ever reference
# these names, which is what makes cross-project comparison possible.
CANONICAL_FIELDS = [
    "schema_version",
    "suite",            # logical benchmark suite (usually one per project)
    "source_project",   # which repo/folder the record came from
    "source_path",      # file the record was read from (provenance)
    "run_id",
    "timestamp",
    "case_id",
    "split",            # "visible" | "holdout" | "unknown"
    "arm",              # configuration / strategy / policy under test
    "arm_label",
    "repeat",
    "model",
    "reasoning_effort",
    "status",           # terminal status reported by the source runner
    "completed",        # bool: run reached a scoreable end state
    "primary_score",    # normalized 0..1 quality score (suite-defined)
    "primary_metric",   # name of the metric primary_score came from
    "correct",          # bool | None: binary success where the suite defines one
    "latency_s",
    "cost_usd",
    "input_tokens",
    "output_tokens",
    "tool_calls",
    "error",
    "input_digest",     # hash of the inputs, when the source records one
]


@dataclass
class RunRecord:
    suite: str
    source_project: str
    source_path: str
    run_id: str
    case_id: str
    arm: str
    schema_version: int = SCHEMA_VERSION
    timestamp: str | None = None
    split: str = "unknown"
    arm_label: str | None = None
    repeat: int = 1
    model: str | None = None
    reasoning_effort: str | None = None
    status: str | None = None
    completed: bool = True
    primary_score: float | None = None
    primary_metric: str | None = None
    correct: bool | None = None
    latency_s: float | None = None
    cost_usd: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    tool_calls: int | None = None
    error: str | None = None
    input_digest: str | None = None
    # Source-native grade fields, kept as-is for suite-specific reporting.
    metrics: dict[str, Any] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)

    def flat(self) -> dict[str, Any]:
        """Flat dict: canonical columns plus metrics.* prefixed columns."""
        d = asdict(self)
        row = {k: d[k] for k in CANONICAL_FIELDS}
        for k, v in (self.metrics or {}).items():
            if isinstance(v, (int, float, bool)) or v is None:
                row[f"metric.{k}"] = v
        return row


@dataclass
class CaseRecord:
    """A benchmark case: the question plus whatever defines a correct answer."""

    suite: str
    case_id: str
    split: str = "unknown"
    category: str | None = None
    query: str | None = None
    expected_status: str | None = None
    expected_answer: str | None = None
    expected_source_refs: list[str] = field(default_factory=list)
    required_terms: list[str] = field(default_factory=list)
    forbidden_terms: list[str] = field(default_factory=list)
    verified_by_owner: bool | None = None
    notes: str | None = None

    def flat(self) -> dict[str, Any]:
        return asdict(self)
