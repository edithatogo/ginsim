# Phase 4 Plan: Validation and Verification

**Track:** gdpe_0002_evidence_anchoring  
**Phase:** 4 — Validation and verification  
**Estimated duration:** 2 weeks  
**Start date:** 2026-03-03

---

## Goal

Systematic model validation across all dimensions to ensure credibility, transparency, and fitness for policy advice.

---

## Acceptance Criteria

- [ ] ≥2 external experts complete face validity review
- [ ] Cross-validation against ≥3 published studies completed
- [ ] Stress tests pass for all extreme scenarios
- [ ] Posterior predictive checks show adequate fit
- [ ] Validation report completed and signed off

---

## Tasks

### Task 1: Face Validity Protocol

**Objective:** Obtain expert review of model structure and assumptions

**Actions:**
1. Identify 2-3 external experts (health economics, insurance markets, genetic policy)
2. Prepare review package:
   - Model structure documentation
   - Assumptions registry
   - Evidence registers (AU + NZ)
   - Calibration configs
3. Send review requests with structured questionnaire
4. Collect and document feedback
5. Address critical concerns

**Deliverables:**
- Expert reviewer list
- Review package sent
- Feedback summary document
- Response to reviewer comments

**Timeline:** Week 1

**Success criteria:**
- ≥2 expert reviews received
- All critical issues addressed
- Model structure validated

---

### Task 2: Cross-Validation Against Published Literature

**Objective:** Compare model outputs to existing studies

**Actions:**
1. Identify ≥3 published studies for comparison:
   - Similar policy questions (genetic discrimination, insurance)
   - Comparable methodologies (Bayesian decision analysis, CEAs)
   - AU/NZ or similar health systems
2. Extract comparable outputs from studies:
   - Testing uptake changes
   - Premium impacts
   - Welfare effects
3. Run model with comparable parameters
4. Compare outputs and document differences
5. Explain discrepancies (model structure, assumptions, data)

**Deliverables:**
- Cross-validation studies list
- Comparison tables
- Discrepancy analysis document

**Timeline:** Week 1

**Success criteria:**
- ≥3 studies compared
- Differences <20% or well-explained
- Model outputs within plausible ranges

---

### Task 3: Stress Tests and Edge Case Validation

**Objective:** Verify model behavior under extreme scenarios

**Actions:**
1. Define extreme scenarios:
   - **Scenario A:** 100% testing uptake (no deterrence)
   - **Scenario B:** 0% adverse selection (no information asymmetry)
   - **Scenario C:** 100% enforcement (perfect compliance)
   - **Scenario D:** 0% enforcement (no compliance)
   - **Scenario E:** 100% proxy substitution (perfect substitutes)
   - **Scenario F:** 0% proxy substitution (no substitutes)
2. Run model for each scenario
3. Verify expected behavior:
   - Monotonicity where expected
   - Bounds respected (no negative premiums, etc.)
   - Logical consistency
4. Document any unexpected behavior
5. Fix bugs if found

**Deliverables:**
- Stress test scenarios document
- Model outputs for each scenario
- Validation results
- Bug fix log (if applicable)

**Timeline:** Week 1-2

**Success criteria:**
- All scenarios run without errors
- Model behavior matches expectations
- No logical inconsistencies found

---

### Task 4: Posterior Predictive Checks

**Objective:** Verify that priors generate plausible outputs

**Actions:**
1. Draw samples from all priors (n=2000)
2. Simulate model outputs for each draw
3. Compare to empirical targets:
   - Baseline testing uptake (~52%)
   - Observed premium levels
   - Insurance take-up rates
4. Generate posterior predictive plots
5. Identify mis-calibrated parameters
6. Adjust priors if necessary

**Deliverables:**
- Prior predictive simulation code
- Comparison plots
- Calibration assessment
- Adjusted priors (if needed)

**Timeline:** Week 2

**Success criteria:**
- Prior predictive distributions cover empirical targets
- No systematic bias
- Uncertainty ranges plausible

---

### Task 5: Phase 4 Review

**Objective:** Complete validation report and sign-off

**Actions:**
1. Compile validation results:
   - Face validity feedback
   - Cross-validation comparisons
   - Stress test results
   - Posterior predictive checks
2. Write validation report
3. Generate Phase 4 review document
4. Run reference validation
5. Update decision log
6. Sign off on Phase 4 completion

**Deliverables:**
- Validation report (`docs/VALIDATION_REPORT.md`)
- Phase 4 review (`conductor/tracks/.../phase_4_review.md`)
- Reference validation report
- Updated decision log

**Timeline:** Week 2

**Success criteria:**
- All validation activities documented
- No critical issues outstanding
- Phase 4 review passed

---

## Resources Needed

### Expert Reviewers (Task 1)

**Potential reviewers:**
1. Health economist with insurance expertise
2. Genetic policy researcher
3. Actuary with genetic discrimination knowledge

**Review package:**
- Model documentation (20-30 pages)
- Evidence registers
- Calibration configs
- Structured questionnaire

### Computational Resources (Tasks 3-4)

**Requirements:**
- Standard laptop (JAX CPU execution)
- ~2-4 hours for stress tests
- ~1-2 hours for posterior predictive checks

**Scripts needed:**
- `scripts/run_stress_tests.py`
- `scripts/run_prior_predictive_checks.py`

---

## Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Expert reviewers unavailable | Medium | High | Start early; have backup reviewers |
| Cross-validation studies not comparable | Medium | Medium | Use wide comparison criteria; focus on direction |
| Stress tests reveal bugs | Low | High | Fix before Phase 5; document thoroughly |
| Posterior predictive checks show mis-calibration | Medium | Medium | Adjust priors; re-run checks |

---

## Timeline

| Week | Tasks |
|------|-------|
| **Week 1** | Task 1 (Face validity), Task 2 (Cross-validation), Task 3 (Stress tests) |
| **Week 2** | Task 3 (complete), Task 4 (Posterior predictive), Task 5 (Phase 4 review) |

---

## Decision Log Entries (Phase 4)

Document decisions made during Phase 4:
- Expert reviewer selection criteria
- Cross-validation study selection
- Stress test scenario definitions
- Prior adjustments (if any)
- Validation acceptance criteria

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0002_evidence_anchoring
