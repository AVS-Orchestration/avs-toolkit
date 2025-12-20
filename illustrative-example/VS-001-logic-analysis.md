# ==============================================================================
# Value Story Logic: VS-001 Analysis & Strategy
#
# This file contains the Goal and Instructions for the "Analysis & Strategy"
# Value Story (VS-001). It is designed to be ingested by the
# 'assemble_prompt.py' script, which combines it with context files
# (job description, raw resume) to generate a complete, executable
# Value Story YAML for an AI Agent.
#
# Use this file to define the *what* (Goal) and *how* (Instructions) of
# this specific Value Story.
# ==============================================================================

# THE GOAL: The "Minimum Unique Information" needed to produce the product.
# This defines the "North Star" for the Agent's internal reasoning loop.

goal:
  outcome_statement: "Identify key skills, experiences, and keywords from the job description and raw resume, and generate a strategic plan for resume tailoring."
  success_metrics:
    - "Generated strategic plan clearly outlines resume tailoring approach."
    - "Strategic plan identifies at least 5 key skills/keywords from job description."

# INSTRUCTIONS: Must be "Algorithmically Legible."
# Precise enough for AI execution, clear enough for Human audit.

instructions:
  reasoning_pattern: "Chain-of-Thought"  # Reflection, Planning, or CoT
  execution_steps:
    - step: 1
      action: "Parse provided job description to extract required skills, keywords, responsibilities, and company culture cues."
      validation_rule: "List of extracted requirements is comprehensive and accurate."
    - step: 2
      action: "Parse provided candidate's raw resume to identify relevant experience, education, achievements, and technical proficiencies."
      validation_rule: "List of candidate's relevant attributes is comprehensive and accurate."
    - step: 3
      action: "Perform a detailed gap analysis comparing extracted job requirements with candidate attributes to identify strengths, weaknesses, and tailoring opportunities."
      validation_rule: "Gap analysis report highlights crucial alignment points and discrepancies."
    - step: 4
      action: "Develop a strategic plan for tailoring the resume, including prioritization of candidate's content, specific keywords to integrate, and sections to emphasize or de-emphasize."
      validation_rule: "Strategic plan is actionable, coherent, and directly addresses the gap analysis findings."
  constraints:
    - "Do not hallucinate facts outside the provided Context."
    - "Output must be formatted as a structured strategic plan."
    - "Save the generated strategic plan to 'company_job-title_description.md' derived from job description details."

product:
  type: "Document"
  format: "Markdown"
  handoff_target: "VS-002-resume-generation"
  output_path: "illustrative-example"

# CONTEXT MANIFEST: The "Bill of Materials" for this Value Story.
# Defines what external files/data must be assembled by the script.

context_manifest:
  - key: "job_description"
    description: "The full text of the target job description."
    required: true
    default_path: "illustrative-example/job-description.md"

  - key: "raw_resume"
    description: "The candidate's original, untailored resume."
    required: true
    default_path: "illustrative-example/raw-resume.md"