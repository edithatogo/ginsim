# Track Specification: Comprehensive Sensitivity Suite Overhaul

**Track ID:** gdpe_0038_sensitivity_overhaul
**Type:** Feature / Optimization
**Goal:** Optimize and expand the repository's uncertainty quantification suite (DSA, PSA, Sobol, VOI) and ensure high-rigor integration into the dashboard.

## 1. Overview
The current sensitivity tools exist but are fragmented across several scripts. This track consolidates them into a unified, high-performance engine that leverages JAX vectorization for rapid Monte Carlo simulations (PSA) and Sobol index calculation.

## 2. Functional Requirements
- **Unified Sensitivity Engine:** Create `src/model/uncertainty_engine.py` to house vectorized DSA and PSA logic.
- **Sobol Integration:** Implement JAX-compatible Sobol sequence sampling for high-efficiency global sensitivity analysis.
- **VOI Optimization:** Optimize the Value of Information (VOI) and EVPPI calculations to run in < 10 seconds for the dashboard.
- **Scenario Convergence:** Ensure the scenario analysis engine (`scenario_analysis.py`) uses the same underlying uncertainty kernels.

## 3. Non-Functional Requirements
- **Performance:** PSA with 10,000 draws should complete in < 5 seconds using JAX.
- **Correctness:** Compare new vectorized results against legacy `scripts/run_full_uncertainty.py` to ensure zero regressions.

## 4. Acceptance Criteria
- [ ] Vectorized PSA/Sobol engine functional.
- [ ] EVPPI calculations optimized and verified.
- [ ] New "Global Uncertainty" tab added to Streamlit dashboard.
- [ ] Interaction-level tests confirm uncertainty UI robustness.
