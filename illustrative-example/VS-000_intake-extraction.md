# VS-000: Intake & Extraction
```
ARCHITECT'S GUIDE: VS-000
This is the "Entry Gate" for the Resume Tailoring Stream.
It uses Gemini + Google Search to scrape a URL and extract
the fundamental identity of the opportunity.
```
metadata:
  story_id: "VS-000"
  version: "1.2"
  author: "Patrick Heaney"
  status: "active"
  preferred_model: "llama3"

goal:
  as_a: "As a Career Intake Specialist"
  i_want: >
    Extract the hiring company name and the exact position title from a 
    specific job posting URL.
  so_that: >
    The Agentic Value Stream has a verified target for research (VS-004) 
    and strategy analysis (VS-001).

instructions:
  reasoning_pattern: "Chain-of-Thought"
  execution_steps:
    - step: 1
      action: "Review the 'raw_posting_content' fetched from the internet."
      validation_rule: "The content must contain text related to a job vacancy."
    - step: 2
      action: "Identify and extract the official Name of the Company and the Job Title."
      validation_rule: "Both fields must be extracted; use 'Unknown' if not found."
    - step: 3
      action: "Format the output as a clean header block: [Company] - [Job Title]."
      validation_rule: "The output matches the handoff format for VS-001."

context_manifest:
  - key: "raw_posting_content"
    description: "Core info from a job posting."
    search_query: >
      This website is a job posting, https://careers.oracle.com/en/sites/jobsearch/jobs/preview/316074 Read it and provide:
      1. the company name
      2. the approximate number of this company's employees
      3. the "Mission Statement" of this company.

product:
  type: "Document"
  format: "Markdown"
  output_path: "illustrative-example/"