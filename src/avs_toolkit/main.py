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

app = typer.Typer(help="AVS Toolkit: Orchestrate Agentic Value Streams.")
console = Console()

async def web_research(query: str) -> str:
    """Uses Gemini API with Google Search to fetch current context."""
    # API key is provided by environment for local dev or execution environment.
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment. Please see docs/GUIDE_GEMINI_SEARCH_SETUP.md"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{ "text": f"Provide a factual summary including: Full proper name, headquarters location, size/employee count, and whether they are private or public for: {query}" }]
        }],
        "tools": [{ "google_search": {} }]
    }

    # Exponential backoff for API calls
    for delay in [1, 2, 4, 8, 16]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                
                # Extract text
                text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "")
                # Extract grounding sources
                grounding = result.get('candidates', [{}])[0].get('groundingMetadata', {}).get('groundingAttributions', [])
                
                if text:
                    footer = "\n\nSources:\n" + "\n".join([f"- {a.get('web', {}).get('title')}: {a.get('web', {}).get('uri')}" for a in grounding if a.get('web')])
                    return text + footer
                return "No research results found."
        except Exception:
            # Retry with delay
            await asyncio.sleep(delay)
            
    return "Error: Web research failed after multiple retries."

def get_story_data(path: Path) -> dict:
    """Parses a file and returns the raw dictionary."""
    if not path.exists():
        console.print(f"[red]Error:[/red] File not found: {path}")
        raise typer.Exit(1)
    
    content = path.read_text()
    # Check if it's already a briefcase (YAML)
    if path.suffix == ".yaml" and "assembled_at" in content:
        return yaml.safe_load(content)
    
    return parse_markdown_story(content)

@app.command()
def validate(path: Path):
    """Checks a Value Story against the Agile Standard Building Code."""
    try:
        data = get_story_data(path)
        story = ValueStory(**data)
        
        panel_content = Table.grid(padding=(0, 1))
        panel_content.add_row("[bold]Story ID:[/bold]", story.metadata.story_id)
        panel_content.add_row("[bold]Persona:[/bold]", story.goal.as_a)
        panel_content.add_row("[bold]Context Assets:[/bold]", str(len(story.context_manifest)))
        panel_content.add_row("[bold]Web Research Tasks:[/bold]", str(sum(1 for i in story.context_manifest if i.search_query)))
        panel_content.add_row("[bold]Preferred Model:[/bold]", story.metadata.preferred_model or "System Default")
        
        console.print(Panel(
            panel_content,
            title=f"[bold green]Governance Pass[/bold green]",
            border_style="green"
        ))
    except ValidationError as e:
        console.print(f"\n[bold red]❌ Governance Failure in {path.name}[/bold red]")
        for error in e.errors():
            loc = " -> ".join([str(x) for x in error['loc']])
            console.print(f"  • [yellow]{loc}[/yellow]: {error['msg']}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error during validation:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def assemble(path: Path):
    """The Information Hunt: Injects local files and performs web research."""
    data = get_story_data(path)
    try:
        story = ValueStory(**data)
        console.print(f"\n[bold blue]Assembling Context for {story.metadata.story_id}...[/bold blue]")
        
        async def do_assembly():
            for item in story.context_manifest:
                # Task 1: Web Research
                if item.search_query:
                    with Live(Spinner("dots", text=f"Researching: {item.search_query}..."), transient=True):
                        item.content = await web_research(item.search_query)
                        console.print(f"  [green]✓ Web Research Complete:[/green] {item.key or item.search_query}")
                
                # Task 2: File Injection
                elif item.default_path:
                    asset_path = Path(item.default_path)
                    if not asset_path.exists():
                        asset_path = path.parent / item.default_path

                    if asset_path.exists() and asset_path.is_file():
                        item.content = asset_path.read_text()
                        console.print(f"  [green]✓ Injected File:[/green] {asset_path}")
                    else:
                        console.print(f"  [yellow]⚠ Warning:[/yellow] {item.default_path} not found.")

        asyncio.run(do_assembly())

        # Update Metadata State
        story.metadata.assembled_at = datetime.now().isoformat()
        story.metadata.status = "assembled"
        
        final_data = story.model_dump()
        output_path = path.with_name(f"{story.metadata.story_id}-assembled.yaml")
        
        with open(output_path, 'w') as f:
            yaml.dump(final_data, f, sort_keys=False)
        
        console.print(f"\n[bold green]✓ Assembly Complete[/bold green]")
        console.print(f"  Timestamp: {story.metadata.assembled_at}")
        console.print(f"  Briefcase: {output_path}")
        return output_path
    except ValidationError as e:
        console.print(f"[red]Assembly aborted: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Assembly failed:[/red] {e}")
        raise typer.Exit(1)

@app.command()
def run(
    path: Path, 
    local: bool = typer.Option(False, "--local"), 
    model: Optional[str] = typer.Option(None, "--model", help="Override the model specified in the Value Story.")
):
    """Executes a Value Story. Auto-assembles if necessary."""
    data = get_story_data(path)
    
    try:
        story = ValueStory(**data)
        selected_model = model or story.metadata.preferred_model or "llama3"
        target_path = path

        if not story.is_assembled:
            console.print(f"\n[dim]Notice: Definition file detected. Auto-assembling context for {story.metadata.story_id}...[/dim]")
            target_path = assemble(path)
        
        if local:
            asyncio.run(run_ollama_story(str(target_path), model=selected_model))
        else:
            console.print("[yellow]Cloud execution not yet implemented. Use --local for Ollama.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Run aborted:[/red] {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()