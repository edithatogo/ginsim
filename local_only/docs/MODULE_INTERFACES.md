# Module Interfaces Documentation

**Track:** gdpe_0007_game_execution
**Date:** 2026-03-03
**Version:** 1.0

---

## Overview

This document specifies the interfaces for all game-theoretic modules in the genetic discrimination policy evaluation framework, enabling individual and hybrid execution.

---

## Module A: Behavior/Deterrence

### Interface

**Input:**
- `params: ModelParameters` - Model parameters
- `policy: PolicyConfig` - Policy configuration

**Output:**
- `testing_uptake: float` - Probability of testing [0, 1]

**Dependencies:**
- `src.model.parameters`
- `src.model.module_a_behavior_wrappers`

**Execution Script:** `scripts/run_module_a.py`

**Usage:**
```bash
python -m scripts.run_module_a --policy moratorium
```

---

## Module C: Insurance Equilibrium

### Interface

**Input:**
- `params: ModelParameters` - Model parameters
- `policy: PolicyConfig` - Policy configuration

**Output:**
- `EquilibriumResult` with:
  - `premium_high: float` - High-risk premium
  - `premium_low: float` - Low-risk premium
  - `equilibrium_type: str` - 'Separating' or 'Pooling'

**Dependencies:**
- `src.model.parameters`
- `src.model.module_c_insurance_eq`

**Execution Script:** `scripts/run_module_c.py`

**Usage:**
```bash
python -m scripts.run_module_c --policy ban
```

---

## Module D: Proxy Substitution

### Interface

**Input:**
- `params: ModelParameters` - Model parameters
- `features: Dict[str, float]` - Risk features
- `weights: Dict[str, float]` - Feature weights

**Output:**
- `risk_score: float` - Composite risk score
- `accuracy: ProxyAccuracy` - Sensitivity/specificity

**Dependencies:**
- `src.model.parameters`
- `src.model.module_d_proxy`

**Execution Script:** `scripts/run_module_d.py`

---

## Module E: Pass-Through

### Interface

**Input:**
- `params: ModelParameters` - Model parameters
- `cost_shock: float` - Cost change

**Output:**
- `premium_change: float` - Premium adjustment

**Dependencies:**
- `src.model.parameters`
- `src.model.module_e_passthrough`

**Execution Script:** `scripts/run_module_e.py`

---

## Module F: Data Quality

### Interface

**Input:**
- `params: ModelParameters` - Model parameters
- `policy: PolicyConfig` - Policy configuration

**Output:**
- `participation_rate: float` - Participation probability
- `externality: float` - Social externality value

**Dependencies:**
- `src.model.parameters`
- `src.model.module_f_data_quality`

**Execution Script:** `scripts/run_module_f.py`

---

## Enforcement: Compliance

### Interface

**Input:**
- `params: ModelParameters` - Model parameters
- `policy: PolicyConfig` - Policy configuration

**Output:**
- `compliance_rate: float` - Compliance probability
- `expected_penalty: float` - Expected penalty value

**Dependencies:**
- `src.model.parameters`
- `src.model.module_enforcement`

**Execution Script:** `scripts/run_enforcement.py`

---

## Hybrid Execution

### A+C: Basic Policy Evaluation

**Input:**
- `params: ModelParameters`
- `policy: PolicyConfig`

**Output:**
- `testing_uptake: float`
- `premiums: Dict[str, float]`

**Script:** `scripts/run_hybrid_ac.py`

---

### A+C+D: + Proxy Substitution

**Input:**
- `params: ModelParameters`
- `policy: PolicyConfig`

**Output:**
- `testing_uptake: float`
- `premiums: Dict[str, float]`
- `risk_scores: Dict[str, float]`

**Script:** `scripts/run_hybrid_acd.py`

---

### Full Model: All Modules

**Input:**
- `params: ModelParameters`
- `policy: PolicyConfig`

**Output:**
- Complete policy evaluation results

**Script:** `scripts/run_full_model.py`

---

## Data Flow

```
Policy → Module A → Testing Uptake
              ↓
Module C → Premiums
              ↓
Module D → Risk Scores
              ↓
Module E → Premium Adjustments
              ↓
Module F → Participation Rate
              ↓
Enforcement → Compliance Rate
```

---

**Version:** 1.0
**Date:** 2026-03-03
**Status:** Complete ✅
