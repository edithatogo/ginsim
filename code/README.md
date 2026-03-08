# Code Submodule README

# Genetic Discrimination Policy Economic Model

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A modular Bayesian decision analysis model for quantifying the economic and welfare impacts of policies that restrict genetic discrimination in life insurance.

## Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from src.model import ModelParameters, PolicyConfig, evaluate_policy_sweep

# Load parameters
params = ModelParameters.from_config('configs/calibration_australia.yaml')

# Evaluate all policies
results = evaluate_policy_sweep(params)

# Print summary
print(generate_policy_summary(results))
```

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this code, please cite:

```
Mordaunt, D. A. (2026). Genetic Discrimination Policy Economic Model [Computer software].
https://github.com/yourusername/genetic-discrimination-policy-code
```

## Development

### Running Tests

```bash
pytest -v
```

### Code Quality

```bash
ruff check src/ scripts/
ruff format src/ scripts/ --check
pyright src/
```

## Features

- **Modular architecture:** 6 modules (behavior, clinical, insurance, proxy, passthrough, data quality)
- **Bayesian inference:** Full probabilistic sensitivity analysis
- **JAX acceleration:** Fast computation with XLA
- **VOI analysis:** EVPI and EVPPI computation
- **Sensitivity analysis:** Tornado diagrams, scenario analysis

## Requirements

- Python 3.10+
- JAX, NumPyro, BlackJAX
- attrs, msgspec, beartype, chex

See `pyproject.toml` for full list of dependencies.
