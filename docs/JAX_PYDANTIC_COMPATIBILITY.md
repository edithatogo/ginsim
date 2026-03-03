# JAX + Pydantic Compatibility Guide

**Problem:** JAX's `@jit` cannot trace pydantic models because they are Python objects, not JAX arrays.

---

## The Issue

```python
from pydantic import BaseModel
from jax import jit

class Config(BaseModel):
    learning_rate: float

@jit
def train(config: Config):  # ❌ FAILS - JAX can't trace pydantic models
    return config.learning_rate * 2
```

**Error:**
```
TypeError: Error interpreting argument to <function train> as an abstract array.
The problematic value is of type <class '__main__.Config'> and was passed to the function.
This typically means that a jit-wrapped function was called with a non-array argument.
```

---

## Solution 1: Wrapper Pattern (Recommended)

**Extract primitives before calling JIT functions:**

```python
from pydantic import BaseModel
from jax import jit

class Config(BaseModel):
    learning_rate: float

@jit
def _train_jit(lr: float):  # ✅ Uses primitives
    return lr * 2

def train(config: Config):  # ✅ Wrapper function
    """Public API accepts pydantic, extracts primitives."""
    return _train_jit(config.learning_rate)
```

**Benefits:**
- ✅ Pydantic validation at API boundary
- ✅ JAX optimization for core functions
- ✅ Clear separation of concerns

**Used in:** `src/model/module_a_behavior_wrappers.py`

---

## Solution 2: chex.dataclass (For JAX-Native Code)

**Use chex.dataclass for internal JAX code:**

```python
import chex
from jax import jit

@chex.dataclass
class JAXState:
    """JAX-compatible dataclass."""
    params: chex.Array
    step: int

@jit
def update(state: JAXState):  # ✅ Works with chex.dataclass
    return JAXState(params=state.params * 2, step=state.step + 1)
```

**Benefits:**
- ✅ JAX-compatible dataclass
- ✅ Lighter weight than pydantic
- ✅ Part of DeepMind JAX ecosystem

**Use case:** Internal JAX state, not config validation

---

## Solution 3: Static Arguments

**Mark pydantic models as static (disables JIT for those args):**

```python
from jax import jit

@jit
def train(config, data):  # config is static
    return config.learning_rate * data

# Call with static_argnums
train_jit = jit(train, static_argnums=(0,))
```

**Benefits:**
- ✅ Simple for infrequent calls

**Drawbacks:**
- ❌ No JIT optimization for static args
- ❌ Recompiles for each unique config

---

## Solution 4: Equinox Modules (Advanced)

**Use Equinox for JAX-compatible modules:**

```python
import equinox as eqx
from jax import jit

class Model(eqx.Module):
    """JAX-compatible module."""
    weight: chex.Array
    
    @jit
    def __call__(self, x):
        return self.weight * x
```

**Benefits:**
- ✅ Full JAX compatibility
- ✅ Pydantic-like validation
- ✅ Part of JAX ecosystem

**Use case:** Complex JAX models with state

---

## Our Architecture

```
┌─────────────────────────────────────────────────────┐
│  Config Layer (pydantic)                            │
│  - External validation                              │
│  - Type checking                                    │
│  - Default values                                   │
└─────────────────────────────────────────────────────┘
                        ↓ (extract primitives)
┌─────────────────────────────────────────────────────┐
│  Wrapper Layer (pure Python)                        │
│  - Extract primitives from pydantic                 │
│  - Call JIT functions                               │
└─────────────────────────────────────────────────────┘
                        ↓ (primitives only)
┌─────────────────────────────────────────────────────┐
│  JAX Layer (@jit, chex.dataclass)                   │
│  - Optimized computation                            │
│  - JAX-native types only                            │
└─────────────────────────────────────────────────────┘
```

---

## Best Practices

### DO:
- ✅ Use pydantic for config validation at API boundaries
- ✅ Use wrapper functions to extract primitives
- ✅ Use chex.dataclass for JAX-native state
- ✅ Keep JAX functions pure (arrays/primitives only)

### DON'T:
- ❌ Pass pydantic models to @jit functions
- ❌ Use Python conditionals on traced values
- ❌ Mix pydantic and JAX in same function

---

## Testing Pattern

```python
# Test wrapper function (accepts pydantic)
def test_train_wrapper():
    config = Config(learning_rate=0.01)
    result = train(config)  # Tests wrapper
    assert result == 0.02

# Test JIT function directly (uses primitives)
def test_train_jit():
    result = _train_jit(0.01)  # Tests JIT function
    assert result == 0.02
```

---

## References

- Chex documentation: https://chex.readthedocs.io/
- Equinox: https://docs.kidger.site/equinox/
- JAX pytrees: https://jax.readthedocs.io/en/latest/pytrees.html
