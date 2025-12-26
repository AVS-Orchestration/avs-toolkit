# VS-001 Analysis & Strategy
```
# ARCHITECT'S GUIDE: VS-001
# This story extracts the "Winning Strategy" by mapping candidate history
# to the specific semantic requirements of a job description.
```
metadata:
  story_id: "VS-001"
  version: "1.2"
  author: "Patrick Heaney"
  status: "active"
  preferred_model: "llama3"

# THE GOAL: The "North Star" for the Agentic-Agent.
goal:
  as_a: "As a Senior Career Strategist"
  i_want: >
    Identify key skills, experiences, and keywords from the job description and raw resume, 
    and generate a high-fidelity Strategic Alignment Matrix.
    - Requirement 1: Identify at least 5 key skills/keywords from the job description.
    - Requirement 2: Map at least 3 specific candidate achievements to these skills.
  so_that: >
    The candidate has a clear blueprint for alignment that maximizes their 
    competitiveness for the specific role and eliminates "Context Blindness."

# INSTRUCTIONS: Must be "Algorithmically Legible."
instructions:
  reasoning_pattern: "Chain-of-Thought"
  execution_steps:
    - step: 1
      action: "Parse provided job description to extract required skills, keywords, responsibilities, and company culture cues."
      validation_rule: "List of extracted requirements is comprehensive and accurate."
    - step: 2
      action: "Parse provided candidate's raw resume to identify relevant experience, education, achievements, and technical proficiencies."
      validation_rule: "List of candidate's relevant attributes is comprehensive and accurate."
    - step: 3
      action: "Perform a detailed gap analysis comparing job requirements with candidate attributes."
      validation_rule: "Gap analysis report highlights crucial alignment points and discrepancies."
    - step: 4
      action: "Develop a strategic plan for tailoring the resume, including prioritization of content and specific keywords."
      validation_rule: "Strategic plan is actionable and directly addresses the gap analysis findings."
  constraints:
    - "You MUST NOT invent, embellish, or infer any new facts outside of the sources."
    - "Output must be formatted as a structured strategic plan."

# CONTEXT MANIFEST: The "Bill of Materials" for this Value Story.
context_manifest:
  - key: "job_description"
    description: "The full text of the target job description."
    default_path: "illustrative-example/job-description.md"
  - key: "raw_resume"
    description: "The candidate's original, untailored resume."
    default_path: "illustrative-example/raw-resume.md"

# PRODUCT: The expected deliverable.
product:
  type: "Document"
  format: "Markdown"
  output_path: "illustrative-example/"
  handoff_target: "VS-002-resume-generation"