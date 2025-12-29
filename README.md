# AVS Value Story

## A Framework for Making AI your personal Force Multiplier.

Developed by **Patrick Heaney**, this framework provides a rigorous methodological shift from "automating work" to **multiplying value** by externalizing tacit knowledge into **Algorithmically Legible Instructions**.

## 🚀 **The Problem: The Information Hunt**

The current crisis in knowledge work is characterized by the **"5–15 hour information hunt"**—time lost every week by workers simply trying to gather the context needed to do their actual jobs [cite: 1.1, 2.1]. This **"context blindness"** is the primary reason AI requires excessive human oversight [cite: 2.4, 6.2] and fails to produce acceptable results.

# 💡 **The Solution: Agentic Value Streams (AVS)**

The Agentic Value Stream (AVS) tracks the flow of agency and decision-making rather than just static data [cite: 1.1]. It organizes the capabilities of Large Language Models (LLMs) into a **cascading, iterative, and cumulative sequence** of value creation centered around the Value Story [cite: 1.1].

**Web Research Integration:** AVS now integrates **Live Web Research** via Gemini 2.5 Flash with Google Search grounding to automate the retrieval of public information and market data.

```mermaid
graph LR
    subgraph Process [The AVS Pattern]
        direction TB
        VS-000(Intake & Research)
        VS-001(Analysis & Strategy)
        VS-002(Product Generation)
        VS-003(Review & Refine)

        
        %% Vertical flow connections
        VS-000 ==> VS-001 ==> VS-002 ==> VS-003 
    end

    Context[(MCP,<br>Database,<br>File System,<br>URL, etc)]
    AI-CLoud[(Gemini 2.5 Flash<br>Web Search API)]

    %% Connections to the right
    VS-000 <-.-> AI-CLoud
    VS-001 <-.-> Context
    VS-002 <-.-> Context
    VS-003 <-.-> Context
    VS-003 ==> Context
```

## Core Definitions

**Value Story**: The atomic unit of agentic work. It is a self-contained module comprising a **Goal** (Outcome), **Instructions** (Algorithm), and **Context-Manifest** (Data) [cite: 2.1.3].

Every Value Story in this repository follows the **Agile v1.2 Standard**, ensuring that every unit of work is aligned with a specific persona and business outcome:

* **As a [Persona]**: Defines the perspective and voice of the agent.

* **I want [Action]**: Defines the specific technical deliverable and success metrics.

* **So that [Value]**: Provides the "Why," allowing the agent to resolve ambiguities through the lens of intended value.

**Algorithmically Legible Instructions**: Precise enough for an AI-Agent to execute with zero "context blindness," yet semantically clear enough for Human-Agents to oversee and audit [cite: 2.2.2].

**Context-Manifest**: A mandatory component that shifts the burden of information retrieval from "runtime execution" to "design-time definition." It supports local files and **Live Web Research** via the `search_query` field [cite: 2.2.3].


## 🧠 The Strategic Shift

Under the **AVS Framework**, the highest-value human contributions complete the shift higher level thinking. Users shift from "doing the work" to strategicly generating and improving the goals, instructions, and context, used by Agentic-AI-Agents to produce the product. This moves the human architect from the role of a "task-manager" to a **"Orchestrator of Agency"** and moves the Agentic AI Agent from a "task-doer" to a **"force multiplier."**

# 🛠️ The Value Story Lifecyle
This diagram illustrates the **Value Story** lifecycle: **Plan** (Human), **Run** (Agent), and **Review** (Human).

```mermaid
graph TD
    subgraph VS [" "]
        subgraph plan ["<span style='font-size:20px'>**1-Plan**</span>"]
            Start([Human-Agent]) ==> Goal
            Goal --> Instructions --> Context-Manifest
            Start ==> Instructions
            Start ==> Context-Manifest
        end
        subgraph run  ["<span style='font-size:20px'>**2-Run**</span>"]
            Goal ==> Automation
            Instructions ==> Automation
            Context-Manifest ==> Automation
            Automation == **.YAML** ==> AI-Agent
        end
        subgraph review ["<span style='font-size:20px'>**3-Review**</span>"]
            AI-Agent ==> Product
            Business-Review{Human<br>Review}
            Product ==> Business-Review
            Business-Review -- **Refine** --> Goal
            
        end
        Business-Review == **Release** ==> Context[(GitHub, MCP,<br>Local Files)]
        Context <==> Automation
    end
    
    %% Syles
    classDef Plan fill:#ffb6c1,stroke:#333,stroke-width:2px;
    classDef Run fill:#90ee90,stroke:#333,stroke-width:2px;
    classDef Review fill:#add8e6,stroke:#333,stroke-width:2px;
    
    %% Assignments
    class plan Plan;
    class run Run;
    class review Review;
```
## Illustrative Example

