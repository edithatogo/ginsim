# Data Provenance and Transformation Log

**Track:** gdpe_0002_evidence_anchoring — Phase 3
**Date:** 2026-03-03
**Version:** 1.0

---

## Overview

This document tracks the origin, transformations, and lineage of all data used in this research project.

**Current Status:** Phase 1-3 use publicly available aggregate data and published studies. No individual-level data accessed yet.

---

## Current Data Inventory (Phase 1-3)

### Public Aggregate Data

| Dataset | Source | Type | Access | Use |
|---------|--------|------|--------|-----|
| FSC Moratorium documents | Financial Services Council | Policy | Public | Evidence register |
| HRC Inquiry Report | Human Rights Commission | Report | Public | Evidence register |
| APRA insurance statistics | APRA | Aggregate | Public | Context |
| Published studies | Various journals | Literature | Public | Evidence registers |

**Provenance:** All sources publicly available, no transformation required.

---

## Future Data Inventory (Phase 4+)

### Australia

#### MBS Genetic Testing Data

**Registration:**
```yaml
dataset_id: "AU_testing_001"
title: "Medicare Benefits Schedule Genetic Testing Data"
version: "1.0"
registration_date: "TBD"

# Source information
source_type: "Administrative"
source_organization: "Department of Health and Aged Care"
access_conditions: "Research application required"
license: "Crown Copyright"

# Temporal coverage
time_period_start: "2015-01"
time_period_end: "Present"
update_frequency: "Monthly"

# Variables (expected)
variables:
  - name: "service_date"
    type: "date"
    description: "Date of service"
  - name: "mbs_item_code"
    type: "categorical"
    description: "MBS item number"
  - name: "patient_age"
    type: "continuous"
    description: "Age at service"
  - name: "patient_sex"
    type: "categorical"
    description: "Sex"
  - name: "state"
    type: "categorical"
    description: "State/territory"

# File information (expected)
file_path_raw: "data/raw/au_mbs/testing_data.csv"
file_format: "CSV"
checksum_md5: "[to be computed]"

# Access and governance
data_custodian: "Department of Health"
access_approval_required: true
ethics_approval: "[TBD]"
```

**Transformation Plan:**
```yaml
transformation_id: "T001_au_mbs_clean"
dataset_id: "AU_testing_001"

# Input
input_file: "data/raw/au_mbs/testing_data.csv"

# Output
output_file: "data/processed/au_mbs_cleaned.parquet"

# Transformation steps
steps:
  - step: 1
    operation: "Date parsing"
    description: "Convert service_date to ISO 8601"

  - step: 2
    operation: "Filter"
    description: "Retain genetic testing MBS items only"
    codes: ["73300", "73301", "73302", "..."]

  - step: 3
    operation: "Aggregate"
    description: "Monthly counts by item code"

  - step: 4
    operation: "Quality check"
    description: "Verify no missing dates, codes"

# Validation
validation_checks:
  - check: "Record count"
    expected: ">0"
  - check: "Date range"
    expected: "2015-present"
  - check: "Missing values"
    expected: "0"
```

---

### New Zealand

#### National Genetic Testing Database

**Registration:**
```yaml
dataset_id: "NZ_testing_001"
title: "National Genetic Testing Database"
version: "1.0"
registration_date: "TBD"

# Source information
source_type: "Administrative"
source_organization: "Lablink / National Health Board"
access_conditions: "Research application to NHB"
license: "Crown Copyright"

# Temporal coverage
time_period_start: "2010-01"
time_period_end: "Present"
update_frequency: "Quarterly"

# Variables (expected)
variables:
  - name: "test_date"
    type: "date"
    description: "Date of test"
  - name: "test_type"
    type: "categorical"
    description: "Type of genetic test"
  - name: "indication"
    type: "categorical"
    description: "Clinical indication"
  - name: "result"
    type: "categorical"
    description: "Test result (de-identified)"
  - name: "ethnicity"
    type: "categorical"
    description: "Ethnic group"

# File information (expected)
file_path_raw: "data/raw/nz_testing/testing_data.csv"
file_format: "CSV"
checksum_md5: "[to be computed]"

# Access and governance
data_custodian: "National Health Board"
access_approval_required: true
ethics_approval: "[TBD]"
maori_data_sovereignty: true
```

