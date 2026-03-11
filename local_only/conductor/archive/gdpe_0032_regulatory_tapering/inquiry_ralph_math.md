# Inquiry: Mathematical Kernels for Regulatory Tapering

**Track:** gdpe_0032_regulatory_tapering
**Persona:** Ralph (Deep Thinking Architect)
**Question:** How can we implement smooth tapering without introducing local minima that break the JAX Jacobian solver?

## 1. The Challenge
The current policy logic is "Piecewise Constant":
$$ \text{Protection}(x) = \begin{cases} 1 & \text{if } x \leq \text{Cap} \\ 0 & \text{if } x > \text{Cap} \end{cases} $$
The derivative of this function is zero everywhere except at the Cap, where it is undefined (Dirac delta). This makes gradient-based optimization (like finding the optimal premium or equilibrium) impossible.

## 2. Smooth Approximation Candidates

### Option A: Standard Sigmoid (Logistic)
$$ S(x) = 1 - \sigma\left(\frac{x - \text{Cap}}{\text{Scale}}\right) $$
- **Pros:** Infinitely differentiable.
- **Cons:** Never actually reaches 1.0 or 0.0. Regulatory "hard caps" are violated even at values far from the cap.

### Option B: Piecewise Linear with Smoothing (The "Diamond" Choice)
Use a linear ramp between $x_{start}$ and $x_{end}$, but smooth the "corners" using a tiny quadratic or softplus term.
- **Pros:** Respects the "Hard Cap" outside the taper range.
- **Cons:** Complex to implement in pure JAX without control flow overhead.

### Option C: Generalized Sigmoids (Double Softplus)
$$ f(x) = \text{softplus}(\text{Cap}_{upper} - x) - \text{softplus}(\text{Cap}_{lower} - x) $$
- **Pros:** Naturally bounded and smooth.
- **Cons:** Hard to parameterize exactly to match a specific "Taper Range."

## 3. Consensus Recommendation: Piecewise Sigmoid (Interpolated)
We will define a `taper_function(x, cap, range)` that:
1. Returns $1.0$ if $x < cap$.
2. Returns $0.0$ if $x > cap + range$.
3. Interpolates using a cosine-based smooth-step or a local sigmoid between them.

For JAX stability, **Option B (Smooth Piecewise Linear)** is generally preferred for economic screening models as it avoids the "tail behavior" of logistics that can bias distant equilibria.

## 4. Ralph's Iterative Improvement
- **Self-Inquiry:** "What happens if multiple caps apply (e.g., Life + TPD)?"
- **Answer:** We should use the *minimum* protection offered across all applicable caps. In JAX, this is `jnp.min`.
- **Action:** Update `module_a_behavior.py` to accept `taper_range` and implement the smooth-step kernel.
