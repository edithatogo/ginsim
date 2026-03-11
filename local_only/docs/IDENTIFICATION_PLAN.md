# Identification Plan

**Track:** gdpe_0002_evidence_anchoring — Phase 3
**Date:** 2026-03-03
**Version:** 1.0

---

## Overview

This document outlines the identification strategy for estimating model parameters and validating model outputs for the genetic discrimination policy evaluation project.

---

## Identification Strategy by Module

### Module A: Behaviour / Deterrence

#### Parameters to Identify
- `baseline_testing_uptake` — Baseline rate of genetic testing
- `deterrence_elasticity` — Effect of insurance concerns on testing
- `moratorium_effect` — Effect of moratorium on reducing deterrence

#### Identification Approaches

**1. Event Study (Preferred)**
```
Design: Interrupted time series around policy changes
Data: Genetic testing volumes (monthly/quarterly)
Treatment: FSC moratorium (July 2019)
Control: Conditions not affected by moratorium
Identification: Pre-post comparison with controls
```

**Requirements:**
- Testing volume time series (2015-present)
- Breakdown by condition (hereditary cancer, cardiac, etc.)
- Insurance-relevant vs non-insurance-relevant conditions

**2. Survey Linkage (Alternative)**
```
Design: Cross-sectional survey with discrete choice experiment
Data: Stated preferences re: testing under different insurance regimes
Identification: Structural model of testing choice
```

**Requirements:**
- Survey data on testing intentions
- Insurance concern measures
- Demographic controls

**3. Calibration to Evidence (Current Approach)**
```
Design: Use evidence register priors
Data: Published studies (see evidence registers)
Identification: Bayesian updating with informative priors
```

**Status:** Using Approach 3 (calibration) for Phase 1-4. Approach 1 recommended for future empirical work.

---

### Module C: Insurance Equilibrium

#### Parameters to Identify
- `adverse_selection_elasticity` — Premium response to information asymmetry
- `demand_elasticity_high_risk` — Demand response for high-risk individuals
- `baseline_loading` — Premium loading for genetic conditions

#### Identification Approaches

**1. Structural Estimation (Preferred)**
```
Design: Estimate demand and supply equations simultaneously
Data: Insurance application/approval/claims data
Identification: Exogenous variation in genetic risk information
Instruments: Policy regime changes, genetic testing guidelines
```

**Requirements:**
- Individual-level insurance data (applications, outcomes, premiums)
- Genetic test status (restricted due to privacy)
- Policy variation (pre/post moratorium)

**2. Reduced Form (Alternative)**
```
Design: Compare outcomes before/after moratorium
Data: Aggregate insurance statistics
Identification: Policy shock as exogenous variation
```

**Requirements:**
- Aggregate premium data by risk category
- Take-up rates by condition
- Moratorium implementation date

**3. Calibration to Evidence (Current Approach)**
```
Design: Use evidence register priors
Data: Published studies (see evidence registers)
Identification: Bayesian updating with informative priors
```

**Status:** Using Approach 3 (calibration). Approach 1 not feasible without restricted data access.

---

### Module D: Proxy Substitution

#### Parameters to Identify
- `family_history_sensitivity` — Accuracy of family history as proxy
- `proxy_substitution_rate` — Proportion of genetic risk captured by proxies

#### Identification Approaches

**1. Diagnostic Accuracy Study**
```
Design: Compare family history vs genetic test results
Data: Clinical records with both measures
Identification: Direct estimation of sensitivity/specificity
```

**Requirements:**
- Linked family history and genetic test data
- Gold standard (genetic test) availability

**2. Underwriting Model Comparison**
```
Design: Compare underwriting accuracy with/without genetic info
Data: Insurer underwriting records
Identification: Counterfactual prediction
```

**Requirements:**
- Historical underwriting data
- Access to insurer models (unlikely)

