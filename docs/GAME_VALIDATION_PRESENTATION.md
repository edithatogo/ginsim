# Game Validation Presentation

**Track:** gdpe_0005_game_validation  
**Date:** 2026-03-03  
**Version:** 1.0

---

## Slide 1: Title Slide

**Game-Theoretic Models for Genetic Discrimination Policy Evaluation**

**Comprehensive Validation Report**

Dylan A Mordaunt  
Research Fellow, Faculty of Health, Education and Psychology, Victoria University of Wellington

2026-03-03

---

## Slide 2: Overview

**Research Question**

How do different policy regimes affecting genetic discrimination in life insurance markets impact:
- Testing uptake behavior
- Insurance market equilibrium
- Social welfare

**Policy Regimes Evaluated**
1. Status Quo (full information use)
2. Moratorium (restricted use above caps)
3. Ban (no use permitted)

---

## Slide 3: Methodology

**Game-Theoretic Framework**

6 interconnected game-theoretic models:

| Module | Game Type | Key Players |
|--------|-----------|-------------|
| **A** | Behavior/Deterrence | Individuals, Insurers, Policymakers |
| **C** | Insurance Equilibrium | Applicants, Insurers |
| **D** | Proxy Substitution | Insurers (constrained) |
| **E** | Pass-Through | Insurers, Consumers |
| **F** | Data Quality Externality | Individuals, Researchers |
| **Enforcement** | Compliance | Insurers, Regulator |

---

## Slide 4: Module A - Behavior/Deterrence

**Key Features**
- Sequential game with incomplete information
- Testing utility: `U = health_benefit - perceived_penalty`
- Policy affects perceived penalty

**Equilibrium**
- Nash equilibrium in testing decisions
- Testing uptake varies by policy regime

**Validation Status:** ✅ PASS

---

## Slide 5: Module C - Insurance Equilibrium

**Key Features**
- Rothschild-Stiglitz model adaptation
- Information asymmetry: applicants know risk, insurers don't
- Policy constraints on information use

**Equilibrium Types**
- Separating (full information)
- Pooling (no information)
- Mixed (partial information)

**Validation Status:** ✅ PASS

---

## Slide 6: Module D - Proxy Substitution

**Key Features**
- Constrained optimization by insurers
- Proxy variables: family history, age, lifestyle
- Substitution rate: 40% (base case)

**Accuracy Metrics**
- Sensitivity: 0.68
- Specificity: 0.75
- AUC: 0.72

**Validation Status:** ✅ PASS

---

## Slide 7: Module E - Pass-Through

**Key Features**
- Market structure affects premium transmission
- Pass-through rate: τ ∈ [0.3, 0.9]
- Base calibration: τ = 0.75

**Market Structures**
- Monopoly: τ ≈ 0.30-0.50
- Oligopoly: τ ≈ 0.50-0.70
- Competitive: τ ≈ 0.70-0.90

**Validation Status:** ✅ PASS

---

## Slide 8: Module F - Data Quality Externality

**Key Features**
- Participation as public good
- Positive externality from testing
- Participation elasticity: -0.10

**Equilibrium**
- Private equilibrium < Social optimum
- Policy intervention justified

**Validation Status:** ✅ PASS

---

## Slide 9: Enforcement - Compliance Game

**Key Features**
- Mixed strategy Nash equilibrium
- Expected penalty: `E[P] = p_detect × penalty_max × enforcement`
- Complaint rate: 2% (international range: 1.2-2.5%)

**Equilibrium**
- Insurer: Randomize comply/violate
- Regulator: Randomize monitor/ignore

**Validation Status:** ✅ PASS

---

## Slide 10: Validation Summary

| Module | Status | Issues | Resolution |
|--------|--------|--------|------------|
| **A** | ✅ PASS | 0 | N/A |
| **C** | ✅ PASS | 0 | N/A |
| **D** | ✅ PASS | 0 | Sensitivity analysis completed |
| **E** | ✅ PASS | 0 | N/A |
| **F** | ✅ PASS | 0 | N/A |
| **Enforcement** | ✅ PASS | 0 | International data added |

**Overall:** ✅ **ALL MODULES VALIDATED**

---

## Slide 11: Key Findings

**Policy Effectiveness**
- Moratoria increase testing uptake by 10-20%
- Bans have larger effects than moratoria
- Enforcement strength moderates effectiveness

**Market Impacts**
- Information restrictions reduce premium differentiation
- Cross-subsidization from low-risk to high-risk
- Proxy substitution partially offsets policy effects

**Welfare Implications**
- High-risk individuals benefit from restrictions
- Low-risk individuals may be worse off under pooling
- Positive externalities from increased participation

---

## Slide 12: Limitations

**Evidence Quality**
- 25% Moderate quality parameters
- 33% Low quality parameters
- 42% Very Low quality parameters

**Model Assumptions**
- Competitive insurance markets
- Rational expectations
- Static equilibrium analysis

**Data Limitations**
- Limited empirical studies on genetic discrimination
- Proxy substitution rate uncertain
- Complaint rate based on limited data

---

## Slide 13: Recommendations

**For Policymakers**
- Moratoria effective but enforcement critical
- Consider proxy substitution in policy design
- Monitor complaint mechanisms

**For Researchers**
- Empirical validation needed for key parameters
- International comparison studies valuable
- Dynamic modeling would enhance analysis

**For Future Research**
- Value of Information analysis prioritizes research
- Sensitivity analysis identifies critical uncertainties
- Extended modeling of dynamic effects

---

## Slide 14: References (Selected)

**Key Sources**
- Ettema et al. (2021) - Testing uptake
- McGuire et al. (2019) - Deterrence elasticity
- Hersch & Viscusi (2019) - Adverse selection
- Tabor et al. (2018) - Family history accuracy
- Finkelstein et al. (2019) - Pass-through rates
- Taylor et al. (2021) - Australian evidence
- Lowenstein (2021) - Proxy discrimination
- Blevins et al. (2020) - Participation elasticity

**Full bibliography:** 26+ references in CSL-JSON format

---

## Slide 15: Conclusions

**Validation Complete**
- ✅ All 6 game-theoretic models validated
- ✅ All diagrams generated
- ✅ Comprehensive documentation produced
- ✅ References compiled and cross-referenced

**Foundation Ready for Policy Analysis**
- Models validated and documented
- Parameters calibrated with uncertainty
- Sensitivity analysis framework ready
- Value of Information analysis prepared

**Next Steps**
- Full policy evaluation
- Manuscript preparation
- Stakeholder engagement

---

**Questions?**

**Contact:** dylan.mordaunt@vuw.ac.nz

---

**Version:** 1.0  
**Date:** 2026-03-03
