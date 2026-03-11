# Jurisdictional Expansion Guide: SOTA Comparative Roadmap

**Date:** 2026-03-08  
**Context:** Based on Simulated Stakeholder Meeting #1 (Nature, Lancet, Treasury, MoH).

## 1. Executive Summary
To elevate GINSIM beyond the Australia/New Zealand context, we recommend adding the **United Kingdom (UK)** and **Canada** as comparative benchmarks. These jurisdictions represent the two primary regulatory pathways currently under debate in ANZ.

## 2. Priority Jurisdictions

### #1 United Kingdom (Voluntary Moratorium / ABI Agreement)
- **Rationale:** The UK has the world's most mature voluntary code between the government and the Association of British Insurers (ABI).
- **Required Inputs:** 
    - ABI Code of Practice limits.
    - UK-specific disease prevalence (Lynch, BRCA).
    - NHS-specific prevention costs.
- **Value:** Provides a 'Lower Bound' for the effectiveness of self-regulation vs. legislation.

### #2 Canada (Statutory Ban / Genetic Non-Discrimination Act)
- **Rationale:** Canada represents the 'Pure Ban' path, with legislated protections that survived high-court challenges.
- **Required Inputs:**
    - GNDA legislative constraints.
    - Provincial-level health cost variations.
- **Value:** Provides an 'Upper Bound' for public confidence and testing uptake.

### #3 United States (HIPAA/GINA / Fragmented Regulation)
- **Rationale:** Significant data available, but the fragmented, employer-linked health system is less directly applicable to the ANZ public-payer context.
- **Value:** Useful for stress-testing 'extreme' information leakage scenarios.

## 3. Implementation Roadmap

1.  **Metadata Definition:** Add `jurisdiction_id: uk` and `jurisdiction_id: canada` to the policy engine.
2.  **Evidence Anchoring:** Create `local_only/context/jurisdiction_profiles/uk_evidence_register.yaml`.
3.  **Visual Alignment:** Implement a "Global Benchmarking" toggle in the Streamlit dashboard.
