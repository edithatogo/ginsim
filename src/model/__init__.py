"""Core economic model package with lazy public exports.

Keep imports lightweight during Streamlit startup while exposing the public model API.
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .agentic_auditor import AgenticAuditor, PersonaVerdict
    from .dcba_ledger import DCBAResult, compute_dcba
    from .parameters import ModelParameters, PolicyConfig
    from .pipeline import evaluate_single_policy, run_full_evaluation

_EXPORT_MODULES = {
    "AgenticAuditor": "agentic_auditor",
    "DCBAResult": "dcba_ledger",
    "ModelParameters": "parameters",
    "PersonaVerdict": "agentic_auditor",
    "PolicyConfig": "parameters",
    "compute_dcba": "dcba_ledger",
    "evaluate_single_policy": "pipeline",
    "run_full_evaluation": "pipeline",
}
__all__ = [
    "AgenticAuditor",
    "DCBAResult",
    "ModelParameters",
    "PersonaVerdict",
    "PolicyConfig",
    "compute_dcba",
    "evaluate_single_policy",
    "run_full_evaluation",
]


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        message = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(message)
    value = getattr(import_module(f".{module_name}", __name__), name)
    globals()[name] = value
    return value
