# Specification: Model Implementation and Policy Analysis

**Track ID:** gdpe_0003_model_implementation  
**Type:** Research + Implementation  
**Duration:** 6-8 weeks  
**Dependencies:** gdpe_0002_evidence_anchoring (complete - provides calibrated priors)

---

## Goal

Implement the full game-theoretic economic model for genetic discrimination policy analysis, replacing all placeholder simulations with actual equilibrium calculations, and produce evidence-based policy recommendations for Australia and New Zealand.

---

## Problem Statement

The previous track (gdpe_0002_evidence_anchoring) established the evidence base and calibration framework, but **did not implement the actual game-theoretic model**. All policy scenario results currently use placeholder simulations.

This track delivers the **actual implementation** needed to:
1. Quantify policy impacts on testing uptake, premiums, and welfare
2. Identify optimal policy regimes for AU and NZ
3. Produce peer-reviewed publication
4. Inform government policy decisions

---

## Strategic Interactions to Model

Based on `GAME_THEORETIC_FRAMING.md`, five strategic "games" must be implemented:

### Game 1: Adverse Selection (Module C)
**Players:** Applicants (informed), Insurers (uninformed), Regulator  
**Mechanism:** Rothschild-Stiglitz screening model with policy constraints  
**Equilibrium:** Separating/pooling equilibrium under different information regimes  
**Policy lever:** Information restrictions (ban/moratorium/caps)

### Game 2: Testing Participation (Module A)
**Players:** Individuals, Insurers (downstream penalty), Policymakers  
**Mechanism:** Strategic participation under discrimination risk  
**Equilibrium:** Testing uptake as function of perceived penalty  
**Policy lever:** Discrimination protections

### Game 3: Proxy Substitution (Module D)
**Players:** Insurers (constrained optimization), Applicants  
**Mechanism:** Insurer re-optimization under information constraints  
**Equilibrium:** New underwriting rules using allowed proxies  
**Policy lever:** Scope of information restrictions

### Game 4: Data Quality Externality (Module F)
**Players:** Individuals (participation), Researchers, Health system  
**Mechanism:** Public goods problem (participation benefits future patients)  
**Equilibrium:** Participation rate as function of privacy protections  
**Policy lever:** Privacy protections, research exemptions

### Game 5: Enforcement/Compliance (Enforcement Module)
**Players:** Insurers, Regulator, Applicants  
**Mechanism:** Compliance game with monitoring and penalties  
**Equilibrium:** Compliance rate as function of enforcement strength  
**Policy lever:** Enforcement resources, penalty severity

---

## Technical Requirements

### Module A: Behavior/Deterrence
**Current:** Placeholder formula  
**Required:** Structural discrete choice model
```
U(test) = α + β·benefits - γ·perceived_penalty + ε
perceived_penalty = f(policy_regime, enforcement_strength)
```
**Implementation:**
- Logit/probit model of testing choice
- Policy regime enters via perceived_penalty term
- Calibrated to evidence register priors

### Module C: Insurance Equilibrium
**Current:** Placeholder formula  
**Required:** Rothschild-Stiglitz equilibrium solver
```
High-risk demand: D_H(p) = f(p, information_availability)
Low-risk demand: D_L(p) = f(p, information_availability)
Insurer zero-profit: p_H·D_H + p_L·D_L = expected_claims
Equilibrium: No profitable deviation
```
**Implementation:**
- Solve for separating equilibrium (when information allowed)
- Solve for pooling equilibrium (when information restricted)
- Compute premium divergence between regimes
- Use JAX for root-finding

### Module D: Proxy Substitution
**Current:** Fixed substitution rate  
**Required:** Constrained optimization
```
max Underwriting_accuracy(feature_set)
s.t. feature_set ⊆ Allowed_features (policy constraint)
```
**Implementation:**
- Logistic regression or ML model for risk prediction
- Policy removes genetic_test_result from feature set
- Model re-optimizes using remaining features
- Compute accuracy loss vs. privacy gain

