# Technology Stack

## Core Technology Stack

### Programming Language
- **Python 3.10-3.12** - Primary development language with modern type hints and async support

### Core Dependencies

#### Bayesian Inference & JAX Ecosystem
| Package | Version | Purpose |
|---------|---------|---------|
| `jax` | >=0.4.25 | Accelerated linear algebra, XLA compilation |
| `jaxlib` | >=0.4.25 | JAX runtime library |
| `numpyro` | >=0.15.0 | Probabilistic programming, MCMC sampling |
| `optax` | >=0.2.2 | Gradient processing, optimization |
| `distrax` | >=0.1.5 | Probability distributions |
| `equinox` | >=0.11.3 | Neural networks, differentiable programming |
| `chex` | >=0.1.86 | Testing utilities for JAX |
| `jaxopt` | >=0.8.3 | Mathematical optimization |
| `jaxtyping` | >=0.2.25 | Runtime type checking for JAX arrays |

#### Data Processing & Numerical Computing
| Package | Version | Purpose |
|---------|---------|---------|
| `numpy` | >=1.26 | Numerical computing, array operations |
| `polars` | >=0.20.0 | Fast DataFrame operations, data manipulation |

#### Game Theory & Economic Modeling
| Package | Version | Purpose |
|---------|---------|---------|
| `nashpy` | >=0.0.32 | Nash equilibrium computation |
| `quantecon` | >=0.8.0 | Quantitative economics tools |
| `networkx` | >=3.0 | Graph theory, network analysis |

#### Configuration & Validation
| Package | Version | Purpose |
|---------|---------|---------|
| `hydra-core` | >=1.3 | Hierarchical configuration management |
| `pyyaml` | >=6.0 | YAML parsing for config files |
| `pydantic` | >=2.6 | Data validation, settings management |
| `beartype` | >=0.18.0 | Runtime type checking |
| `msgspec` | >=0.18.0 | Fast serialization/deserialization |

#### CLI & User Interface
| Package | Version | Purpose |
|---------|---------|---------|
| `typer` | >=0.9.0 | Command-line interface framework |
| `rich` | >=13.7.0 | Terminal formatting, progress bars |
| `streamlit` | (implicit) | Interactive dashboard framework |
| `tqdm` | >=4.66.0 | Progress bars for loops |
| `loguru` | >=0.7.2 | Structured logging |

#### Visualization & Reporting
| Package | Version | Purpose |
|---------|---------|---------|
| `matplotlib` | >=3.8 | Static plotting, figure generation |
| `tabulate` | >=0.9 | Table formatting for reports |
| `python-docx` | >=1.1 | Word document generation |
| `reportlab` | >=4.0 | PDF report generation |

### Development Dependencies

#### Testing & Quality Assurance
| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=8.0 | Test framework |
| `pytest-cov` | >=4.0 | Coverage reporting |
| `pytest-xdist` | >=3.5 | Parallel test execution |
| `pytest-mock` | >=3.12 | Mocking utilities |
| `pytest-timeout` | >=2.2 | Test timeout enforcement |
| `hypothesis` | >=6.97 | Property-based testing |
| `mutmut` | >=2.4 | Mutation testing |

#### Code Quality & Linting
| Package | Version | Purpose |
|---------|---------|---------|
| `ruff` | >=0.3.0 | Fast linting and formatting |
| `pyright` | >=1.1.350 | Static type checking |
| `pre-commit` | >=3.6 | Git pre-commit hooks |

#### Build & Workflow
| Package | Version | Purpose |
|---------|---------|---------|
| `uv` | >=0.1.0 | Fast Python package installer |
| `nox` | >=2024.3.2 | Test automation across environments |
| `ipython` | >=8.20 | Interactive Python shell |
| `attrs` | >=23.2.0 | Class creation with less boilerplate |

---

## Architecture Overview

### Module Structure
```
src/
├── model/              # Core economic modeling engine
│   ├── module_a_behavior.py      # Individual testing decisions
│   ├── module_b_clinical.py      # Clinical pathway modeling
│   ├── module_c_insurance_eq.py  # Insurance market equilibrium
│   ├── module_d_proxy.py         # Proxy variable reconstruction
│   ├── module_enforcement.py     # Regulatory enforcement game
│   ├── module_e_passthrough.py   # Cost passthrough modeling
│   ├── module_f_data_quality.py  # Data quality assessment
│   ├── dcba_ledger.py            # Distributional CBA aggregation
│   └── parameters.py             # Parameter schemas & validation
├── inference/          # Bayesian inference utilities
└── utils/              # Shared utilities
```

### Application Layers
1. **Core Engine** (`src/model/`) - JAX-based economic modeling
2. **Inference Layer** (`src/inference/`) - MCMC, variational inference
3. **Configuration** (`configs/`) - YAML-based calibration & scenarios
4. **CLI** (`scripts/`) - Typer-based command-line tools
5. **Dashboard** (`streamlit_app/`) - Interactive policy sandbox
6. **Tests** (`tests/`) - Unit, integration, and property-based tests

---

## Infrastructure & Deployment

### Containerization
- **Docker** - Reproducible environments via `Dockerfile`
- **Base Image** - Python 3.11 slim
- **JAX Optimization** - CUDA/cuDNN for GPU acceleration (optional)

### CI/CD
- **GitHub Actions** - Automated testing, deployment
- **Streamlit Cloud** - Live dashboard hosting
- **Zenodo Integration** - DOI minting for releases

### Development Environment
- **Virtual Environments** - `.venv/` with uv/pip
- **Pre-commit Hooks** - Automated linting, formatting
- **Nox Sessions** - Multi-environment test runs

---

## Version Management

### Dependency Pinning
- **Lock File** - `uv.lock` for reproducible installs
- **Semantic Versioning** - MAJOR.MINOR.PATCH with constraints in `pyproject.toml`
- **Minimum Versions** - All dependencies specify minimum compatible versions

### Python Version Policy
- **Minimum** - Python 3.10
- **Maximum** - Python 3.12 (exclusive: <3.13)
- **Recommended** - Python 3.11 (balanced ecosystem support)

---

## Tech Stack Decision Rationale

### Why JAX?
- **Performance** - XLA compilation, GPU/TPU support
- **Autodiff** - Gradient-based optimization, sensitivity analysis
- **Ecosystem** - NumPyro for Bayesian inference, Optax for optimization

### Why Polars over Pandas?
- **Speed** - Lazy evaluation, parallel execution
- **Memory Efficiency** - Out-of-core processing for large datasets
- **API Design** - More intuitive for complex transformations

### Why Hydra for Configuration?
- **Hierarchical** - Composable configs (base + jurisdiction + policy)
- **Overrides** - CLI parameter sweeps without code changes
- **Type Safety** - Integration with Pydantic for validation

### Why Streamlit?
- **Rapid Prototyping** - Pure Python, no frontend framework needed
- **Interactivity** - Built-in widgets, automatic rerun on input change
- **Deployment** - One-click hosting on Streamlit Cloud
