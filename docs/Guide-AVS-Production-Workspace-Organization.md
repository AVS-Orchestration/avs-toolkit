# AVS Production Workspace Organization

This structure separates the Engine and Library from your Private Projects. By using a project-specific folder, you can keep your data organized and easily back up or move individual projects.

> 💡 Best Practice: We strongly recommend hosting this entire AVS-Orchestration-Workspace/ folder within your OneDrive (e.g., ~/Library/CloudStorage/OneDrive-Personal/). This ensures your private data is persistent across devices and remains under your sovereign control.

## The Recommended Root Structure

Place your project folders at the root of AVS-Orchestration-Workspace/:

```text
AVS-Orchestration-Workspace/    <-- Workspace root
├── .env                        <-- Global API Keys
├── avs-toolkit/                <-- THE ENGINE (Git Repo)
├── avs-standard-library/       <-- THE BLUEPRINTS (Git Repo)
│
└── my-job-hunt/                <-- YOUR PROJECT FOLDER (Create This)
    ├── inputs/                 
    │   └── raw-resume.md       <-- Your master data
    └── outputs/                
        └── oracle-tpm-role/    <-- Results generated here
```

## Steps to Configure Your Workspace

1. **Create your Project Folder**: Create `my-job-hunt/` (or any name you prefer) in the workspace root.

2. **Organize Inputs**: Create your `inputs/` folder (with your resume) inside `my-job-hunt/`.

3. **Position your .env**: Move your `.env` file at the absolute root of AVS-Orchestration-Workspace/. The avs command is smart enough to find it when you run commands from the project folder.

## How to Run from this Layout

To keep your outputs contained within the correct project, you should always **"stand" in your project folder** when running commands:

```text
# 1. Move into your project folder
cd ~/Library/CloudStorage/OneDrive-Personal/AVS-Orchestration-Workspace/my-job-hunt

# 2. Run the story from the library (referencing the path back out)
avs run ../avs-standard-library/value-stories/job-hunting/vs-000-logic-intake.md --local
```

Why this is important:

**Project Isolation**: If you start a "Second Job Hunt" or a different project, you just create a new folder. They won't share inputs/ or outputs/, preventing data mixing.

**Relative Pathing**: Since you are inside my-job-hunt/, the value story's instruction to save to outputs/ will correctly resolve to my-job-hunt/outputs/.

**Clean Sidebar**: In VS Code, your active work is clearly separated from the tool's source code.
