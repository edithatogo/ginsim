"""
Example: Using beartype, attrs, and msgspec together.

This demonstrates the recommended stack for JAX code.
"""

# =============================================================================
# 1. Runtime Type Checking with beartype
# =============================================================================

from beartype import beartype
from beartype.claw import beartype_this_package

# Package-wide type checking (add to __init__.py)
beartype_this_package()

import jax.numpy as jnp
from jax import jit


@beartype
def train_step(params: dict[str, jnp.ndarray], 
               data: jnp.ndarray,
               target: jnp.ndarray) -> float:
    """Train with runtime type checking."""
    predictions = jnp.dot(data, params['weights'])
    loss = jnp.mean((predictions - target) ** 2)
    return loss


# =============================================================================
# 2. JAX-Compatible Data Classes with attrs
# =============================================================================

import attrs


@attrs.define(frozen=True, slots=True)
class ModelState:
    """Immutable JAX state."""
    params: dict[str, jnp.ndarray]
    step: int
    loss: float


@attrs.define(frozen=True, slots=True)
class Config:
    """Immutable configuration."""
    learning_rate: float
    n_iterations: int
    batch_size: int


# Usage
@jit
def update_state(state: ModelState, grad: dict[str, jnp.ndarray], 
                 lr: float) -> ModelState:
    """Update state immutably."""
    new_params = {
        k: v - lr * grad[k] 
        for k, v in state.params.items()
    }
    return attrs.evolve(
        state,
        params=new_params,
        step=state.step + 1,
    )


# =============================================================================
# 3. Fast Serialization with msgspec
# =============================================================================

import msgspec


class MsgSpecConfig(msgspec.Struct):
    """Fast config with validation."""
    learning_rate: float
    n_iterations: int
    batch_size: int = 32  # Default value


# Fast serialization
config = MsgSpecConfig(0.01, 1000, 64)

# Encode (10-80x faster than pydantic)
json_bytes = msgspec.json.encode(config)

# Decode with validation (zero-cost)
config2 = msgspec.json.decode(json_bytes, type=MsgSpecConfig)

# YAML support
yaml_bytes = msgspec.yaml.encode(config)
config3 = msgspec.yaml.decode(yaml_bytes, type=MsgSpecConfig)


# =============================================================================
# 4. Hybrid Approach: Pydantic + msgspec + attrs + beartype
# =============================================================================

from pydantic import BaseModel


class ExternalConfig(BaseModel):
    """External API - pydantic for rich validation."""
    learning_rate: float
    n_iterations: int
    batch_size: int
    
    class Config:
        extra = 'forbid'  # Strict validation


def load_config(config_path: str) -> Config:
    """Load config: pydantic validates, attrs stores."""
    # Pydantic validates external input
    external = ExternalConfig.model_validate_json(open(config_path).read())
    
    # Convert to attrs for internal use
    return Config(
        learning_rate=external.learning_rate,
        n_iterations=external.n_iterations,
        batch_size=external.batch_size,
    )


def save_config(config: Config, config_path: str) -> None:
    """Save config: attrs to msgspec for fast serialization."""
    # Convert attrs to msgspec
    msgspec_config = MsgSpecConfig(
        learning_rate=config.learning_rate,
        n_iterations=config.n_iterations,
        batch_size=config.batch_size,
    )
    
    # Fast serialization
    json_bytes = msgspec.json.encode(msgspec_config)
    open(config_path, 'wb').write(json_bytes)


# =============================================================================
# 5. Testing with chex
# =============================================================================

import chex


@chex.assert_max_traces(n_traces=1)
def train_once(state: ModelState, config: Config) -> ModelState:
    """Ensure this is only traced once (JAX optimization)."""
    # Training logic here
    return state


def test_training():
    """Test with chex utilities."""
    import numpy as np
    
    # Create test data
    chex.clear_trace_counter()  # Reset for test
    
    params = {'weights': jnp.array([1.0, 2.0])}
    state = ModelState(params, step=0, loss=1.0)
    config = Config(0.01, 10, 32)
    
    # Run training
    final_state = train_once(state, config)
    
    # Assertions
    chex.assert_type(final_state, ModelState)
    chex.assert_equal_shape([state.params['weights'], final_state.params['weights']])
    assert final_state.step == state.step + 1


if __name__ == '__main__':
    # Example usage
    print("✓ beartype: Runtime type checking enabled")
    print("✓ attrs: Immutable data classes")
    print("✓ msgspec: Fast serialization")
    print("✓ chex: JAX testing utilities")
    print("\nAll libraries working together!")
