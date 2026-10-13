"""Ingest handler base — every handler validates one payload shape."""
from __future__ import annotations

from abc import ABC, abstractmethod

from qr_art_generator.models.job import ArtJob


class IngestError(ValueError):
    """Raised when a payload can't be normalized into a QR-safe string."""


class IngestHandler(ABC):
    name: str = "base"

    @abstractmethod
    def can_handle(self, job: ArtJob) -> bool: ...

    @abstractmethod
    def normalize(self, job: ArtJob) -> ArtJob:
        """Return a job whose payload is a validated, QR-encodable string."""