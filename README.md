# GINSIM: Genetic Discrimination Policy Integrated Economic Evaluation

![Deployment Status](https://github.com/edithatogo/ginsim/actions/workflows/remote-e2e.yml/badge.svg)
![License](https://img.shields.io/github/license/edithatogo/ginsim)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

**GINSIM** is a state-of-the-art, reproducible modelling framework designed to quantify the economic and welfare impacts of policies that restrict genetic discrimination in life insurance. It provides a robust laboratory for policy evaluation with a primary focus on the Australian and Aotearoa New Zealand contexts.

---

## 🚀 Key Features

| Feature | Description |
|:---|:---|
| **High Performance JAX Backend** | Leverages JAX and XLA for high-speed, vectorized Monte Carlo simulations and gradient-based optimization. |
| **International Scenarios** | Standardized policy benchmarks for Australia (FSC Moratorium, 2025 Ban), New Zealand, USA (GINA), Canada (GNDA), and the UK. |
| **Distributional Equity Metrics** | Implements Distributional Cost-Benefit Analysis (DCBA) to assess impacts across risk quintiles and Indigenous populations. |
| **Game-Theoretic Framework** | Models strategic interactions between insurers and applicants, including Nash equilibria in enforcement and adversarial re-optimization on proxy data. |
| **Interactive Dashboard** | A Streamlit-based visualization tool for real-time policy "sandbox" exploration and sensitivity analysis. |

---

## 📖 About the Research

This repository supports research into the complex trade-offs between consumer protection and insurance market stability. By modelling the "Information Leakage" from proxy variables (like family history) and the "Scientific Loss" from research participation deterrence, GINSIM provides a comprehensive view of the societal value of genetic non-discrimination laws.

The model is calibrated against structured evidence registers, ensuring that all priors and behavioral elasticities are grounded in established literature (e.g., Taylor et al. 2021, Ettema et al. 2021).

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

**Author:** Dylan Mordaunt  
**Affiliation:** Victoria University of Wellington  
**Live App:** [https://ginsim.streamlit.app/](https://ginsim.streamlit.app/)
