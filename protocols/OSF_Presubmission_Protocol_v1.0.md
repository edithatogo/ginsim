# OSF Presubmission: Protocol Summary (Copy-Paste Ready)

**Title:** Integrated Economic Evaluation of Policy Options to Restrict Genetic Discrimination  
**Version:** v1.0  
**Date:** 02 March 2026  
**Primary investigator:** Dylan A. Mordaunt (edit)  



---
**Repo update:** executable scaffolds for Modules D–F and VOI added in v1.1 (02 March 2026).
---

## Study type

**Initial jurisdictions (implementation focus):** Australia and Aotearoa New Zealand (life insurance), with jurisdiction-specific comparators defined in the repository configuration.

Policy evaluation using linked empirical estimation and decision-analytic modelling (confirmatory primary outcomes with exploratory secondary analyses).

## Research questions
1. What are the net social impacts of alternative policy regimes restricting the use of genetic information (health, fiscal, insurance market, and welfare)?
2. How much does each policy regime change genetic testing uptake, cascade testing, and research participation?
3. What is the magnitude of adverse selection and premium impacts under each policy regime, including proxy substitution and market structure effects?
4. Which uncertainties most influence the preferred policy choice (VOI)?

## Hypotheses
H1. More protective regimes reduce deterrence and increase uptake of clinically indicated genetic testing and cascade testing.  
H2. Increased testing yields net health gains and, for selected conditions, offsets some downstream costs through prevention and early detection.  
H3. More restrictive information regimes increase adverse selection pressure in voluntary risk-rated insurance, raising premiums relative to less restrictive regimes, but the magnitude depends on product design, caps, and risk-sharing.  
H4. Net distributional welfare improves for people with higher genetic risk, with overall net effect depending on premium incidence and fiscal spillovers.

## Design plan
### Data sources
- Genetic testing utilisation time series (claims, lab volumes, registries).
- Surveys and/or discrete choice experiments about perceived discrimination risk and testing behaviour.
- Clinical outcomes and effect estimates for preventive interventions.
- Insurance market data (take-up, sums insured, premiums, underwriting outcomes, lapse, reinsurance), aggregated if required.
- Genomic research participation metrics, where available.

### Units and samples
Population-level time series for utilisation and insurance outcomes, with subgroup stratification where data permit. Condition-level modelling for prioritised genetic conditions.

### Primary outcomes
1. Change in testing uptake and cascade testing (relative and absolute).  
2. Change in premiums and take-up for selected insurance products.  
3. Net QALYs and net costs (health system and prevention).  
4. Net fiscal impact.  
5. Net distributional welfare impacts (DCBA) and uncertainty around preferred policy.

### Secondary outcomes
- Proxy substitution effects on underwriting accuracy and subgroup mispricing.
- Pass-through and incidence (consumer vs insurer).
- Data-quality externality metrics (representativeness and predictive tool performance).

## Analysis plan

**Strategic interactions:** The analysis explicitly models key strategic channels (insurance screening/adverse selection; testing participation under perceived penalties; proxy substitution; data-quality externalities; enforcement), summarised in `docs/GAME_THEORETIC_FRAMING.md`.

### Overview
A modular, linked Bayesian decision analysis implemented with JAX/XLA (NumPyro and BlackJAX) and differentiable simulation. Policy contrasts use common random numbers.

### Statistical models
- Module A (behaviour/uptake): Bayesian event-study and/or diffusion model; latent perceived-risk factor if survey data available.
- Module B (clinical): disease-specific microsimulation or Markov models; uncertainty propagated via priors on penetrance, effects, and adherence.
- Module C (insurance equilibrium): structural demand and pricing; equilibrium solved via JAX root finding; adverse selection represented as informed demand shifts.
- Modules D to F: underwriting prediction under constraints, pass-through models, and selection-bias evaluation of genomic datasets.

### Inference
- MCMC (NUTS/HMC) or tempered SMC via BlackJAX where appropriate.
- Variational inference (SVI) or normalizing flows when likelihoods are difficult or speed is required.
- Probabilistic sensitivity analysis integrates uncertainty across modules.

### Decision criteria
Preferred policy is selected based on a pre-specified decision metric set:
- Net benefits (DCBA), distributional impacts, and uncertainty.
- Social welfare where utility-based evaluation is feasible.
- VOI to prioritise future evidence generation.

### Robustness checks
- High/low deterrence and high/low adverse selection scenarios.
- Alternative proxy substitution specifications.
- Competitive vs concentrated market pass-through assumptions.
- Posterior predictive checks for module-level fit.

## Data management and sharing
- Use de-identified data where possible and comply with jurisdictional privacy laws for genetic and insurance data.
- Publish aggregated outputs and code where permitted.
- Where data cannot be shared, publish synthetic exemplars and reproducible run manifests.

## Deviations
Any deviations from this prespecified analysis plan will be documented with rationale, dated, and versioned, and will be reported alongside results.
