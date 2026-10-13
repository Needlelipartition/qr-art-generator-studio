"""Maps driver name -> driver instance. Extend by adding to _DRIVERS."""
from __future__ import annotations

from qr_art_generator.drivers.base import OutputDriver
from qr_art_generator.drivers.png_driver import PngDriver
from qr_art_generator.drivers.svg_driver import SvgDriver


def build_output_drivers() -> dict[str, OutputDriver]:
    drivers: list[OutputDriver] = [PngDriver(), SvgDriver()]
    return {d.name: d for d in drivers}
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>