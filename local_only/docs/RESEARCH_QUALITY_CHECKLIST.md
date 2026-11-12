# Research Quality Checklist

Use this checklist before releasing outputs, submitting for publication, or sharing with policy stakeholders.

---

## Documentation

- [ ] **Product definition** is up to date (`conductor/product.md`)
- [ ] **Tech stack** documented (`conductor/tech-stack.md`)
- [ ] **Workflow** documented (`conductor/workflow.md`)
- [ ] **Runbook** includes all new scripts (`docs/RUNBOOK.md`)
- [ ] **Decision log** captures key modelling choices (`context/decision_log.md`)
- [ ] **Assumptions registry** is complete (`context/assumptions_registry.yaml`)
- [ ] **Evidence registers** populated for all modules (`context/jurisdiction_profiles/`)
- [ ] **Data provenance** documented for all datasets (`context/data_provenance_template.md`)

---

## Code Quality

- [ ] All new code passes `ruff check` and `ruff format`
- [ ] Docstrings added for public functions and classes
- [ ] Type hints added where appropriate
- [ ] Random seeds set for reproducibility
- [ ] No hardcoded paths or credentials
- [ ] Config-driven parameters (not in code)

---

## Testing

- [ ] Unit tests added for new modules
- [ ] Tests pass: `pytest -q`
- [ ] Integration test run for full pipeline
- [ ] Extreme condition tests documented
- [ ] Reproducibility verified (same seed → same output)

---

## Evidence and Calibration

- [ ] All parameters sourced from evidence register
- [ ] Evidence quality graded using GRADE rubric (`context/evidence_grading_rubric.md`)
- [ ] Prior distributions justified with citations
- [ ] Calibration targets documented
- [ ] Calibration results within acceptable bounds (±20%)

---

## Validation

- [ ] Face validity review completed (≥2 experts)
- [ ] Internal validity checks passed
- [ ] External validity compared to published literature
- [ ] Sensitivity analysis completed:
  - [ ] One-way sensitivity (tornado diagram)
  - [ ] Probabilistic sensitivity (≥1000 draws)
  - [ ] Scenario analysis (structural assumptions)
- [ ] Value of information computed (EVPI/EVPPI)
- [ ] Validation report completed (`protocols/model_validation_protocol.md`)

---

## Reproducibility

- [ ] Run manifest generated (config + git hash + timestamp)
- [ ] All outputs versioned
- [ ] Dependencies pinned or version ranges specified
- [ ] Python version specified (≥3.10)
- [ ] Installation instructions tested
- [ ] Example commands documented and tested

---

## Data Governance

- [ ] Data use agreements in place (if required)
- [ ] Ethics approval covers intended use
- [ ] Privacy impact assessment completed (if needed)
- [ ] De-identification verified (if individual-level data)
- [ ] Synthetic exemplars generated for restricted data
- [ ] File checksums recorded

---

## Outputs

- [ ] All figures have:
  - [ ] Descriptive titles
  - [ ] Labeled axes with units
  - [ ] Uncertainty intervals shown
  - [ ] Colorblind-safe palette
  - [ ] Source/citation if adapted
- [ ] Tables have:
  - [ ] Clear column headers
  - [ ] Units specified
  - [ ] Notes on methods
- [ ] Policy brief includes:
  - [ ] Executive summary (≤1 page)
  - [ ] Key findings with uncertainty
  - [ ] Limitations
  - [ ] Recommendations with caveats

---

## Publication Readiness

- [ ] CITATION.cff up to date
- [ ] Zenodo metadata prepared (`.zenodo.json`)
- [ ] LICENSE file present
- [ ] README includes:
  - [ ] Installation instructions
  - [ ] Quick start guide
  - [ ] Example outputs
  - [ ] Citation guidance
- [ ] Methods section drafted for journal submission
- [ ] Reporting guidelines followed:
  - [ ] CHEERS 2022 (economic evaluations)
  - [ ] ISPOR-SMDM good practices
  - [ ] PRISMA (if systematic review component)

---

## Stakeholder Review

- [ ] Technical appendix prepared for expert reviewers
- [ ] Policy brief prepared for decision makers
- [ ] Plain language summary for public communication
- [ ] Media Q&A prepared (if applicable)
- [ ] Māori translation considered (for NZ outputs)

---

## Version Control

- [ ] Git repository clean (no uncommitted changes)
- [ ] Version tag created (semantic versioning)
- [ ] CHANGELOG updated (if applicable)
- [ ] GitHub release drafted (if applicable)

---

## Sign-off

**Lead researcher:** _________________ Date: _______

**Co-authors/reviewers:** _________________ Date: _______

**Intended use:**
- [ ] Internal working paper
- [ ] Peer-reviewed publication
- [ ] Policy brief for government
- [ ] Public release
- [ ] Conference presentation

**Notes:**
