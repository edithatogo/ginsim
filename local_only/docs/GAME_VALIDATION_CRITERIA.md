# Game Validation Criteria

**Track:** gdpe_0005_game_validation
**Date:** 2026-03-03
**Version:** 1.0

---

## 1. Overview

This document defines the validation criteria for all game-theoretic models in the genetic discrimination policy evaluation framework.

---

## 2. Player Definition Criteria

### 2.1 Completeness

- [ ] All players in the game are explicitly identified
- [ ] Player roles are clearly defined
- [ ] Player objectives are specified
- [ ] Information sets for each player are documented
- [ ] Strategy spaces for each player are defined

### 2.2 Accuracy

- [ ] Player definitions match economic theory
- [ ] Player incentives are realistic
- [ ] Information asymmetries are correctly modeled
- [ ] Player rationality assumptions are stated

### 2.3 Documentation

- [ ] Player descriptions (100-200 words each)
- [ ] Justification for player inclusion
- [ ] References to game theory literature

---

## 3. Mechanism Validation Criteria

### 3.1 Completeness

- [ ] Game rules are fully specified
- [ ] Timing/sequence of moves is defined
- [ ] Payoff functions are specified
- [ ] Information structure is documented
- [ ] Constraints are identified

### 3.2 Accuracy

- [ ] Mechanism matches policy reality
- [ ] Payoff functions are mathematically correct
- [ ] Timing reflects real-world sequence
- [ ] Constraints are binding/non-binding as intended

### 3.3 Implementation

- [ ] Code matches mathematical specification
- [ ] Parameter values are calibrated
- [ ] Boundary conditions are handled
- [ ] Edge cases are tested

---

## 4. Equilibrium Validation Criteria

### 4.1 Concept Selection

- [ ] Equilibrium concept is appropriate for game type
- [ ] Nash equilibrium (complete information)
- [ ] Bayesian Nash equilibrium (incomplete information)
- [ ] Perfect Bayesian equilibrium (dynamic + incomplete)
- [ ] Mixed strategy (where pure doesn't exist)

### 4.2 Existence

- [ ] Existence conditions are verified
- [ ] Fixed point theorems applied where needed
- [ ] Compactness/continuity conditions checked
- [ ] Existence proof or reference provided

### 4.3 Uniqueness

- [ ] Uniqueness conditions are verified
- [ ] Multiple equilibria identified where they exist
- [ ] Equilibrium selection criteria specified
- [ ] Stability analysis conducted

### 4.4 Computation

- [ ] Equilibrium computation method is correct
- [ ] Numerical methods converge
- [ ] Solutions are verified analytically where possible
- [ ] Sensitivity to parameters is tested

---

## 5. Parameter Validation Criteria

### 5.1 Calibration

- [ ] All parameters have source documentation
- [ ] Parameter values are from peer-reviewed sources
- [ ] Uncertainty is quantified (confidence intervals)
- [ ] Jurisdiction-specific values are used where available

### 5.2 Sensitivity

- [ ] Sensitivity analysis plan is defined
- [ ] Key parameters are identified
- [ ] Reasonable ranges are specified
- [ ] Tornado diagrams will be produced

### 5.3 Documentation

- [ ] Parameter table with all values
- [ ] Source citations for each parameter
- [ ] Evidence quality assessment (GRADE)
- [ ] Justification for assumptions

---

## 6. Validation Report Template

For each game, the validation report will include:

### 6.1 Executive Summary

- Game name and purpose
- Validation status (Pass/Fail/Partial)
- Key findings
- Recommendations

### 6.2 Player Validation

- Player definitions
- Completeness assessment
- Accuracy assessment
- Issues identified

### 6.3 Mechanism Validation

- Mechanism description
- Completeness assessment
- Accuracy assessment
- Implementation verification
- Issues identified

### 6.4 Equilibrium Validation

- Equilibrium concept
- Existence verification
- Uniqueness verification
- Computation verification
- Issues identified

### 6.5 Parameter Validation

- Parameter table
- Calibration sources
- Sensitivity analysis
- Issues identified

### 6.6 Overall Assessment

- Validation status
- Summary of issues
- Recommendations
- References

---

## 7. Validation Status Codes

| Code | Meaning |
|------|---------|
| **PASS** | All criteria met, no issues |
| **PASS-MINOR** | Minor issues, no impact on validity |
| **PARTIAL** | Some criteria not met, needs attention |
| **FAIL** | Critical criteria not met, major revision needed |

---

## 8. Review Process

1. **Self-review:** Author completes validation
2. **Technical review:** Independent reviewer verifies
3. **Approval:** Track lead approves validation report

---

**Version:** 1.0
**Date:** 2026-03-03
**Status:** Ready for use
