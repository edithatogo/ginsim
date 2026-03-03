# Technical Infrastructure Specification

**Track:** gdpe_0003_model_implementation  
**Purpose:** Define SOTA technical stack for game-theoretic economic modelling  
**Date:** 2026-03-03  
**Version:** 1.0

---

## Executive Summary

**Current State:** Basic JAX/Python scaffold with minimal DevOps infrastructure.

**Required State:** Production-ready research infrastructure with:
- ✅ Reproducible computation (containers, workflow orchestration)
- ✅ Automated testing and CI/CD
- ✅ Experiment tracking and versioning
- ✅ Optimized JAX computation (vmap, pmap, jit)
- ✅ Proper parameter abstraction (configs, hyperparameters)
- ✅ Type safety and code quality enforcement

---

## 1. Core Library Stack (SOTA Review)

### 1.1 Numerical Computation ✅ CURRENT

| Library | Current | Status | Notes |
|---------|---------|--------|-------|
| **JAX** | >=0.4.25 | ✅ SOTA | Best for autodiff + XLA acceleration |
| **NumPyro** | >=0.15.0 | ✅ SOTA | Best HMC/NUTS for Bayesian inference |
| **BlackJAX** | >=1.1.0 | ✅ SOTA | Advanced samplers (SGMCMC, VI) |
| **Equinox** | >=0.11.3 | ✅ SOTA | Neural networks + structural models |
| **Optax** | >=0.2.2 | ✅ SOTA | Gradient transformations |

**Recommendation:** ✅ **Keep current stack** — All libraries are SOTA for Bayesian computation.

---

### 1.2 Game Theory / Economics ⚠️ MISSING

| Library | Current | Required | Status |
|---------|---------|----------|--------|
| **NashPy** | ❌ | ✅ | Compute Nash equilibria |
| **QuantEcon** | ❌ | ✅ | Economic modelling tools |
| **NetworkX** | ❌ | ✅ | Strategic network models |
| **Axelrod** | ❌ | ⚠️ Optional | Iterated game simulations |

**Recommendation:** Add for game-theoretic equilibrium computation.

---

### 1.3 Workflow Orchestration ⚠️ MISSING

| Tool | Current | Required | Status |
|------|---------|----------|--------|
| **Snakemake** | ❌ | ✅ | Pipeline orchestration |
| **DVC** | ❌ | ✅ | Data versioning |
| **MLflow** | ❌ | ⚠️ Optional | Experiment tracking |

**Recommendation:** Add Snakemake for reproducible pipelines, DVC for data versioning.

---

### 1.4 Containerization ⚠️ MISSING

| Tool | Current | Required | Status |
|------|---------|----------|--------|
| **Docker** | ❌ | ✅ | Reproducible environments |
| **Docker Compose** | ❌ | ⚠️ Optional | Multi-container workflows |

**Recommendation:** Add Dockerfile for reproducible computation.

---

### 1.5 CI/CD ⚠️ MISSING

| Tool | Current | Required | Status |
|------|---------|----------|--------|
| **GitHub Actions** | ❌ | ✅ | Automated testing |
| **pre-commit** | ✅ | ✅ | Already configured |
| **pytest** | ✅ | ✅ | Already configured |

**Recommendation:** Add GitHub Actions for CI/CD.

---

### 1.6 Type Safety ⚠️ PARTIAL

| Tool | Current | Required | Status |
|------|---------|----------|--------|
| **mypy** | ❌ | ✅ | Static type checking |
| **jaxtyping** | ✅ | ✅ | Already configured |
| **pydantic** | ✅ | ✅ | Already configured |

**Recommendation:** Add mypy for comprehensive type checking.

---

## 2. Configuration Architecture

### 2.1 Current State

**Structure:**
```
configs/
├── base.yaml              # Global settings
├── policies.yaml          # Policy rules
├── policies_australia.yaml
├── policies_new_zealand.yaml
├── calibration_australia.yaml   # Prior distributions
└── calibration_new_zealand.yaml
```

**Issues:**
- ❌ No separation of parameters vs. hyperparameters
- ❌ No hierarchical config inheritance
- ❌ No runtime config validation
- ❌ No experiment config tracking

