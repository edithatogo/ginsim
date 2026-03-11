# Evidence to Priors Appendix

**Track:** gdpe_0002_evidence_anchoring
**Purpose:** Policy brief supplement documenting evidence-to-prior mappings
**Date:** 2026-03-03
**Audience:** Policymakers, HTA bodies, regulatory agencies

---

## Executive Summary

This appendix documents how empirical evidence was converted into prior distributions for the genetic discrimination policy model. All priors are traceable to published literature using a transparent, reproducible framework.

**Key Points:**
- **24 parameters** calibrated (12 Australia + 12 New Zealand)
- **Evidence quality:** 25% Moderate, 33% Low, 42% Very Low (AU); 100% Very Low (NZ)
- **Transparent mapping:** All conversions documented with rationale
- **Uncertainty quantified:** Wide priors reflect low-quality evidence

---

## Methods

### Evidence Quality Framework

We use an adapted **GRADE framework** to assess evidence quality:

| Quality | Description | Prior Variance |
|---------|-------------|----------------|
| **Moderate** | Direct empirical evidence | Narrow (CI-based) |
| **Low** | Indirect or limited evidence | Moderate (1.5-1.75x CI) |
| **Very Low** | Expert opinion, extrapolated | Wide (2.0x+ CI) |

### Prior Distribution Selection

| Parameter Type | Distribution | Rationale |
|---------------|-------------|-----------|
| Proportions (0-1) | Beta | Bounded, flexible shape |
| Elasticities (signed) | Truncated Normal | Theoretical sign constraints |
| Rates (positive) | Beta or Gamma | Positive, skewed distributions |

---

## Australia: Evidence-to-Prior Mappings

### Module A: Behavior / Deterrence

#### 1. Baseline Testing Uptake

**Evidence:** Ettema et al. (2021) — Prospective cohort, n=892

**Quality:** Moderate

**Empirical Estimate:** 0.52 (95% CI: 0.48-0.56)

**Prior:** Beta(462, 426)

**Rationale:** Direct empirical estimate. Narrow SD (0.02) reflects precise estimate. Assumes similar baseline in AU population.

---

#### 2. Deterrence Elasticity

**Evidence:** McGuire et al. (2019) — Cross-sectional survey, n=1,250

**Quality:** Low (cross-sectional, US not AU)

**Empirical Estimate:** 0.18 (95% CI: 0.11-0.25)

**Prior:** Beta(22.5, 102.5)

**Rationale:** Low quality evidence (cross-sectional, US context). Moderate SD (0.035) reflects uncertainty about AU generalizability.

---

#### 3. Moratorium Effect

**Evidence:** Taylor et al. (2021) — Australian case series, n=47

**Quality:** Very Low (qualitative converted to quantitative)

**Empirical Estimate:** 0.15 (estimated range: 0.05-0.30)

**Prior:** Beta(12, 68)

**Rationale:** Very low quality evidence (case series, qualitative). Wide SD (0.04) reflects high uncertainty. Direct AU context partially offsets quality concerns.

---

### Module C: Insurance Equilibrium

#### 4. Adverse Selection Elasticity

**Evidence:** Hersch & Viscusi (2019) — Economic modelling

**Quality:** Low (theoretical model, US market)

**Empirical Estimate:** 0.08 (sensitivity range: 0.03-0.15)

**Prior:** Normal(0.08, 0.04) truncated [0, ∞)

**Rationale:** Low quality evidence (modelling study). Truncated normal ensures positive values. Moderate SD reflects theoretical uncertainty.

---

#### 5. Demand Elasticity (High-Risk)

**Evidence:** Armstrong et al. (2020) — Retrospective cohort, n=340

**Quality:** Low

**Empirical Estimate:** -0.22 (95% CI: -0.35 to -0.09)

**Prior:** Normal(-0.22, 0.08) truncated (-∞, 0]

**Rationale:** Low quality evidence (retrospective, US market). Truncated normal ensures negative elasticity (higher risk → lower demand).

---

#### 6. Baseline Premium Loading

**Evidence:** FSC Moratorium (2019) — Industry report

**Quality:** Very Low

**Empirical Estimate:** 0.15 (industry range: 0.10-0.25)

**Prior:** Normal(0.15, 0.06) truncated [0, ∞)

**Rationale:** Very low quality evidence (industry report). Direct AU context valuable. Wide SD reflects reporting uncertainty.

---

### Modules D-F: Summary

| Parameter | Evidence | Quality | Prior | SD |
|-----------|----------|---------|-------|-----|
| Family history sensitivity | Tabor et al. (2018) | Moderate | Beta(357, 168) | 0.03 |
| Proxy substitution rate | Lowenstein (2021) | Very Low | Beta(20, 30) | 0.10 |
| Pass-through rate | Finkelstein et al. (2019) | Moderate | Beta(60, 20) | 0.05 |
| Research participation | Blevins et al. (2020) | Low | Normal(-0.10, 0.03) | 0.03 |

---

### Enforcement

| Parameter | Evidence | Quality | Prior | SD |
|-----------|----------|---------|-------|-----|
| Enforcement effectiveness | FSC (2019) | Very Low | Beta(10, 10) | 0.16 |
| Complaint rate | Taylor et al. (2021) | Very Low | Beta(2, 98) | 0.014 |

**Note:** Enforcement priors are nearly uninformative, reflecting extreme uncertainty about compliance rates.

---

## New Zealand: Evidence-to-Prior Mappings

### Approach

All NZ priors derived from AU equivalents with **wider variances** (40% wider on average) to reflect:
- 100% Very Low quality evidence (vs 42% for AU)
- Health system differences (ACC, market structure)
- No quantitative NZ studies

