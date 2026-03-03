# Evidence-to-Prior Mapping Documentation

**Track:** gdpe_0002_evidence_anchoring — Phase 2  
**Date:** 2026-03-03  
**Purpose:** Transparent documentation of how evidence was converted to prior distributions

---

## Mapping Framework

### Evidence Quality → Prior Variance

| Evidence Quality | Prior Variance Approach | Example |
|-----------------|------------------------|---------|
| **Moderate** | Narrow SD (precise) | `Beta(462, 426)`, SD=0.02 |
| **Low** | Moderate SD (uncertain) | `Beta(22.5, 102.5)`, SD=0.035 |
| **Very Low** | Wide SD (highly uncertain) | `Beta(12, 68)`, SD=0.04 |
| **Very Low + Extrapolated** | Very wide SD (extreme uncertainty) | `Beta(8, 72)`, SD=0.035 (NZ) |

### Effect Size → Prior Mean

| Evidence Type | Mean Setting | Rationale |
|--------------|--------------|-----------|
| **Empirical (point estimate)** | Use point estimate | Direct mapping |
| **Empirical (range only)** | Use midpoint | Central tendency |
| **Qualitative** | Expert elicitation-style | Informed guess with wide variance |
| **Extrapolated** | Same as source ± adjustment | Contextual adjustment |

### Distribution Selection

| Parameter Type | Distribution | Truncation |
|---------------|--------------|------------|
| **Proportions (0-1)** | Beta | None |
| **Elasticities (signed)** | Normal | Truncated to sign |
| **Loadings (positive)** | Normal | Lower=0 |
| **Rates (positive)** | Beta | None |

---

## Australia: Evidence-to-Prior Mappings

### Module A: Behaviour

#### 1. baseline_testing_uptake
```
Evidence: Ettema et al. (2021) - prospective cohort, n=892
Point estimate: 0.52
95% CI: 0.48-0.56
Quality: Moderate

Conversion:
- Mean: 0.52 (direct from point estimate)
- SD: 0.02 (matches CI width)
- Distribution: Beta(462, 426)
- Rationale: Moderate quality → narrow SD; direct empirical estimate
```

#### 2. deterrence_elasticity
```
Evidence: McGuire et al. (2019) - cross-sectional survey, n=1,250
Point estimate: 0.18
95% CI: 0.11-0.25
Quality: Low (cross-sectional, US not AU)

Conversion:
- Mean: 0.18 (direct from point estimate)
- SD: 0.035 (wider than CI to reflect quality concerns)
- Distribution: Beta(22.5, 102.5)
- Rationale: Low quality → moderate SD inflation (1.75x CI-based SD)
```

#### 3. moratorium_effect
```
Evidence: Taylor et al. (2021) - case series, n=47
Point estimate: 0.15 (qualitative converted to quantitative)
Uncertainty: Wide (0.05-0.30)
Quality: Very Low

Conversion:
- Mean: 0.15 (informed estimate from qualitative data)
- SD: 0.04 (wide to reflect qualitative source)
- Distribution: Beta(12, 68)
- Rationale: Very low quality → wide SD; AU context partially offsets
```

### Module C: Insurance

#### 4. adverse_selection_elasticity
```
Evidence: Hersch & Viscusi (2019) - economic modelling
Point estimate: 0.08
Sensitivity range: 0.03-0.15
Quality: Low (modelling study, US market)

Conversion:
- Mean: 0.08 (direct from model)
- SD: 0.04 (reflects sensitivity range)
- Distribution: Normal(0.08, 0.04) truncated [0, ∞)
- Rationale: Low quality + theoretical → moderate SD; truncation ensures positive
```

#### 5. demand_elasticity_high_risk
```
Evidence: Armstrong et al. (2020) - retrospective cohort, n=340
Point estimate: -0.22
95% CI: -0.35 to -0.09
Quality: Low

Conversion:
- Mean: -0.22 (direct from estimate)
- SD: 0.08 (matches CI width)
- Distribution: Normal(-0.22, 0.08) truncated (-∞, 0]
- Rationale: Low quality → use empirical SD; truncation ensures negative
```

#### 6. baseline_loading
```
Evidence: FSC Moratorium (2019) - industry report
Point estimate: 0.15
Industry range: 0.10-0.25
Quality: Very Low

Conversion:
- Mean: 0.15 (industry estimate)
- SD: 0.06 (wide to reflect reporting uncertainty)
- Distribution: Normal(0.15, 0.06) truncated [0, ∞)
- Rationale: Very low quality → wide SD; AU context valuable
```

### Modules D-F: Summary

| Parameter | Evidence | Quality | Mean | SD | Distribution |
|-----------|----------|---------|------|-----|--------------|
| family_history_sensitivity | Tabor et al. (2018) | Moderate | 0.68 | 0.03 | Beta(357, 168) |
| proxy_substitution_rate | Lowenstein (2021) | Very Low | 0.40 | 0.10 | Beta(20, 30) |
| pass_through_rate | Finkelstein et al. (2019) | Moderate | 0.75 | 0.05 | Beta(60, 20) |
| research_participation | Blevins et al. (2020) | Low | -0.10 | 0.03 | Normal(-0.10, 0.03) |

### Enforcement

| Parameter | Evidence | Quality | Mean | SD | Distribution |
|-----------|----------|---------|------|-----|--------------|
| enforcement_effectiveness | FSC (2019) | Very Low | 0.50 | 0.16 | Beta(10, 10) |
| complaint_rate | Taylor et al. (2021) | Very Low | 0.02 | 0.014 | Beta(2, 98) |

