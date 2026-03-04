# Study Submodule README

# Genetic Discrimination Policy Study - Australia & New Zealand

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.TODO.svg)](https://doi.org/10.5281/zenodo.TODO)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Study artefacts for the economic evaluation of genetic discrimination policies in Australia and New Zealand.

## Contents

- **Evidence Registers:** Systematic evidence reviews for AU and NZ
- **Calibration Configs:** Parameter priors from evidence
- **Model Outputs:** Results from policy analysis
- **Documentation:** Statistical analysis plan, data management plan
- **Protocols:** OSF presubmission, study protocol

## Quick Start

### Load Evidence

```python
import yaml

# Load Australia evidence
with open('evidence/australia_evidence_register.yaml') as f:
    au_evidence = yaml.safe_load(f)

# Load NZ evidence
with open('evidence/new_zealand_evidence_register.yaml') as f:
    nz_evidence = yaml.safe_load(f)
```

### Load Calibration

```python
from src.model.config_serialization import load_config

# Load Australia calibration
au_config = load_config('calibration/calibration_australia.yaml')

# Load NZ calibration
nz_config = load_config('calibration/calibration_new_zealand.yaml')
```

## Documentation

- [Statistical Analysis Plan](docs/STATISTICAL_ANALYSIS_PLAN.md)
- [Data Management Plan](docs/DATA_MANAGEMENT_PLAN.md)
- [Artefact Audit](docs/ARTEFACT_AUDIT.md)
- [Evidence-to-Prior Mapping](docs/EVIDENCE_TO_PRIOR_MAPPING.md)

## License

CC-BY 4.0 - See [LICENSE](LICENSE) for details.

## Citation

If you use these study results, please cite:

```
Mordaunt, D. A. (2026). Economic Evaluation of Genetic Discrimination 
Policies in Australia and New Zealand [Data set]. 
Zenodo. https://doi.org/10.5281/zenodo.TODO
```

## Access

This submodule contains study-specific artefacts. For the model code, see:

https://github.com/yourusername/genetic-discrimination-policy-code

## Contact

Dylan A. Mordaunt  
Victoria University of Wellington  
dylan.mordaunt@vuw.ac.nz
