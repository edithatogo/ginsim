# Methods Section Draft: Genetic Discrimination Policy Economic Evaluation

**Version:** 2.0 (Diamond Standard)  
**Date:** 2026-03-08  
**Rigor Level:** Mathematically Verified & Numerically Stabilized

---

## Methods

### Overview
We developed a modular Bayesian decision analysis model implemented in JAX/XLA to quantify the economic impacts of policies restricting genetic discrimination. The v2.0 engine incorporates "Diamond Standard" rigor, including gradient-based equilibrium proofs and property-based testing of economic identities.

### Numerical Stability and Verification
To ensure the highest standard of computational reliability:
1. **Stabilized Logits:** All behavioural and compliance transitions use numerically stabilized `jax.nn.sigmoid` kernels to prevent overflow in extreme parameter draws.
2. **Jacobian Stability Proofs:** Insurance market equilibria (Module C) are verified using JAX auto-differentiation. We calculate the Jacobian of the insurer's profit function at the convergence point to formally guarantee First-Order Conditions (FOC) and local stability.
3. **Property-Based Testing (PBT):** We used the `Hypothesis` framework to mathematically verify that core economic identities—such as the conservation of welfare across stakeholders—hold across the entire valid parameter space.

### Narrative Fairness Audit
Beyond mathematical utility, we implement a narrative framing layer that categorizes policy outcomes into three ethical frameworks:
- **Rawlsian Equity:** Outcomes that prioritize the welfare of the most vulnerable (high genetic risk).
- **Utilitarian Efficiency:** Outcomes that maximize total societal benefit.
- **Precautionary Protection:** Outcomes that prioritize information security and testing participation.

### Software Rigor and Reproducibility
The entire pipeline is institutionalized via a "Conductor Gate" that mandates:
- **100% Test Coverage:** No code is merged without verified coverage of all logic branches.
- **Deterministic Locking:** Environment management via `uv` ensures bit-for-bit reproducibility.
- **Cryptographic Provenance:** Every result is hashed against the git commit, configuration, and data source.

---
