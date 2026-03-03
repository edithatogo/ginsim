# Phase 3 Review: Identification Plan and Data Access

**Track:** gdpe_0002_evidence_anchoring  
**Phase:** Phase 3 — Identification plan and data access  
**Review date:** 2026-03-03  
**Reviewer:** AI Assistant (Conductor workflow)

---

## Phase Completion Checklist

### Tasks
- [x] Write identification plan (survey linkage; admin health; insurer aggregates; event study)
- [x] Add "data access and governance" appendix
- [x] Update runbook with calibration workflow
- [x] Document data provenance and transformation lineage
- [x] Phase 3 review: Verify data provenance completeness

### Acceptance Criteria
- [x] Identification plan document completed
- [x] Data access and governance appendix completed
- [x] Runbook updated with calibration workflow
- [x] Data provenance documented for all datasets

### Quality Checks
- [x] Reference validation run (`python -m scripts.validate_references --report`)
- [x] No critical reference errors
- [x] Decision log updated
- [x] Data provenance templates complete

### Documentation
- [x] All documentation follows product-guidelines.md
- [x] Writing tone appropriate for technical/research audience
- [x] All claims evidence-based or labeled as assumptions

---

## Automated Check Results

### Reference Validation

**Command:** `python -m scripts.validate_references --report`

**Results:**
```
Total entries: 27
Valid: 27 (100%)
Warnings: 2 (acceptable)
Duplicates: 0
```

**Status:** ✅ **Pass** (no new issues)

---

## Phase 3 Artifacts Produced

| Artifact | Path | Description |
|----------|------|-------------|
| Identification Plan | `docs/IDENTIFICATION_PLAN.md` | Data sources, identification strategies, event study design |
| Data Access Governance | `docs/DATA_ACCESS_GOVERNANCE.md` | Ethics, privacy, Māori data sovereignty, security |
| Data Provenance Log | `docs/DATA_PROVENANCE_LOG.md` | Data lineage, transformations, version control |
| Runbook v2.0 | `docs/RUNBOOK.md` | Updated with calibration workflow |
| Phase 3 Review | `conductor/tracks/gdpe_0002_evidence_anchoring/phase_3_review.md` | This document |

---

## Identification Strategy Summary

### Module-by-Module Approach

| Module | Preferred Identification | Current Approach | Status |
|--------|-------------------------|-----------------|--------|
| A (Behaviour) | Event study | Calibration | Documented |
| C (Insurance) | Structural estimation | Calibration | Documented |
| D (Proxy) | Diagnostic accuracy | Calibration | Documented |
| E (Pass-through) | Empirical pass-through | Calibration | Documented |
| F (Data quality) | Survey-based | Calibration | Documented |
| Enforcement | Administrative data | Calibration | Documented |

**Rationale:** Calibration approach used for Phase 1-3 due to data access constraints. Empirical estimation documented for future research.

---

## Data Sources Inventory

### Australia (5 sources identified)

| Dataset | Custodian | Access | Status |
|---------|-----------|--------|--------|
| MBS genetic testing | Dept Health | Application | Not yet accessed |
| APRA statistics | APRA | Public | Available |
| Cancer Database | AIHW | Ethics | Not yet accessed |
| FSC complaints | FSC | Industry | Not yet accessed |
| 45 and Up Study | Sax Institute | Application | Potential |

### New Zealand (5 sources identified)

| Dataset | Custodian | Access | Status |
|---------|-----------|--------|--------|
| Genetic Testing DB | Lablink/NHB | Application | Not yet accessed |
| Cancer Registry | MoH | HQSC | Not yet accessed |
| NZ Health Survey | MoH | Stats NZ | Potential |
| HRC complaints | HRC | Application | Not yet accessed |
| IRD insurance | IRD | Restricted | Unlikely |

---

## Data Governance Framework

### Ethics Requirements

| Jurisdiction | Body | Timeline | Status |
|-------------|------|----------|--------|
| Australia | HREC/NHRMC | 8-12 weeks | Not yet applied |
| New Zealand | HDEC | 6-10 weeks | Not yet applied |

### Māori Data Sovereignty

**Principles acknowledged:**
- Rangatiratanga (control)
- Whai Rawa (ownership)
- Kotahitanga (collective/individual)
- Manaakitanga (enhance mana)
- Tiakitanga (responsible use)
- Tino Rangatiratanga (authority)

**Current status:**
- Principles acknowledged in documentation
- No Māori data accessed (Phase 1-3)
- Commitment to partnership in future phases

---

## Data Provenance Status

### Current Data (Phase 1-3)

**Classification:** Public aggregate data

| Data Type | Source | Transformation | Provenance |
|-----------|--------|---------------|------------|
| Evidence registers | Published studies | None | Documented |
| Calibration configs | Evidence registers | Manual extraction | Documented |
| Policy documents | FSC, HRC | None | Documented |

**Status:** ✅ All provenance documented

### Future Data (Phase 4+)

**Classification:** Restricted administrative data

**Planned documentation:**
- Dataset registration (YAML)
- Transformation logs (YAML)
- Checksums (MD5)
- Access logs
- Version control

**Status:** ⏳ Templates ready, awaiting data access

---

## Issues and Recommendations

### Critical Issues
**None** - All Phase 3 deliverables complete.

### Notes

1. **Empirical Identification Not Yet Feasible**
   - **Status:** Documented for future research
   - **Timeline:** 12-18 months (data access applications)
   - **Action:** Proceed with calibration approach

2. **Māori Data Sovereignty Requires Active Partnership**
   - **Status:** Acknowledged in documentation
   - **Commitment:** Contact Māori researchers in Phase 4
   - **Action:** Add to Phase 4 commitments

3. **Data Access Applications Not Yet Submitted**
   - **Status:** Planned for Phase 4
   - **Timeline:** 8-12 weeks approval
   - **Action:** Prepare applications in parallel with model development

---

## Review Decision

- [x] **Proceed to next phase** — All criteria met
- [ ] Proceed with minor revisions
- [ ] Requires major revisions

**Reviewer sign-off:** ✅ AI Assistant (Conductor workflow)  
**Date:** 2026-03-03

**Rationale:** All Phase 3 acceptance criteria met. Identification strategy documented. Data governance framework established. Data provenance templates ready. Reference validation passed.

---

## Next Phase Preparation

**Next phase:** Phase 4 — Validation and verification  
**Ready to start:** Yes  
**Prerequisites met:** Yes

**Phase 4 tasks:**
1. Face validity protocol (expert review of model structure and assumptions)
2. Cross-validation against published literature
3. Stress tests and edge case validation
4. Posterior predictive checks for module-level fit
5. Phase 4 review: Validation report sign-off

**Notes:**
- Calibration complete; ready for validation
- Prior predictive checks scheduled for Phase 4
- Expert recruitment for face validity review

---

## Appendix: Data Lineage Summary

```
Phase 1-3 (Current)
===================

Public Sources → Evidence Registers → Calibration Configs → Model
     ↓                  ↓                    ↓              ↓
  FSC, HRC,      YAML files          YAML configs     Prior draws
  APRA, Journals  (12+5 items)      (12+12 params)   (24 total)

Phase 4+ (Planned)
==================

Raw Data → Cleaned Data → Analysis Data → Model Outputs
   ↓           ↓              ↓              ↓
MBS,       Parquet        Aggregated     Posterior
Lablink    files          tables         draws
```

---

**END OF PHASE 3 REVIEW**
