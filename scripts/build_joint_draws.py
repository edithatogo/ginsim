from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from src.utils.posterior import deterministic_subsample, load_draws_npy, save_draws_npy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--n_draws", type=int, default=1000)
    parser.add_argument("--mapping", default="")
    parser.add_argument("--behavior", default="")
    parser.add_argument("--clinical", default="")
    parser.add_argument("--insurance", default="")
    parser.add_argument("--passthrough", default="")
    parser.add_argument("--data_quality", default="")
    parser.add_argument("--mode", default="common_index", choices=["common_index", "independent"])
    args = parser.parse_args()

    group_paths = {
        "mapping": args.mapping,
        "behavior": args.behavior,
        "clinical": args.clinical,
        "insurance": args.insurance,
        "passthrough": args.passthrough,
        "data_quality": args.data_quality,
    }

    groups: dict[str, list[dict[str, Any]]] = {}
    for g, p in group_paths.items():
        if p:
            draws = load_draws_npy(Path(p))
            groups[g] = deterministic_subsample(draws, args.n_draws)

    n = args.n_draws
    out_draws = []
    for i in range(n):
        d: dict[str, Any] = {}
        for g, draws in groups.items():
            if args.mode == "common_index":
                idx = round(i * (len(draws) - 1) / (n - 1)) if n > 1 else 0
            else:
                idx = i % len(draws)
            d[g] = draws[idx]
        out_draws.append(d)

    save_draws_npy(Path(args.out), out_draws)
    print(f"Wrote joint draws: {args.out} (n={n}, groups={list(groups.keys())})")


if __name__ == "__main__":
    main()
