"""
HTA (Health Technology Assessment) Interoperability and Export.

Provides a standardized JSON schema for policy evaluation outcomes,
enabling auditable replication and cross-platform integration.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from loguru import logger

from src.model.reporting_common import PolicyEvaluationResult


@dataclass(frozen=True)
class HTAOutcomeSchema:
    """Standardized schema for HTA dossiers."""

    version: str = "1.0.0"
    metadata: dict[str, Any] = None
    inputs: dict[str, Any] = None
    policy: dict[str, Any] = None
    outcomes: dict[str, Any] = None
    uncertainty: dict[str, Any] | None = None


class HTAExporter:
    """Handles export of results to standardized formats."""

    @staticmethod
    def to_json_dossier(result: PolicyEvaluationResult, params: Any, out_path: Path | str) -> Path:
        """Export a single evaluation result to a standardized JSON dossier."""
        out_path = Path(out_path)

        # 1. Prepare Metadata
        metadata = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "jurisdiction": result.jurisdiction,
            "policy_name": result.policy_name,
            "engine": "GINSIM-JAX",
            "schema_version": "1.0.0",
        }

        # 2. Prepare Inputs (Model Parameters)
        # 3. Prepare Outcomes (Welfare Ledger)
        def _to_plain(val: Any) -> Any:
            """Recursive conversion of JAX/NumPy types to plain Python."""
            if hasattr(val, "tolist"):
                return val.tolist()
            if isinstance(val, (np.float32, np.float64, np.int32, np.int64)):
                return float(val)
            if isinstance(val, dict):
                return {k: _to_plain(v) for k, v in val.items()}
            if isinstance(val, (list, tuple)):
                return [_to_plain(v) for v in val]
            return val

        input_params = {
            k: _to_plain(v)
            for k, v in asdict(params).items()
            if k not in ["jurisdiction", "calibration_date"]
        }

        outcomes = {
            "utilitarian_welfare": float(result.welfare_impact),
            "equity_weighted_welfare": float(result.equity_weighted_welfare),
            "components": {
                "consumer_surplus": float(result.dcba_result.consumer_surplus),
                "producer_surplus": float(result.dcba_result.producer_surplus),
                "health_benefits": float(result.dcba_result.health_benefits),
                "fiscal_impact": float(result.dcba_result.fiscal_impact),
                "research_externalities": float(result.dcba_result.research_externalities),
            },
            "behavioral": {
                "testing_uptake": float(result.testing_uptake),
                "compliance_rate": float(result.compliance_rate),
            },
            "clinical": _to_plain(result.clinical_outcomes),
            "market": _to_plain(result.insurance_premiums),
            "all_metrics": _to_plain(result.all_metrics),
        }

        # 4. Assemble Dossier
        dossier = {
            "metadata": metadata,
            "inputs": input_params,
            "outcomes": outcomes,
        }

        # 5. Write to File
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(dossier, f, indent=2)

        logger.info(f"HTA Dossier exported to: {out_path}")
        return out_path

    @staticmethod
    def to_excel_template(results: list[PolicyEvaluationResult], out_path: Path | str):
        """Export a list of results to a multi-sheet Excel file for HTA submission."""
        import pandas as pd

        out_path = Path(out_path)

        summary_rows = []
        ledger_rows = []

        for res in results:
            summary_rows.append(
                {
                    "Policy": res.policy_name,
                    "Jurisdiction": res.jurisdiction,
                    "Uptake": float(res.testing_uptake),
                    "Welfare (Net)": float(res.welfare_impact),
                    "Welfare (Equity)": float(res.equity_weighted_welfare),
                    "Compliance": float(res.compliance_rate),
                }
            )

            ledger_rows.append(
                {
                    "Policy": res.policy_name,
                    "Consumer Surplus": float(res.dcba_result.consumer_surplus),
                    "Producer Surplus": float(res.dcba_result.producer_surplus),
                    "Health Benefits": float(res.dcba_result.health_benefits),
                    "Fiscal Impact": float(res.dcba_result.fiscal_impact),
                    "Research Ext": float(res.dcba_result.research_externalities),
                }
            )

        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            pd.DataFrame(summary_rows).to_excel(writer, sheet_name="Summary", index=False)
            pd.DataFrame(ledger_rows).to_excel(writer, sheet_name="Welfare_Ledger", index=False)

        logger.info(f"HTA Excel Template exported to: {out_path}")
        return out_path
