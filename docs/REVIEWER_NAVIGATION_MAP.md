# Reviewer Navigation Map: Diamond Standard Hardening

This document guides reviewers through the hardened, publication-grade analytical surfaces of the repository.

## 1. Grounding & Evidence
- **References:** `context/references.bib` (100% harmonized)
- **Assumptions:** `context/assumptions_registry.yaml` (Programmatically linked to BibTeX)
- **Evidence Explorer:** Dashboard page `pages/traceability.py`

## 2. Technical Rigor
- **Logic Verification:** `tests/test_economic_logic.py` (Hypothesis property-based tests)
- **Mathematical Proofs:** `src/model/module_c_insurance_eq.py` (JAX Jacobian equilibrium verification)
- **Security:** `ci.yaml` includes automated `pip-audit` and secret scanning.

## 3. Reproduction
- **One-Click:** Run `uv sync` followed by `python scripts/reproduce_all.py`.
