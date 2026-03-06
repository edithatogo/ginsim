# Current Status

**Last updated:** 2026-03-06  
**Current track:** none active  
**Most recently completed track:** gdpe_0018_dashboard_alignment  
**Next planned track:** none

---

## Repository State

- Conductor registry milestone status remains: **14 archived milestone tracks complete** and **publication-ready baseline achieved**.
- The repository also contains a substantial **post-milestone dirty working tree** across `src/`, `scripts/`, `streamlit_app/`, `tests/`, and packaging files.
- The dirty working tree has been classified into explicit follow-on tracks; `gdpe_0016_repo_hardening`, `gdpe_0017_reporting_pipeline`, and `gdpe_0018_dashboard_alignment` are now complete.

---

## Reporting Outcome

1. Reporting scripts now share a coherent meta-pipeline/run-directory contract through `scripts/reporting_common.py`.
2. Table generation, figure generation, and publish-pack generation now read the same policy-summary and uncertainty inputs instead of mixing live logic with hardcoded template data.
3. Validation and policy-brief outputs were tightened so PPC results serialize with summaries and report formatting remains human-readable.
4. A synthetic smoke suite now verifies reporting-table, reporting-figure, and publish-pack outputs from representative run-directory fixtures.
5. The stray `$null` artifact has been removed from the repository root.

---

## Dashboard Alignment Outcome

1. `gin-sim/` is now explicitly classified as a deployment wrapper for `streamlit_app/app.py`, not a second independently maintained dashboard.
2. The public `gin-sim/app.py` entrypoint now executes the canonical dashboard app instead of shipping a divergent hardcoded UI.
3. Dashboard-only logic moved into `streamlit_app/dashboard_helpers.py`, which now backs the Scenario Sandbox evaluation and the Delta View positive-share summary.
4. The Scenario Sandbox no longer uses placeholder formulas; it now evaluates a custom policy through the core policy pipeline.
5. The minimum dashboard smoke suite is now defined in `gin-sim/README.md`, and the remote Playwright check is opt-in via `GDPE_REMOTE_DASHBOARD_URL`.

---

## Verified Checks

- `ruff check scripts/reporting_common.py scripts/generate_tables.py scripts/generate_figures.py scripts/publish_pack.py src/model/output_formatter.py src/model/validation.py tests/unit/test_reporting_pipeline.py` passes.
- `pyright scripts/reporting_common.py scripts/generate_tables.py scripts/generate_figures.py scripts/publish_pack.py src/model/output_formatter.py src/model/validation.py tests/unit/test_reporting_pipeline.py` passes with 0 errors.
- `pytest tests/unit/test_reporting_pipeline.py` passes.
- `pytest tests/unit/test_module_enforcement.py tests/integration/test_pipeline.py tests/unit/test_reporting_pipeline.py` passes directly.
- `pytest tests/unit/test_dashboard_helpers.py tests/unit/test_gin_sim_wrapper.py tests/e2e/test_dashboard.py tests/e2e/test_remote_app.py` passes with `14 passed, 1 skipped`.

---

## Classified Follow-on Tracks

The current dirty working tree remains split into explicit follow-on tracks:

1. `gdpe_0015_reconciliation` is now complete.
2. `gdpe_0016_repo_hardening` is now complete.
3. `gdpe_0017_reporting_pipeline` is now complete.
4. `gdpe_0018_dashboard_alignment` is now complete.

---

## Working Tree Snapshot

- Modified tracked files still span model core, output generation, Streamlit UI, scripts, and project configuration.
- Untracked additions currently include new reporting/dashboard helper modules and focused unit tests.
- The working tree therefore represents active development rather than a clean publication-ready checkout.
- Hardening baseline results at closure: the original baselines were `ruff check .` with 824 findings and `pyright src` with 83 errors; the closing baseline is `ruff check .` with 440 findings, `ruff format --check .` passing, and `pyright src` with 0 errors.
- The remaining Ruff debt is now concentrated in a smaller set of non-blocking structural refactor candidates outside the now-closed reporting and dashboard alignment tracks.
- Runtime verification is no longer blocked. The enforcement and pipeline path now passes focused unit/integration pytest runs directly.
- The dashboard and `gin-sim` follow-on surface is no longer classified as an open track; remote deployment validation remains an explicit opt-in check rather than a mandatory local test.

---

## Reconciliation Notes

- The reconciliation track normalized stale status records and promoted the current work into explicit follow-on tracks.
- The reporting and dashboard follow-on tracks are closed; there is no remaining planned Conductor follow-up track from the current classified working tree.

---

## Next Review Point

When a new follow-on track is opened, using the now-stable lint/type/test configuration and the aligned reporting/dashboard contract established by `gdpe_0016_repo_hardening`, `gdpe_0017_reporting_pipeline`, and `gdpe_0018_dashboard_alignment`.
