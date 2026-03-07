from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def load_draws_npy(path: Path) -> list[dict[str, Any]]:
    payload = np.load(path, allow_pickle=True)
    if isinstance(payload, np.ndarray):
        return payload.tolist()
    return list(payload)


def save_draws_npy(draws: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, np.array(draws, dtype=object), allow_pickle=True)


def deterministic_subsample(draws: list[dict[str, Any]], n: int) -> list[dict[str, Any]]:
    if n <= 0:
        return []
    if len(draws) <= n:
        return list(draws)
    if n == 1:
        return [draws[0]]

    indices = np.linspace(0, len(draws) - 1, num=n)
    return [draws[int(round(index))] for index in indices]
