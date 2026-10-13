# Contributing to qr-art-generator-studio

Thanks for wanting to mash new patterns into the tater. This repo is the
pipeline/worker AI QR code art generator — ingest handlers feed the control
net, processors diff the error map, output drivers stamp the final QR art.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e .[dev]
pytest -q
```

## Architecture in one breath

```
ingest/  ->  processors/  ->  drivers/  ->  gallery output
   ^              |                ^
   |         job utils         config models
```

- `src/qr_art_generator/ingest/` — handlers that pull seeds, prompts, payloads.
- `src/qr_art_generator/processors/` — the diffusion + QR-error-map pipeline.
- `src/qr_art_generator/drivers/` — writers that render and export final art.
- `src/qr_art_generator/models/` — dataclasses for jobs, configs, results.
- `src/qr_art_generator/utils/` — QR math, image ops, logging.
- `src/qr_art_generator/services/` — long-running workers, queue, scheduler.

## Adding a new ingest handler

1. Drop a module in `ingest/`.
2. Subclass `IngestHandler` from `ingest/base.py`.
3. Register it in `ingest/registry.py`.
4. Add a test in `tests/`.

## Adding a new output driver

Same shape, but subclass `OutputDriver` in `drivers/base.py`. Registered in
`drivers/registry.py`. Drivers own everything past the final tensor — encoding,
dithering, module shaping.

## Style

- Ruff + black. Line length 100.
- Type hints required on public functions.
- No print debugging in `processors/` — use `utils/logging.py`.

## PR checklist

- [ ] `pytest -q` green
- [ ] `ruff check src tests`
- [ ] New handler/driver has a registry entry
- [ ] No model weights committed
- [ ] Changelog line added

## Community

This is a hobbyist/educational repo. We ship tools for QR art, generative
pipelines, and control-net experimentation. Bring your weird gradients.