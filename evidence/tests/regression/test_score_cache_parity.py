from pathlib import Path

import numpy as np
import pytest

from vxn_ramnet.config.models import DecisionSettings, DetectionSettings
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.io.npz import load_npz
from vxn_ramnet.recognition import RouteRecognizer, learn_route_memory

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/notebook04"


@pytest.mark.parametrize(
    "segment_policy,window_selection", [("disjoint", "top_k_mean"), ("legacy_overlap", "legacy_best")]
)
@pytest.mark.parametrize("query_id", ["query_route_1", "query_route_2"])
def test_precomputed_frame_evidence_matches_reference_recomputation(segment_policy, window_selection, query_id):
    learning = load_npz(FIXTURE / "learning.npz")
    query = load_npz(FIXTURE / (query_id + ".npz"))
    detection = DetectionSettings(segment_policy=segment_policy)
    memory, _ = learn_route_memory(
        EncodedSequence("learning", learning["embeddings"], learning["flipped_embeddings"], (), {}), detection
    )
    sequence = EncodedSequence(query_id, query["embeddings"], query["flipped_embeddings"], (), {})
    recognizer = RouteRecognizer(DecisionSettings(window_selection=window_selection), detection)
    cached = recognizer.classify(sequence, memory)
    reference = recognizer.classify(sequence, memory, cache_frame_scores=False)
    assert (cached["decision_kind"], cached["branch_id"]) == (reference["decision_kind"], reference["branch_id"])
    for key in ("branch_a_score", "branch_b_score", "common_score", "junction_score", "branch_gap"):
        assert np.isclose(cached[key], reference[key], atol=2e-6, rtol=0)
    a = {(r["start"], r["end"]): r for r in cached["evidence"]["all_windows"]}
    b = {(r["start"], r["end"]): r for r in reference["evidence"]["all_windows"]}
    assert a.keys() == b.keys()
    for interval in a:
        assert np.isclose(a[interval]["window_quality"], b[interval]["window_quality"], atol=2e-6, rtol=0)
