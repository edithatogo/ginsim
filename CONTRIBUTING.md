# Contributing to GINSIM

Thank you for your interest in contributing to the Genetic Discrimination Policy Integrated Economic Evaluation (GINSIM) project. We welcome contributions that improve the model structure, add new policy scenarios, or enhance the evidence registers.

## 🤝 Ways to Contribute

1.  **Report Issues:** Use the GitHub Issue tracker to report bugs or suggest improvements.
2.  **Add Policy Scenarios:** Propose new policy configurations in `configs/`.
3.  **Update Evidence:** Submit updates to the evidence registers in `context/jurisdiction_profiles/` with appropriate citations.
4.  **Enhance the Model:** Improve the JAX/NumPyro implementation in `src/`.

## 🛠️ Development Workflow

### Setup
1.  Fork and clone the repository.
2.  Create a virtual environment: `python -m venv .venv`.
3.  Install in editable mode with development dependencies: `pip install -e .`.

### Quality Standards
- **Linting:** Use `ruff check .`.
- **Formatting:** Use `ruff format .`.
- **Tests:** Run `pytest` to ensure no regressions.
- **Documentation:** All new features must include docstrings and be reflected in the Formulae Inventory or Game Descriptions.

### Submitting Changes
1.  Create a feature branch.
2.  Commit your changes with clear, descriptive messages.
3.  Submit a Pull Request.

## ⚖️ Code of Conduct
Please be respectful and professional in all interactions within this project.

---
**License:** By contributing, you agree that your contributions will be licensed under the MIT License.
