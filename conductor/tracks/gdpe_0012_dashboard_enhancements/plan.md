# Implementation Plan: Dashboard Enhancements

**Track ID:** gdpe_0012_dashboard_enhancements  
**Estimated duration:** 2-3 weeks

---

## Phase 1 — Game Diagrams (Week 1)

**Goal:** Add interactive game structure diagrams to dashboard

### Tasks
- [x] **Task 1.1:** Create game diagram generation functions
    - [x] Module A diagram (Behavior/Deterrence)
    - [x] Module C diagram (Insurance Equilibrium)
    - [x] Module D diagram (Proxy Substitution)
    - [x] Module E diagram (Pass-Through)
    - [x] Module F diagram (Data Quality)
    - [x] Enforcement diagram (Compliance)

- [x] **Task 1.2:** Create dashboard page for diagrams
    - [x] New page: `pages/game_diagrams.py`
    - [x] Navigation from main page
    - [x] Interactive elements

- [x] **Task 1.3:** Add export functionality
    - [x] PNG export
    - [x] SVG export
    - [x] Download buttons

**Acceptance criteria:**
- [x] All 6 game diagrams displayed
- [x] Interactive elements working
- [x] Export functionality working

**Phase Completion:**
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md) 7e0db93

---

## Phase 1.5 — Review Fixes

**Goal:** Address code review findings

### Tasks
- [x] **Task 1.4:** Apply review suggestions
    - [x] Fix unused variables (gauge_y, feedback_arrow)
    - [x] Add 15 unit tests for game diagram generation
    - [x] Add conftest.py for pytest configuration
    - [x] Format code with ruff
    - [x] All tests passing

**Acceptance criteria:**
- [x] All linting issues resolved or documented
- [x] Test coverage added (15 tests)
- [x] All tests passing

---

## Phase 2 — Comprehensive Sensitivity Analysis (Week 2)

**Goal:** Implement comprehensive sensitivity analysis with Sobol indices

**Status:** [x] Complete

### Tasks
- [x] **Task 2.1:** One-way & Two-way sensitivity (Core Implementation) ed5ba95
    - [x] Implement tornado and heat map logic in `src/model/`
    - [x] Link dashboard UI to these core functions
    - [x] Created `src/model/sensitivity_total.py` with JAX-accelerated functions
    - [x] Created Streamlit page with interactive visualizations

- [x] **Task 2.2:** Global Sensitivity (Sobol Indices) ed5ba95
    - [x] Implement Sobol index calculation using JAX/XLA
    - [x] First-order and total-order indices
    - [x] Visualize interaction effects
    - [x] **Review Fixes:** Applied all code review recommendations (CRITICAL + HIGH priority) 3d407ab
    - [x] **Additional Fix:** Bind loop variable in CEAC analysis (B023) 639020d
    - [ ] **Traceability:** Update `docs/UNCERTAINTY_DECOMPOSITION.md`.

- [x] **Task 2.3:** Probabilistic sensitivity (CEAC)
    - [x] JAX-accelerated Monte Carlo simulation
    - [x] CEAC calculation implemented in `src/model/sensitivity_total.py`
    - [ ] CEAC visualization for AU vs NZ (deferred to Phase 3 dashboard integration)

- [ ] **Task 2.4: Advanced Welfare & Market Metrics**
    - [ ] **DCEA Implementation**: Calculate distributional impacts across risk groups.
    - [ ] **Market Tipping Points**: Calculate the % population drop-off (uninsured rate) per $ increase in premium.
    - [ ] **Enforcement ROI**: Model the net benefit of increasing `enforcement_strength` vs. administrative cost.
    - [ ] **Scientific Loss**: Quantify the QALY-equivalent of the "data quality externality" in Module F.


## Phase 3 — Scenario Analysis, JAX Verification & Australian Policy Sandbox (Week 3)

**Goal:** Implement scenario analysis, verify JAX logic, and add AU policy designer

**Status:** [~] In Progress

### Tasks
- [x] **Task 3.1:** Pre-defined scenarios (AU 2025 Ban, FSC Moratorium) 5d31cbf
    - [x] Standardized scenario definitions in `configs/scenarios.yaml`
    - [x] Add scenario selector to dashboard
    - [x] Created 8 predefined scenarios (AU, NZ, international benchmarks)
    - [x] Implemented scenario comparison with delta calculations
    - [x] Australian Policy Designer (Sandbox) with interactive sliders
    - [x] **Review Fixes:** Added 8 unit tests for scenario analysis module 874fc0e

- [ ] **Task 3.3:** **Extended Strategic Games**
    - [ ] Implement **"Information Leakage"**, **"Genetic Altruism"**, and **"Cascade Testing"**.
    - [ ] **Traceability:** Update `docs/GAME_DESCRIPTIONS.md` with new game logic.

- [ ] **Task 3.4:** Comparative **"Delta" View**
    - [ ] Side-by-side policy comparison with automatic Net Welfare Gain calculation.

- [ ] **Task 3.5:** JAX/XLA Performance & Dashboard Finalization
    - [ ] **Performance Benchmarking**: Establish baseline (NumPy) vs. JAX/XLA speedup report.
    - [ ] Final verification of JAX/XLA "Single Source of Truth" implementation.
    - [ ] Add tooltips for international policy terms.


**Phase Completion:**
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

---

## Summary Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| **Phase 1** | Week 1 | Game diagrams (6 diagrams) |
| **Phase 2** | Week 2 | Comprehensive sensitivity analysis |
| **Phase 3** | Week 3 | Scenario analysis + JAX verification |

---

**Version:** 1.0  
**Date:** 2026-03-04
