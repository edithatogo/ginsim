# Project Workflow

## Guiding principles
1. **The plan is the source of truth:** all work must be tracked in `conductor/tracks/<track_id>/plan.md`.
2. **Config-driven:** prefer adding/adjusting YAML configs over hard-coded constants.
3. **Reproducibility:** deterministic seeds where possible; each run writes `run_manifest.json`.
4. **Evidence anchoring:** priors/assumptions must be logged in `context/jurisdiction_profiles/*`.
5. **Tests where it matters:** prioritise unit tests for core transforms, IO boundaries, and invariants.
6. **Phase gates:** each phase requires review and validation before proceeding.

## Task workflow (adapted for research repos)
Status codes:
- `[ ]` not started
- `[~]` in progress
- `[x]` done

Standard flow:
1. Select next `[ ]` task in the active track's plan.
2. Mark `[~]`.
3. Implement change.
4. Run relevant checks (tests, lint, smoke run).
5. Mark `[x]` and note key artifacts/outputs/paths.
6. Commit code changes + commit plan update.

## Phase review workflow

At the end of each phase, complete the following review:

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

## Minimal development commands
### Setup
```bash
python -m venv .venv
# Activate:
#   macOS/Linux: source .venv/bin/activate
#   Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

### Run key pipelines
```bash
python -m scripts.run_meta_pipeline --n_draws 500
python -m scripts.publish_pack --meta_dir outputs/runs/meta_pipeline/<timestamp>
```

### Validation and quality
```bash
# Reference validation
python -m scripts.validate_references --report

# Code quality
ruff check src/ scripts/
ruff format src/ scripts/

# Tests
pytest -q
```
