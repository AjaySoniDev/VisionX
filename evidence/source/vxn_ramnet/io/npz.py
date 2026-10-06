from __future__ import annotations

import io
from pathlib import Path
from typing import Any, Mapping
from zipfile import ZipFile

import numpy as np

from vxn_ramnet.core.exceptions import ArtifactError

from .atomic import atomic_write_bytes


def save_npz(path: str | Path, arrays: Mapping[str, np.ndarray]) -> Path:
    for key, value in arrays.items():
        arr = np.asarray(value)
        if arr.dtype.hasobject:
            raise ArtifactError(f"Object arrays are forbidden in safe NPZ artifacts: {key}")
        if np.issubdtype(arr.dtype, np.floating) and not np.all(np.isfinite(arr)):
            raise ArtifactError(f"Non-finite values in array: {key}")
    buffer = io.BytesIO()
    payload: dict[str, Any] = dict(arrays)
    np.savez_compressed(buffer, **payload)
    return atomic_write_bytes(path, buffer.getvalue())


def load_npz(
    path: str | Path, required: set[str] | None = None, *, maximum_expanded_bytes: int = 512_000_000
) -> dict[str, np.ndarray]:
    source = Path(path)
    if not source.is_file():
        raise ArtifactError(f"NPZ artifact not found: {source}")
    try:
        with ZipFile(source) as archive:
            members = archive.infolist()
            if sum(member.file_size for member in members) > maximum_expanded_bytes:
                raise ArtifactError("NPZ expanded content exceeds the configured limit")
            if len({member.filename for member in members}) != len(members):
                raise ArtifactError("NPZ contains duplicate members")
        with np.load(source, allow_pickle=False) as data:
            result = {key: data[key] for key in data.files}
        for key, value in result.items():
            if value.dtype.hasobject or (np.issubdtype(value.dtype, np.number) and not np.all(np.isfinite(value))):
                raise ArtifactError(f"Unsafe numeric or object array: {key}")
    except Exception as exc:
        raise ArtifactError(f"Unsafe or corrupt NPZ artifact {source}: {exc}") from exc
    missing = (required or set()) - result.keys()
    if missing:
        raise ArtifactError(f"NPZ artifact {source} is missing keys: {sorted(missing)}")
    return result
