# AVS Value Story

## A Framework for Multiplying Human Value in the Era of Autonomous Orchestration.

Developed by Patrick Heaney, this framework provides a rigorous methodological shift from "automating work" to multiplying value by externalizing tacit knowledge into Algorithmically Legible Instructions.

🚀 **The Problem: The Information Hunt**

The current crisis in knowledge work is characterized by the "5–15 hour information hunt"—time lost every week by workers simply trying to gather the context needed to do their actual jobs [cite: 1.1, 2.1]. This "context blindness" is the primary reason AI deployments fail, lead to hallucinations, or require excessive human oversight [cite: 2.4, 6.2].

💡 **The Solution: Agentic Value Streams (AVS)**

The Agentic Value Stream (AVS) tracks the flow of agency and decision-making rather than just static data [cite: 1.1]. It organizes the capabilities of Large Language Models (LLMs) into a linear, cumulative sequence of value creation centered around the Value Story [cite: 1.1].

### Core Definitions

**Value Story**: The atomic unit of agentic work. It is a self-contained module comprising a Goal (Outcome), Instructions (Algorithm), and Context (Data) [cite: 2.1.3].

**Algorithmically Legible Instructions**: Precise enough for an AI-Agent to execute with zero "context blindness," yet semantically clear enough for Human-Agents to oversee and audit [cite: 2.2.2].

**Context**: A mandatory component that shifts the burden of information retrieval from "runtime execution" to "design-time definition," effectively eliminating the "Information Hunt" [cite: 2.2.3].

## 🛠️ Framework Architecture

```mermaid
graph TD
    subgraph "Value-Story"
        Goal --> Automation
        Instructions --> Automation
        Context --> Automation
        Automation --.YAML --> Agentic-Agent
        Agentic-Agent --> Product
        Business-Review <--> Product
        Business-Review --> Release
    end
```

### The Strategic Shift

Under the AVS Framework, the highest-value human contributions shift from "doing the work" to generating and improving the goals, instructions, and context used by Agentic-AI-Agents to produce the product.

## 🏅 About the Author

Patrick Heaney brings over 20 years of experience in high-stakes program management and the intelligence community [cite: user_context].

Recipient of two "US Army Top 10 Inventions" awards for systems that drastically reduced friction and saved lives in combat environments [cite: user_context].

Architect of the AVS Framework, designed to solve the structural "context gap" in modern enterprise AI [cite: 1.1, 6.2].

## 📄 License & Attribution

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

### How to Cite

If you utilize this framework, templates, or logic in a professional, academic, or commercial context, please provide attribution as follows:

Heaney, P. (2025). AVS Value Story: A Framework for Autonomous Orchestration. GitHub: PatrickHeaney/avs-value-story.

## 🤝 Getting Started

Explore the Templates: Check the /templates folder for YAML schemas for creating your first Value Story.

Integrate with MCP: This repository includes implementation guides for the Model Context Protocol (MCP) to provide mandatory context to your agents [cite: 7.1].

Contribute: Fork this repo to share your own "Algorithmically Legible" instructions for common industry value streams.

## ✨ Illustrative Example: Tailored Resume Generation

To demonstrate the power of Agentic Value Streams, consider the task of generating a tailored resume for a specific job application. This complex task can be broken down into a sequence of interconnected Value Stories:

### 1. VS-001: Analysis & Strategy

**Goal:** Understand the job description and the candidate's existing resume to identify key skills, experiences, and keywords for optimal matching.
**Instructions:**
*   Parse job description to extract required skills, keywords, and responsibilities.
*   Parse candidate's raw resume to identify relevant experience, education, and achievements.
*   Perform a gap analysis between job requirements and candidate profile.
*   Develop a strategic plan for resume tailoring, including prioritization of content and keyword integration.
**Context:** Job description (URL or text), Candidate's raw resume (PDF or text).

### 2. VS-002: Resume Generation

**Goal:** Produce a draft resume tailored to the specific job application, following the strategic plan.
**Instructions:**
*   Select and prioritize relevant sections and bullet points from the candidate's raw resume based on the strategic plan.
*   Rewrite/rephrase existing bullet points to incorporate job-specific keywords and align with the job description's language.
*   Ensure resume adheres to best practices for formatting and readability.
**Context:** Output from VS-001 (strategic plan), Candidate's raw resume, Resume formatting guidelines.

### 3. VS-003: Audit (Hallucination Detection)

**Goal:** Conduct a forensic audit of the tailored resume to ensure zero fabrication of facts. Identify and report any claims that deviate from the factual ground truth of the raw resume.
**Instructions:**
*   Compare tailored resume against job description for keyword density and thematic alignment.
*   Check for clarity, conciseness, and absence of generic language.
*   Identify any remaining gaps or areas for improvement.
*   Suggest specific revisions to optimize the resume further.
**Context:** Tailored resume (draft), Original job description, Best practices for resume optimization.

### Value Stream Flow

The sequence of these Value Stories forms a clear, auditable Agentic Value Stream:

