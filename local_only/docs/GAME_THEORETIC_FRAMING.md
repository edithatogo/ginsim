# Game-theoretic framing, empirical evidence, and mathematical representation

This document makes explicit **which strategic interactions (“games”)** are being represented in the model,
**what empirical evidence** motivates each channel, and **why the current mathematical forms** were chosen.

It is intended to reduce “hidden degrees of freedom” by documenting modelling choices up-front.

---

## 1) Strategic interactions represented (conceptual “games”)

### A) Underwriting and contract choice under asymmetric information (adverse selection / screening)
**Conceptual game:** Bayesian screening / adverse selection (Rothschild–Stiglitz intuition).
**Players:** applicants (informed about their risk or ability to learn it), insurers (pricing/contract design under regulation), regulator (ruleset).
**Core mechanism:** regulation constrains information; applicants’ private information affects demand; insurers adjust premiums/terms; equilibrium may change.

**Where represented:** Module C (insurance equilibrium) + policy ruleset.

---

### B) Testing / research participation under perceived downstream penalty (participation with an anticipated cost)
**Conceptual game:** participation under penalty risk; can be framed as signalling or strategic participation.
**Players:** individuals deciding to test/participate; insurers/employers as downstream “audiences”; policymakers as rule-setters.
**Core mechanism:** perceived discrimination risk reduces testing/research participation; protections reduce the expected penalty and increase uptake.

**Where represented:** Module A (behaviour/uptake). Currently reduced-form rather than explicit signalling equilibrium.

---

### C) Proxy substitution under regulatory constraint (constrained optimisation / regulatory substitution)
**Conceptual game:** constrained optimisation by insurers (or “mechanism design with constraints”).
**Players:** insurers (choose features/proxies and decision rules), applicants (respond through selection), regulator (constraints).
**Core mechanism:** banning genetic test results may shift underwriting to other correlated proxies (family history, diagnosis, postcode, etc.),
changing mispricing and selection pressure.

**Where represented:** Module D (proxy substitution), implemented as constrained re-optimisation + calibration/mispricing diagnostics.

---

### D) Data-quality externality (participation as a public good)
**Conceptual game:** public goods / free-rider externality.
**Players:** individuals (participate or not), health system and future patients (benefit from better models), researchers/industry (build tools).
**Core mechanism:** participation improves dataset representativeness and future predictive tools; fear-induced non-participation reduces data quality.

**Where represented:** Module F (data-quality), stylised selection model → representativeness proxy → performance proxy.

---

### E) Enforcement and compliance (regulator–insurer compliance game)
**Conceptual game:** enforcement/compliance game.
**Players:** regulator (audit/enforcement intensity), insurers (compliance effort), consumers (complaints).
**Core mechanism:** “policy on paper” is not equivalent to “policy in effect”; enforcement changes effective protection.

**Where represented:** currently reduced-form via `enforcement_strength` encoded into protection intensity; can be upgraded to an explicit audit/compliance module.

---

## 2) Evidence base: what is strong vs what is typically assumption-driven

### Stronger empirical footing
- Deterrence of testing/research participation driven by **fear of insurance discrimination**.
- Reported experiences of insurance difficulty following genetic testing in some settings.

**Implication:** Module A (uptake) should be calibrated/identified with empirical designs (event studies, DiD, diffusion, survey linkage).

### More limited / indirect empirical footing (often scenario-based)
- Magnitude of adverse selection impacts when insurers cannot use genetic test results.
- Degree and direction of proxy substitution specifically attributable to genetic information restrictions.
- Quantification of enforcement effects (how strongly an on-paper rule changes underwriting in practice).

**Implication:** treat these as uncertain parameters, propagate uncertainty, and prioritise evidence gaps with VOI / EVPPI.

---

## 3) Why the current mathematical forms were chosen

### Principle 1 — Decision-first modelling
We started from outputs decision-makers typically need:
- net health outcomes (QALYs/events)
- insurance outcomes (premiums/take-up/coverage)
- DCBA ledger + VOI/EVPPI + sensitivity

