import pytest
from avs_toolkit.parser import parse_markdown_story

def test_parse_fenced_yaml_block():
    """Test extracting YAML from fenced code blocks."""
    content = """
# Title
Some text.

```yaml
metadata:
  story_id: "VS-TEST-01"
goal:
  as_a: "As a User"
  i_want: "To test fenced blocks"
  so_that: "It works."
instructions:
  execution_steps:
    - step: 1
      action: "Test"
      validation_rule: "Pass"
```
"""
    data = parse_markdown_story(content)
    assert data["metadata"]["story_id"] == "VS-TEST-01"
    assert data["goal"]["i_want"] == "To test fenced blocks"

def test_parse_hybrid_markdown():
    """Test parsing raw markdown with headers (fallback mode)."""
    content = """
metadata:
  story_id: "VS-TEST-02"

# Goal Section
goal:
  as_a: "As a User"
  i_want: "To test hybrid mode"
  so_that: "It works."

# Instructions Section
instructions:
  execution_steps:
    - step: 1
      action: "Test"
      validation_rule: "Pass"
"""
    data = parse_markdown_story(content)
    assert data["metadata"]["story_id"] == "VS-TEST-02"
    assert data["goal"]["i_want"] == "To test hybrid mode"

def test_parse_empty_content():
    """Test parsing empty content returns empty dict."""
    data = parse_markdown_story("")
    assert data == {}

def test_parse_malformed_yaml():
    """Test parsing malformed content returns empty dict or handles gracefully."""
    content = """
```yaml
key: [ unclosed list
```
"""
    data = parse_markdown_story(content)
    assert data == {} 
