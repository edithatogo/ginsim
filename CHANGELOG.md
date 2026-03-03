# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning.

---

## [Unreleased]

### Phase 3 - Identification Plan and Data Access (2026-03-03)
**Track:** gdpe_0002_evidence_anchoring

#### Added
- Identification plan (`docs/IDENTIFICATION_PLAN.md`) — Data sources, event study design, power analysis
- Data access and governance appendix (`docs/DATA_ACCESS_GOVERNANCE.md`) — Ethics, privacy, Māori data sovereignty
- Data provenance log (`docs/DATA_PROVENANCE_LOG.md`) — Data lineage, transformations, version control
- Runbook v2.0 — Updated with calibration workflow

#### Changed
- Runbook expanded with calibration workflow (5 steps)
- Phase review workflow documented in runbook

#### Technical Notes
- Empirical identification documented for future research (12-18 months)
- Current approach: calibration with evidence register priors
- Data access applications to be prepared in Phase 4

### Phase 2 - Calibration Targets and Priors (2026-03-03)
**Track:** gdpe_0002_evidence_anchoring

#### Added
- Australia calibration configuration (`configs/calibration_australia.yaml`) - 12 parameters with priors
- New Zealand calibration configuration (`configs/calibration_new_zealand.yaml`) - 12 parameters with wider priors
- Evidence-to-prior mapping documentation (`docs/EVIDENCE_TO_PRIOR_MAPPING.md`)
- EVPPI parameter groupings for sensitivity analysis

#### Changed
- NZ priors 40% wider than AU on average (reflects 100% Very Low quality evidence)
- Systematic quality-to-variance mapping (Moderate=1.0x, Low=1.5-1.75x, Very Low=2.0x+)

#### Technical Notes
- All priors documented with explicit rationale
- Truncated normals for signed parameters (elasticities)
- Beta distributions for proportions
- Prior predictive checks deferred to Phase 4

### Phase 1 - Evidence Registers (2026-03-03)
**Track:** gdpe_0002_evidence_anchoring

#### Added
- Australia evidence register (12 evidence items across modules A-F + enforcement)
- New Zealand evidence register (5 evidence items, adapted from AU with wider priors)
- Policy timeline document (comparative AU/NZ)
- Evidence quality grading rubric (GRADE-adapted)
- Reference validation pipeline (`scripts/validate_references.py`)
- Decision log with 12 key decisions documented
- Phase review workflow with automated checks

#### Changed
- Updated track plan with phase review gates
- Updated workflow.md with phase review procedure
- Added validation dependencies to pyproject.toml

#### Fixed
- `fsc_moratorium_2019` reference - added missing institution field

---

## [0.1.0] - 2026-03-02

### Added
- Initial repository structure (src/, scripts/, configs/, context/, docs/)
- Conductor workflow setup (tracks registry, metadata)
- Base modelling infrastructure (JAX/NumPyro/BlackJAX stack)
- Policy schema + loader (Pydantic + YAML)
- Baseline AU/NZ policy configs
- OSF presubmission protocol
- Product definition and tech stack documentation

### Changed
- README.md with quick start instructions

---

## Notes for Future Entries

**Format:**
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for removed features
- `Fixed` for bug fixes
- `Security` for security improvements

**Update when:**
- Completing a phase
- Making significant decisions
- Adding new infrastructure
- Releasing versions
