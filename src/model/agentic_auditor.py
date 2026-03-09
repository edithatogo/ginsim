"""
Agentic Auditor: Multi-Persona Governance Layer.

Loads stakeholder personas and computes persona-specific welfare verdicts
to measure epistemic divergence and build consensus via Delphi Protocol.
Supports dynamic 'Teaching' of new personas from external documents.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path

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

    def __init__(
        self, 
        config_path: str = "configs/stakeholder_personas.yaml",
        taught_path: str = "configs/taught_stakeholders.yaml"
    ):
        self.config_path = config_path
        self.taught_path = taught_path
        self.personas = {}
        
        # 1. Load standard personas
        self._load_standard_personas()
        
        # 2. Load taught (cached) personas
        self._load_taught_personas()
        
        logger.info(f"AgenticAuditor initialized with {len(self.personas)} personas.")

    def _load_standard_personas(self):
        try:
            if Path(self.config_path).exists():
                with open(self.config_path) as f:
                    config = yaml.safe_load(f)
                self.personas.update(config.get("personas", {}))
        except Exception as e:
            logger.error(f"Failed to load standard personas from {self.config_path}: {e}")

    def _load_taught_personas(self):
        try:
            if Path(self.taught_path).exists():
                with open(self.taught_path) as f:
                    taught = yaml.safe_load(f)
                if taught and "personas" in taught:
                    self.personas.update(taught["personas"])
                    logger.info(f"Loaded {len(taught['personas'])} taught personas from cache.")
        except Exception as e:
            logger.error(f"Failed to load taught personas from {self.taught_path}: {e}")

    def add_persona(self, persona_config: dict[str, Any], persist: bool = True):
        """
        Dynamically add a new persona to the auditor.
        """
        pid = persona_config.get("id")
        if pid:
            self.personas[pid] = persona_config
            logger.info(f"Dynamically added persona: {pid}")
            if persist:
                self.save_taught_personas()

    def save_taught_personas(self):
        """
        Save all non-standard personas to the taught_path for persistence.
        """
        # We assume standard personas are those in the main config
        # This is a bit brittle, but works for the current architecture.
        try:
            with open(self.config_path) as f:
                standard_config = yaml.safe_load(f)
            standard_ids = set(standard_config.get("personas", {}).keys())
            
            taught_personas = {
                pid: pdata for pid, pdata in self.personas.items() 
                if pid not in standard_ids
            }
            
            if taught_personas:
                with open(self.taught_path, "w") as f:
                    yaml.dump({"personas": taught_personas}, f)
                logger.info(f"Saved {len(taught_personas)} taught personas to {self.taught_path}")
        except Exception as e:
            logger.error(f"Failed to save taught personas: {e}")

    def audit_policy(
        self, result: DCBAResult, previous_verdicts: dict[str, PersonaVerdict] | None = None
    ) -> dict[str, PersonaVerdict]:
        """
        Compute subjective verdicts for all loaded personas.
        If previous_verdicts provided, simulates a "Delphi Round" adjustment.
        """
        verdicts = {}

        consensus_mean = 0.0
        if previous_verdicts:
            consensus_mean = float(
                jnp.mean(jnp.array([v.subjective_welfare for v in previous_verdicts.values()]))
            )

        for pid, pdata in self.personas.items():
            w = pdata.get("weighting", {}).copy()

            if previous_verdicts:
                my_prev = previous_verdicts[pid].subjective_welfare
                shift = (consensus_mean - my_prev) * 0.1
            else:
                shift = 0.0

            score = (
                float(result.consumer_surplus) * w.get("consumer_surplus", 0.0)
                + float(result.producer_surplus) * w.get("producer_surplus", 0.0)
                + float(result.health_benefits) * w.get("health_benefits", 0.0)
                + float(result.fiscal_impact) * w.get("fiscal_impact", 0.0)
                + float(result.research_externalities) * w.get("research_externalities", 0.0)
            ) + shift

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
