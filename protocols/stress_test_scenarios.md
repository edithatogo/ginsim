# Stress Test Scenarios

**Track:** gdpe_0002_evidence_anchoring — Phase 4  
**Purpose:** Define extreme scenarios for model validation

---

## Overview

Stress tests verify model behavior under extreme parameter values. Expected behaviors:
- No crashes or errors
- Logical consistency (monotonicity where expected)
- Bounds respected (no negative values where inappropriate)
- Outputs remain interpretable

---

## Scenario Definitions

### Scenario A: 100% Testing Uptake (No Deterrence)

**Purpose:** Test upper bound of testing behavior

**Parameters:**
```yaml
module_a:
  baseline_testing_uptake: 1.0  # 100%
  deterrence_elasticity: 0.0    # No deterrence
  moratorium_effect: 0.0        # No policy effect needed
```

**Expected outcomes:**
- Maximum clinical benefits (all eligible individuals tested)
- No welfare loss from deterrence
- Maximum adverse selection pressure (if information used)
- No incremental policy benefit (already at ceiling)

**Validation checks:**
- [ ] Model runs without errors
- [ ] Clinical outputs at theoretical maximum
- [ ] No negative premiums or costs
- [ ] Welfare impacts positive or neutral

---

### Scenario B: 0% Adverse Selection

**Purpose:** Test lower bound of information asymmetry

**Parameters:**
```yaml
module_c:
  adverse_selection_elasticity: 0.0    # No response to information
  demand_elasticity_high_risk: 0.0     # No demand change
  baseline_loading: 0.0                # No premium loading
```

**Expected outcomes:**
- No premium divergence by risk status
- No welfare loss from adverse selection
- Policy interventions have minimal impact (no market failure)

**Validation checks:**
- [ ] Model runs without errors
- [ ] Premiums identical across risk groups
- [ ] Policy incremental benefits near zero
- [ ] No logical inconsistencies

---

### Scenario C: 100% Enforcement (Perfect Compliance)

**Purpose:** Test upper bound of policy effectiveness

**Parameters:**
```yaml
enforcement:
  enforcement_effectiveness: 1.0  # 100% compliance
  complaint_rate: 0.0             # No violations
```

**Expected outcomes:**
- Maximum policy effectiveness
- No proxy substitution (perfect enforcement)
- Maximum welfare gains from policy

**Validation checks:**
- [ ] Model runs without errors
- [ ] Policy effects at theoretical maximum
- [ ] No violations or complaints generated
- [ ] Monotonic relationship with enforcement strength

---

### Scenario D: 0% Enforcement (No Compliance)

**Purpose:** Test lower bound of policy effectiveness

**Parameters:**
```yaml
enforcement:
  enforcement_effectiveness: 0.0  # No compliance
  complaint_rate: 1.0             # Maximum violations
```

**Expected outcomes:**
- No policy effectiveness (same as no policy)
- Maximum discrimination (unchecked)
- Maximum welfare losses

**Validation checks:**
- [ ] Model runs without errors
- [ ] Policy effects near zero
- [ ] Outcomes similar to no-policy baseline
- [ ] No negative welfare (bounded at zero)

---

### Scenario E: 100% Proxy Substitution (Perfect Substitutes)

**Purpose:** Test upper bound of proxy accuracy

**Parameters:**
```yaml
module_d:
  family_history_sensitivity: 1.0    # Perfect prediction
  proxy_substitution_rate: 1.0       # All risk captured
```

**Expected outcomes:**
- No loss of underwriting accuracy
- Minimal adverse selection even without genetic info
- Policy effects minimal (proxies work perfectly)

**Validation checks:**
- [ ] Model runs without errors
- [ ] Underwriting accuracy maintained
- [ ] Premium divergence minimal
- [ ] Policy incremental benefits near zero

---

### Scenario F: 0% Proxy Substitution (No Substitutes)

**Purpose:** Test lower bound of proxy accuracy

**Parameters:**
```yaml
module_d:
  family_history_sensitivity: 0.0    # No prediction
  proxy_substitution_rate: 0.0       # No risk captured
```