**3. Calibration to Evidence (Current Approach)**
```
Design: Use evidence register priors
Data: Published diagnostic accuracy studies
Identification: Bayesian updating
```

**Status:** Using Approach 3. Approach 1 possible via clinical collaboration.

---

### Module E: Pass-Through / Market Structure

#### Parameters to Identify
- `pass_through_rate` — Proportion of costs passed to consumers

#### Identification Approaches

**1. Empirical Pass-Through Estimation**
```
Design: Exploit cost shocks to insurers
Data: Premium and cost data over time
Identification: Cost variation as instrument
```

**Requirements:**
- Insurer cost data
- Premium data by product
- Exogenous cost shocks

**2. Calibration to Evidence (Current Approach)**
```
Design: Use evidence register priors
Data: Published pass-through studies
Identification: Bayesian updating
```

**Status:** Using Approach 3. Approach 1 requires insurer cooperation.

---

### Module F: Data Quality Externality

#### Parameters to Identify
- `research_participation_elasticity` — Effect of privacy concerns on research participation

#### Identification Approaches

**1. Survey-Based Estimation**
```
Design: Survey on research participation intentions
Data: Stated willingness to participate under different privacy regimes
Identification: Structural model
```

**Requirements:**
- Survey data
- Variation in privacy concerns

**2. Calibration to Evidence (Current Approach)**
```
Design: Use evidence register priors
Data: Published studies on research participation
Identification: Bayesian updating
```

**Status:** Using Approach 3.

---

### Enforcement and Compliance

#### Parameters to Identify
- `enforcement_effectiveness` — Compliance rate with policy regime
- `complaint_rate` — Rate of discrimination complaints

#### Identification Approaches

**1. Administrative Data Analysis**
```
Design: Analyze complaints data
Data: HRC/FSC complaints records
Identification: Direct estimation from administrative data
```

**Requirements:**
- Complaints data from HRC/FSC
- Denominator (total genetic tests)
- Time series (pre/post policy)

**2. Calibration to Evidence (Current Approach)**
```
Design: Use evidence register priors
Data: HRC Inquiry report, FSC data
Identification: Bayesian updating
```

**Status:** Using Approach 3. Approach 1 possible via data sharing agreement.

---

## Data Sources Inventory

### Australia

| Dataset | Custodian | Type | Coverage | Access | Status |
|---------|-----------|------|----------|--------|--------|
| MBS genetic testing data | Dept Health | Administrative | 2015-present | Application | Not yet accessed |
| APRA insurance statistics | APRA | Aggregate | 2010-present | Public | Available |
| Australian Cancer Database | AIHW | Registry | 1982-present | Ethics approval | Not yet accessed |
| FSC complaints data | FSC | Administrative | 2019-present | Industry | Not yet accessed |
| 45 and Up Study | Sax Institute | Survey | 2006-present | Application | Potential linkage |

### New Zealand

| Dataset | Custodian | Type | Coverage | Access | Status |
|---------|-----------|------|----------|--------|--------|
| National Genetic Testing Database | Lablink/NHB | Administrative | 2010-present | Application | Not yet accessed |
| NZ Cancer Registry | MoH | Registry | 1994-present | HQSC approval | Not yet accessed |
| NZ Health Survey | MoH | Survey | Annual | Stats NZ DataLab | Potential |
| HRC complaints data | HRC | Administrative | 2010-present | Application | Not yet accessed |
| IRD insurance data | IRD | Administrative | 2015-present | Restricted | Unlikely access |

---

## Data Linkage Opportunities

### Australia

**Feasible Linkages:**
1. MBS + Cancer Registry (via state linkages)
   - Purpose: Validate testing volumes by condition
   - Requirements: State ethics approval
   - Timeline: 3-6 months

2. 45 and Up Study + survey module
   - Purpose: Testing intentions and insurance concerns
   - Requirements: Survey module funding
   - Timeline: 6-12 months