This requires linking policy → behaviour → market outcomes → health outcomes → fiscal and welfare impacts.

### Principle 2 — Structural modelling only where it buys leverage
- Insurance equilibrium (Module C) is where debates hinge on “adverse selection” → structural/equilibrium component is warranted.
- Testing deterrence (Module A) is more often identified empirically than via explicit signalling equilibria → reduced-form is the base case.

### Principle 3 — Separate “policy text” from “policy effect”
Legal categories (ban, moratorium, caps, enforcement) are mapped into a numeric *protection intensity*.
That mapping is itself uncertain and can be **estimated** (repo includes a NumPyro scaffold for this).

### Principle 4 — Make substitution/externalities measurable
Proxy substitution and data-quality externalities are easy to hand-wave; we represent them in forms that can be confronted with data:
- constrained underwriting optimisation + calibration/mispricing (Module D)
- selection → representativeness → tool performance (Module F)

### Principle 5 — Tractability + extensibility (JAX/XLA)
We use JAX-friendly modular code to enable:
- large posterior simulations
- VOI / EVPPI and sensitivity decomposition
- later upgrades to richer game forms without rewriting the whole pipeline

---

## 4) Mapping table: modules ↔ games ↔ implementation choices

| Module | Strategic interaction (“game”) | Implemented form now | Identification / calibration plan | Upgrade path |
|---|---|---|---|---|
| A Behaviour/Uptake | Participation under penalty (signalling/participation game) | Reduced-form uptake response to protection intensity | Event study / DiD / diffusion + survey linkage | Explicit dynamic decision model with perceived penalty and information frictions |
| B Clinical | Not a game per se (biophysical + intervention dynamics) | Decision-analytic microsim/Markov scaffold | Literature + registries + priors | Disease-specific microsim; adherence heterogeneity; competing risks |
| C Insurance equilibrium | Bayesian screening/adverse selection | Fixed-point equilibrium placeholder | Insurer aggregates; demand elasticities; scenario + posterior | Structural demand + pricing; reinsurance; product menu; dynamic lapses |
| D Proxy substitution | Constrained optimisation under regulation | Re-optimisation + calibration/mispricing metrics | Underwriting feature/decision logs where possible | Endogenous selection feedback into C; fairness constraints; alternative proxy sets |
| E Pass-through | IO incidence / market power | Hierarchical pass-through scaffold | Premium changes vs concentration and cost shocks | Full IO pass-through estimation; reinsurance pass-through |
| F Data quality | Public-good externality | Selection model → representativeness → performance proxy | Cohort participation + model calibration metrics | PRS/score evaluation; downstream clinical net benefit; equity impacts |
| Enforcement (encoded) | Compliance game | Reduced-form enforcement_strength | Complaints + audit data where available | Explicit audit/compliance submodel |

---

## 5) Repository artefacts that implement these choices
- Canonical policy schema: `src/model/schema.py`
- Policy → intensity mapping (heuristic + parametric): `src/model/policy_encoding.py`
- Mapping estimation scaffold: `src/inference/fit_policy_mapping.py`
- DCBA ledger scaffold: `src/model/dcba_ledger.py`
- Full uncertainty propagation (with sampling controls): `scripts/run_full_uncertainty.py`
- Sensitivity decomposition: `scripts/run_uncertainty_decomposition.py` and `scripts/run_uncertainty_decomposition_total.py`
- EVPPI by group: `scripts/run_evppi_by_group_from_run_dir.py`
- Meta pipeline + publish pack: `scripts/run_meta_pipeline.py`, `scripts/publish_pack.py`

---

## 6) TODO for “evidence anchoring”
For each jurisdiction and domain (Australia/NZ; life insurance; employment extension), add an evidence table with:
- key studies or official analyses used to set priors
- policy change dates and definitions
- data access notes (what can be measured vs assumed)

Recommended placement:
- `context/jurisdiction_profiles/<jurisdiction>_<domain>_evidence.md`
