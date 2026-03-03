# Specification: Evidence register + calibration for AU/NZ

## Goal
Anchor each modelling channel (A–F + enforcement) to an explicit evidence base for Australia and New Zealand,
including effect-size priors, identification strategy, and data access notes.

## Scope
- Populate evidence registers under `context/jurisdiction_profiles/`
- Define calibration targets and data sources for each module
- Define identification plan (DiD/event study where relevant; insurer aggregates; survey linkage)
- Update priors and document assumptions in configs
- Update publish pack narrative sections to cite evidence sources (where appropriate)

## Acceptance criteria
- Each channel has: evidence summary, prior range, and a plan to estimate.
- One “evidence gaps → VOI priorities” table per jurisdiction.
