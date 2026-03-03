# Runbook

## Quick Start

```bash
# Setup
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev,validation]"

# Run calibration
python -m scripts.run_calibration --jurisdiction australia --n_draws 2000

# Run policy evaluation
python -m scripts.run_policy_sweep --jurisdiction australia

# Validate references
python -m scripts.validate_references --report
```

---

## 1) Configure the jurisdiction and policy rules

- Choose a jurisdiction (`australia` or `new_zealand`).
- Use `configs/policies_australia.yaml` or `configs/policies_new_zealand.yaml`.
- Update / validate the matching profile in `context/jurisdiction_profiles/`.

**Calibration configs (Phase 2 complete):**
- `configs/calibration_australia.yaml` — AU prior distributions
- `configs/calibration_new_zealand.yaml` — NZ prior distributions

---

## 2) Define data schemas

- Fill out `context/data_dictionary_template.md` for each dataset.
- Implement ETL into `data/processed/` (not included in scaffold).

**Data provenance (Phase 3):**
- Use `context/data_provenance_template.md` for lineage tracking
- Document all transformations with checksums

---

## 3) Calibration Workflow (NEW)

### Step 1: Load Evidence Registers

```python
import yaml
from pathlib import Path

# Load Australia evidence register
with open('context/jurisdiction_profiles/australia_evidence_register.yaml') as f:
    au_evidence = yaml.safe_load(f)

# Load calibration config
with open('configs/calibration_australia.yaml') as f:
    au_calibration = yaml.safe_load(f)
```

### Step 2: Extract Priors

```python
# Example: Extract Module A priors
module_a = au_calibration['module_a_calibration']['parameters']

baseline_uptake = module_a['baseline_testing_uptake']['prior']
# Returns: {'distribution': 'Beta', 'parameters': {'alpha': 462, 'beta': 426}, ...}
```

### Step 3: Generate Prior Draws

```python
import numpy as np
from scipy.stats import beta, norm

# Draw from Beta prior
draws = beta.rvs(
    a=baseline_uptake['parameters']['alpha'],
    b=baseline_uptake['parameters']['beta'],
    size=2000,
    random_state=20260303
)
```

### Step 4: Prior Predictive Check (Phase 4)

```python
# Simulate model with prior draws
# Compare to empirical targets
# Adjust if necessary
```

### Step 5: Save Run Manifest

```json
{
  "timestamp": "2026-03-03T14:00:00+13:00",
  "jurisdiction": "australia",
  "config_hash": "abc123...",
  "git_commit": "def456...",
  "n_draws": 2000,
  "priors_version": "1.0"
}
```

---

## 4) Fit modules

- Use NumPyro/BlackJAX in `src/inference/` (to be implemented for your data).
- Store posterior draws in `outputs/posterior_samples/` with run manifests.

---

## 5) Run policy evaluation

- `python -m scripts.run_policy_sweep`
- `python -m scripts.run_voi`

---

## 6) Validation and Quality (NEW)

### Reference Validation

```bash
# Full validation with report
python -m scripts.validate_references --report

# Auto-fix common issues
python -m scripts.validate_references --fix

# Include DOI resolution check (slow)
python -m scripts.validate_references --doi-check
```

### Code Quality

```bash
# Lint
ruff check src/ scripts/

# Format
ruff format src/ scripts/

# Type checking (optional)
mypy src/
```

### Tests (when implemented)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_calibration.py
```

---

## 7) Record assumptions and decisions

- Update `context/assumptions_registry.yaml` and `context/decision_log.md`.
- Create an experiment card for each major run.

**Decision logging:**
- Document decisions when choosing between viable options
- Use template in `context/decision_log.md`
- Update at end of each phase

---

## 8) Phase Review Workflow (NEW)

At the end of each phase:

### Step 1: Complete Phase Tasks
- Ensure all tasks in the phase are marked `[x]`
- Verify all acceptance criteria are met

### Step 2: Run Automated Checks
```bash
# Reference validation (required)
python -m scripts.validate_references --report

# Code quality (if code changes)
ruff check src/ scripts/
ruff format src/ scripts/ --check

# Tests (if applicable)
pytest -q
```

### Step 3: Update Decision Log
- Add any decisions made during the phase to `context/decision_log.md`
- Ensure rationale and alternatives are documented

### Step 4: Generate Phase Review Report
Create `conductor/tracks/<track_id>/phase_<N>_review.md`:

```markdown
# Phase N Review

**Track:** <track_id>  
**Review date:** YYYY-MM-DD

## Checklist
- [ ] All phase tasks completed
- [ ] Acceptance criteria met
- [ ] Reference validation passed
- [ ] Decision log updated

## Issues Found
[List any issues, warnings, or recommendations]

## Recommendation
[ ] Proceed to next phase
[ ] Proceed with minor revisions
[ ] Requires major revisions
```

### Step 5: Sign-off and Proceed
- Mark phase review task as `[x]`
- Update track metadata (`metadata.json`) with phase completion
- Proceed to next phase

---

## Troubleshooting

### Common Issues

**Issue:** Reference validation fails  
**Solution:** Run `python -m scripts.validate_references --fix`

**Issue:** Import errors  
**Solution:** `pip install -e ".[dev,validation]"`

**Issue:** Calibration config not found  
**Solution:** Check `configs/calibration_*.yaml` exists

---

## Related Documentation

- `docs/IDENTIFICATION_PLAN.md` — Data sources and identification strategies
- `docs/DATA_ACCESS_GOVERNANCE.md` — Ethics and governance requirements
- `docs/EVIDENCE_TO_PRIOR_MAPPING.md` — Calibration rationale
- `context/data_provenance_template.md` — Data lineage tracking
- `conductor/workflow.md` — Conductor workflow procedures

---

**Last updated:** 2026-03-03  
**Version:** 2.0 (Phase 3 update)
