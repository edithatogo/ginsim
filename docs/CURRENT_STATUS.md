# Current Status

**Last updated:** 2026-03-06  
**Current track:** gdpe_0016_repo_hardening  
**Current phase:** Phase 3 - Verification

---

## Repository State

- Conductor registry milestone status remains: **14 completed tracks** and **publication-ready baseline achieved**.
- The repository also contains a substantial **post-milestone dirty working tree** across `src/`, `scripts/`, `streamlit_app/`, `tests/`, and packaging files.
- The dirty working tree has been classified and the next active implementation track is now `gdpe_0016_repo_hardening`.

---

## Current Objectives

1. Stabilize the expanded Ruff, typing, and automation baseline.
2. Separate mechanical hardening edits from behavior-affecting code changes.
3. Use the hardening findings to reduce ambiguity before `gdpe_0017` and `gdpe_0018`.
4. Preserve all existing files; no deletions are permitted in this pass.

---

## Hardening Triage

- Mechanical hardening candidates are now identified across examples, many tests, and several page-level formatting edits.
- High-risk semantic candidates are concentrated in `src/model/rng.py`, `src/model/module_a_behavior_wrappers.py`, `src/model/extended_games.py`, `src/model/module_c_insurance_eq.py`, `src/model/sensitivity.py`, `src/model/sensitivity_total.py`, and `src/model/voi_analysis.py`.
- Reporting-oriented files have been explicitly deferred to `gdpe_0017_reporting_pipeline`.
- Dashboard/test/mirror files have been explicitly deferred to `gdpe_0018_dashboard_alignment`.
- Seven low-risk hardening tranches have now been cleaned, the full `tests/` tree is Ruff-clean, multiple touched runner-script tranches are now either Ruff-clean or reduced to structural-only warnings, and the model typing hardening pass now leaves `pyright src` at 0 errors.

---

## Classified Follow-on Tracks

The current dirty working tree has been split into three follow-on tracks:

1. `gdpe_0015_reconciliation` is now complete.
2. `gdpe_0016_repo_hardening` is active.
3. `gdpe_0017_reporting_pipeline` remains planned.
4. `gdpe_0018_dashboard_alignment` remains planned.

---

## Working Tree Snapshot

- Modified tracked files still span model core, output generation, Streamlit UI, scripts, and project configuration.
- Untracked additions currently include `noxfile.py`, `gin-sim/`, and test package markers.
- The working tree therefore represents active development rather than a clean publication-ready checkout.
- Hardening baseline results so far: the original baselines were `ruff check .` with 824 findings and `pyright src` with 83 errors; the current re-scoped baseline is `ruff check .` with 721 findings and `pyright src` with 0 errors. Subsequent cleanup eliminated the remaining Ruff issues under `tests/`, cleaned several runner scripts outright, reduced the `run_full_uncertainty*` pair to structural Ruff warnings only, and cleared both lower-risk and higher-risk model typing slices.
- Runtime verification remains partially open: targeted `pytest` required overriding repo `addopts` because `pytest-xdist` is unavailable in the current environment, and the resulting focused test run still exposes JAX/beartype compatibility failures in the enforcement and pipeline path.

---

## Reconciliation Notes

- The reconciliation track normalized stale status records and promoted the current work into explicit follow-on tracks.
- The next active effort is now the repo-hardening baseline rather than further Conductor restructuring.

---

## Next Review Point

After `gdpe_0016_repo_hardening` resolves the remaining runtime verification failures in the enforcement and pipeline path, or explicitly splits those runtime repairs into a dedicated follow-up task.
