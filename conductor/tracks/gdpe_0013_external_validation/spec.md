# Track Specification: External Validation (Simulated Expert Review & Cross-Validation)

**Track ID:** gdpe_0013_external_validation  
**Type:** Validation & Synthesis  
**Estimated duration:** 3-4 weeks  
**Dependencies:** gdpe_0002_evidence_anchoring (completed), gdpe_0003_model_implementation (completed)

---

## 1. Objective
Formalize the model's external validation through simulated expert face-validity reviews and empirical cross-validation against published literature. This track addresses the remaining 20% of validation work identified in Phase 4 of the project.

## 2. Scope

### Phase 1: Simulated Expert Face-Validity Review
- **Experts:** Simulate feedback from 4 distinct expert personas:
    1. **Health Economist:** Focus on QALYs, welfare aggregation, and VOI.
    2. **Insurance Actuary:** Focus on adverse selection, pooling vs. separating equilibria, and premium setting.
    3. **Genetic Policy Expert:** Focus on deterrence, moratorium effects, and privacy/discrimination.
    4. **Indigenous Data Governance Specialist:** Review handling of proxy data (Module D) and implications for Māori and Aboriginal/Torres Strait Islander equity in AU/NZ models.
- **Protocol:** Use `protocols/face_validity_review_package.md` to generate structured feedback.
- **Deliverable:** Consolidated Expert Review Report and Action Log.

### Phase 2: Empirical Cross-Validation & Australian Prior Audit
- **Comparison:** Cross-validate model outputs against 5 key studies:
    1. **Hersch & Viscusi (2019):** Adverse selection in life insurance.
    2. **Bombard et al. (2018):** Deterrence effects of genetic discrimination.
    3. **Taylor et al. (2021):** Australian insurance market behavior.
    4. **Armstrong et al. (2020):** Genetic testing uptake under different regimes.
    5. **Lowenstein (2021):** Comparative policy analysis.
- **Australian Prior Audit:**
    - Perform a sensitivity audit on **Australia-specific priors** (`AU_behav_001` and `AU_ins_003`).
    - Verify if the direction of Australian policy advice (Ban vs. Moratorium) is stable across the 95% credible intervals of these priors.
- **Deliverable:** Cross-Validation & Prior Sensitivity Report.


### Phase 3: Final Synthesis & Publication Readiness
- **Integration:** Update model assumptions, priors, or structure based on validation findings.
- **Documentation:** Finalize the Model Validation Report (`docs/MODEL_VALIDATION_REPORT.md`).
- **Sign-off:** Final review of the repository against "Publication Ready" standards.

## 3. Success Criteria
- [ ] 3 simulated expert reviews completed and documented.
- [ ] Cross-validation against 5 studies shows acceptable alignment (discrepancies explained).
- [ ] Action log items addressed in the codebase or documentation.
- [ ] Final validation report signed off by the "Conductor" process.

## 4. Resource Requirements
- **Context:** Access to `docs/MODEL_CARD.md`, `context/assumptions_registry.yaml`, and `configs/calibration_*.yaml`.
- **Expertise:** AI-driven simulation of domain-specific expertise.
- **Tools:** `run_shell_command` for model runs if calibration adjustments are needed.

---

**Version:** 1.0  
**Date:** 2026-03-04  
**Status:** Active
