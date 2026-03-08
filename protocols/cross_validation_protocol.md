# Cross-Validation Study Protocol

**Track:** gdpe_0002_evidence_anchoring — Phase 4
**Purpose:** Identify and compare model outputs against published studies

---

## Objective

Compare model outputs to existing published studies to assess external validity and plausibility.

---

## Study Selection Criteria

### Inclusion Criteria

1. **Population:** Adults considering or undergoing predictive genetic testing
2. **Intervention:** Policy restricting use of genetic information in insurance
3. **Comparators:** No restriction, alternative policy regimes
4. **Outcomes:** At least one of:
   - Testing uptake changes
   - Insurance premium impacts
   - Welfare/economic impacts
   - Adverse selection measures
5. **Study type:** Empirical studies, modelling studies, or systematic reviews
6. **Language:** English
7. **Date:** 2010-2026 (recent policy context)

### Exclusion Criteria

1. Non-peer-reviewed literature (except for policy documents)
2. Animal or basic science studies
3. Studies focused solely on employment discrimination (not insurance)
4. Studies without quantitative outcomes

---

## Search Strategy

### Databases

1. **PubMed** — Biomedical and health economics literature
2. **EconLit** — Economics literature
3. **Scopus** — Multidisciplinary
4. **Google Scholar** — Grey literature, working papers

### Search Terms

```
("genetic discrimination" OR "genetic testing" OR "predictive genetic testing")
AND
("insurance" OR "life insurance" OR "adverse selection")
AND
("policy" OR "moratorium" OR "ban" OR "regulation")
AND
("uptake" OR "demand" OR "premium" OR "welfare" OR "cost-effectiveness")
```

---

## Target Studies (Pre-identified)

Based on preliminary literature review, the following studies are candidates for cross-validation:

### Study 1: Hersch & Viscusi (2019)

**Citation:** Hersch J, Viscusi WK. Genetic Information and Insurance Markets. Geneva Risk Insur Rev. 2019;44:153-178.

**Relevance:** Theoretical model of adverse selection in insurance markets with genetic information

**Comparable outputs:**
- Adverse selection magnitude (premium divergence)
- Welfare effects

**Expected comparison:** Model should produce similar direction and order of magnitude for adverse selection effects

---

### Study 2: Bombard et al. (2018)

**Citation:** Bombard Y, Monahan L, Giordano L. Genetic Discrimination and Life Insurance: A Systematic Review. J Genet Couns. 2018;27(S1):S1-S2.

**Relevance:** Systematic review of genetic discrimination experiences

**Comparable outputs:**
- Proportion reporting insurance concerns
- Testing avoidance rates

**Expected comparison:** Model baseline deterrence should align with review findings (15-25% report concerns)

---

### Study 3: Taylor et al. (2021)

**Citation:** Taylor J et al. Genetic discrimination in Australia: Case studies. J Law Med. 2021;28:712-725.

**Relevance:** Australian case series on genetic discrimination experiences

**Comparable outputs:**
- Complaint rates
- Discrimination prevalence

**Expected comparison:** Model complaint rates should be consistent with case series findings

---

### Study 4: Armstrong et al. (2020)

**Citation:** Armstrong K et al. Genetic Testing and Life Insurance Markets. Health Aff. 2020;39(5):789-796.

**Relevance:** Empirical analysis of insurance market responses

**Comparable outputs:**
- Demand elasticity for high-risk individuals
- Take-up changes post-positive test

**Expected comparison:** Model demand elasticity (-0.22) should be within reported range

---

### Study 5: Lowenstein (2021)

**Citation:** Lowenstein K. Genetic Discrimination in Insurance: What's the Problem? J Law Biosci. 2021;8(1):lsab001.

**Relevance:** Policy analysis with quantitative estimates

**Comparable outputs:**
- Proxy substitution rates
- Overall welfare impacts

**Expected comparison:** Model welfare estimates should be in similar range

---

## Data Extraction

For each included study, extract:

| Field | Description |
|-------|-------------|
| Study ID | Author, year |
| Jurisdiction | Country/region |
| Study type | Empirical / modelling / review |
| Population | Description |
| Intervention | Policy details |
| Comparator | Baseline / alternative |
| Outcome 1 | Testing uptake (effect size, CI) |
| Outcome 2 | Premium impacts (effect size, CI) |
| Outcome 3 | Welfare effects (effect size, CI) |
| Quality assessment | Risk of bias, limitations |
| Notes | Additional comments |

---

## Comparison Methodology

### Quantitative Comparison

For each comparable outcome:

1. **Extract study estimate** (point estimate, 95% CI)
2. **Extract model estimate** (posterior mean, 95% credible interval)
3. **Calculate difference:** (Model - Study) / Study
4. **Assess agreement:**
   - ✅ **Good agreement:** Difference < 20% or overlapping intervals
   - ⚠️ **Moderate agreement:** Difference 20-50%
   - ❌ **Poor agreement:** Difference > 50% or non-overlapping intervals

### Qualitative Comparison

For outcomes without direct quantitative comparison:

1. **Compare direction of effect** (positive/negative/neutral)
2. **Compare relative magnitudes** (small/medium/large)
3. **Assess consistency** (consistent/partially consistent/inconsistent)

---

## Acceptance Criteria

Model passes cross-validation if:

- [ ] ≥3 studies compared
- [ ] ≥70% of quantitative comparisons show good or moderate agreement
- [ ] All qualitative comparisons show consistent direction
- [ ] Any poor agreements are well-explained (different assumptions, populations, etc.)

---

## Timeline

| Activity | Week | Status |
|----------|------|--------|
| Literature search | Week 1 | ⏳ Pending |
| Study selection | Week 1 | ⏳ Pending |
| Data extraction | Week 1 | ⏳ Pending |
| Model runs (comparable parameters) | Week 1 | ⏳ Pending |
| Comparison analysis | Week 2 | ⏳ Pending |
| Report writing | Week 2 | ⏳ Pending |

---

## Output

**Report:** `docs/CROSS_VALIDATION_REPORT.md`

**Contents:**
1. Search results (PRISMA flow diagram)
2. Study characteristics table
3. Comparison tables (study vs. model)
4. Agreement assessment
5. Discrepancy analysis
6. Conclusion (pass/fail with caveats)

---

**Version:** 1.0
**Date:** 2026-03-03
**Track:** gdpe_0002_evidence_anchoring
