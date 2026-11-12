import jax.numpy as jnp

from src.model.voi import compute_evpi


def test_evpi_nonnegative():
    nb = jnp.array([[0.0, 1.0], [0.5, 0.2], [1.0, 0.0]])
    # compute_evpi expects (n_policies, n_draws)
    # The nb array above is (3, 2) which matches
    assert float(compute_evpi(nb)) >= -1e-8
