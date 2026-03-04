# Implementation Plan: Dashboard Enhancements

**Track ID:** gdpe_0012_dashboard_enhancements  
**Estimated duration:** 2-3 weeks

---

## Phase 1 — Game Diagrams (Week 1)

**Goal:** Add interactive game structure diagrams to dashboard

### Tasks
- [ ] **Task 1.1:** Create game diagram generation functions
    - [ ] Module A diagram (Behavior/Deterrence)
    - [ ] Module C diagram (Insurance Equilibrium)
    - [ ] Module D diagram (Proxy Substitution)
    - [ ] Module E diagram (Pass-Through)
    - [ ] Module F diagram (Data Quality)
    - [ ] Enforcement diagram (Compliance)

- [ ] **Task 1.2:** Create dashboard page for diagrams
    - [ ] New page: `pages/game_diagrams.py`
    - [ ] Navigation from main page
    - [ ] Interactive elements

- [ ] **Task 1.3:** Add export functionality
    - [ ] PNG export
    - [ ] SVG export
    - [ ] Download buttons

**Acceptance criteria:**
- All 6 game diagrams displayed
- Interactive elements working
- Export functionality working

**Phase Completion:**
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

---

## Phase 2 — Comprehensive Sensitivity Analysis (Week 2)

**Goal:** Implement comprehensive sensitivity analysis features

### Tasks
- [ ] **Task 2.1:** One-way sensitivity (tornado diagrams)
    - [ ] Tornado diagram generation
    - [ ] Interactive parameter selection
    - [ ] Real-time updates

- [ ] **Task 2.2:** Two-way sensitivity (heat maps)
    - [ ] Heat map generation
    - [ ] Parameter pair selection
    - [ ] Interactive exploration

- [ ] **Task 2.3:** Probabilistic sensitivity (CEAC)
    - [ ] Monte Carlo simulation
    - [ ] CEAC generation
    - [ ] Uncertainty visualization

- [ ] **Task 2.4:** Create dashboard page
    - [ ] New page: `pages/sensitivity.py`
    - [ ] Tab navigation for different analyses
    - [ ] Export functionality

**Acceptance criteria:**
- One-way sensitivity working
- Two-way sensitivity working
- Probabilistic sensitivity working
- All visualizations interactive

**Phase Completion:**
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

---

## Phase 3 — Scenario Analysis & JAX Verification (Week 3)

**Goal:** Implement scenario analysis and verify JAX logic

### Tasks
- [ ] **Task 3.1:** Pre-defined scenarios
    - [ ] Best case policy
    - [ ] Worst case policy
    - [ ] Current policy (baseline)
    - [ ] International comparisons (≥2)

- [ ] **Task 3.2:** Custom scenarios
    - [ ] Scenario creation interface
    - [ ] Save scenarios
    - [ ] Load scenarios
    - [ ] Scenario comparison table

- [ ] **Task 3.3:** Stress testing
    - [ ] Extreme parameter values
    - [ ] Boundary condition testing
    - [ ] Model robustness verification

- [ ] **Task 3.4:** JAX/XLA verification
    - [ ] Verify JAX backend usage
    - [ ] Verify XLA acceleration
    - [ ] Performance benchmarks
    - [ ] Consistency tests with model

- [ ] **Task 3.5:** Create dashboard page
    - [ ] New page: `pages/scenarios.py`
    - [ ] Scenario management interface
    - [ ] Comparison visualization

**Acceptance criteria:**
- ≥5 pre-defined scenarios
- Custom scenario creation working
- Stress testing complete
- JAX verification complete
- Documentation complete

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
