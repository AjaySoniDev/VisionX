import numpy as np
import pytest

from vxn_ramnet.config.models import DecisionSettings, DetectionSettings
from vxn_ramnet.core.enums import ComponentKind
from vxn_ramnet.core.exceptions import InsufficientEvidenceError
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.memory.store import RouteMemoryStore
from vxn_ramnet.recognition import RouteRecognizer


def test_low_quality_enrollment_cannot_authorize_branch_acceptance():
    embeddings = np.eye(100, dtype=np.float32)
    kinds = list(ComponentKind)
    mapping = {kind: tuple(range(i * 20, (i + 1) * 20)) for i, kind in enumerate(kinds)}
    memory = RouteMemoryStore.build(embeddings, embeddings, mapping, {kind: kind.value for kind in kinds}, {})
    query_values = embeddings[40:60].repeat(3, axis=0)
    query = EncodedSequence("query-a", query_values, query_values, (), {})
    recognizer = RouteRecognizer(DecisionSettings(), DetectionSettings())
    assert recognizer.classify(query, memory)["branch_id"] == "BRANCH_A"
    memory.metadata["quality"] = {"junction_confidence": "low", "backtrack_confidence": "high"}
    result = recognizer.classify(query, memory)
    assert result["decision_kind"] == "uncertain"
    assert result["branch_id"] is None
    assert result["evidence"]["graph_degraded"]


def test_short_queries_fail_explicitly():
    values = np.eye(10, dtype=np.float32)
    with pytest.raises(InsufficientEvidenceError):
        RouteRecognizer(DecisionSettings(), DetectionSettings()).classify(
            EncodedSequence("qa", values, values, (), {}), None
        )
