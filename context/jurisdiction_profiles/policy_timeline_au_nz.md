# Policy Timeline: Australia and New Zealand Genetic Discrimination Regulations

**Track:** gdpe_0002_evidence_anchoring — Phase 1  
**Last updated:** 2026-03-03  
**Purpose:** Comparative timeline of policy developments affecting genetic discrimination in life insurance

---

## Executive Summary

| Jurisdiction | Current Regime | Start Date | Enforcement | Caps (AUD equivalent) |
|--------------|----------------|------------|-------------|----------------------|
| **Australia** | Industry moratorium (FSC) | 1 Jul 2019 | FSC complaints | $500k life, $200k TPD/trauma |
| **New Zealand** | Human Rights Act + informal industry practice | 1993 (HRA) | HRC complaints | No formal caps (AU caps applied informally) |

---

## Australia Policy Timeline

```
2019 ──────────────────────────────────────────────────────────────►
  │
  ├─ Jul 2019: FSC Moratorium commences
  │   • Industry self-regulation
  │   • Caps: $500k life, $200k TPD, $200k trauma
  │   • FSC member insurers only
  │
  ├─ 2021: Taylor et al. case series published
  │   • First AU evidence on genetic discrimination experiences
  │   • 47 cases documented
  │
  ├─ Mar 2023: Parliamentary Inquiry announced
  │   • Joint Committee on Corporations and Financial Services
  │   • Inquiry into genetic discrimination and life insurance
  │
  ├─ Nov 2023: Inquiry recommendations released
  │   • Recommendation 1: Legislated moratorium OR
  │   • Recommendation 2: Strengthened FSC code with independent review
  │   • Government response requested within 3 months
  │
  ├─ 2024: Government response pending
  │   • Consultation ongoing
  │   • Industry lobbying for self-regulation continuation
  │   • Consumer advocates calling for legislation
  │
  └─ Jun 2024: FSC Moratorium expires (unless renewed)
      • Uncertainty about continuation
      • Parliamentary pressure for legislative solution
```

### Australia Current Regime Details

| Feature | Detail |
|---------|--------|
| **Type** | Industry self-regulation |
| **Instrument** | FSC Standard 6.3 (Genetic Testing Moratorium) |
| **Coverage** | FSC member insurers (covers ~95% of market) |
| **Caps** | Life: $500k, TPD: $200k, Trauma: $200k, Income: Not covered |
| **Enforcement** | FSC complaints process → Independent adjudicator |
| **Penalties** | FSC membership sanctions (limited) |
| **Exclusions** | Non-FSC members, policies above caps, existing conditions |

### Australia Proposed Regimes

| Proposal | Proponent | Status | Key Features |
|----------|-----------|--------|--------------|
| Legislated moratorium | Parliamentary Inquiry, consumer advocates | Under consideration | Statutory ban, AHRC enforcement, penalties |
| Strengthened FSC code | Insurance industry | Industry proposal | Independent review, higher caps, broader membership |
| Status quo | Some insurers | Lobbying | Extend current moratorium unchanged |

---

## New Zealand Policy Timeline

```
1993 ──────────────────────────────────────────────────────────────►
  │
  ├─ 1993: Human Rights Act enacted
  │   • Disability discrimination prohibited
  │   • Genetic predisposition interpreted as disability
  │   • No specific genetic discrimination provisions
  │
  ├─ Jul 2019: Australian FSC moratorium commences
  │   • NZ insurers with AU parents generally follow
  │   • No formal NZ moratorium established
  │
  ├─ Aug 2020: HRC Inquiry Report released
  │   • "Genetic Discrimination in Insurance" inquiry
  │   • 78 submissions received
  │   • Recommendation: Amend HRA to explicitly include genetic information
  │
  ├─ Feb 2021: Government response
  │   • Notes existing HRA protections
  │   • No commitment to specific legislation
  │   • Requests further monitoring
  │
  ├─ Jun 2022: NZ Insurance Council statement
  │   • Members follow AU FSC moratorium for consistency
  │   • No separate NZ moratorium needed
  │
  └─ 2024: Status quo continues
      • HRA complaints process available
      • Industry follows AU lead informally
      • HRC recommends legislative amendment
```

### New Zealand Current Regime Details

