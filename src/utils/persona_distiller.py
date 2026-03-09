"""
Persona Distiller: LLM-driven organizational priority extraction.

Transforms raw policy text into structured component weightings for the Agentic Auditor.
"""

from __future__ import annotations

import re
from typing import Any, Dict
from loguru import logger

MOCK_POLICY_STATEMENT = """
Our organization prioritizes fiscal sustainability above all else. 
We believe the state's budget must be protected from excessive health spending. 
While consumer rights are important, they cannot come at the expense of market stability 
and the profitability of the insurance sector which provides thousands of jobs. 
Research is a secondary concern compared to immediate economic efficiency.
"""

class PersonaDistiller:
    """
    Distills policy documents into numerical weighting vectors.
    """

    def __init__(self, model_name: str = "mock-llm"):
        self.model_name = model_name

    def distill_persona(self, text: str, name: str = "Custom Persona") -> Dict[str, Any]:
        """
        Parses text and returns a persona configuration dictionary.
        In a production environment, this would call an LLM API.
        """
        logger.info(f"Distilling persona '{name}' from text (length: {len(text)})")
        
        # 1. LLM Prompt Construction (Theoretical)
        prompt = f"""
        Analyze the following policy text and assign weightings (0.0 to 1.0) 
        to these five economic components such that they sum to 1.0:
        - consumer_surplus
        - producer_surplus
        - health_benefits
        - fiscal_impact
        - research_externalities
        
        TEXT: {text}
        """
        
        # 2. Mock Logic: Keyword-based heuristic for development
        weights = self._mock_distillation_heuristic(text)
        
        # 3. Construct Persona Config
        persona_id = re.sub(r'[^a-z0-9]', '_', name.lower())
        
        return {
            "id": persona_id,
            "name": name,
            "focus": text[:100] + "...",
            "weighting": weights,
            "prompt": f"You are a stakeholder representing: {name}. Use the distilled weights to evaluate policy."
        }

    def _mock_distillation_heuristic(self, text: str) -> Dict[str, float]:
        """Heuristic fallback for distillation without live LLM."""
        text_lower = text.lower()
        weights = {
            "consumer_surplus": 0.2,
            "producer_surplus": 0.2,
            "health_benefits": 0.2,
            "fiscal_impact": 0.2,
            "research_externalities": 0.2
        }
        
        # Adjust based on keywords
        if "fiscal" in text_lower or "budget" in text_lower:
            weights["fiscal_impact"] += 0.2
            weights["consumer_surplus"] -= 0.05
            weights["health_benefits"] -= 0.05
            weights["producer_surplus"] -= 0.05
            weights["research_externalities"] -= 0.05
            
        if "patient" in text_lower or "health" in text_lower:
            weights["health_benefits"] += 0.2
            # Balance others... (simplified)
            
        # Ensure sum is 1.0 (Normalization)
        total = sum(weights.values())
        return {k: v / total for k, v in weights.items()}
