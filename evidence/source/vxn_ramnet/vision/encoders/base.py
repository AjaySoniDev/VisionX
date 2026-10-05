from __future__ import annotations

from pathlib import Path
from typing import Protocol, Sequence

import numpy as np


class VisualEncoder(Protocol):
    @property
    def manifest(self) -> dict: ...
    def encode(self, frame_paths: Sequence[Path], *, flip: bool = False) -> np.ndarray: ...
