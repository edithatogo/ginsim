# Manuscript Asset Inventory

**Status:** Validated against the current generated package on 2026-03-07  
**Current package root:** `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack`  
**Purpose:** Provide one reviewer-facing inventory of the assets actually produced by the active reporting path.

---

## Core brief artifacts

| Asset ID | Artifact | Generator / source | Current path | Status | Notes |
|---|---|---|---|---|---|
| MBA-001 | Policy brief markdown | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/POLICY_BRIEF.md` | Generated | Canonical text output for rapid review and diffing. |
| MBA-002 | Policy brief DOCX | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/POLICY_BRIEF.docx` | Generated | Includes current figures and summary tables. |
| MBA-003 | Policy brief PDF | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/POLICY_BRIEF.pdf` | Generated | Distribution-ready review copy from the same bundle. |

## Current figures

| Asset ID | Artifact | Generator / source | Current path | Status | Notes |
|---|---|---|---|---|---|
| MFA-001 | Australia net-benefit figure | `scripts/generate_figures.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/figures/australia_net_benefit.png` | Generated | Mean net benefit with 90% interval. |
| MFA-002 | Australia figure caption | `scripts/generate_figures.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/figures/australia_net_benefit_caption.md` | Generated | Caption paired to the net-benefit figure. |
| MFA-003 | New Zealand net-benefit figure | `scripts/generate_figures.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/figures/new_zealand_net_benefit.png` | Generated | Mean net benefit with 90% interval. |
| MFA-004 | New Zealand figure caption | `scripts/generate_figures.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/figures/new_zealand_net_benefit_caption.md` | Generated | Caption paired to the net-benefit figure. |

## Structured tables and provenance

| Asset ID | Artifact | Generator / source | Current path | Status | Notes |
|---|---|---|---|---|---|
| MTA-001 | Combined policy summary | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/policy_summary.csv` | Generated | Combined Australia and New Zealand summary table. |
| MTA-002 | Australia policy summary | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/australia_policy_summary.csv` | Generated | Jurisdiction-specific summary table. |
| MTA-003 | New Zealand policy summary | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/new_zealand_policy_summary.csv` | Generated | Jurisdiction-specific summary table. |
| MTA-004 | Reporting manifest | `scripts/publish_pack.py` | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack/reporting_manifest.json` | Generated | Pack-level provenance and table manifest. |
| MTA-005 | Meta comparison report | `scripts/run_meta_pipeline.py` | `outputs/runs/meta_pipeline/20260307T064546Z/compare/REPORT.md` | Generated | Records the run summary and optional stage failures. |

## Not generated in the current package

| Asset ID | Artifact | Expected legacy path | Current status | Reason |
|---|---|---|---|---|
| MGA-001 | EVPPI figure/table set | `<publish_pack>/figures/*_evppi.*` | Not generated | Legacy EVPPI runner depends on removed `src.model.evppi_rff`. |
| MGA-002 | Uncertainty decomposition figure/table set | `<publish_pack>/figures/*_uncertainty_decomposition.*` | Not generated | Legacy decomposition runners depend on removed `sobol_first_order_rff`. |

## Cross-reference

- Current blockers are tracked in [SUBMISSION_GAP_REGISTER.md](./SUBMISSION_GAP_REGISTER.md).
- Reviewer orientation is tracked in [REVIEWER_NAVIGATION_MAP.md](./REVIEWER_NAVIGATION_MAP.md).
