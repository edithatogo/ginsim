# JAX + Pydantic Compatibility Notes

**Issue:** JAX's `@jit` doesn't work with pydantic models or boolean conditionals.

**Solution Implemented:** Hybrid approach

1. **Core numerical functions** (`module_*_core.py`):
   - Use `@jit` on pure array operations
   - No pydantic models as arguments
   - No boolean conditionals

2. **Wrapper functions** (`module_*_wrappers.py`):
   - Accept pydantic models
   - Extract primitives
   - Call core functions
   - No `@jit` (overhead not worth it for wrapper)

3. **Functions with boolean args**:
   - Don't use `@jit` (JAX limitation)
   - Performance impact minimal for control flow functions

**Files to Update:**
- ✅ Module A: Core + wrappers split
- ⏳ Module C: Needs same treatment
- ⏳ Module D: Needs same treatment  
- ⏳ Module F: Needs same treatment
- ⏳ Enforcement: Needs same treatment

**Tests:**
- Update imports to use wrappers
- Some tests need signature updates

**Performance Impact:**
- Minimal - `@jit` kept on heavy numerical ops
- Wrapper overhead negligible
- Boolean functions typically small

**Best Practice Going Forward:**
```python
# Core function (JIT-compiled)
@jit
def heavy_computation(x: Array, y: Array) -> Array:
    return x @ y

# Wrapper (accepts pydantic)
def compute(params: ModelParameters) -> float:
    result = heavy_computation(params.x_array, params.y_array)
    return float(result)
```
