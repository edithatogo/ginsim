# Face Validity Review Package

**Track:** gdpe_0002_evidence_anchoring — Phase 4  
**Purpose:** Expert review materials for model validation

---

## Package Contents

1. **Model Overview** (this document)
2. **Model Structure Documentation** (`docs/MODEL_CARD.md`)
3. **Evidence Registers** (`context/jurisdiction_profiles/*_evidence_register.yaml`)
4. **Calibration Configs** (`configs/calibration_*.yaml`)
5. **Assumptions Registry** (`context/assumptions_registry.yaml`)
6. **Decision Log** (`context/decision_log.md`)
7. **Review Questionnaire** (below)

---

## Model Overview

### Research Question

What are the net social impacts of alternative policy regimes restricting the use of genetic information in life insurance underwriting?

### Policy Context

- **Australia:** FSC Moratorium (2019-2024), proposed statutory ban (2025)
- **New Zealand:** HRC Inquiry (2020), no specific legislation

### Model Structure

**Six interconnected modules:**

```
Policy Rules → Module A (Behavior) → Module B (Clinical)
                    ↓
            Module C (Insurance Equilibrium)
                    ↓
    Module D (Proxy) → Module E (Pass-through) → Module F (Data Quality)
                    ↓
            DCBA Ledger → VOI/EVPPI
```

**Module Descriptions:**

| Module | Purpose | Key Parameters |
|--------|---------|---------------|
| **A: Behavior** | Testing uptake, deterrence effects | baseline_uptake, deterrence_elasticity, moratorium_effect |
| **B: Clinical** | Health outcomes, QALYs | condition-specific penetrance, intervention effectiveness |
| **C: Insurance** | Adverse selection, premium setting | adverse_selection_elasticity, demand_elasticity, loading |
| **D: Proxy** | Family history accuracy | sensitivity, substitution_rate |
| **E: Pass-through** | Market structure, incidence | pass_through_rate |
| **F: Data Quality** | Research participation effects | participation_elasticity |

### Bayesian Framework

**Approach:** Full probabilistic Bayesian decision analysis

**Uncertainty propagation:**
- Priors from evidence registers (GRADE-quality assessed)
- MCMC sampling (NumPyro/BlackJAX)
- Common random numbers for policy contrasts

**Outputs:**
- Posterior distributions for all outcomes
- EVPI/EVPPI for research prioritization
- Cost-effectiveness acceptability curves

---

## Policy Scenarios

| Scenario | Description | Enforcement | Caps |
|----------|-------------|-------------|------|
| **Status Quo** | No restrictions | N/A | None |
| **FSC Moratorium** | Industry self-regulation | Industry body | $500k life, $200k TPD/trauma |
| **Statutory Ban** | Legislative prohibition | Statutory penalties | None (full ban) |

---

## Key Assumptions

1. **Behavioral:** Deterrence reduces testing uptake; moratorium reduces deterrence
2. **Insurance:** Adverse selection occurs when informed high-risks purchase more coverage
3. **Clinical:** Earlier detection → better outcomes (condition-specific)
4. **Proxy:** Family history partially substitutes for genetic information
5. **Market:** Costs passed through to consumers (degree depends on competition)
6. **Data:** Genetic testing restrictions affect research participation

**Full assumptions registry:** `context/assumptions_registry.yaml`

---

## Evidence Base

### Australia

| Module | Evidence Items | Quality (GRADE) |
|--------|---------------|-----------------|
| A | 3 | 1 Moderate, 2 Low/Very Low |
| C | 3 | 3 Low/Very Low |
| D | 2 | 1 Moderate, 1 Very Low |
| E | 1 | 1 Moderate |
| F | 1 | 1 Low |
| Enforcement | 2 | 2 Very Low |

### New Zealand

| Module | Evidence Items | Quality (GRADE) |
|--------|---------------|-----------------|
| All | 5 total | 100% Very Low |

**Note:** NZ evidence base is extremely weak. All parameters adapted from international studies with widened priors.

**Full evidence registers:** `context/jurisdiction_profiles/*_evidence_register.yaml`

---

## Review Questionnaire

### Section 1: Model Structure

**Q1.1:** Does the causal framework (policy → behavior → insurance → clinical → welfare) make sense for this policy question?

