# SOTA Profiling and Coverage Guide

**Track:** gdpe_0003_model_implementation
**Purpose:** Comprehensive SOTA profiling and coverage
**Date:** 2026-03-03
**Version:** 2.0

---

## Executive Summary

**SOTA Stack:**

| Category | Tool | Why SOTA |
|----------|------|----------|
| **CPU Profiler** | scalene | CPU+GPU+memory, ML-aware, 0.1% overhead |
| **Call Stack** | pyinstrument | Better than cProfile, interactive |
| **Sampling** | py-spy | Works with JAX, production-safe |
| **Memory** | memray | Flame graphs, leak detection |
| **Line Profiler** | line_profiler | Line-by-line timing |
| **Coverage** | coverage.py + diff-cover | Branch coverage, PR integration |
| **Mutation** | mutmut | Tests your tests |
| **Property** | hypothesis | Finds edge cases |

---

## 1. Scalene (SOTA CPU+GPU+Memory Profiler)

**Why SOTA:**
- ✅ Profiles CPU, GPU, AND memory simultaneously
- ✅ ML-aware (recognizes NumPy, JAX, PyTorch operations)
- ✅ 0.1% overhead (vs 10-50% for other profilers)
- ✅ Shows exact lines causing allocations
- ✅ Differentiates Python vs native code time

**Usage:**
```bash
# Profile script
scalene scripts/run_model.py

# Profile with output file
scalene --outfile outputs/profiles/scalene.html scripts/run_model.py

# Profile module
scalene -m scripts.run_model

# Profile with GPU (if available)
scalene --gpu scripts/run_model.py
```

**Output:**
```
                              Scalene: Summary by Filename

  Filename                           CPU Time    GPU Time    Memory Time
  ─────────────────────────────────  ──────────  ──────────  ────────────
  src/model/module_c_equilibrium.py     45.2s       0.0s         12.3s
  src/model/module_a_behavior.py        23.1s       0.0s          5.6s
  scripts/run_model.py                  12.4s       0.0s          2.1s
```

**Key Features:**
- 🔥 **Hotspot detection:** Shows exact lines consuming most CPU
- 💾 **Memory leaks:** Identifies lines causing allocations
- 🎯 **Copy volume:** Shows excessive data copying
- ⚡ **Vectorization opportunities:** Highlights Python loops that could be vectorized

---

## 2. PyInstrument (Call Stack Profiler)

**Why SOTA:**
- ✅ Sampling profiler (low overhead)
- ✅ Shows call stack, not just flat function times
- ✅ Interactive HTML output
- ✅ Works with JAX

**Usage:**
```bash
# Profile and save
pyinstrument -r html -o outputs/profiles/pyinstrument.html scripts/run_model.py

# Profile module
pyinstrument -m scripts.run_model

# Show in terminal
pyinstrument scripts/run_model.py
```

**Output (terminal):**
```
  _     ._   __/__   _ _  _  _ _/_   Recorded: 14:30:00  Samples:  1000
 /_//_/// /_\ / //_// / //_'/ //     Duration: 00:05.234   CPU Time:  4.891

Time   Total Time   File                 Function
────   ──────────   ────                 ────────
5.234  100.0%       scripts/run_model.py main
                       └─ 4.123 (78.8%)  src/model/equilibrium.py compute_equilibrium
                          └─ 3.456 (66.0%) src/model/utils.py solve_root
                             └─ 2.789 (53.3%) jax/_src/lax.py control_flow
```

---

## 3. Py-Spy (Production Sampling Profiler)

**Why SOTA:**
- ✅ Works with JAX/JIT code
- ✅ Can attach to running processes
- ✅ <5% overhead
- ✅ No code changes needed

**Usage:**
```bash
# Record to flame graph
py-spy record -o outputs/profiles/flame.svg -- python -m scripts.run_model

# Record top functions
py-spy top -- python -m scripts.run_model

# Attach to running process
py-spy record -p <PID> -o profile.svg

# Record with native frames (shows JAX internals)
py-spy record --native -o profile.svg -- python -m scripts.run_model
```

---

## 4. Memray (Memory Profiler)

**Why SOTA:**
- ✅ Tracks all memory allocations
- ✅ Native JAX array tracking
- ✅ Flame graphs for memory
- ✅ Leak detection

**Usage:**
```bash
# Run with memory profiling
memray run -o outputs/profiles/memray.bin -m scripts.run_model

# Generate flame graph
memray flamegraph outputs/profiles/memray.bin

# Generate table
memray table outputs/profiles/memray.bin

# Generate tree view
memray tree outputs/profiles/memray.bin

# Find leaks (compare two snapshots)
memray diff snapshot1.bin snapshot2.bin
```

---

## 5. Line Profiler (Line-by-Line Timing)

**Usage:**
```python
# Add @profile decorator
@profile
def compute_equilibrium(params):
    init = initialize_state(params)  # Line 42
    for i in range(100):  # Line 43
        state = update(state)  # Line 44
    return state  # Line 45
```

```bash
# Run with line profiler
kernprof -l -v scripts/run_model.py

# View results
python -m line_profiler run_model.py.lprof
```

**Output:**
```
Timer unit: 1e-06 s

Total time: 0.5123 s
File: scripts/run_model.py
Function: compute_equilibrium at line 42

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    42                                           @profile
    43         1        50000.0  50000.0      9.8      init = initialize_state(params)
    44       100       400000.0   4000.0     78.1      for i in range(100):
    45        99        62300.0    629.3     12.2          state = update(state)
```

