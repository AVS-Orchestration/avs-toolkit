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
    """
    Performs live web research using Gemini Flash with Google Search grounding.
    Implements a robust fallback and forensic error reporting for v1beta troubleshooting.
    """
    raw_api_key = os.getenv("GEMINI_API_KEY")
    if not raw_api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."
    
    # Sanitize the key to prevent malformed URLs
    api_key = raw_api_key.strip()

    # Model Fallback Hierarchy based on your region's confirmed available models
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-001", "gemini-flash-latest"]
    
    last_error_detail = "No attempts made."
    
    async with httpx.AsyncClient() as client:
        for model_id in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{ "text": query }]
                }],
                "tools": [{ "google_search": {} }]
            }

            for attempt in range(3):
                try:
                    # Grounding calls require significant time for the search index retrieval
                    response = await client.post(url, json=payload, timeout=60.0)
                    
                    if response.status_code == 200:
                        result = response.json()
                        candidates = result.get('candidates', [])
                        if candidates:
                            content = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', "")
                            return content
                        last_error_detail = f"[{model_id}] 200: Success but contained no candidates."
                        break # Try the next model
                    
                    elif response.status_code == 429:
                        # Rate limit hit: Capture the error and retry this specific model
                        last_error_detail = f"[{model_id}] 429: Too Many Requests (Rate Limit)"
                        await asyncio.sleep(2 ** (attempt + 1))
                    
                    else:
                        # If we get a 404, 403, or 500, log the detail and move to the next model
                        last_error_detail = f"[{model_id}] {response.status_code}: {response.text}"
                        break # Try the next model in models_to_try
                
                except Exception as e:
                    last_error_detail = f"[{model_id}] Connection/Timeout: {str(e)}"
                    await asyncio.sleep(1) # Brief pause before retry
        
    return (
        f"Error: Web research failed after trying {', '.join(models_to_try)}. "
        f"Primary failure detail: {last_error_detail}"
    )

def get_story_data(path: Path) -> dict:
    """Parses a file and returns the raw dictionary for model validation."""
    if not path.exists():
        console.print(f"[red]Error:[/red] File not found: {path}")
        raise typer.Exit(1)
    
    content = path.read_text()
    if path.suffix == ".yaml" and "assembled_at" in content:
        return yaml.safe_load(content)
    
    return parse_markdown_story(content)

async def perform_assembly(path: Path) -> Path:
    """Core logic for assembly, shared between CLI commands."""
    raw_data = get_story_data(path)
    story = ValueStory(**raw_data)
    
    console.print(f"\n[bold blue]Assembling Briefcase for {story.metadata.story_id}...[/bold blue]")
    
    for item in story.context_manifest:
        if item.search_query:
            with Live(Spinner("dots", text=f"Researching: {item.search_query}..."), transient=True):
                item.content = await web_research(item.search_query)
                if item.content.startswith("Error:"):
                    console.print(f"  [red]✗ Research failed:[/red] {item.key or 'Web Search'}")
                    # PRINT THE FORENSIC DETAIL TO TERMINAL
                    console.print(f"    [dim]{item.content}[/dim]")
                else:
                    console.print(f"  [green]✓ Research complete:[/green] {item.key or 'Web Search'}")
        
        elif item.default_path:
            asset_path = Path(item.default_path)
            if not asset_path.exists():
                asset_path = path.parent / item.default_path

            if asset_path.exists() and asset_path.is_file():
                item.content = asset_path.read_text()
                console.print(f"  [green]✓ Injected file:[/green] {asset_path.name}")
            else:
                console.print(f"  [yellow]⚠ Warning:[/yellow] {item.default_path} not found.")

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
        panel_content.add_row("[bold]Persona:[/bold]", story.goal.as_a)
        panel_content.add_row("[bold]Context Assets:[/bold]", str(len(story.context_manifest)))
        panel_content.add_row("[bold]Web Research:[/bold]", str(sum(1 for i in story.context_manifest if i.search_query)))
        
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

@app.command()
def assemble(path: Path):
    """The Information Hunt: Injects raw context and performs web research."""
    try:
        asyncio.run(perform_assembly(path))
    except Exception as e:
        console.print(f"[red]Assembly failed: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def run(
    path: Path, 
    local: bool = typer.Option(False, "--local"), 
    model: Optional[str] = typer.Option(None, "--model")
):
    """Executes a Value Story. Auto-assembles if a briefcase doesn't exist."""
    data = get_story_data(path)
    try:
        story = ValueStory(**data)
        selected_model = model or story.metadata.preferred_model or "llama3"
        target_path = path

        if not story.is_assembled:
            target_path = asyncio.run(perform_assembly(path))
        
        if not target_path:
            console.print("[red]Error:[/red] Could not determine the path for execution.")
            raise typer.Exit(1)

        if local:
            asyncio.run(run_ollama_story(str(target_path), model=selected_model))
        else:
            console.print("[yellow]Cloud execution not implemented. Use --local.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Run aborted: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()