# 🧬 gin-sim

**Genetic Information Non-Discrimination Simulation**

Interactive dashboard for exploring the economic impacts of genetic discrimination policies in life insurance markets.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gin-sim.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

gin-sim is an interactive web dashboard that allows policymakers, researchers, and stakeholders to explore how different policy regimes affect:

- **Genetic testing uptake**
- **Insurance premiums**
- **Social welfare**
- **Market dynamics**

---

## 🚀 Quick Start

### Try the Live Demo

Visit our [Streamlit Cloud deployment](https://gin-sim.streamlit.app)

### Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/gin-sim.git
cd gin-sim

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## 📊 Features

### Interactive Controls

- **Policy Regime Selection**
  - Status Quo (full information use)
  - Moratorium (restricted use above caps)
  - Statutory Ban (no use permitted)

- **Parameter Adjustment**
  - Baseline testing uptake
  - Deterrence elasticity
  - Moratorium effect

### Visualizations

- Policy comparison charts
- Sensitivity analysis
- Interactive metrics

### Data Export

- Download policy comparison data (CSV)
- Export results for further analysis

---

## 📖 Documentation

### Model Overview

The dashboard implements a game-theoretic model of genetic discrimination in life insurance markets with the following modules:

1. **Module A**: Behavior/Deterrence - Testing participation decisions
2. **Module C**: Insurance Equilibrium - Premium setting under asymmetric information
3. **Module D**: Proxy Substitution - Insurer response to information constraints
4. **Module E**: Pass-Through - Market structure effects
5. **Module F**: Data Quality - Research participation externalities
6. **Enforcement**: Compliance - Regulatory enforcement

### Key Parameters

| Parameter | Base Value | Source |
|-----------|------------|--------|
| Baseline Testing Uptake | 0.52 | Ettema et al. (2021) |
| Deterrence Elasticity | 0.18 | McGuire et al. (2019) |
| Moratorium Effect | 0.15 | Taylor et al. (2021) |

### Usage Guide

1. **Select a Policy Regime** from the dropdown
2. **Adjust Parameters** using the sliders
3. **Explore Results** across four tabs:
   - **Results**: Key metrics and detailed tables
   - **Charts**: Interactive visualizations
   - **Comparison**: Side-by-side policy comparison
   - **Documentation**: Model documentation and references

---

## 🛠️ Development

### Testing

```bash
# Run E2E tests
python -m pytest tests/e2e/ -v
```

### Test Coverage

- ✅ Sidebar controls
- ✅ Tab rendering
- ✅ Computations accuracy
- ✅ Policy impact calculations

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

**Developer:** Dylan A. Mordaunt  
**Affiliation:** Victoria University of Wellington  
**Email:** dylan.mordaunt@vuw.ac.nz

---

## 🙏 Acknowledgments

This project is part of the Genetic Discrimination Policy Economic Evaluation research project.

---

**Dashboard v1.0 | Model v0.2.0**
