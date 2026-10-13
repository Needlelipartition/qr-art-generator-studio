"""Job + result dataclasses passed between pipeline stages."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ArtJob:
    payload: str
    prompt: str
    output_dir: Path
    seed: int | None = None
    job_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ArtResult:
    job_id: str
    image_path: Path
    scan_score: float
    elapsed_ms: int
    seed_used: int