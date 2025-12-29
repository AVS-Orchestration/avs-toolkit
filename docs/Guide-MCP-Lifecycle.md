# MCP Lifecycle: The Ephemeral Approach

When we discuss running MCP servers via `npx` or `uvx` within the AVS Toolkit, we are talking about an **Ephemeral Stdio Transport** model.

### 1. How it Works (The "On-Demand" Loop)

Unlike a web server that stays on 24/7, an ephemeral MCP server follows this timeline:

1. **Trigger**: You run `avs assemble`.

2. **Spawn**: The Toolkit sees an MCP server in your manifest (e.g., Firecrawl). It executes a subprocess command: `npx -y @lh7/mcp-server-firecrawl`.

3. **Connection**: The Toolkit connects to that process via `stdin` and `stdout`.

4. **Action**: The Toolkit sends a request (e.g., `call_tool: scrape_url`).

5. **Result**: The server performs the scrape, sends back the Markdown text, and goes idle.

6. **Termination**: Once the assembly is finished, the Toolkit sends a shutdown signal or simply closes the process. The server vanishes from your computer's memory.

### 2. Why "Ephemeral" is Better for AVS

* **Zero Background Drain**: You don't have to remember to "turn off" your tools. They only consume CPU and RAM during the few seconds you are actually assembling a briefcase.

* **Version Freshness**: Using `npx` ensures you are pulling the latest version of the scraper or tool without having to manually manage updates in a global `node_modules` folder.

* **No Port Conflicts**: Because communication happens through standard input/output (pipes) rather than network ports (like localhost:8080), you never have to worry about one MCP server blocking another.

### 3. The "uv" Connection

Since you use **uv**, we can apply this same logic to Python-based MCP servers. Instead of `npx`, we can use `uvx` (the uv equivalent of npx) to run Python MCP tools.

**Example Manifest Entry:**

```yaml
mcp_servers:
  - name: "filesystem"
    command: "uvx"
    args: ["mcp-server-git", "--repository", "."]
```

### 4. Trade-offs
The only real trade-off is **Startup Latency**. It takes a second or two for Node or Python to "spin up" the environment. However, for a CLI tool like AVS where accuracy and context-gathering are the goals, a 2-second delay is a small price to pay for a perfectly clean, isolated execution environment.

**Architect's Note**: By treating MCP servers as ephemeral utilities, the AVS Toolkit remains lightweight. Your machine stays clean, and your "Information Hunt" remains reproducible.
