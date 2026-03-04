# Specification: Formulae Verification and Documentation

**Track ID:** gdpe_0006_formulae_verification  
**Type:** Feature  
**Date:** 2026-03-03

---

## 1. Overview

This track identifies, verifies, references, and documents all mathematical formulae used in the genetic discrimination policy evaluation model, producing a comprehensive formulae report.

---

## 2. Scope

### 2.1 Formulae Categories

1. **Behavioral Model Formulae** (Module A)
   - Testing utility functions
   - Perceived penalty calculations
   - Uptake probability functions

2. **Insurance Equilibrium Formulae** (Module C)
   - Premium calculations
   - Demand elasticity functions
   - Equilibrium conditions

3. **Proxy Substitution Formulae** (Module D)
   - Risk score calculations
   - Accuracy metrics
   - Substitution rate functions

4. **Pass-Through Formulae** (Module E)
   - Market structure equations
   - Pass-through rate calculations

5. **Data Quality Formulae** (Module F)
   - Participation functions
   - Externality calculations

6. **Enforcement Formulae**
   - Detection probability
   - Expected penalty calculations
   - Compliance rate functions

7. **VOI/Sensitivity Formulae**
   - EVPI calculations
   - EVPPI calculations
   - Sensitivity indices

---

## 3. Functional Requirements

### 3.1 Formulae Identification

- [ ] **FR1:** Extract all formulae from source code
- [ ] **FR2:** Extract all formulae from documentation
- [ ] **FR3:** Create formula inventory with unique IDs
- [ ] **FR4:** Categorize formulae by module

### 3.2 Formulae Verification

- [ ] **FR5:** Verify mathematical correctness of each formula
- [ ] **FR6:** Verify implementation matches mathematical specification
- [ ] **FR7:** Verify dimensional consistency
- [ ] **FR8:** Verify boundary conditions

### 3.3 Referencing

- [ ] **FR9:** Add academic references for each formula
- [ ] **FR10:** Ensure ≥1 reference per formula
- [ ] **FR11:** Add to CSL-JSON bibliography
- [ ] **FR12:** Cross-reference with code

### 3.4 Documentation

- [ ] **FR13:** Write formula descriptions (100-200 words each)
- [ ] **FR14:** Document variable definitions
- [ ] **FR15:** Document assumptions
- [ ] **FR16:** Document units/dimensions

### 3.5 Report

- [ ] **FR17:** Produce comprehensive formulae report (30-50 pages)
- [ ] **FR18:** Include formulae by category
- [ ] **FR19:** Include verification results
- [ ] **FR20:** Include references

---

## 4. Acceptance Criteria

- [ ] **AC1:** All formulae identified and catalogued (≥50 formulae)
- [ ] **AC2:** All formulae verified with documented results
- [ ] **AC3:** All formulae referenced (≥1 reference each)
- [ ] **AC4:** Formulae report complete (30-50 pages)
- [ ] **AC5:** CSL-JSON updated with formulae references

---

## 5. Deliverables

| ID | Deliverable | Format | Location |
|----|-------------|--------|----------|
| D1 | Formulae inventory | CSV/Markdown | `docs/FORMULAE_INVENTORY.md` |
| D2 | Verification report | PDF/Markdown | `docs/FORMULAE_VERIFICATION_REPORT.md` |
| D3 | Updated bibliography | CSL-JSON | `study/references/references.json` |
| D4 | Formulae extraction script | Python | `scripts/extract_formulae.py` |

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Status:** Ready for planning
