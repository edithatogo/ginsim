# Data Provenance and Transformation Log

## Purpose
Track the origin, transformations, and lineage of all data used in this research to ensure reproducibility and transparency.

---

## Data Inventory Template

### Dataset Registration

```yaml
dataset_id: "AU_testing_data"
title: "Australian Genetic Testing Utilisation Data"
version: "1.0"
registration_date: "YYYY-MM-DD"

# Source information
source_type: "Administrative data"  # Options: Administrative, Survey, Claims, Registry, Published, Synthetic
source_organization: "[Organization name]"
source_contact: "[Contact if applicable]"
source_url: "[URL if publicly available]"
access_conditions: "[Restrictions, data use agreements, etc.]"
license: "[CC-BY, restricted, etc.]"

# Temporal coverage
time_period_start: "YYYY-MM"
time_period_end: "YYYY-MM"
update_frequency: "Annual"  # or One-time, Quarterly, etc.

# Geographic coverage
geographic_coverage: "Australia"  # or "New Zealand", "Multi-country"

# Variables included
variables:
  - name: "test_date"
    type: "date"
    description: "Date of genetic test"
  - name: "test_type"
    type: "categorical"
    description: "Type of genetic test (diagnostic, predictive, carrier)"
  - name: "indication"
    type: "categorical"
    description: "Clinical indication for testing"
  - name: "age"
    type: "continuous"
    description: "Age at testing"
  - name: "sex"
    type: "categorical"
    description: "Sex/gender"

# Quality indicators
completeness: "Estimated 95% of all tests"
known_limitations: "Private testing not captured"
validation_status: "Validated against registry data"

# File information
file_path_raw: "data/raw/au_testing/raw_data.csv"
file_format: "CSV"
checksum_md5: "[md5 hash]"
file_size_mb: 45.2

# Access and governance
data_custodian: "[Name/role]"
access_approval_required: true
ethics_approval: "[Protocol number]"
data_use_agreement: "[Reference]"

# Related datasets
related_datasets:
  - "NZ_testing_data"
  - "AU_insurance_claims"
```

---

## Transformation Log

### Transformation Record

```yaml
transformation_id: "T001_au_testing_clean"
dataset_id: "AU_testing_data"
transformation_date: "YYYY-MM-DD"
transformer: "[Name/initials]"

# Input
input_file: "data/raw/au_testing/raw_data.csv"
input_version: "1.0"

# Output
output_file: "data/processed/au_testing_cleaned.csv"
output_version: "1.0"

# Transformation steps
steps:
  - step: 1
    operation: "Filter"
    description: "Retain only predictive genetic tests"
    code_reference: "scripts/etl/au_testing_etl.py:line_45"

  - step: 2
    operation: "Recoding"
    description: "Standardize test type codes to ontology"
    code_reference: "scripts/etl/au_testing_etl.py:line_62"

  - step: 3
    operation: "Date parsing"
    description: "Convert test_date to ISO 8601 format"
    code_reference: "scripts/etl/au_testing_etl.py:line_78"

  - step: 4
    operation: "Derived variable"
    description: "Calculate age at testing from DOB and test_date"
    code_reference: "scripts/etl/au_testing_etl.py:line_91"

  - step: 5
    operation: "Quality check"
    description: "Remove records with missing age or invalid dates"
    records_removed: 23
    code_reference: "scripts/etl/au_testing_etl.py:line_105"

# Validation
validation_checks:
  - check: "Record count"
    expected: ">1000"
    actual: 1227
    status: "PASS"
  - check: "Age range"
    expected: "18-100"
    actual: "18-94"
    status: "PASS"
  - check: "Date range"
    expected: "2015-2024"
    actual: "2016-2024"
    status: "PASS"

# Output checksum
output_checksum_md5: "[md5 hash]"

# Reproducibility
script_path: "scripts/etl/au_testing_etl.py"
script_version: "1.0"
python_version: "3.11"
dependencies:
  - "pandas==2.2.0"
  - "numpy==1.26.0"
execution_command: "python scripts/etl/au_testing_etl.py --input data/raw/... --output data/processed/..."
execution_timestamp: "2026-03-03T10:30:00+13:00"
random_seed: 42  # If applicable

# Notes
notes: "First complete ETL run. 23 records removed due to missing age."
```

---

## Data Lineage Diagram

```
Raw Data Sources                    Processed Data                    Model Inputs
────────────────                    ────────────                    ────────────

[AU Testing Raw] ──────────────┐
  (data/raw/au_testing/)        │
                                ▼
                                [AU Testing Cleaned] ──────────────┐
  (data/raw/nz_testing/)          (data/processed/)                 │
                                │                                   │
[NZ Testing Raw] ──────────────┤                                   │
                                │                                   ▼
                                │                            [Calibration Data]
[AU Insurance Claims] ──────────┤                             (outputs/calibration/)
                                │                                   │
  (data/raw/au_insurance/)      │                                   │
                                ▼                                   │
                                [AU Insurance Aggregated] ───────────┤
  (data/raw/nz_insurance/)        (data/processed/)                 │
                                │                                   │
[NZ Insurance Data] ────────────┘                                   │
                                                                    │
                                                                    ▼
                                                            [Module A: Behaviour]
                                                            [Module C: Insurance]
                                                            [Module D-F: Extensions]
```

---

## Data Access and Governance

### Access Levels

| Level | Description | Examples | Approval Required |
|-------|-------------|----------|-------------------|
| **Open** | Publicly available, no restrictions | Published summary statistics, government data | None |
| **Registered** | Available upon registration | Some survey data, aggregated insurance data | Email request |
| **Restricted** | Data use agreement required | Individual-level claims data | DUA + ethics |
| **Closed** | Not shareable | Identifiable health data | N/A (synthetic only) |

### Governance Checklist

For each dataset, confirm:
- [ ] Ethics approval covers intended use
- [ ] Data use agreement in place (if required)
- [ ] Privacy impact assessment completed (if needed)
- [ ] Data minimization applied (only necessary variables)
- [ ] De-identification verified (if individual-level)
- [ ] Storage meets security requirements
- [ ] Retention/destruction plan documented

---

## Synthetic Data Generation

For restricted datasets, generate synthetic exemplars:

```yaml
synthetic_dataset_id: "SYN_AU_testing"
source_dataset_id: "AU_testing_data"  # Reference to original (not shared)
generation_date: "YYYY-MM-DD"

# Method
method: "Differential privacy"  # or "Multiple imputation", "SMOTE", etc.
privacy_budget_epsilon: 1.0  # If DP
software: "synthpop R package"

# Validation
utility_checks:
  - "Marginal distributions match source"
  - "Correlation structure preserved"
  - "No exact matches to source records"

# Output
output_file: "data/synthetic/au_testing_synthetic.csv"
output_checksum_md5: "[hash]"

# Documentation
documentation: "docs/SYNTHETIC_DATA_GUIDE.md"
```

---

## File Naming Conventions

```
{jurisdiction}_{data_type}_{processing_level}_{version}.{ext}

Examples:
- au_testing_raw_v1.csv
- nz_insurance_cleaned_v2.parquet
- au_calibration_data_v1.csv
```

---

## Version Control

- **Raw data:** Never modified; new versions get new version numbers
- **Processed data:** Versioned with semantic versioning (MAJOR.MINOR.PATCH)
- **Code:** Git version control with tagged releases
- **Documentation:** Versioned alongside code

---

## References

- Wilkinson MD, et al. The FAIR Guiding Principles for scientific data management. Sci Data. 2016.
- Data Citation Synthesis Group. Joint Declaration of Data Citation Principles. 2014.
