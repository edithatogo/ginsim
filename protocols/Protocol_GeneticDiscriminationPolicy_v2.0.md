# Protocol: Integrated Economic Evaluation of Policy Options to Restrict Genetic Discrimination

**Version:** v2.0 (Diamond Standard)
**Date:** 08 March 2026
**Author:** Dylan A Mordaunt

---
**Revision Note (v2.0):** This version incorporates "Diamond Standard" re-engineering, including JAX Jacobian equilibrium proofs, property-based testing for economic identities, and an institutionalized "Unattended Loop" for autonomous model hardening.
---

## 1. Background and rationale
Concerns about genetic discrimination have shaped policy debates across health, employment, and insurance. This protocol specifies an integrated economic evaluation that quantifies multiple strategic channels: adverse selection, behavioural deterrence, proxy substitution, and research-participation externalities.

## 2. Objectives
### 2.1 Primary objective
To estimate the net social impacts of alternative policy regimes restricting the use of genetic information, using a mathematically verified, high-rigor JAX-based simulation engine.

### 2.2 Secondary objectives
1. To quantify the magnitude of deterrence effects on genetic testing and research participation.
2. To estimate adverse selection and premium impacts, verified via gradient-based equilibrium proofs.
3. To quantify fiscal and data-quality externalities.
4. To PRIORITIZE research via SOTA Value of Information (VOI) analysis.
5. To categorize policy outcomes via a Narrative Fairness Audit (Rawlsian vs. Utilitarian).

## 3. Methodological Rigor (Diamond Standard)
As of v2.0, the model adheres to the following rigorous standards:
- **Numerical Stability:** All logit-based decision functions (Module A and E) utilize stabilized `jax.nn.sigmoid` kernels.
- **Equilibrium Verification:** Competitive insurance equilibria (Module C) are formally verified using JAX Jacobians to confirm zero-profit First-Order Conditions (FOC).
- **Property-Based Testing (PBT):** Core economic identities (e.g., Welfare Conservation: `Net = CS + PS + Fiscal + Health - Research`) are verified using `Hypothesis` across the entire valid parameter space.
- **Institutionalized Verification Loops:** The model development utilizes a 3-strike "Circuit Breaker" and a mandatory "Quality Gate" enforcing 100% test coverage and zero-defect linting/typing.

## 4. Conceptual framework
(See Game-Theoretic framing in `docs/GAME_THEORETIC_FRAMING.md`)

## 5. Software and Reproducibility
- **Environment:** Unified deterministic environment managed via `uv` and `uv.lock`.
- **Infrastructure:** Hermetic CI/CD with automated security auditing (`pip-audit`) and static analysis (`Pyright` 100% green).
- **Provenance:** Cryptographic `PROVENANCE_HASH` linking code, data, and configuration to every output artifact.

## 6. Integration and DCBA
### 6.1 Welfare Ledger
The ledger utilizes a consistent geometric-series discounting kernel. Research externalities (Module F) are formally integrated into the headline net-welfare surface.

### 6.2 Narrative Fairness Audit
Policy results are translated into narrative verdicts:
- **Rawlsian Equity:** Focus on protecting high-risk individuals.
- **Utilitarian Efficiency:** Focus on maximum societal net benefit.
- **Precautionary Protection:** Focus on information safety.

## 11. Implementation plan
- **Diamond Gate Enforcement:** No phase progression is permitted without 100% test coverage and `scripts/quality_gate.py` passing.
- **Critical Review:** Mandatory adversarial review of all SOTA implementations.

## 13. Outputs
- **Diamond Submission Pack:** ZIP including `REPRODUCTION_REPORT.md` and `CITATION_GRAPH.json`.
