from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np

from vxn_ramnet.config.models import DecisionSettings
from vxn_ramnet.core.enums import DecisionKind
from vxn_ramnet.core.types import BranchDecision


@dataclass(frozen=True)
class AggregatedScores:
    branch_a: float
    branch_b: float
    gap: float
    best: float
    common: float
    junction: float

    def __post_init__(self) -> None:
        if not all(math.isfinite(v) for v in asdict(self).values()):
            raise ValueError("Decision scores must be finite")
        if not all(
            -1.0001 <= v <= 1.0001 for v in (self.branch_a, self.branch_b, self.best, self.common, self.junction)
        ):
            raise ValueError("Decision similarities must lie within [-1, 1]")
        if not math.isclose(self.best, max(self.branch_a, self.branch_b), abs_tol=1e-6):
            raise ValueError("Best score is inconsistent with branch scores")
        if not math.isclose(self.gap, abs(self.branch_a - self.branch_b), abs_tol=1e-6):
            raise ValueError("Gap is inconsistent with branch scores")


def aggregate_windows(rows: list[dict], selected: list[dict]) -> AggregatedScores:
    if not selected:
        raise ValueError("No windows selected")

    def mean(key: str) -> float:
        return float(np.mean([r[key] for r in selected]))

    a, b = mean("branch_a_score"), mean("branch_b_score")
    return AggregatedScores(a, b, abs(a - b), max(a, b), mean("common_score"), mean("junction_score"))


def _confidence(best: float, gap: float, temperature: float) -> float:
    separation = 1.0 / (1.0 + math.exp(-gap / temperature))
    strength = max(0.0, min(1.0, (best + 1.0) / 2.0))
    return float(max(0.0, min(1.0, 0.55 * separation + 0.45 * strength)))


def decide(
    scores: AggregatedScores, settings: DecisionSettings, branch_a_name: str, branch_b_name: str, evidence: dict
) -> BranchDecision:
    if not branch_a_name.strip() or not branch_b_name.strip() or branch_a_name == branch_b_name:
        raise ValueError("Branch names must be nonblank and distinct")
    if scores.best < settings.unknown_score:
        return BranchDecision(
            DecisionKind.UNKNOWN_ROUTE, None, None, "Evidence is weak for both learned branches.", evidence
        )
    if scores.gap < settings.minimum_branch_gap:
        return BranchDecision(
            DecisionKind.UNCERTAIN, None, None, "Branch evidence is too close to distinguish a branch.", evidence
        )
    if scores.best < settings.minimum_branch_score:
        return BranchDecision(
            DecisionKind.UNKNOWN_ROUTE,
            None,
            None,
            "Best branch score is below the minimum recognition threshold.",
            evidence,
        )
    branch = branch_a_name if scores.branch_a > scores.branch_b else branch_b_name
    strength = (
        "Strong"
        if scores.best >= settings.strong_branch_score and scores.gap >= settings.strong_branch_gap
        else "Acceptable"
    )
    return BranchDecision(
        DecisionKind.KNOWN_BRANCH,
        branch,
        _confidence(scores.best, scores.gap, settings.confidence_temperature),
        f"{strength} evidence for {branch}.",
        evidence,
    )


def scores_to_dict(scores: AggregatedScores) -> dict:
    return asdict(scores)
