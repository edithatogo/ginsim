# Implementation Plan: Quality Assurance and Publication Readiness

**Track ID:** gdpe_0004_quality_assurance  
**Type:** Quality Assurance + Infrastructure  
**Estimated duration:** 2-3 weeks  
**Dependencies:** gdpe_0003_model_implementation (Phases 1-4 complete)

---

## Phase 1 — Code Quality (Week 1)

**Goal:** Achieve publication-quality code standards

### Tasks
- [ ] **Task 1.1:** Test coverage analysis
  - Run coverage.py on full test suite
  - Identify modules <95% coverage
  - Add tests for uncovered code
  - Document any justified exceptions

- [ ] **Task 1.2:** Ruff strict configuration
  - Update pyproject.toml with strict rules
  - Fix all linting violations
  - Configure pre-commit hook

- [ ] **Task 1.3:** Pyright strict typing
  - Configure pyright with strict mode
  - Add type hints where missing
  - Fix all type errors
  - Configure pre-commit hook

- [ ] **Task 1.4:** Pre-commit hooks setup
  - Configure .pre-commit-config.yaml
  - Include: ruff, pyright, coverage check
  - Test hooks on sample commit

**Acceptance criteria:**
- Test coverage ≥95%
- Ruff passes with strict configuration
- Pyright passes with strict configuration
- Pre-commit hooks installed and working

---

## Phase 2 — Artefact Audit (Week 1-2)

**Goal:** Ensure all required artefacts are present and meet guidelines

### Tasks
- [ ] **Task 2.1:** Download publication guidelines
  - CHEERS 2022 checklist
  - ISPOR-SMDM modelling guidelines
  - Target journal author guidelines (Value in Health, MDM, JHE)
  - OSF presubmission checklist

- [ ] **Task 2.2:** Artefact inventory
  - List all existing artefacts
  - Categorize by type (protocol, code, data, outputs, documentation)
  - Map to guideline requirements

- [ ] **Task 2.3:** Gap analysis
  - Identify missing artefacts
  - Identify artefacts needing updates
  - Prioritize by importance

- [ ] **Task 2.4:** Produce missing artefacts
  - Create missing documentation
  - Update incomplete artefacts
  - Verify against guidelines

**Acceptance criteria:**
- All guidelines downloaded and catalogued
- Complete artefact inventory
- Gap analysis completed
- Missing artefacts produced

---

## Phase 3 — Repository Structure (Week 2)

**Goal:** Separate code and study artefacts for flexible synchronization

### Tasks
- [ ] **Task 3.1:** Design submodule structure
  - Code submodule (public, syncable)
  - Study artefacts submodule (private/sensitive)
  - Shared configuration

- [ ] **Task 3.2:** Create submodules
  - Initialize code submodule
  - Initialize study artefacts submodule
  - Configure .gitmodules

- [ ] **Task 3.3:** Migrate existing content
  - Move code to code submodule
  - Move study artefacts to study submodule
  - Update import paths

- [ ] **Task 3.4:** Configure sync settings
  - Document sync procedures
  - Test code-only sync
  - Test full sync

**Acceptance criteria:**
- Submodule structure implemented
- All content migrated
- Sync procedures documented and tested

---

## Phase 4 — Reference Mapping (Week 2)

**Goal:** Ensure all inputs and assumptions are properly referenced

### Tasks
- [ ] **Task 4.1:** Inventory inputs and assumptions
  - Extract from model code
  - Extract from config files
  - Extract from documentation

- [ ] **Task 4.2:** Map to references
  - Link each input to ≥2 references where possible
  - Document evidence quality (GRADE)
  - Flag inputs with insufficient references

- [ ] **Task 4.3:** Create canonical CSL-JSON
  - Consolidate all references
  - Remove duplicates
  - Validate CSL-JSON schema
  - Cross-reference with inputs

- [ ] **Task 4.4:** Address gaps
  - Search for additional references
  - Document unavoidable gaps
  - Sensitivity analysis for uncertain inputs

**Acceptance criteria:**
- All inputs mapped to references
- All assumptions mapped to references
- ≥2 references per input (where available)
- Canonical CSL-JSON created and validated

---

## Phase 5 — Output Management (Week 3)

**Goal:** Ensure all outputs are publication-ready

### Tasks
- [ ] **Task 5.1:** Output inventory
  - List all tables
  - List all plots
  - List all diagnostic outputs
  - Map to model components

- [ ] **Task 5.2:** Format conversion
  - Convert all plots to 1200dpi PNG
  - Convert all plots to SVG
  - Ensure colorblind-safe palettes
  - Verify font sizes for publication

- [ ] **Task 5.3:** Table formatting
  - Ensure publication-suitable formatting
  - Add uncertainty intervals
  - Format per journal guidelines
  - Add notes and sources

- [ ] **Task 5.4:** Diagnostic plots
  - MCMC convergence diagnostics
  - Posterior predictive checks
  - Sensitivity analysis tornado plots
  - VOI results visualization

- [ ] **Task 5.5:** Versioning and organization
  - Implement version numbering
  - Organize in intuitive directory structure
  - Create index/manifest file
  - Document naming conventions

**Acceptance criteria:**
- All outputs mapped and catalogued
- All plots in 1200dpi PNG + SVG
- All tables publication-suitable
- Diagnostic plots complete
- Versioning system implemented
- Intuitive organization documented

---

## Summary Timeline

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| **Phase 1** | Week 1 | 95% coverage, strict ruff/pyright, pre-commit hooks |
| **Phase 2** | Week 1-2 | Guidelines downloaded, artefact audit, gaps filled |
| **Phase 3** | Week 2 | Submodule structure, sync configuration |
| **Phase 4** | Week 2 | Reference mapping, CSL-JSON bibliography |
| **Phase 5** | Week 3 | Output management, 1200dpi/SVG, diagnostics |

---

## Resource Requirements

### Computational
- Storage: ~5GB for high-resolution outputs
- CI/CD: Coverage testing integration

### Tools
- coverage.py
- ruff
- pyright
- Zotero/BibTeX
- ImageMagick

---

## Risks and Mitigation

| Risk | Mitigation |
|------|-----------|
| Test coverage <95% | Prioritize critical modules; document exceptions |
| Missing artefacts | Create templates; produce systematically |
| Submodule complexity | Document workflow; test sync procedures |
| Reference mapping incomplete | Systematic audit; flag gaps |
| Output conversion time | Automate conversion pipeline |

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0004_quality_assurance
