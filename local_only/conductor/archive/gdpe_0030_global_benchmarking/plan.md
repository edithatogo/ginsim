# Implementation Plan: Global Benchmarking & Threshold Architecture

**Track ID:** gdpe_0030_global_benchmarking
**Execution mode:** Autonomous Phase Loop

## Phase 1: Parameter Abstraction & Evidence
- [ ] Task: Refactor `src/model/parameters.py` to remove hardcoded defaults.
- [ ] Task: Create YAML loaders for jurisdiction profiles.
- [ ] Task: Migrate AU and NZ to the new YAML structure.
- [ ] Task: Create YAML profiles for UK, Canada, and US (including PPP rates).
- [ ] Task: Conductor - Auto-Review & Remediation 'Parameter Abstraction'

## Phase 2: Core Engine Upgrades (Threshold Math)
- [ ] Task: Update `PolicyConfig` schema to support `sum_insured_caps`.
- [ ] Task: Refactor `module_a_behavior.py` and `module_c_insurance_eq.py` to process threshold vectors using `jax.lax.cond`.
- [ ] Task: Update `dcba_ledger.py` to apply PPP normalization factors.
- [ ] Task: Conductor - Auto-Review & Remediation 'Engine Upgrades'

## Phase 3: Retrofitting & Matrix Testing
- [ ] Task: Retrofit the AU FSC Moratorium to use the new exact financial threshold logic ($500k life).
- [ ] Task: Refactor `tests/` to use `pytest.mark.parametrize` over all 5 jurisdiction configs.
- [ ] Task: Conductor - Auto-Review & Remediation 'Matrix Testing'

## Phase 4: Streamlit Dashboard Promulgation
- [ ] Task: Add "Global Benchmarking" tab to `app.py` with the Frontier Scatter Plot.
- [ ] Task: Add "Cross-Pollination Sandbox" allowing decoupled Policy/Population selection.
- [ ] Task: Add the Regulatory Matrix data table.
- [ ] Task: Conductor - Auto-Review & Remediation 'Dashboard Promulgation'

## Phase 5: CI/CD & Final Verification
- [ ] Task: Update GitHub Actions workflow (`.github/workflows/ci.yaml`) to run matrix tests if necessary.
- [ ] Task: Run full E2E dashboard suite to verify UI integrations.
- [ ] Task: Finalize Track.
