# Infrastructure Improvements Summary

**Date:** 3 March 2026  
**Track:** gdpe_0002_evidence_anchoring (Infrastructure Phase)

---

## Overview

This document summarizes all research infrastructure improvements made to strengthen reproducibility, validation, and quality assurance for the genetic discrimination policy economics research project.

---

## Files Created

### 1. Humanizer-next Extension (`.qwen/extensions/humanizer-next/`)

| File | Purpose |
|------|---------|
| `GEMINI.md` | Extension documentation with commands for `/humanize`, `/check-references`, `/polish-paragraph` |
| `config.yaml` | Configuration for tone, audience, reference validation settings |

**Purpose:** Provides academic writing refinement and automated reference validation integrated with Conductor phase reviews.

---

### 2. Reference Validation Pipeline (`scripts/validate_references.py`)

**Features:**
- Validates BibTeX completeness (required fields by entry type)
- DOI format validation
- Duplicate detection (by DOI and title similarity)
- Citation usage tracking (finds citations in project files)
- Orphaned entry detection (in bib but not cited)
- Missing citation detection (cited but not in bib)
- Auto-fix common issues (DOI prefixes, year brackets)
- Generates markdown validation reports

**Usage:**
```bash
# Full validation with report
python -m scripts.validate_references --report

# Auto-fix common issues
python -m scripts.validate_references --fix

# Include DOI resolution check (slow)
python -m scripts.validate_references --doi-check
```

**Dependencies:** Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
validation = [
  "bibtex-tidy>=1.0",
  "bibtexparser>=1.4",
  "requests>=2.31",
  "habanero>=1.2",
]
```

---

### 3. Product Guidelines (`conductor/product-guidelines.md`)

**Sections:**
- Voice and tone (academic, policy, public audiences)
- Writing principles (evidence-first, transparent uncertainty, comparative framing)
- Document-specific guidelines (papers, briefs, reports, presentations)
- Visual design (colorblind-safe palettes, figure/table standards)
- Naming and terminology (preferred terms, acronyms)
- Citation and attribution standards
- Ethics and positionality guidance
- Review and quality assurance checklist

**Purpose:** Defines communication style and branding for all research outputs. Required for Conductor synchronization step.

---

### 4. Phase Review Template (`conductor/phase_review_template.md`)

**Components:**
- Phase completion checklist
- Automated check results sections
- Issues and recommendations
- Artifacts produced table
- Review decision (proceed/revise/block)
- Next phase preparation

**Purpose:** Standardized template for phase gate reviews, ensuring consistent quality checks before proceeding.

---

## Files Modified

### 1. Track Plan (`conductor/tracks/gdpe_0002_evidence_anchoring/plan.md`)

**Changes:**
- Added track metadata (ID, type, duration, dependencies)
- Added goal, estimated duration, and acceptance criteria for each phase
- Added phase review gate tasks at end of each phase:
  - Phase 1 review: Run reference validation and quality check
  - Phase 2 review: Validate priors against evidence and run smoke test
  - Phase 3 review: Verify data provenance completeness
  - Phase 4 review: Validation report sign-off
  - Phase 5 review: Final quality check and reference validation
  - Track complete: All phases signed off
- Marked completed tasks (CITATION.cff, Zenodo metadata, evidence rubric, citation structure)

---

### 2. Workflow (`conductor/workflow.md`)

**Changes:**
- Added principle #6: "Phase gates: each phase requires review and validation before proceeding"
- Added complete "Phase review workflow" section with 6 steps:
  1. Complete phase tasks
  2. Run automated checks (reference validation, code quality, tests)
  3. Humanizer-next quality check
  4. Generate phase review report
  5. Address recommendations
  6. Sign-off and proceed
- Added validation and quality commands to minimal development commands

---

### 3. Dependencies (`pyproject.toml`)

**Changes:**
- Added `[project.optional-dependencies.validation]` section
- Dependencies: bibtex-tidy, bibtexparser, requests, habanero

---

## Integration with Conductor

### Automatic Phase Review Flow

1. **Complete Phase Tasks** → Mark all as `[x]`
2. **Run Validation** → `python -m scripts.validate_references --report`
3. **Generate Report** → Create `conductor/tracks/<track_id>/phase_<N>_review.md`
4. **Address Issues** → Fix critical blockers
5. **Update Metadata** → Set phase complete in `metadata.json`
6. **Proceed to Next Phase**

### Human-in-the-Loop Points

The workflow requires user confirmation at:
- Phase review sign-off (expert review for Phase 4)
- Critical issue resolution (if validation fails)
- Final track completion

---

## Usage Guide

### Starting a Phase

1. Open `conductor/tracks/gdpe_0002_evidence_anchoring/plan.md`
2. Find first incomplete task in current phase
3. Mark as `[~]` (in progress)
4. Implement task
5. Mark as `[x]` (complete)
6. Repeat until all phase tasks complete

### Completing a Phase

1. Verify all acceptance criteria met
2. Run: `python -m scripts.validate_references --report`
3. Copy output to phase review template
4. Fill in checklist and artifacts
5. If validation fails: fix issues and re-run
6. Sign off and proceed to next phase

### Reference Validation

Run before any public output:

```bash
cd "Project - 2026.03 - Economics and Genetic Discrimination"
python -m scripts.validate_references --report --fix
```

Review `docs/REFERENCE_VALIDATION_REPORT.md` for issues.

---

## Next Steps

### Immediate (Phase 1)

1. **Populate Australia evidence register**
   - Use template: `context/jurisdiction_profiles/australia_life_insurance_evidence_template.md`
   - Grade evidence using: `context/evidence_grading_rubric.md`
   - Add citations to: `context/references.bib`

2. **Run first reference validation**
   ```bash
   python -m scripts.validate_references --report
   ```

3. **Complete Phase 1 review**
   - Fill out: `conductor/tracks/gdpe_0002_evidence_anchoring/phase_1_review.md`
   - Mark phase review task as complete

### Short-term

- Install validation dependencies: `pip install -e ".[validation]"`
- Set up pre-commit hooks: `pre-commit install`
- Configure humanizer-next in Gemini CLI extensions

---

## Commit Message Template

When ready to commit these changes:

```bash
git add .qwen/
git add scripts/validate_references.py
git add conductor/product-guidelines.md
git add conductor/phase_review_template.md
git add conductor/tracks/gdpe_0002_evidence_anchoring/plan.md
git add conductor/workflow.md
git add pyproject.toml

