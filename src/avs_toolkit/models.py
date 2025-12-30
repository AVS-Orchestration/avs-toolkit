from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class Metadata(BaseModel):
    story_id: str
    version: str = "1.0"
    author: Optional[str] = None
    status: str = "draft"
    preferred_model: Optional[str] = Field(None)
    assembled_at: Optional[str] = Field(None)

class Goal(BaseModel):
    as_a: str = Field(...)
    i_want: str = Field(..., min_length=20)
    so_that: str = Field(...)

    @field_validator('as_a')
    @classmethod
    def validate_as_a(cls, v: str):
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
    search_query: Optional[str] = None
    mcp_tool_name: Optional[str] = None
    mcp_tool_args: Optional[Dict[str, Any]] = None
    content: Optional[str] = None

class MCPServerConfig(BaseModel):
    name: str = Field(...)
    command: str = Field(...)
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None

class Product(BaseModel):
    type: str = "Document"
    format: str = "Markdown"
    output_path: str = "outputs"
    handoff_target: Optional[str] = None

class ValueStory(BaseModel):
    metadata: Metadata
    goal: Goal
    instructions: Instructions
    mcp_servers: List[MCPServerConfig] = Field(default_factory=list)
    context_manifest: List[ContextManifestItem]
    product: Product = Field(default_factory=Product)

    @model_validator(mode='after')
    def validate_mcp_alignment(self) -> 'ValueStory':
        """
        Governance Check: Ensures any requested MCP tools have 
        at least one server defined in the manifest.
        """
        has_tool_call = any(item.mcp_tool_name for item in self.context_manifest)
        if has_tool_call and not self.mcp_servers:
            raise ValueError(
                "Context Manifest contains MCP tool calls, but no 'mcp_servers' are defined. "
                "The Agent will have 'Context Blindness' for these items."
            )
        return self

    @property
    def is_assembled(self) -> bool:
        return self.metadata.assembled_at is not None