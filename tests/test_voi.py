import jax.numpy as jnp
from src.model.voi import evpi, evppi

def test_evpi_nonnegative():
    nb = jnp.array([[0.0, 1.0],[0.5, 0.2],[1.0, 0.0]])
    assert float(evpi(nb)) >= -1e-8

def test_evppi_nonnegative():
    nb = jnp.array([[0.0, 1.0],[0.5, 0.2],[1.0, 0.0]])
    p = jnp.array([0.1, 0.2, 0.3])
    assert float(evppi(nb, p, n_bins=2)) >= -1e-8
