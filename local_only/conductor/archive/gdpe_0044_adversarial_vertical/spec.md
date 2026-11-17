# Track Specification: Adversarial Economic Red-Teaming Vertical

**Track ID:** gdpe_0044_adversarial_vertical
**Type:** Structural Overhaul / Robustness
**Goal:** Implement an Adversarial Engine using JAX optimization to identify the specific parameter combinations that collapse the model's equilibria.

## 1. Overview
A truly robust model should seek its own point of failure. This track implements "Red Teaming" for economics, using gradient-based optimization to find the "Worst-Case Scenario" for each policy.

## 2. Functional Requirements
- **Adversarial Engine:** Implement `src/model/adversarial_engine.py` using `Optax`.
- **Breaking Point Search:** Minimize `Net Social Benefit` or `Insurer Profits` with respect to model parameters to find market collapse thresholds.
- **Robustness Surface:** Calculate the "Safe Zone" manifold for policy stability.

## 3. Acceptance Criteria
- [ ] Every policy regime has a documented "Breaking Point" (the parameter values where it fails).
- [ ] New "Market Stress Test" tab added to Streamlit.
- [ ] Automated "Red Teaming Report" generated per run.
