"""Content identities independent of checkout location and Git availability."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from vxn_ramnet.io.checksums import sha256_file


def source_identity() -> dict:
    package = Path(__file__).resolve().parents[1]
    files = {
        path.relative_to(package).as_posix(): sha256_file(path)
        for path in sorted(package.rglob("*"))
        if path.is_file() and path.suffix in {".py", ".json"}
    }
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {"sha256": digest, "files": files}


def git_identity(directory: Path) -> dict:
    # Only record a repository whose tracked root contains this package.
    try:
        commit = subprocess.run(
            ["git", "-C", str(directory), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(directory), "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        ).stdout
        return {"commit": commit, "dirty": bool(status)}
    except (OSError, subprocess.SubprocessError):
        return {"commit": None, "dirty": None, "reason": "No usable Git checkout; source SHA-256 is authoritative"}


def canonical_digest(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()
