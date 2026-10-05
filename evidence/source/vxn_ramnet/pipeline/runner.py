from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from vxn_ramnet.config.models import PipelineConfig
from vxn_ramnet.core.exceptions import ArtifactError, StageExecutionError
from vxn_ramnet.core.types import EncodedSequence
from vxn_ramnet.core.version import ARTIFACT_SCHEMA_VERSION
from vxn_ramnet.io.atomic import atomic_write_json
from vxn_ramnet.io.checksums import sha256_file, short_digest
from vxn_ramnet.io.paths import is_within, remove_managed_subdirectory
from vxn_ramnet.io.video import extract_evenly_spaced_frames, inspect_video
from vxn_ramnet.memory.store import RouteMemoryStore
from vxn_ramnet.observability import build_run_manifest, configure_logging
from vxn_ramnet.observability.manifest import dependency_versions
from vxn_ramnet.observability.provenance import canonical_digest, source_identity
from vxn_ramnet.recognition import RouteRecognizer, learn_route_memory
from vxn_ramnet.reporting import write_final_reports
from vxn_ramnet.vision import EfficientNetB0VisualEncoder, VisualEncoder, encode_sequence

from .artifacts import ArtifactStore
from .serialization import load_encoded_sequence, save_encoded_sequence


@dataclass(frozen=True)
class PipelineResult:
    run_id: str
    run_directory: Path
    report_files: dict[str, str]
    summary: dict[str, Any]


def _generated_run_id(config: PipelineConfig) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    identity = "|".join([config.learning_video.id, *[q.id for q in config.query_videos], timestamp])
    return f"run-{timestamp}-{short_digest(identity, 6)}"


