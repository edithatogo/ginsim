# Implementation Plan: Model Implementation and Policy Analysis

**Track ID:** gdpe_0003_model_implementation  
**Type:** Research + Implementation  
**Estimated duration:** 6-8 weeks  
**Dependencies:** gdpe_0002_evidence_anchoring (complete - provides calibrated priors)

---

## Phase 1 — Core Game Implementation (Weeks 1-2)

**Goal:** Implement the five strategic games with actual equilibrium calculations

### Tasks
- [ ] **Task 1.1:** Module A - Discrete choice model for testing behavior
  - Implement logit/probit model of testing choice
  - Policy regime enters via perceived_penalty term
  - Integrate with calibrated priors from Phase 2 (gdpe_0002)
  - Unit tests for choice probabilities

- [ ] **Task 1.2:** Module C - Rothschild-Stiglitz equilibrium solver
  - Implement separating equilibrium (information allowed)
  - Implement pooling equilibrium (information restricted)
  - JAX root-finding for equilibrium prices
  - Unit tests for equilibrium conditions

- [ ] **Task 1.3:** Module D - Constrained proxy optimization
  - Implement risk prediction model (logistic regression)
  - Policy removes genetic_test_result from feature set
  - Re-optimize using allowed features
  - Compute accuracy metrics

- [ ] **Task 1.4:** Module F - Data quality externality
  - Implement participation function
  - Selection bias model
  - Impact on predictive performance

- [ ] **Task 1.5:** Enforcement module - Compliance game
  - Implement detection probability function
  - Solve for mixed-strategy Nash equilibrium
  - Integrate enforcement_strength parameter

**Acceptance criteria:**
- All 5 games implemented with actual calculations (no placeholders)
- Unit tests pass for all modules
- Equilibrium solvers converge in <100 iterations

---

## Phase 2 — Integration and Pipeline (Week 3)

**Goal:** Integrate modules into unified policy evaluation pipeline

### Tasks
- [ ] **Task 2.1:** Policy scenario encoder
  - Encode 3 policy regimes (status quo, moratorium, ban)
  - Encode for both AU and NZ
  - Validate against policy configs

- [ ] **Task 2.2:** Module integration
  - Connect Module A → C → D → F → Enforcement
  - Ensure data flows correctly between modules
  - Parallel execution where possible

- [ ] **Task 2.3:** DCBA ledger integration
  - Aggregate welfare impacts across modules
  - Distributional impacts by risk group
  - Fiscal impacts (health system costs)

- [ ] **Task 2.4:** Output formatter
  - Generate tables for policy brief
  - Generate figures (testing uptake, premiums, welfare)
  - Uncertainty intervals (95% CrI)

**Acceptance criteria:**
- Full pipeline executes without errors
- Results generated for all 6 scenarios (3 policies × 2 jurisdictions)
- Runtime <4 hours for 2000 draws

---

## Phase 3 — Validation and Calibration (Week 4)

**Goal:** Validate full model against empirical targets

### Tasks
- [ ] **Task 3.1:** Posterior predictive checks
  - Run full model with calibrated priors
  - Compare to empirical targets
  - Adjust model structure if poor fit

- [ ] **Task 3.2:** Cross-validation
  - Compare results to ≥3 published studies
  - Document agreement/discrepancies
  - Explain any large discrepancies

- [ ] **Task 3.3:** Stress tests
  - Run 8 extreme scenarios
  - Verify logical consistency
  - Check bounds and monotonicity

- [ ] **Task 3.4:** Face validity review
  - Send model structure to ≥2 expert reviewers
  - Collect and address feedback
  - Document reviewer responses

**Acceptance criteria:**
- PPC shows good calibration (coverage >50%, bias <20%)
- Cross-validation: ≥70% good/moderate agreement
- Stress tests: 8/8 pass
- Face validity: ≥2 reviews received, all critical issues addressed

---

## Phase 4 — Policy Analysis (Week 5)

**Goal:** Generate policy results and recommendations

### Tasks
- [ ] **Task 4.1:** Main policy analysis
  - Run full policy sweep (2000 draws)
  - Generate results tables for all outcomes
  - Compute incremental effects (ban vs moratorium vs status quo)

- [ ] **Task 4.2:** Uncertainty analysis
  - Generate 95% credible intervals
  - Cost-effectiveness acceptability curves
  - Identify parameters driving decision uncertainty

- [ ] **Task 4.3:** Value of Information analysis
  - Compute EVPI (overall uncertainty)
  - Compute EVPPI by parameter group
  - Identify research priorities

- [ ] **Task 4.4:** Sensitivity analysis
  - One-way sensitivity (tornado diagrams)
  - Scenario analysis (best/worst case)
  - Identify key drivers of results

**Acceptance criteria:**
- Results generated for all scenarios
- Uncertainty fully quantified
- EVPI/EVPPI computed
- Key drivers identified

---

## Phase 5 — Dissemination (Weeks 6-8)

**Goal:** Prepare outputs for publication and policy engagement

### Tasks
- [ ] **Task 5.1:** Manuscript preparation
  - Complete methods section (from gdpe_0002)
  - Write results section
  - Write discussion/conclusions
  - Select target journal (Value in Health / MDM / JHE)
  - Format per journal guidelines

- [ ] **Task 5.2:** Policy brief preparation
  - Executive summary (≤200 words)
  - Key findings (3-5 bullet points)
  - Policy recommendations
  - Plain language glossary
  - Colorblind-safe figures

- [ ] **Task 5.3:** Code and data deposition
  - Prepare Zenodo deposition
  - Ensure all code documented
  - Assign DOI
  - Verify reproducibility

- [ ] **Task 5.4:** Stakeholder engagement
  - Identify AU/NZ government contacts
  - Send policy brief to stakeholders
  - Offer briefing presentations

**Acceptance criteria:**
- Manuscript submitted to journal
- Policy brief completed
- Zenodo DOI assigned
- Stakeholders engaged

---

## Summary Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| **Phase 1** | Weeks 1-2 | 5 game implementations, unit tests |
| **Phase 2** | Week 3 | Integrated pipeline, DCBA ledger |
| **Phase 3** | Week 4 | Validation results, expert reviews |
| **Phase 4** | Week 5 | Policy results, VOI analysis |
| **Phase 5** | Weeks 6-8 | Manuscript, policy brief, Zenodo DOI |

---

## Resource Requirements

### Computational
- Standard laptop with CPU (JAX XLA acceleration)
- ~4-8 hours per full model run (2000 draws)
- Storage: ~10GB for posterior samples

### Expertise
- Game theory / mechanism design
- Insurance economics (adverse selection)
- Bayesian econometrics
- JAX/Python programming

### Reviewers
- ≥2 experts for face validity review
- Suggested: Health economist, insurance market expert

---

## Risks and Mitigation

| Risk | Mitigation |
|------|-----------|
| Equilibrium solvers fail to converge | Multiple initialization points; approximate fallbacks |
| Results inconsistent with literature | Module-by-module cross-validation |
| Computational cost too high | JAX acceleration; reduce draws for initial runs |
| Policy results inconclusive | Ensure adequate power; focus on low-uncertainty parameters |

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0003_model_implementation
