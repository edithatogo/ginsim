# Track Complete: gdpe_0019_review_and_author_metadata

**Completed:** 2026-03-06

## Outcome

`gdpe_0019_review_and_author_metadata` is complete.

This track produced a repository-level review of the core analytical surfaces, dashboard alignment, reporting outputs, and author metadata, then applied the requested author-name and affiliation corrections in the repository metadata and author-facing documents. It also fixed a reproduced JAX tracer failure in `src/model/voi.py` so the lightweight EVPPI helper is again compatible with `jax.vmap`.

## Prioritized Findings

### 1. High: The landing dashboard exposes a `Statutory Ban` policy path that does not exist in the canonical policy registry.

- `streamlit_app/app.py` maps the sidebar option `Statutory Ban` to `statutory_ban`, and then dereferences `STANDARD_POLICIES[selected_policy_id]`.
- The canonical policy registry in `src/model/module_a_behavior.py` exposes `status_quo`, `moratorium`, and `ban`, not `statutory_ban`.
- The same mismatch is repeated in the comparison loops on the landing page.

**Why this matters:** selecting `Statutory Ban`, or rendering any comparison path that touches that key, can fail at runtime and breaks the dashboard’s claim that all three benchmark policies are available from the source-of-truth model.

### 2. High: The Scenario Analysis and Comparative Delta pages present policy comparisons, but the underlying engine always evaluates the `status_quo` policy object.

- `src/model/scenario_analysis.py` constructs `ModelParameters` from scenario config, but then always fetches `status_quo` from `get_standard_policies()` and evaluates that policy regardless of the scenario name.
- Scenario YAML fields such as `enforcement_strength` and `penalty_rate` are defined under `configs/scenarios.yaml`, but they are not valid `ModelParameters` fields, so they are ignored in the fallback path.
- `streamlit_app/pages/3_Scenarios.py` and `streamlit_app/pages/5_Delta_View.py` therefore compare parameterized `status_quo` evaluations rather than true policy-regime comparisons.

**Why this matters:** these pages currently overstate their fidelity to the policy model. The labels imply Australia/NZ/international regime comparisons, but the implementation does not bind scenario definitions to the policy configuration layer.

### 3. High: The landing-page `Jurisdiction` selector is not wired into the model evaluation and the documentation panel still hardcodes Australian evidence.

- `streamlit_app/app.py` exposes a sidebar jurisdiction selector, but the `ModelParameters(...)` object built for evaluation does not include `jurisdiction`.
- The same page’s documentation tab always says the model is calibrated using the Australia evidence register, even when `New Zealand` is selected.

**Why this matters:** the UI implies a jurisdictional calibration switch, but current behavior is presentation-only. That is a direct alignment problem between the dashboard and the codebase.

### 4. Medium: The Extended Strategic Games page mixes real result fields with hardcoded illustrative values.

- In the Genetic Altruism section, the chart compares the result against a hardcoded `0.5` baseline rather than a baseline derived from the current parameterization.
- In the Cascade Testing section, `Estimated Detections` is computed from an inline formula rather than being surfaced by the underlying result object.

**Why this matters:** this weakens auditability and makes the page feel less trustworthy than the rest of the JAX-backed dashboard.

### 5. Medium: Dashboard automated coverage is concentrated on the landing page and helper smoke paths, leaving most page-specific alignment risks untested.

- `tests/e2e/test_dashboard.py` covers only `streamlit_app/app.py`.
- `tests/e2e/test_remote_app.py` is an opt-in title/heading smoke test, not a workflow-level deployment test.
- There is useful unit coverage for `streamlit_app/dashboard_helpers.py`, but no equivalent page-level tests for Scenarios, Sensitivity, Delta View, or Extended Games.

**Why this matters:** the current test surface is good enough to protect the wrapper and landing-page smoke path, but it does not protect the richer review findings above.

### 6. Medium: Reporting outputs are structurally coherent but still too generic for publication-facing narrative use.

- `scripts/publish_pack.py` now reuses the reporting bundle cleanly, but the executive-summary prose remains mostly template text rather than synthesizing the actual best policy, dominant uncertainty drivers, or jurisdiction-specific contrasts.
- `scripts/generate_figures.py` currently exposes net-benefit and EVPPI figures, but not a visual for the uncertainty decomposition table that the reporting pipeline already computes.

**Why this matters:** the artifact generation pipeline is reproducible, but readers still have to interpret the most important findings manually. That is acceptable for internal runs, but weak for a publication or policy-brief surface.

## UX and Dashboard Recommendations

### Plain-language explanation improvements

- Add a short “What this page answers” panel at the top of each page with 2-3 plain-language bullets.
- Add a glossary expander for terms such as deterrence elasticity, compliance rate, welfare impact, QALYs, pass-through, and Sobol indices.
- Add an “Interpret this chart” note below each major figure so non-methodologists can read directionality and meaning quickly.

### User-guide and workflow improvements

- Add a persistent “Suggested workflow” block on the landing page that tells users where to go next: core results, sensitivity, scenarios, delta view, then extended games.
- Add explicit provenance notes on scenario and delta pages stating whether outputs are benchmark policy comparisons, parameterized sandbox comparisons, or illustrative game outputs.
- Add warnings or badges wherever a page is exploratory or illustrative rather than fully policy-calibrated.

### Alignment improvements

- Unify dashboard labels with canonical policy IDs from the model layer so the UI cannot drift from the source-of-truth policy registry.
- Refactor the scenario engine so YAML scenarios bind both `ModelParameters` and `PolicyConfig`, rather than only passing through parameter subsets.
- Replace hardcoded illustrative baselines on Extended Games with derived baseline result objects or label them clearly as illustrative.
- Make publish-pack summaries data-driven so the brief narrative names the leading policy, interval width, and top uncertainty drivers instead of repeating static boilerplate.

## Verified Good Alignment

- `gin-sim/app.py` is now a clean deployment wrapper that executes `streamlit_app/app.py` and keeps the public deployment entrypoint aligned with the canonical dashboard source.
- `streamlit_app/dashboard_helpers.py` is a good move toward shared, testable dashboard logic for sandbox evaluation and summary formatting.
- Repository author metadata and main author-facing docs now use the requested `Dylan A Mordaunt` and `Research Fellow, Faculty of Health, Education and Psychology, Victoria University of Wellington` attribution.

## Verification

- `pytest tests/integration/test_pipeline.py tests/model/test_scenario_analysis.py tests/test_voi.py tests/unit/test_reporting_pipeline.py tests/unit/test_dashboard_helpers.py tests/e2e/test_dashboard.py`
  Before the `src/model/voi.py` patch: `41 passed, 1 failed`, with the failure isolated to `tests/test_voi.py::test_evppi_nonnegative`.
- `pytest tests/test_voi.py`
  After the patch: `2 passed`.

## Suggested Follow-on Work

- A follow-up implementation track should focus on canonical policy-ID unification and scenario-engine repair before adding more dashboard features.
- A second follow-up track should add page-level dashboard tests for Scenarios, Sensitivity, Delta View, and Extended Games, with at least one regression test for each of the issues above.
