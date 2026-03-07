# Methods Section Draft: Genetic Discrimination Policy Economic Evaluation

**Track:** gdpe_0020_dashboard_policy_alignment_and_publication_sync  
**Purpose:** Draft methods section for journal submission  
**Target Journal:** Nature Human Behaviour / Value in Health / Medical Decision Making  
**Date:** 2026-03-07

---

## Methods

### Overview

We developed a modular Bayesian decision analysis model to quantify the economic and welfare impacts of policies restricting genetic discrimination in life insurance. The model integrates evidence from multiple sources (behavioral, clinical, insurance markets, and research-participation externalities) and propagates uncertainty through all modules to generate probabilistic policy recommendations.

### Model Structure

The model comprises six interconnected modules representing the policy causal pathway:

1. **Module A (Behavior/Deterrence):** Models how policy regimes affect perceived discrimination risk and subsequently genetic testing uptake
2. **Module B (Clinical Outcomes):** Estimates health outcomes (QALYs, costs) from changes in testing behavior
3. **Module C (Insurance Equilibrium):** Models adverse selection, premium setting, and market responses
4. **Module D (Proxy Substitution):** Estimates underwriting accuracy when genetic information is restricted
5. **Module E (Pass-Through/Market Structure):** Models incidence of costs across market participants
6. **Module F (Data Quality Externality):** Estimates impacts on research participation and data quality

Modules are linked sequentially: policy rules → behavioral response → insurance equilibrium → clinical outcomes and data-quality effects → welfare impacts.

**[Figure 1: Model structure diagram would be inserted here]**

### Bayesian Framework

We use full probabilistic Bayesian decision analysis to quantify uncertainty in all model parameters. Prior distributions were elicited from systematic evidence reviews using an adapted GRADE framework for quality assessment.

**Prior specification:**
- Proportions (bounded [0,1]): Beta distributions
- Elasticities (signed): Truncated Normal distributions (constrained to theoretical sign)
- Rates (positive): Beta or Gamma distributions

**Uncertainty propagation:**
- Markov Chain Monte Carlo (MCMC) sampling using NumPyro/BlackJAX
- 2,000 posterior draws per policy scenario
- Common random numbers for policy contrasts (variance reduction)

**Posterior estimation:**
- NUTS (No-U-Turn Sampler) with 4 chains
- 1,000 warmup iterations, 2,000 sampling iterations
- Convergence assessed via R-hat statistic (<1.1 threshold)

### Evidence Base

#### Search Strategy

We conducted systematic evidence reviews for each module covering:
- PubMed (biomedical literature)
- EconLit (economics literature)
- Scopus (multidisciplinary)
- Google Scholar (grey literature)

Search terms: `("genetic discrimination" OR "genetic testing") AND ("insurance" OR "adverse selection") AND ("policy" OR "moratorium" OR "ban")`

**Inclusion criteria:**
- Population: Adults considering/undergoing predictive genetic testing
- Intervention: Policy restricting genetic information use in insurance
- Outcomes: Testing uptake, premiums, welfare, adverse selection measures
- Study type: Empirical, modelling, or systematic reviews
- Language: English
- Date: 2010-2026

#### Evidence Quality Assessment

Evidence quality was assessed using an adapted GRADE framework:

| Quality | Description | Prior Variance Inflation |
|---------|-------------|-------------------------|
| **Moderate** | Direct empirical evidence (RCTs, prospective cohorts) | 1.0x (CI-based) |
| **Low** | Indirect or limited evidence (cross-sectional, retrospective) | 1.5-1.75x |
| **Very Low** | Expert opinion, extrapolated, case series | 2.0x+ |

#### Evidence Synthesis

For each parameter:
1. Extract point estimate and uncertainty (95% CI or SD)
2. Assess evidence quality using GRADE
3. Convert to prior distribution (mean = point estimate, SD = CI-based × inflation factor)
4. Document rationale and source

**Example:** Deterrence elasticity
- Source: McGuire et al. (2019) — cross-sectional survey, n=1,250
- Estimate: 0.18 (95% CI: 0.11-0.25)
- Quality: Low (cross-sectional, US not AU context)
- Prior: Beta(22.5, 102.5), SD = 0.035 (1.75x CI-based SD)

### Policy Scenarios

We evaluated three canonical benchmark policy regimes:

