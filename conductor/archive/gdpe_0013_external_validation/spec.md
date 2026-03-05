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
- **Experts:** Simulate feedback from 4 expert personas.
- **Advanced Metrics Audit:** Explicitly review the logic for:
    1. **Distributional Cost-Effectiveness (DCEA):** Is the breakdown of winners/losers plausible?
    2. **Participation Thresholds:** Does the "uninsured rate" response align with actuarial data?
    3. **Enforcement Net Benefit:** Is the "Return on Investment" for regulation correctly modeled?
    4. **Scientific Opportunity Cost:** Is the translation of "research participation" into "medical progress delay" credible?
    5. **Political Time-Horizons (NEW):** Does the model clearly separate short-term fiscal costs from long-term health savings?

### Phase 2: Empirical Cross-Validation, Global Audit & Proxy Accuracy
- **Comparison:** Cross-validate against studies from the **US, UK, and Canada**.
- **Historical Concordance (NEW):** Cross-reference simulated expert critiques against actual public submissions from the 2023 Australian Parliamentary Inquiry and Canadian GNDA debates.
- **Proxy "Reconstruction Accuracy" Audit:** Cross-validate the 40% (default) "Information Leakage" accuracy against diagnostic studies (e.g., Tabor et al. 2018).
- **International Logic Mapping:** Technical audit of the translation of GINA (US), GNDA (Canada), and ABI Code (UK) into model boolean logic.
- **Structural Sensitivity:** Test the impact of "Step-Function" vs. "Linear Elasticity" across the international scenarios.

### Phase 3: Final Synthesis & Publication Readiness
- **Integration:** Update model assumptions, priors, or structure based on validation findings.
- **Documentation:** Finalize the Model Validation Report (`docs/MODEL_VALIDATION_REPORT.md`).
- **Sign-off:** Final review of the repository against "Publication Ready" standards.

### 2.5 Parallel Synchronization Protocol (CRITICAL)
- **Dynamic Gating:** Tasks in `gdpe_0013` that depend on `gdpe_0012` outputs MUST verify those outputs exist before execution.
- **Change Propagation:** If `gdpe_0012` results in a structural change, Expert Reviewers MUST be "re-briefed".

---

## 3. Expert Persona Anchoring Briefs

To ensure high-signal, critical feedback, the simulated experts are anchored with specific technical biases and concerns:

| Persona | Technical Anchor / Bias | Primary Concern |
|---------|-------------------------|-----------------|
| **Health Economist** | Welfare-maximizing; focus on QALYs and research externalities. | **Time Dynamics (NEW):** Critiques whether the model accurately reflects the delay between immediate policy costs and long-term health gains. |
| **Insurance Actuary** | Market stability; focus on premium adequacy and adverse selection. | **Adversarial Fairness (NEW):** Audits the XLA gradient solver; does insurer ML re-optimization on proxies disproportionately penalize noisy/sparse baseline data? |
| **Policy Expert** | Regulatory compliance; focus on legal "spirit" and enforcement. | **Political Viability (NEW):** Evaluates if the enforcement ROI metrics map to realistic 3-4 year election cycle budgeting. |
| **Indigenous Specialist** | Data sovereignty; focus on Māori and First Nations equity. | **Algorithmic Bias (NEW):** Audits if proxy-based "Information Leakage" introduces algorithmic bias against Indigenous populations due to historical health data disparities. |



---

## 4. GRADE-Weighted Validation Logic
- **Priority:** Experts MUST disproportionately focus their review on parameters and modules marked as **"Very Low"** or **"Low"** quality in the Evidence Registers (`AU_behav_002`, `NZ_all`).
- **Justification:** Validation effort must be inversely proportional to evidence quality.


---

**Version:** 1.0  
**Date:** 2026-03-04  
**Status:** Active
