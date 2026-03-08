# Model card (draft)

**Project:** Genetic discrimination policy economic evaluation
**Repo version:** active `gdpe_0020` working state
**Date:** 07 March 2026

## Intended use
Decision support for comparing policy options restricting use of genetic information (insurance/employment as configured).

## Not intended use
Individual-level prediction for underwriting, clinical decision-making, or eligibility decisions.

## Key components
- Module A: behaviour/uptake
- Module B: clinical prevention/outcomes
- Module C: insurance equilibrium
- Module D: proxy substitution
- Module E: pass-through/market power
- Module F: dataset selection and predictive tool performance
- Integration: DCBA / welfare / VOI

## Active benchmark comparators
- `status_quo`
- `moratorium`
- `ban`

These are the canonical benchmark regimes on the active dashboard, scenario engine, and policy-evaluation path. Additional scenario designs should be treated as exploratory unless explicitly promoted into the canonical comparator registry.

## Data sensitivities
Genetic and insurance data are sensitive; require strong governance, minimisation, and secure handling.

## Known limitations
- The active path now integrates proxy-substitution, data-quality, and dual-horizon welfare surfaces, but several empirical components still rely on adapted or transfer assumptions rather than direct jurisdiction-specific estimates.
- Some older documents and historical milestone summaries in the repository still describe superseded “publication-ready” or “SOTA-ready” states and should not be treated as authoritative over the active conductor track.
- Publication-facing figure/caption breadth is improved but still not complete across all older repo materials.
