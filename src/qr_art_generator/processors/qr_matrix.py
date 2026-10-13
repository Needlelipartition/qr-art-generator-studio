"""Builds the QR ground-truth matrix the diffusion output must stay scannable against."""
from __future__ import annotations

import numpy as np
import qrcode
from qrcode.constants import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
)

from qr_art_generator.models.qr_spec import QRSpec

_EC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}


def build_qr_spec(payload: str, error_correction: str = "H", border_modules: int = 4) -> QRSpec:
    if error_correction not in _EC_MAP:
        raise ValueError(f"unknown error correction level: {error_correction!r}")
    qr = qrcode.QRCode(
        error_correction=_EC_MAP[error_correction],
        border=border_modules,
        box_size=1,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    matrix = np.asarray(qr.get_matrix(), dtype=np.uint8)
    return QRSpec(
        payload=payload,
        modules=matrix,
        error_correction=error_correction,
        border_modules=border_modules,
    )