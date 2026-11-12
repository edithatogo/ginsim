# Track Specification: Empirical 'Information Gap' Mapping

**Track ID:** gdpe_0035_empirical_information_gap
**Type:** Scientific Grounding
**Goal:** Map the abstract 'Information Gap' metric in Module D to empirical findings from the literature to improve model credibility for Nature/Lancet review.

## 1. Overview
Reviewers (Nature) identified that the "Information Gap" (the residual genetic information available via proxies) is currently too abstract. This track anchors that metric in specific studies of proxy underwriting accuracy.

## 2. Functional Requirements
- **Evidence Review:** Systematic search for papers quantifying the correlation between non-genetic factors (e.g., family history, medical history) and specific genetic risks (BRCA, Lynch).
- **Module D Calibration:** Update `module_d_proxy.py` to use these empirical correlations to bound the `proxy_substitution_rate`.
- **Transparency:** Surface the empirical source for each "Gap" calculation in the dashboard.

## 3. Acceptance Criteria
- [ ] Every "Information Gap" calculation in the dashboard is linked to at least one empirical citation.
- [ ] `module_d_proxy.py` logic updated to reflect real-world underwriting accuracy loss.
