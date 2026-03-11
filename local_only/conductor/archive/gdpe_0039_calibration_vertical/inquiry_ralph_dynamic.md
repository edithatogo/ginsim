# Inquiry: Automated Bayesian Model Updates

**Track:** gdpe_0039_calibration_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement fully automated Bayesian model updates using BlackJAX/NumPyro when new regional data is uploaded to the dashboard?

## 1. The Dynamic Calibration Frontier
Currently, we use static grounded priors (Lacker & Weinberg 1989, Taylor 2021). As jurisdictional data arrives (e.g., from the Royal Australasian College of Physicians), we have an opportunity to move from **Priors** to **Posteriors** dynamically.

## 2. Technical Feasibility
JAX is the backend for both `NumPyro` and `BlackJAX`.
- **SVI (Stochastic Variational Inference):** Could be implemented as a dashboard background task. When a user uploads a CSV of "Testing Share by Year", the engine runs SVI to update the `deterrence_elasticity` mean and variance in real-time.
- **MCMC:** Too slow for interactive UI but could be run as a "Nightly Job" via a GitHub Action.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is it overkill for policy analysis?"
- **Answer:** Not for a Nature-level publication. Reviewers will ask how we accounted for the most recent data. Automated Bayesian updating provides a "Future-Proof" answer.
- **Action:** I recommend adding a `calibration_mode: [static, dynamic]` toggle to the `HyperParameters` in **Track `gdpe_0042_temporal_evolution`**.
