"""Fallback handler — normalizes free text payloads."""
from __future__ import annotations

from qr_art_generator.ingest.base import IngestError, IngestHandler
from qr_art_generator.models.job import ArtJob


class TextHandler(IngestHandler):
    name = "text"

    def can_handle(self, job: ArtJob) -> bool:
        return bool(job.payload.strip())

    def normalize(self, job: ArtJob) -> ArtJob:
        text = job.payload.strip()
        if not text:
            raise IngestError("empty text payload")
        job.payload = text
        return job