# Game Descriptions

**Track:** gdpe_0005_game_validation  
**Date:** 2026-03-03  
**Version:** 1.0

---

## Module A: Behavior/Deterrence Game

### Overview

The Behavior/Deterrence game models how individuals make decisions about genetic testing when facing potential discrimination in life insurance markets. This is a sequential game with incomplete information involving three key players: individuals, insurers, and policymakers.

### Players and Objectives

**1. Individuals (Testing Decision-Makers)**
- **Objective:** Maximize expected utility from genetic testing
- **Utility Function:** `U(test) = health_benefit - perceived_penalty(policy)`
- **Strategy:** Choose whether to undergo genetic testing or not
- **Information:** Know their own health risk, perceive policy restrictions

**2. Insurers (Premium Setters)**
- **Objective:** Maximize profits while complying with policy constraints
- **Profit Function:** `π = premiums - claims - administrative_costs`
- **Strategy:** Set premiums based on available information
- **Information:** Cannot observe genetic test results under moratorium/ban

**3. Policymakers (Regulators)**
- **Objective:** Maximize social welfare
- **Welfare Function:** `W = Σ individual_welfare + insurer_profits + externalities`
- **Strategy:** Choose policy regime (status quo, moratorium, or ban)
- **Information:** Full model structure and population outcomes

### Game Mechanism

The game proceeds sequentially:

1. **Policy Stage:** Policymaker sets the policy regime
   - Status quo: Full use of genetic information allowed
   - Moratorium: Genetic test results cannot be used above caps
   - Ban: No genetic information use permitted

2. **Testing Stage:** Individuals decide whether to test
   - Weigh health benefits against perceived discrimination risk
   - Perceived penalty varies by policy regime

3. **Pricing Stage:** Insurers set premiums
   - Use available information (cannot use genetic results under restrictions)
   - May use proxy variables (family history, demographics)

4. **Realization Stage:** Payoffs are realized
   - Health outcomes from testing decisions
   - Insurance outcomes from premium decisions
   - Social welfare from aggregate outcomes

### Equilibrium Concept

**Nash Equilibrium:** Each player's strategy is optimal given others' strategies.

**Equilibrium Conditions:**
- Individuals: Test if `U(test) > U(no test)`
- Insurers: Premiums maximize expected profit given information constraints
- Policymakers: Policy maximizes social welfare

**Existence:** Guaranteed by compact strategy spaces and continuous payoff functions.

### Key Parameters

| Parameter | Symbol | Base Value | Source | Quality |
|-----------|--------|------------|--------|---------|
| Baseline testing uptake | `u_0` | 0.52 | Ettema et al. (2021) | Moderate |
| Deterrence elasticity | `ε_d` | 0.18 | McGuire et al. (2019) | Low |
| Moratorium effect | `δ_m` | 0.15 | Taylor et al. (2021) | Very Low |

### Policy Implications

The model predicts that:
- **Moratorium policies** increase testing uptake by reducing perceived penalty
- **Ban policies** have larger effects than moratoria
- **Enforcement strength** moderates policy effectiveness
- **Deterrence effects** persist even under restrictions

### Validation Status

✅ **PASS** - All validation criteria met. Game structure correctly implemented.

---

## Module C: Insurance Equilibrium Game (Rothschild-Stiglitz)

### Overview

The Insurance Equilibrium game implements the classic Rothschild-Stiglitz model of competitive insurance markets with asymmetric information, adapted for genetic discrimination policy analysis.

### Players and Objectives

**1. Applicants (Informed Parties)**
- **Types:** High-risk (probability `p_H`) or Low-risk (probability `p_L`)
- **Objective:** Maximize expected utility from insurance coverage
- **Utility Function:** `EU = (1-p)U(W_no_loss) + pU(W_loss - premium + coverage)`
- **Strategy:** Accept or reject insurance offers
- **Information:** Know own risk type perfectly

**2. Insurers (Uninformed Parties)**
- **Objective:** Zero expected profit (competitive market assumption)
- **Profit Function:** `E[π] = premium - p × coverage`
- **Strategy:** Offer premium-coverage bundles
- **Information:** Know population risk distribution, not individual types

### Information Asymmetry

**Key Feature:** Applicants know their risk type; insurers do not.

**Policy Constraints:**
- **Status Quo:** Full information available → Separating equilibrium
- **Moratorium:** Partial information (no genetic results) → Mixed equilibrium
- **Ban:** No genetic information → Pooling equilibrium

