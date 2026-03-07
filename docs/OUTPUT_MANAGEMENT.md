# Output Management Guide

**Track:** gdpe_0004_quality_assurance  
**Phase:** 5 — Output Management  
**Date:** 2026-03-03

---

## Overview

This document describes the output management framework for reporting tables, figures, captions, and diagnostic plots. The active reporting path is driven by `scripts/reporting_common.py`, `scripts/generate_figures.py`, and `scripts/publish_pack.py`.

For a reviewer-facing summary of the main manuscript/package assets, see `docs/MANUSCRIPT_ASSET_INVENTORY.md`.

---

## Output Inventory

### Tables

| ID | Description | Location | Format | Status |
|----|-------------|----------|--------|--------|
| **T1** | Parameter table (all modules) | `outputs/tables/parameters.csv` | CSV | ⏳ Template ready |
| **T2** | Policy comparison table | `outputs/tables/policy_comparison.csv` | CSV | ⏳ Template ready |
| **T3** | VOI results table | `outputs/tables/voi_results.csv` | CSV | ⏳ Template ready |
| **T4** | Sensitivity analysis table | `outputs/tables/sensitivity.csv` | CSV | ⏳ Template ready |
| **T5** | Evidence quality summary | `outputs/tables/evidence_quality.csv` | CSV | ⏳ Template ready |

### Figures

| ID | Description | Location | Formats | Status |
|----|-------------|----------|---------|--------|
| **F1** | Policy net-benefit ranking | `<publish_pack>/figures/<jurisdiction>_net_benefit` | PNG | ✅ Active |
| **F2** | EVPPI by parameter group | `<publish_pack>/figures/<jurisdiction>_evppi` | PNG | ✅ Active |
| **F3** | Uncertainty decomposition | `<publish_pack>/figures/<jurisdiction>_uncertainty_decomposition` | PNG | ✅ Active |
| **F4** | Figure captions | `<publish_pack>/figures/*_caption.md` | Markdown | ✅ Active |

### Diagnostic Plots

| ID | Description | Location | Formats | Status |
|----|-------------|----------|---------|--------|
| **D1** | MCMC convergence (trace plots) | `outputs/diagnostics/mcmc_traces` | PNG (1200dpi), SVG | ⏳ Template ready |
| **D2** | MCMC convergence (R-hat) | `outputs/diagnostics/mcmc_rhat` | PNG (1200dpi), SVG | ⏳ Template ready |
| **D3** | Posterior predictive checks | `outputs/diagnostics/ppc` | PNG (1200dpi), SVG | ⏳ Template ready |
| **D4** | Prior vs posterior | `outputs/diagnostics/prior_posterior` | PNG (1200dpi), SVG | ⏳ Template ready |

---

## Format Specifications

### PNG

**Purpose:** Reporting and manuscript drafting raster images

**Settings:**
- Resolution: 300 dpi in the active publish pack; higher-resolution export remains a follow-up option
- Color mode: RGB
- Compression: Lossless (PNG)
- Font: Sans-serif (Arial/Helvetica)
- Font size: ≥8pt for labels

**Use cases:**
- Journal submissions (most require raster)
- Presentations
- Web display

### SVG

**Purpose:** Vector graphics for infinite scalability

**Settings:**
- Format: SVG 1.1
- Font: Embedded or converted to paths
- Colors: sRGB color space

**Use cases:**
- Supplementary materials
- Posters
- Further editing in Illustrator/Inkscape

---

## Colorblind-Safe Palettes

### Primary Palette (Okabe-Ito)

```python
OKABE_ITO = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'bluish_green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermilion': '#D55E00',
    'reddish_purple': '#CC79A7',
    'black': '#000000',
}
```

### Sequential Palette (Viridis)

```python
# For continuous data
VIRIDIS = ['#440154', '#30678D', '#35B779', '#FDE725']
```

### Diverging Palette (RdBu)

```python
# For positive/negative effects
RDBU = ['#053061', '#4393C3', '#FFFFFF', '#D6604D', '#B2182B']
```

---

## Table Templates

### T1: Parameter Table

```csv
parameter,module,mean,sd,ci_lower,ci_upper,distribution,source,quality
baseline_testing_uptake,A,0.52,0.02,0.48,0.56,Beta,Ettema et al. 2021,Moderate
deterrence_elasticity,A,0.18,0.035,0.11,0.25,Beta,McGuire et al. 2019,Low
...
```

### T2: Policy Comparison Table

```csv
policy,testing_uptake,premium_change,welfare_impact,qalys_gained,fiscal_impact
status_quo,0.52,0.00,0,0,0
moratorium,0.58,0.02,150000,120,-50000
ban,0.62,0.05,250000,180,-80000
```

---

## Figure Generation Pipeline

### Step 1: Run Model

```bash
python -m scripts.run_meta_pipeline --n_draws 2000 --output outputs/runs/meta_20260303
```

### Step 2: Generate Tables

```bash
python -m scripts.generate_tables --run_dir outputs/runs/meta_20260303 --output outputs/tables
```

### Step 3: Generate Figures

```bash
python -m scripts.generate_figures --meta_dir outputs/runs/meta_pipeline/<timestamp> --output outputs/figures --dpi 300 --formats png
```

### Step 4: Generate Diagnostics

```bash
python -m scripts.generate_diagnostics --run_dir outputs/runs/meta_20260303 --output outputs/diagnostics --dpi 1200 --formats png svg
```

---

## Versioning

### Directory Structure

```
outputs/
├── runs/
│   └── meta_20260303_143022/
│       ├── run_manifest.json
│       └── posterior_samples.npy
├── tables/
│   ├── v1.0/
│   │   ├── parameters.csv
│   │   └── policy_comparison.csv
│   └── latest -> v1.0/
├── figures/
│   ├── v1.0/
│   │   ├── policy_comparison.png
│   │   └── policy_comparison.svg
│   └── latest -> v1.0/
└── diagnostics/
    ├── v1.0/
    └── latest -> v1.0/
```

### Version Naming

- **v1.0:** Initial reporting outputs
- **v1.1:** Label/caption corrections
- **v2.0:** Major updates (new analysis, additional scenarios)

---

## Publication Suitability Checklist

### Tables

- [ ] All values have appropriate precision
- [ ] Uncertainty intervals included (95% CI)
- [ ] Units specified
- [ ] Notes section with abbreviations
- [ ] Source citations included
- [ ] CHEERS 2022 compliant

### Figures

- [ ] Resolution appropriate to intended use and regenerated at submission quality when needed
- [ ] Caption file generated for each publication-facing figure
- [ ] Colorblind-safe palette
- [ ] Font size ≥8pt
- [ ] Axis labels with units
- [ ] Legend clear and concise
- [ ] No chart junk

### Diagnostics

- [ ] MCMC convergence verified (R-hat <1.1)
- [ ] Effective sample size adequate (ESS >400)
- [ ] Prior-posterior comparison shown
- [ ] PPC results interpretable

---

## Acceptance Criteria

- [ ] All 5 tables generated
- [ ] All active publish-pack figures and captions generated
- [ ] All 4 diagnostic plots generated (PNG + SVG)
- [ ] Colorblind-safe palettes used
- [ ] Versioning system implemented
- [ ] Publication suitability verified

---

## Next Steps

1. Generate tables, figures, and captions from the reporting bundle
2. Review metric labels, units, and figure captions
3. Regenerate higher-resolution or vector assets if a submission venue requires them
4. Version and organize
5. Document in manuscript

---

**Status:** Active reporting path implemented; broader manuscript harmonization still in progress.
