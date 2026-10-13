# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security-only |
| < 0.3   | no        |

## Reporting a vulnerability

Do **not** open a public issue for security problems. Email
`security@qr-art-generator-studio.dev` with:

- repro steps
- affected module (`ingest/`, `processors/`, `drivers/`, `services/`)
- crash log or stack trace

We respond within 72 hours.

## Threat model notes

This tool loads user-supplied prompts and images and runs them through a
diffusion pipeline. The relevant surfaces:

- **Model loading** — `.ckpt` / `.safetensors` files are loaded with
  `weights_only=True` where possible. Never load a checkpoint from an
  untrusted source; pickle-based `.ckpt` can execute code.
- **Plugin/handler loading** — third-party ingest handlers run in-process.
  Only install handlers you've reviewed.
- **Prompt injection into exported SVG** — drivers escape user payload
  strings before embedding in SVG. Report any bypass.
- **Outbound network** — the default config makes zero outbound calls after
  model download. `services/fetch_service.py` is opt-in.

## Disclosure

We credit reporters in `CHANGELOG.md` unless you ask otherwise.