from __future__ import annotations

from pathlib import Path
from typing import Mapping

import numpy as np

from vxn_ramnet.algorithms.similarity import normalized_centroid, validate_embedding_pair
from vxn_ramnet.core.enums import ComponentKind
from vxn_ramnet.core.exceptions import ArtifactError
from vxn_ramnet.core.version import ARTIFACT_SCHEMA_VERSION
from vxn_ramnet.io.atomic import atomic_write_json
from vxn_ramnet.io.checksums import sha256_file
from vxn_ramnet.io.json import read_json
from vxn_ramnet.io.npz import load_npz, save_npz
from vxn_ramnet.io.schema import validate_schema

from .schema import COMPONENT_ORDER, ComponentMemory, RouteMemory


class RouteMemoryStore:
    ARRAY_KEYS = {"embeddings", "flipped_embeddings", "labels", "centroids", "component_names", "source_indices"}

    @staticmethod
    def build(
        original: np.ndarray,
        flipped: np.ndarray,
        segment_map: Mapping[ComponentKind, tuple[int, ...]],
        display_names: Mapping[ComponentKind, str],
        metadata: dict,
    ) -> RouteMemory:
        original, flipped = validate_embedding_pair(original, flipped, "route-memory")
        components: dict[ComponentKind, ComponentMemory] = {}
        for kind in COMPONENT_ORDER:
            indices = np.asarray(segment_map[kind], dtype=np.int32)
            if indices.ndim != 1 or not len(indices) or np.any(indices < 0) or np.any(indices >= len(original)):
                raise ArtifactError(f"Invalid source indices for component {kind.value}")
            values = original[indices].astype(np.float32)
            values_flip = flipped[indices].astype(np.float32)
            components[kind] = ComponentMemory(
                kind, display_names[kind], values, values_flip, normalized_centroid(values), indices
            )
        meta = dict(metadata)
        meta["artifact_schema_version"] = ARTIFACT_SCHEMA_VERSION
        meta["component_order"] = [kind.value for kind in COMPONENT_ORDER]
        meta["component_counts"] = {kind.value: len(component.embeddings) for kind, component in components.items()}
        return RouteMemory(components, meta)

    @staticmethod
    def save(memory: RouteMemory, arrays_path: str | Path, metadata_path: str | Path) -> None:
        embeddings = []
        flipped = []
        labels = []
        source_indices = []
        centroids = []
        names = []
        for label, kind in enumerate(COMPONENT_ORDER):
            component = memory.components[kind]
            embeddings.append(component.embeddings)
            flipped.append(component.flipped_embeddings)
            labels.append(np.full(len(component.embeddings), label, dtype=np.int16))
            source_indices.append(component.source_indices.astype(np.int32))
            centroids.append(component.centroid)
            names.append(component.display_name)
        arrays = {
            "embeddings": np.vstack(embeddings).astype(np.float32),
            "flipped_embeddings": np.vstack(flipped).astype(np.float32),
            "labels": np.concatenate(labels),
            "centroids": np.vstack(centroids).astype(np.float32),
            "component_names": np.asarray(names, dtype="U64"),
            "source_indices": np.concatenate(source_indices).astype(np.int32),
        }
        validate_schema("route-memory-metadata.schema.json", memory.metadata)
        save_npz(arrays_path, arrays)
        atomic_write_json(metadata_path, {**memory.metadata, "arrays_sha256": sha256_file(Path(arrays_path))})

    @staticmethod
    def load(arrays_path: str | Path, metadata_path: str | Path) -> RouteMemory:
        arrays = load_npz(arrays_path, RouteMemoryStore.ARRAY_KEYS)
        try:
            metadata = read_json(Path(metadata_path))
        except Exception as exc:
            raise ArtifactError(f"Could not read route-memory metadata: {exc}") from exc
        if not isinstance(metadata, dict):
            raise ArtifactError("Route-memory metadata must be a JSON object")
        if metadata.get("artifact_schema_version") != ARTIFACT_SCHEMA_VERSION:
            raise ArtifactError(f"Unsupported route-memory schema: {metadata.get('artifact_schema_version')}")
        validate_schema("route-memory-metadata.schema.json", metadata)
        if metadata.get("arrays_sha256") and metadata["arrays_sha256"] != sha256_file(Path(arrays_path)):
            raise ArtifactError("Route-memory arrays do not match their metadata checksum")
        if metadata["component_order"] != [kind.value for kind in COMPONENT_ORDER]:
            raise ArtifactError("Unsupported component order")
        for key in ("labels", "source_indices"):
            if arrays[key].ndim != 1 or not np.issubdtype(arrays[key].dtype, np.integer):
                raise ArtifactError(f"Invalid integer vector: {key}")
        if (
            np.any(arrays["labels"] < 0)
            or np.any(arrays["labels"] >= 5)
            or np.any(arrays["source_indices"] < 0)
            or np.any(arrays["source_indices"] > 2_147_483_647)
        ):
            raise ArtifactError("Route-memory contains out-of-range integer values")
        emb = arrays["embeddings"].astype(np.float32)
        flip = arrays["flipped_embeddings"].astype(np.float32)
        labels = arrays["labels"].astype(np.int16)
        centroids = arrays["centroids"].astype(np.float32)
        names = arrays["component_names"].astype(str)
        indices = arrays["source_indices"].astype(np.int32)
        if (
            emb.ndim != 2
            or flip.shape != emb.shape
            or centroids.shape != (5, emb.shape[1])
            or names.shape != (5,)
            or len(emb) != len(labels)
            or len(emb) != len(indices)
        ):
            raise ArtifactError("Route-memory array shapes are inconsistent")
        if not np.all(np.isfinite(emb)) or not np.all(np.isfinite(flip)) or not np.all(np.isfinite(centroids)):
            raise ArtifactError("Route-memory contains non-finite numeric values")
        if np.any(labels < 0) or np.any(labels >= 5) or np.any(indices < 0):
            raise ArtifactError("Route-memory contains invalid labels or indices")
        try:
            validate_embedding_pair(emb, flip, "loaded-memory")
            validate_embedding_pair(centroids, centroids, "loaded-centroids")
        except ValueError as exc:
            raise ArtifactError(str(exc)) from exc
        components = {}
        for label, kind in enumerate(COMPONENT_ORDER):
            mask = labels == label
            if not np.any(mask):
                raise ArtifactError(f"Route-memory component is empty: {kind.value}")
            if metadata["component_counts"] and metadata["component_counts"].get(kind.value) != int(mask.sum()):
                raise ArtifactError(f"Component count mismatch: {kind.value}")
            components[kind] = ComponentMemory(
                kind, str(names[label]), emb[mask], flip[mask], centroids[label], indices[mask]
            )
        return RouteMemory(components, metadata)
