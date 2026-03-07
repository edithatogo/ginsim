# Manuscript Asset Inventory

**Status:** Active inventory scaffold created in `gdpe_0021`  
**Purpose:** Provide one reviewer-facing inventory of the main manuscript and policy-brief assets generated or described by the active reporting path.

---

## Core brief artifacts

| Asset ID | Artifact | Generator / source | Typical path | Status | Notes |
|---|---|---|---|---|---|
| MBA-001 | Policy brief markdown | `scripts/publish_pack.py` | `<meta_dir>/publish_pack/POLICY_BRIEF.md` | Active | Canonical text output for quick review and diffing. |
| MBA-002 | Policy brief DOCX | `scripts/publish_pack.py` | `<meta_dir>/publish_pack/POLICY_BRIEF.docx` | Active if dependency available | Includes tables, figures, and caption text when Word export dependencies are present. |
| MBA-003 | Policy brief PDF | `scripts/publish_pack.py` | `<meta_dir>/publish_pack/POLICY_BRIEF.pdf` | Active if dependency available | PDF rendering path for distribution-ready review copies. |

## Publication-facing figures

| Asset ID | Artifact | Generator / source | Typical path | Status | Notes |
|---|---|---|---|---|---|
| MFA-001 | Net benefit figure | `scripts/generate_figures.py` | `<publish_pack>/figures/<jurisdiction>_net_benefit.png` | Active | Benchmark policy comparison figure for each jurisdiction. |
| MFA-002 | EVPPI figure | `scripts/generate_figures.py` | `<publish_pack>/figures/<jurisdiction>_evppi.png` | Active | Parameter-group value-of-information figure for each jurisdiction. |
| MFA-003 | Uncertainty decomposition figure | `scripts/generate_figures.py` | `<publish_pack>/figures/<jurisdiction>_uncertainty_decomposition.png` | Active | Shows variance contribution by group on the active reporting path. |
| MFA-004 | Figure captions | `scripts/generate_figures.py` | `<publish_pack>/figures/*_caption.md` | Active | One caption file per publication-facing figure. |

## Structured tables and supporting data

| Asset ID | Artifact | Generator / source | Typical path | Status | Notes |
|---|---|---|---|---|---|
| MTA-001 | Policy summary tables | `scripts/reporting_common.py`, `scripts/publish_pack.py` | reporting bundle and brief tables | Active | Table content is derived from the same reporting bundle used by figures and narrative text. |
| MTA-002 | EVPPI by group CSV | `scripts/reporting_common.py` | `<output_dir>/evppi_by_group.csv` and jurisdiction-specific variants | Active | Structured supporting table behind the EVPPI figure. |
| MTA-003 | Uncertainty decomposition CSV | `scripts/reporting_common.py` | `<output_dir>/uncertainty_decomposition.csv` and jurisdiction-specific variants | Active | Structured supporting table behind the decomposition figure. |
| MTA-004 | Run manifest | reporting pipeline | `<meta_dir>/run_manifest.json` | Active | Provenance surface for reproducibility and reviewer audit. |

## Current gaps tracked elsewhere

- Remaining packaging blockers and reviewer-facing gaps are tracked in [SUBMISSION_GAP_REGISTER.md](./SUBMISSION_GAP_REGISTER.md).
- Claim-to-evidence navigation is tracked in [REVIEWER_NAVIGATION_MAP.md](./REVIEWER_NAVIGATION_MAP.md).
