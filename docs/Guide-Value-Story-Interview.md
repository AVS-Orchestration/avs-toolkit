# Value Story Inteview Guide

The purpose of this document is to guide a recorded discussion of a Value Story for the AVS Framework.  The purpose of the recorded discussion is to transform it into a transcript, then transform the transcript into a high-fidelity AVS Value Story. Answering these five categories of questions will maximize the effectiveness of generated AVS Value Story.

## 1. The Persona & The "North Star" (The Goal)

- The Persona: **"When the agent runs this, who is it pretending to be?"** (e.g., Forensic Auditor, Career Strategist, Technical Lead).

- The Specific Action: **"What exactly are we doing?"** (e.g., Identifying hallucinations, mapping skills).

- The 'So That': **"What is the ultimate value created?"** (e.g., Eliminating context-blindness, ensuring factual integrity).

- The Success Criteria: **"What are 2-3 measurable requirements?"** (e.g., 'Extract at least 5 keywords', 'Flag all date discrepancies').

## 2. The Algorithm (Execution Steps)

- The Sequence: **"Walk me through the steps 1, 2, 3. How does a human expert do this?"**

- Validation Rules: **"For each step, how do we know the agent did it correctly?"** (e.g., 'Step 1 is successful if the agent has a list of claims to verify').

- Reasoning Pattern: **"Should the agent use 'Chain-of-Thought', 'Reflection', or 'Planning' logic?"**

## 3. The Context (Bill of Materials)

- Input Sources: **"What data does the agent need to look at?"**

- The Digital Thread: **"Is any of this data the output of a previous story?"** (e.g., 'Use the intake report from VS-000').

- Keys: **"What should we call these inputs in the code?"** (e.g., raw_resume, job_description).

## 4. The Guardrails (Constraints)

- The Forbidden: **"What must the agent NOT do?"** (e.g., 'Do not invent facts', 'Do not remove the education section').

- Formatting: **"Are there specific naming conventions or locations for the output file?"**

## 5. The Deliverable (The Product)

- Format: **"Is the output a Markdown file, a JSON object, or a structured report?"**

- Handoff: **"Which story comes next in the stream?"**

## Example Prompt for the Transcript

"I want to build a value story for 'Code Review'. I'm the Senior Security Architect. I need to look at a PR diff and a set of security guidelines. First, I want to scan for hardcoded keys, then check for SQL injection patterns. I'll know it's working if I get a table of vulnerabilities. Don't mention styling issues, just security. Save it as security-audit.md."