---

## Data Lineage Diagram

```
Phase 1-3 (Current)
===================

Public Sources → Evidence Registers → Calibration Configs → Model
     ↓                  ↓                    ↓              ↓
  FSC, HRC,      YAML files          YAML configs     Prior draws
  APRA, Journals

Phase 4+ (Planned)
==================

Raw Data → Cleaned Data → Analysis Data → Model Outputs
   ↓           ↓              ↓              ↓
MBS,       Parquet        Aggregated     Posterior
Lablink    files          tables         draws
```

---

## File Naming Conventions

```
{jurisdiction}_{data_type}_{processing_level}_{version}.{ext}

Examples:
- au_testing_raw_v1.csv
- nz_insurance_cleaned_v2.parquet
- au_calibration_data_v1.csv
- au_posterior_draws_v1.npy
```

---

## Version Control

### Data Versions

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-03 | Evidence registers (Phase 1) |
| v1.1 | 2026-03-03 | Calibration configs (Phase 2) |
| v2.0 | TBD | Administrative data (Phase 4) |

### Code Versions

- Git commit hash recorded in run manifests
- Semantic versioning for releases
- CHANGELOG.md tracks changes

---

## Quality Assurance

### Automated Checks

**Reference Validation:**
```bash
python -m scripts.validate_references --report
```

**Data Validation (when data accessed):**
```python
# Checksums
md5sum data/raw/*.csv > data/checksums.txt

# Validation script
python scripts/validate_data.py --dataset AU_testing_001
```

### Manual Checks

- [ ] Source data matches expected format
- [ ] Transformation logic verified
- [ ] Output counts reasonable
- [ ] No unexpected missing values
- [ ] Date ranges correct

---

## Reproducibility

### Run Manifests

Each analysis run generates a manifest:

```json
{
  "timestamp": "2026-03-03T14:00:00+13:00",
  "jurisdiction": "australia",
  "config_hash": "abc123...",
  "git_commit": "def456...",
  "data_versions": {
    "evidence_registers": "v1.0",
    "calibration": "v1.1"
  },
  "n_draws": 2000,
  "random_seed": 20260303
}
```

### Environment

```yaml
python: "3.10+"
dependencies:
  - numpy: ">=1.26"
  - pandas: ">=2.2"
  - jax: ">=0.4.25"
  - numpyro: ">=0.15.0"
  - pyyaml: ">=6.0"
```

---

## Data Access Log

### Current Access (Phase 1-3)

| Date | User | Dataset | Purpose | Approved |
|------|------|---------|---------|----------|
| - | - | - | - | - |

*No individual-level data accessed yet*

### Future Access (Phase 4+)

| Date | User | Dataset | Purpose | Approved |
|------|------|---------|---------|----------|
| TBD | PI | MBS testing | Event study | Pending |
| TBD | PI | NZ testing | Event study | Pending |

---

## Security Measures

### Current (Phase 1-3)

- Public data only
- No special security required
- Standard password protection

### Future (Phase 4+)

**Required:**
- Encrypted storage (AES-256)
- Named user access only
- Access logging
- Secure deletion after project

**Prohibited:**
- Personal devices for data access
- Cloud storage without approval
- Onward sharing without permission

---

## References

- Wilkinson MD et al. The FAIR Guiding Principles. Sci Data. 2016.
- Data Citation Synthesis Group. Joint Declaration of Data Citation Principles. 2014.
- Te Mana Raraunga. Māori Data Sovereignty Principles. 2019.

---

**Version:** 1.0
**Date:** 2026-03-03
**Track:** gdpe_0002_evidence_anchoring
