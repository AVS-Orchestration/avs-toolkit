# AVS Guide: Local-First Privacy with OneDrive

This guide explains how to maintain the **AVS Toolkit** as a "Read-Only Tool" while keeping your private **Value Stories**, sensitive resumes, and business strategies in a separate, OneDrive-backed workspace. This setup ensures your private data is never tracked by Git and is automatically backed up.

## 1. The Architectural Strategy: Tool vs. Workspace

We will separate the **Orchestration Engine** (the code) from the **Context & Logic** (your data).

* **The Tool (`avs-toolkit/`)**: Cloned from the public GitHub repo. You only touch this to `git pull` updates.
* **The Workspace (`AVS-Workspace/`)**: Your private OneDrive folder. This is where you write your stories and store your outputs.

## 2. Recommended Folder Structure

Organize your OneDrive as follows:

```text
OneDrive/
└── AVS-Management/
    ├── avs-toolkit/        <-- Clone of public repo (The Engine)
    └── My-Value-Streams/   <-- Your private work (The Content)
        ├── 2026-Job-Hunt/
        ├── Internal-Strategy/
        └── custom-vs.md
```

## 3. Initial Setup

### Step A: Create Your Workspace

Create a separate folder for your private content:
```
mkdir -p ~/OneDrive/AVS-Management/My-Value-Streams
cd cd ~/OneDrive/AVS-Management
```

### Step B: Clone the Tool

Open your terminal and move to your OneDrive directory:
```
git clone https://github.com/AVS-Orchestration/avs-toolkit.git avs-toolkit
cd avs-toolkit
uv sync
```

## 4. Execution Workflow (Running Across Folders)

To run the toolkit against your private files without being inside the toolkit folder, you use the `--project` flag in `uv`. This tells `uv` where the py`project.toml` and virtual environment are located.

### Move to your Private Workspace:
```
cd ~/OneDrive/AVS-Management/My-Value-Streams
```

### Run a Validation:
```
uv run --project ../avs-toolkit avs validate my-private-story.md
```

### Run a full Local Execution:
```
uv run --project ../avs-toolkit avs run my-private-story.md --local
```

## 5. Best Practices for Privacy & Maintenance

### Update the Engine

When you want to get the latest features from the public AVS repo, simply move to the toolkit folder and pull:
```
cd ~/OneDrive/AVS-Management/avs-toolkit
git pull origin main
uv sync
```

### Use Absolute Paths for "Master" Context

If you have a master resume in a different OneDrive folder, use the full absolute path in your Value Story's `context_manifest`. The toolkit will reach out and grab it during assembly.
```
context_manifest:
  - key: "master_resume"
    default_path: "/Users/yourname/OneDrive/Documents/Master-Resume.md"
```

### Cleaning Up "Briefcases"

OneDrive version history protects your .md files. However, the *-assembled.yaml "Briefcases" can be large. Since they are easily recreated with the assemble command, you can delete them periodically to save OneDrive storage space.

## 6. Why this is the "Golden Path" for Sovereignty

**Air-Gapped Logic**: Your private folder has no `.git` directory. It is impossible to accidentally `git push` your personal data to the public internet.

**Seamless Cloud Sync**: OneDrive handles the syncing between your Mac Studio and other devices.

**Local Privacy**: Your uv `run ... --local` command keeps the actual LLM "thinking" inside your machine (Ollama), ensuring your business intelligence never leaves your control.
