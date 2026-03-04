# Specification: Dashboard Enhancements

**Track ID:** gdpe_0012_dashboard_enhancements  
**Type:** Feature  
**Date:** 2026-03-04

---

## 1. Overview

This track implements comprehensive enhancements to the gin-sim Streamlit dashboard based on user feedback, including game diagram visualization, expanded sensitivity and scenario analysis, and verification that the dashboard uses the same JAX/XLA logic as the core model.

---

## 2. Scope

### 2.1 Game Diagrams

1. **Game Structure Visualizations**
   - Module A: Behavior/Deterrence game diagram
   - Module C: Insurance equilibrium (separating vs pooling)
   - Module D: Proxy substitution diagram
   - Module E: Pass-through mechanism
   - Module F: Data quality externality
   - Enforcement: Compliance game

2. **Interactive Elements**
   - Clickable diagrams showing equilibrium outcomes
   - Policy regime overlays
   - Parameter impact visualization

### 2.2 Comprehensive Sensitivity Analysis

1. **One-Way Sensitivity**
   - Tornado diagrams for all parameters
   - Interactive parameter sliders
   - Real-time updates

2. **Multi-Way Sensitivity**
   - Two-way sensitivity surfaces
   - Heat maps for parameter interactions
   - Threshold analysis

3. **Probabilistic Sensitivity**
   - Monte Carlo simulations
   - Cost-effectiveness acceptability curves (CEAC)
   - Uncertainty visualization

### 2.3 Comprehensive Scenario Analysis

1. **Pre-defined Scenarios**
   - Best case policy
   - Worst case policy
   - Current policy (baseline)
   - International comparisons

2. **Custom Scenarios**
   - User-defined parameter sets
   - Save/load scenarios
   - Scenario comparison

3. **Stress Testing**
   - Extreme parameter values
   - Boundary condition testing
   - Model robustness verification

### 2.4 JAX/XLA Logic Verification

1. **Backend Verification**
   - Verify dashboard uses same JAX functions as model
   - Ensure XLA acceleration is enabled
   - Performance benchmarking

2. **Consistency Testing**
   - Compare dashboard outputs with model outputs
   - Verify numerical accuracy
   - Test edge cases

---

## 3. Functional Requirements

### 3.1 Game Diagrams

- [ ] **FR1:** Display 6 game structure diagrams
- [ ] **FR2:** Interactive diagram elements
- [ ] **FR3:** Policy regime overlays on diagrams
- [ ] **FR4:** Equilibrium outcome visualization
- [ ] **FR5:** Export diagrams (PNG, SVG)

### 3.2 Sensitivity Analysis

- [ ] **FR6:** One-way sensitivity (tornado diagrams)
- [ ] **FR7:** Two-way sensitivity (heat maps)
- [ ] **FR8:** Probabilistic sensitivity (CEAC)
- [ ] **FR9:** Interactive parameter controls
- [ ] **FR10:** Real-time updates

### 3.3 Scenario Analysis

- [ ] **FR11:** Pre-defined scenarios (≥5)
- [ ] **FR12:** Custom scenario creation
- [ ] **FR13:** Save/load scenarios
- [ ] **FR14:** Scenario comparison table
- [ ] **FR15:** Stress testing interface

### 3.4 JAX/XLA Verification

- [ ] **FR16:** Verify JAX backend usage
- [ ] **FR17:** Verify XLA acceleration
- [ ] **FR18:** Performance benchmarks
- [ ] **FR19:** Consistency tests with model
- [ ] **FR20:** Documentation of verification

---

## 4. Non-Functional Requirements

### 4.1 Performance

- [ ] **NFR1:** Dashboard load time < 5s
- [ ] **NFR2:** Diagram rendering < 2s
- [ ] **NFR3:** Sensitivity updates < 1s
- [ ] **NFR4:** JAX functions match model performance

### 4.2 Usability

- [ ] **NFR5:** Intuitive navigation
- [ ] **NFR6:** Clear visualizations
- [ ] **NFR7:** Helpful tooltips
- [ ] **NFR8:** Mobile-responsive design

### 4.3 Maintainability

- [ ] **NFR9:** Well-documented code
- [ ] **NFR10:** Modular architecture
- [ ] **NFR11:** Easy to add new diagrams
- [ ] **NFR12:** Easy to add new scenarios

---

## 5. Acceptance Criteria

- [ ] **AC1:** All 6 game diagrams displayed and interactive
- [ ] **AC2:** Comprehensive sensitivity analysis (one-way, two-way, probabilistic)
- [ ] **AC3:** Comprehensive scenario analysis (≥5 pre-defined + custom)
- [ ] **AC4:** Dashboard verified to use same JAX/XLA logic as model
- [ ] **AC5:** Performance acceptable (< 5s load, < 2s rendering)
- [ ] **AC6:** All new features tested (≥20 new tests)
- [ ] **AC7:** Documentation complete

---

## 6. Out of Scope

- Creating new game-theoretic models (only visualization of existing)
- Modifying core model logic (only verification)
- Adding new policy regimes (only visualization of existing)

---

## 7. Deliverables

| ID | Deliverable | Format | Location |
|----|-------------|--------|----------|
| D1 | Game diagrams module | Python | `streamlit_app/pages/game_diagrams.py` |
| D2 | Enhanced sensitivity analysis | Python | `streamlit_app/pages/sensitivity.py` |
| D3 | Scenario analysis module | Python | `streamlit_app/pages/scenarios.py` |
| D4 | JAX verification tests | Python | `tests/verification/test_jax_consistency.py` |
| D5 | Updated README | Markdown | `gin-sim/README.md` |
| D6 | Verification report | Markdown | `docs/JAX_VERIFICATION_REPORT.md` |

---

**Version:** 1.0  
**Date:** 2026-03-04  
**Status:** Ready for planning