---

## 6. Coverage (SOTA Configuration)

**Configuration (pyproject.toml):**
```toml
[tool.coverage.run]
source = ["src"]
branch = true  # Branch coverage, not just line
parallel = true  # Parallel execution
concurrency = ["multiprocessing", "thread"]  # Multi-process support
sigterm = true  # Handle SIGTERM gracefully
plugins = ["covdefaults"]  # Sensible defaults

[tool.coverage.report]
show_missing = true
precision = 2
fail_under = 85.0  # Fail if <85% coverage
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]
```

**Usage:**
```bash
# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# View HTML report
open outputs/coverage_html/index.html

# Generate badge
coverage-badge -o outputs/coverage.svg

# Coverage on PR diff
diff-cover coverage.xml --compare-branch=origin/main
```

**Output:**
```
Name                                    Stmts   Miss Branch   BrPart  Cover   Missing
-------------------------------------------------------------------------------------
src/model/module_a_behavior.py            150      8     42        3    93%   45-48, 67, 89
src/model/module_c_equilibrium.py         230     12     68        5    92%   123-130, 156, 178, 201
src/model/module_d_proxy.py               120      5     34        2    95%   78-80, 95
-------------------------------------------------------------------------------------
TOTAL                                    1500     85    420       20    91%

Required test coverage: 85.0%
Reached 91.0% ✅
```

---

## 7. Diff Cover (Coverage on PRs)

**Purpose:** Ensure new code is tested

**Usage:**
```bash
# Run on PR diff
diff-cover coverage.xml --compare-branch=origin/main

# Output
-------------
Diff Coverage
Diff: origin/main...HEAD, 85% covered
-------------
src/model/new_module.py (92.3%): Missing lines 45-48, 67
-------------
Total:   150 lines
Missing: 12 lines
Coverage: 92%
-------------
```

**CI Integration:**
```yaml
# .github/workflows/ci.yaml
- name: Check diff coverage
  run: |
    pytest --cov=src --cov-report=xml
    diff-cover coverage.xml --fail-under=80 --compare-branch=origin/main
```

---

## 8. Complete Profiling Workflow

### Step 1: Baseline
```bash
# Run without profiling
time python -m scripts.run_model --n_draws 100
```

### Step 2: Scalene (CPU+Memory)
```bash
# Identify hotspots
scalene --outfile outputs/profiles/scalene.html scripts/run_model.py
```

### Step 3: PyInstrument (Call Stack)
```bash
# Understand call patterns
pyinstrument -r html -o outputs/profiles/pyinstrument.html scripts/run_model.py
```

### Step 4: Line Profiler (Specific Functions)
```bash
# Profile specific slow functions
kernprof -l -v scripts/run_model.py
```

### Step 5: Optimize
```python
# Apply optimizations based on profiling data
# - Add @jit to hot functions
# - Use vmap for loops
# - Reduce memory allocations
```

### Step 6: Verify
```bash
# Re-profile to confirm improvement
scalene scripts/run_model.py
```

### Step 7: Coverage
```bash
# Ensure tests cover optimized code
pytest --cov=src --cov-report=html
diff-cover coverage.xml --compare-branch=origin/main
```

---

## 9. JAX-Specific Profiling

### JAX Profiler
```python
from jax import profiler

profiler.start_profiler("outputs/profiles/jax")
result = compiled_function(params)
profiler.stop_profiler()

# View in TensorBoard
tensorboard --logdir outputs/profiles/jax
```

### JAX Memory Stats
```python
import jax

# Check device memory
print(jax.devices())
print(jax.default_device())

# Profile memory
from jax._src import profiler
profiler.get_memory_profile()
```

### JAX Compilation Cache
```python
from jax import cache_size

# Check cache hits/misses
print(cache_size())

# Clear cache
jax.clear_caches()
```

---

## 10. Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Test Coverage** | >85% | `coverage report` |
| **Branch Coverage** | >80% | `coverage report --show-missing` |
| **Mutation Score** | >70% | `mutmut results` |
| **Single Policy Eval** | <100ms | `py-spy` |
| **Full MCMC (2000 draws)** | <30 min | `time` |
| **Memory Usage** | <4GB | `memray` |
| **JAX Compilation** | <10s | `pyinstrument` |

---

## 11. Common Issues and Solutions

### Issue: JAX JIT Not Working
**Symptom:** Slow execution, no compilation
**Solution:**
```python
from jax import jit

@jit
def slow_function(params):
    # Implementation
    pass
```

### Issue: Excessive Memory
**Symptom:** OOM errors, slow execution
**Detection:** `memray` or `scalene --memory`
**Solution:**
```python
# Use generators instead of lists
for item in generator():  # ✅
    process(item)

# Instead of:
items = list(all_data())  # ❌
for item in items:
    process(item)
```

### Issue: Python Loops
**Symptom:** Scalene shows "Python time" >> "Native time"
**Solution:**
```python
# Vectorize with vmap
from jax import vmap

@vmap
def process_batch(item):
    return expensive_op(item)

results = process_batch(batch)  # ✅ Fast
```

---

## 12. CI/CD Integration

```yaml
# .github/workflows/ci.yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-report=xml --cov-report=term-missing

- name: Check coverage
  run: |
    coverage report --fail-under=85

- name: Check diff coverage
  run: |
    diff-cover coverage.xml --fail-under=80 --compare-branch=origin/main

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

---

**Version:** 2.0
**Date:** 2026-03-03
**Track:** gdpe_0003_model_implementation
