# Security Policy

## Reporting a vulnerability

Do not open public GitHub issues for suspected security problems, credential exposure, or unpublished-study data leaks.

Report security issues privately to the repository owner with:

- a short description of the issue
- affected file paths or workflows
- reproduction steps
- any evidence of secret, dataset, or artifact exposure

## Repository handling rules

- Treat `local_only/` as non-public working material.
- Do not commit generated archives, coverage outputs, temporary deployment environments, or local caches.
- Prefer pull requests with passing CI before changing deployment or workflow configuration.

## Deployment notes

- The canonical Streamlit app lives at `streamlit_app/app.py`.
- The `gin-sim/` directory is a deployment wrapper and should not diverge from the canonical app surface.
