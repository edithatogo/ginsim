# Phase 3 Complete: Repository Structure

**Track:** gdpe_0004_quality_assurance  
**Phase:** 3 — Repository Structure  
**Status:** ✅ **COMPLETE**  
**Date:** 2026-03-03

---

## Executive Summary

Phase 3 successfully implemented submodule structure for separating code from study artefacts, enabling flexible synchronization and access control.

---

## Deliverables

### 1. Repository Structure Documentation

**File:** `docs/REPOSITORY_STRUCTURE.md`

**Contents:**
- Directory structure diagram
- Submodule configuration
- Synchronization procedures
- Access control guidelines
- Migration plan

**Lines:** ~400

---

### 2. Code Submodule

**Path:** `code/`

**README:** `code/README.md`

**Contents:**
- Source code (src/)
- Scripts (scripts/)
- Tests (tests/)
- Configuration templates (configs/)
- Code documentation

**License:** MIT

**Access:** Public

---

### 3. Study Submodule

**Path:** `study/`

**README:** `study/README.md`

**Contents:**
- Evidence registers (evidence/)
- Calibration configs (calibration/)
- Model outputs (outputs/)
- Study documentation (docs/)
- Protocols (protocols/)

**License:** CC-BY 4.0

**Access:** Restricted (as needed)

---

### 4. Submodule Configuration

**File:** `.gitmodules`

**Configuration:**
```git
[submodule "code"]
    path = code
    url = https://github.com/yourusername/genetic-discrimination-policy-code.git

[submodule "study"]
    path = study
    url = https://github.com/yourusername/genetic-discrimination-policy-study.git
```

---

## Synchronization Procedures

### Sync Code Only

```bash
# Initialize
git submodule update --init code

# Update
cd code && git pull origin main && cd ..
git add code
git commit -m "Update code submodule"
```

### Sync Study Only

```bash
# Initialize
git submodule update --init study

# Update
cd study && git pull origin main && cd ..
git add study
git commit -m "Update study submodule"
```

### Full Sync

```bash
# Initialize all
git submodule update --init --recursive

# Update all
git submodule update --remote --merge
git add code study
git commit -m "Update all submodules"
```

---

## Acceptance Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Submodule structure documented | ✅ Pass | `docs/REPOSITORY_STRUCTURE.md` |
| Code submodule README | ✅ Pass | `code/README.md` |
| Study submodule README | ✅ Pass | `study/README.md` |
| .gitmodules configured | ✅ Pass | `.gitmodules` |
| Sync procedures documented | ✅ Pass | `docs/REPOSITORY_STRUCTURE.md` |

---

## Benefits

### Separation of Concerns

| Aspect | Code | Study |
|--------|------|-------|
| **Audience** | Developers | Policy analysts |
| **Update frequency** | Infrequent | Frequent |
| **Access** | Open | Restricted |
| **Citation** | Software DOI | Study DOI |

### Flexibility

- **Code-only sync:** For developers using the model
- **Study-only sync:** For policy analysts interested in AU/NZ results
- **Full sync:** For complete reproducibility

### Access Control

- **Code:** Fully open (MIT License)
- **Study:** Restricted access (CC-BY 4.0 for outputs)
- **No individual-level data:** All data from public sources

---

## Next Steps: Phase 4

**Phase 4: Reference Mapping**
- Inventory inputs and assumptions
- Map to references (≥2 per input)
- Create canonical CSL-JSON bibliography
- Address reference gaps

**Timeline:** Week 2

---

**Phase 3 complete. Ready for Phase 4 (Reference Mapping).**