**Challenging Linkages:**
1. Insurance claims + genetic testing
   - Purpose: Direct adverse selection estimation
   - Barriers: Privacy, insurer cooperation
   - Timeline: 12+ months (if feasible)

### New Zealand

**Feasible Linkages:**
1. Genetic Testing Database + Cancer Registry
   - Purpose: Validate testing volumes, outcomes
   - Requirements: Ethics + NHB approval
   - Timeline: 3-6 months

2. IDM linkage (Integrated Data Infrastructure)
   - Purpose: Health outcomes + insurance proxies
   - Requirements: Stats NZ approval
   - Timeline: 2-4 months

**Challenging Linkages:**
1. Insurance data + health data
   - Barriers: No routine collection, privacy concerns
   - Timeline: Not feasible in current project

---

## Event Study Design

### Primary Specification

**Treatment:** FSC Moratorium (July 1, 2019)

**Outcome:** Genetic testing rate (per 100,000 population)

**Design:**
```
Y_it = α + β·Post_t + γ·Treatment_i + δ·(Post_t × Treatment_i) + ε_it

Where:
- Y_it = testing rate for condition i at time t
- Post_t = 1 if t ≥ July 2019
- Treatment_i = 1 if condition affected by moratorium
- δ = moratorium effect (parameter of interest)
```

**Data Requirements:**
- Monthly/quarterly testing volumes
- Multiple conditions (treatment and control)
- Sufficient pre/post periods (≥2 years each)

**Identification Assumptions:**
- Parallel trends (treatment and control would have evolved similarly)
- No confounding policy changes
- Stable composition over time

**Threats:**
- COVID-19 disruption (2020-2022)
- Other policy changes
- Testing guideline changes

**Mitigation:**
- Exclude COVID period (2020-2022)
- Include condition-specific time trends
- Test for pre-trends

---

## Power Analysis

### Minimum Detectable Effects

**For event study design:**
- Baseline testing rate: 50 per 100,000
- Standard deviation: 5 per 100,000
- Pre-periods: 24 months
- Post-periods: 24 months
- Power: 80%
- Alpha: 0.05

**Minimum detectable effect:** 3 per 100,000 (6% change)

**For calibration approach:**
- Prior SD: 0.035 (deterrence elasticity)
- Desired posterior SD: 0.02
- Required sample size: N/A (using existing evidence)

---

## Timeline

| Activity | Q1 2026 | Q2 2026 | Q3 2026 | Q4 2026 |
|----------|---------|---------|---------|---------|
| Ethics applications | Jan-Mar | | | |
| Data access applications | | Apr-Jun | | |
| Data linkage | | | Jul-Sep | |
| Event study analysis | | | | Oct-Dec |
| Calibration (current) | Jan-Mar | | | |

**Current approach (calibration):** Complete
**Empirical estimation:** 12-18 months (future work)

---

## Recommendations

### Immediate (Current Project)

1. **Continue with calibration approach**
   - Use evidence register priors
   - Transparent uncertainty quantification
   - VOI to identify high-value parameters

2. **Document data gaps**
   - Make evidence limitations prominent
   - VOI will show where data matters most

### Medium-term (Future Research)

1. **Pursue data access for event study**
   - MBS testing data (Australia)
   - Genetic Testing Database (NZ)
   - HRC/FSC complaints data

2. **Explore survey options**
   - Discrete choice experiment on testing intentions
   - Link to existing surveys (45 and Up, NZHS)

3. **Build clinical collaborations**
   - Access to family history + genetic test data
   - Diagnostic accuracy studies

---

## References

- Meyer BD. Natural and Quasi-Experiments in Economics. JBE&S. 1995.
- Wing C et al. Designing Difference in Difference Studies. JCE. 2018.
- ISPOR-SMDM Modeling Good Practices Task Force. Value Health. 2012.

---

**Version:** 1.0
**Date:** 2026-03-03
**Track:** gdpe_0002_evidence_anchoring