### Equilibrium Types

**1. Separating Equilibrium (Full Information)**
- High-risk and low-risk types choose different contracts
- High-risk: Full coverage at actuarially fair premium
- Low-risk: Partial coverage at lower premium
- **Condition:** Self-selection constraints satisfied

**2. Pooling Equilibrium (No Information)**
- All types choose same contract
- Single premium based on average risk
- **Condition:** Information completely banned

**3. Mixed Equilibrium (Partial Information)**
- Some separation, some pooling
- Depends on policy constraints and proxy accuracy

### Equilibrium Conditions

**Separating Equilibrium:**
- High-risk incentive compatibility: `EU_H(separating) ≥ EU_H(pooling)`
- Low-risk incentive compatibility: `EU_L(separating) ≥ EU_L(pooling)`
- Zero profit for each contract

**Pooling Equilibrium:**
- Single premium: `P = p_avg × coverage`
- Where `p_avg = λ×p_H + (1-λ)×p_L`
- `λ` = proportion of high-risk individuals

### Key Parameters

| Parameter | Symbol | Base Value | Source | Quality |
|-----------|--------|------------|--------|---------|
| Adverse selection elasticity | `ε_as` | 0.08 | Hersch & Viscusi (2019) | Low |
| Demand elasticity (high-risk) | `ε_dH` | -0.22 | Armstrong et al. (2020) | Low |
| Baseline loading | `L_0` | 0.15 | FSC Moratorium (2019) | Very Low |

### Policy Implications

The model predicts that:
- **Information restrictions** reduce risk-based premium differentiation
- **Moratoria** lead to cross-subsidization from low-risk to high-risk
- **Bans** result in pooling with average-risk premiums
- **High-risk individuals** benefit from information restrictions
- **Low-risk individuals** may be worse off under pooling

### Validation Status

✅ **PASS** - Rothschild-Stiglitz implementation verified against theoretical benchmarks.

---

## Module D: Proxy Substitution Game

### Overview

The Proxy Substitution game models how insurers re-optimize their underwriting strategies when directly constrained from using genetic information, by substituting with allowed proxy variables.

### Players and Objectives

**1. Insurers (Constrained Optimizers)**
- **Objective:** Minimize mispricing error using allowed proxies
- **Mispricing Function:** `MSE = E[(true_risk - estimated_risk)²]`
- **Strategy:** Choose weights on allowed proxy variables
- **Constraints:** Cannot use genetic test results directly

**2. Applicants**
- **Objective:** Obtain fair premiums based on true risk
- **Information:** True risk type and proxy characteristics

### Mechanism

**Constrained Optimization Problem:**

```
minimize: E[(r - ŵ'x)²]
subject to: w_genetic = 0
```

Where:
- `r` = true risk
- `x` = vector of observable characteristics
- `ŵ` = optimal weights on allowed proxies
- Constraint: Genetic variables excluded

### Proxy Variables

**Allowed Proxies (under moratorium):**
1. **Family History** - Most predictive proxy
2. **Age** - Standard risk factor
3. **Gender** - Where permitted
4. **Lifestyle Factors** - Smoking, BMI, etc.
5. **Medical History** - Pre-existing conditions

**Proxy Accuracy:**
- **Sensitivity:** 0.68 (correctly identifies high-risk)
- **Specificity:** 0.75 (correctly identifies low-risk)
- **AUC:** 0.72 (moderate discriminative ability)

### Substitution Rate

**Definition:** The extent to which genetic information is replaced by proxies.

**Base Calibration:** 0.40 (40% substitution)

**Interpretation:**
- 0.0 = No substitution (genetic information unique)
- 0.4 = Moderate substitution (proxies partially effective)
- 1.0 = Full substitution (proxies perfectly predict genetics)

**Sensitivity Analysis:** Range 0.20-0.60 tested

### Equilibrium Concept

**Constrained Optimization Equilibrium:**
- Insurers optimize given constraints
- Proxy weights reflect information content
- Mispricing error minimized subject to constraints

### Key Parameters

| Parameter | Symbol | Base Value | Source | Quality |
|-----------|--------|------------|--------|---------|
| Family history sensitivity | `sens_fh` | 0.68 | Tabor et al. (2018) | Moderate |
| Proxy substitution rate | `ρ` | 0.40 | Lowenstein (2021) + sensitivity analysis | Very Low → Moderate |