1. **Status Quo (Baseline):** No restrictions on genetic information use
2. **Moratorium:** Industry self-regulation with financial caps ($500k life, $200k TPD/trauma in the benchmark Australian implementation)
3. **Ban:** Legislative prohibition with statutory penalties

Policy parameters encoded as:
- **Allow genetic test results:** {true, false}
- **Enforcement strength:** {baseline, industry, statutory}
- **Sum insured caps:** {null, $500k/$200k}

### Outcomes

**Primary outcomes:**
1. Change in genetic testing uptake (absolute and relative)
2. Change in insurance premiums and take-up
3. Net QALYs gained/lost
4. Net fiscal impact (health system costs)
5. Net welfare impact (distributional cost-benefit analysis, with short- and long-horizon views)

**Secondary outcomes:**
1. Adverse selection magnitude (premium divergence)
2. Proxy substitution effects (underwriting accuracy)
3. Research participation impacts
4. Enforcement effectiveness

In the current active implementation, proxy-substitution outputs and data-quality externalities are integrated into the reported welfare surface rather than treated only as disconnected auxiliary diagnostics.

**Uncertainty quantification:**
- 95% credible intervals for all outcomes
- Cost-effectiveness acceptability curves
- Expected Value of Perfect Information (EVPI)
- Expected Value of Partial Perfect Information (EVPPI) by parameter group

### Value of Information Analysis

**EVPI calculation:**
```
EVPI = E[max NB(d, θ)] - max E[NB(d, θ)]
```

Where NB = net benefit, d = decision, θ = uncertain parameters

**EVPPI calculation:**
- Monte Carlo estimation using Gaussian process regression
- Parameter groups: behavioral, insurance, clinical, enforcement
- 2,000 outer draws, 50 inner draws

**Interpretation:**
- EVPI: Maximum value of eliminating all uncertainty
- EVPPI: Value of eliminating uncertainty in specific parameter groups
- Guides research prioritization

### Model Validation

**Face validity:**
- Expert review of model structure and assumptions (≥2 independent reviewers)
- Structured questionnaire covering: model structure, assumptions, parameters, policy relevance

**Cross-validation:**
- Comparison against ≥3 published studies
- Outcomes: testing uptake, premium impacts, welfare effects
- Acceptance criteria: ≥70% good/moderate agreement

**Stress testing:**
- 8 extreme scenarios (100% uptake, 0% adverse selection, 100% enforcement, etc.)
- Validation: logical consistency, bounds respected, monotonicity

**Posterior predictive checks:**
- 2,000 prior draws
- Comparison to empirical targets
- Acceptance criteria: coverage >50%, bias <20%

### Software and Reproducibility

**Implementation:**
- Python 3.10+
- JAX/XLA for accelerated simulation
- NumPyro for probabilistic programming
- BlackJAX for MCMC sampling

**Code availability:**
- Repository and archival identifiers should be inserted only once finalized.
- Public reporting artifacts should use canonical run identifiers and manifest excerpts without exposing local filesystem paths.
- License: MIT (code), CC-BY 4.0 (documentation)

**Reproducibility:**
- Deterministic seeds (20260303)
- Run manifests include: git hash, timestamp, config versions
- All analyses can be reproduced via: `python -m scripts.run_meta_pipeline --n_draws 2000`

### Patient and Public Involvement

No patients or public were directly involved in this modelling study. Evidence sources include published studies of patient experiences and preferences.

### Ethics Approval

Ethics approval was not required for this modelling study using published aggregate data.

---

## Reporting Guidelines

This study follows:
- **CHEERS 2022** reporting guidelines for economic evaluations
- **ISPOR-SMDM** modelling good practices
- **PRISMA** guidelines for systematic evidence reviews

---

## Statistical Appendix

### Prior Distributions (Full Table)

**[Table A1: All prior distributions with parameters would be inserted here]**

### Calibration Targets

**[Table A2: Empirical calibration targets with sources would be inserted here]**

### Sensitivity Analysis

**[Table A3: One-way sensitivity analysis results would be inserted here]**

---

**Word count:** ~1,200 (excluding tables and appendix)

**Target journal requirements:**
- Value in Health: Methods section ~1,000-1,500 words ✅
- Medical Decision Making: Methods section ~1,500-2,000 words ✅ (with appendix)

---

**Version:** 1.1 draft  
**Date:** 2026-03-07  
**Track:** gdpe_0020_dashboard_policy_alignment_and_publication_sync  
**Phase:** publication-facing synchronization
