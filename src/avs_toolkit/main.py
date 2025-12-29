import os
import typer
import yaml
import asyncio
import httpx
from pathlib import Path
from datetime import datetime
from typing import Optional
from pydantic import ValidationError
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

from .parser import parse_markdown_story
from .models import ValueStory
from .runner import run_ollama_story
from .mcp_client import MCPRuntime, execute_mcp_item

app = typer.Typer(help="AVS Toolkit: Orchestrate Agentic Value Streams.")
console = Console()

async def web_research_tavily(query: str) -> str:
    """Performs research using Tavily API (Optimized for Agents)."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key: return "Error: TAVILY_API_KEY not found."
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key.strip(),
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "max_results": 3
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=30.0)
            if response.status_code == 200:
                result = response.json()
                return result.get("answer") or "\n".join([r.get("content", "") for r in result.get("results", [])])
            return f"Error: Tavily returned {response.status_code}"
        except Exception as e: return f"Error: Tavily failed: {str(e)}"

async def web_research_gemini(query: str) -> str:
    """Original Gemini fallback logic with grounding."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return "Error: GEMINI_API_KEY not found."
    api_key = api_key.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": query}]}],
        "tools": [{"google_search": {}}]
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=60.0)
            if response.status_code == 200:
                result = response.json()
                candidates = result.get('candidates', [])
                if candidates:
                    return candidates[0].get('content', {}).get('parts', [{}])[0].get('text', "")
            return f"Error: Gemini failed with {response.status_code}"
        except Exception as e: return f"Error: Gemini connection failed: {str(e)}"

async def dispatch_research(query: str) -> str:
    """Prioritizes Tavily for better agentic context."""
    if os.getenv("TAVILY_API_KEY"):
        return await web_research_tavily(query)
    return await web_research_gemini(query)

def get_story_data(path: Path) -> dict:
    if not path.exists():
        console.print(f"[red]Error:[/red] File not found: {path}")
        raise typer.Exit(1)
    content = path.read_text()
    if path.suffix == ".yaml" and "assembled_at" in content:
        return yaml.safe_load(content)
    return parse_markdown_story(content)

async def perform_assembly(path: Path) -> Path:
    """The Information Hunt: Now supports Web Research and MCP Tooling."""
    raw_data = get_story_data(path)
    story = ValueStory(**raw_data)
    
    console.print(f"\n[bold blue]Assembling Briefcase for {story.metadata.story_id}...[/bold blue]")
    
    # Initialize MCP Runtime if servers are defined
    mcp_runtime = None
    if story.mcp_servers:
        mcp_runtime = MCPRuntime(story.mcp_servers)
        console.print(f"  [dim]Initializing {len(story.mcp_servers)} MCP server(s)...[/dim]")

    try:
        for item in story.context_manifest:
            # 1. Check for MCP Tool Calls
            if item.mcp_tool_name and mcp_runtime:
                with Live(Spinner("dots", text=f"Calling Tool: {item.mcp_tool_name}..."), transient=True):
                    item.content = await execute_mcp_item(mcp_runtime, item)
                    if item.content.startswith("Error:"):
                        console.print(f"  [red]✗ MCP Tool failed:[/red] {item.mcp_tool_name}")
                        console.print(f"    [dim]{item.content}[/dim]")
                    else:
                        console.print(f"  [green]✓ MCP Tool complete:[/green] {item.mcp_tool_name}")

            # 2. Check for Web Research
            elif item.search_query:
                provider = "Tavily" if os.getenv("TAVILY_API_KEY") else "Gemini"
                with Live(Spinner("dots", text=f"Researching ({provider}): {item.search_query}..."), transient=True):
                    item.content = await dispatch_research(item.search_query)
                    if item.content.startswith("Error:"):
                        console.print(f"  [red]✗ Research failed:[/red] {item.key}")
                    else:
                        console.print(f"  [green]✓ Research complete:[/green] {item.key} ({provider})")
            
            # 3. Local File Fallback
            elif item.default_path:
                asset_path = Path(item.default_path)
                if not asset_path.exists():
                    asset_path = path.parent / item.default_path

                if asset_path.exists() and asset_path.is_file():
                    item.content = asset_path.read_text()
                    console.print(f"  [green]✓ Injected file:[/green] {asset_path.name}")
                else:
                    console.print(f"  [yellow]⚠ Warning:[/yellow] {item.default_path} not found.")

    finally:
        if mcp_runtime:
            await mcp_runtime.shutdown()

    story.metadata.assembled_at = datetime.now().isoformat()
    story.metadata.status = "assembled"
    
    final_data = story.model_dump()
    output_path = path.parent / f"{story.metadata.story_id}-assembled.yaml"
    
    with open(output_path, 'w') as f:
        yaml.dump(final_data, f, sort_keys=False)
    
    console.print(f"\n[bold green]✓ Assembly Complete[/bold green]")
    console.print(f"  Briefcase: {output_path}")
    return output_path

@app.command()
def validate(path: Path):
    """Checks a Value Story against the Agile Standard Building Code."""
    try:
        data = get_story_data(path)
        story = ValueStory(**data)
        panel_content = Table.grid(padding=(0, 1))
        panel_content.add_row("[bold]Story ID:[/bold]", story.metadata.story_id)
        panel_content.add_row("[bold]MCP Servers:[/bold]", str(len(story.mcp_servers)))
        console.print(Panel(panel_content, title="Governance Pass", border_style="green"))
    except ValidationError as e:
        console.print(f"\n[bold red]❌ Governance Failure[/bold red]")
        raise typer.Exit(1)

@app.command()
def assemble(path: Path):
    """The Information Hunt: Injects raw context, Web Research, and MCP Tools."""
    try:
        asyncio.run(perform_assembly(path))
    except Exception as e:
        console.print(f"[red]Assembly failed: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def run(path: Path, local: bool = typer.Option(False, "--local"), model: Optional[str] = typer.Option(None)):
    """Executes a Value Story. Auto-assembles if necessary."""
    data = get_story_data(path)
    story = ValueStory(**data)
    selected_model = model or story.metadata.preferred_model or "llama3"
    target_path = path
    if not story.is_assembled:
        target_path = asyncio.run(perform_assembly(path))
    if local:
        asyncio.run(run_ollama_story(str(target_path), model=selected_model))

if __name__ == "__main__":
    app()