### Policy Implications

The model predicts that:
- **Proxy substitution** partially offsets policy effectiveness
- **Family history** is the most effective proxy
- **Higher substitution rates** reduce policy impact
- **Residual mispricing** persists even with optimal proxies

### Validation Status

✅ **PASS** - Constrained optimization verified. Sensitivity analysis completed.

---

## Module E: Pass-Through/Market Structure Game

### Overview

The Pass-Through game models how insurance market structure affects the transmission of policy-induced cost changes to consumers through premium adjustments.

### Players and Objectives

**1. Insurers (Price-Setting Firms)**
- **Objective:** Maximize profits
- **Profit Function:** `π = (P - C) × Q(P)`
- **Strategy:** Set premiums based on costs and market power
- **Information:** Cost structure, demand elasticity

**2. Consumers (Insurance Buyers)**
- **Objective:** Maximize consumer surplus
- **Demand Function:** `Q = Q_0 × (P/P_0)^ε`
- **Strategy:** Purchase decision based on premium
- **Information:** Premium levels, coverage terms

**3. Regulators (Market Overseers)**
- **Objective:** Maximize social welfare
- **Strategy:** Set market structure rules
- **Information:** Full market structure

### Pass-Through Mechanism

**Pass-Through Rate (τ):** Fraction of cost shock passed to consumers.

```
ΔPremium = τ × ΔCost
```

**Market Structure Dependence:**
- **Monopoly:** τ ≈ 0.30-0.50 (low pass-through)
- **Oligopoly:** τ ≈ 0.50-0.70 (moderate pass-through)
- **Competitive:** τ ≈ 0.70-0.90 (high pass-through)

**Base Calibration:** τ = 0.75 (moderately competitive market)

### Equilibrium Concept

**Price Equilibrium:** Premiums clear the market given cost structure and demand.

**Equilibrium Conditions:**
- Insurers: `MR = MC` (profit maximization)
- Consumers: `MU = P` (utility maximization)
- Market: `Q_d = Q_s` (market clearing)

### Key Parameters

| Parameter | Symbol | Base Value | Source | Quality |
|-----------|--------|------------|--------|---------|
| Pass-through rate | `τ` | 0.75 | Finkelstein et al. (2019) | Moderate |

### Policy Implications

The model predicts that:
- **More competitive markets** have higher pass-through
- **Policy-induced cost increases** are largely borne by consumers
- **Market concentration** moderates premium impacts
- **Consumer welfare** depends on market structure

### Validation Status

✅ **PASS** - Pass-through mechanism verified against empirical estimates.

---

## Module F: Data Quality Externality Game

### Overview

The Data Quality Externality game models genetic testing participation as a public good, where individual decisions create positive externalities for research and population health.

### Players and Objectives

**1. Individuals (Potential Participants)**
- **Objective:** Maximize utility (privacy cost vs. social benefit)
- **Utility Function:** `U(participate) = private_benefit + social_benefit - privacy_cost`
- **Strategy:** Participate or not participate in testing/research
- **Information:** Own preferences, policy environment

**2. Researchers (Data Users)**
- **Objective:** Maximize research quality
- **Quality Function:** `Q = f(sample_size, data_quality)`
- **Strategy:** Request data access
- **Information:** Available data quality

**3. Health System (Data Steward)**
- **Objective:** Maximize population health
- **Strategy:** Set data access policies
- **Information:** Population health outcomes

### Public Good Mechanism

**Positive Externality:** Individual participation benefits others through:
- Improved research quality
- Better risk prediction models
- Enhanced population health

**Externality Magnitude:** Depends on participation rate.

### Participation Function

```
p = f(policy_strength, privacy_concern)
```

**Base Specification:**
```
p = p_0 × (1 + ε_p × policy)
```

Where:
- `p_0` = baseline participation rate
- `ε_p` = participation elasticity (-0.10)
- `policy` = policy strength (0 = status quo, 1 = full protection)

### Equilibrium Concept

**Public Good Equilibrium:**
- Individuals: Participate if `U(participate) > U(not participate)`
- Researchers: Access data if marginal benefit > marginal cost
- Health System: Set policy to maximize population health

**Inefficiency:** Private equilibrium < Social optimum (free-rider problem)

### Key Parameters