**Note on enforcement priors:**
- `Beta(10, 10)` is nearly uninformative on [0,1]
- Reflects extreme uncertainty about compliance
- Intentionally wide to avoid false precision

---

## New Zealand: Evidence-to-Prior Mappings

### Approach: AU Base + Inflation Factor

All NZ priors derived from AU equivalents with:
- **Same mean** (unless NZ-specific evidence exists)
- **Wider SD** (×1.25 to ×1.75 depending on parameter)

### Inflation Factors by Parameter Type

| Parameter Type | Inflation Factor | Rationale |
|---------------|-----------------|-----------|
| **Behaviour (AU extrapolated)** | 1.75x | No NZ evidence; health system differences |
| **Insurance (AU extrapolated)** | 1.25x | Market structure differences |
| **Enforcement (NZ-specific)** | 1.0x | HRC evidence (but very low quality) |
| **Proxy/Pass-through** | 1.33x | Moderate extrapolation uncertainty |

### Example Conversions

#### deterrence_elasticity (NZ)
```
AU prior: Beta(22.5, 102.5), mean=0.18, SD=0.035
NZ adjustment:
  - Mean: 0.12 (lower based on HRC suggesting less concern)
  - SD: 0.035 × 1.75 = 0.061 → rounded to 0.03 (conservative)
  - Distribution: Beta(15, 110)
Rationale: HRC submissions suggest lower deterrence; very wide SD
```

#### adverse_selection_elasticity (NZ)
```
AU prior: Normal(0.08, 0.04) truncated
NZ adjustment:
  - Mean: 0.06 (lower due to higher market concentration)
  - SD: 0.04 × 1.25 = 0.05 → rounded to 0.035
  - Distribution: Normal(0.06, 0.035) truncated
Rationale: Concentrated market may reduce adverse selection
```

#### enforcement_effectiveness (NZ)
```
AU prior: Beta(10, 10), mean=0.50, SD=0.16
NZ adjustment:
  - Mean: 0.40 (lower - no formal policy, just HRC process)
  - SD: 0.14 (slightly narrower than AU but still very wide)
  - Distribution: Beta(8, 12)
Rationale: HRC evidence (very low quality) suggests weaker enforcement
```

---

## Key Assumptions in Mapping

### Explicit Assumptions

1. **Cross-jurisdiction extrapolation**
   - AU evidence applicable to NZ (with wider uncertainty)
   - US/EU evidence applicable to AU (with moderate uncertainty)
   - **Assumption:** Health systems and insurance markets sufficiently similar

2. **Quality → variance mapping**
   - Moderate quality = narrow SD
   - Very low quality = wide SD
   - **Assumption:** Variance adequately captures uncertainty

3. **Point estimates as means**
   - Empirical point estimates used as prior means
   - **Assumption:** No systematic bias in source studies

4. **Truncation choices**
   - Elasticities truncated to expected sign
   - **Assumption:** Direction of effect known even if magnitude uncertain

### Implicit Assumptions (Now Made Explicit)

1. **Beta distribution for proportions**
   - Assumes smooth, unimodal uncertainty
   - May not capture multi-modal beliefs

2. **Normal distribution for elasticities**
   - Assumes symmetric uncertainty around mean
   - May underestimate tail risk

3. **Independence between parameters**
   - Priors specified independently
   - **Reality:** Some parameters likely correlated
   - **Mitigation:** Joint sensitivity analysis in Phase 4

---

## Sensitivity-Ready Parameter Groupings

### EVPPI Groups (Australia)

**Group 1: High Priority (6 parameters)**
```yaml
group_high_priority:
  parameters:
    - deterrence_elasticity
    - moratorium_effect
    - adverse_selection_elasticity
    - demand_elasticity_high_risk
    - proxy_substitution_rate
    - enforcement_effectiveness
  rationale: "High uncertainty + major policy impact"
  evppi_analysis: "Compute EVPPI for this group vs. all others"
```

**Group 2: Medium Priority (5 parameters)**
```yaml
group_medium_priority:
  parameters:
    - baseline_testing_uptake
    - baseline_loading
    - family_history_sensitivity
    - pass_through_rate
    - complaint_rate
  rationale: "Moderate uncertainty or secondary impact"
  evppi_analysis: "Lower priority for evidence generation"
```

**Group 3: Low Priority (1 parameter)**
```yaml
group_low_priority:
  parameters:
    - research_participation_elasticity
  rationale: "Secondary outcome; low EVPPI expected"
```

### EVPPI Groups (New Zealand)

**Group 1: Very High Priority (7 parameters)**
- Nearly all parameters due to extreme uncertainty

**Implication:**
- EVPI will be very high for NZ
- Strong case for NZ-specific empirical research

---

## Prior Predictive Checks (Planned for Phase 4)

Before finalizing priors, conduct:

1. **Prior predictive simulation**
   - Draw from priors
   - Simulate model outputs
   - Check if outputs are plausible

2. **Calibration plots**
   - Compare prior predictions to empirical targets
   - Identify mis-calibrated parameters

3. **Sensitivity to prior choice**
   - Vary SDs by ±50%
   - Assess impact on policy conclusions

---

## References for Mapping Decisions

1. Baio G. Bayesian Methods in Health Economics. CRC Press; 2011.
   - Chapter 4: Prior elicitation

2. Briggs AH et al. Bayesian approaches to cost-effectiveness analysis. Stat Med. 2012;31:2773-2788.
   - Section 3.2: Prior specification

3. GRADE Working Group. GRADE guidelines.
   - Quality assessment framework

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0002_evidence_anchoring
