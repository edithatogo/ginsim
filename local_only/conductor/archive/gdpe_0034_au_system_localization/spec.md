# Track Specification: AU System Localization (Medicare & Oversight)

**Track ID:** gdpe_0034_au_system_localization
**Type:** Feature / Jurisdictional Rigor
**Goal:** Implement a 'Medicare Toggle' for testing costs and model the behavioral impact of ASIC/APRA regulatory oversight in Australia.

## 1. Overview
Australian stakeholders (Health/Treasury) requested more granular modeling of cost-sharing (Medicare) and the credibility of moratorium enforcement (ASIC/APRA). This track moves these from static multipliers to dynamic model parameters.

## 2. Functional Requirements
- **Medicare Toggle:** Add `medicare_cost_share: float` to `ModelParameters`. If set to 1.0, individual testing costs in `module_a_behavior.py` drop to zero (fully funded).
- **Oversight Modeling:** Model the expected penalty as a function of APRA/ASIC "Audit Intensity" rather than a generic `enforcement_effectiveness`.
- **AU-Specific Evidence:** Anchor all new parameters in the `australia_evidence_register.yaml`.

## 3. Acceptance Criteria
- [ ] Dashboard includes a "Medicare Testing Rebate" slider.
- [ ] Policy evaluations reflect the fiscal shift from individuals to the Commonwealth when rebates increase.
- [ ] Enforcement success is explicitly linked to APRA/ASIC audit intensity parameters.
