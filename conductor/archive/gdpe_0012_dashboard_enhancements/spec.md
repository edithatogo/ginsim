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

### 2.2 Comprehensive Sensitivity & Uncertainty Analysis

1. **One-Way & Two-Way Sensitivity**
   - Tornado diagrams and interactive heat maps.
   
2. **Global Sensitivity (Sobol Indices)**
   - Implement Sobol indices to identify non-linear parameter interactions.

3. **Probabilistic Sensitivity (CEAC, CEAF, CERAC)**
   - **CEAC:** Probability of cost-effective.
   - **CEAF:** Optimal policy frontier.
   - **CERAC:** Risk-averse Sortino Ratio analysis.

4. **Advanced Welfare & Market Metrics (NEW)**
   - **Distributional Equity (DCEA):** Breakdown of welfare gains by risk-group and income-proxy.
   - **Market Participation (Uninsured Rate):** Calculate the % of population "priced out" at different premium thresholds.
   - **Value of Implementation (VOI-E):** ROI analysis for different enforcement spending levels.
   - **Scientific Opportunity Cost:** Quantify the "delay in medical progress" (in QALYs) due to reduced research participation.


### 2.3 Comprehensive Scenario Analysis & "New Games"

1. **Pre-defined Scenarios (Australia 2025 Ban, FSC Moratorium)**
   
2. **International Benchmarks (NEW)**
   - **USA (GINA):** Health-only protection, life insurance "patchwork".
   - **UK (ABI Code):** £500k cap + Huntington's exception.
   - **Canada (GNDA):** Full criminal prohibition of disclosure.
   - **Belgium/France:** Strict non-acceptance of voluntary results.

3. **AU Policy Designer (Sandbox)**
   - Interactive sliders for $500k/$200k caps and enforcement penalties.

4. **Extended Strategic Games (NEW)**
   - **The "Information Leakage" Game:** Proxy-based risk reconstruction accuracy.
   - **The "Genetic Altruism" Game:** Impact on research biobank participation.
   - **The "Cascade Testing" Game:** Deterrence spillover effects on family members.

5. **Comparative "Delta" View**
   - Side-by-side policy contrast with automatic "Net Gain" calculation.


### 2.4 JAX/XLA Logic & Single Source of Truth

1. **Core-Dashboard Linking (MANDATORY)**
   - Dashboard MUST import from `src/model/pipeline.py`.
   - All analytical logic (Sobol, Leakage Game, CEAF/CERAC) must be implemented as JAX-transformable functions in `src/`.
   - **Scientific Traceability:** All analytical logic changes MUST be documented in `docs/GAME_DESCRIPTIONS.md` and `docs/FORMULAE_INVENTORY.md`.




---

## 3. Functional Requirements

### 3.0 Core Integration (CRITICAL)

- [ ] **FR0.1:** Refactor dashboard to import from `src/model/pipeline.py`
- [ ] **FR0.2:** Remove all duplicated logic from dashboard
- [ ] **FR0.3:** Add `@st.cache_data` for model computations
- [ ] **FR0.4:** Verify JAX/XLA backend usage
- [ ] **FR0.5:** Add JAX consistency tests (≥10 tests)

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

### 3.5 Module Integration

- [ ] **FR21:** Display Module A outputs (Behavior/Deterrence)
- [ ] **FR22:** Display Module C outputs (Insurance Equilibrium)
- [ ] **FR23:** Display Module D outputs (Proxy Substitution)
- [ ] **FR24:** Display Module E outputs (Pass-Through)
- [ ] **FR25:** Display Module F outputs (Data Quality)
- [ ] **FR26:** Display Enforcement outputs (Compliance)
- [ ] **FR27:** Integrate full pipeline evaluation
- [ ] **FR28:** Add VOI/EVPPI analysis tab
- [ ] **FR29:** Add jurisdiction selection (Australia vs New Zealand)

### 3.6 Performance

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

- [ ] **AC0:** Dashboard imports from `src/model/` (no duplicated logic)
- [ ] **AC1:** All 6 game diagrams displayed and interactive
- [ ] **AC2:** Comprehensive sensitivity analysis (one-way, two-way, probabilistic)
- [ ] **AC3:** Comprehensive scenario analysis (≥5 pre-defined + custom)
- [ ] **AC4:** Dashboard verified to use same JAX/XLA logic as model
- [ ] **AC5:** Performance acceptable (< 5s load, < 2s rendering)
- [ ] **AC6:** All new features tested (≥20 new tests)
- [ ] **AC7:** Documentation complete
- [ ] **AC8:** All 6 modules accessible (A, C, D, E, F, Enforcement)
- [ ] **AC9:** VOI/EVPPI analysis working
- [ ] **AC10:** JAX verification tests pass (≥10 tests)

---

## 6. Out of Scope

- Creating new game-theoretic models (only visualization of existing)
- Modifying core model logic (only verification)
- Adding new policy regimes (only visualization of existing)

---

## 7. Deliverables

| ID | Deliverable | Format | Location |
|----|-------------|--------|----------|
| D0 | Refactored dashboard app | Python | `streamlit_app/app.py` |
| D1 | Game diagrams module | Python | `streamlit_app/pages/1_Game_Diagrams.py` |
| D2 | Enhanced sensitivity analysis | Python | `streamlit_app/pages/2_Sensitivity.py` |
| D3 | Scenario analysis module | Python | `streamlit_app/pages/3_Scenarios.py` |
| D4 | VOI analysis module | Python | `streamlit_app/pages/4_VOI_Analysis.py` |
| D5 | UI components library | Python | `streamlit_app/components/` |
| D6 | JAX verification tests | Python | `tests/verification/test_jax_consistency.py` |
| D7 | Updated README | Markdown | `gin-sim/README.md` |
| D8 | JAX verification report | Markdown | `docs/JAX_VERIFICATION_REPORT.md` |
| D9 | Updated requirements | TXT | `streamlit_app/requirements.txt` |

---

**Version:** 1.0  
**Date:** 2026-03-04  
**Status:** Ready for planning
