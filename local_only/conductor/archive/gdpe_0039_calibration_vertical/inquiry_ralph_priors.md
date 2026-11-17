# Inquiry: Hierarchical Bayesian Prior Structure

**Track:** gdpe_0039_calibration_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How do we structure hierarchical priors for global elasticities to satisfy both local nuance and global consistency?

## 1. The Global Hierarchy
We model 5 jurisdictions. While they have different systems (Medicare, ACC, NHS), the underlying "Genetic Altruism" and "Insurance Deterrence" behaviors likely share a common human core.
- **Top Level:** $\theta_{global} \sim \text{Normal}(\mu, \sigma)$ (The "Global Human" elasticity).
- **Jurisdictional Level:** $\theta_{j} \sim \text{Normal}(\theta_{global}, \tau)$ (Local deviation based on institutional culture).

## 2. Parameter Priors

### Adverse Selection Elasticity
- **Source:** Grounded in Lacker & Weinberg (1989) and updated for genomic markets.
- **Prior:** $\text{LogNormal}(-1.2, 0.3)$ (Ensures elasticity is negative and concentrated around -0.3).

### Deterrence Elasticity
- **Source:** Qualitative surveys (Taylor et al. 2021).
- **Prior:** $\text{Gamma}(2.0, 10.0)$ (Concentrated around 0.2, strictly positive).

## 3. Implementation Action
1. **Create `src/inference/priors.py`:** Define the NumPyro model for hierarchical parameter estimation.
2. **Refactor `uncertainty_engine.py`:** Replace the uniform jitter logic with draws from these Bayesian posteriors (or priors if no data).
3. **Data Linkage:** Implement a `InferenceData` class that can load historical testing share data for AU/NZ to "Tighten" the priors.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "Do we need full MCMC or is SVI enough?"
- **Answer:** For the dashboard, we should use **Stochastic Variational Inference (SVI)** to get posterior approximations in seconds. We reserve MCMC for the "Nature Submission" scripts.
- **Action:** Add an `inference_mode` toggle to the engine.