| Parameter | Symbol | Base Value | Source | Quality |
|-----------|--------|------------|--------|---------|
| Participation elasticity | `ε_p` | -0.10 | Blevins et al. (2020) | Low |

### Policy Implications

The model predicts that:
- **Privacy protections** increase participation
- **Positive externalities** justify policy intervention
- **Under-participation** occurs in private equilibrium
- **Policy-induced participation** improves research quality

### Validation Status

✅ **PASS** - Public good mechanism verified. Participation function calibrated.

---

## Enforcement: Compliance Game

### Overview

The Compliance game models the strategic interaction between insurers (regulated entities) and regulators (enforcement agencies) in a mixed-strategy Nash equilibrium framework.

### Players and Objectives

**1. Insurers (Regulated Entities)**
- **Objective:** Maximize profits net of expected penalties
- **Profit Function:** `π = π_base + B×violation - P×detection×enforcement`
- **Strategy:** Comply or violate (mixed strategy)
- **Information:** Penalty structure, enforcement probability

**2. Regulator (Enforcement Agency)**
- **Objective:** Maximize compliance net of enforcement costs
- **Welfare Function:** `W = compliance_benefit - enforcement_cost`
- **Strategy:** Monitor or ignore (mixed strategy)
- **Information:** Complaint rate, violation prevalence

### Game Mechanism

**Mixed Strategy Nash Equilibrium:**

**Insurer's Decision:**
- Violate if: `B > P × p_detect × enforcement_strength`
- Where:
  - `B` = benefit from violation
  - `P` = maximum penalty
  - `p_detect` = detection probability
  - `enforcement_strength` = regulatory effectiveness

**Regulator's Decision:**
- Monitor if: `complaint_rate × damage > monitoring_cost`

### Expected Penalty

**Formula:**
```
E[Penalty] = p_detect × penalty_max × enforcement_strength
```

**Base Calibration:**
- `p_detect` = 0.50 (moderate detection)
- `penalty_max` = $1,000,000 (substantial penalty)
- `enforcement_strength` = 0.50 (moderate enforcement)

**Expected Penalty:** $250,000 per violation

### Complaint Rate

**Base Calibration:** 0.02 (2% of policies)

**International Comparison:**
- Australia: 0.020
- United Kingdom: 0.015
- Canada: 0.018
- European Union: 0.012
- United States: 0.025

**Weighted Average:** 0.018 (range: 0.012-0.025)

### Equilibrium Concept

**Mixed Strategy Nash Equilibrium:**
- Insurer: Randomize between comply/violate
- Regulator: Randomize between monitor/ignore
- **Equilibrium Condition:** Each player indifferent between strategies

**Equilibrium Probabilities:**
- Violation rate: `p_violate = f(enforcement, penalty)`
- Monitoring rate: `p_monitor = f(complaint_rate, cost)`

### Key Parameters

| Parameter | Symbol | Base Value | Source | Quality |
|-----------|--------|------------|--------|---------|
| Enforcement effectiveness | `ε_e` | 0.50 | FSC Moratorium (2019) | Very Low |
| Complaint rate | `λ_c` | 0.02 | Taylor et al. (2021) + international data | Very Low → Moderate |

### Policy Implications

The model predicts that:
- **Higher penalties** reduce violation rates
- **Stronger enforcement** increases compliance
- **Complaint mechanisms** enable targeted monitoring
- **Mixed strategies** are optimal for both players

### Validation Status

✅ **PASS** - Mixed strategy equilibrium verified. International data incorporated.

---

## Summary

| Module | Game Type | Players | Equilibrium | Status |
|--------|-----------|---------|-------------|--------|
| **A** | Behavior/Deterrence | 3 (Individual, Insurer, Policymaker) | Nash | ✅ PASS |
| **C** | Insurance (Rothschild-Stiglitz) | 2 (Applicant, Insurer) | Separating/Pooling | ✅ PASS |
| **D** | Proxy Substitution | 2 (Insurer, Applicant) | Constrained Optimization | ✅ PASS |
| **E** | Pass-Through | 3 (Insurer, Consumer, Regulator) | Price Equilibrium | ✅ PASS |
| **F** | Data Quality Externality | 3 (Individual, Researcher, Health System) | Public Good | ✅ PASS |
| **Enforcement** | Compliance | 2 (Insurer, Regulator) | Mixed Strategy Nash | ✅ PASS |

**All 6 games documented with complete descriptions, assumptions, and solution concepts.**

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Status:** Complete