---

### 2.2 Proposed Architecture

**Structure:**
```
configs/
├── base/
│   ├── defaults.yaml          # Default values for all parameters
│   ├── parameters.yaml        # Model parameters (calibrated)
│   └── hyperparameters.yaml   # MCMC settings, draws, etc.
│
├── experiments/
│   ├── phase1_unit_tests.yaml
│   ├── phase3_validation.yaml
│   ├── phase4_policy_sweep.yaml
│   └── phase5_sensitivity.yaml
│
├── jurisdictions/
│   ├── australia.yaml
│   └── new_zealand.yaml
│
└── policies/
    ├── status_quo.yaml
    ├── moratorium.yaml
    └── statutory_ban.yaml
```

**Features:**
- ✅ Hierarchical inheritance (base → jurisdiction → experiment)
- ✅ Clear parameter/hyperparameter separation
- ✅ Experiment configs track all settings
- ✅ Runtime validation with pydantic

---

### 2.3 Parameter Abstraction

**Current:**
```python
# Hardcoded in scripts
baseline_testing_uptake = 0.52
deterrence_elasticity = 0.18
```

**Proposed:**
```python
from pydantic import BaseModel
from typing import Dict, Any

class ModelParameters(BaseModel):
    baseline_testing_uptake: float
    deterrence_elasticity: float
    # ... all parameters
    
    class Config:
        extra = 'forbid'  # Catch typos

# Load from config
params = ModelParameters(**load_config('configs/experiments/phase4_policy_sweep.yaml'))
```

**Benefits:**
- ✅ Type safety
- ✅ Validation at load time
- ✅ Catch typos/missing parameters
- ✅ Reproducible experiments

---

## 3. Computation Optimization

### 3.1 Current State

**Issues:**
- ❌ No explicit `jit` decorators
- ❌ No `vmap` for vectorization
- ❌ No `pmap` for multi-device
- ❌ Random seed management unclear

---

### 3.2 Proposed Optimization Strategy

#### Level 1: Function-Level JIT
```python
from jax import jit

@jit
def compute_equilibrium(params: ModelParameters) -> jax.Array:
    """Compute insurance equilibrium."""
    # Implementation
    return equilibrium
```

#### Level 2: Batched Computation (vmap)
```python
from jax import vmap

# Vectorize over policy scenarios
@jit
@vmap
def evaluate_policy(scenario_params: ModelParameters) -> Dict[str, float]:
    """Evaluate single policy scenario."""
    return run_model(scenario_params)

# Batch evaluate all scenarios
results = evaluate_policy(all_scenarios)  # Parallel over scenarios
```

#### Level 3: Multi-Device (pmap) - Optional
```python
from jax import pmap

@pmap
def mcmc_chain(rng_key: jax.Array, data: jax.Array) -> Samples:
    """Run MCMC on separate devices."""
    return run_mcmc(rng_key, data)

# Parallel chains across GPUs
chains = mcmc_chain(rng_keys, data_batched)
```

#### Level 4: Gradient-Based Calibration
```python
import jax.numpy as jnp
from jax import grad, value_and_grad

@jit
@value_and_grad
def log_posterior(params: ModelParameters, data: jax.Array) -> float:
    """Compute log posterior and gradient."""
    log_likelihood = compute_likelihood(params, data)
    log_prior = compute_prior(params)
    return log_likelihood + log_prior

# Use gradient for HMC efficiency
grad_fn = grad(log_posterior)
```

---

### 3.3 Random Seed Management

**Current:** Unclear

**Proposed:**
```python
import jax.random as jr

class RNGManager:
    def __init__(self, base_seed: int = 20260303):
        self.base_key = jr.PRNGKey(base_seed)
        self.counters = {}
    
    def get_key(self, stream_name: str) -> jax.Array:
        """Get unique key for computation stream."""
        if stream_name not in self.counters:
            self.counters[stream_name] = 0
        
        subkey, self.base_key = jr.split(self.base_key)
        self.counters[stream_name] += 1
        
        return subkey
    
    def get_policy_comparison_keys(self, n_policies: int) -> jax.Array:
        """Get CRN keys for policy comparison (variance reduction)."""
        return jr.split(self.get_key('policy_comparison'), n_policies)

# Usage
rng = RNGManager()
mcmc_key = rng.get_key('mcmc')
policy_keys = rng.get_policy_comparison_keys(3)  # Status quo, moratorium, ban
```

