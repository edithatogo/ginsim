# Submission Gap Register

**Status:** Updated against the current generated submission package on 2026-03-07  
**Current package:** `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack`  
**Purpose:** Record the remaining blockers between the current repository state and a cleaner top-tier journal submission package.

---

## Closed in this pass

- A fresh meta run was generated at `outputs/runs/meta_pipeline/20260307T064546Z`.
- A current publish pack was generated at `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack`.
- The package now includes `POLICY_BRIEF.md`, `POLICY_BRIEF.docx`, `POLICY_BRIEF.pdf`, jurisdiction-specific policy summary CSVs, `policy_summary.csv`, `reporting_manifest.json`, and net-benefit figure/caption pairs for Australia and New Zealand.

## Remaining blockers

| Gap ID | Blocker | Reviewer impact | Affected artifact(s) | Current status | Planned closure mechanism | Deferral rationale |
|---|---|---|---|---|---|---|
| SGR-001 | Legacy uncertainty decomposition scripts still depend on removed APIs (`sobol_first_order_rff`) | Reviewer cannot inspect current first-order or total-order decomposition sidecars from the packaged run | `scripts/run_uncertainty_decomposition.py`, `scripts/run_uncertainty_decomposition_total.py`, `outputs/runs/meta_pipeline/20260307T064546Z/decomp_*` | Open | Rebuild decomposition scripts against the current sensitivity surface or retire them formally from the package contract | Not safe to fake these outputs |
| SGR-002 | Legacy EVPPI runner still depends on removed module `src.model.evppi_rff` | Reviewer cannot inspect current EVPPI-by-group sidecars from the packaged run | `scripts/run_evppi_by_group_from_run_dir.py`, `outputs/runs/meta_pipeline/20260307T064546Z/evppi_by_group` | Open | Rebuild EVPPI generation on the current model surface or remove EVPPI from the active package promise | Not safe to claim missing value-of-information outputs |
| SGR-003 | The generated package is policy-brief grade, not yet a full manuscript asset pack | Reviewer still needs a separate manuscript assembly step for journal submission tables/figures | `outputs/runs/meta_pipeline/20260307T064546Z/publish_pack`, manuscript-facing docs | Open | Create a dedicated manuscript asset build that lifts the packaged summaries into manuscript figure/table numbering and captions | Current package is valid but narrower than a final journal bundle |
| SGR-004 | `compare/REPORT.md` still shows status-quo as top policy in this run, which may require interpretive scrutiny before manuscript framing | Reviewer may question whether comparator framing and normative interpretation are aligned with substantive claims | `outputs/runs/meta_pipeline/20260307T064546Z/compare/REPORT.md`, manuscript discussion text | Open | Review calibration, interpretation, and manuscript wording before locking policy-facing conclusions | Requires substantive interpretation, not just formatting |

## Use

- Close a row only when the underlying artifact exists and the supporting scripts run cleanly.
- Treat this file as the canonical blocker list for submission packaging, not the conductor track history.
- If a blocker is intentionally deferred, keep the rationale explicit and reviewer-safe.
