# Research Infrastructure Improvements

**Date:** 3 March 2026
**Track:** gdpe_0002_evidence_anchoring (Phase 5 integration)

---

## Summary

This document summarizes the research infrastructure improvements made to strengthen reproducibility, transparency, and policy credibility. These changes reflect best practices for health economics and policy modelling research.

---

## Files Created

### 1. Legal and Citation Infrastructure

| File | Purpose |
|------|---------|
| `LICENSE` | MIT License for code; enables open collaboration |
| `CITATION.cff` | Standardized citation metadata for academic use |
| `.zenodo.json` | Metadata for DOI assignment and long-term archiving |

**Impact:** Makes the research citable, legally clear, and archivable.

---

### 2. Reproducibility Infrastructure

| File | Purpose |
|------|---------|
| `.gitignore` | Prevents accidental commits of outputs, environments, sensitive data |
| `.pre-commit-config.yaml` | Automated quality checks (YAML validation, code formatting) |

**Impact:** Protects against common reproducibility failures.

---

### 3. Evidence and Documentation Infrastructure

| File | Purpose |
|------|---------|
| `context/evidence_grading_rubric.md` | Adapted GRADE framework for policy modelling evidence quality |
| `context/data_provenance_template.md` | Data lineage tracking from source to model inputs |
| `context/references.bib` | BibTeX bibliography organized by module |
| `context/decision_log.md` | Structured decision tracking with rationale and alternatives |

**Impact:** Transparent evidence-to-prior mapping; auditable decisions.

---

### 4. Validation and Quality Infrastructure

| File | Purpose |
|------|---------|
| `protocols/model_validation_protocol.md` | Face validity, internal/external validity, sensitivity analysis protocols |
| `docs/RESEARCH_QUALITY_CHECKLIST.md` | Pre-release checklist for publications and policy briefs |

**Impact:** Systematic validation before policy advice.

---

### 5. Updated Files

| File | Changes |
|------|---------|
| `README.md` | Expanded with research infrastructure overview, quick reference table, quality links |
| `conductor/tracks/gdpe_0002_evidence_anchoring/plan.md` | Added 10 new tasks across 5 phases (evidence grading, validation, dissemination) |

---

## Track Plan Updates

### gdpe_0002_evidence_anchoring — Updated Structure

**Phase 1 — Evidence registers** (5 tasks)
- Original: 3 tasks
- Added: Evidence grading rubric, citation management structure

**Phase 2 — Calibration targets and priors** (4 tasks)
- Original: 3 tasks
- Added: Evidence-to-prior mapping documentation

**Phase 3 — Identification plan and data access** (4 tasks)
- Original: 3 tasks
- Added: Data provenance documentation

**Phase 4 — Validation and verification** (4 tasks) — *NEW*
- Face validity protocol
- Cross-validation against literature
- Stress tests
- Posterior predictive checks

**Phase 5 — Research outputs and dissemination** (5 tasks) — *NEW*
- Evidence tables in publish pack
- "Evidence to priors" appendix
- CITATION.cff
- Zenodo metadata
- Methods section for journal submission

**Total:** 22 tasks (was 12)

---

## Alignment with Research Standards

These improvements align with:

| Standard | Implementation |
|----------|----------------|
| **FAIR data principles** | Data provenance templates, versioning, checksums |
| **ISPOR-SMDM good practices** | Validation protocol, decision log, assumption registry |
| **CHEERS 2022** | Reporting checklist integrated into quality checklist |
| **GRADE framework** | Evidence grading rubric adapted for modelling |
| **ASME V&V 40** | Model validation protocol (face, internal, external validity) |

---

## Next Steps

### Immediate (Phase 1)
1. Populate Australia evidence register using `context/jurisdiction_profiles/australia_life_insurance_evidence_template.md`
2. Grade each evidence item using `context/evidence_grading_rubric.md`
3. Add citations to `context/references.bib`

### Short-term (Phase 2-3)
1. Define calibration targets with uncertainty ranges
2. Convert evidence to prior distributions (document rationale)
3. Document data provenance for all input datasets

### Medium-term (Phase 4)
1. Recruit 2-3 experts for face validity review
2. Run extreme condition tests
3. Cross-validate against published AU/NZ studies

### Long-term (Phase 5)
1. Submit to Zenodo for DOI
2. Draft methods paper
3. Prepare policy brief pack

---

## File Locations Quick Reference

```
Repository root
├── LICENSE
├── CITATION.cff
├── .zenodo.json
├── .gitignore
├── .pre-commit-config.yaml
│
├── context/
│   ├── evidence_grading_rubric.md
│   ├── data_provenance_template.md
│   ├── references.bib
│   ├── decision_log.md
│   └── jurisdiction_profiles/
│       ├── australia_*_evidence_template.md
│       └── new_zealand_*_evidence_template.md
│
├── protocols/
│   ├── OSF_Presubmission_Protocol_v1.0.*
│   └── model_validation_protocol.md
│
├── docs/
│   ├── RESEARCH_QUALITY_CHECKLIST.md
│   ├── RUNBOOK.md
│   └── [other documentation]
│
└── conductor/
    └── tracks/
        └── gdpe_0002_evidence_anchoring/
            ├── plan.md (updated)
            ├── spec.md
            ├── index.md
            └── metadata.json
```

---

## Notes for Collaborators

This infrastructure is **research-first, software-second**. The tools exist to support:
1. Transparent evidence synthesis
2. Reproducible modelling
3. Credible policy advice
4. Publishable methods

If any component feels burdensome, discuss simplification — but don't skip validation or evidence documentation.

---

## References

- Guyatt GH, et al. GRADE: An emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336:924-926.
- Eddy DM, et al. ISPOR-SMDM Modeling Good Practices Task Force. Value Health. 2012;15(6):839-842.
- Husereau D, et al. Consolidated Health Economic Evaluation Reporting Standards (CHEERS) 2022. Value Health. 2022;25(1):3-9.
- ASME. V&V 40-2018: Assessing Credibility of Computational Modeling through Verification and Validation. 2018.