git commit -m "feat(infrastructure): Add humanizer-next, reference validation, and phase review gates

- Create .qwen/extensions/humanizer-next/ for academic writing refinement
- Add scripts/validate_references.py for BibTeX validation and DOI checking
- Add conductor/product-guidelines.md for communication standards
- Add phase review workflow with mandatory quality gates
- Update track plan with acceptance criteria and review tasks
- Add validation dependencies to pyproject.toml

Part of gdpe_0002_evidence_anchoring track."
```

---

## File Inventory

### New Files (11)
1. `.qwen/extensions/humanizer-next/GEMINI.md`
2. `.qwen/extensions/humanizer-next/config.yaml`
3. `scripts/validate_references.py`
4. `conductor/product-guidelines.md`
5. `conductor/phase_review_template.md`
6. `context/evidence_grading_rubric.md` (created earlier)
7. `context/data_provenance_template.md` (created earlier)
8. `context/references.bib` (created earlier)
9. `protocols/model_validation_protocol.md` (created earlier)
10. `docs/RESEARCH_QUALITY_CHECKLIST.md` (created earlier)
11. `docs/RESEARCH_INFRASTRUCTURE_IMPROVEMENTS.md` (created earlier)

### Modified Files (4)
1. `conductor/tracks/gdpe_0002_evidence_anchoring/plan.md`
2. `conductor/workflow.md`
3. `pyproject.toml`
4. `README.md`

### Supporting Files (created earlier)
- `LICENSE`
- `CITATION.cff`
- `.zenodo.json`
- `.gitignore`
- `.pre-commit-config.yaml`

---

## Questions?

For issues or questions about this infrastructure:
1. Check `conductor/workflow.md` for phase review procedures
2. See `scripts/validate_references.py --help` for validation options
3. Review `conductor/product-guidelines.md` for writing standards
4. Consult `docs/RESEARCH_QUALITY_CHECKLIST.md` before releases