Before diving into the technical setup, you can explore a complete Illustrative Example focused on tailoring a resume. This walkthrough demonstrates how a sequence of Value Stories generates a high-fidelity "Strategic Alignment Matrix," mapping a candidate's background to specific job requirements to ensure the agent produces a competitive, fact-based product without context blindness.

# Getting Started

## 1. Prerequisites

### For Non-Developers
Follow the detailed instructions in the [Guide-Setup-for-Non-Developers](./docs/Guide-Setup-for-Non-Developers.md)
Ensure you have `homebrew` installed on your system:
### For Developers
Verify installation on macOS and Windows (assuming Git Bash or similar shell on Windows)
```
if command -v uv &> /dev/null; then
    echo "uv is installed. Version information:"
    uv --version
else
    echo "uv is not installed or not found in the system's PATH."
fi
```
If `uv` is not installed, I included instructions in Phase 5 of the [Setup for Non-Developers](./docs/Guide-Setup-for-Non-Developers.md) guide.

* **Ollama**: Install [Ollama](https://ollama.com) and run `ollama pull llama3`.
* **Gemini API Key**: Required for live web research. Set it in your environment: `export GEMINI_API_KEY="your_key"`.

## 2. Installation

Clone the repository and sync the environment:
```
git clone https://github.com/PatrickHeaney/avs-value-story.git
cd avs-value-story
uv sync
```
## 3. Your First Governance Pass

Validate the provided template to ensure your environment is configured correctly:
```
uv run avs validate vs-000-template.yaml
```
## 🛠 The Toolkit CLI

The `avs` toolkit provides a suite of commands to move from architectural intent to execution.

### `validate`

Checks a Value Story against the "Building Code" (Pydantic models). It ensures your goal is properly framed and your instructions meet the minimum precision requirements.
```
uv run avs validate illustrative-example/VS-001-logic-analysis.md
```

### `assemble`

The "Information Hunt" automation. It reads your `context_manifest`, **performs live web research via Gemini 2.5 Flash** (if `search_query` is present), and packages everything into a **Briefcase** (`*-assembled.yaml`) stamped with a unique `assembled_at` timestamp.

```
uv run avs assemble illustrative-example/VS-001-logic-analysis.md
```

### `run`

Executes the Value Story. If the file has not been assembled yet, `run` will automatically perform the assembly step before dispatching the payload to your local LLM (defaulting to Ollama/Llama3).
```
uv run avs run illustrative-example/VS-001-logic-analysis.md --local
```

🧠 **Advanced**: See [Model Orchestration Guide](docs/GUIDE_MODEL_ORCHESTRATION.md) for using specialized models like Gemma or Mistral.

## 📂 Architecture: Value Story vs. Briefcase

The AVS Toolkit manages the lifecycle of a Value Story through three distinct file types visible in the repository:

1.  **The Value Story (`VS-XXX.md`)**: The human-editable source of truth. It contains the Goal, Instructions, and pointers to context. This is what you commit to Git.
2.  **The Assembled VS (`VS-XXX-assembled.yaml`)**: An execution-ready snapshot. Created by `avs assemble`, it contains the logic plus the **full injected text** of all context assets.
3.  **The Output Product (`VS-XXX_output.md`)**: The final deliverable generated by the Agent. This is saved to the `output_path` defined in your Blueprint (e.g., `outputs/` or `illustrative-example/`).

> **Tip:** We recommend adding `*-assembled.yaml` to your `.gitignore` to prevent repository bloat and accidental exposure of sensitive context data.

## 🏗 Repository Structure

* `src/avs_toolkit/`: The core orchestration engine.
  * `models.py`: Pydantic data schemas for Value Stories.
  * `parser.py`: Hybrid YAML/Markdown logic engine.
  * `runner.py`: Local execution logic for Ollama/Llama3.
  * `main.py`: CLI command definitions.
* `illustrative-example/`: A complete Resume Tailoring stream.

* `VS-000-template.md`: Master markdown template for new Value Stories.
* `Visual-Studio-Code-Setup-Guide.md`: Dev environment optimization.
* `docs/`: A library of implementation guides including [Gemini Search Setup](./docs/GUIDE_GEMINI_SEARCH_SETUP.md).
* `ARCHITECTURE.md` & `SOURCES.md`: Framework documentation.

## 🏅 About the Author

Patrick Heaney brings over 20 years of experience in high-stakes program management and the intelligence community [cite: user_context].

Recipient of two "US Army Top 10 Inventions" awards for systems that drastically reduced friction and saved lives in combat environments [cite: user_context].

Architect of the AVS Framework, designed to solve the structural "context gap" in modern enterprise AI [cite: 1.1, 6.2].

## 📄 License & Attribution

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

### How to Cite

If you utilize this framework, templates, or logic in a professional, academic, or commercial context, please provide attribution as follows:

Heaney, P. (2025). AVS Value Story: A Framework for Autonomous Orchestration. GitHub: PatrickHeaney/avs-value-story.

