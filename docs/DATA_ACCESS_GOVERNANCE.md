# Data Access and Governance Appendix

**Track:** gdpe_0002_evidence_anchoring — Phase 3
**Date:** 2026-03-03
**Version:** 1.0

---

## Overview

This appendix documents data access requirements, governance frameworks, and ethical considerations for the genetic discrimination policy evaluation project.

---

## Data Classification

### Sensitivity Levels

| Level | Description | Examples | Handling Requirements |
|-------|-------------|----------|---------------------|
| **Public** | No restrictions | Aggregate statistics, published papers | No special handling |
| **Internal** | Project use only | Analysis code, draft documents | Password protection |
| **Restricted** | Ethics approval required | De-identified individual data | Secure storage, access log |
| **Highly Restricted** | Data use agreement required | Linked administrative data | Encrypted, named users only |

### Current Project Data

| Data Type | Classification | Storage | Access |
|-----------|---------------|---------|--------|
| Evidence registers | Public | Git repository | Open |
| Calibration configs | Public | Git repository | Open |
| Analysis code | Public | Git repository | Open |
| Bibliography | Public | Git repository | Open |
| Model outputs (aggregated) | Public | Git repository (excludes raw data) | Open |
| Raw administrative data | Highly Restricted | Not yet accessed | N/A |

---

## Ethics Requirements

### Australia

**Human Research Ethics:**
- Required: Yes (for primary data collection)
- Not required: Secondary analysis of public data
- Body: University HREC or NHRMC-certified committee

**Data Access:**
- MBS data: Department of Health application
- Cancer Registry: AIHW + state/territory approval
- Timeframe: 8-12 weeks

**Key Guidelines:**
- National Statement on Ethical Conduct in Human Research (2007, updated 2018)
- NHMRC Guidelines for Human Research

### New Zealand

**Human Research Ethics:**
- Required: Yes (for primary data collection)
- Not required: Audit/evaluation of existing services
- Body: HDEC or low-risk ethics committee

**Data Access:**
- Genetic Testing Database: National Health Board application
- Cancer Registry: Health Quality & Safety Commission
- IDM: Stats NZ DataLab approval
- Timeframe: 6-10 weeks

**Key Guidelines:**
- Ethical Standards for Psychologists (if applicable)
- HDEC Operating Standard
- Privacy Act 2020

---

## Māori Data Sovereignty

### Te Mana Raraunga Principles

For research involving Māori genetic data or health information:

1. **Rangatiratanga** — Māori have an inherent right to control Māori data
2. **Whai Rawa** — Māori have ownership rights over data and information
3. **Kotahitanga** — Māori data sovereignty is collective and individual
4. **Manaakitanga** — Data use should enhance Māori collective mana
5. **Tiakitanga** — Data should be stored and used responsibly
6. **Tino Rangatiratanga** — Māori should exercise authority over data

### Implications for This Research

**Current Phase (1-3):**
- No individual-level Māori data accessed
- Aggregate data only (public sources)
- Acknowledgment of principles in documentation

**Future Phases (if accessing individual data):**
- Māori governance involvement required
- Clear benefit to Māori must be demonstrated
- Partnership with Māori researchers/organizations
- Adherence to tikanga (Māori protocols)

**Actions Taken:**
- Principles acknowledged in NZ evidence register
- Commitment to Māori researcher partnership (Phase 2 reflexive journal)
- No Māori data accessed without governance

---

## Privacy Act Compliance

### Australia

**Privacy Act 1988 (Cth):**
- Australian Privacy Principles (APPs) apply
- Genetic information = sensitive information
- Requires explicit consent for collection/use

**Research Exemptions:**
- Public interest research may be exempt
- Requires ethics approval
- De-identification required where possible

### New Zealand

**Privacy Act 2020:**
- Information Privacy Principles (IPPs) apply
- Genetic information not separately classified
- Requires lawful purpose for collection

**Health Information Privacy Code 2020:**
- Specific rules for health information
- Access, correction, and disclosure rules
- Research provisions available

---

## Data Sharing Agreements

### Required Agreements (Future Phases)

| Data Source | Agreement Type | Parties | Status |
|-------------|---------------|---------|--------|
| MBS testing data | Data License | Dept Health + Researcher | Not yet negotiated |
| Cancer Registry | Data Access Agreement | AIHW + Researcher | Not yet negotiated |
| Genetic Testing Database | Data Sharing Agreement | NHB + Researcher | Not yet negotiated |
| HRC complaints data | Confidentiality Agreement | HRC + Researcher | Not yet negotiated |

