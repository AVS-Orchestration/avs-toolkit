import os
import typer
import yaml
import asyncio
import httpx
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
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

async def fetch_remote_story(url: str) -> str:
    """Fetches a Value Story from a remote URL (GitHub, etc)."""
    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            with Live(Spinner("dots", text=f"Fetching remote story..."), transient=True):
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                return response.text
        except Exception as e:
            console.print(f"[red]Error fetching remote story:[/red] {e}")
            raise typer.Exit(1)

async def get_story_content(path_or_url: str) -> str:
    """Determines if the input is a local file or a URL."""
    if path_or_url.startswith(("http://", "https://")):
        return await fetch_remote_story(path_or_url)
    
    path = Path(path_or_url)
    if not path.exists():
        console.print(f"[red]Error:[/red] File not found: {path}")
        raise typer.Exit(1)
    return path.read_text()

async def research_tavily(query: str) -> Optional[str]:
    """Internal helper for Tavily research."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key: return None
    
    url = "https://api.tavily.com/search"
    payload = {"api_key": api_key.strip(), "query": query, "include_answer": True}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json=payload, timeout=30.0)
            if res.status_code == 200:
                return res.json().get("answer")
        except Exception:
            pass
    return None

async def research_gemini(query: str) -> Optional[str]:
    """Internal helper for Gemini 2.5 Flash research."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return None
    
    # Using gemini-2.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key.strip()}"
    payload = {"contents": [{"parts": [{"text": query}]}], "tools": [{"google_search": {}}]}
    
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json=payload, timeout=30.0)
            if res.status_code == 200:
                data = res.json()
                if 'candidates' in data and data['candidates']:
                    return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            pass
    return None

async def dispatch_research(query: str) -> str:
    """Resilient Research: Tries Gemini 2.5 first, then falls back to Tavily."""
    # 1. Try Gemini first
    result = await research_gemini(query)
    if result: return result
    
    # 2. Fallback to Tavily
    result = await research_tavily(query)
    if result: return result
    
    return "Error: Research failed. Both Gemini and Tavily were unavailable or rate-limited."

async def perform_assembly(path_or_url: str) -> Path:
    content = await get_story_content(path_or_url)
    is_yaml = "assembled_at" in content
    data = yaml.safe_load(content) if is_yaml else parse_markdown_story(content)
    
    try:
        story = ValueStory(**data)
    except Exception as e:
        console.print(f"[red]Governance Failure:[/red] {e}")
        raise typer.Exit(1)
    
    console.print(f"\n[bold blue]Assembling Briefcase for {story.metadata.story_id}...[/bold blue]")
    
    mcp_runtime = MCPRuntime(story.mcp_servers) if story.mcp_servers else None

    try:
        for item in story.context_manifest:
            # 1. MCP Tools
            if item.mcp_tool_name and mcp_runtime:
                item.content = await execute_mcp_item(mcp_runtime, item)
                if "Error" in (item.content or ""):
                    console.print(f"  [red]✗ MCP Tool failed:[/red] {item.mcp_tool_name}")
                else:
                    console.print(f"  [green]✓ MCP Tool complete:[/green] {item.mcp_tool_name}")
            
            # 2. Web Research
            elif item.search_query:
                item.content = await dispatch_research(item.search_query)
                if "Error" in (item.content or ""):
                    console.print(f"  [red]✗ Research failed:[/red] {item.key}")
                else:
                    console.print(f"  [green]✓ Research complete:[/green] {item.key}")
            
            # 3. Local Files
            elif item.default_path:
                p = Path(item.default_path)
                if not p.exists() and not path_or_url.startswith("http"):
                    p = Path(path_or_url).parent / item.default_path
                
                if p.exists() and p.is_file():
                    item.content = p.read_text()
                    console.print(f"  [green]✓ Injected file:[/green] {p.name}")
                else:
                    console.print(f"  [yellow]⚠ Warning:[/yellow] {item.default_path} not found.")

    finally:
        if mcp_runtime: await mcp_runtime.shutdown()

    story.metadata.assembled_at = datetime.now().isoformat()
    story.metadata.status = "assembled"
    
    output_path = Path.cwd() / f"{story.metadata.story_id}-assembled.yaml"
    output_path.write_text(yaml.dump(story.model_dump(), sort_keys=False))
    
    console.print(f"\n[bold green]✓ Assembly Complete[/bold green]")
    console.print(f"  Briefcase: {output_path}")
    return output_path

@app.command()
def validate(path_or_url: str):
    """Checks a Value Story against the Agile Standard Building Code."""
    try:
        content = asyncio.run(get_story_content(path_or_url))
        data = yaml.safe_load(content) if "assembled_at" in content else parse_markdown_story(content)
        ValueStory(**data)
        console.print("[bold green]✓ Governance Pass[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Governance Failure:[/bold red] {e}")
        raise typer.Exit(1)

@app.command()
def assemble(path_or_url: str):
    """The Information Hunt: Injects context from local, web, or remote sources."""
    try:
        asyncio.run(perform_assembly(path_or_url))
    except Exception as e:
        console.print(f"[red]Assembly failed: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def run(path_or_url: str, local: bool = typer.Option(False, "--local"), model: Optional[str] = typer.Option(None)):
    """Executes a Value Story. Supports Local files or GitHub URLs."""
    try:
        content = asyncio.run(get_story_content(path_or_url))
        is_yaml = "assembled_at" in content
        data = yaml.safe_load(content) if is_yaml else parse_markdown_story(content)
        story = ValueStory(**data)
        
        briefcase = path_or_url if story.is_assembled else asyncio.run(perform_assembly(path_or_url))
        
        if local:
            asyncio.run(run_ollama_story(str(briefcase), model=model or story.metadata.preferred_model or "llama3"))
    except Exception as e:
        console.print(f"[red]Execution failed: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()