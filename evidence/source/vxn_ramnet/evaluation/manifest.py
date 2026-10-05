from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from vxn_ramnet.algorithms.similarity import validate_embedding_pair
from vxn_ramnet.config.models import DetectionSettings, Identifier, StrictModel
from vxn_ramnet.core.exceptions import InputValidationError
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.io.checksums import sha256_file
from vxn_ramnet.io.json import read_json
from vxn_ramnet.io.npz import load_npz

Label = Literal["BRANCH_A", "BRANCH_B", "UNKNOWN", "AMBIGUOUS"]


class SequenceRecord(StrictModel):
    id: Identifier
    path: Path
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    session_id: str = Field(min_length=1)
    split: Literal["enrollment", "development", "calibration", "test", "regression", "synthetic"]
    expected_label: Label | None = None


class EventAnnotations(StrictModel):
    first_junction_index: int = Field(ge=0)
    turnaround_index: int = Field(ge=0)
    return_junction_index: int = Field(ge=0)
    provenance: str = Field(min_length=1)

    @model_validator(mode="after")
    def ordered(self) -> EventAnnotations:
        if not self.first_junction_index < self.turnaround_index < self.return_junction_index:
            raise ValueError("Event annotations must follow the enrollment order")
        return self


class DatasetManifest(StrictModel):
    schema_version: Literal["1.0.0"] = "1.0.0"
    dataset_id: Identifier
    purpose: Literal["regression", "synthetic", "held_out"]
    root: Path = Path(".")
    provenance: str = Field(min_length=1)
    encoder_provenance: str = Field(min_length=1)
    learning: SequenceRecord
    queries: list[SequenceRecord] = Field(min_length=1)
    expected_events: EventAnnotations | None = None
    detection: DetectionSettings = Field(default_factory=DetectionSettings)
    maximum_total_embedding_bytes: int = Field(default=512_000_000, ge=1_000_000, le=4_000_000_000)

    @model_validator(mode="after")
    def validate_design(self) -> DatasetManifest:
        records = [self.learning, *self.queries]
        if len({r.id for r in records}) != len(records):
            raise ValueError("Sequence IDs must be unique")
        if len({r.sha256 for r in records}) != len(records):
            raise ValueError("Identical cached files cannot serve as distinct evaluation journeys")
        if any(r.expected_label is None for r in self.queries):
            raise ValueError("Every query needs a predeclared expected label")
        if self.purpose == "held_out":
            if any(r.split != "test" for r in self.queries):
                raise ValueError("Held-out evaluation requires frozen test queries")
            if any(r.session_id == self.learning.session_id for r in self.queries):
                raise ValueError("Enrollment and test queries must use separate acquisition sessions")
            if self.learning.split != "enrollment":
                raise ValueError("Learning record must identify enrollment data")
        return self


def load_dataset(path: Path) -> tuple[DatasetManifest, EncodedSequence, dict[str, EncodedSequence]]:
    manifest = DatasetManifest.model_validate(read_json(path))
    root = (path.parent / manifest.root).resolve()
    loaded: dict[str, EncodedSequence] = {}
    resolved_paths = set()
    content_digests = set()
    total_bytes = 0
    for record in [manifest.learning, *manifest.queries]:
        candidate = (root / record.path).resolve()
        if record.path.is_absolute() or not candidate.is_relative_to(root) or candidate in resolved_paths:
            raise InputValidationError("Dataset paths must be distinct and contained within the declared root")
        resolved_paths.add(candidate)
        if sha256_file(candidate) != record.sha256:
            raise InputValidationError(f"Dataset checksum mismatch for {record.id}")
        arrays = load_npz(candidate, {"embeddings", "flipped_embeddings"})
        original, flipped = validate_embedding_pair(arrays["embeddings"], arrays["flipped_embeddings"], record.id)
        total_bytes += original.nbytes + flipped.nbytes
        if total_bytes > manifest.maximum_total_embedding_bytes:
            raise InputValidationError("Dataset exceeds its total embedding memory budget")
        if len(original) > (2000 if record.id == manifest.learning.id else 1000) or original.shape[1] > 8192:
            raise InputValidationError("Dataset exceeds supported frame/dimension bounds")
        if len(original) < (40 if record.id == manifest.learning.id else 20):
            raise InputValidationError(f"Insufficient frames for {record.id}")
        # Also reject duplicate arrays compressed into different NPZ containers.
        import hashlib

        digest = hashlib.sha256(original.tobytes() + flipped.tobytes()).hexdigest()
        if digest in content_digests:
            raise InputValidationError("Duplicate embedding content detected across journeys")
        content_digests.add(digest)
        loaded[record.id] = EncodedSequence(
            record.id, original, flipped, (), {"encoder": {"provenance": manifest.encoder_provenance}}
        )
    learning = loaded.pop(manifest.learning.id)
    if any(sequence.embeddings.shape[1] != learning.embeddings.shape[1] for sequence in loaded.values()):
        raise InputValidationError("Learning and query descriptor dimensions differ")
    if manifest.expected_events and manifest.expected_events.return_junction_index >= len(learning.embeddings):
        raise InputValidationError("Event annotation exceeds enrollment length")
    return manifest, learning, loaded
