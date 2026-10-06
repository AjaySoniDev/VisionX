"""Transparent comparison methods using the same automatically learned memory.

Suffix methods use the last 55% of completed queries. DTW is an ordinary
global-alignment baseline, not an implementation or claimed replication of SeqSLAM.
"""

from __future__ import annotations

import numpy as np

from vxn_ramnet.algorithms.decision import AggregatedScores, decide
from vxn_ramnet.algorithms.similarity import flip_aware_similarity
from vxn_ramnet.config.models import DecisionSettings
from vxn_ramnet.core.enums import ComponentKind
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.memory.schema import RouteMemory


def dtw_similarity(similarity: np.ndarray) -> float:
    matrix = np.asarray(similarity, dtype=float)
    if matrix.ndim != 2 or not matrix.size or not np.isfinite(matrix).all():
        raise ValueError("DTW requires a finite nonempty similarity matrix")
    if np.any(matrix < -1.0001) or np.any(matrix > 1.0001):
        raise ValueError("DTW similarities must lie within [-1, 1]")
    n, m = matrix.shape
    costs = np.full((n + 1, m + 1), np.inf)
    lengths = np.zeros((n + 1, m + 1), dtype=np.int32)
    costs[0, 0] = 0.0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            choices = ((i - 1, j - 1), (i - 1, j), (i, j - 1))
            a, b = min(choices, key=lambda pair: costs[pair])
            costs[i, j] = costs[a, b] + 1.0 - matrix[i - 1, j - 1]
            lengths[i, j] = lengths[a, b] + 1
    return float(1.0 - costs[n, m] / lengths[n, m])


def classify_baseline(method: str, query: EncodedSequence, memory: RouteMemory, settings: DecisionSettings) -> dict:
    if method == "fixed_branch_a":
        return {
            "query_id": query.sequence_id,
            "decision_kind": "known_branch",
            "branch_id": "BRANCH_A",
            "confidence": None,
            "reason": "Predeclared always-A forced-choice baseline",
            "best_branch_score": None,
        }
    start = int(0.45 * len(query.embeddings))
    q, qf = query.embeddings[start:], query.flipped_embeddings[start:]
    scores = []
    for kind in (ComponentKind.BRANCH_A, ComponentKind.BRANCH_B):
        component = memory.components[kind]
        if method == "global_centroid":
            c = component.centroid
            score = float(np.maximum(q @ c, qf @ c).mean())
        elif method == "last_frame_nn":
            score = float(
                flip_aware_similarity(q[-1:], qf[-1:], component.embeddings, component.flipped_embeddings).max()
            )
        elif method == "mean_frame_nn":
            score = float(
                flip_aware_similarity(q, qf, component.embeddings, component.flipped_embeddings).max(axis=1).mean()
            )
        elif method == "dtw_suffix":
            qi = np.linspace(0, len(q) - 1, min(64, len(q)), dtype=int)
            mi = np.linspace(0, len(component.embeddings) - 1, min(64, len(component.embeddings)), dtype=int)
            score = dtw_similarity(
                flip_aware_similarity(q[qi], qf[qi], component.embeddings[mi], component.flipped_embeddings[mi])
            )
        else:
            raise ValueError(f"Unknown baseline: {method}")
        scores.append(score)
    a, b = scores
    aggregated = AggregatedScores(a, b, abs(a - b), max(a, b), 0.0, 0.0)
    decision = decide(aggregated, settings, "BRANCH_A", "BRANCH_B", {})
    return {
        "query_id": query.sequence_id,
        "decision_kind": decision.kind.value,
        "branch_id": decision.branch_id,
        "confidence": decision.confidence,
        "reason": decision.reason,
        "branch_a_score": a,
        "branch_b_score": b,
        "branch_gap": abs(a - b),
        "best_branch_score": max(a, b),
    }
