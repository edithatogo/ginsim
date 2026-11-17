# Track Specification: Regulatory Tapering & Nuance

**Track ID:** gdpe_0032_regulatory_tapering
**Type:** Feature / Regulatory Logic
**Goal:** Implement nuanced 'Sum-Insured Tapering' rules (glide paths) to model gradual loss of protection above financial thresholds.

## 1. Overview
The current threshold logic is binary: protected below cap, unprotected above. Stakeholders (Treasury) requested "Tapering" where protection phases out, reflecting more realistic regulatory compromises.

## 2. Functional Requirements
- **Tapering Schema:** Update `PolicyConfig` to support `taper_range: float` (e.g., $500k to $750k).
- **Smooth Transitions:** Use sigmoid or linear interpolation in JAX to model the gradual increase in deterrence within the taper range.
- **Equilibrium Impact:** Ensure `module_c_insurance_eq.py` calculates the blended premium using the integral of the taper function.

## 3. Acceptance Criteria
- [ ] JAX engine supports continuous tapering of policy protections.
- [ ] Dashboard includes "Taper Width" sliders for Moratorium regimes.
