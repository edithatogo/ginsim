# Profiling Guide

**Track:** gdpe_0003_model_implementation
**Purpose:** Performance profiling and optimization
**Date:** 2026-03-03

---

## Quick Start

```bash
# Install profiling dependencies
pip install -e ".[profiling]"

# Run with sampling profiler (minimal overhead)
py-spy record -o outputs/profiles/profile.svg -- python -m scripts.run_model

# Run with line profiler
kernprof -l -v scripts/run_model.py

# Run with memory profiler
memray run -o outputs/profiles/memray.bin -m scripts.run_model
memray flamegraph outputs/profiles/memray.bin
```

---

## Profiling Tools

### 1. py-spy (Sampling Profiler) — RECOMMENDED

**Best for:** Production profiling, JAX code

**Usage:**
```bash
# Record to SVG flame graph
py-spy record -o profile.svg -- python -m scripts.run_model

# Record top functions
py-spy top -- python -m scripts.run_model

# Attach to running process
py-spy record -p <PID>
```

**Benefits:**
- ✅ Works with JAX/JIT
- ✅ Minimal overhead (<5%)
- ✅ No code changes needed
- ✅ Can attach to running processes

---

### 2. line_profiler

**Best for:** Line-by-line timing

**Usage:**
```bash
# Add @profile decorator to functions
@profile
def compute_equilibrium(params):
    # Implementation
    pass

# Run with line profiler
kernprof -l -v scripts/run_model.py

# View results
python -m line_profiler run_model.py.lprof
```

**Output:**
```
Timer unit: 1e-06 s

Total time: 0.5 s
File: scripts/run_model.py
Function: compute_equilibrium at line 42

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    42                                           @profile
    43                                           def compute_equilibrium(params):
    44         1        50000.0  50000.0     10.0      init = initialize_state(params)
    45       100       400000.0   4000.0     80.0      for i in range(100):
    46        99        49500.0    500.0     10.0          state = update(state)
```

---

### 3. memray (Memory Profiler)

**Best for:** Memory leaks, large allocations

**Usage:**
```bash
# Run with memory profiling
memray run -o memray.bin -m scripts.run_model

# Generate flame graph
memray flamegraph memray.bin

# Generate table
memray table memray.bin

# Generate tree
memray tree memray.bin
```

**Benefits:**
- ✅ Tracks all allocations
- ✅ Identifies memory leaks
- ✅ Native JAX array tracking

---

### 4. cProfile + snakeviz

**Best for:** Function-level timing

**Usage:**
```bash
# Run with cProfile
python -m cProfile -o profile.stats -m scripts.run_model

# View with snakeviz
snakeviz profile.stats
```

---

## JAX-Specific Profiling

### 1. JAX Profiling Utilities

```python
from jax import profiler

# Profile XLA compilation
profiler.start_profiler("outputs/profiles/jax")
result = compiled_function(params)
profiler.stop_profiler()

# View in TensorBoard
tensorboard --logdir outputs/profiles/jax
```

### 2. JAX Memory Statistics

```python
from jax import device_put
import jax

# Check memory usage
print(jax.devices())
print(jax.default_device())

# Profile memory
from jax._src import profiler
profiler.get_memory_profile()
```

### 3. JAX Compilation Cache

```python
from jax import cache_size

# Check cache hits/misses
print(cache_size())

# Clear cache
jax.clear_caches()
```

---

## Optimization Strategies

### 1. Vectorization (vmap)

**Before:**
```python
results = []
for scenario in scenarios:
    result = run_model(scenario)
    results.append(result)
```

**After:**
```python
from jax import vmap

@vmap
def run_model_batched(scenario):
    return run_model(scenario)

results = run_model_batched(scenarios)  # 10-100x faster
```

---

### 2. JIT Compilation

**Before:**
```python
def compute_loss(params, data):
    # Complex computation
    return loss

for i in range(1000):
    loss = compute_loss(params, data)  # Slow
```

**After:**
```python
from jax import jit

@jit
def compute_loss(params, data):
    # Complex computation
    return loss

for i in range(1000):
    loss = compute_loss(params, data)  # Fast
```

---

### 3. Parallel Chains (pmap)

**Before:**
```python
# Sequential MCMC chains
for chain in range(4):
    samples = run_mcmc(rng_key, data)  # Slow
```

**After:**
```python
from jax import pmap

@pmap
def run_chain(keys, data_batched):
    return run_mcmc(keys, data_batched)

# Parallel chains
samples = run_chain(rng_keys, data_batched)  # 4x faster
```

---

## Performance Benchmarks

### Target Performance

| Operation | Target Time | Current | Status |
|-----------|-------------|---------|--------|
| Single policy evaluation | <100ms | TBD | ⏳ |
| Full MCMC (2000 draws) | <30 min | TBD | ⏳ |
| Policy sweep (3 scenarios) | <2 hours | TBD | ⏳ |
| VOI computation | <1 hour | TBD | ⏳ |

---

## Common Performance Issues

### 1. Python Loops (SLOW)

**Problem:**
```python
for i in range(1000):
    x = x + i  # Very slow in Python
```

**Solution:**
```python
import jax.numpy as jnp

x = x + jnp.arange(1000)  # Vectorized
```

---

### 2. Unnecessary Device Transfers

**Problem:**
```python
for i in range(100):
    x = device_put(x)  # Slow transfer
    y = compute(x)
    y = np.array(y)  # Transfer back to CPU
```

**Solution:**
```python
x = device_put(x)  # Once at start
for i in range(100):
    y = compute(x)  # Stay on device
# Transfer back once at end
```

---

### 3. Recomputation vs. Caching

**Problem:**
```python
@jit
def loss(params):
    features = compute_features(params)  # Expensive
    loss1 = compute_loss1(features)
    loss2 = compute_loss2(features)  # Recomputes features!
    return loss1 + loss2
```

**Solution:**
```python
@jit
def loss(params):
    features = compute_features(params)
    loss1 = compute_loss1(features)
    loss2 = compute_loss2(features)  # Uses cached features
    return loss1 + loss2
```

---

## Profiling Workflow

1. **Baseline:** Run without profiling to get baseline time
2. **Profile:** Use py-spy for low-overhead profiling
3. **Identify:** Find top 3 slowest functions
4. **Optimize:** Apply vmap/jit/pmap
5. **Verify:** Re-profile to confirm improvement
6. **Repeat:** Iterate until performance targets met

---

**Version:** 1.0
**Date:** 2026-03-03
**Track:** gdpe_0003_model_implementation