### Module F: Data Quality
**Current:** Fixed participation elasticity  
**Required:** Public goods game
```
Participation_rate = g(privacy_protections, social_benefit_perception)
Data_quality = h(participation_rate, selection_bias)
Research_value = i(data_quality)
```
**Implementation:**
- Participation as function of privacy protections
- Selection bias model (who opts out)
- Impact on predictive model performance

### Enforcement Module
**Current:** Fixed compliance rate  
**Required:** Compliance game
```
Insurer payoff: Profit(violation) - Penalty·detection_probability
Detection_probability = f(enforcement_resources, monitoring_intensity)
Equilibrium compliance: Mixed strategy Nash equilibrium
```
**Implementation:**
- Detection probability from enforcement strength
- Penalty severity from policy regime
- Solve for equilibrium compliance rate

---

## Integration Requirements

### Policy Scenario Encoding
Each policy regime encoded as:
```yaml
policy_regime:
  allow_genetic_tests: true/false/limited
  enforcement_strength: 0.0-1.0
  sum_insured_caps: {death: 500000, tpd: 200000, trauma: 200000}
  penalties: {fine_max: 1000000, license_revocation: true/false}
```

### Module Integration
```
Policy rules → Module A (testing choice)
            → Module C (insurance equilibrium)
            → Module D (proxy optimization)
            → Module F (data quality)
            → Module E (pass-through)
            → DCBA ledger (welfare aggregation)
            → VOI/EVPPI (uncertainty analysis)
```

### Output Requirements
For each policy scenario:
- Testing uptake change (absolute, relative, 95% CrI)
- Premium changes by risk group (95% CrI)
- Insurance take-up changes (95% CrI)
- QALYs gained/lost (95% CrI)
- Net welfare impact (95% CrI)
- EVPI/EVPPI (research prioritization)

---

## Acceptance Criteria

### Code Implementation
- [ ] All 5 games implemented with actual equilibrium calculations
- [ ] Zero placeholder simulations remaining
- [ ] All modules integrated into unified pipeline
- [ ] JAX/XLA acceleration for MCMC and root-finding
- [ ] Unit tests for all equilibrium solvers
- [ ] Integration tests for full pipeline

### Validation
- [ ] Stress tests pass (8 scenarios)
- [ ] Posterior predictive checks show good calibration
- [ ] Cross-validation against published studies (≥3 studies)
- [ ] Face validity review (≥2 expert reviewers)

### Policy Results
- [ ] Results generated for 3 policy scenarios (status quo, moratorium, ban)
- [ ] Results for both AU and NZ
- [ ] Uncertainty quantified (95% credible intervals)
- [ ] VOI analysis identifies research priorities

### Dissemination
- [ ] Manuscript submitted to peer-reviewed journal
- [ ] Policy brief prepared for government stakeholders
- [ ] Code and data deposited in Zenodo (with DOI)
- [ ] Presentation materials for conferences

---

## Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Equilibrium solvers fail to converge | Medium | High | Use multiple initialization points; fallback to approximate solutions |
| Results inconsistent with literature | Low | High | Cross-validate at each module; adjust model structure if needed |
| Computational cost too high | Medium | Medium | Use JAX acceleration; reduce draws for initial runs |
| Policy results inconclusive | Medium | High | Ensure adequate statistical power; focus on parameters with low uncertainty |

---

## Success Metrics

**Technical:**
- 100% of placeholder simulations replaced
- All equilibrium solvers converge in <100 iterations
- MCMC R-hat <1.1 for all parameters
- Runtime <4 hours for full policy sweep (2000 draws)

**Research:**
- Manuscript submitted to Q1 journal (Value in Health, MDM, or JHE)
- Code DOI assigned via Zenodo
- ≥2 expert reviewers validate model structure

**Policy:**
- Policy brief delivered to AU/NZ government stakeholders
- Clear recommendations on optimal policy regime
- VOI analysis guides future research funding

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0003_model_implementation
