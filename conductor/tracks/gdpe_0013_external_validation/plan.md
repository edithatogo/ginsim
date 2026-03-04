# Implementation Plan: External Validation (Simulated Expert Review & Cross-Validation)

**Track ID:** gdpe_0013_external_validation  
**Estimated duration:** 3-4 weeks  
**Dependencies:** gdpe_0002_evidence_anchoring (completed), gdpe_0003_model_implementation (completed)

---

## Phase 1 — Simulated Expert Face-Validity Review (Week 1)

**Goal:** Simulate formal expert feedback for model validation

### Tasks
- [ ] **Task 1.1:** Persona definition and review simulation (Health Economist)
  - Simulate expert persona: Health economist specializing in genetic policy
  - Evaluate model structure, welfare aggregation, and VOI metrics
  - Return structured feedback based on `protocols/face_validity_review_package.md`

- [ ] **Task 1.2:** Persona definition and review simulation (Insurance Actuary)
  - Simulate expert persona: Actuary specializing in adverse selection and life insurance
  - Evaluate Module C (equilibrium solvers) and Module D (proxy substitution)
  - Return structured feedback based on `protocols/face_validity_review_package.md`

- [ ] **Task 1.3:** Persona definition and review simulation (Genetic Policy Expert)
  - Simulate expert persona: Legal/Policy expert on genetic discrimination
  - Evaluate Module A (behavioral deterrence) and enforcement mechanisms
  - Return structured feedback based on `protocols/face_validity_review_package.md`

- [ ] **Task 1.4:** Consolidated validation report
  - Integrate all 3 expert reports into a final document
  - Create Action Log of recommended changes or justifications

**Acceptance criteria:**
- 3 structured expert review reports generated
- Consolidated Expert Review Report and Action Log completed

---

## Phase 2 — Empirical Cross-Validation (Week 2)

**Goal:** Validate model outputs against published studies

### Tasks
- [ ] **Task 2.1:** Data extraction and comparison (Adverse Selection)
  - Extract quantitative targets from Hersch & Viscusi (2019)
  - Compare model premium divergence and uptake under adverse selection

- [ ] **Task 2.2:** Data extraction and comparison (Deterrence)
  - Extract quantitative targets from Bombard et al. (2018)
  - Compare model deterrence elasticity and testing uptake

- [ ] **Task 2.3:** Data extraction and comparison (Market Behavior)
  - Extract quantitative targets from Taylor et al. (2021) and Armstrong et al. (2020)
  - Compare Australian market behavior and policy impacts

- [ ] **Task 2.4:** Cross-validation report
  - Document overall agreement/discrepancies
  - Explain discrepancies based on model assumptions or context

**Acceptance criteria:**
- Cross-validation against 5 studies documented
- Discrepancies addressed and justified

---

## Phase 3 — Integration and Final Validation (Weeks 3-4)

**Goal:** Finalize model validation and publication readiness

### Tasks
- [ ] **Task 3.1:** Execute Action Log items
  - Update model structure, parameters, or documentation based on Phase 1 & 2 findings
  - Re-run calibration if necessary

- [ ] **Task 3.2:** Final Model Validation Report
  - Finalize `docs/MODEL_VALIDATION_REPORT.md` integrating all validation work (Stress tests, PPC, Expert Review, Cross-Validation)

- [ ] **Task 3.3:** Final Publication Readiness Check
  - Perform final review of all artifacts (Manuscript draft, Policy brief, Zenodo metadata)
  - Mark track complete and archive

**Acceptance criteria:**
- Model Validation Report complete
- Publication readiness standards met
- Track archived

---

## Summary Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| **Phase 1** | Week 1 | 3 Expert Review Reports, Action Log |
| **Phase 2** | Week 2 | Cross-Validation Report |
| **Phase 3** | Weeks 3-4 | Final Validation Report, Final Publication Check |

---

## Automation Protocol

**At the end of each phase, the following will execute automatically:**

1. **Conductor Review** - Run `conductor:review` skill
2. **Automated Checks** - ruff, pytest, reference validation
3. **Generate Report** - Phase review report with findings
4. **Implement Recommendations** - Auto-fix issues where possible
5. **Auto-Progress** - Move to next phase automatically

---

**Version:** 1.0  
**Date:** 2026-03-04  
**Status:** Active
