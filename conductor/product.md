# Product definition

## What this repository is
A research-grade, reproducible modelling and analysis repository to **quantify the economic and welfare impacts of policies that restrict genetic discrimination**, with an initial focus on **life insurance** and explicit comparative framing for **Australia** and **Aotearoa New Zealand**.

The repo implements a modular pipeline:
policy rules → behavioural response → insurance equilibrium outcomes → health/clinical downstream impacts → DCBA ledger → VOI/EVPPI/sensitivity → AU/NZ comparison outputs → publish pack.

## Primary users
- Health economists and policy analysts (HTA / regulatory impact / social policy)
- Researchers working on genomics policy, insurance, and discrimination
- Government and advisory bodies evaluating bans vs moratoria vs caps vs enforcement regimes
- Technical collaborators extending model structure and inference

## What success looks like
- A transparent mapping from **policy levers** (ban/moratorium/caps/enforcement) to **outcomes** (testing uptake, premiums/take-up, QALYs, costs).
- Explicit uncertainty quantification with clear “what matters most” diagnostics (EVPI/EVPPI; S1/ST).
- A structured evidence register per jurisdiction that anchors priors/assumptions.
- Outputs that are publication-ready (policy brief pack + reproducible run manifests).
- **Automated remote monitoring ensures 24/7 availability of the policy simulation dashboard.**
- **Professionalised repository with standardized Open Science metadata (CITATION.cff, CONTRIBUTING.md).**

## Non-goals (for now)
- Employment discrimination modelling (unless explicitly added as a domain extension track)
- Fully structural insurer competition models (unless the evidence and data justify it)
- High-fidelity disease microsimulation beyond the scaffolds (unless scoped)

## Constraints
- Must run on standard research laptops with Python >= 3.10.
- Prefer JAX/NumPyro/BlackJAX-compatible approaches for inference and Monte Carlo.
- Reproducibility: deterministic seeds where possible; outputs include run manifests with hashes.