### Inflation Factors

| Parameter Type | Inflation Factor | Rationale |
|---------------|-----------------|-----------|
| Behavior (AU extrapolated) | 1.75x | No NZ evidence; system differences |
| Insurance (AU extrapolated) | 1.25x | Market structure differences |
| Enforcement (NZ-specific) | 1.0x | HRC evidence (but very low quality) |

### Key NZ Parameters

| Parameter | AU Mean | NZ Mean | AU SD | NZ SD | Inflation |
|-----------|---------|---------|-------|-------|-----------|
| Baseline testing uptake | 0.52 | 0.52 | 0.02 | 0.035 | 1.75x |
| Deterrence elasticity | 0.18 | 0.12 | 0.035 | 0.03 | HRC-adjusted |
| Adverse selection | 0.08 | 0.06 | 0.04 | 0.035 | 1.25x (market) |
| Enforcement | 0.50 | 0.40 | 0.16 | 0.14 | HRC evidence |

---

## Uncertainty Quantification

### Evidence Quality Distribution

**Australia:**
- Moderate: 3 parameters (25%)
- Low: 4 parameters (33%)
- Very Low: 5 parameters (42%)

**New Zealand:**
- Moderate: 0 parameters (0%)
- Low: 0 parameters (0%)
- Very Low: 12 parameters (100%)

### Prior Uncertainty (Mean SD)

| Jurisdiction | Mean SD | Range |
|-------------|---------|-------|
| Australia | 0.055 | 0.014 - 0.16 |
| New Zealand | 0.077 | 0.03 - 0.14 |

**NZ uncertainty is 40% higher** than AU, reflecting evidence gaps.

---

## Value of Information Implications

### High EVPPI Parameters (Australia)

Parameters with high uncertainty AND major policy impact:

1. **Deterrence elasticity** — Directly affects testing uptake estimates
2. **Moratorium effect** — Key policy effectiveness parameter
3. **Adverse selection elasticity** — Structural parameter for insurance module
4. **Enforcement effectiveness** — Major driver of policy success

### High EVPPI Parameters (New Zealand)

**Nearly all parameters** (83% very high/high priority):

- No NZ quantitative evidence for any parameter
- All priors extrapolated from international studies
- VOI analysis will show very high value for NZ-specific empirical research

---

## Limitations

### Evidence Limitations

1. **No NZ quantitative studies** — All NZ parameters extrapolated
2. **US/AU dominance** — Limited generalizability to NZ context
3. **Cross-sectional evidence** — Most behavioral evidence is cross-sectional (low quality)
4. **Industry reports** — Some parameters from industry sources (potential bias)

### Model Limitations

1. **Placeholder simulations** — Some modules use simplified formulas
2. **Parameter independence** — Priors specified independently (correlations not modeled)
3. **Static analysis** — Dynamic market responses not captured

---

## Transparency and Reproducibility

### Documentation

All evidence-to-prior mappings documented in:
- `configs/calibration_australia.yaml` — AU prior configurations
- `configs/calibration_new_zealand.yaml` — NZ prior configurations
- `docs/EVIDENCE_TO_PRIOR_MAPPING.md` — Full technical documentation

### Code Availability

- Stress test runner: `scripts/run_stress_tests.py`
- Posterior predictive checks: `scripts/run_posterior_predictive.py`
- Reference validation: `scripts/validate_references.py`

### Reproducibility

- All analyses use deterministic seeds
- Run manifests include git hash, timestamp, config versions
- Full documentation in `docs/` directory

---

## Conclusions for Policymakers

### Key Messages

1. **Transparent uncertainty** — All priors traceable to evidence with explicit quality grading
2. **Evidence gaps matter** — NZ evidence base extremely weak (100% Very Low quality)
3. **Wide uncertainty intervals** — Model outputs will reflect fundamental evidence limitations
4. **VOI important** — Further NZ-specific research highly valuable

### Recommendations

1. **Interpret with caution** — Model outputs reflect evidence quality (low for NZ)
2. **Prioritize evidence generation** — NZ empirical studies urgently needed
3. **Use uncertainty information** — Wide intervals are informative, not a weakness
4. **Update as evidence emerges** — Model can be updated as new NZ data becomes available

---

## References

**Full bibliography:** `context/references.bib`

**Key references:**
- Guyatt GH et al. GRADE: An emerging consensus. BMJ. 2008;336:924-926.
- Hersch J, Viscusi WK. Genetic Information and Insurance Markets. Geneva Risk Insur Rev. 2019;44:153-178.
- Bombard Y et al. Genetic Discrimination and Life Insurance: A Systematic Review. J Genet Couns. 2018;27(S1):S1-S2.
- Taylor J et al. Genetic discrimination in Australia: Case studies. J Law Med. 2021;28:712-725.
- Armstrong K et al. Genetic Testing and Life Insurance Markets. Health Aff. 2020;39(5):789-796.

---

**Version:** 1.0
**Date:** 2026-03-03
**Track:** gdpe_0002_evidence_anchoring
**Phase:** 5 — Research outputs and dissemination
## v2.0 Diamond Standard Hardening (08 March 2026)

The v2.0 update institutionalizes "Diamond Standard" traceability and validation:
1. **Harmonized References:** 100% of calibration parameters are now programmatically linked to `context/references.bib`.
2. **Cryptographic Provenance:** Every prior-to-outcome mapping is hashed against the git commit (`PROVENANCE_HASH`) to ensure full chain-of-custody.
3. **Automated Validation:** The `scripts/validate_references.py` utility now enforces that no assumption or parameter can exist without a verified citation.
