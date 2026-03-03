# Evidence Quality Grading Rubric

Adapted from the GRADE framework for policy modelling contexts.

## Purpose
This rubric guides systematic evaluation of evidence quality when populating evidence registers and converting evidence to prior distributions.

---

## Evidence Quality Domains

### 1. Study Design Quality

| Grade | Design Type | Examples |
|-------|-------------|----------|
| **A** | Randomised controlled trials, systematic reviews/meta-analyses | RCTs of genetic testing interventions, meta-analyses of discrimination effects |
| **B** | Prospective cohort studies, quasi-experimental designs | Longitudinal studies of testing behaviour, natural experiments from policy changes |
| **C** | Retrospective cohort, case-control, interrupted time series | Historical claims analysis, pre-post policy comparisons |
| **D** | Cross-sectional surveys, case series | One-time surveys on perceived discrimination, case reports |
| **E** | Expert opinion, modelling studies, narrative reviews | Expert elicitation, published modelling assumptions, commentary |

---

### 2. Directness (Applicability to AU/NZ Context)

| Level | Description | Downgrade |
|-------|-------------|-----------|
| **Direct** | Evidence from AU or NZ life insurance markets, or directly comparable jurisdictions (UK, Canada) | None |
| **Indirect** | Evidence from other high-income countries with different insurance systems (US, EU) | -1 level |
| **Very indirect** | Evidence from different insurance products (health insurance) or non-insurance contexts | -2 levels |

---

### 3. Precision and Uncertainty

| Level | Criteria |
|-------|----------|
| **Precise** | Narrow confidence intervals, large sample size (>1000), low risk of type II error |
| **Moderately precise** | Moderate sample size (100-1000), confidence intervals span decision-relevant ranges |
| **Imprecise** | Small sample size (<100), wide confidence intervals, high uncertainty |

---

### 4. Consistency

| Level | Criteria |
|-------|----------|
| **Consistent** | Multiple studies show similar effect directions and magnitudes |
| **Inconsistent** | Studies show conflicting results, substantial heterogeneity (I² > 50%) |
| **Unknown** | Single study or insufficient data to assess consistency |

---

### 5. Risk of Bias

Assess using domain-specific tools:
- **RCTs:** Cochrane Risk of Bias 2
- **Observational studies:** ROBINS-I
- **Surveys:** AAPOR standards
- **Modelling studies:** ISPOR-SMDM checklist

| Level | Criteria |
|-------|----------|
| **Low risk** | All domains low risk |
| **Moderate risk** | Some concerns in 1-2 domains |
| **High risk** | Serious concerns in ≥1 domain |

---

## Overall Evidence Quality Rating

Combine domain assessments:

| Starting Grade | Downgrades | Final Grade | Interpretation |
|----------------|------------|-------------|----------------|
| A (RCT/meta-analysis) | 0 | **High** | Very confident in effect estimate |
| A | 1-2 | **Moderate** | Moderately confident; true effect likely close |
| A | 3+ | **Low** | Limited confidence; true effect may differ |
| B (cohort) | 0-1 | **Moderate** | Moderately confident |
| B | 2+ | **Low** | Limited confidence |
| C (retrospective) | 0-1 | **Low** | Limited confidence |
| C | 2+ | **Very Low** | Very uncertain |
| D-E | Any | **Very Low** | Very uncertain; use with caution |

---

## Application to Prior Distributions

### High Quality Evidence
- Use informative priors with narrow variance
- Center prior on point estimate from meta-analysis
- Example: `Normal(μ=0.15, σ=0.03)` for testing uptake elasticity

### Moderate Quality Evidence
- Use weakly informative priors
- Wider variance to reflect uncertainty
- Example: `Normal(μ=0.15, σ=0.10)`

### Low/Very Low Quality Evidence
- Use diffuse priors or expert elicitation
- Consider multiple priors in sensitivity analysis
- Example: `Normal(μ=0.15, σ=0.25)` or uniform bounds

---

## Evidence Register Entry Template

```yaml
evidence_id: "AU_behav_001"
module: "A"  # Behaviour/deterrence
parameter: "testing_uptake_elasticity"

# Study details
citation: "Author et al. (Year). Title. Journal."
doi: "10.xxxx/xxxxx"
study_design: "Prospective cohort"
jurisdiction: "Australia"
population: "Adults considering predictive genetic testing"
sample_size: 1250

# Quality assessment
initial_grade: "B"
directness: "Direct"
precision: "Precise"
consistency: "Consistent"
risk_of_bias: "Low"
final_grade: "Moderate"

# Effect estimate
point_estimate: 0.15
confidence_interval_lower: 0.09
confidence_interval_upper: 0.21

# Prior conversion
prior_distribution: "Normal"
prior_mean: 0.15
prior_sd: 0.10
rationale: "Moderate quality evidence; widened SD to reflect uncertainty"

# Notes
notes: "Key study for AU calibration. Consider EVPPI for this parameter."
```

---

## Review Process

1. **Initial grading:** Evidence grader assigns preliminary ratings
2. **Independent review:** Second reviewer assesses 20% of entries
3. **Reconciliation:** Discrepancies resolved through discussion
4. **Documentation:** All grades recorded in evidence register with rationale

---

## References

- Guyatt GH, et al. GRADE: An emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008.
- Schünemann HJ, et al. GRADE Handbook. 2013.
- ISPOR-SMDM Modeling Good Practices Task Force. Value in Health. 2012.
