from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class Metadata(BaseModel):
    story_id: str
    version: str = "1.0"
    author: Optional[str] = None
    status: str = "draft"
    preferred_model: Optional[str] = Field(
        None,
        description="The specific Ollama model (e.g., llama3:70b) recommended by the Architect for this story."
    )
    assembled_at: Optional[str] = Field(
        None, 
        description="ISO timestamp indicating when context was injected. If null, this is a template/definition."
    )

class Goal(BaseModel):
    as_a: str = Field(..., description="The persona or role receiving the value.")
    i_want: str = Field(..., min_length=20, description="The technical outcome or product required.")
    so_that: str = Field(..., description="The business value or rationale for the agent.")

    @field_validator('as_a')
    @classmethod
    def validate_as_a(cls, v: str):
        """Self-healing validator: ensures the persona starts with 'As a'."""
        if not v.lower().startswith("as a"):
            return f"As a {v}"
        return v

class InstructionStep(BaseModel):
    step_number: int
    action: str = Field(..., min_length=10)
    validation_rule: str = Field(..., min_length=5)

class Instructions(BaseModel):
    reasoning_pattern: str = "Chain-of-Thought"
    execution_steps: List[InstructionStep]

class ContextManifestItem(BaseModel):
    key: Optional[str] = None
    description: Optional[str] = None
    default_path: Optional[str] = None
    search_query: Optional[str] = Field(
        None, 
        description="An internet search query to execute during assembly to fetch current data."
    )
    content: Optional[str] = Field(
        None, 
        description="The actual text of the asset or search result, populated during assembly."
    )

class Product(BaseModel):
    type: str = "Document"
    format: str = "Markdown"
    output_path: str = "outputs"
    handoff_target: Optional[str] = None

class ValueStory(BaseModel):
    metadata: Metadata
    goal: Goal
    instructions: Instructions
    context_manifest: List[ContextManifestItem]
    product: Product = Field(default_factory=Product)
    
    @property
    def is_assembled(self) -> bool:
        """Determines if the story has already been packaged with context."""
        return self.metadata.assembled_at is not None