# Inquiry: Unified JAX-Vectorized Sensitivity Kernel

**Track:** gdpe_0038_sensitivity_overhaul
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How can we unify DSA, PSA, and Sobol into a single JAX-vectorized map function without sacrificing readability?

## 1. The Fragmentation Problem
Currently, our sensitivity tools use different loops:
- **DSA:** Single-parameter grid loops.
- **PSA:** Random sampling loops.
- **Sobol:** Sequence-based sampling loops.

In a traditional environment, these are different classes. In JAX, they should all be **`vmap` operations over a parameter matrix.**

## 2. The Unified Input Matrix
We can define a generic `UncertaintyMatrix` of shape `(N_simulations, N_parameters)`.
- For **DSA:** The matrix is mostly constant, with one column varying in a grid.
- For **PSA:** The matrix is populated by random draws.
- For **Sobol:** The matrix is populated by quasi-random sequences.

## 3. The Unified Engine Design
We will implement a single `evaluate_batch(params_matrix, policy)` function that uses `jax.vmap` to map `evaluate_single_policy` over the entire matrix in one XLA call.

$$ \mathbf{Y} = \text{vmap}(f, \text{in\_axes}=(0, \text{None}))(\mathbf{P}, \text{policy}) $$

- **Benefit:** Massive performance gain (10,000 simulations in milliseconds).
- **Challenge:** The `evaluate_single_policy` function must be fully "Pure JAX" (no side effects or Python branching inside).

## 4. Implementation Action
1. **Create `src/model/uncertainty_engine.py`:** Standardize the `UncertaintyResult` dataclass.
2. **Refactor Pipeline:** Extract the "Core Mathematical Kernel" into a JIT-pure function `evaluate_core_logic` that doesn't use `PolicyConfig` objects (which are Pydantic and slow) but rather raw arrays.
3. **Sobol Generator:** Implement a JAX-compatible Sobol sequence sampler.

## 5. Ralph's Iterative Improvement
- **Self-Inquiry:** "What about the dashboard memory?"
- **Answer:** We should return only the summary statistics (Mean, Median, 95% CrI) and a subsample of 100 points for the swarm plots to keep the Streamlit state lean.
- **Action:** Add a `summary_only` flag to the `evaluate_batch` function.
