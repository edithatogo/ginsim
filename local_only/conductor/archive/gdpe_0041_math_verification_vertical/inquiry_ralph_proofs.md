# Inquiry: Formal Invariants & 'Conservation of Welfare'

**Track:** gdpe_0041_math_verification_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** What is the fundamental 'Conservation of Welfare' invariant for our DCBA ledger?

## 1. The Zero-Sum Core
In a frictionless, utilitarian economy with actuarially fair insurance and no health externalities:
$$ \sum \Delta \text{Surplus} = 0 $$
The gains to consumers (from protection) must exactly equal the costs to insurers (from claims) and the state (from enforcement).

## 2. The Real-World Leakage
In our model, the sum is NOT zero because of:
1. **Health Benefits (Positive):** Prevention value from testing.
2. **Fiscal Costs (Negative):** Testing subsidies.
3. **Research Externalities (Positive/Negative):** Participation shifts.

## 3. The 'Conservation Invariant'
The **Net Social Benefit (NSB)** must satisfy:
$$ \text{NSB} = (\Delta CS + \Delta PS + \Delta FI - \Delta RE) + \text{Clinical Value} $$

- **Proof Task:** Implement a "Mathematical Consistency" test that disables health/research benefits and verifies that the remaining ledger balances within a 1% floating-point tolerance (accounting for JAX `float32` precision).

## 4. Implementation Action
1. **Create `tests/verification/test_economic_invariants.py`:** A suite of high-precision proofs.
2. **Test Case 1:** Actuarially fair pricing proof (Module C).
3. **Test Case 2:** Welfare sum invariant (DCBA).
4. **Test Case 3:** Policy Monotonicity (Ban Uptake > Moratorium Uptake > SQ Uptake).

## 5. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is float32 enough for a formal proof?"
- **Answer:** No. For the proof engine, I'll temporarily switch the engine to `jax_enable_x64=True` to verify invariants at double precision, then switch back for performance.
- **Action:** Add a `double_precision_audit` fixture to the test suite.
