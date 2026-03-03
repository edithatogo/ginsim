# Model Validation and Verification Protocol

## Purpose
Establish systematic validation procedures to ensure model credibility, transparency, and fitness for policy advice.

---

## Validation Framework

Adapted from ISPOR-SMDM Modeling Good Practices and ASME V&V 40 for computational models.

### Validation Dimensions

1. **Face Validity** — Does the model structure make sense to experts?
2. **Internal Validity** — Does the model behave as intended?
3. **External Validity** — Does the model match real-world observations?
4. **Cross-Model Validity** — How do results compare to alternative models?

---

## 1. Face Validity Protocol

### Expert Review Checklist

**Reviewers:** 2-3 independent experts in health economics, insurance markets, or genetic policy

#### Model Structure Review
- [ ] Causal pathways are plausible and evidence-based
- [ ] Key feedback loops are represented (adverse selection, testing behaviour)
- [ ] Time horizons are appropriate for the policy question
- [ ] Population subgroups are adequately represented
- [ ] Policy levers map to realistic interventions

#### Assumption Review
- [ ] All assumptions are explicitly documented
- [ ] Assumptions are justified with evidence or clearly labeled as necessary simplifications
- [ ] Alternative assumptions are noted for sensitivity analysis
- [ ] Assumptions are consistent with published literature

#### Parameter Review
- [ ] Parameter values are sourced from evidence register
- [ ] Uncertainty ranges are justified
- [ ] Correlations between parameters are considered

### Face Validity Report Template

```markdown
## Face Validity Assessment

**Reviewer:** [Name, affiliation]
**Date:** YYYY-MM-DD
**Model version:** [Git commit hash]

### Overall Assessment
[ ] Suitable for policy advice
[ ] Suitable with minor revisions
[ ] Requires major revisions before use
[ ] Not suitable

### Strengths
[List]

### Concerns
[List with severity: Low/Medium/High]

### Recommended Revisions
[Specific changes]

### Comments on Specific Modules

#### Module A (Behaviour/Deterrence)
[Comments]

#### Module B (Clinical Outcomes)
[Comments]

#### Module C (Insurance Equilibrium)
[Comments]

#### Modules D-F (Extensions)
[Comments]
```

---

## 2. Internal Validity Protocol

### Code Verification

**Purpose:** Ensure the code implements the intended model correctly.

#### Unit Tests
- [ ] Policy schema validation (Pydantic)
- [ ] Config loading and validation
- [ ] Random seed reproducibility
- [ ] Deterministic outputs with fixed seeds
- [ ] Boundary condition handling

#### Integration Tests
- [ ] End-to-end pipeline execution
- [ ] Data flow between modules
- [ ] Output file generation and format

#### Numerical Tests
- [ ] Equilibrium solver convergence
- [ ] MCMC convergence diagnostics (R-hat < 1.1)
- [ ] Gradient checking (if using VI)
- [ ] Mass matrix adaptation (for HMC/NUTS)

### Extreme Condition Tests

Test model behavior under extreme inputs:

| Test | Input | Expected Behavior |
|------|-------|-------------------|
| **Zero testing uptake** | `uptake = 0` | No clinical benefits, no adverse selection |
| **100% testing uptake** | `uptake = 1.0` | Maximum clinical benefits, maximum adverse selection pressure |
| **Zero adverse selection** | `elasticity = 0` | No premium impacts from information asymmetry |
| **Perfect adverse selection** | `elasticity = 1.0` | Maximum premium divergence |
| **Full enforcement** | `enforcement = 1.0` | No proxy substitution, no discrimination |
| **No enforcement** | `enforcement = 0.0` | Maximum proxy substitution effects |

### Conservation and Balance Checks

- [ ] Population totals are conserved across transitions
- [ ] Financial flows balance (premiums = claims + expenses + profits)
- [ ] QALY calculations are internally consistent
- [ ] Cohort tracking is accurate over time

---

## 3. External Validity Protocol

### Calibration Target Comparison

Compare model outputs to empirical targets:

| Target | Source | Model Output | Deviation | Status |
|--------|--------|--------------|-----------|--------|
| Testing uptake rate (baseline) | [Citation] | X% | ±Y% | [ ] Pass [ ] Fail |
| Premium levels (baseline) | [Industry data] | $X | ±Y% | [ ] Pass [ ] Fail |
| Insurance take-up rate | [Survey] | X% | ±Y% | [ ] Pass [ ] Fail |

