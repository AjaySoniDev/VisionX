from __future__ import annotations

import os
import platform
import sys
import sysconfig
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Iterable

from vxn_ramnet.core.version import __version__
from vxn_ramnet.io.checksums import sha256_file

from .provenance import git_identity, source_identity


def host_hardware() -> dict:
    cpu_name = platform.processor()
    if sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                cpu_name = str(winreg.QueryValueEx(key, "ProcessorNameString")[0]).strip()
        except (ImportError, OSError):
            pass
    build_platform = sysconfig.get_platform()
    process_arch = (
        "AMD64" if build_platform == "win-amd64" else "ARM64" if build_platform == "win-arm64" else build_platform
    )
    host_arch = os.environ.get("PROCESSOR_ARCHITEW6432") or platform.machine()
    return {
        "cpu_model": cpu_name,
        "logical_processors": os.cpu_count(),
        "process_architecture": process_arch,
        "host_architecture": host_arch,
        "architecture_mismatch": process_arch.lower().replace("x86_64", "amd64").replace("aarch64", "arm64")
        != host_arch.lower().replace("x86_64", "amd64").replace("aarch64", "arm64")
        if sys.platform == "win32"
        else None,
        "note": "Architecture mismatch may indicate emulation; timings are specific to this environment.",
    }


def dependency_versions(names: Iterable[str]) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for name in names:
        try:
            result[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            result[name] = None
    return result


def build_run_manifest(run_id: str, input_paths: dict[str, Path], model_manifest: dict | None = None) -> dict:
    return {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "vxn_ramnet_version": __version__,
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "process_id": os.getpid(),
        "dependencies": dependency_versions(
            ["numpy", "opencv-python-headless", "Pillow", "pydantic", "PyYAML", "tensorflow"]
        ),
        "source": source_identity(),
        "git": git_identity(Path(__file__).resolve().parents[3]),
        "processor": platform.processor(),
        "hardware": host_hardware(),
        "thread_environment": {
            key: os.environ.get(key) for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
        },
        "inputs": {
            key: {"path": path.as_posix(), "sha256": sha256_file(path), "bytes": path.stat().st_size}
            for key, path in input_paths.items()
        },
        "model": model_manifest,
    }
