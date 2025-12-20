# VS Code Setup for AVS & Value Stories

To effectively manage and audit Algorithmically Legible Instructions, your development environment should prioritize structural clarity. Here are the recommended extensions for working with the AVS Framework.

## 1. YAML by Red Hat (The Foundation)

Extension ID: `redhat.vscode-yaml`
This is the industry standard. It provides the "eyes" for your editor to understand YAML syntax.

- **Why for AVS:** It provides instant validation. If you miss an indentation in a Value Story, it will flag it immediately, preventing "Context Blindness" at the execution level.

- **Key Feature:** It allows you to link your YAML files to a JSON schema (coming soon to this repo) for auto-completion of goal, instructions, and context fields.

## 2. Indent Rainbow (The Visualizer)

Extension ID: `oderwat.indent-rainbow`
YAML's logic is entirely whitespace-dependent. This extension colors the indentation levels in your file.

- **Why for AVS:** It makes nested Instructions and Context blocks instantly readable. It helps you visually verify that a sub-task is properly parented under the correct step.

## 3. Better Comments

Extension ID: `aaron-bond.better-comments`
This allows you to categorize your human-in-the-loop guidance.

- **Why for AVS:** You can use specific tags like # ! IMPORTANT for critical constraints or # ? for questions to the Human-Agent during the Business-Review phase.

## 4. Mermaid Editor

Extension ID: tomoyukim.vscode-mermaid-editor

- **Why for AVS:** Since the AVS architecture is depicted using Mermaid scripts in your ARCHITECTURE.md, this allows you to preview your Agentic Value Stream diagrams in real-time as you modify the flow of agency.

## 5. Edit-in-Context Tip

When working with Value Stories, open a split window in VS Code (Cmd + \ or Ctrl + \):

- **Left Side:** The value_story_template.yaml you are editing.

- **Right Side:** The SOURCES.md or ARCHITECTURE.md for reference.
This setup eliminates the "Information Hunt" for you while you are building the stream.