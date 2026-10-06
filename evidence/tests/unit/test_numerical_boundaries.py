import json

import numpy as np
import pytest
from pydantic import ValidationError

from vxn_ramnet.algorithms.decision import AggregatedScores
from vxn_ramnet.algorithms.similarity import flip_aware_similarity, l2_normalize_rows, validate_embedding_pair
from vxn_ramnet.config.models import DecisionSettings, EncoderSettings, FrameSettings
from vxn_ramnet.core.exceptions import ArtifactError, InputValidationError
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.io.atomic import atomic_write_json
from vxn_ramnet.io.json import read_json
from vxn_ramnet.io.npz import load_npz, save_npz
from vxn_ramnet.io.video import extract_evenly_spaced_frames
from vxn_ramnet.pipeline.serialization import load_encoded_sequence, save_encoded_sequence


@pytest.mark.parametrize(
    "matrix", [np.zeros((2, 4)), np.full((2, 4), np.nan), np.full((2, 4), np.inf), np.empty((0, 4))]
)
def test_unusable_embeddings_cannot_be_normalized(matrix):
    with pytest.raises(ValueError):
        l2_normalize_rows(matrix)


@pytest.mark.parametrize("chunk", [0, -1, 0.5])
def test_similarity_rejects_invalid_chunk_sizes(chunk):
    with pytest.raises(ValueError):
        flip_aware_similarity(np.eye(3), np.eye(3), np.eye(3), np.eye(3), chunk)


def test_similarity_rejects_nonunit_descriptors():
    with pytest.raises(ValueError):
        validate_embedding_pair(np.ones((2, 4)), np.ones((2, 4)), "bad")


@pytest.mark.parametrize("a,b,gap,best", [(np.nan, 0.4, 0.2, 0.6), (0.7, 0.6, 0.8, 0.7), (0.7, 0.6, 0.1, 0.9)])
def test_decision_rejects_nonfinite_or_inconsistent_evidence(a, b, gap, best):
    with pytest.raises(ValueError):
        AggregatedScores(a, b, gap, best, 0.1, 0.1)


def test_config_and_json_refuse_nonfinite_values(tmp_path):
    with pytest.raises(ValidationError):
        DecisionSettings(minimum_branch_score=float("nan"))
    with pytest.raises(ValidationError):
        DecisionSettings(unknown_score=0.8)
    with pytest.raises(ValidationError):
        EncoderSettings(weights="made-up")
    with pytest.raises(ValueError):
        atomic_write_json(tmp_path / "bad.json", {"score": float("nan")})


def test_npz_read_validation_and_expansion_limit(tmp_path):
    path = tmp_path / "bad.npz"
    np.savez_compressed(path, embeddings=np.array([float("inf")]))
    with pytest.raises(ArtifactError):
        load_npz(path)
    save_npz(path, {"embeddings": np.eye(10)})
    with pytest.raises(ArtifactError):
        load_npz(path, maximum_expanded_bytes=20)


def test_encoded_pair_identity_and_checksum_are_verified(tmp_path):
    arrays, metadata = tmp_path / "sequence.npz", tmp_path / "sequence.json"
    sequence = EncodedSequence("qa", np.eye(3, dtype=np.float32), np.eye(3, dtype=np.float32), ("1", "2", "3"), {})
    save_encoded_sequence(sequence, arrays, metadata)
    assert load_encoded_sequence("qa", arrays, metadata).embeddings.shape == (3, 3)
    with pytest.raises(ArtifactError):
        load_encoded_sequence("qb", arrays, metadata)
    content = json.loads(metadata.read_text())
    content["arrays_sha256"] = "0" * 64
    metadata.write_text(json.dumps(content))
    with pytest.raises(ArtifactError):
        load_encoded_sequence("qa", arrays, metadata)


def test_sampling_rejects_invalid_request_before_io(tmp_path):
    with pytest.raises(InputValidationError):
        extract_evenly_spaced_frames(tmp_path / "missing.avi", tmp_path / "out", 0, 3, FrameSettings())


@pytest.mark.parametrize("payload", ['{"value": NaN}', '{"value":1,"value":2}', "{invalid"])
def test_json_read_rejects_invalid_numbers_duplicates_and_syntax(tmp_path, payload):
    path = tmp_path / "invalid.json"
    path.write_text(payload)
    with pytest.raises(ArtifactError):
        read_json(path)


def test_json_read_is_bounded(tmp_path):
    path = tmp_path / "large.json"
    path.write_text('{"value": "long"}')
    with pytest.raises(ArtifactError):
        read_json(path, maximum_bytes=4)
