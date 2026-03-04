# Repository Structure Guide

**Track:** gdpe_0004_quality_assurance  
**Phase:** 3 — Repository Structure  
**Date:** 2026-03-03

---

## Overview

This document describes the repository structure for separating code from study artefacts, enabling code synchronization without study-specific data.

---

## Directory Structure

```
genetic-discrimination-policy-econ/
├── .git/                          # Git repository
├── .gitmodules                    # Submodule configuration
│
├── code/                          # Code submodule (public, syncable)
│   ├── src/                       # Source code
│   │   ├── __init__.py
│   │   ├── model/                 # Model modules
│   │   │   ├── __init__.py
│   │   │   ├── parameters.py
│   │   │   ├── rng.py
│   │   │   ├── module_a_behavior.py
│   │   │   ├── module_c_insurance_eq.py
│   │   │   ├── module_d_proxy.py
│   │   │   ├── module_enforcement.py
│   │   │   ├── module_f_data_quality.py
│   │   │   ├── pipeline.py
│   │   │   ├── voi_analysis.py
│   │   │   ├── sensitivity.py
│   │   │   ├── config_serialization.py
│   │   │   └── dcba_ledger.py
│   │   └── utils/
│   ├── scripts/                   # Runnable scripts
│   │   ├── __init__.py
│   │   ├── run_meta_pipeline.py
│   │   ├── run_policy_sweep.py
│   │   ├── run_voi.py
│   │   ├── run_stress_tests.py
│   │   └── validate_references.py
│   ├── tests/                     # Tests
│   │   ├── __init__.py
│   │   ├── unit/
│   │   └── integration/
│   ├── configs/                   # Configuration templates
│   │   ├── base.yaml
│   │   └── policies.yaml
│   ├── pyproject.toml             # Python package config
│   ├── README.md                  # Code documentation
│   └── LICENSE                    # MIT License
│
├── study/                         # Study submodule (private/sensitive)
│   ├── evidence/                  # Evidence registers
│   │   ├── australia_evidence_register.yaml
│   │   ├── new_zealand_evidence_register.yaml
│   │   └── references.bib
│   ├── calibration/               # Calibration configs
│   │   ├── calibration_australia.yaml
│   │   └── calibration_new_zealand.yaml
│   ├── outputs/                   # Model outputs
│   │   ├── results/
│   │   ├── figures/
│   │   └── runs/
│   ├── docs/                      # Study documentation
│   │   ├── STATISTICAL_ANALYSIS_PLAN.md
│   │   ├── DATA_MANAGEMENT_PLAN.md
│   │   ├── ARTEFACT_AUDIT.md
│   │   └── EVIDENCE_TO_PRIOR_MAPPING.md
│   └── protocols/                 # Protocols
│       ├── OSF_Presubmission_Protocol_v1.0.*
│       └── Protocol_GeneticDiscriminationPolicy_v1.0.*
│
└── conductor/                     # Project management (stays in main repo)
    ├── tracks/
    ├── product.md
    ├── tech-stack.md
    ├── workflow.md
    └── product-guidelines.md
```

---

## Submodule Configuration

### .gitmodules

```git
[submodule "code"]
    path = code
    url = https://github.com/yourusername/genetic-discrimination-policy-code.git
    update = checkout

[submodule "study"]
    path = study
    url = https://github.com/yourusername/genetic-discrimination-policy-study.git
    update = checkout
```

---

## Synchronization Procedures

### Sync Code Only (Public)

```bash
# Initialize code submodule
git submodule update --init code

# Update code submodule
cd code
git pull origin main
cd ..

# Commit submodule update
git add code
git commit -m "Update code submodule to latest"
```

### Sync Study Only (Private/Restricted)

```bash
# Initialize study submodule
git submodule update --init study

# Update study submodule
cd study
git pull origin main
cd ..

# Commit submodule update
git add study
git commit -m "Update study submodule to latest"
```

### Full Sync

```bash
# Initialize all submodules
git submodule update --init --recursive

# Update all submodules
git submodule update --remote --merge

# Commit updates
git add code study
git commit -m "Update all submodules"
```

---

## Access Control

### Code Submodule (Public)

**Access:** Open access

**License:** MIT License

**Contents:**
- Source code
- Scripts
- Tests
- Configuration templates
- Code documentation

### Study Submodule (Restricted)

**Access:** Restricted (as needed)

**License:** CC-BY 4.0 (for public outputs)

**Contents:**
- Evidence registers
- Calibration configs
- Model outputs
- Study documentation
- Protocols

**Note:** No individual-level data stored. All data is from public sources or synthetic.

---

## Rationale

### Why Separate?

1. **Different audiences:**
   - Code: Developers, researchers wanting to use the model
   - Study: Policy analysts, stakeholders interested in AU/NZ results

2. **Different update frequencies:**
   - Code: Infrequent (major releases)
   - Study: Frequent (analysis updates, new evidence)

3. **Different access requirements:**
   - Code: Fully open
   - Study: Some outputs may be embargoed until publication

4. **Different citation needs:**
   - Code: Cite software DOI
   - Study: Cite study results DOI

---

## Migration Plan

### Phase 1: Create Submodules (Week 2)

1. Create `code/` repository
2. Create `study/` repository
3. Move files to appropriate submodules
4. Configure `.gitmodules`
5. Test synchronization

### Phase 2: Test and Document (Week 2)

1. Test all sync procedures
2. Update README with submodule instructions
3. Document access procedures
4. Train team on workflow

### Phase 3: Deploy (Week 3)

1. Push submodules to GitHub
2. Update CI/CD for submodules
3. Set up Zenodo DOIs for each submodule
4. Announce new structure

---

## Acceptance Criteria

- [ ] Code submodule created and tested
- [ ] Study submodule created and tested
- [ ] `.gitmodules` configured correctly
- [ ] Sync procedures documented
- [ ] README updated with submodule instructions
- [ ] All tests pass in new structure
- [ ] CI/CD configured for submodules

---

## Next Steps

1. Create GitHub repositories for submodules
2. Move files to appropriate submodules
3. Configure and test
4. Document and train

---

**Status:** Ready for implementation.
