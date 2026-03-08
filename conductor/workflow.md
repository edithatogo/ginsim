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

## Autonomous phase-loop mode

For tracks that explicitly opt in, phase execution should run as an autonomous loop:

1. Complete the current phase tasks.
2. Run the Conductor review protocol from the skill definition at `commands/conductor/review.toml`, adapted to the current track/phase scope.
3. Persist a phase review artifact at `conductor/tracks/<track_id>/phase_<N>_review.md`.
4. Automatically implement in-scope review recommendations.
5. Re-run the same phase review until:
   - no critical or high findings remain; and
   - any remaining medium/low findings are either fixed or explicitly documented as deferred.
6. Only then mark the phase complete and move to the next phase.

Autonomous phase-loop mode does not override judgment:
- Do not auto-apply recommendations that are out of scope for the track.
- Do not auto-apply recommendations that would require destructive repo changes or conflict with unreviewed user edits.
- If a finding implies a scope expansion, first update the track spec/plan so the new work is explicit.

Tracks using this mode should say so in their `spec.md`, `plan.md`, and `index.md`.

## Nature-depth chained-track template

For repository-hardening work that should proceed one aspect at a time, use the template at `conductor/templates/nature_depth_cycle/`.

This template adds five operating rules beyond the standard autonomous phase loop:

1. **Deep aspect audit first:** one track should focus on one repository aspect and explore it in depth before implementation starts.
2. **Nature-grade standard:** the aspect must be judged against publication-grade sophistication, completeness, traceability, clarity, and deployment robustness.
3. **Track hardening rounds:** before implementation, run 3 to 5 refinement rounds asking whether the track itself should be improved, then incorporate those improvements.
4. **Remote closure gate:** after local verification, push the change, monitor workflows for the pushed commit, and verify the Streamlit dashboard locally and remotely where configured.
5. **Chained progression:** the close-out of one track should assess flow-on effects and create the next follow-on track if material work remains.

The template is written to be portable across Codex, Gemini CLI, and Qwen Code:

- use stable markdown and JSON artifacts;
- avoid agent-specific slash-command assumptions;
- keep handoff state in files rather than transient chat only.

Recommended instantiation path:

```bash
python -m scripts.create_nature_depth_track \
  --track-id <track_id> \
  --title "<title>" \
  --aspect "<single_repo_aspect>" \
  --status planned
```

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
