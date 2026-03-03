# Testing Strategy

**Track:** gdpe_0003_model_implementation  
**Purpose:** Comprehensive testing with hypothesis and mutmut  
**Date:** 2026-03-03

---

## Testing Pyramid

```
        /\
       /  \      E2E Tests (slow, few)
      /----\    
     /      \    Integration Tests (medium)
    /--------\  
   /          \  Unit Tests (fast, many)
  /------------\ 
```

---

## 1. Unit Tests (pytest)

**Location:** `tests/unit/`

**Purpose:** Test individual functions in isolation

**Example:**
```python
# tests/unit/test_equilibrium.py
import pytest
from src.model.module_c_insurance_eq import compute_equilibrium

def test_equilibrium_converges():
    """Test that equilibrium solver converges."""
    params = ModelParameters(...)
    equilibrium = compute_equilibrium(params)
    
    assert equilibrium.converged
    assert equilibrium.premiums > 0
    assert equilibrium.takeup > 0

def test_equilibrium_zero_profit():
    """Test zero-profit condition holds."""
    params = ModelParameters(...)
    equilibrium = compute_equilibrium(params)
    
    # Insurer profits should be ~0 at equilibrium
    assert abs(equilibrium.profits) < 1e-6
```

---

## 2. Property-Based Tests (hypothesis)

**Location:** `tests/property/`

**Purpose:** Test properties that should always hold

**Example:**
```python
# tests/property/test_monotonicity.py
from hypothesis import given, settings
from hypothesis import strategies as st
import jax.numpy as jnp

@given(
    enforcement=st.floats(0.0, 1.0),
    baseline=st.floats(0.1, 0.9)
)
@settings(max_examples=100, deadline=500)
def test_enforcement_increases_compliance(enforcement, baseline):
    """Test that higher enforcement → higher compliance (monotonicity)."""
    params_low = ModelParameters(enforcement_strength=enforcement)
    params_high = ModelParameters(enforcement_strength=enforcement * 1.5)
    
    compliance_low = run_model(params_low).compliance_rate
    compliance_high = run_model(params_high).compliance_rate
    
    # Property: more enforcement → more compliance
    assert compliance_high >= compliance_low

@given(
    testing_uptake=st.floats(0.0, 1.0)
)
def test_welfare_bounded(testing_uptake):
    """Test that welfare is bounded (no infinity/NaN)."""
    params = ModelParameters(baseline_testing_uptake=testing_uptake)
    result = run_model(params)
    
    # Property: welfare should be finite
    assert jnp.isfinite(result.welfare_impact)
    assert result.welfare_impact > -1e6  # Reasonable lower bound
    assert result.welfare_impact < 1e6   # Reasonable upper bound
```

**Benefits:**
- ✅ Finds edge cases you didn't think of
- ✅ Tests entire input space, not just examples
- ✅ Shrinks failing cases to minimal example

---

## 3. Mutation Tests (mutmut)

**Purpose:** Test your tests by mutating code

**How it works:**
1. Mutmut makes small changes to your code (mutations)
2. Runs your tests
3. If tests pass → **BAD** (your tests didn't catch the bug)
4. If tests fail → **GOOD** (your tests work)

**Usage:**
```bash
# Run mutation testing
mutmut run

# Show results
mutmut results

# Show specific mutant
mutmut show 1
```

**Example Output:**
```
- Mutation 1: src/model/equilibrium.py:42
  Original: return premiums * quantity
  Mutated:  return premiums + quantity
  
  Status: SURVIVED (tests didn't catch this!)
  
  Recommendation: Add test for premium*quantity relationship
```

**Target:** >80% mutation score (killed mutants / total mutants)

---

## 4. Integration Tests

**Location:** `tests/integration/`

**Purpose:** Test module interactions

**Example:**
```python
# tests/integration/test_full_pipeline.py
import pytest

def test_full_policy_evaluation():
    """Test complete policy evaluation pipeline."""
    # Arrange
    params = ModelParameters.from_config("configs/experiments/test.yaml")
    
    # Act
    results = run_full_pipeline(params)
    
    # Assert
    assert results.testing_uptake is not None
    assert results.premium_divergence is not None
    assert results.welfare_impact is not None
    assert len(results.posterior_samples) == 100  # Test draws
```

---

## 5. Parallel Testing

**Configuration:**
```toml
[tool.pytest.ini_options]
addopts = "-n auto"  # Auto-detect CPU cores
```

**Usage:**
```bash
# Run tests in parallel
pytest -n auto

# Run specific number of workers
pytest -n 4
```

---

## Test Coverage Targets

| Module | Target | Current |
|--------|--------|---------|
| Module A (Behavior) | 90% | TBD |
| Module C (Insurance) | 90% | TBD |
| Module D (Proxy) | 85% | TBD |
| Module F (Data Quality) | 85% | TBD |
| Equilibrium solvers | 95% | TBD |
| Utilities | 80% | TBD |

**Overall target:** >85% coverage

---

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Parallel execution
pytest -n auto

# Property-based tests only
pytest -m property

# Slow tests only
pytest -m slow

# Mutation testing
mutmut run

# Show mutation results
mutmut results
```

---

## Test File Structure

```
tests/
├── unit/
│   ├── test_module_a_behavior.py
│   ├── test_module_c_insurance_eq.py
│   ├── test_module_d_proxy.py
│   └── test_utils.py
├── property/
│   ├── test_monotonicity.py
│   ├── test_bounds.py
│   └── test_invariants.py
├── integration/
│   ├── test_full_pipeline.py
│   └── test_policy_comparison.py
└── conftest.py  # Shared fixtures
```

---

## Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest
from src.model.parameters import ModelParameters

@pytest.fixture
def default_params():
    """Default model parameters for testing."""
    return ModelParameters(
        baseline_testing_uptake=0.52,
        deterrence_elasticity=0.18,
        # ... other defaults
    )

@pytest.fixture
def au_params():
    """Australia-calibrated parameters."""
    return ModelParameters.from_config("configs/calibration_australia.yaml")

@pytest.fixture
def nz_params():
    """New Zealand-calibrated parameters."""
    return ModelParameters.from_config("configs/calibration_new_zealand.yaml")

@pytest.fixture
def rng_key():
    """Default RNG key for reproducibility."""
    return jax.random.PRNGKey(20260303)
```

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0003_model_implementation
