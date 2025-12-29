# VS-000: Template for New Value Stories

```txt
# ARCHITECT'S GUIDE: How to use this template
# 1. Provide a Story ID (VS-XXX) in the title above.
# 2. Fill in the 'goal' with a statement longer than 20 characters.
# 3. List at least 2 'execution_steps' with specific 'validation_rules'.
# 4. Define your 'context_manifest' using local paths or MCP URIs.
```

metadata:
  story_id: "VS-000"
  version: "1.3"
  author: "Patrick Heaney"
  preferred_model: "llama3"

## THE GOAL: The "North Star" for the Agentic-Agent

goal:
  as_a: "As a <customer/role who receives the value>"
  i_want: >
    Define exactly what success looks like in at least 20 characters.
    Include specific requirements as bullet points if necessary.
  so_that: >
    The agent understands the business value and rationale behind the task.

## INSTRUCTIONS: The Core Algorithm (Execution Logic)

instructions:
  reasoning_pattern: "Chain-of-Thought"
  execution_steps:
    - step: 1
      action: "Initial data gathering or analysis step [Minimum 10 chars]."
      validation_rule: "Specific logic used to verify this step is correct."
    - step: 2
      action: "The primary production or transformation step."
      validation_rule: "Forensic check to ensure zero hallucinations."
    - step: 3
      action: "syncthesize the collected information into a business report"
      validation_rule: "The report is professionally formatted in Markdown"

## CONTEXT MANIFEST: The "Bill of Materials" for the Information Hunt

context_manifest:

  - key: "web_research"
    description: "Real-time data fetched from the internet using Gemini Search."
    search_query: "Current market news and competitor news for the `Agentic Value Stream`."

  - key: "primary_context"
    description: "The main source document."
    default_path: "path/to/source.md"

## PRODUCT: The expected deliverable

product:
  type: "Analysis/Document"
  format: "Markdown"
  output_path: ""
