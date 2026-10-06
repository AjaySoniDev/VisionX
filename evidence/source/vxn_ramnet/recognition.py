"""Pure cached-embedding API shared by the video pipeline and evaluation.

Enrollment infers a constrained topology. Recognition uses completed queries;
neither API estimates physical turn direction or provides live guidance.
"""

from __future__ import annotations

import numpy as np

from vxn_ramnet.algorithms.decision import aggregate_windows, decide
from vxn_ramnet.algorithms.junction import ConstrainedJunctionDetector, candidate_to_dict, junction_confidence
from vxn_ramnet.algorithms.scoring import branch_windows, component_score, select_diverse_top_windows
from vxn_ramnet.algorithms.segmentation import build_segments
from vxn_ramnet.algorithms.similarity import flip_aware_similarity, suppress_diagonal, validate_embedding_pair
from vxn_ramnet.algorithms.turnaround import (
    ReverseSequenceTurnaroundDetector,
    turnaround_confidence,
    turnaround_to_dict,
)
from vxn_ramnet.config.models import DecisionSettings, DetectionSettings
from vxn_ramnet.core.enums import ComponentKind, DecisionKind
from vxn_ramnet.core.exceptions import InsufficientEvidenceError
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.memory.schema import RouteMemory
from vxn_ramnet.memory.store import RouteMemoryStore


def learn_route_memory(
    learning: EncodedSequence,
    settings: DetectionSettings,
    branch_a_name: str = "BRANCH_A",
    branch_b_name: str = "BRANCH_B",
    *,
    fail_on_degraded_graph: bool = False,
) -> tuple[RouteMemory, np.ndarray]:
    original, flipped = validate_embedding_pair(learning.embeddings, learning.flipped_embeddings, "learning")
    similarity = flip_aware_similarity(original, flipped, original, flipped, settings.self_similarity_chunk_size)
    similarity = suppress_diagonal(similarity, max(8, int(0.035 * len(original))))
    junction, junctions = ConstrainedJunctionDetector(settings).detect(similarity)
    turnaround, turnarounds = ReverseSequenceTurnaroundDetector(settings).detect(
        original, flipped, junction.first_index, junction.return_index
    )
    segments = build_segments(len(original), junction.first_index, turnaround.index, junction.return_index, settings)
    quality = {
        "junction_score": junction.raw_score,
        "junction_confidence": junction_confidence(junction.raw_score, settings),
        "backtrack_score": turnaround.raw_score,
        "backtrack_confidence": turnaround_confidence(turnaround.raw_score, settings),
    }
    if fail_on_degraded_graph and "low" in (quality["junction_confidence"], quality["backtrack_confidence"]):
        raise InsufficientEvidenceError("Enrollment graph failed its configured quality gate")
    mapping = {
        ComponentKind.COMMON_PATH: segments.common,
        ComponentKind.JUNCTION: segments.junction,
        ComponentKind.BRANCH_A: segments.branch_a,
        ComponentKind.BACKTRACK: segments.backtrack,
        ComponentKind.BRANCH_B: segments.branch_b,
    }
    display = {kind: kind.value.upper() for kind in mapping}
    display[ComponentKind.BRANCH_A] = branch_a_name
    display[ComponentKind.BRANCH_B] = branch_b_name
    metadata = {
        "mode": "constrained_single_junction_backtracking",
        "topology_limit": "one junction and two exploration-order branches",
        "segment_policy": settings.segment_policy,
        "events": {
            "first_junction_index": junction.first_index,
            "turnaround_index": turnaround.index,
            "return_junction_index": junction.return_index,
        },
        "quality": quality,
        "segments": segments.as_ranges(),
        "component_counts": {kind.value: len(values) for kind, values in mapping.items()},
        "top_junction_candidates": [candidate_to_dict(c) for c in junctions],
        "top_turnaround_candidates": [turnaround_to_dict(c) for c in turnarounds],
        "branch_label_note": "Branch names describe exploration order, not validated physical left/right direction.",
        "encoder": learning.metadata.get("encoder", {}),
    }
    return RouteMemoryStore.build(original, flipped, mapping, display, metadata), similarity


