# AVS Guide: Model Orchestration & Selection

The AVS Toolkit is designed to be **Model-Sovereign**. This means the framework does not lock you into a single LLM; instead, it allows the **Architect** (the story writer) or the **Operator** (the person running the command) to negotiate which model is best for a specific task.

## 1. The Resolution Hierarchy

When you run a Value Story, the toolkit determines which model to use based on this priority order:

1. CLI Flag (--model): The ultimate override. If you specify a model in the terminal, it wins.

2. Metadata (preferred_model): The Architect's intent. The model recommended inside the .md or .yaml file.

3. System Default: If no choice is made, the toolkit falls back to llama3.

## 2. Setting a Preferred Model (Architect Intent)

As the Architect, you can specify a model that is uniquely suited for the logic in your Value Story. For example, a "Strategy" story might require a high-parameter model like gemma2:27b, while a "Formatting" story might only need a fast, small model like phi3.

Add the `preferred_model` key to your metadata block:
```
metadata:
  story_id: "VS-001"
  version: "1.2"
  preferred_model: "gemma2:27b"  # Recommended for high-fidelity reasoning
```

## 3. The Operator Override (CLI)

Even if an Architect has suggested a model, the Operator can override it at runtime to save resources or test different outputs:
```
# Force the story to run on Mistral instead of the preferred model
uv run avs run my-story.md --local --model mistral
```

## 4. Resource Strategy: Picking the Right Model

On local hardware like a Mac Studio or MacBook Air, selecting the right model is about balancing **Reasoning Depth** vs. **Hardware Constraints**:

| Task Type | Recommended Model | Rationale |
| :--- | :--- | :--- |
| **Logic/Strategy** | `gemma2:27b` or `llama3:70b` | High reasoning capability for complex gap analysis. |
| **Drafting/Prose** | `llama3` (8b) | Fast, creative, and follows instructions well. |
| **Audit/Formatting** | `phi3` or `gemma:2b` | Extremely fast; perfect for "forensic" checks of specific data points. |

## 5. Troubleshooting: "HTTP 400 Bad Request"

If you attempt to run a story with a preferred_model that you have not yet downloaded, the toolkit will display a warning.

The Fix: You must pull the model via the terminal before the AVS Toolkit can use it:
```
ollama pull gemma2:27b
```

## 6. Why this Matters

By encoding the Model Intent into the Value Story, you eliminate "Execution Friction." You no longer have to remember which model worked best for a specific project; the Value Story carries that intelligence with it.