### Standard Clauses

**Typical requirements:**
- Named users only
- Secure storage (encrypted, password-protected)
- No re-identification attempts
- Destruction after project completion
- Reporting breaches within 24 hours
- No onward sharing without permission

---

## Security Measures

### Current (Phase 1-3)

**Data Storage:**
- Git repository (public data only)
- University OneDrive (working documents)
- No individual-level data stored

**Access Control:**
- Principal investigator only (single-author project)
- No external access granted

**Security Measures:**
- Password-protected devices
- Encrypted storage (OneDrive)
- Regular backups

### Future (Phase 4+, if accessing restricted data)

**Required Security:**
- Encrypted storage (AES-256)
- Named user access only
- Access logging
- Secure deletion after project
- No cloud storage without approval

**Infrastructure:**
- University secure research environment
- Stats NZ DataLab (for NZ IDM data)
- No personal devices for data access

---

## Data Retention and Destruction

### Retention Periods

| Data Type | Retention Period | Rationale |
|-----------|-----------------|-----------|
| Research data (individual-level) | 5 years post-project | NHMRC requirement |
| Ethics documentation | 5 years post-project | Compliance |
| Publications | Permanent | Academic record |
| Code | Permanent (via GitHub) | Reproducibility |

### Destruction Methods

**Electronic Data:**
- Secure deletion (DoD 5220.22-M standard)
- Certificate of destruction
- Log of destroyed files

**Physical Data:**
- Cross-cut shredding
- Secure disposal service
- Certificate of destruction

---

## Breach Response Plan

### Breach Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Low** | Internal error, no data exposure | 7 days |
| **Medium** | Potential exposure, limited scope | 48 hours |
| **High** | Confirmed exposure, individual data | 24 hours |
| **Critical** | Confirmed exposure, sensitive data | Immediate |

### Response Procedures

**For High/Critical Breaches:**

1. **Contain** — Secure systems, prevent further exposure
2. **Assess** — Determine scope, affected data, individuals
3. **Notify** — Ethics committee, data custodian, affected individuals
4. **Mitigate** — Password resets, credit monitoring if needed
5. **Review** — Root cause analysis, prevent recurrence
6. **Document** — Full incident report

### Notification Requirements

**Australia:**
- OAIC (Office of the Australian Information Commissioner)
- Affected individuals
- Ethics committee

**New Zealand:**
- OPC (Office of the Privacy Commissioner)
- Affected individuals
- HDEC (if health data)

---

## Governance Checklist

### Before Data Access

- [ ] Ethics approval obtained
- [ ] Data use agreement signed
- [ ] Security measures in place
- [ ] Named users trained
- [ ] Storage approved
- [ ] Backup procedures documented
- [ ] Destruction plan confirmed

### During Project

- [ ] Access logged
- [ ] Regular security audits
- [ ] Breach procedures tested
- [ ] Data minimization practiced
- [ ] Only necessary data accessed

### After Project Completion

- [ ] Data destroyed per agreement
- [ ] Certificates obtained
- [ ] Final report to custodian
- [ ] Publications archived
- [ ] Code made available (if permitted)

---

## Contact Information

### Australia

**Ethics:**
- University Human Research Ethics Committee
- Email: [ethics@university.edu.au]

**Data Custodians:**
- MBS: Department of Health [data.request@health.gov.au]
- Cancer Registry: AIHW [data@aihw.gov.au]

**Regulators:**
- NHMRC [grants@nhmrc.gov.au]
- OAIC [privacy@oaic.gov.au]

### New Zealand

**Ethics:**
- HDEC [hdec@moh.govt.nz]
- Low-risk ethics: [ethics@university.ac.nz]

**Data Custodians:**
- Genetic Testing: National Health Board [contact@nhb.govt.nz]
- Cancer Registry: HQSC [data@hqsc.govt.nz]
- IDM: Stats NZ [datalab@stats.govt.nz]

**Regulators:**
- HDEC [hdec@moh.govt.nz]
- OPC [privacy@privacy.org.nz]

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-03 | Initial version |

---

**END OF DATA ACCESS AND GOVERNANCE APPENDIX**
