"""SVG output driver — embeds the raster as a base64 <image>, escapes payload."""
from __future__ import annotations

import base64
import html
import io
from pathlib import Path

import numpy as np
from PIL import Image


class SvgDriver:
    name = "svg"
    extension = "svg"

    def __init__(self, title: str = "qr-art") -> None:
        self.title = title

    def write(self, image: np.ndarray, out_path: Path) -> Path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        buf = io.BytesIO()
        Image.fromarray(image, mode="RGB").save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        h, w = image.shape[:2]
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">\n'
            f"  <title>{html.escape(self.title)}</title>\n"
            f'  <image width="{w}" height="{h}" '
            f'href="data:image/png;base64,{b64}"/>\n'
            f"</svg>\n"
        )
        out_path.write_text(svg, encoding="utf-8")
        return out_path