```mermaid
graph TD
    A[User Request: Job + Candidate Resume] --> B(VS-001: Analysis & Strategy)
    B --> C(VS-002: Resume Generation)
    C --> D(VS-003: Audit & Refine)
    D --> E[Final Tailored Resume]
```

### The Automation Step: Assembling the AI Prompt

In the AVS framework, "Automation" isn't the AI thinking; it is the **assembly line** that builds the perfect prompt.

To multiply human value, we don't just "ask the AI." We systematically assemble the prompt by combining:
1.  **The Goal:** The specific outcome defined by the human architect.
2.  **The Instructions:** The "Algorithmically Legible" logic for *how* to do the work.
3.  **The Context:** The specific data (e.g., `job-description.md` and `raw-resume.md`) needed to prevent hallucination.

This process generates a single, auditable package (the Value Story YAML) that serves as the **Context-Rich, Algorithmically Legible Prompt** for the Agent.

*👉 Check the `/illustrative-example` folder to see the input files and the resulting assembled YAML.*

### Updated Value Stream Flow

The full end-to-end pipeline for the tailored resume generation demonstrates the complete AVS framework:

```mermaid
graph TD
    subgraph "Human-Agent Input"
        JD[Job Description]
        CR[Candidate Raw Resume]
    end

    subgraph "VS-001: Analysis & Strategy"
        direction LR
        L1[Logic: VS-001-logic-analysis.md] --> A1[Automation: assemble_prompt.py]
        JD -- Context --> A1
        CR -- Context --> A1
        A1 --> P1(VS-001-assembled.yaml Prompt)
    end

    P1 --> AI1[AI Agent (Analyzes)]
    AI1 --> SP[Strategic Plan Output]

    subgraph "VS-002: Resume Generation"
        direction LR
        L2[Logic: VS-002-logic-generation.md] --> A2[Automation: assemble_prompt.py]
        SP -- Context --> A2
        CR -- Context --> A2
        JD -- Context --> A2
        A2 --> P2(VS-002-assembled.yaml Prompt)
    end

    P2 --> AI2[AI Agent (Generates)]
    AI2 --> TR[Tailored Resume Output]

    subgraph "VS-003: Audit"
        direction LR
        L3[Logic: VS-003-logic-audit.md] --> A3[Automation: assemble_prompt.py]
        TR -- Context --> A3
        CR -- Context --> A3
        A3 --> P3(VS-003-assembled.yaml Prompt)
    end

    P3 --> AI3[AI Agent (Audits)]
    AI3 --> AR[Audit Report Output]

    AR --> HumanReview[Human-Agent Review]
```

### The Assembly Process

The core of AVS is the "Automation" step, where human-defined logic and context are assembled into an AI-ready prompt. For this example, the `illustrative-example/assemble_prompt.py` script orchestrates this. It reads a Value Story's logic (`VS-XXX-logic-XXX.md`)—which now includes a `context_manifest`—and dynamically embeds the specified input files into a comprehensive `VS-XXX-assembled.yaml` prompt.

### Running the Example

To fully experience this end-to-end Value Stream, navigate to the project root and execute the assembly script for each Value Story. The script will generate the `VS-XXX-assembled.yaml` prompt, which you would then provide to your chosen AI Agent. The AI's output from one step often becomes the input (context) for the next.

**1. Assemble VS-001 (Analysis & Strategy)**
This step combines the job description and raw resume into a prompt for the AI to generate a strategic plan.
```bash
uv run illustrative-example/assemble_prompt.py --logic illustrative-example/VS-001-logic-analysis.md --output VS-001-assembled.yaml
# Manually 'run' VS-001-assembled.yaml as a prompt to get the Strategic Plan.
# The output (Strategic Plan) should be saved to: illustrative-example/InnovateCorp_Senior-Product-Manager-AI-Solutions_Strategic-Plan.md
```

**2. Assemble VS-002 (Resume Generation)**
This step combines the strategic plan, raw resume, and job description into a prompt for the AI to generate a tailored resume.
```bash
uv run illustrative-example/assemble_prompt.py --logic illustrative-example/VS-002-logic-generation.md --output VS-002-assembled.yaml
# Manually 'run' VS-002-assembled.yaml as a prompt to get the Tailored Resume.
# The output (Tailored Resume) should be saved to: illustrative-example/InnovateCorp_Senior-Product-Manager-AI-Solutions_Tailored-Resume.md
```

**3. Assemble VS-003 (Audit)**
This step combines the tailored resume and the raw resume into a prompt for the AI to audit for factual consistency and generate a report.
```bash
uv run illustrative-example/assemble_prompt.py --logic illustrative-example/VS-003-logic-audit.md --output VS-003-assembled.yaml
# Manually 'run' VS-003-assembled.yaml as a prompt to get the Audit Report.
# The output (Audit Report) should be saved to: illustrative-example/InnovateCorp_Senior-Product-Manager-AI-Solutions_Hallucination-Audit-Report.md
```