class RouteRecognizer:
    def __init__(
        self,
        settings: DecisionSettings,
        detection: DetectionSettings,
        branch_a_name: str = "BRANCH_A",
        branch_b_name: str = "BRANCH_B",
    ):
        self.settings = settings
        self.detection = detection
        self.branch_a_name = branch_a_name
        self.branch_b_name = branch_b_name

    def classify(self, query: EncodedSequence, memory: RouteMemory, *, cache_frame_scores: bool = True) -> dict:
        original, flipped = validate_embedding_pair(query.embeddings, query.flipped_embeddings, "query")
        windows = branch_windows(len(original))
        if not windows:
            raise InsufficientEvidenceError("Query needs at least 20 embeddings for window evidence")
        kinds = (
            ("branch_a", ComponentKind.BRANCH_A),
            ("branch_b", ComponentKind.BRANCH_B),
            ("common", ComponentKind.COMMON_PATH),
            ("junction", ComponentKind.JUNCTION),
        )
        frame_scores = {}
        if cache_frame_scores:
            # Component evidence is frame-independent. Calculate it once rather
            # than rebuilding the same similarities for overlapping windows.
            for key, kind in kinds:
                component = memory.components[kind]
                _, frame_scores[key] = component_score(
                    original,
                    flipped,
                    component.embeddings,
                    component.flipped_embeddings,
                    component.centroid,
                    self.detection.self_similarity_chunk_size,
                )
        rows = []
        for start, end in windows:
            scores = {}
            for key, kind in kinds:
                if cache_frame_scores:
                    scores[key] = float(np.mean(frame_scores[key][start:end]))
                else:
                    component = memory.components[kind]
                    scores[key], _ = component_score(
                        original[start:end],
                        flipped[start:end],
                        component.embeddings,
                        component.flipped_embeddings,
                        component.centroid,
                        self.detection.self_similarity_chunk_size,
                    )
            best = max(scores["branch_a"], scores["branch_b"])
            gap = abs(scores["branch_a"] - scores["branch_b"])
            shared = max(scores["common"], scores["junction"])
            rows.append(
                {
                    "start": start,
                    "end": end,
                    "frame_count": end - start,
                    "branch_a_score": scores["branch_a"],
                    "branch_b_score": scores["branch_b"],
                    "common_score": scores["common"],
                    "junction_score": scores["junction"],
                    "best_branch_score": best,
                    "branch_gap": gap,
                    "shared_score": shared,
                    "window_quality": best + 0.70 * gap - 0.25 * shared + 0.03 * (start / max(1, len(original))),
                }
            )
        if not rows:
            raise InsufficientEvidenceError("Query needs at least 20 embeddings for window evidence")
        if self.settings.window_selection == "legacy_best":
            selected = [max(rows, key=lambda row: row["window_quality"])]
        else:
            selected = select_diverse_top_windows(rows, self.settings.top_k_windows)
        aggregate = aggregate_windows(rows, selected)
        quality = memory.metadata.get("quality", {})
        degraded = "low" in (quality.get("junction_confidence"), quality.get("backtrack_confidence"))
        evidence = {
            "selected_windows": [
                {"start": r["start"], "end": r["end"], "quality": r["window_quality"]} for r in selected
            ],
            "all_windows": sorted(rows, key=lambda row: row["window_quality"], reverse=True),
            "aggregation": self.settings.window_selection,
            "graph_degraded": degraded,
            "confidence_semantics": "uncalibrated heuristic; not a probability",
            "score_execution": "cached_frame_scores" if cache_frame_scores else "reference_window_recomputation",
        }
        decision = decide(aggregate, self.settings, self.branch_a_name, self.branch_b_name, evidence)
        result = {
            "query_id": query.sequence_id,
            "decision_kind": decision.kind.value,
            "branch_id": decision.branch_id,
            "confidence": decision.confidence,
            "reason": decision.reason,
            "branch_a_score": aggregate.branch_a,
            "branch_b_score": aggregate.branch_b,
            "branch_gap": aggregate.gap,
            "common_score": aggregate.common,
            "junction_score": aggregate.junction,
            "selected_windows": len(selected),
            "evidence": decision.evidence,
        }
        if degraded:
            result.update(
                {
                    "decision_kind": DecisionKind.UNCERTAIN.value,
                    "branch_id": None,
                    "confidence": None,
                    "reason": "Enrollment graph quality is low; branch acceptance is withheld.",
                }
            )
        return result
