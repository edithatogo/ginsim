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
- pydantic for schema validation (external API)
- attrs for JAX-compatible data classes (internal state)
- msgspec for fast serialization (config I/O)

## Reporting
- matplotlib for figures
- python-docx for DOCX export
- reportlab for PDF export

## Testing / quality (recommended)
- pytest
- ruff (lint)
- black (format)
- pyright (strict typing)
- beartype (runtime type checking)
- chex (JAX testing utilities)
- attrs (immutable data classes)
- msgspec (fast serialization)

## Determinism
- Set random seeds when feasible.
- Use common random numbers for policy comparisons (fold-in draw index).
