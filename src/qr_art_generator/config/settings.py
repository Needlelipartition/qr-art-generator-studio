"""Typed settings loaded from TOML + env overrides."""
from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class DiffusionSettings(BaseModel):
    model_id: str = "stabilityai/sd-turbo"
    controlnet_id: str = "monster-labs/control_v1p_sd15_qrcode_monster"
    steps: int = Field(default=8, ge=1, le=50)
    guidance: float = Field(default=1.6, ge=0.0, le=10.0)
    qr_weight: float = Field(default=1.35, ge=0.0, le=3.0)
    device: str = "cuda"
    dtype: str = "float16"


class IngestSettings(BaseModel):
    max_payload_bytes: int = 2048
    allowed_schemes: list[str] = ["http", "https", "text", "wifi", "vcard"]


class RenderSettings(BaseModel):
    size: int = Field(default=768, ge=256, le=2048)
    border_modules: int = Field(default=4, ge=0, le=10)
    error_correction: str = "H"


class Settings(BaseModel):
    diffusion: DiffusionSettings = DiffusionSettings()
    ingest: IngestSettings = IngestSettings()
    render: RenderSettings = RenderSettings()
    cache_dir: Path = Path("models_cache")
    log_level: str = "INFO"


def load_settings(path: Path | None) -> Settings:
    raw: dict = {}
    if path and path.exists():
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    if env_cfg := os.environ.get("QRART_CONFIG"):
        raw.update(tomllib.loads(Path(env_cfg).read_text(encoding="utf-8")))
    if level := os.environ.get("QRART_LOG_LEVEL"):
        raw.setdefault("log_level", level)
    return Settings.model_validate(raw)