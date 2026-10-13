"""Output driver base — every driver takes a final RGB array and writes bytes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

import numpy as np


class OutputDriver(ABC):
    name: str = "base"
    extension: str = "bin"

    @abstractmethod
    def write(self, image: np.ndarray, out_path: Path) -> Path: ...