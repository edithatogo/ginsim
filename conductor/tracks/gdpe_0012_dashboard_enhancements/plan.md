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

### Tasks
- [ ] **Task 2.1:** One-way & Two-way sensitivity (Core Implementation)
    - [ ] Implement tornado and heat map logic in `src/model/`
    - [ ] Link dashboard UI to these core functions

- [ ] **Task 2.2:** Global Sensitivity (Sobol Indices)
    - [ ] **NEW:** Implement Sobol index calculation using JAX/XLA
    - [ ] Visualize interaction effects in AU policy context

- [ ] **Task 2.3:** Probabilistic sensitivity (CEAC)
    - [ ] JAX-accelerated Monte Carlo simulation
    - [ ] CEAC visualization for AU vs NZ

## Phase 3 — Scenario Analysis, JAX Verification & Australian Policy Sandbox (Week 3)

**Goal:** Implement global scenario analysis, verify JAX logic, and add AU policy designer

### Tasks
- [ ] **Task 3.1:** Pre-defined scenarios & **International Benchmarks**
    - [ ] Australia 2025 Ban vs. FSC Moratorium
    - [ ] **USA GINA**: Health-only baseline
    - [ ] **UK Code**: High-cap Huntington's exception
    - [ ] **Canada GNDA**: Criminal non-disclosure

- [ ] **Task 3.2:** **Australian Policy Designer (Sandbox)**
    - [ ] Interactive sliders for caps ($500k/$200k) and enforcement penalties

- [ ] **Task 3.3:** **Extended Strategic Games**
    - [ ] **NEW:** Implement **"Information Leakage"** proxy-bypass logic
    - [ ] **NEW:** Implement **"Genetic Altruism"** research participation impact
    - [ ] **NEW:** Implement **"Cascade Testing"** family deterrence impact

- [ ] **Task 3.4:** Comparative **"Delta" View**
    - [ ] Side-by-side policy comparison with automatic Net Welfare Gain calculation

- [ ] **Task 3.5:** JAX/XLA "Single Source of Truth" & Dashboard Finalization
    - [ ] Refactor dashboard to import directly from `src/model/`
    - [ ] Add tooltips for international policy terms




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
