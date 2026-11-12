# Phase 1 Traceability Audit

**Track:** `gdpe_0020_dashboard_policy_alignment_and_publication_sync`
**Date:** 2026-03-07
**Status:** In progress

---

## Scope

This audit covers the first implementation slice of `gdpe_0020`:
- active evidence/config citation-key consistency;
- current reference-validation tooling behavior;
- assumptions-registry completeness;
- New Zealand transferability/adaptation exposure.

## Summary

The repository currently does not have a functioning publication-grade traceability layer.

The main blockers are:
- evidence-register/config source keys do not resolve to the canonical CSL-JSON identifier scheme;
- the current validator targets the wrong source of truth and crashes on Windows console output;
- the assumptions registry is still placeholder-grade;
- New Zealand calibration remains heavily adaptation-based and needs structured disclosure.

## Findings

### 1. Citation-key mismatch against canonical CSL-JSON

Audit result:
- Canonical CSL-JSON entries in `study/references/references.json`: `33`
- Distinct raw `source` / `citation_key` values found across `context/` and `configs/`: `24`
- Atomic normalized source keys after splitting combined entries: `12`
- Atomic normalized keys that resolve directly to CSL-JSON IDs: `0`
- Atomic normalized keys that do **not** resolve directly to CSL-JSON IDs: `12`

Unresolved atomic keys:
- `Authors' analysis based on policy documents`
- `armstrong_genetic_testing_insurance_2020`
- `blevins_genomic_data_bias_2020`
- `ettema_genetic_testing_uptake_2021`
- `finkelstein_insurance_market_structure_2019`
- `fsc_moratorium_2019`
- `hersch_viscusi_insurance_discrimination_2019`
- `hrc_nz_genetic_discrimination_2020`
- `lowenstein_genetic_discrimination_insurance_2021`
- `mcguire_perceived_discrimination_testing_2019`
- `tabor_family_history_proxy_2018`
- `taylor_australia_genetic_discrimination_2021`

Interpretation:
- the evidence/config layer currently uses a long-form naming scheme;
- the CSL-JSON layer currently uses a short-form ID scheme;
- there is no resolver map between them, so "canonical" reference traceability is not yet operational.

### 2. Reference validator is not fit for the current repo

Observed behavior from `python scripts/validate_references.py`:
- loads `21` entries from `context/references.bib`;
- scans project files and reports `0` citations found;
- reports all `21` BibTeX entries as orphaned;
- crashes at the end with `UnicodeEncodeError` on Windows due to the warning emoji output.

Interpretation:
- the validator is still built around the legacy BibTeX store, not the canonical CSL-JSON file;
- it is not scanning the actual YAML/config evidence surfaces in a useful way;
- it is currently not reliable as a CI or local publication-QA tool.

### 3. Assumptions registry is still placeholder-grade

Observed state in `context/assumptions_registry.yaml`:
- total assumptions recorded: `3`
- entries marked `status: "placeholder"`: `3`

Current entries:
- `A001` policy protection reduces fear and increases uptake
- `A002` adverse selection increases effective loss cost
- `A003` proxy substitution occurs under restriction

Interpretation:
- the registry does not yet enumerate jurisdiction transfers, welfare-ledger assumptions, scenario-field interpretation rules, or other active-path structural assumptions;
- this is not sufficient for external peer review.

### 4. New Zealand calibration is still adaptation-heavy

Observed in `configs/calibration_new_zealand.yaml`:
- lines explicitly signalling adaptation / extrapolation / transferability logic: `15`

Representative examples:
- `ettema_genetic_testing_uptake_2021 (extrapolated)`
- `Netherlands (applied to NZ)`
- `hersch_viscusi_insurance_discrimination_2019 (adapted for NZ)`
- `US model applied to NZ`
- `armstrong_genetic_testing_insurance_2020 (extrapolated)`
- `United States (applied to NZ)`
- `tabor_family_history_proxy_2018 (extrapolated)`
- `US (applied to NZ)`
- `lowenstein_genetic_discrimination_insurance_2021 (extrapolated)`
- `Multiple (applied to NZ)`
- `US (adapted for NZ concentration)`
- `blevins_genomic_data_bias_2020 (extrapolated)`
- `International (applied to NZ)`

Interpretation:
- NZ calibration is still structurally dependent on borrowed evidence;
- this is not inherently disqualifying, but it requires a formal transferability audit plus explicit downstream sensitivity/VOI treatment.

## Immediate Implications for `gdpe_0020`

The next implementation steps should be:
1. build a citation reconciliation map between long-form evidence/config keys and CSL-JSON IDs;
2. replace or rewrite `scripts/validate_references.py` around `study/references/references.json`;
3. expand `context/assumptions_registry.yaml` into an active-path assumption inventory;
4. create an explicit NZ transferability register or sectioned audit artifact;
5. prevent docs/dashboard/manuscript-adjacent surfaces from implying stronger empirical closure than this layer currently supports.

## Implementation Progress Landed in This Phase

The following closure work has now been implemented:
- added `study/references/reference_key_aliases.json` as an explicit resolver layer between long-form evidence/config keys and canonical CSL-JSON IDs;
- replaced `scripts/validate_references.py` with a CSL-JSON-based validator that scans YAML/Markdown/code citation surfaces and runs cleanly on Windows;
- added `tests/unit/test_reference_validation.py` to verify alias resolution, internal-only sources, and unresolved-key detection.
- expanded `context/assumptions_registry.yaml` into a broader active-path assumption inventory covering structural, transferability, scenario-engine, and exploratory-surface assumptions;
- added `NZ_TRANSFERABILITY_AUDIT.md` to document the specific NZ calibration entries that remain adaptation-based and their replacement priority.

Current validator status after the rewrite:
- canonical references: `33`
- raw keys found across scanned repo surfaces: `25`
- resolved canonical keys: `11`
- internal-only allowed keys: `1`
- unresolved keys: `0`
- unused canonical references: `22`

Interpretation:
- the canonical traceability path now works mechanically for the currently referenced evidence/config surfaces;
- the next traceability task is no longer “make validation run” but “propagate the now-explicit assumptions and transferability disclosures into manuscript-adjacent, dashboard, and publication-output surfaces.”

## Recommended Deliverables

- `reference_key_map.yaml` or equivalent canonical resolver file
- rewritten CSL-JSON-based validator with YAML/Markdown/code scanning
- expanded assumptions registry
- NZ transferability audit artifact
- updated manuscript/protocol/dashboard copy drawing from the reconciled traceability layer
