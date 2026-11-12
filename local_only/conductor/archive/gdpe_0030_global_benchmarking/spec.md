# Track Specification: Global Benchmarking & Threshold Architecture

**Track ID:** gdpe_0030_global_benchmarking
**Type:** Feature / Architecture
**Goal:** Expand the repository into a Global Benchmarking Engine by adding UK, Canada, and US jurisdictions, implementing threshold-based regulatory math, and standardizing currency via PPP.

## 1. Overview
This track upgrades the core JAX engine and Streamlit dashboard to support complex international comparisons. It transitions parameter handling from hardcoded Python defaults to a data-driven YAML architecture, retrofits existing AU/NZ models with new threshold math, and surfaces a "Cross-Pollination" sandbox in the UI.

## 2. Functional Requirements

### 2.1 Core Engine Expansions (JAX)
- **Threshold Math:** Update Module A and C to handle `sum_insured_thresholds`. If a policy specifies a threshold (e.g., UK ABI Code, AU FSC Moratorium), the model must calculate blended deterrence and premium effects for populations above/below the cap.
- **PPP Normalization:** Update `dcba_ledger.py` to accept local currency and output PPP-adjusted standardized currency for comparative benchmarking.

### 2.2 Parameter Abstraction
- Strip default values from `ModelParameters`.
- Create a configuration ingestion layer that loads `configs/jurisdictions/<country>.yaml`.
- Retrofit Australia and New Zealand to use this new data-driven ingestion.

### 2.3 New Jurisdictions
- Add empirical profiles for **United Kingdom** (ABI Code), **Canada** (GNDA), and **United States** (GINA context).

### 2.4 Streamlit Dashboard Enhancements
- **Global Frontier Chart:** Scatter plot comparing Net Social Benefit (PPP-adjusted) vs. Testing Uptake across all 5 jurisdictions.
- **Counterfactual Sandbox:** UI controls to apply Country A's policy to Country B's population.
- **Regulatory Matrix Table:** Detailed side-by-side comparison of international legal instruments.

## 3. Non-Functional Requirements
- **Test Matrix:** `pytest` must loop over all 5 jurisdiction configs for Property-Based Tests to ensure mathematical stability everywhere.
- **Backward Compatibility:** If thresholds are `None`, the math must default to the current continuous logic.

## 4. Acceptance Criteria
- [ ] JAX functions successfully handle boolean, continuous, and threshold-based enforcement logic.
- [ ] AU, NZ, UK, CAN, US YAML configs created and integrated.
- [ ] `pytest` matrix tests pass across all 5 jurisdictions.
- [ ] Streamlit dashboard renders the "Global Frontier" visualization.
- [ ] "Cross-Pollination" scenarios execute successfully in the app.
