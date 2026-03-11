# Track Specification: Formal Mathematical Anchoring Vertical

**Track ID:** gdpe_0041_math_verification_vertical
**Type:** Structural Overhaul / Verification
**Goal:** Implement an end-to-end "Proof Engine" using JAX Jacobians to verify First-Order Conditions (FOCs) and equilibrium stability theorems.

## 1. Overview
Nature editors expect rigorous proof that the computed results represent true Nash Equilibria. This track formalizes the "Diamond Standard" by creating a suite of tests that link code directly to the mathematical theorems in the manuscript.

## 2. Functional Requirements
- **FOC Verifier:** Create `tests/verification/test_formal_focs.py` to calculate gradients at the equilibrium point and verify they are approximately zero.
- **Stability Analysis:** Automate the calculation of the Hessian matrix to prove equilibrium uniqueness and stability.
- **Symbolic Linkage:** Document the mapping between code symbols (e.g., `compute_demand`) and manuscript variables (e.g., $D(p)$).

## 3. Acceptance Criteria
- [ ] Every equilibrium solve in the pipeline is followed by a Jacobian-based FOC check.
- [ ] New "Technical Proofs" expander added to every dashboard page showing live gradients.
- [ ] Mathematical stability verified across the entire parameter space.
