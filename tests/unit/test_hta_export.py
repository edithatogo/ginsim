import json

import pandas as pd
import pytest

from src.model.dcba_ledger import DCBAResult
from src.model.parameters import get_default_parameters
from src.model.reporting_common import PolicyEvaluationResult
from src.utils.hta_export import HTAExporter


@pytest.fixture
def mock_result():
    dcba = DCBAResult(
        consumer_surplus=100.0,
        producer_surplus=-50.0,
        health_benefits=200.0,
        fiscal_impact=10.0,
        research_externalities=5.0,
        net_welfare=255.0,
        equity_weighted_welfare=300.0,
        equity_factor=1.2,
        distributional_weight=1.0,
    )
    return PolicyEvaluationResult(
        policy_name="test_policy",
        jurisdiction="australia",
        testing_uptake=0.6,
        welfare_impact=255.0,
        equity_weighted_welfare=300.0,
        clinical_outcomes={"total_qaly_gains": 1.5, "total_cost_savings": 500.0},
        insurance_premiums={"premium_high": 0.2, "premium_low": 0.1},
        compliance_rate=0.95,
        dcba_result=dcba,
        all_metrics={"welfare": {}, "proxy": {}},
    )


def test_json_export(mock_result, tmp_path):
    params = get_default_parameters()
    out_path = tmp_path / "dossier.json"
    HTAExporter.to_json_dossier(mock_result, params, out_path)

    assert out_path.exists()
    with open(out_path) as f:
        data = json.load(f)

    assert data["metadata"]["policy_name"] == "test_policy"
    assert data["outcomes"]["utilitarian_welfare"] == 255.0
    assert "inputs" in data


def test_excel_export(mock_result, tmp_path):
    out_path = tmp_path / "submission.xlsx"
    HTAExporter.to_excel_template([mock_result], out_path)

    assert out_path.exists()
    df = pd.read_excel(out_path, sheet_name="Summary")
    assert df.iloc[0]["Policy"] == "test_policy"
    assert df.iloc[0]["Welfare (Net)"] == 255.0
