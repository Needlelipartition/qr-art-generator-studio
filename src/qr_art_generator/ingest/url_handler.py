"""Validates http/https payloads and rejects QR-hostile schemes."""
from __future__ import annotations

from urllib.parse import urlparse

from qr_art_generator.ingest.base import IngestError, IngestHandler
from qr_art_generator.models.job import ArtJob


class UrlHandler(IngestHandler):
    name = "url"

    def can_handle(self, job: ArtJob) -> bool:
        return "://" in job.payload

    def normalize(self, job: ArtJob) -> ArtJob:
        parsed = urlparse(job.payload)
        if parsed.scheme not in {"http", "https"}:
            raise IngestError(f"unsupported scheme: {parsed.scheme!r}")
        if not parsed.netloc:
            raise IngestError("missing host in URL payload")
        job.payload = job.payload.strip()
        return job