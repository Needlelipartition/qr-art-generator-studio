"""PNG output driver — the default gallery format."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


class PngDriver:
    name = "png"
    extension = "png"

    def __init__(self, compress_level: int = 6) -> None:
        self.compress_level = compress_level

    def write(self, image: np.ndarray, out_path: Path) -> Path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.fromarray(image, mode="RGB")
        img.save(out_path, format="PNG", compress_level=self.compress_level)
        return out_path