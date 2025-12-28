metadata:
  story_id: "VS-004"
  version: "1.2"
  author: "Patrick Heaney"
  status: "active"

goal:
  as_a: "As a Corporate Intelligence Analyst"
  i_want: >
    Research specific details about a target employer and generate a
    Company Profile Matrix.
  so_that: >
    Tailoring agents have factual grounding for company size, culture,
    and headquarters location.

instructions:
  reasoning_pattern: "Chain-of-Thought"
  execution_steps:
    - step: 1
      action: "Review the 'target_company_data' fetched from the internet."
      validation_rule: "The company's proper name and HQ are identified."
    - step: 2
      action: "Determine if the company is public or private and its approximate size."
      validation_rule: "Size and status are explicitly stated."
    - step: 3
      action: "Identify the primary industry and core business focus."
      validation_rule: "Industry and focus are accurately mapped."

context_manifest:
  - key: "target_company_data"
    description: "Real-time research on the target employer."
    search_query: "NVIDIA Corporation headquarters, size, private or public status, and core business"

product:
  type: "Document"
  format: "Markdown"
  output_path: "illustrative-example/"