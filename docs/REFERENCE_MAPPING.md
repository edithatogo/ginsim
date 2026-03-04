# Reference Mapping Report

**Track:** gdpe_0004_quality_assurance  
**Phase:** 4 — Reference Mapping  
**Date:** 2026-03-03  
**Status:** IN PROGRESS

---

## 1. Input and Assumption Inventory

### 1.1 Module A: Behavior/Deterrence

| Parameter | Base Value | Source | References | Quality |
|-----------|------------|--------|------------|---------|
| `baseline_testing_uptake` | 0.52 | Ettema et al. (2021) | 1 reference | Moderate |
| `deterrence_elasticity` | 0.18 | McGuire et al. (2019) | 1 reference | Low |
| `moratorium_effect` | 0.15 | Taylor et al. (2021) | 1 reference | Very Low |

**Gap:** Need additional references for deterrence_elasticity and moratorium_effect

### 1.2 Module C: Insurance Equilibrium

| Parameter | Base Value | Source | References | Quality |
|-----------|------------|--------|------------|---------|
| `adverse_selection_elasticity` | 0.08 | Hersch & Viscusi (2019) | 1 reference | Low |
| `demand_elasticity_high_risk` | -0.22 | Armstrong et al. (2020) | 1 reference | Low |
| `baseline_loading` | 0.15 | FSC Moratorium (2019) | 1 reference | Very Low |

**Gap:** Need additional references for all parameters

### 1.3 Module D: Proxy Substitution

| Parameter | Base Value | Source | References | Quality |
|-----------|------------|--------|------------|---------|
| `family_history_sensitivity` | 0.68 | Tabor et al. (2018) | 1 reference | Moderate |
| `proxy_substitution_rate` | 0.40 | Lowenstein (2021) | 1 reference | Very Low |

**Gap:** Need additional references for proxy_substitution_rate

### 1.4 Module E: Pass-Through

| Parameter | Base Value | Source | References | Quality |
|-----------|------------|--------|------------|---------|
| `pass_through_rate` | 0.75 | Finkelstein et al. (2019) | 1 reference | Moderate |

**Gap:** Need additional references

### 1.5 Module F: Data Quality

| Parameter | Base Value | Source | References | Quality |
|-----------|------------|--------|------------|---------|
| `research_participation_elasticity` | -0.10 | Blevins et al. (2020) | 1 reference | Low |

**Gap:** Need additional references

### 1.6 Enforcement

| Parameter | Base Value | Source | References | Quality |
|-----------|------------|--------|------------|---------|
| `enforcement_effectiveness` | 0.50 | FSC Moratorium (2019) | 1 reference | Very Low |
| `complaint_rate` | 0.02 | Taylor et al. (2021) | 1 reference | Very Low |

**Gap:** Need additional references for both parameters

---

## 2. Reference Gap Analysis

### Summary

| Module | Parameters | ≥2 refs | 1 ref | 0 refs |
|--------|-----------|---------|-------|--------|
| **Module A** | 3 | 0 | 1 | 2 |
| **Module C** | 3 | 0 | 2 | 1 |
| **Module D** | 2 | 0 | 1 | 1 |
| **Module E** | 1 | 0 | 1 | 0 |
| **Module F** | 1 | 0 | 1 | 0 |
| **Enforcement** | 2 | 0 | 0 | 2 |
| **TOTAL** | **12** | **0** | **6** | **6** |

**Coverage:** 50% (6/12) have at least 1 reference  
**Target:** 100% have ≥1 reference, ≥50% have ≥2 references  
**Current:** 0% have ≥2 references

---

## 3. Actions to Address Gaps

### High Priority (0 references)

1. **moratorium_effect** - Search for additional Australian policy evaluation studies
2. **baseline_loading** - Search for insurance loading studies
3. **proxy_substitution_rate** - Search for underwriting proxy studies
4. **enforcement_effectiveness** - Search for compliance studies
5. **complaint_rate** - Search for discrimination complaint data

### Medium Priority (1 reference, need ≥2)

1. **deterrence_elasticity** - Add Bombard et al. (2018) systematic review
2. **adverse_selection_elasticity** - Add Binmore et al. (2017)
3. **demand_elasticity_high_risk** - Add additional insurance demand studies
4. **family_history_sensitivity** - Add additional diagnostic accuracy studies
5. **pass_through_rate** - Add additional market structure studies
6. **research_participation_elasticity** - Add additional participation studies

---

## 4. Canonical CSL-JSON Bibliography

**Location:** `study/references/references.json`

**Status:** In progress

**Current count:** 27 entries in `context/references.bib`

**Action:** Convert BibTeX to CSL-JSON, remove duplicates, validate schema

---

## 5. Evidence Quality Distribution

| Quality | Count | Percentage |
|---------|-------|------------|
| **Moderate** | 3 | 25% |
| **Low** | 4 | 33% |
| **Very Low** | 5 | 42% |

**Implication:** 75% of parameters have Low or Very Low quality evidence
**Recommendation:** Sensitivity analysis critical for Low/Very Low parameters

---

## 6. Next Steps

1. **Literature search** for missing references (Priority: High)
2. **Convert BibTeX to CSL-JSON** (Priority: High)
3. **Validate CSL-JSON schema** (Priority: Medium)
4. **Document unavoidable gaps** (Priority: Medium)
5. **Plan sensitivity analysis** for parameters with weak evidence (Priority: High)

---

**Status:** Gap analysis complete. Proceeding to address gaps and create CSL-JSON.
