# Tech stack

## Language/runtime
- Python 3.10+
- Cross-platform (macOS, Windows, Linux)

## Core numerical stack
- JAX / XLA (vectorisation and accelerated simulation)
- NumPyro (probabilistic programming)
- BlackJAX (MCMC kernels / SOTA sampling)
- Optax / JAXopt / Distrax / Equinox (as needed)

## Data + config
- pandas, numpy
- PyYAML for configs
- pydantic for schema validation

## Reporting
- matplotlib for figures
- python-docx for DOCX export
- reportlab for PDF export

## Testing / quality (recommended)
- pytest
- ruff (lint)
- black (format)
- mypy (optional; or pyright externally)

## Determinism
- Set random seeds when feasible.
- Use common random numbers for policy comparisons (fold-in draw index).