class VxnPipeline:
    """Reproducible runner for the constrained camera-only VXN-RAMNet baseline.

    The encoder is injectable, allowing deterministic unit/integration tests without
    TensorFlow. The production default is a frozen EfficientNetB0 adapter.
    """

    def __init__(self, config: PipelineConfig, encoder: VisualEncoder | None = None):
        self.config = config
        self._encoder = encoder
        self.logger = logging.getLogger("vxn_ramnet")

    def _preflight(self) -> tuple[dict, dict[str, Path]]:
        inputs = {self.config.learning_video.id: self.config.resolve_input(self.config.learning_video)}
        inputs.update({item.id: self.config.resolve_input(item) for item in self.config.query_videos})
        resolved = list(inputs.values())
        if any(is_within(path, self.config.resolved_output_root) for path in resolved):
            raise ValueError("Inputs cannot be stored inside the managed output root")
        if len({path.resolve() for path in resolved}) != len(resolved):
            raise ValueError("Each sequence must reference a distinct video file")
        reports = {key: asdict(inspect_video(path, self.config.frames)) for key, path in inputs.items()}
        for report in reports.values():
            report["path"] = Path(report["path"]).as_posix()
        return {"validated_at": datetime.now(timezone.utc).isoformat(), "videos": reports}, inputs

    def _encoder_instance(self) -> VisualEncoder:
        if self._encoder is None:
            self._encoder = EfficientNetB0VisualEncoder(self.config.encoder)
        return self._encoder

    def _extract(self, store: ArtifactStore, inputs: dict[str, Path]) -> dict:
        layout = store.layout
        report_path = layout.frame_report
        if self.config.artifacts.resume and store.is_complete("01-frame-extraction", [report_path]):
            cached = json.loads(report_path.read_text(encoding="utf-8"))
            embedding_outputs = list(self._embedding_paths(layout, self.config.learning_video.id, True))
            for item in self.config.query_videos:
                embedding_outputs.extend(self._embedding_paths(layout, item.id, False))
            frame_paths = cached["learning"]["frame_paths"] + [
                p for q in cached["queries"].values() for p in q["frame_paths"]
            ]
            if store.is_complete("02-visual-encoding", embedding_outputs) or all(
                Path(p).is_file() and sha256_file(Path(p)) == cached["frame_sha256"][p] for p in frame_paths
            ):
                return cached
        with store.stage("01-frame-extraction", [report_path]):
            learning_dir = layout.frames / "learning" / self.config.learning_video.id
            learning = extract_evenly_spaced_frames(
                inputs[self.config.learning_video.id],
                learning_dir,
                self.config.frames.learning_count,
                self.config.frames.learning_max_seconds,
                self.config.frames,
            )
            queries = {}
            for item in self.config.query_videos:
                queries[item.id] = extract_evenly_spaced_frames(
                    inputs[item.id],
                    layout.frames / "queries" / item.id,
                    self.config.frames.query_count,
                    self.config.frames.query_max_seconds,
                    self.config.frames,
                )
            report = {
                "schema_version": ARTIFACT_SCHEMA_VERSION,
                "learning": {"id": self.config.learning_video.id, **learning},
                "queries": queries,
            }
            report["frame_sha256"] = {
                p: sha256_file(Path(p))
                for p in learning["frame_paths"] + [p for q in queries.values() for p in q["frame_paths"]]
            }
            atomic_write_json(report_path, report)
            return report

    def _embedding_paths(self, layout, sequence_id: str, learning: bool = False) -> tuple[Path, Path]:
        base = layout.embeddings / ("learning" if learning else "queries")
        return base / f"{sequence_id}.npz", base / f"{sequence_id}.json"

    def _encode(
        self, store: ArtifactStore, frame_report: dict
    ) -> tuple[EncodedSequence, dict[str, EncodedSequence], dict]:
        layout = store.layout
        all_outputs = []
        learn_arrays, learn_meta = self._embedding_paths(layout, self.config.learning_video.id, True)
        all_outputs += [learn_arrays, learn_meta]
        for item in self.config.query_videos:
            all_outputs += list(self._embedding_paths(layout, item.id, False))
        if self.config.artifacts.resume and store.is_complete("02-visual-encoding", all_outputs):
            learning = load_encoded_sequence(self.config.learning_video.id, learn_arrays, learn_meta)
            queries = {
                item.id: load_encoded_sequence(item.id, *self._embedding_paths(layout, item.id, False))
                for item in self.config.query_videos
            }
            return learning, queries, learning.metadata.get("encoder", {})
        with store.stage("02-visual-encoding", all_outputs):
            encoder = self._encoder_instance()
            learning_frames = [Path(path) for path in frame_report["learning"]["frame_paths"]]
            learning = encode_sequence(self.config.learning_video.id, learning_frames, encoder)
            learning.metadata["sampling"] = {
                key: frame_report["learning"][key]
                for key in ("source_frame_indices", "source_timestamps_seconds", "timestamp_semantics")
            }
            save_encoded_sequence(learning, learn_arrays, learn_meta)
            queries = {}
            for item in self.config.query_videos:
                frames = [Path(path) for path in frame_report["queries"][item.id]["frame_paths"]]
                sequence = encode_sequence(item.id, frames, encoder)
                sequence.metadata["sampling"] = {
                    key: frame_report["queries"][item.id][key]
                    for key in ("source_frame_indices", "source_timestamps_seconds", "timestamp_semantics")
                }
                save_encoded_sequence(sequence, *self._embedding_paths(layout, item.id, False))
                queries[item.id] = sequence
            return learning, queries, encoder.manifest

    def _learn_memory(self, store: ArtifactStore, learning: EncodedSequence):
        layout = store.layout
        outputs = [layout.memory_arrays, layout.memory_metadata]
        if self.config.artifacts.save_self_similarity_matrix:
            outputs.append(layout.root / "memory" / "self-similarity.npz")
        if self.config.artifacts.resume and store.is_complete("03-route-memory", outputs):
            return RouteMemoryStore.load(layout.memory_arrays, layout.memory_metadata)
        with store.stage("03-route-memory", outputs):
            memory, similarity = learn_route_memory(
                learning,
                self.config.detection,
                self.config.branch_a_name,
                self.config.branch_b_name,
                fail_on_degraded_graph=self.config.runtime.fail_on_degraded_graph,
            )
            RouteMemoryStore.save(memory, layout.memory_arrays, layout.memory_metadata)
            if self.config.artifacts.save_self_similarity_matrix:
                from vxn_ramnet.io.npz import save_npz

                save_npz(outputs[-1], {"self_similarity": similarity.astype(np.float32)})
            return memory

    def _classify_query(self, query: EncodedSequence, memory) -> dict:
        # Compatibility wrapper; new integrations use RouteRecognizer directly.
        return RouteRecognizer(
            self.config.decision,
            self.config.detection,
            self.config.branch_a_name,
            self.config.branch_b_name,
        ).classify(query, memory)

    def _classify(self, store: ArtifactStore, queries: dict[str, EncodedSequence], memory) -> list[dict]:
        output = store.layout.reports / "query-decisions.json"
        query_paths = [store.layout.reports / "queries" / f"{query_id}.json" for query_id in queries]
        if self.config.artifacts.resume and store.is_complete("04-query-classification", [output, *query_paths]):
            return json.loads(output.read_text(encoding="utf-8"))["queries"]
        with store.stage("04-query-classification", [output, *query_paths]):
            reports = []
            for query_id, sequence in queries.items():
                report = self._classify_query(sequence, memory)
                reports.append(report)
                atomic_write_json(store.layout.reports / "queries" / f"{query_id}.json", report)
            atomic_write_json(output, {"schema_version": ARTIFACT_SCHEMA_VERSION, "queries": reports})
            return reports

    def run(self) -> PipelineResult:
        preflight, inputs = self._preflight()  # all inputs are validated before any managed output is removed/created
        run_id = self.config.artifacts.run_id or _generated_run_id(self.config)
        np.random.seed(self.config.runtime.deterministic_seed)
        encoder_identity = self._encoder_instance().manifest
        if self.config.artifacts.resume and self.config.artifacts.run_id is None:
            raise ValueError("resume requires an explicit artifacts.run_id")
        store = ArtifactStore.create(
            self.config.resolved_output_root,
            run_id,
            self.config.artifacts.overwrite_existing_run,
            self.config.artifacts.resume,
            self.config.runtime.include_diagnostic_details,
        )
        self.logger = configure_logging(self.config.runtime.log_level, store.layout.logs)
        config_identity = self.config.model_dump(mode="json")
        for field in ("resume", "overwrite_existing_run"):
            config_identity["artifacts"].pop(field)
        identity = {
            "config": config_identity,
            "inputs": {key: sha256_file(path) for key, path in inputs.items()},
            "source_sha256": source_identity()["sha256"],
            "encoder": encoder_identity,
            "dependencies": dependency_versions(
                ["numpy", "opencv-python-headless", "Pillow", "pydantic", "tensorflow"]
            ),
        }
        identity_path = store.layout.root / "resume-identity.json"
        identity_payload = {"sha256": canonical_digest(identity), "identity": identity}
        if self.config.artifacts.resume:
            if not identity_path.is_file() or json.loads(identity_path.read_text(encoding="utf-8")) != identity_payload:
                raise ArtifactError(
                    "Resume identity mismatch or legacy run: use a fresh run ID; no cached files were changed"
                )
        else:
            atomic_write_json(identity_path, identity_payload)
        if not self.config.artifacts.resume:
            atomic_write_json(store.layout.config, self.config.model_dump(mode="json"))
            atomic_write_json(store.layout.preflight, preflight)
        self.logger.info("Starting VXN-RAMNet run %s", run_id)
        try:
            frame_report = self._extract(store, inputs)
            learning, queries, model_manifest = self._encode(store, frame_report)
            if not self.config.artifacts.resume or not store.layout.manifest.is_file():
                atomic_write_json(store.layout.manifest, build_run_manifest(run_id, inputs, model_manifest))
            memory = self._learn_memory(store, learning)
            query_reports = self._classify(store, queries, memory)
            summary = {
                "schema_version": ARTIFACT_SCHEMA_VERSION,
                "run_id": run_id,
                "system": "VXN-RAMNet",
                "implementation_status": "camera-only constrained research baseline",
                "route_memory": memory.metadata,
                "query_results": query_reports,
            }
            with store.stage(
                "05-reporting",
                [store.layout.reports / name for name in ("summary.json", "query-results.csv", "report.md")],
            ):
                report_files = write_final_reports(store.layout.reports, summary)
            if not self.config.artifacts.save_frames:
                remove_managed_subdirectory(store.layout.frames, store.layout.root)
            final = json.loads(Path(report_files["json"]).read_text(encoding="utf-8"))
            self.logger.info("Run complete: %s", report_files["markdown"])
            return PipelineResult(run_id, store.layout.root, report_files, final)
        except Exception as exc:
            if self.config.runtime.include_diagnostic_details:
                self.logger.exception("Pipeline failed")
            else:
                self.logger.error("Pipeline failed (%s). Diagnostic details are redacted.", type(exc).__name__)
            raise StageExecutionError(
                f"Pipeline failed in run {run_id} ({type(exc).__name__}). Review the stage state and local log."
            ) from exc


def run_pipeline(config: PipelineConfig, encoder: VisualEncoder | None = None) -> PipelineResult:
    return VxnPipeline(config, encoder).run()
