# Track Specification: Bayesian Calibration Vertical

**Track ID:** gdpe_0039_calibration_vertical
**Type:** Structural Overhaul / Bayesian
**Goal:** Transition point-estimate parameters to full Bayesian distributions using NumPyro/BlackJAX, anchored in GRADE evidence quality.

## 1. Overview
Currently, the model uses YAML point estimates. To reach SOTA scientific standards, we must model parameter uncertainty explicitly. This track implements a Bayesian Inference layer that translates "GRADE Evidence Strength" into "Prior Distribution Width."

## 2. Functional Requirements
- **Prior Generator:** Implement logic to convert YAML evidence ratings (High, Low, Very Low) into parameterized distributions (e.g., Beta, Gamma).
- **Inference Engine:** Integrate `NumPyro` for MCMC/SVI sampling of the model parameters.
- **Uncertainty Propagation:** Ensure the central pipeline supports distribution-in / distribution-out execution.

## 3. Acceptance Criteria
- [ ] Model results display 95% Credible Intervals (CrI) instead of just point estimates.
- [ ] New "Evidence to Prior" mapping documented.
- [ ] Dashboard includes a "Prior Probability Explorer."
