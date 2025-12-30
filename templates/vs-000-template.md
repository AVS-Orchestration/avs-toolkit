# VS-000: Template for New Value Stories

```txt
# ARCHITECT'S GUIDE: How to use this template
# 1. Provide a Story ID (VS-XXX) in the title above.
# 2. Fill in the 'goal' with a statement longer than 20 characters.
# 3. List at least 2 'execution_steps' with specific 'validation_rules'.
# 4. Define your 'context_manifest' using local paths or MCP URIs.
```

## Metadata

```yaml
metadata:
  story_id: "VS-000"
  version: "1.5"
  author: "Patrick Heaney"
  preferred_model: "llama3"
```

## THE MCP MANIFEST: Defines ephemeral servers (e.g., firecrawl, filesystem)

```yaml
mcp_servers:
  - name: "firecrawl"
    command: "npx"
    args: ["-y", "firecrawl-mcp"]
```

## THE GOAL: The "North Star" for the Agentic-Agent

```yaml
goal:
  as_a: "As a <customer/role who receives the value>"
  i_want: >
    Define exactly what success looks like in at least 20 characters.
    Include specific requirements as bullet points if necessary.
  so_that: >
    The agent understands the business value and rationale behind the task.
```

## INSTRUCTIONS: The Core Algorithm (Execution Logic)

```yaml
instructions:
  reasoning_pattern: "Chain-of-Thought"
  execution_steps:
    - step: 1
      action: "Review the raw JSON asset (e.g., 'scraped_data'). Locate the 'markdown' field; this contains the target text for extraction."
      validation_rule: "The JSON is successfully parsed and the specific field is identified."
    - step: 2
      action: "Synthesize findings into a business report or summary."
      validation_rule: "The synthesis is accurate and formatted in Markdown."
    - step: 3
      action: "Create a heading '# Appendix: Source Text'. Under this, reproduce the content of the field from Step 1 VERBATIM. Do NOT summarize or omit sections. Output the text exactly as it appears in the source."
      validation_rule: "The full, un-summarized source text is included in the output."
```

## CONTEXT MANIFEST: The "Bill of Materials" for the Information Hunt

```yaml
context_manifest:
  - key: "web_research"
    description: "Real-time data fetched from the internet using Gemini Search."
    search_query: "Current market news and competitor news for the `Agentic Value Stream`."

  - key: "scraped_data"
    description: "Data retrieved via an MCP tool call."
    mcp_tool_name: "firecrawl_scrape"
    mcp_tool_args:
      url: "https://www.mphasis.com/home/thought-leadership/blog/how-can-enterprises-transform-value-streams-with-agentic-ai.html"
      formats: ["markdown"]

  - key: "primary_context"
    description: "The main source document."
    default_path: "path/to/source.md"
```

## PRODUCT: The expected deliverable

```yaml
product:
  type: "Analysis/Document"
  format: "Markdown"
  output_path: ""
```
