import pytest
from pathlib import Path

@pytest.fixture
def project_root():
    """Returns the root directory of the project."""
    return Path(__file__).parent.parent

@pytest.fixture
def sample_yaml_story():
    """Returns a valid YAML string for a Value Story."""
    return """
metadata:
  story_id: "TEST-001"
  version: "1.0"
  status: "draft"
goal:
  as_a: "As a Tester"
  i_want: "To verify the parser works."
  so_that: "We can trust the tools."
instructions:
  execution_steps:
    - step_number: 1
      action: "Do something."
      validation_rule: "Check it."
context_manifest: []
product:
  type: "Test"
"""

@pytest.fixture
def sample_markdown_story():
    """Returns a valid Markdown string with fenced YAML."""
    return """
# Test Story

```yaml
metadata:
  story_id: "TEST-002"
goal:
  as_a: "As a Tester"
  i_want: "To verify markdown parsing."
  so_that: "We support both formats."
instructions:
  execution_steps:
    - step_number: 1
      action: "Parse this."
      validation_rule: "Parsed."
context_manifest: []
```
"""