**Acceptance criteria:** Model outputs within ±20% of empirical targets for key calibration points.

### Cross-Validation with Published Studies

Compare to published modelling studies:

```markdown
## Cross-Validation: [Study Name]

**Reference:** [Full citation]
**Comparison date:** YYYY-MM-DD

### Study Characteristics
- Jurisdiction: [Country]
- Policy scenario: [Description]
- Model type: [CEA, Markov, microsimulation, etc.]

### Comparison of Results

| Outcome | Published Study | This Model | Difference | Notes |
|---------|----------------|------------|------------|-------|
| Δ Testing uptake | +X% | +Y% | |Y-X|% | |
| Δ Premiums | +A% | +B%% | |B-A|% | |
| ICER | $X/QALY | $Y/QALY | |Y-X|% | |
| Net benefit | $X | $Y | |Y-X|% | |

### Discussion of Differences
[Explain any substantial differences]

### Conclusion
[ ] Consistent with published literature
[ ] Differences explained by model structure
[ ] Differences require investigation
```

---

## 4. Sensitivity Analysis Protocol

### One-Way Sensitivity

For each key parameter:
- Vary ±25% from base case (or use confidence interval bounds)
- Record impact on primary outcomes
- Generate tornado diagram

### Probabilistic Sensitivity Analysis

- Run full PSA with ≥1000 draws
- Generate cost-effectiveness acceptability curves
- Report 95% uncertainty intervals

### Value of Information

- Compute EVPI (overall uncertainty)
- Compute EVPPI (by parameter group)
- Identify top 5 parameters for research prioritization

### Scenario Analysis

Test alternative structural assumptions:
- [ ] High vs low deterrence scenarios
- [ ] Competitive vs concentrated market structure
- [ ] Strong vs weak enforcement
- [ ] Alternative proxy substitution specifications

---

## 5. Documentation Requirements

### Model Description

- [ ] Full mathematical specification (equations)
- [ ] Causal diagram / influence diagram
- [ ] State transition diagrams (if applicable)
- [ ] Parameter table with sources
- [ ] Assumptions log

### Technical Documentation

- [ ] Code documentation (docstrings)
- [ ] API documentation for key functions
- [ ] Installation and run instructions
- [ ] Example workflows

### User Guide

- [ ] How to run the model
- [ ] How to interpret outputs
- [ ] Limitations and caveats
- [ ] Citation guidance

---

## 6. Validation Report Template

```markdown
# Model Validation Report

**Model:** Genetic Discrimination Policy Economic Evaluation
**Version:** [Git commit hash]
**Validation date:** YYYY-MM-DD

## Executive Summary

[Brief overview of validation activities and conclusions]

## Validation Activities

### Face Validity
- Reviewers: [Names]
- Date: [Date]
- Outcome: [Pass/Fail/Conditional]
- Key concerns: [List]

### Internal Validity
- Unit tests: [X/Y passed]
- Integration tests: [X/Y passed]
- Extreme condition tests: [X/Y passed]
- Numerical verification: [Summary]

### External Validity
- Calibration targets: [X/Y met]
- Cross-validation: [Summary]

### Sensitivity Analysis
- One-way: [Completed]
- PSA: [Completed, n=X draws]
- VOI: [Completed]

## Limitations

[List known limitations and their implications]

## Conclusion

[ ] Model is valid for intended use
[ ] Model is valid with noted limitations
[ ] Model requires revisions before use
[ ] Model is not valid for intended use

## Sign-off

**Lead modeller:** _________________ Date: _______
**Independent reviewer:** _________________ Date: _______
```

---

## 7. Continuous Validation

### Version Control Integration

- Each major version requires re-validation
- Automated tests run on every commit
- Validation report versioned with model

### Change Log

Document all changes that affect validity:

```markdown
## Version 0.2.0 (2026-03-03)

### Changes
- Added Module D (proxy substitution)
- Updated Module C equilibrium solver

### Validation Impact
- Face validity: Re-review Module C structure
- Internal validity: New unit tests for Module D
- External validity: Re-calibration required

### Validation Status
[ ] Complete
[ ] In progress
[ ] Not started
```

---

## References

- Eddy DM, et al. ISPOR-SMDM Modeling Good Practices Task Force. Value in Health. 2012.
- ASME V&V 40-2018: Assessing Credibility of Computational Modeling through Verification and Validation.
- Chilcott J, et al. A review of studies to assess the value of further research. Value in Health. 2009.