**Benefits:**
- ✅ Reproducible across runs
- ✅ Common random numbers for policy comparison
- ✅ No accidental key reuse

---

## 4. Workflow Orchestration

### 4.1 Current State

**Issue:** ❌ No pipeline orchestration — manual script execution

---

### 4.2 Proposed: Snakemake Pipeline

**File:** `Snakefile`
```python
# Snakemake pipeline for genetic discrimination model

configfile: "configs/experiments/phase4_policy_sweep.yaml"

rule all:
    input:
        "outputs/results/policy_sweep/summary.csv",
        "outputs/figures/policy_comparison.png",
        "outputs/voi/evppi_by_group.csv"

rule run_model:
    input:
        config="configs/experiments/{experiment}.yaml"
    output:
        "outputs/results/{experiment}/posterior_samples.npy"
    conda:
        "environment.yaml"
    script:
        "scripts/run_model.py"

rule compute_voi:
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/voi/{experiment}/evppi_by_group.csv"
    script:
        "scripts/compute_voi.py"

rule generate_figures:
    input:
        "outputs/results/{experiment}/posterior_samples.npy"
    output:
        "outputs/figures/{experiment}/policy_comparison.png"
    script:
        "scripts/generate_figures.py"
```

**Usage:**
```bash
# Run full pipeline
snakemake --cores all --configfile configs/experiments/phase4_policy_sweep.yaml

# Dry run (see what will run)
snakemake --dryrun

# Run specific target
snakemake outputs/voi/evppi_by_group.csv
```

**Benefits:**
- ✅ Reproducible pipeline
- ✅ Automatic dependency management
- ✅ Parallel execution
- ✅ Checkpointing (resume from failures)
- ✅ Conda environment per rule

---

## 5. Version Control Strategy

### 5.1 Current State

**Git:** ✅ Configured  
**DVC:** ❌ Missing  
**Data versioning:** ❌ Missing

---

### 5.2 Proposed: Git + DVC

**Git tracks:**
- ✅ Source code
- ✅ Configs
- ✅ Documentation
- ✅ Tests

**DVC tracks:**
- ✅ Large data files (>10MB)
- ✅ Posterior samples
- ✅ Generated figures
- ✅ Model outputs

**Setup:**
```bash
# Initialize DVC
dvc init

# Track large outputs
dvc add outputs/results/
dvc add outputs/posterior_samples/

# Commit
git add outputs/results.dvc outputs/posterior_samples.dvc
git commit -m "Add DVC tracking for model outputs"
```

**Benefits:**
- ✅ Git repo stays small
- ✅ Large files versioned
- ✅ Reproducible outputs
- ✅ Easy to share results

---

## 6. CI/CD Pipeline

### 6.1 Proposed: GitHub Actions

**File:** `.github/workflows/ci.yaml`
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev,validation]"
    
    - name: Lint (ruff)
      run: ruff check src/ scripts/
    
    - name: Type check (mypy)
      run: mypy src/
    
    - name: Test (pytest)
      run: pytest -v --cov=src
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  validate-model:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run validation tests
      run: |
        python -m scripts.run_stress_tests
        python -m scripts.run_posterior_predictive --n_draws 100
    
    - name: Validate reference integrity
      run: python -m scripts.validate_references --report
```

**Benefits:**
- ✅ Automated testing on every commit
- ✅ Multi-Python version testing
- ✅ Type safety enforcement
- ✅ Coverage tracking
- ✅ Model validation automated

---

## 7. Containerization

### 7.1 Proposed: Docker

**File:** `Dockerfile`
```dockerfile
FROM python:3.11-slim

# Install JAX with GPU support (optional)
ENV JAX_PLATFORMS=cuda  # or 'cpu' for CPU-only

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[dev,validation]"

# Copy source code
COPY src/ src/
COPY scripts/ scripts/
COPY configs/ configs/

