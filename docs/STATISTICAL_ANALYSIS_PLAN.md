# Statistical Analysis Plan

**Track:** gdpe_0004_quality_assurance  
**Version:** 1.0  
**Date:** 2026-03-03

---

## 1. Overview

This document outlines the statistical analysis plan for the genetic discrimination policy economic evaluation.

---

## 2. Primary Analysis

### 2.1 Policy Comparison

**Objective:** Compare policy regimes (status quo, moratorium, statutory ban)

**Method:** Bayesian decision analysis with probabilistic sensitivity analysis

**Outcomes:**
- Testing uptake (absolute and relative change)
- Insurance premiums (by risk group)
- Net welfare impact (DCBA)
- QALYs gained/lost
- Fiscal impact

**Analysis:**
```python
# For each policy scenario
for policy in [status_quo, moratorium, ban]:
    # Run model with 2000 posterior draws
    results = run_policy_evaluation(policy, n_draws=2000)
    
    # Compute outcomes
    uptake = results.testing_uptake
    premiums = results.insurance_premiums
    welfare = results.welfare_impact
    
    # Store results
    store_results(policy, results)
```

### 2.2 Uncertainty Quantification

**Method:** Probabilistic sensitivity analysis

**Parameters:**
- All model parameters varied simultaneously
- Distributions from evidence registers
- 2000 Monte Carlo draws

**Outputs:**
- 95% credible intervals for all outcomes
- Cost-effectiveness acceptability curves
- Uncertainty intervals for welfare impacts

---

## 3. Secondary Analysis

### 3.1 Value of Information

**Objective:** Identify research priorities

**Method:** EVPI and EVPPI computation

**Analysis:**
```python
# Compute EVPI
evpi = compute_evpi(net_benefits, optimal_benefit)

# Compute EVPPI by parameter group
evppi = compute_evppi(
    net_benefits,
    parameter_samples,
    optimal_benefit,
)
```

**Outputs:**
- EVPI (overall uncertainty)
- EVPPI by parameter group
- Research priority ranking

### 3.2 Sensitivity Analysis

**Objective:** Identify key drivers of results

**Method:**
- One-way sensitivity (tornado diagrams)
- Scenario analysis (best/worst case)
- Threshold analysis

**Analysis:**
```python
# One-way sensitivity
for param in key_parameters:
    result = one_way_sensitivity(
        model_func,
        base_params,
        param,
        range_pct=0.25,
    )
```

---

## 4. Subgroup Analysis

### 4.1 By Jurisdiction

- Australia (separate analysis)
- New Zealand (separate analysis)
- Comparative analysis (AU vs NZ)

### 4.2 By Risk Group

- High-risk individuals
- Low-risk individuals
- Average population

---

## 5. Model Validation

### 5.1 Face Validity

**Method:** Expert review

**Process:**
- Send model structure to ≥2 experts
- Collect feedback on assumptions
- Document and address all comments

### 5.2 Cross-Validation

**Method:** Compare to published studies

**Targets:**
- Hersch & Viscusi (2019) - adverse selection
- Bombard et al. (2018) - systematic review
- Taylor et al. (2021) - Australian evidence

**Acceptance:** ≥70% good/moderate agreement

### 5.3 Stress Tests

**Method:** Extreme scenario testing

**Scenarios:**
1. 100% testing uptake
2. 0% adverse selection
3. 100% enforcement
4. 0% enforcement
5. 100% proxy substitution
6. 0% proxy substitution
7. Best case policy
8. Worst case policy

**Acceptance:** All scenarios pass logical consistency checks

### 5.4 Posterior Predictive Checks

**Method:** Compare model outputs to empirical targets

**Targets:**
- Testing uptake: 0.52 (95% CI: 0.48-0.56)
- Deterrence rate: 0.18 (95% CI: 0.11-0.25)

**Acceptance:**
- Coverage >50%
- Bias <20%

---

## 6. Software

### 6.1 Implementation

**Language:** Python 3.10+

**Libraries:**
- JAX/XLA (numerical computation)
- NumPyro (Bayesian inference)
- BlackJAX (MCMC sampling)
- attrs (data structures)
- msgspec (serialization)
- beartype (runtime type checking)
- chex (testing)

### 6.2 Reproducibility

**Seeds:** Fixed random seed (20260303)

**Version Control:** Git with tagged releases

**Run Manifests:** Each run generates manifest with:
- Git commit hash
- Timestamp
- Config file hash
- Parameter values

---

## 7. Reporting

### 7.1 Tables

**Format:** Publication-ready tables

**Content:**
- Baseline characteristics
- Policy outcomes (mean, 95% CI)
- Incremental effects
- VOI results

### 7.2 Figures

**Format:** 1200dpi PNG + SVG

**Content:**
- Model structure diagram
- Policy comparison (forest plots)
- Uncertainty (CEAC curves)
- Sensitivity (tornado diagrams)
- VOI results (bar charts)

### 7.3 Supplementary Materials

**Content:**
- Full model equations
- Parameter tables (all parameters)
- Additional sensitivity analyses
- Code availability statement

---

## 8. Timeline

| Activity | Date | Status |
|----------|------|--------|
| Analysis plan | 2026-03-03 | ✅ Complete |
| Model runs | 2026-03-10 | ⏳ Pending |
| Validation | 2026-03-17 | ⏳ Pending |
| Results tables | 2026-03-24 | ⏳ Pending |
| Figures | 2026-03-31 | ⏳ Pending |
| Manuscript | 2026-04-14 | ⏳ Pending |

---

## 9. Approvals

**Prepared by:** Dylan A. Mordaunt  
**Date:** 2026-03-03

**Reviewed by:** [Pending expert review]  
**Date:** [Pending]

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial version |

---

**END OF STATISTICAL ANALYSIS PLAN**
