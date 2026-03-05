# Extended Strategic Games Documentation

## Overview

This document describes the extended strategic games implemented for genetic discrimination policy analysis. These games model complex behavioral dynamics beyond basic policy evaluation.

---

## Game 1: Information Leakage Game

### Purpose

Model how insurers may circumvent genetic discrimination bans using proxy variables to reconstruct genetic risk information.

### Game Structure

**Players:**
- Insurer (seeks to minimize adverse selection)
- Regulator (seeks to enforce ban)
- Individual (seeks insurance coverage)

**Information Flow:**
```
Genetic Test Results → [BLOCKED by Ban]
                          ↓
Proxy Variables → Insurer Inference → Risk Reconstruction
    • Family History
    • Medical Records
    • Lifestyle Factors
```

### Key Equations

**Reconstruction Accuracy:**
```
Reconstruction_Accuracy = Proxy_Accuracy × Insurer_Inference_Strength
```

**Bypass Rate:**
```
Bypass_Rate = Reconstruction_Accuracy × (1 - Ban_Effectiveness)
```

**Effective Testing Uptake:**
```
Effective_Uptake = Baseline_Uptake + Ban_Boost × (1 - Bypass_Rate)
```

Where `Ban_Boost` is typically ~20% increase from ban implementation.

### Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `proxy_accuracy` | 0.0-1.0 | 0.6 | How well proxies predict genetic risk |
| `insurer_inference_strength` | 0.0-1.0 | 0.7 | Insurer's ability to use proxies |
| `ban_effectiveness` | 0.0-1.0 | 0.8 | How effectively ban prevents discrimination |

### Implementation

**Module:** `src/model/extended_games.py::information_leakage_game()`

**Dashboard:** `streamlit_app/pages/4_Extended_Games.py`

### Policy Implications

- **Strong enforcement alone is insufficient** if proxy accuracy is high
- **Broad definitions of genetic information** reduce leakage
- **Regular audits** of insurer practices needed to maintain effectiveness

---

## Game 2: Genetic Altruism Game

### Purpose

Model testing decisions influenced by family welfare, where individuals get tested not just for themselves but to help family members make informed decisions.

### Game Structure

**Players:**
- Individual (decision maker)
- Family Members (beneficiaries of information)

**Decision Factors:**
- Self-interest (personal health information)
- Altruism (helping family members)
- Family size (number of potential beneficiaries)

### Key Equations

**Altruism Coefficient:**
```
Altruism_Coefficient = Altruism_Strength × min(Family_Size / 5, 1.0)
```

**Family Testing Rate:**
```
Family_Testing_Rate = Baseline_Uptake × (1 + Altruism_Coefficient × Family_Risk_Level)
```

**Spillover Effect:**
```
Spillover_Effect = Altruism_Coefficient × Family_Risk_Level × 0.1
```

### Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `altruism_strength` | 0.0-1.0 | 0.5 | Strength of altruistic motivation |
| `family_risk_level` | 0.0-1.0 | 0.3 | Family's genetic risk level |
| `family_size` | 2-10 | 4 | Number of family members |

### Implementation

**Module:** `src/model/extended_games.py::genetic_altruism_game()`

**Dashboard:** `streamlit_app/pages/4_Extended_Games.py`

### Policy Implications

- **Family-centered interventions** may be more effective than individual-focused approaches
- **Larger families** show stronger altruism effects
- **High-risk families** benefit most from altruistic testing

---

## Game 3: Cascade Testing Game

### Purpose

Model sequential testing within families after an index case is identified, creating a cascade effect of testing.

### Game Structure

**Players:**
- Index Case (initial tester)
- Family Members (contacted after index case)
- Healthcare System (facilitates cascade)

**Cascade Process:**
```
Index Case Identified
        ↓
Family Contact (rate: 70%)
        ↓
Offer Testing (uptake: 40%)
        ↓
Secondary Cases Identified
        ↓
Repeat for their families
```

### Key Equations

**Secondary Cases:**
```
Eligible_Families = Index_Cases × Family_Contact_Rate
Testable_Relatives = Eligible_Families × (Average_Family_Size - 1)
Secondary_Cases = Testable_Relatives × Uptake_After_Contact
```

**Cascade Rate:**
```
Cascade_Rate = Secondary_Cases / Index_Cases
```

**Cost-Effectiveness:**
```
Total_Cost = Total_Tests × Cost_Per_Test
Detections = Index_Cases × Detection_Yield + Secondary_Cases × Detection_Yield × 0.5
Cost_Per_Detection = Total_Cost / Detections
```

### Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `index_case_rate` | 0.01-0.2 | 0.05 | Rate of initial testers |
| `family_contact_rate` | 0.0-1.0 | 0.7 | Fraction of families contacted |
| `uptake_after_contact` | 0.0-1.0 | 0.4 | Testing uptake after family contact |
| `cost_per_test` | $0-$5000 | $500 | Cost per genetic test |
| `detection_yield` | 0.01-0.5 | 0.1 | Probability of detecting mutation |

### Implementation

**Module:** `src/model/extended_games.py::cascade_testing_game()`

**Dashboard:** `streamlit_app/pages/4_Extended_Games.py`

### Policy Implications

- **Cascade testing is cost-effective** compared to population screening
- **Family contact programs** significantly increase testing rates
- **Lower cost per detection** in cascade vs. opportunistic testing

---

## Comparative Analysis

### When to Use Each Game

| Scenario | Recommended Game |
|----------|-----------------|
| Evaluating ban effectiveness | Information Leakage |
| Family-based interventions | Genetic Altruism |
| Cost-effectiveness analysis | Cascade Testing |
| Comprehensive policy analysis | All three games |

### Interaction Effects

**Information Leakage × Cascade Testing:**
- High leakage reduces cascade effectiveness (less value in family information)
- Cascade testing can partially offset leakage by increasing overall uptake

**Altruism × Cascade:**
- Strong altruism increases cascade uptake
- Cascade programs leverage altruistic motivations

### Combined Welfare Impact

The total welfare impact of policy can be decomposed as:

```
Total_Welfare = Direct_Policy_Effect
              - Leakage_Loss
              + Altruism_Gain
              + Cascade_Efficiency_Gain
```

---

## Validation and Calibration

### Data Sources

| Parameter | Source | Jurisdiction |
|-----------|--------|--------------|
| Deterrence elasticity | Taylor et al. (2021) | AU |
| Proxy accuracy | Hersch & Viscusi (2019) | US |
| Family contact rate | Bombard et al. (2018) | CA |
| Cascade uptake | Armstrong et al. (2020) | AU |

### Sensitivity Analysis

All games should be run with sensitivity analysis to understand parameter uncertainty. See `docs/UNCERTAINTY_DECOMPOSITION.md` for methods.

---

## Future Extensions

### Planned Games
1. **Genetic Altruism with Time Dynamics** - Multi-period family decisions
2. **Insurer Counter-Strategy Game** - Dynamic response to enforcement
3. **Multi-Insurer Competition** - Market structure effects

### Research Questions
- How does information leakage evolve over time?
- What is the optimal enforcement strategy given limited resources?
- How do cultural differences affect altruism parameters?

---

**Version:** 1.0  
**Last Updated:** 2026-03-05  
**Authors:** Authors' analysis  
**Related Documentation:** `docs/UNCERTAINTY_DECOMPOSITION.md`