# Set working directory
WORKDIR /app

# Default command
CMD ["python", "-m", "scripts.run_meta_pipeline", "--n_draws", "2000"]
```

**Usage:**
```bash
# Build image
docker build -t genetic-discrimination-model:latest .

# Run model
docker run --rm -v $(pwd)/outputs:/app/outputs genetic-discrimination-model:latest

# Run with GPU (if available)
docker run --gpus all --rm genetic-discrimination-model:latest
```

**Benefits:**
- ✅ Reproducible environment
- ✅ No dependency conflicts
- ✅ Easy to share with collaborators
- ✅ Production deployment ready

---

## 8. Experiment Tracking

### 8.1 Proposed: MLflow (Optional)

**Setup:**
```python
import mlflow

# Start experiment
mlflow.set_experiment("genetic-discrimination-policy")

# Log run
with mlflow.start_run():
    # Log parameters
    mlflow.log_params(params.dict())
    
    # Log metrics
    mlflow.log_metric("evpi", evpi_value)
    mlflow.log_metric("runtime_seconds", runtime)
    
    # Log artifacts
    mlflow.log_artifact("outputs/results/posterior_samples.csv")
    mlflow.log_artifact("outputs/figures/policy_comparison.png")
```

**Benefits:**
- ✅ Track all experiments
- ✅ Compare parameter settings
- ✅ Reproduce past runs
- ✅ Collaborative experiment database

---

## 9. Documentation

### 9.1 Proposed: Sphinx + MyST

**Setup:**
```bash
pip install sphinx myst-parser sphinx-rtd-theme
```

**Structure:**
```
docs/
├── conf.py                  # Sphinx config
├── index.rst               # Main documentation
├── api/                    # API documentation
│   ├── modules.rst
│   └── model.rst
├── user-guide/             # User documentation
│   ├── installation.md
│   ├── quickstart.md
│   └── tutorials/
└── developer-guide/        # Developer documentation
    ├── architecture.md
    └── contributing.md
```

**Benefits:**
- ✅ Professional documentation
- ✅ API auto-documentation
- ✅ Searchable
- ✅ Versioned with releases

---

## 10. Summary: Required Changes

### Critical (Must Have)

| Component | Current | Required | Priority |
|-----------|---------|----------|----------|
| **Parameter abstraction** | ❌ | ✅ Pydantic models | 🔴 Critical |
| **JAX optimization** | ❌ | ✅ jit/vmap/pmap | 🔴 Critical |
| **RNG management** | ❌ | ✅ RNGManager class | 🔴 Critical |
| **Type checking** | ⚠️ Partial | ✅ mypy | 🔴 Critical |
| **CI/CD** | ❌ | ✅ GitHub Actions | 🔴 Critical |
| **Workflow orchestration** | ❌ | ✅ Snakemake | 🔴 Critical |

### Important (Should Have)

| Component | Current | Required | Priority |
|-----------|---------|----------|----------|
| **Containerization** | ❌ | ✅ Dockerfile | 🟡 Important |
| **Data versioning** | ❌ | ✅ DVC | 🟡 Important |
| **Game theory libs** | ❌ | ✅ NashPy, QuantEcon | 🟡 Important |
| **Documentation** | ⚠️ Basic | ✅ Sphinx | 🟡 Important |

### Optional (Nice to Have)

| Component | Current | Required | Priority |
|-----------|---------|----------|----------|
| **Experiment tracking** | ❌ | ⚠️ MLflow | 🟢 Optional |
| **Multi-device** | ❌ | ⚠️ pmap | 🟢 Optional |

---

## 11. Implementation Plan

### Week 0: Infrastructure Setup

**Tasks:**
1. ✅ Add pydantic parameter models
2. ✅ Implement RNGManager
3. ✅ Add jit/vmap decorators
4. ✅ Configure mypy
5. ✅ Create Dockerfile
6. ✅ Set up GitHub Actions
7. ✅ Create Snakemake pipeline
8. ✅ Add NashPy/QuantEcon

**Deliverable:** Production-ready infrastructure before Phase 1 starts.

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0003_model_implementation