- [ ] Yes, fully appropriate
- [ ] Mostly appropriate, minor issues
- [ ] Partially appropriate, major issues
- [ ] No, fundamentally flawed

**Comments:**

---

**Q1.2:** Are there any critical pathways or mechanisms missing from the model?

- [ ] No, model is comprehensive
- [ ] Minor omissions (please specify)
- [ ] Major omissions (please specify)

**Comments:**

---

**Q1.3:** Is the modular approach (separate behavior, clinical, insurance modules) appropriate?

- [ ] Yes, well-suited to the problem
- [ ] Acceptable with minor modifications
- [ ] Problematic (please explain)

**Comments:**

---

### Section 2: Key Assumptions

**Q2.1:** Are the behavioral assumptions (deterrence → reduced testing) reasonable?

- [ ] Yes, well-supported by evidence
- [ ] Reasonable but uncertain
- [ ] Questionable (please explain)
- [ ] Unsupported

**Comments:**

---

**Q2.2:** Is the adverse selection mechanism (informed high-risks → higher premiums) appropriately modeled?

- [ ] Yes, standard economic theory
- [ ] Reasonable simplification
- [ ] Oversimplified (please explain)
- [ ] Incorrect

**Comments:**

---

**Q2.3:** Are the proxy substitution assumptions (family history as partial substitute) reasonable?

- [ ] Yes, well-supported
- [ ] Reasonable approximation
- [ ] Overstates proxy accuracy
- [ ] Understates proxy accuracy

**Comments:**

---

### Section 3: Parameter Choices

**Q3.1:** Do the prior distributions align with the evidence base?

- [ ] Yes, well-calibrated
- [ ] Mostly appropriate
- [ ] Some concerns (please specify)
- [ ] Major concerns (please specify)

**Comments:**

---

**Q3.2:** Are the uncertainty ranges (prior variances) appropriate given evidence quality?

- [ ] Yes, appropriately wide for low-quality evidence
- [ ] Somewhat appropriate
- [ ] Too narrow (overconfident)
- [ ] Too wide (uninformative)

**Comments:**

---

**Q3.3:** For New Zealand parameters (adapted from Australia with wider priors), is this approach reasonable?

- [ ] Yes, only option given data limitations
- [ ] Acceptable with caveats
- [ ] Problematic (please explain)

**Comments:**

---

### Section 4: Policy Relevance

**Q4.1:** Will the model outputs (testing uptake, premiums, QALYs, welfare) be useful for policy makers?

- [ ] Yes, directly relevant
- [ ] Mostly relevant
- [ ] Partially relevant
- [ ] Not particularly relevant

**Comments:**

---

**Q4.2:** Is the uncertainty quantification (posterior distributions, EVPI/EVPPI) appropriate for policy advice?

- [ ] Yes, essential for honest advice
- [ ] Appropriate level
- [ ] Excessive detail for policy audience
- [ ] Insufficient

**Comments:**

---

**Q4.3:** Are there additional outputs or analyses that would enhance policy relevance?

**Comments:**

---

### Section 5: Overall Assessment

**Q5.1:** Overall, is the model structure and approach fit for purpose?

- [ ] Yes, fully fit for policy advice
- [ ] Fit with minor modifications
- [ ] Fit with major modifications
- [ ] Not fit for purpose

**Comments:**

---

**Q5.2:** What are the top 3 strengths of this modelling approach?

1.
2.
3.

---

**Q5.3:** What are the top 3 weaknesses or limitations?

1.
2.
3.

---

**Q5.4:** Would you recommend any changes before the model is used for policy advice?

- [ ] No, ready for use
- [ ] Minor changes recommended (please specify)
- [ ] Major changes required (please specify)
- [ ] Not ready for policy use

**Comments:**

---

## Submission

**Please return completed questionnaire by:** [Date, 2 weeks from invitation]

**Return to:** [Email address]

**Format:** PDF or Word document with comments

---

## Reviewer Information

**Name:**

**Affiliation:**

**Expertise area:**
- [ ] Health economics
- [ ] Insurance markets / actuarial science
- [ ] Genetic policy / law
- [ ] Other: _________

**Conflict of interest declaration:**
- [ ] No conflicts to declare
- [ ] Potential conflicts (please specify): _________

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0002_evidence_anchoring
