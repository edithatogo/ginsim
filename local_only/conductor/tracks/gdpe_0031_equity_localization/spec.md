# Track Specification: Equity Localization (Māori & Quintile Weights)

**Track ID:** gdpe_0031_equity_localization
**Type:** Feature / Social Impact
**Goal:** Implement jurisdictional-specific equity weights in the DCBA ledger to support Māori health obligations (NZ) and socio-economic quintile analysis (AU).

## 1. Overview
Current welfare metrics are Utilitarian (sum of benefits). This track enables "Equity-Weighted" social benefit calculations, allowing policymakers to prioritize outcomes for vulnerable or treaty-protected populations.

## 2. Functional Requirements
- **Distributional Weights:** Add `equity_weights: dict[str, float]` to `ModelParameters`.
- **DCBA Integration:** Update `dcba_ledger.py` to apply these weights to specific population sub-segments.
- **Māori Health Framework:** (NZ) Implement a weight factor for Māori health outcomes based on the 'Te Mana Raraunga' principles identified in the simulation.
- **Socio-economic quintiles:** (AU) Implement a weight factor favoring lower-income quintiles who may face greater financial deterrence.

## 3. Acceptance Criteria
- [ ] DCBA ledger supports non-utilitarian (weighted) welfare aggregation.
- [ ] Streamlit dashboard includes an "Equity Weighting" toggle.
- [ ] Fairness Audit (Page 5) reflects these jurisdictional weights.
