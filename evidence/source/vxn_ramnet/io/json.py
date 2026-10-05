"""Bounded JSON input that rejects duplicate fields and nonstandard numbers."""

from __future__ import annotations

import json
from pathlib import Path

from vxn_ramnet.core.exceptions import ArtifactError


def _pairs(items: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"Nonstandard JSON numeric value: {value}")


def read_json(path: Path, maximum_bytes: int = 16_000_000):
    try:
        if path.stat().st_size > maximum_bytes:
            raise ValueError("JSON input exceeds its configured byte limit")
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs, parse_constant=_constant)
    except (OSError, ValueError) as exc:
        raise ArtifactError(f"Invalid JSON artifact: {type(exc).__name__}") from exc
