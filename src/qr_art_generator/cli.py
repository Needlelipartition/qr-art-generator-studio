"""Entry point. Wires the pipeline: ingest -> process -> drive."""
from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console

from qr_art_generator.config.settings import load_settings
from qr_art_generator.models.job import ArtJob
from qr_art_generator.services.pipeline_service import PipelineService

app = typer.Typer(add_completion=False, help="AI QR code art generator studio.")
console = Console()


@app.command()
def generate(
    payload: str = typer.Argument(..., help="Text or URL to encode into the QR art."),
    prompt: str = typer.Option("stained glass cathedral, vivid", help="Style prompt."),
    out: Path = typer.Option(Path("output_gallery"), help="Output directory."),
    config: Path | None = typer.Option(None, help="Path to a TOML config override."),
    seed: int | None = typer.Option(None, help="RNG seed for reproducibility."),
) -> None:
    """Render one QR art image from a payload + style prompt."""
    settings = load_settings(config)
    job = ArtJob(payload=payload, prompt=prompt, output_dir=out, seed=seed)
    service = PipelineService(settings)
    result = asyncio.run(service.run(job))
    console.print(f"[green]ok[/green] {result.image_path} (scan_score={result.scan_score:.3f})")


@app.command()
def batch(
    manifest: Path = typer.Argument(..., exists=True, help="JSONL manifest of jobs."),
    out: Path = typer.Option(Path("output_gallery")),
) -> None:
    """Run a batch of jobs from a JSONL manifest."""
    settings = load_settings(None)
    service = PipelineService(settings)
    count = asyncio.run(service.run_batch(manifest, out))
    console.print(f"[green]done[/green] {count} jobs rendered")


if __name__ == "__main__":
    app()