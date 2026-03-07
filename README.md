# GINSIM: Genetic Information Non-Discrimination Policy Integrated Economic Evaluation

![Deployment Status](https://github.com/edithatogo/ginsim/actions/workflows/remote-e2e.yml/badge.svg)
![License](https://img.shields.io/github/license/edithatogo/ginsim)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

**GINSIM** is a research-grade, reproducible modelling framework designed to quantify the economic and welfare impacts of policies that restrict genetic discrimination in life insurance. It provides a policy-analysis and reviewer-auditable workflow with a primary focus on the Australian and Aotearoa New Zealand contexts.

---

## 🚀 Key Features

| Feature | Description |
|:---|:---|
| **High Performance JAX Backend** | Leverages JAX and XLA for high-speed, vectorized Monte Carlo simulations and gradient-based optimization. |
| **Canonical Policy Benchmarks** | Active benchmark comparators are `status_quo`, `moratorium`, and `ban`, with additional international scenarios treated as exploratory unless explicitly promoted. |
| **Distributional Equity Metrics** | Implements Distributional Cost-Benefit Analysis (DCBA) to assess impacts across risk quintiles and Indigenous populations. |
| **Game-Theoretic Framework** | Models strategic interactions between insurers and applicants, including Nash equilibria in enforcement and adversarial re-optimization on proxy data. |
| **Interactive Dashboard** | A Streamlit-based visualization tool for real-time policy "sandbox" exploration and sensitivity analysis. |

---

## 📖 About the Research

This repository supports research into the complex trade-offs between consumer protection and insurance market stability. By modelling the "Information Leakage" from proxy variables (like family history) and the "Scientific Loss" from research participation deterrence, GINSIM provides a comprehensive view of the societal value of genetic non-discrimination laws.

The model is calibrated against structured evidence registers, with active assumptions and transfer decisions tracked in the repository context and reference-validation surfaces. Reviewer-facing documentation should be preferred over older milestone notes when interpreting current readiness.

---

## 🛠️ Quick Start (Local)

1. **Create an environment** (recommended: conda or venv):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -e .
   ```
3. **Run the Dashboard**:
   ```bash
   streamlit run streamlit_app/app.py
   ```

---

## 📁 Repository Structure

- `src/` — Core modelling engine (JAX/NumPyro).
- `streamlit_app/` — Interactive dashboard source code.
- `configs/` — YAML definitions for policy regimes and priors.
- `context/` — Evidence registers and jurisdictional profiles.
- `protocols/` — Research protocols and validation frameworks.
- `docs/` — Technical documentation and Model Card.

---

## ⚖️ License & Citation

- **Code:** [MIT License](LICENSE)
- **Documentation:** CC-BY 4.0
- **Citation:** Please see [CITATION.cff](CITATION.cff) for bibtex and APA formats.

---

**Author:** Dylan A Mordaunt  
**Affiliation:** Research Fellow, Faculty of Health, Education and Psychology, Victoria University of Wellington  
**Live App:** [https://ginsim.streamlit.app/](https://ginsim.streamlit.app/)
