from __future__ import annotations

from pathlib import Path

import numpy as np

from vxn_ramnet.algorithms.similarity import validate_embedding_pair
from vxn_ramnet.core.exceptions import ArtifactError
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.io.atomic import atomic_write_json
from vxn_ramnet.io.checksums import sha256_file
from vxn_ramnet.io.json import read_json
from vxn_ramnet.io.npz import load_npz, save_npz


def save_encoded_sequence(sequence: EncodedSequence, arrays_path: Path, metadata_path: Path) -> None:
    validate_embedding_pair(sequence.embeddings, sequence.flipped_embeddings, sequence.sequence_id)
    if len(sequence.frame_paths) != len(sequence.embeddings):
        raise ArtifactError("Frame-path count differs from embeddings")
    max_len = max(1, max((len(path) for path in sequence.frame_paths), default=1))
    save_npz(
        arrays_path,
        {
            "embeddings": sequence.embeddings.astype(np.float32),
            "flipped_embeddings": sequence.flipped_embeddings.astype(np.float32),
            "frame_paths": np.asarray(sequence.frame_paths, dtype=f"U{max_len}"),
        },
    )
    atomic_write_json(
        metadata_path,
        {**sequence.metadata, "sequence_id": sequence.sequence_id, "arrays_sha256": sha256_file(arrays_path)},
    )


def load_encoded_sequence(sequence_id: str, arrays_path: Path, metadata_path: Path) -> EncodedSequence:
    arrays = load_npz(arrays_path, {"embeddings", "flipped_embeddings", "frame_paths"})
    metadata = read_json(metadata_path)
    if metadata.get("sequence_id") != sequence_id:
        raise ArtifactError("Encoded sequence identity mismatch")
    if metadata.get("arrays_sha256") and metadata["arrays_sha256"] != sha256_file(arrays_path):
        raise ArtifactError("Encoded arrays checksum does not match metadata")
    validate_embedding_pair(arrays["embeddings"], arrays["flipped_embeddings"], sequence_id)
    if arrays["embeddings"].shape != arrays["flipped_embeddings"].shape:
        raise ValueError("Original/flipped embedding shapes differ")
    if len(arrays["frame_paths"]) != len(arrays["embeddings"]):
        raise ValueError("Frame path count differs from embedding count")
    return EncodedSequence(
        sequence_id,
        arrays["embeddings"].astype(np.float32),
        arrays["flipped_embeddings"].astype(np.float32),
        tuple(arrays["frame_paths"].astype(str).tolist()),
        metadata,
    )
