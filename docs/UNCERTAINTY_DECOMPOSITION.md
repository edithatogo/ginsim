# Uncertainty Decomposition Analysis

## Overview

This document describes the uncertainty quantification methods used in the genetic discrimination policy model, including sensitivity analysis and value of information (VOI) calculations.

## Sensitivity Analysis Methods

### One-Way Sensitivity (Tornado Diagrams)

**Purpose:** Identify which parameters have the largest impact on model outcomes.

**Method:**
- Vary each parameter ±25% from baseline
- Calculate change in testing uptake
- Rank parameters by sensitivity magnitude

**Implementation:** `src/model/sensitivity_total.py::tornado_sensitivity()`

**Key Findings:**
- Deterrence elasticity typically has the largest effect on testing uptake
- Enforcement strength is critical for policy effectiveness
- Proxy accuracy significantly impacts ban effectiveness

### Two-Way Sensitivity (Heat Maps)

**Purpose:** Explore interactions between pairs of parameters.

**Method:**
- Create 2D grid of parameter combinations
- Evaluate model at each grid point
- Visualize outcome surface

**Implementation:** `src/model/sensitivity_total.py::twoway_sensitivity()`

**Key Interactions:**
- Enforcement × Penalty Rate: Strong interaction for compliance
- Proxy Accuracy × Inference Strength: Determines information leakage

### Global Sensitivity (Sobol Indices)

**Purpose:** Decompose output variance into contributions from each parameter and their interactions.

**Method:**
- Saltelli's sampling scheme for efficient estimation
- First-order indices (S_i): Main effects
- Total-order indices (S_Ti): Main effects + all interactions

**Implementation:** `src/model/sensitivity_total.py::sobol_sensitivity()`

**Interpretation:**
- **S_i >> 0**: Parameter has strong main effect
- **S_Ti >> S_i**: Parameter has strong interaction effects
- **S_i ≈ S_Ti ≈ 0**: Parameter has minimal impact

**Typical Results:**
| Parameter | S_i (First-Order) | S_Ti (Total-Order) | Interpretation |
|-----------|------------------|-------------------|----------------|
| Deterrence Elasticity | 0.45 | 0.52 | Strong main effect |
| Enforcement Strength | 0.28 | 0.41 | Moderate + interactions |
| Proxy Accuracy | 0.15 | 0.35 | Weak main, strong interactions |

## Value of Information Analysis

### Expected Value of Perfect Information (EVPI)

**Purpose:** Quantify the maximum value of eliminating all uncertainty.

**Formula:**
```
EVPI = E[max_a U(a, θ)] - max_a E[U(a, θ)]
```

Where:
- `a` = policy action (ban, moratorium, status quo)
- `θ` = uncertain parameters
- `U` = utility/welfare function

**Implementation:** `src/model/voi.py::calculate_evpi()`

**Interpretation:**
- High EVPI → Decision is sensitive to uncertainty
- Low EVPI → Current evidence sufficient for decision

### Expected Value of Partial Perfect Information (EVPPI)

**Purpose:** Identify which parameters are most valuable to research.

**Method:**
- Calculate EVPI for subsets of parameters
- Rank parameters by EVPPI

**Implementation:** `src/model/voi.py::calculate_evpPI()`

**Typical EVPPI Rankings:**
1. Deterrence elasticity (highest research priority)
2. Enforcement effectiveness
3. Proxy substitution accuracy

## Probabilistic Sensitivity Analysis

### Cost-Effectiveness Acceptability Curves (CEAC)

**Purpose:** Show probability that each policy is cost-effective at different willingness-to-pay thresholds.

**Method:**
- Monte Carlo simulation with parameter uncertainty
- Calculate net benefit for each policy at each threshold
- Count frequency each policy is optimal

**Implementation:** `src/model/sensitivity_total.py::ceac_analysis()`

**Interpretation:**
- Curve position = probability of cost-effectiveness
- Curve slope = decision uncertainty
- Crossing points = threshold where optimal policy changes

### Cost-Effectiveness Acceptability Frontier (CEAF)

**Purpose:** Show optimal policy and its certainty across thresholds.

**Method:**
- Identify policy with highest expected net benefit at each threshold
- Plot probability that optimal policy is truly cost-effective

**Status:** Planned for future implementation

## Key Uncertainties by Parameter Group

### Behavioral Parameters
- **Deterrence Elasticity:** ±30% uncertainty range
- **Baseline Testing Uptake:** ±10% uncertainty range
- **Research Priority:** HIGH (large EVPPI)

### Insurance Market Parameters
- **Risk Premium Differential:** ±20% uncertainty range
- **Information Asymmetry:** ±25% uncertainty range
- **Research Priority:** MEDIUM

### Enforcement Parameters
- **Detection Probability:** ±15% uncertainty range
- **Penalty Effectiveness:** ±35% uncertainty range
- **Research Priority:** HIGH (strong interaction effects)

## Recommendations for Future Research

1. **Priority 1:** Empirical estimation of deterrence elasticity in AU/NZ context
2. **Priority 2:** Insurer behavior under different enforcement regimes
3. **Priority 3:** Proxy substitution accuracy and information leakage rates

## References

- Jackson C. Multi-Parameter Evidence Synthesis. 2010.
- Claxton K, et al. Probabilistic sensitivity analysis for NICE technology assessment. 2005.
- Saltelli A, et al. Global Sensitivity Analysis. 2008.

---

**Version:** 1.0  
**Last Updated:** 2026-03-05  
**Authors:** Authors' analysis
