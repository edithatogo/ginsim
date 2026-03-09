# Product definition

## What this repository is
A research-grade, reproducible modelling and analysis engine to **quantify the clinical, economic, and welfare impacts of policies that restrict genetic discrimination**, with an initial focus on **life insurance** and explicit comparative framing for **Australia, Aotearoa New Zealand, the UK, Canada, and the US**.

The repo implements an integrated clinical-economic pipeline:
**Threshold-aware policy rules** -> behavioural response -> insurance equilibrium outcomes -> **disease-specific clinical microsimulation (Lynch, BRCA, FH)** -> **PPP-standardized DCBA ledger** -> VOI/EVPPI/sensitivity -> **Global benchmarking outputs**.

## Primary users
- Health economists and policy analysts (HTA / regulatory impact / social policy)
- Researchers working on genomics policy, insurance, and discrimination
- Government and advisory bodies evaluating bans vs moratoria vs caps vs enforcement regimes
- Technical collaborators extending model structure and inference

## What success looks like
- A transparent mapping from **policy levers** (ban/moratorium/sum-insured caps/enforcement) to **outcomes** (testing uptake, premiums/take-up, QALYs, costs).
- Explicit uncertainty quantification with clear "what matters most" diagnostics (EVPI/EVPPI; S1/ST).
- **Adversarial Robustness:** Automated "Red-Teaming" engine using gradient-based optimization to identify parameter combinations that collapse policy welfare.
- **Permanent Governance Layer:** Integrated Agentic Delphi Protocol providing live stakeholder sentiment (Nature, Lancet, Treasury) for every scenario.
- A structured evidence register per jurisdiction that anchors priors/assumptions.
- Outputs that are reproducible, reviewer-auditable (Lancet/Nature grade), and suitable for high-impact manuscript/package assembly.
- Integrated clinical utility that grounds economic QALY gains in real-world genetic condition cohorts.
- A repository structure optimized for public visibility (Reviewer-First README) with internal development context securely isolated in `local_only/`.
- Programmatic linkage between scientific assumptions and the peer-reviewed evidence base.
- Global benchmarking engine comparing international efficiency frontiers (AU, NZ, UK, CAN, US).
- Cross-pollination analysis: applying policies from one jurisdiction to populations of another.

## Non-goals (for now)
- Employment discrimination modelling (unless explicitly added as a domain extension track)
- Fully structural insurer competition models (unless the evidence and data justify it)
- High-fidelity disease microsimulation beyond the implemented cohorts (unless scoped)

## Constraints
- Must run on standard research laptops with Python >= 3.11.
- Prefer JAX/NumPyro/BlackJAX-compatible approaches for inference and Monte Carlo.
- Reproducibility: deterministic seeds where possible; outputs include run manifests with hashes.
- Absolute Verification: 100% test coverage and zero-defect quality gates.
