"""
Agentic Auditor: Multi-Persona Governance Layer.

Loads stakeholder personas and computes persona-specific welfare verdicts
to measure epistemic divergence and build consensus via Delphi Protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import jax.numpy as jnp
import yaml
from loguru import logger

from .dcba_ledger import DCBAResult


@dataclass(frozen=True)
class PersonaVerdict:
    """The outcome of a single persona's audit."""

    persona_id: str
    name: str
    subjective_welfare: float
    qualitative_feedback: str
    key_concerns: list[str] = field(default_factory=list)
    weight_adjustments: dict[str, float] = field(default_factory=dict)


class AgenticAuditor:
    """
    Orchestrates multi-persona audits and Delphi consensus rounds.
    """

    def __init__(self, config_path: str = "configs/stakeholder_personas.yaml"):
        try:
            with open(config_path) as f:
                self.config = yaml.safe_load(f)
            self.personas = self.config["personas"]
            logger.info(f"AgenticAuditor initialized with {len(self.personas)} personas.")
        except Exception as e:
            logger.error(f"Failed to load stakeholder personas from {config_path}: {e}")
            self.personas = {}

    def audit_policy(
        self, result: DCBAResult, previous_verdicts: dict[str, PersonaVerdict] | None = None
    ) -> dict[str, PersonaVerdict]:
        """
        Compute subjective verdicts for all loaded personas.
        If previous_verdicts provided, simulates a "Delphi Round" adjustment.
        """
        verdicts = {}

        # Calculate consensus welfare mean if in Delphi mode
        consensus_mean = 0.0
        if previous_verdicts:
            consensus_mean = float(
                jnp.mean(jnp.array([v.subjective_welfare for v in previous_verdicts.values()]))
            )

        for pid, pdata in self.personas.items():
            # 1. Base weights from config
            w = pdata.get("weighting", {}).copy()

            # 2. Consensus Adjustment (Mathematical Proxy for 'Listening' to others)
            # In a real Delphi round, personas might shift their priorities if they see
            # a massive divergence from the group mean.
            if previous_verdicts:
                my_prev = previous_verdicts[pid].subjective_welfare
                # Shift factor: 10% move towards the mean
                shift = (consensus_mean - my_prev) * 0.1
                # We apply this as a direct scalar shift to the score for this proxy
            else:
                shift = 0.0

            # 3. Compute Score
            score = (
                float(result.consumer_surplus) * w.get("consumer_surplus", 0.0)
                + float(result.producer_surplus) * w.get("producer_surplus", 0.0)
                + float(result.health_benefits) * w.get("health_benefits", 0.0)
                + float(result.fiscal_impact) * w.get("fiscal_impact", 0.0)
                + float(result.research_externalities) * w.get("research_externalities", 0.0)
            ) + shift

            # 4. Construct Verdict
            # For now, qualitative feedback is generated as a structured summary.
            feedback = self._generate_simulated_feedback(pid, score, result)

            verdicts[pid] = PersonaVerdict(
                persona_id=pid,
                name=pdata.get("name", pid),
                subjective_welfare=float(score),
                qualitative_feedback=feedback,
                key_concerns=self._extract_key_concerns(pid, result),
            )

        return verdicts

    def run_delphi_session(
        self, result: DCBAResult, max_rounds: int = 3
    ) -> list[dict[str, PersonaVerdict]]:
        """
        Run multiple rounds of the Delphi Protocol until consensus stabilizes.
        """
        history = []
        current_verdicts = self.audit_policy(result)
        history.append(current_verdicts)

        for r in range(max_rounds - 1):
            div = self.compute_divergence(current_verdicts)
            if div["coefficient_of_variation"] < 0.05:
                logger.info(f"Consensus reached in round {r + 1}")
                break

            current_verdicts = self.audit_policy(result, previous_verdicts=current_verdicts)
            history.append(current_verdicts)

        return history

    def compute_divergence(self, verdicts: dict[str, PersonaVerdict]) -> dict[str, float]:
        """
        Calculate metrics for Epistemic Divergence.
        """
        if not verdicts or len(verdicts) < 2:
            return {"std_dev": 0.0, "coefficient_of_variation": 0.0}

        scores = jnp.array([v.subjective_welfare for v in verdicts.values()])
        mean_val = jnp.mean(scores)
        std_val = jnp.std(scores)
        cv = std_val / (jnp.abs(mean_val) + 1e-10)

        return {
            "mean_subjective_welfare": float(mean_val),
            "std_dev": float(std_val),
            "coefficient_of_variation": float(cv),
            "range": float(jnp.max(scores) - jnp.min(scores)),
        }

    def _generate_simulated_feedback(self, pid: str, score: float, result: DCBAResult) -> str:
        """Structured feedback generator (simulates persona reasoning)."""
        if score > 0:
            sentiment = "Cautiously Optimistic" if score < 100 else "Strongly Supportive"
        else:
            sentiment = "Critical" if score > -100 else "Strongly Opposed"

        return f"Persona '{pid}' evaluates this scenario as '{sentiment}'. Subjective Value: {score:.2f}M."

    def _extract_key_concerns(self, pid: str, result: DCBAResult) -> list[str]:
        """Heuristic-based concern extraction."""
        concerns = []
        if pid == "treasury" and float(result.fiscal_impact) < 0:
            concerns.append("Negative fiscal impact detected; unsustainable public cost.")
        if pid == "lancet" and float(result.health_benefits) < 10:
            concerns.append("Marginal health gains; policy may not justify clinical overhead.")
        if pid == "nature" and float(result.research_externalities) < 0:
            concerns.append("Scientific data loss due to privacy restrictions.")
        if pid == "watchdog" and float(result.consumer_surplus) < 0:
            concerns.append("Consumers are worse off under this regime.")
        return concerns
