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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Internal Imports
from .parser import parse_markdown_story
from .models import ValueStory
from .runner import run_story
from .mcp_client import MCPRuntime, execute_mcp_item
from .diagnostics.mcp_doctor import run_diagnostics

app = typer.Typer(help="AVS Toolkit: Orchestrate Agentic Value Streams.")
console = Console()

# ... (omitted fetching/research functions for brevity, they remain unchanged)

@app.command()
def run(path_or_url: str, local: bool = typer.Option(True, "--local"), model: Optional[str] = typer.Option(None)):
    """
    Executes a Value Story. Supports Local files or GitHub URLs.
    Now supports hybrid execution (Ollama or Cloud LLMs) via story configuration.
    """
    try:
        content = asyncio.run(get_story_content(path_or_url))
        is_yaml = "assembled_at" in content
        data = yaml.safe_load(content) if is_yaml else parse_markdown_story(content)
        story = ValueStory(**data)
        
        briefcase = path_or_url if story.is_assembled else asyncio.run(perform_assembly(path_or_url))
        
        if local:
            asyncio.run(run_story(str(briefcase), model=model or story.metadata.preferred_model or "llama3"))
    except Exception as e:
        console.print(f"[red]Execution failed: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()