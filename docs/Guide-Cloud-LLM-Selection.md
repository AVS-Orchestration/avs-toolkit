# Guide: Cloud LLM Selection (Hybrid Agency)

The AVS Toolkit now supports **Hybrid Agency**, allowing you to route specific Value Stories to cloud-based LLMs (like Google Gemini) while keeping others local (Ollama).

This enables you to use heavy-duty reasoning models for strategic tasks (VS-001) while using fast, free local models for drafting and formatting (VS-002).

## 1. Why Use Cloud Models?

*   **Reasoning Power**: Cloud models like Gemini 1.5 Pro often outperform local 8b/70b models on complex strategic analysis.
*   **Context Window**: Larger context windows allow for analyzing massive documents that might choke a local model.
*   **Speed**: For users without high-end GPUs, cloud inference can be significantly faster.

## 2. Prerequisites

To use the Google Gemini provider, you must have a valid API Key.

1.  **Get a Key**: Visit [Google AI Studio](https://aistudio.google.com/) and create a free API key.
2.  **Configure Environment**: Add the key to your `.env` file in the workspace root:

    ```env
    GEMINI_API_KEY="your_api_key_here"
    ```

## 3. Configuring a Value Story

You do not need to change your CLI commands. You control the provider **inside the Value Story's metadata**.

Open any `.md` Value Story and update the `metadata` block:

```yaml
metadata:
  story_id: "VS-001"
  version: "2.0"
  provider: "google-gemini"       # NEW: Specifies the cloud backend
  preferred_model: "gemini-2.5-flash" # Specifies the model variant
```

**Supported Providers:**
*   `ollama` (Default)
*   `google-gemini`

**Supported Models (Gemini):**
*   `gemini-2.5-flash` (Fast, efficient)
*   `gemini-1.5-pro` (High reasoning, slower)

## 4. How to Test (User Instructions)

Follow these steps to verify that your Hybrid Agency setup is working.

### Step A: Create a Test Story

Create a file named `test-cloud.md` in your project folder with the following content:

```markdown
# VS-TEST: Cloud Connectivity Check

## Metadata
```yaml
metadata:
  story_id: "VS-TEST"
  provider: "google-gemini"
  preferred_model: "gemini-2.5-flash"
```

## Goal
```yaml
goal:
  as_a: "Cloud Connectivity Tester"
  i_want: "To verify that the AVS Toolkit can successfully route this prompt to Google Gemini."
  so_that: "I can confidently run strategic workloads in the cloud."
```

## Instructions
```yaml
instructions:
  execution_steps:
    - step: 1
      action: "Reply with the exact phrase: 'Connection Successful: Hello from Google Gemini!'"
      validation_rule: "The response matches the phrase."
```

## Context Manifest
```yaml
context_manifest: []
```
```

### Step B: Run the Test

Execute the story from your workspace root:

```bash
uv run avs run test-cloud.md
```

### Step C: Verify Output

Watch the terminal output. You should see:

1.  A spinner saying: `Agent (google-gemini:gemini-2.5-flash) is thinking...`
2.  A final success message with the content: **"Connection Successful: Hello from Google Gemini!"**

If you see this, your Hybrid Agency architecture is live.
