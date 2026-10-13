"""Ordered ingest chain — first handler that claims the job wins."""
from __future__ import annotations

from qr_art_generator.ingest.base import IngestHandler
from qr_art_generator.ingest.text_handler import TextHandler
from qr_art_generator.ingest.url_handler import UrlHandler
from qr_art_generator.models.job import ArtJob


def build_ingest_chain() -> list[IngestHandler]:
    return [UrlHandler(), TextHandler()]


def run_ingest_chain(job: ArtJob, chain: list[IngestHandler] | None = None) -> ArtJob:
    for handler in chain or build_ingest_chain():
        if handler.can_handle(job):
            return handler.normalize(job)
    raise ValueError("no ingest handler could process the payload")