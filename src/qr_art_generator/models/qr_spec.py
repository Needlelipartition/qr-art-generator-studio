"""Canonical QR spec: the ground truth the diffusion output must respect."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class QRSpec:
    payload: str
    modules: np.ndarray          # (N, N) uint8, 1 = dark module
    error_correction: str
    border_modules: int

    @property
    def module_count(self) -> int:
        return int(self.modules.shape[0])

    def scaled(self, size: int) -> np.ndarray:
        """Nearest-neighbour upscale to `size` px, returns (size,size) float in [0,1]."""
        n = self.module_count
        rep = max(1, size // n)
        big = np.kron(self.modules, np.ones((rep, rep), dtype=np.uint8))
        return big.astype(np.float32)