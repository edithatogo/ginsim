
import pytest
import jax.numpy as jnp
from src.model.dcba_ledger import DCBAResult
from src.model.agentic_auditor import AgenticAuditor

def test_auditor_initialization():
    auditor = AgenticAuditor("configs/stakeholder_personas.yaml")
    assert len(auditor.personas) == 4
    assert "nature" in auditor.personas
    assert "lancet" in auditor.personas

def test_audit_logic():
    auditor = AgenticAuditor("configs/stakeholder_personas.yaml")
    
    # Create a result where Health Benefits is the dominant positive factor
    result = DCBAResult(
        net_welfare=100.0,
        equity_weighted_welfare=150.0,
        consumer_surplus=10.0,
        producer_surplus=10.0,
        health_benefits=200.0,
        fiscal_impact=-50.0,
        research_externalities=10.0,
        distributional_weight=1.0,
        equity_factor=1.5,
        time_horizon=20
    )
    
    verdicts = auditor.audit_policy(result)
    
    # Lancet should have a high subjective welfare because it weights health_benefits at 0.5
    # score = 10*0.2 + 10*0.05 + 200*0.5 - 50*0.1 + 10*0.15 = 2 + 0.5 + 100 - 5 + 1.5 = 99.0
    assert pytest.approx(verdicts["lancet"].subjective_welfare, 0.1) == 99.0
    
    # Treasury weights fiscal_impact at 0.5
    # score = 10*0.1 + 10*0.3 + 200*0.1 - 50*0.5 + 10*0 = 1 + 3 + 20 - 25 + 0 = -1.0
    assert pytest.approx(verdicts["treasury"].subjective_welfare, 0.1) == -1.0

def test_delphi_consensus():
    auditor = AgenticAuditor("configs/stakeholder_personas.yaml")
    result = DCBAResult(
        net_welfare=1000.0,
        equity_weighted_welfare=1000.0,
        consumer_surplus=500.0,
        producer_surplus=200.0,
        health_benefits=400.0,
        fiscal_impact=-100.0,
        research_externalities=50.0,
        distributional_weight=1.0,
        equity_factor=1.0,
        time_horizon=20
    )
    
    history = auditor.run_delphi_session(result, max_rounds=5)
    
    # Divergence should decrease
    div_start = auditor.compute_divergence(history[0])["coefficient_of_variation"]
    div_end = auditor.compute_divergence(history[-1])["coefficient_of_variation"]
    
    assert div_end < div_start
    assert len(history) <= 5
