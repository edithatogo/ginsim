# Study Submodule README

# Genetic Discrimination Policy Study - Australia & New Zealand

[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Study artefacts for the economic evaluation of genetic discrimination policies in Australia and New Zealand.

DOI note: Zenodo deposition metadata is not finalized in this working tree. Do not cite a Zenodo DOI from this file until a real DOI has been assigned.

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
with open('context/jurisdiction_profiles/australia_evidence_register.yaml') as f:
    au_evidence = yaml.safe_load(f)

# Load NZ evidence
with open('context/jurisdiction_profiles/new_zealand_evidence_register.yaml') as f:
    nz_evidence = yaml.safe_load(f)
```

### Load Calibration

```python
import yaml

# Load Australia calibration
with open('configs/calibration_australia.yaml') as f:
    au_config = yaml.safe_load(f)

# Load NZ calibration
with open('configs/calibration_new_zealand.yaml') as f:
    nz_config = yaml.safe_load(f)
```

## Documentation

- [Statistical Analysis Plan](docs/STATISTICAL_ANALYSIS_PLAN.md)
- [Data Management Plan](docs/DATA_MANAGEMENT_PLAN.md)
- [Artefact Audit](docs/ARTEFACT_AUDIT.md)
- [Evidence-to-Prior Mapping](docs/EVIDENCE_TO_PRIOR_MAPPING.md)

## License

CC-BY 4.0 - See [LICENSE](LICENSE) for details.

## Citation

If you use these study results, cite the repository metadata or manuscript record that is current at the time of use. A dataset DOI placeholder should not be cited.

Working citation metadata is maintained in:
- `CITATION.cff`
- `.zenodo.json`
- `study/references/references.json`

## Access

The study artefacts and model code live in the same repository. The core implementation is in:
- `src/model/`
- `streamlit_app/`
- `configs/`

## Contact

Dylan A Mordaunt  
Research Fellow, Faculty of Health, Education and Psychology, Victoria University of Wellington  
dylan.mordaunt@vuw.ac.nz
