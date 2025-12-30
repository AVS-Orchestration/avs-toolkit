import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock
from avs_toolkit.main import app, dispatch_research

runner = CliRunner()

@pytest.fixture
def mock_httpx(mocker):
    return mocker.patch("httpx.AsyncClient")

def test_validate_command(tmp_path):
    """Test that the validate command passes for a valid story."""
    story_file = tmp_path / "test_story.md"
    story_file.write_text("""
metadata:
  story_id: "CLI-TEST-01"
  version: "1.0"
goal:
  as_a: "As a Tester"
  i_want: "To validate the CLI command functions correctly"
  so_that: "We have confidence."
instructions:
  execution_steps:
    - step_number: 1
      action: "Execute test command properly"
      validation_rule: "Output is green"
context_manifest: []
""")
    result = runner.invoke(app, ["validate", str(story_file)])
    assert result.exit_code == 0
    assert "Governance Pass" in result.stdout

def test_validate_command_fail(tmp_path):
    """Test that validation fails for invalid story."""
    story_file = tmp_path / "bad_story.md"
    story_file.write_text("Not valid yaml")
    result = runner.invoke(app, ["validate", str(story_file)])
    assert result.exit_code == 1
    assert "Governance Failure" in result.stdout

@pytest.mark.asyncio
async def test_research_fallback(mocker):
    """
    Test that dispatch_research tries Gemini first, then Tavily.
    """
    # Mock environment variables
    mocker.patch.dict("os.environ", {"GEMINI_API_KEY": "fake_gemini", "TAVILY_API_KEY": "fake_tavily"})

    # Mock httpx.AsyncClient to simulate responses
    mock_post = mocker.patch("httpx.AsyncClient.post")
    
    # Scenario: Gemini fails (400), Tavily succeeds (200)
    mock_response_gemini = MagicMock()
    mock_response_gemini.status_code = 400
    
    mock_response_tavily = MagicMock()
    mock_response_tavily.status_code = 200
    mock_response_tavily.json.return_value = {"answer": "Tavily Answer"}

    # Configure side_effect to return Gemini response first, then Tavily
    mock_post.side_effect = [mock_response_gemini, mock_response_tavily]

    result = await dispatch_research("Test Query")
    
    assert result == "Tavily Answer"
    assert mock_post.call_count == 2 

def test_assemble_command(tmp_path, mocker):
    """Test the assemble command generates an assembled yaml file."""
    # Mock research to avoid network calls
    mocker.patch("avs_toolkit.main.dispatch_research", return_value="Mocked Research")
    
    story_file = tmp_path / "VS-ASM.md"
    story_file.write_text("""
metadata:
  story_id: "VS-ASM"
goal:
  as_a: "As a Builder"
  i_want: "To assemble a briefcase with context"
  so_that: "It works."
instructions:
  execution_steps:
    - step: 1
      action: "Assemble the briefcase now"
      rule: "Done successfully"
context_manifest:
  - key: "research"
    search_query: "Test"
""")
    
    # We need to run this in the tmp_path so the output file is written there
    # But the app uses Path.cwd(), so we must change directory
    mocker.patch("pathlib.Path.cwd", return_value=tmp_path)
    result = runner.invoke(app, ["assemble", str(story_file)])
    
    assert result.exit_code == 0
    assert "Assembly Complete" in result.stdout
    
    output_file = tmp_path / "VS-ASM-assembled.yaml"
    assert output_file.exists()
    content = output_file.read_text()
    assert "Mocked Research" in content
    assert "assembled_at" in content