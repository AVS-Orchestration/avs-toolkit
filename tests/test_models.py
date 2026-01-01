import pytest
from pydantic import ValidationError
from avs_toolkit.models import ValueStory, Goal, Metadata, Instructions, ContextManifestItem, MCPServerConfig

def test_goal_validator_as_a():
    """Test that 'as_a' field automatically prepends 'As a ' if missing."""
    goal = Goal(
        as_a="Software Engineer", 
        i_want="To have auto-complete functionality in the IDE", 
        so_that="I save time"
    )
    assert goal.as_a == "As a Software Engineer"

    goal_correct = Goal(
        as_a="As a User", 
        i_want="To have validation rules that ensure quality", 
        so_that="It works"
    )
    assert goal_correct.as_a == "As a User"

def test_valuestory_mcp_alignment_error():
    """Test that validation fails if an MCP tool is used without a defined server."""
    with pytest.raises(ValidationError) as excinfo:
        ValueStory(
            metadata=Metadata(story_id="TEST-FAIL"),
            goal=Goal(as_a="Tester", i_want="To fail validation gracefully when servers are missing", so_that="Safe"),
            instructions=Instructions(execution_steps=[
                {"step_number": 1, "action": "Perform a test action here", "validation_rule": "Verified successfully"}
            ]),
            context_manifest=[
                ContextManifestItem(key="data", mcp_tool_name="scrape", mcp_tool_args={})
            ],
            mcp_servers=[]  # Empty servers list should trigger error
        )
    assert "Context Manifest contains MCP tool calls, but no 'mcp_servers' are defined" in str(excinfo.value)

def test_valuestory_mcp_alignment_success():
    """Test that validation passes if server is present for tool call."""
    story = ValueStory(
        metadata=Metadata(story_id="TEST-PASS"),
        goal=Goal(as_a="Tester", i_want="To pass validation when servers are correctly defined", so_that="Safe"),
        instructions=Instructions(execution_steps=[
            {"step_number": 1, "action": "Perform a test action here", "validation_rule": "Verified successfully"}
        ]),
        context_manifest=[
            ContextManifestItem(key="data", mcp_tool_name="scrape", mcp_tool_args={})
        ],
        mcp_servers=[
            MCPServerConfig(name="scraper", command="npx", args=["firecrawl"])
        ]
    )
    assert story.metadata.story_id == "TEST-PASS"

def test_metadata_provider_default():
    """Test that the 'provider' field defaults to 'ollama'."""
    meta = Metadata(story_id="TEST-DEFAULT")
    assert meta.provider == "ollama"

    meta_cloud = Metadata(story_id="TEST-CLOUD", provider="google-gemini")
    assert meta_cloud.provider == "google-gemini"