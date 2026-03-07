from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
from pydantic import BaseModel, ValidationError

from src.model.param_schema import (
    BehaviorParamsDraw,
    ClinicalParamsDraw,
    DataQualityParamsDraw,
    InsuranceParamsDraw,
    PassThroughParamsDraw,
    PolicyMappingParamsDraw,
)
from src.utils.posterior import save_draws_npy

SCHEMAS: dict[str, type[BaseModel]] = {
    "behavior": BehaviorParamsDraw,
    "clinical": ClinicalParamsDraw,
    "insurance": InsuranceParamsDraw,
    "passthrough": PassThroughParamsDraw,
    "data_quality": DataQualityParamsDraw,
    "mapping": PolicyMappingParamsDraw,
}


def convert(csv_path: Path, kind: str) -> list[dict[str, Any]]:
    if kind not in SCHEMAS:
        message = f"Unknown kind: {kind}. Choose from {sorted(SCHEMAS.keys())}"
        raise ValueError(message)
    schema = SCHEMAS[kind]

    df = pd.read_csv(csv_path, comment="#")
    draws: list[dict[str, Any]] = []
    errors: list[str] = []

    for i, row in df.iterrows():
        d = {k: row[k] for k in df.columns}
        d = {k: (v.item() if hasattr(v, "item") else v) for k, v in d.items()}
        try:
            obj = schema(**d)
            draws.append(obj.model_dump())
        except ValidationError as e:
            errors.append(f"Row {i}: {e}")

    if errors:
        msg = "\n".join(errors[:20])
        message = f"Validation failed for {len(errors)} rows. First errors:\n{msg}"
        raise ValueError(message)

    return draws


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--kind", required=True, choices=sorted(SCHEMAS.keys()))
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    draws = convert(Path(args.csv), args.kind)
    save_draws_npy(Path(args.out), draws)
    print(f"Wrote {len(draws)} draws to {args.out}")


if __name__ == "__main__":
    main()
