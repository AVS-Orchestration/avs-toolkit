# AVS Toolkit: Private Starter Guide

If you want to use the AVS Toolkit as a foundation for your own private **Value Stories** (VS) without pushing your content back to the public repository, follow these steps to "Sever & Restart."

## 1. Clone into a Custom Folder

Instead of a standard clone, specify your own project name for the folder.
```
git clone https://github.com/PatrickHeaney/avs-value-story.git my-private-value-stream
cd my-private-value-stream
```

## 2. Sever the Link to the Original Repo

To ensure you don't accidentally push your private resumes, strategy documents, or business logic back to the public AVS repo, delete the existing `.git` history.
```
# Removes all git history and remote links
rm -rf .git
```
## 3. Initialize Your Private Repository

Now, start a fresh history that belongs only to you.
```
git init
git add .
git commit -m "Initial commit: AVS Toolkit v1.2 Standard"
```

## 4. Setup the Environment with `uv`

Sync the environment to ensure the `avs` CLI is available on your machine.

```
uv sync
```

## 5. Privacy Guardrail: Check `.gitignore`

The toolkit is designed to be "Context-Aware" but "Data-Private." Ensure your `.gitignore` includes the following to prevent sensitive data from being committed:

```
# .gitignore
*-assembled.yaml
outputs/
.venv/
__pycache__/
```

## 6. Create Your First VS Template

You can now use the provided template as a starting point for your own logic:

```
cp vs-000-template.md my-first-story.md
# Edit my-first-story.md with your private goal and context paths
```

## 7. Run and Verify

Test your local setup with Ollama;
```
uv run avs validate my-first-story.md
uv run avs run my-first-story.md --local
```

**Note:** By following this process, your `origin` remote is empty. You can now link this to your own private GitHub/GitLab repository:
`git remote add origin https://github.com/your-username/your-private-repo.git`