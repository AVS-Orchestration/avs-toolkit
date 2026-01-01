from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class Metadata(BaseModel):
    """
    Administrative tracking for the Value Story.
    Ensures every unit of work has an owner, version, and status.
    """
    story_id: str = Field(..., description="Unique identifier for the story (e.g., VS-001).")
    version: str = Field("1.0", description="Semantic version of this story logic.")
    author: Optional[str] = Field(None, description="The Human Architect who designed this story.")
    status: str = Field("draft", description="Lifecycle status: draft, active, or archived.")
    provider: str = Field("ollama", description="The LLM backend provider (e.g., ollama, google-gemini).")
    preferred_model: Optional[str] = Field(
        None, 
        description="The recommended LLM (e.g., llama3, gemma2:27b) for this specific logic."
    )
    assembled_at: Optional[str] = Field(
        None, 
        description="ISO timestamp added during assembly. Indicates the 'Briefcase' is ready."
    )

class Goal(BaseModel):
    """
    The 'North Star' of the Value Story.
    Follows the Agile format to provide persona, technical target, and business rationale.
    """
    as_a: str = Field(..., description="The persona or role receiving the value.")
    i_want: str = Field(
        ..., 
        min_length=20, 
        description="The specific technical outcome or deliverable required."
    )
    so_that: str = Field(..., description="The business value or 'Why' behind this task.")

    @field_validator('as_a')
    @classmethod
    def validate_as_a(cls, v: str):
        """Self-healing validator: ensures the persona starts with 'As a'."""
        if not v.lower().startswith("as a"):
            return f"As a {v}"
        return v

class InstructionStep(BaseModel):
    """A single, algorithmically legible step in the execution logic."""
    step_number: int = Field(..., description="Sequential order of execution.")
    action: str = Field(..., min_length=10, description="What the Agent must actually do.")
    validation_rule: str = Field(..., min_length=5, description="How to verify the action was successful.")

class Instructions(BaseModel):
    """The core algorithm defining the Agent's reasoning path."""
    reasoning_pattern: str = Field(
        "Chain-of-Thought", 
        description="The mental model the LLM should adopt (CoT, Reflection, etc)."
    )
    execution_steps: List[InstructionStep] = Field(..., description="List of granular actions.")

class ContextManifestItem(BaseModel):
    """
    A single asset requirement.
    Defines the 'Information Hunt' required to eliminate context blindness.
    """
    key: Optional[str] = Field(None, description="Unique label for the asset.")
    description: Optional[str] = Field(None, description="Human-readable purpose of this asset.")
    default_path: Optional[str] = Field(None, description="Local file path for injection.")
    search_query: Optional[str] = Field(None, description="Grounding query for live web research.")
    mcp_tool_name: Optional[str] = Field(None, description="MCP tool name to invoke (e.g., 'scrape').")
    mcp_tool_args: Optional[Dict[str, Any]] = Field(None, description="Arguments for the MCP tool.")
    content: Optional[str] = Field(None, description="The actual text of the asset, populated during assembly.")

class MCPServerConfig(BaseModel):
    """Configuration for ephemeral Model Context Protocol servers."""
    name: str = Field(..., description="Unique identifier for the server.")
    command: str = Field(..., description="The launch command (e.g., 'npx', 'uvx').")
    args: List[str] = Field(default_factory=list, description="Launch arguments.")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables (e.g., API keys).")

class Product(BaseModel):
    """Defines the deliverable and the handoff mechanism."""
    type: str = Field("Document", description="Nature of the product (Document, Analysis, Code).")
    format: str = Field("Markdown", description="File format (Markdown, JSON).")
    output_path: str = Field("outputs", description="Local directory for the product.")
    handoff_repo: Optional[str] = Field(
        None, 
        description="Target repository in the AVS-Orchestration Org."
    )
    handoff_path: Optional[str] = Field(
        None, 
        description="Specific path within the handoff repository."
    )

class ValueStory(BaseModel):
    """
    The top-level container for a unit of work.
    Combines administration, logic, and data requirements.
    """
    metadata: Metadata
    goal: Goal
    instructions: Instructions
    mcp_servers: List[MCPServerConfig] = Field(
        default_factory=list, 
        description="Manifest of required MCP servers."
    )
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
        """Determines if the story has already been packaged with context."""
        return self.metadata.assembled_at is not None