from __future__ import annotations

import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from vxn_ramnet.core.enums import StageStatus
from vxn_ramnet.io.atomic import atomic_write_json
from vxn_ramnet.io.checksums import sha256_file
from vxn_ramnet.io.paths import is_within, prepare_run_directory, validate_identifier


@dataclass(frozen=True)
class RunLayout:
    root: Path

    @property
    def config(self) -> Path:
        return self.root / "config.snapshot.json"

    @property
    def manifest(self) -> Path:
        return self.root / "manifest.json"

    @property
    def preflight(self) -> Path:
        return self.root / "inputs" / "preflight.json"

    @property
    def frames(self) -> Path:
        return self.root / "frames"

    @property
    def frame_report(self) -> Path:
        return self.root / "inputs" / "frame-extraction.json"

    @property
    def embeddings(self) -> Path:
        return self.root / "embeddings"

    @property
    def memory_arrays(self) -> Path:
        return self.root / "memory" / "route-memory.npz"

    @property
    def memory_metadata(self) -> Path:
        return self.root / "memory" / "route-memory.json"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    @property
    def logs(self) -> Path:
        return self.root / "logs" / "pipeline.jsonl"

    @property
    def stages(self) -> Path:
        return self.root / "stages"


class ArtifactStore:
    def __init__(self, layout: RunLayout, include_diagnostic_details: bool = False):
        self.layout = layout
        self.include_diagnostic_details = include_diagnostic_details

    @classmethod
    def create(
        cls,
        output_root: Path,
        run_id: str,
        overwrite: bool,
        resume: bool = False,
        include_diagnostic_details: bool = False,
    ) -> "ArtifactStore":
        validate_identifier(run_id)
        candidate = (output_root / run_id).resolve()
        if resume:
            if candidate == output_root.resolve() or not is_within(candidate, output_root):
                raise ValueError("Resume directory escapes the configured output root")
            if not (candidate / ".vxn-run").is_file():
                raise FileNotFoundError(f"Cannot resume unmanaged or missing run: {candidate}")
            return cls(RunLayout(candidate), include_diagnostic_details)
        return cls(
            RunLayout(prepare_run_directory(output_root, run_id, overwrite)),
            include_diagnostic_details,
        )

    def stage_state_path(self, name: str) -> Path:
        validate_identifier(name if not name[:1].isdigit() else "stage-" + name)
        return self.layout.stages / f"{name}.json"

    def is_complete(self, name: str, outputs: list[Path]) -> bool:
        import json

        state = self.stage_state_path(name)
        if not state.is_file() or not all(path.exists() for path in outputs):
            return False
        try:
            payload = json.loads(state.read_text(encoding="utf-8"))
            digests = payload.get("output_sha256", {})
            if payload.get("status") != StageStatus.SUCCEEDED or not digests:
                return False
            for relative, digest in digests.items():
                path = (self.layout.root / relative).resolve()
                if not is_within(path, self.layout.root) or not path.is_file() or sha256_file(path) != digest:
                    return False
            return all(path.relative_to(self.layout.root).as_posix() in digests for path in outputs)
        except Exception:
            return False

    @contextmanager
    def stage(self, name: str, outputs: list[Path] | None = None):
        started = datetime.now(timezone.utc)
        clock_start = time.perf_counter()
        # Recomputing a stage invalidates later caches, even if output names match.
        if self.layout.stages.exists():
            for path in self.layout.stages.glob("*.json"):
                if path.stem > name:
                    path.unlink()
        atomic_write_json(
            self.stage_state_path(name),
            {
                "stage": name,
                "status": StageStatus.RUNNING,
                "started_at": started.isoformat(),
            },
        )
        try:
            yield
            output_sha256 = {}
            for path in outputs or []:
                if not is_within(path, self.layout.root) or not path.is_file():
                    raise ValueError("Stage output must be a file inside its run directory")
                output_sha256[path.relative_to(self.layout.root).as_posix()] = sha256_file(path)
        except Exception as exc:
            payload = {
                "stage": name,
                "status": StageStatus.FAILED,
                "started_at": started.isoformat(),
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "error_type": type(exc).__name__,
                "error": "Diagnostic details are redacted by default.",
                "elapsed_seconds": time.perf_counter() - clock_start,
            }
            if self.include_diagnostic_details:
                payload["error"] = str(exc)
                payload["traceback"] = traceback.format_exc()
            atomic_write_json(self.stage_state_path(name), payload)
            raise
        else:
            atomic_write_json(
                self.stage_state_path(name),
                {
                    "stage": name,
                    "status": StageStatus.SUCCEEDED,
                    "started_at": started.isoformat(),
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "elapsed_seconds": time.perf_counter() - clock_start,
                    "output_sha256": output_sha256,
                },
            )