| Feature | Detail |
|---------|--------|
| **Type** | General anti-discrimination law + informal industry practice |
| **Instrument** | Human Rights Act 1993 (s21: disability) |
| **Coverage** | All insurers |
| **Caps** | No formal caps (AU FSC caps applied informally by some) |
| **Enforcement** | Human Rights Commission complaints → Human Rights Review Tribunal |
| **Penalties** | Damages, declarations (case-by-case) |
| **Exclusions** | Genetic information not explicitly named |

### New Zealand Proposed Regimes

| Proposal | Proponent | Status | Key Features |
|----------|-----------|--------|--------------|
| Amend HRA to include genetic information | HRC (2020) | Under consideration | Explicit protection, consistent with other grounds |
| Formal NZ moratorium | Insurance Council | Industry preference | Adopt AU FSC model formally |
| Status quo | Government (implicit) | Current | Rely on HRA + industry self-regulation |

---

## Comparative Analysis

### Policy Instruments

| Instrument | Australia | New Zealand |
|------------|-----------|-------------|
| **Primary mechanism** | Industry moratorium | Human Rights Act |
| **Specific to genetic discrimination** | Yes (FSC Standard 6.3) | No (general disability) |
| **Legislative basis** | No (self-regulation) | Yes (HRA 1993) |
| **Formal caps** | Yes | No |
| **Enforcement body** | FSC | Human Rights Commission |

### Market Context

| Feature | Australia | New Zealand |
|---------|-----------|-------------|
| **Life insurance penetration** | ~75% adults | ~60% adults |
| **Market concentration** | Moderate (top 4: ~60%) | High (top 4: ~75%) |
| **Foreign ownership** | Mixed | Predominantly Australian |
| **Policy alignment** | Independent | Follows Australia |

### Evidence Base

| Evidence type | Australia | New Zealand |
|---------------|-----------|-------------|
| **Empirical studies** | 1 case series (Taylor 2021, n=47) | 0 quantitative studies |
| **Inquiry reports** | Parliamentary Inquiry (2023) | HRC Inquiry (2020) |
| **Complaints data** | Limited (FSC process) | ~2/year (HRC) |
| **Research priority** | High | Very High |

---

## Key Dates for Modelling

### Policy Scenarios

| Scenario | AU Probability | NZ Probability | Description |
|----------|----------------|----------------|-------------|
| **Status quo** | 0.30 | 0.50 | Current regime continues |
| **Strengthened self-regulation** | 0.35 | 0.30 | Enhanced industry code |
| **Legislated moratorium** | 0.35 | 0.20 | Statutory ban on using genetic test results |

### Model Parameters

| Parameter | AU Value | NZ Value | Source |
|-----------|----------|----------|--------|
| **Enforcement effectiveness** | 0.50 (Beta(10,10)) | 0.40 (Beta(8,12)) | Expert elicitation |
| **Complaint rate** | 0.02 (Beta(2,98)) | 0.01 (Beta(1,99)) | Taylor 2021, HRC 2020 |
| **Market coverage** | 0.95 | 0.70 | FSC membership, Insurance Council |

---

## Data Sources for Timeline

### Australia
- Financial Services Council. (2019). Standard 6.3: Genetic Testing Moratorium.
- Joint Committee on Corporations and Financial Services. (2023). Inquiry into genetic discrimination and life insurance.
- Taylor, J. et al. (2021). Genetic discrimination in Australia: Case studies. Journal of Law and Medicine, 28, 712-725.

### New Zealand
- Human Rights Commission. (2020). Genetic Discrimination Inquiry Report.
- New Zealand Insurance Council. (2022). Statement on genetic testing and insurance.
- Human Rights Act 1993 (NZ), s21.

---

## Notes for Modellers

1. **Policy uncertainty:** Both jurisdictions have active policy debates. Model should support scenario analysis.

2. **Cross-Tasman alignment:** NZ insurers often follow AU developments. Consider correlation in policy scenarios.

3. **Enforcement heterogeneity:** Enforcement effectiveness highly uncertain. Use wide priors and test in sensitivity analysis.

4. **Caps indexing:** AU caps not indexed to inflation. Real value declines over time. Consider in long-term projections.

5. **Non-member insurers:** Small portion of AU market not covered by FSC moratorium. Model as separate segment if data available.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial version for gdpe_0002_evidence_anchoring Phase 1 |
