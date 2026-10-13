"""Diffusion + ControlNet processor. Turns a QR spec + prompt into an image tensor."""
from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import torch

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class DiffusionConfig:
    model_id: str
    controlnet_id: str
    steps: int
    guidance: float
    qr_weight: float
    device: str
    dtype: str


class DiffusionProcessor:
    """Lazily loads SD + QR ControlNet and renders one image per call."""

    def __init__(self, config: DiffusionConfig) -> None:
        self.config = config
        self._pipe = None

    def _ensure_pipe(self) -> None:
        if self._pipe is not None:
            return
        from diffusers import ControlNetModel, StableDiffusionControlNetPipeline

        torch_dtype = torch.float16 if self.config.dtype == "float16" else torch.float32
        controlnet = ControlNetModel.from_pretrained(
            self.config.controlnet_id, torch_dtype=torch_dtype
        )
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            self.config.model_id, controlnet=controlnet, torch_dtype=torch_dtype
        )
        pipe = pipe.to(self.config.device)
        pipe.set_progress_bar_config(disable=True)
        self._pipe = pipe
        logger.info("diffusion pipeline loaded on %s", self.config.device)

    def render(self, qr_condition: np.ndarray, prompt: str, seed: int) -> np.ndarray:
        """qr_condition: (H,W,3) float in [0,1]. Returns (H,W,3) uint8 RGB."""
        self._ensure_pipe()
        generator = torch.Generator(device=self.config.device).manual_seed(seed)
        cond = torch.from_numpy(qr_condition).permute(2, 0, 1).unsqueeze(0)
        cond = cond.to(self.config.device, dtype=torch.float16 if self.config.dtype == "float16" else torch.float32)
        image = self._pipe(
            prompt=prompt,
            image=cond,
            num_inference_steps=self.config.steps,
            guidance_scale=self.config.guidance,
            controlnet_conditioning_scale=self.config.qr_weight,
            generator=generator,
        ).images[0]
        return np.asarray(image, dtype=np.uint8)