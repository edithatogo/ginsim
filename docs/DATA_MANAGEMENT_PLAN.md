# Data Management Plan

**Track:** gdpe_0004_quality_assurance  
**Version:** 1.0  
**Date:** 2026-03-03

---

## 1. Overview

This document outlines data management procedures for the genetic discrimination policy economic evaluation.

---

## 2. Data Types

### 2.1 Model Parameters

**Source:** Evidence registers (systematic literature review)

**Format:** YAML configuration files

**Location:** `configs/calibration_*.yaml`

**Access:** Open (public repository)

### 2.2 Policy Configurations

**Source:** Policy documents (FSC moratorium, legislation)

**Format:** YAML configuration files

**Location:** `configs/policies*.yaml`

**Access:** Open (public repository)

### 2.3 Model Outputs

**Source:** Model simulations

**Format:** 
- NumPy arrays (.npy)
- JSON files
- CSV tables

**Location:** `outputs/results/`

**Access:** Open (public repository)

### 2.4 Bibliography

**Source:** Systematic literature search

**Format:** BibTeX

**Location:** `context/references.bib`

**Access:** Open (public repository)

---

## 3. Data Collection

### 3.1 Literature Search

**Databases:**
- PubMed
- EconLit
- Scopus
- Google Scholar

**Search Terms:**
- "genetic discrimination" AND "insurance"
- "adverse selection" AND "genetic testing"
- "moratorium" AND "genetic information"

**Inclusion Criteria:**
- English language
- 2010-2026
- Empirical or modelling studies
- Relevant to genetic discrimination in insurance

### 3.2 Data Extraction

**Process:**
1. Extract parameter estimates
2. Assess evidence quality (GRADE)
3. Convert to prior distributions
4. Document in evidence registers

**Template:** `context/jurisdiction_profiles/*_evidence_register.yaml`

---

## 4. Data Processing

### 4.1 Parameter Conversion

**Method:** Evidence-to-prior mapping

**Documentation:** `docs/EVIDENCE_TO_PRIOR_MAPPING.md`

**Quality Control:**
- All conversions documented
- Rationale provided
- Uncertainty quantified

### 4.2 Model Runs

**Method:** Batch execution with run manifests

**Manifest Contents:**
- Git commit hash
- Timestamp
- Config file hash
- Parameter values
- Random seed

**Location:** `outputs/runs/<timestamp>/run_manifest.json`

---

## 5. Data Storage

### 5.1 Repository Structure

```
genetic-discrimination-policy-econ/
├── configs/              # Configuration files
├── context/              # Evidence registers, references
├── docs/                 # Documentation
├── outputs/              # Model outputs
│   ├── results/          # Simulation results
│   ├── figures/          # Figures (1200dpi PNG + SVG)
│   └── runs/             # Run manifests
├── src/                  # Source code
└── tests/                # Tests
```

### 5.2 Backup

**Primary:** Git repository (GitHub/GitLab)

**Secondary:** Zenodo deposition (DOI assignment)

**Frequency:** 
- Git: Continuous (each commit)
- Zenodo: At major releases

---

## 6. Data Sharing

### 6.1 Open Data

**Scope:**
- All model parameters
- All model outputs
- All documentation
- All code

**License:** 
- Code: MIT License
- Data: CC-BY 4.0
- Documentation: CC-BY 4.0

### 6.2 Restrictions

**None:** All data is synthetic or from public sources.

**Note:** No individual-level data is used or stored.

---

## 7. Data Quality

### 7.1 Validation

**Methods:**
- Automated tests (pytest)
- Code review (GitHub PRs)
- Reproducibility checks (run manifests)

**Coverage Target:** ≥95% code coverage

### 7.2 Version Control

**System:** Git

**Branching:**
- `main`: Stable releases
- `develop`: Development branch
- `feature/*`: Feature branches

**Tagging:** Semantic versioning (v1.0.0, v1.1.0, etc.)

---

## 8. Documentation

### 8.1 Code Documentation

**Standard:** Docstrings for all public functions

**Format:** Google-style docstrings

**Example:**
```python
def compute_evpi(net_benefits: np.ndarray, optimal_net_benefit: float) -> float:
    """
    Compute Expected Value of Perfect Information.
    
    Args:
        net_benefits: Array of net benefits for each policy
        optimal_net_benefit: Net benefit under current optimal decision
        
    Returns:
        EVPI value
    """
```

### 8.2 User Documentation

**Files:**
- `README.md` - Project overview
- `docs/` - Detailed documentation
- `conductor/` - Track documentation

---

## 9. Compliance

### 9.1 FAIR Principles

**Findable:**
- DOI assignment (Zenodo)
- Rich metadata
- Searchable repository

**Accessible:**
- Open access repository
- Standard protocols (HTTP, Git)
- No authentication required

**Interoperable:**
- Standard formats (YAML, JSON, CSV)
- Controlled vocabularies (GRADE)
- Community standards (CHEERS 2022)

**Reusable:**
- Clear licenses
- Detailed documentation
- Provenance tracking

### 9.2 Ethical Considerations

**Ethics Approval:** Not required (no primary data collection)

**Conflicts of Interest:** None declared

**Funding:** [To be declared]

---

## 10. Timeline

| Activity | Date | Status |
|----------|------|--------|
| Data management plan | 2026-03-03 | ✅ Complete |
| Literature search | 2026-03-10 | ⏳ In progress |
| Data extraction | 2026-03-17 | ⏳ Pending |
| Model runs | 2026-03-24 | ⏳ Pending |
| Zenodo deposition | 2026-04-14 | ⏳ Pending |

---

## 11. Responsibilities

**Data Management:** Dylan A Mordaunt

**Code Quality:** Dylan A Mordaunt

**Documentation:** Dylan A Mordaunt

**Review:** [Pending expert review]

---

## 12. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial version |

---

**END OF DATA MANAGEMENT PLAN**
