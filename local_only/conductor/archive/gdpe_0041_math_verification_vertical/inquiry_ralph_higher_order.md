# Inquiry: Higher-Order Jacobian Verification

**Track:** gdpe_0041_math_verification_vertical
**Persona:** Ralph (Deep Thinking Architect)
**Question:** Should we implement automated verification of the Welfare Jacobian to ensure absolute mathematical precision?

## 1. The Differentiability Frontier
Our engine relies on JAX auto-diff for sensitivity and VOI. If any part of the welfare kernel is non-differentiable (e.g., a hidden `if` statement or a `jnp.where` with a sharp edge), the Jacobian will be sparse or singular.
- **Risk:** This would lead to incorrect sensitivity indices and unstable policy frontiers.

## 2. Jacobian Sanity Proof
We can implement a test that:
1. Calculates the Jacobian of the Net Social Benefit with respect to all primary elasticities using `jax.jacobian`.
2. Verifies that the Jacobian is **Dense** (not all zeros) and **Conditioned** (not singular).
3. Check Monotonicity of the Gradients: $\frac{\partial NSB}{\partial \epsilon_{testing}} > 0$.

## 3. Ralph's Iterative Improvement
- **Self-Inquiry:** "Is this too computationally expensive?"
- **Answer:** No. Since our kernel is vectorized, `jax.jacobian` is extremely fast. We should add this to the "Reviewer Mode" diagnostics.
- **Action:** I recommend adding a `src/model/proof_engine.py` module in **Track `gdpe_0044`** specifically for higher-order mathematical audits (Jacobians, Hessians, and Convergence proofs).
