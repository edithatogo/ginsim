# Implementation Plan: Comprehensive Sensitivity Suite Overhaul

**Track ID:** gdpe_0038_sensitivity_overhaul
**Execution mode:** Autonomous Phase Loop (with Ralph thinking)

## Phase 1: Engine Unification (Ralph Loop #1)
- [x] **Task: Deep Exploration of Mathematical Kernels**
    - [x] Perform a "Ralph Thinking" session: Ask "How can we unify DSA, PSA, and Sobol into a single JAX-vectorized map function without sacrificing readability?"
- [x] **Task: Implement `src/model/uncertainty_engine.py`**
- [x] **Task: Conductor - Autonomous Review & Remediation 'Engine'**

## Phase 2: Performance & VOI
- [x] **Task: Vectorize PSA Sampling**
    - [x] Replace Python-level loops with `jax.vmap` or `jax.pmap`.
- [x] **Task: Optimize VOI/EVPPI**
    - [x] Implement the nested-loop optimization from the recent stakeholder meeting recommendations.
- [x] **Task: Conductor - Autonomous Review & Remediation 'Performance'**

## Phase 3: Dashboard Promulgation
- [x] **Task: Overhaul `pages/2_Sensitivity.py`**
    - [x] Add PSA distribution plots (Histograms with 95% CrI).
    - [x] Add Sobol Index bar charts.
- [x] **Task: Integrate VOI into `app.py`**
- [x] **Task: Conductor - Autonomous Review & Remediation 'UI Integration'**

## Phase 4: Iterative Improvement (Ralph Loop #2)
- [x] **Task: Improvement Inquiry**
    - [x] Ask "Could we implement 'Live Stress-Testing' where users drag distributions instead of points?"
    - [x] Suggest 2 additional high-rigor uncertainty features.
- [x] **Task: Close Track**
