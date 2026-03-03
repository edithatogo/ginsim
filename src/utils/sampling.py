from __future__ import annotations

from typing import Sequence, Any, Literal
import numpy as np

SamplingMode = Literal["independent", "common_index", "random"]

def index_map(i: int, n_draws: int, n_available: int) -> int:
    if n_available <= 0:
        raise ValueError("n_available must be positive")
    if n_draws <= 1:
        return 0
    return int(round(i * (n_available - 1) / (n_draws - 1)))

def select_draw(draws: Sequence[Any] | None, i: int, n_draws: int, mode: SamplingMode, rng: np.random.Generator) -> Any | None:
    if draws is None or len(draws) == 0:
        return None
    if mode == "independent":
        return draws[i % len(draws)]
    if mode == "common_index":
        return draws[index_map(i, n_draws, len(draws))]
    if mode == "random":
        return draws[int(rng.integers(0, len(draws)))]
    raise ValueError(f"Unknown sampling mode: {mode}")
