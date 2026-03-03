# Specification: Bootstrap AU/NZ genetic discrimination policy-econ modelling repo

## Goal
Create a reproducible, JAX-first modelling repository to quantify economic arguments for/against restricting genetic discrimination,
with explicit comparative support for Australia and Aotearoa New Zealand.

## Scope
- Canonical policy schema + loader
- Policy→intensity mapping (heuristic + estimable parametric mapping)
- Modular pipeline (A–F) with JAX simulation glue
- DCBA ledger scaffold
- VOI/EVPPI + sensitivity decomposition (S1 + total-order approximation)
- Posterior propagation (mapping + modules)
- AU/NZ runners + meta pipeline orchestrator
- Publish pack generator (MD/DOCX/PDF/figures)
- Context engineering docs + game-theoretic framing doc + evidence templates
- Windows-friendly zip packaging

## Acceptance criteria
- Running meta pipeline produces AU and NZ outputs + comparison tables.
- Each run writes a manifest with hashes.
- Publish pack can be generated from a meta pipeline run directory.
