# Specification: Quality Assurance and Publication Readiness

**Track ID:** gdpe_0004_quality_assurance  
**Type:** Quality Assurance + Infrastructure  
**Estimated duration:** 2-3 weeks  
**Dependencies:** gdpe_0003_model_implementation (Phases 1-4 complete)

---

## Goal

Ensure the repository meets publication-quality standards for code quality, testing, documentation, and artefact management before manuscript preparation.

---

## Scope

This track covers:

1. **Code Quality**
   - 95% test coverage target
   - Strict ruff configuration
   - Strict pyright typing
   - Pre-commit hooks

2. **Artefact Audit**
   - Download publication guidelines/checklists
   - Audit existing artefacts against guidelines
   - Produce missing artefacts

3. **Repository Structure**
   - Separate code and study artefacts (submodules)
   - Enable code sync without study data

4. **Reference Mapping**
   - Map all inputs/assumptions to references (≥2 per input)
   - Create canonical CSL-JSON bibliography

5. **Output Management**
   - Map all outputs (tables, plots)
   - Ensure 1200dpi PNG + SVG formats
   - Publication-suitable formatting
   - Versioning and organization
   - Diagnostic plots

---

## Strategic Importance

This track ensures:
- **Reproducibility:** All outputs traceable to inputs
- **Publication readiness:** All artefacts meet journal standards
- **Maintainability:** Clean separation of code and data
- **Quality:** Strict typing and testing standards
- **Transparency:** All assumptions referenced

---

## Phases

### Phase 1: Code Quality (Week 1)
- Test coverage analysis and improvement
- Ruff strict configuration
- Pyright strict typing
- Pre-commit hooks setup

### Phase 2: Artefact Audit (Week 1-2)
- Download guidelines (CHEERS 2022, ISPOR-SMDM, etc.)
- Audit existing artefacts
- Produce missing artefacts

### Phase 3: Repository Structure (Week 2)
- Create submodule structure
- Separate code from study artefacts
- Configure sync settings

### Phase 4: Reference Mapping (Week 2)
- Map inputs/assumptions to references
- Create canonical CSL-JSON
- Verify ≥2 references per input

### Phase 5: Output Management (Week 3)
- Map all outputs
- Convert to 1200dpi PNG + SVG
- Ensure publication suitability
- Add diagnostic plots
- Version and organize

---

## Acceptance Criteria

### Code Quality
- [ ] Test coverage ≥95%
- [ ] Ruff set to strict mode
- [ ] Pyright set to strict mode
- [ ] Pre-commit hooks configured and working

### Artefact Audit
- [ ] Guidelines downloaded (CHEERS 2022, ISPOR-SMDM, etc.)
- [ ] Artefact audit completed
- [ ] Missing artefacts produced

### Repository Structure
- [ ] Code/study submodule separation complete
- [ ] Sync configuration tested

### Reference Mapping
- [ ] All inputs mapped to references
- [ ] All assumptions mapped to references
- [ ] ≥2 references per input/assumption
- [ ] Canonical CSL-JSON created

### Output Management
- [ ] All outputs mapped
- [ ] All plots in 1200dpi PNG + SVG
- [ ] All tables publication-suitable
- [ ] Diagnostic plots present
- [ ] Versioning system in place
- [ ] Intuitive organization

---

## Resource Requirements

### Computational
- Storage for high-resolution outputs (~5GB)
- CI/CD for coverage testing

### Expertise
- Publication guidelines knowledge
- Git submodule management
- CSL-JSON bibliography management

### Tools
- Coverage.py
- Ruff
- Pyright
- Zotero/BibTeX for CSL-JSON
- ImageMagick for DPI conversion

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
