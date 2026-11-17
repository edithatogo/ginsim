# Serialization and Type Checking Stack

## Recommended Libraries

### 1. **msgspec** (Serialization + Validation)

**Purpose:** Fast serialization and schema validation

**Why:**
- ✅ **10-80x faster** than pydantic for JSON encoding/decoding
- ✅ **Zero-cost validation** during deserialization
- ✅ **No dependencies** (lightweight)
- ✅ **Struct type** - 5-60x faster than dataclasses/attrs
- ✅ Supports JSON, MessagePack, YAML, TOML

**Use case:** Replace pydantic for config serialization where performance matters

**Example:**
```python
import msgspec

class Config(msgspec.Struct):
    learning_rate: float
    n_iterations: int

# Fast serialization
config = Config(0.01, 1000)
json_bytes = msgspec.json.encode(config)  # 10-80x faster than pydantic
config2 = msgspec.json.decode(json_bytes, type=Config)  # With validation
```

---

### 2. **attrs** (Data Classes)

**Purpose:** General-purpose data classes

**Why:**
- ✅ **Most mature** (since 2015, used by NASA)
- ✅ **Frozen classes** for immutability (JAX-friendly)
- ✅ **Slots** for memory efficiency
- ✅ **Validators and converters**
- ✅ **No runtime overhead** (unlike pydantic)

**Use case:** Internal data structures, JAX-compatible state

**Example:**
```python
import attrs

@attrs.define(frozen=True, slots=True)
class ModelState:
    params: dict
    step: int

# Immutable, efficient
state = ModelState(params={'w': 0.5}, step=0)
# state.step = 1  # ❌ Error - frozen
```

---

### 3. **beartype** (Runtime Type Checking)

**Purpose:** Runtime type enforcement

**Why:**
- ✅ **O(1) constant-time** checking (fastest)
- ✅ **JAX array support** (explicit in docs)
- ✅ **Package-wide enforcement** with 2 lines
- ✅ **No runtime dependencies**
- ✅ **1µs checking time** (near-zero overhead)

**Use case:** Runtime type checking for JAX code

**Example:**
```python
from beartype import beartype
from beartype.claw import beartype_this_package
import jax.numpy as jnp

# Package-wide enforcement
beartype_this_package()

@beartype
def train(params: dict[str, jnp.ndarray], data: jnp.ndarray) -> float:
    return jnp.sum(params['w'] * data)
```

---

## Our Stack Architecture

```
┌─────────────────────────────────────────────────────────┐
│  External API Layer (pydantic)                          │
│  - User-facing configs                                  │
│  - Validation at boundaries                             │
│  - Rich error messages                                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Serialization Layer (msgspec)                          │
│  - Fast JSON/YAML serialization                         │
│  - Zero-cost validation                                 │
│  - Config file I/O                                      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Internal Data Structures (attrs)                       │
│  - Frozen, immutable state                              │
│  - Slots for efficiency                                 │
│  - JAX-compatible                                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  Runtime Type Checking (beartype)                       │
│  - O(1) type checking                                   │
│  - JAX array support                                    │
│  - Package-wide enforcement                             │
└─────────────────────────────────────────────────────────┘
```

---

## Migration Strategy

### Phase 1: Add beartype (Immediate)
```python
# In __init__.py
from beartype.claw import beartype_this_package
beartype_this_package()  # Type-check entire package
```

**Benefits:**
- Catches type errors at runtime
- JAX array support
- Near-zero overhead

### Phase 2: Add attrs (Short-term)
```python
# Replace dataclasses with attrs for JAX state
@attrs.define(frozen=True)
class ModelState:
    params: dict
    step: int
```

**Benefits:**
- Better JAX compatibility
- Immutability by default
- Memory efficient

### Phase 3: Add msgspec (Medium-term)
```python
# Replace pydantic for config serialization
import msgspec

class Config(msgspec.Struct):
    learning_rate: float
    n_iterations: int
```

**Benefits:**
- 10-80x faster serialization
- Zero-cost validation
- Smaller dependency footprint

---

## Comparison Table

| Library | Purpose | Performance | JAX Compatible | Maturity |
|---------|---------|-------------|----------------|----------|
| **pydantic** | Validation | Slow | ⚠️ (needs wrapper) | Mature |
| **msgspec** | Serialization | **Fastest** | ✅ | Growing |
| **attrs** | Data classes | Fast | ✅ | **Most mature** |
| **dataclasses** | Data classes | Fast | ✅ | Standard lib |
| **beartype** | Type checking | **Fastest** | ✅ | Growing |
| **typeguard** | Type checking | Fast | ⚠️ | Mature |
| **chex** | JAX testing | Fast | ✅ | Mature |

---

## Recommendation

**Keep pydantic for:**
- User-facing API validation
- Rich error messages
- Complex validation logic

**Add msgspec for:**
- Config file I/O
- Fast serialization
- Performance-critical paths

**Add attrs for:**
- Internal JAX state
- Immutable data structures
- Memory-efficient containers

**Add beartype for:**
- Runtime type checking
- JAX array validation
- Package-wide enforcement

**Add chex for:**
- JAX-specific testing
- Array shape assertions
- Debugging JAX transformations

---

## Installation

```bash
pip install msgspec attrs beartype chex
```

**Total added size:** ~2MB (minimal)

**Performance impact:**
- beartype: ~1µs per call (negligible)
- attrs: No overhead (frozen, slotted)
- msgspec: 10-80x faster than pydantic
- chex: Only in tests (no runtime impact)
