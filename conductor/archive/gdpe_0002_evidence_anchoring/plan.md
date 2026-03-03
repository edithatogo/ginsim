# Implementation plan: Evidence anchoring and calibration (AU/NZ)

**Track ID:** gdpe_0002_evidence_anchoring  
**Type:** Research  
**Estimated duration:** 6-8 weeks  
**Dependencies:** gdpe_0001_bootstrap (completed)

---

## Phase 1 — Evidence registers
**Goal:** Populate evidence registers for both jurisdictions with graded evidence  
**Estimated duration:** 1-2 weeks  
**Acceptance criteria:**
- [x] All 6 modules (A-F) have evidence entries for Australia
- [x] All 6 modules (A-F) have evidence entries for New Zealand
- [x] All evidence items have quality grades (GRADE framework)
- [x] All evidence items have complete citations in references.bib
- [x] Policy timeline tables created for both jurisdictions

### Tasks
- [x] Populate Australia evidence register (Module A deterrence; Module C assumptions; proxy substitution; enforcement) ✅ COMPLETED 2026-03-03
- [x] Populate New Zealand evidence register ✅ COMPLETED 2026-03-03
- [x] Add policy timeline tables (dates, caps, enforcement mechanisms) ✅ COMPLETED 2026-03-03
- [x] Define evidence quality grading rubric (adapted GRADE framework for policy modelling) ✅ COMPLETED
- [x] Add citation management structure (BibTeX/Zotero integration for evidence tracking) ✅ COMPLETED
- [x] **Phase 1 review: Run reference validation and quality check** ✅ COMPLETED 2026-03-03 (see phase_1_review.md)

---

## Phase 2 — Calibration targets and priors
**Goal:** Convert evidence to prior distributions with transparent rationale  
**Estimated duration:** 1-2 weeks  
**Acceptance criteria:**
- [x] Calibration targets defined for all modules with empirical ranges
- [x] Prior distributions documented in configs with evidence links
- [x] EVPPI parameter groupings defined
- [x] Evidence-to-prior mapping document completed

### Tasks
- [x] Define calibration targets per module (uptake, premium changes, take-up, claims proxies) ✅ COMPLETED 2026-03-03
- [x] Convert evidence into prior distributions (documented in configs) ✅ COMPLETED 2026-03-03
- [x] Add sensitivity-ready parameter groupings for EVPPI ✅ COMPLETED 2026-03-03
- [x] Document evidence-to-prior mapping rationale (transparent assumptions) ✅ COMPLETED 2026-03-03
- [x] **Phase 2 review: Validate priors against evidence and run smoke test** ✅ COMPLETED 2026-03-03 (see phase_2_review.md)

---

## Phase 3 — Identification plan and data access
**Goal:** Document data sources, access pathways, and transformation lineage  
**Estimated duration:** 1 week  
**Acceptance criteria:**
- [x] Identification plan document completed
- [x] Data access and governance appendix completed
- [x] Runbook updated with calibration workflow
- [x] Data provenance documented for all datasets

### Tasks
- [x] Write identification plan (survey linkage; admin health; insurer aggregates; event study) ✅ COMPLETED 2026-03-03
- [x] Add "data access and governance" appendix ✅ COMPLETED 2026-03-03
- [x] Update runbook with calibration workflow ✅ COMPLETED 2026-03-03
- [x] Document data provenance and transformation lineage (input/output schemas) ✅ COMPLETED 2026-03-03
- [x] **Phase 3 review: Verify data provenance completeness** ✅ COMPLETED 2026-03-03 (see phase_3_review.md)

---

## Phase 4 — Validation and verification
**Goal:** Systematic model validation across all dimensions  
**Estimated duration:** 2 weeks  
**Acceptance criteria:**
- [ ] ≥2 external experts complete face validity review
- [ ] Cross-validation against ≥3 published studies completed
- [ ] Stress tests pass for all extreme scenarios
- [ ] Posterior predictive checks show adequate fit

### Tasks
- [ ] Face validity protocol (expert review of model structure and assumptions)
- [ ] Cross-validation against published literature (compare model outputs to existing studies)
- [ ] Stress tests and edge case validation (extreme scenarios: 100% uptake, zero adverse selection)
- [ ] Posterior predictive checks for module-level fit
- [ ] **Phase 4 review: Validation report sign-off** ← NEW GATE

---

## Phase 5 — Research outputs and dissemination
**Goal:** Prepare outputs for publication and policy dissemination  
**Estimated duration:** 1-2 weeks  
**Acceptance criteria:**
- [ ] Evidence tables integrated into publish pack
- [ ] "Evidence to priors" appendix completed
- [ ] CITATION.cff and Zenodo metadata ready
- [ ] Methods section drafted for journal submission

### Tasks
- [ ] Update meta pipeline to include evidence tables in publish pack
- [ ] Produce a brief "evidence to priors" appendix for policy brief
- [ ] Add CITATION.cff for academic citation ✅ COMPLETED
- [ ] Prepare Zenodo metadata for DOI assignment (long-term archiving) ✅ COMPLETED
- [ ] Draft methods section for journal submission (reproducibility focus)
- [ ] **Phase 5 review: Final quality check and reference validation** ← NEW GATE
- [ ] **Track complete: All phases signed off** ← FINAL GATE

