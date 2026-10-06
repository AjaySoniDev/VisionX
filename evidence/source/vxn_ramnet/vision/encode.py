from __future__ import annotations

import time
from pathlib import Path
from typing import Sequence

from vxn_ramnet.algorithms.similarity import validate_embedding_pair
from vxn_ramnet.core.types import EncodedSequence

from .encoders.base import VisualEncoder


def encode_sequence(sequence_id: str, frame_paths: Sequence[Path], encoder: VisualEncoder) -> EncodedSequence:
    start = time.perf_counter()
    original = encoder.encode(frame_paths, flip=False)
    flipped = encoder.encode(frame_paths, flip=True)
    original, flipped = validate_embedding_pair(original, flipped, sequence_id)
    if len(original) != len(frame_paths):
        raise ValueError("Encoder returned the wrong number of descriptors")
    elapsed = time.perf_counter() - start
    return EncodedSequence(
        sequence_id,
        original,
        flipped,
        tuple(Path(p).as_posix() for p in frame_paths),
        {
            "frame_count": len(frame_paths),
            "elapsed_seconds": elapsed,
            "average_ms_per_frame": elapsed / max(1, len(frame_paths)) * 1000,
            "encoder": encoder.manifest,
        },
    )
