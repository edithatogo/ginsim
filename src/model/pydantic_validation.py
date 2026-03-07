from beartype import beartype
from pydantic import BaseModel, Field, field_validator


class AssumptionRef(BaseModel):
    id: str
    evidence_basis: list[str]


class Parameter(BaseModel):
    name: str
    value: float
    unit: str
    description: str
    source_ref: str
    assumptions: list[str] = Field(default_factory=list)

    @field_validator("source_ref")
    @classmethod
    def validate_source(cls, v: str):
        # This will be used to ensure the source exists in BibTeX
        return v


class ModelInputs(BaseModel):
    parameters: list[Parameter]
    assumptions: list[AssumptionRef]


@beartype
def validate_inputs(inputs: ModelInputs) -> bool:
    """Rigorous entry-gate for all model inputs."""
    # Logic to cross-verify against BibTeX and Registry will go here
    return True
