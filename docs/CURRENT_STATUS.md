# Current Status

**Last updated:** 2026-03-07  
**Current track:** none  
**Most recently completed track:** gdpe_0021_manuscript_harmonization_and_submission_pack  
**Next planned track:** none

---

## Repository State

- Conductor registry milestone status remains: **14 archived milestone tracks complete**, but the later review work has superseded the old publication-ready baseline claim.
- The repository also contains a substantial **post-milestone dirty working tree** across `src/`, `scripts/`, `streamlit_app/`, `tests/`, and packaging files.
- The dirty working tree has been classified into explicit follow-on tracks; `gdpe_0016_repo_hardening`, `gdpe_0017_reporting_pipeline`, `gdpe_0018_dashboard_alignment`, `gdpe_0019_review_and_author_metadata`, `gdpe_0020_dashboard_policy_alignment_and_publication_sync`, and `gdpe_0021_manuscript_harmonization_and_submission_pack` are complete.

---

## Reporting Outcome

1. Reporting scripts now share a coherent meta-pipeline/run-directory contract through `scripts/reporting_common.py`.
2. Table generation, figure generation, and publish-pack generation now read the same policy-summary and uncertainty inputs instead of mixing live logic with hardcoded template data.
3. Validation and policy-brief outputs were tightened so PPC results serialize with summaries and report formatting remains human-readable.
4. A synthetic smoke suite now verifies reporting-table, reporting-figure, and publish-pack outputs from representative run-directory fixtures.
5. The stray `$null` artifact has been removed from the repository root.

The reporting surface is now on a stronger footing for manuscript work:
- `publish_pack` narrative is data-driven and path-safe;
- PDF/DOCX/Markdown artifacts are generated from the same reporting bundle;
- uncertainty-decomposition figures and caption files are generated on the active path.

The remaining reporting work is now concentrated in manuscript asset inventory, caption consistency across older materials, and reviewer-facing packaging rather than active-path functionality.

---

## Dashboard Alignment Outcome

1. `gin-sim/` is now explicitly classified as a deployment wrapper for `streamlit_app/app.py`, not a second independently maintained dashboard.
2. The public `gin-sim/app.py` entrypoint now executes the canonical dashboard app instead of shipping a divergent hardcoded UI.
3. Dashboard-only logic moved into `streamlit_app/dashboard_helpers.py`, which now backs the Scenario Sandbox evaluation and the Delta View positive-share summary.
4. The Scenario Sandbox no longer uses placeholder formulas; it now evaluates a custom policy through the core policy pipeline.
5. The minimum dashboard smoke suite is now defined in `gin-sim/README.md`, and the remote Playwright check is opt-in via `GDPE_REMOTE_DASHBOARD_URL`.

The dashboard active path is now aligned enough for reviewer-facing interpretation:
- the landing page uses the canonical `status_quo` / `moratorium` / `ban` comparator set and includes plain-language guidance;
- scenario-field activation and calibrated-versus-exploratory labeling are hardened on the main scenario pages;
- remaining work is now mostly document/manuscript harmonization rather than dashboard computation.

---

## Verified Checks

- `ruff check scripts/reporting_common.py scripts/generate_tables.py scripts/generate_figures.py scripts/publish_pack.py src/model/output_formatter.py src/model/validation.py tests/unit/test_reporting_pipeline.py` passes.
- `pyright scripts/reporting_common.py scripts/generate_tables.py scripts/generate_figures.py scripts/publish_pack.py src/model/output_formatter.py src/model/validation.py tests/unit/test_reporting_pipeline.py` passes with 0 errors.
- `pytest tests/unit/test_reporting_pipeline.py` passes.
- `pytest tests/unit/test_module_enforcement.py tests/integration/test_pipeline.py tests/unit/test_reporting_pipeline.py` passes directly.
- `pytest tests/integration/test_pipeline.py` passes.
- `pytest tests/unit/test_reporting_pipeline.py` passes.
- `pytest tests/unit/test_dashboard_helpers.py tests/model/test_scenario_analysis.py tests/e2e/test_dashboard_pages.py` passes with `20 passed`.

---

## Classified Follow-on Tracks

The current dirty working tree remains split into explicit follow-on tracks:

1. `gdpe_0015_reconciliation` is now complete.
2. `gdpe_0016_repo_hardening` is now complete.
3. `gdpe_0017_reporting_pipeline` is now complete.
4. `gdpe_0018_dashboard_alignment` is now complete.
5. `gdpe_0019_review_and_author_metadata` is now complete.
6. `gdpe_0020_dashboard_policy_alignment_and_publication_sync` is complete.
7. `gdpe_0021_manuscript_harmonization_and_submission_pack` is complete.

---

## Working Tree Snapshot

- Modified tracked files still span model core, output generation, Streamlit UI, scripts, and project configuration.
- Untracked additions currently include new reporting/dashboard helper modules and focused unit tests.
- The working tree therefore represents active development rather than a clean publication-ready checkout.
- Hardening baseline results at closure: the original baselines were `ruff check .` with 824 findings and `pyright src` with 83 errors; the closing baseline is `ruff check .` with 440 findings, `ruff format --check .` passing, and `pyright src` with 0 errors.
- The remaining Ruff debt is now concentrated in a smaller set of non-blocking structural refactor candidates outside the now-closed reporting and dashboard alignment tracks.
- Runtime verification is no longer blocked. The enforcement and pipeline path now passes focused unit/integration pytest runs directly.
- The dashboard and `gin-sim` follow-on surface is no longer classified as a standalone open track, and the remaining reviewer-facing cleanup has moved into `gdpe_0021`.

---

## Reconciliation Notes

- The reconciliation track normalized stale status records and promoted the current work into explicit follow-on tracks.
- The reporting and dashboard follow-on tracks are closed as standalone tracks, but their remaining publication-readiness debt is now consolidated into `gdpe_0020`.

---

## Next Review Point

There is no currently active follow-up track. Use the reviewer navigation map, manuscript asset inventory, and submission-gap register as the main reviewer-facing orientation surfaces for the current repository state.
