# Create a Value Story

This document outlines the steps to create a new Value Story within the AVS framework.

## Step 1: Define the Goal

- **Objective:** Clearly define what you want to achieve with this Value Story.
- **Outcome:** Specify the desired output or result of executing the instructions.

## Step 2: Write Instructions

- **Logic:** Provide detailed, step-by-step instructions for achieving the goal. Ensure these are precise and unambiguous.
- **Algorithmically Legible:** The instructions should be understandable by both humans and AI agents.

## Step 3: Identify Context-Manifest

- **Data Sources:** List all external files, data sources, or APIs needed to execute the task.
- **Context-Rich:** Include any necessary context that will help prevent "context blindness."

## Step 4: Assemble the YAML Prompt

- **Automation Script:** Use `assemble_prompt.py` to combine the goal, instructions, and context-manifest into a single YAML file.
- **Execution:** Provide this YAML file as input to your AI agent.

## Example

### Goal
Generate a tailored resume for a specific job application.

### Instructions
1. Parse the job description to extract required skills, keywords, and responsibilities.
2. Parse the candidate's raw resume to identify relevant experience, education, and achievements.
3. Perform a gap analysis between job requirements and candidate profile.
4. Develop a strategic plan for resume tailoring, including prioritization of content and keyword integration.

### Context-Manifest
- Job description (URL or text)
- Candidate's raw resume (PDF or text)

### YAML Output
```yaml
goal: Generate a tailored resume for a specific job application
instructions:
  - Parse the job description to extract required skills, keywords, and responsibilities.
  - Parse the candidate's raw resume to identify relevant experience, education, and achievements.
  - Perform a gap analysis between job requirements and candidate profile.
  - Develop a strategic plan for resume tailoring, including prioritization of content and keyword integration.
context-manifest:
  - job-description.md
  - raw-resume.md
```

### Execution
Provide the YAML file to your AI agent to generate the tailored resume.

## Review

- **Human Oversight:** Ensure the output meets the desired outcome and is free from errors or hallucinations.
- **Refinement:** If necessary, refine the instructions or context-manifest and repeat the process.