**Expected outcomes:**
- Maximum loss of underwriting accuracy
- Maximum adverse selection (without genetic info)
- Maximum policy effects

**Validation checks:**
- [ ] Model runs without errors
- [ ] Underwriting accuracy severely degraded
- [ ] Large premium divergence
- [ ] Policy effects at maximum

---

## Combined Extreme Scenarios

### Scenario G: Best Case (Maximum Policy Benefit)

**Combination:**
- 100% enforcement (Scenario C)
- 0% proxy substitution (Scenario F)
- High baseline deterrence

**Expected:** Maximum welfare gains from policy

---

### Scenario H: Worst Case (Minimum Policy Benefit)

**Combination:**
- 0% enforcement (Scenario D)
- 100% proxy substitution (Scenario E)
- Low baseline deterrence

**Expected:** Minimal welfare gains from policy

---

## Implementation

### Script: `scripts/run_stress_tests.py`

```python
#!/usr/bin/env python3
"""
Stress test runner for genetic discrimination policy model.

Usage:
    python -m scripts.run_stress_tests --output outputs/stress_tests/
"""

import yaml
from pathlib import Path
from src.model.glue_policy_eval import run_policy_evaluation

# Define scenarios
SCENARIOS = {
    'A_100pct_uptake': {
        'module_a': {
            'baseline_testing_uptake': 1.0,
            'deterrence_elasticity': 0.0,
            'moratorium_effect': 0.0,
        }
    },
    'B_0pct_adverse_selection': {
        'module_c': {
            'adverse_selection_elasticity': 0.0,
            'demand_elasticity_high_risk': 0.0,
            'baseline_loading': 0.0,
        }
    },
    # ... etc for all scenarios
}

def run_stress_test(scenario_name, params):
    """Run single stress test scenario."""
    print(f"Running scenario: {scenario_name}")
    
    # Load base config
    with open('configs/calibration_australia.yaml') as f:
        config = yaml.safe_load(f)
    
    # Override with scenario parameters
    for module, overrides in params.items():
        if module in config:
            config[module].update(overrides)
    
    # Run evaluation
    results = run_policy_evaluation(config)
    
    # Validate outputs
    assert results['testing_uptake'] >= 0, "Negative testing uptake"
    assert results['premiums'] >= 0, "Negative premiums"
    # ... more checks
    
    return results

def main():
    output_dir = Path('outputs/stress_tests')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_results = {}
    
    for name, params in SCENARIOS.items():
        results = run_stress_test(name, params)
        all_results[name] = results
        
        # Save individual results
        with open(output_dir / f'{name}.yaml', 'w') as f:
            yaml.dump(results, f)
    
    # Summary
    summary = generate_summary(all_results)
    with open(output_dir / 'summary.md', 'w') as f:
        f.write(summary)
    
    print(f"Stress tests complete. Results saved to {output_dir}")

if __name__ == '__main__':
    main()
```

---

## Validation Checklist

After running all scenarios:

- [ ] All scenarios run without errors
- [ ] No negative values where inappropriate
- [ ] Monotonicity verified (e.g., higher enforcement → better outcomes)
- [ ] Bounds respected (probabilities in [0,1], etc.)
- [ ] Logical consistency across scenarios
- [ ] Results documented in `docs/STRESS_TEST_REPORT.md`

---

## Expected Results Summary

| Scenario | Testing Uptake | Premium Divergence | Policy Effect | Notes |
|----------|---------------|-------------------|---------------|-------|
| A (100% uptake) | 100% | High | None | Ceiling effect |
| B (0% AS) | Baseline | None | Minimal | No market failure |
| C (100% enforcement) | High | Low | Maximum | Perfect compliance |
| D (0% enforcement) | Low | High | None | No compliance |
| E (100% proxy) | Baseline | Low | Minimal | Proxies work |
| F (0% proxy) | Low | High | Maximum | No substitutes |
| G (Best case) | High | Low | Maximum | Ideal conditions |
| H (Worst case) | Low | High | Minimal | Worst conditions |

---

**Version:** 1.0  
**Date:** 2026-03-03  
**Track:** gdpe_0002_evidence_anchoring
