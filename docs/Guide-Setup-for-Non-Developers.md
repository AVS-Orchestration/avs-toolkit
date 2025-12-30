# Zero-to-Hero: Non-Developer Setup Guide

This guide is for anyone who has never written a line of code or opened a "Terminal." We will walk through exactly how to prepare a brand-new computer (Windows or Mac) to run the AVS Toolkit and the Resume Tailoring example.

## Phase 1: Meet your "Terminal"

Developers don't always use buttons; they use text commands. To do this, you need to open your computer's "Terminal."

- Mac Users: Press `Command + Space` on your keyboard, type Terminal, and press Enter.

- Windows Users: Press the `Windows Key`, type `PowerShell`, and press Enter.

>**Rule #1**: When you see a block of code below, copy it, paste it into that window, and press Enter.

## Phase 2: Install the "Package Managers"

Package managers are like "App Stores" for developers. They make installing tools safe and easy.

### For Mac Users (Homebrew)

Paste this into your Terminal and follow the prompts (it may ask for your computer password):
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

*After it finishes, follow the "Next Steps" instructions displayed in the terminal to add it to your PATH.*

### For Windows Users (Direct Installers)

You don't need a package manager yet; we will use direct installers for the tools below.

## Phase 3: Install Ollama (The "Brain")

Ollama is what allows your computer to run AI models locally without sending data to the cloud.

1. Download: Go to [Ollama.com](www.ollama.com) and download the version for your computer.
2. Install: Run the installer like any other app.
3. Download the Model: Go back to your Terminal/PowerShell and type:
```
ollama pull llama3
```

*Wait for the progress bar to finish. You now have a powerful AI model living on your hard drive.*

## Phase 4: Install VS Code (The "Workshop")

**VS Code** is the specialized text editor used to view and edit Value Stories.

1. Download: Go to [code.visualstudio.com](code.visualstudio.com).
2. Install: Run the installer.
3. Add Extensions: Open VS Code. On the left sidebar, click the icon that looks like four squares (Extensions). Search for and install these three:
	- Python (by Microsoft)
	- Pydantic (by Microsoft)
	- Markdown All in One
	- `redhat.vscode-yaml`
	- `oderwat.indent-rainbow`
	- `aaron-bond.better-comments`
	- `tomoyukim.vscode-mermaid-editor`

## Phase 5: Install uv (The "Engine")

`uv` is the tool that manages the AVS Toolkit and ensures all the technical parts work together.

**Step 1, Test first**:
To verify uv is ready, type this into your terminal or PowerShell:
```
uv --version
```
- **If it works**: You will see a response like `uv 0.5.1`. Move on to the next Phase.
- **if it fails**: If it fails: You will see an error like `command not found` (Mac) or `The term 'uv' is not recognized` (Windows). Continue with the next steps.

### Mac/Linux:

**Step 2, Paste this into your terminal**:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Step 2: Adding to PATH**:
Your computer needs to be told where uv is hidden. Paste this command into your:
```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```
### Windows:

Paste this into PowerShell:
```
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
**Adding to PATH**: The Windows installer usually handles the PATH automatically, but you must close your current PowerShell window and open a brand new one for the change to take effect. If it still isn't found, restart your computer.

## Phase 6: 
The toolkit uses Model Context Protocol (MCP) servers to perform automated research, such as scraping websites with Firecrawl. These servers require Node.js to run on your computer.

### For Mac Users:

In your Terminal, type:
```
brew install node
```

### For Windows Users:

In PowerShell, type:
```
winget install OpenJS.NodeJS
```

*Note: After installation, you can verify it by typing node -v in your terminal. You should see a version number starting with v.*



## Phase 7: Install Git & Utilities

### For Mac Users:

In your Terminal, type:
```
brew install git tree
```

### For Windows Users:

In PowerShell, type:
```
winget install Git.Git GnuWin32.Tree
```

## Phase 8: Set up Search & Scraping Keys

To unlock the full power of the "Information Hunt," you need to save your secret keys.

### 1. Get your Keys (these all have generous free tiers)

- Gemini (Free): Google AI Studio
- Tavily (Search): Tavily.com
- Firecrawl (Scraping): Firecrawl.dev

### 2. Save your Keys

#### Mac Users: Add these to your ~/.zshrc:
```
export GEMINI_API_KEY="your_key"
export TAVILY_API_KEY="your_key"
export FIRECRAWL_API_KEY="your_key"
```

Then run 
```
source ~/.zshrc.
```

#### Windows Users: Run these in PowerShell:
```
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your_key', 'User')
[System.Environment]::SetEnvironmentVariable('TAVILY_API_KEY', 'your_key', 'User')
[System.Environment]::SetEnvironmentVariable('FIRECRAWL_API_KEY', 'your_key', 'User')
```
### How it Works: Ephemeral Tools

The toolkit uses MCP (Model Context Protocol). When you run an assembly, the toolkit will briefly spin up a "Firecrawl" process using Node.js, get the data it needs, and shut it down immediately. This keeps your computer clean and your data fresh.

## Installation 

**Congratulations** 🎉 you implemented all the Prerequisits.  Return to and continue with these [Installation](../README.md#2-installation) instructions.

