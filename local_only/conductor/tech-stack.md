# Tech stack

## Language/runtime
- Python 3.11+
- Cross-platform (macOS, Windows, Linux)
- Unified environment management via `uv` and `uv.lock`.

## Core numerical stack
- JAX / XLA (vectorisation and accelerated simulation)
- NumPyro (probabilistic programming)
- BlackJAX (MCMC kernels / SOTA sampling)
- **Optax** (Adversarial Red-Teaming / Gradient-based Optimization)
- JAXopt / Distrax / Equinox (as needed)

## Data + config
- pandas, numpy, polars
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
- **Playwright (Remote E2E monitoring)**
- ruff (lint & format)
- pyright (strict typing)
- beartype (runtime type checking)
- chex (JAX testing utilities)
- attrs (immutable data classes)
- msgspec (fast serialization)
- Institutionalized Quality Gate (100% coverage requirement).
- Jurisdictional Matrix Testing: Automated pytest parameterization across international configs (AU, NZ, UK, CAN, US).
- Simulated Peer Review Layer: Multi-persona audit framework (Nature/Lancet/Treasury).
- Automated Prioritization Matrix: Agent-driven feature consensus logic.
- Cryptographic Provenance (sha256 hash-linking).

## Determinism
- Set random seeds when feasible.
- Use common random numbers for policy comparisons (fold-in draw index).
