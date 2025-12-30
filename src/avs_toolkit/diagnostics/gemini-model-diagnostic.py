import os
import httpx
import json
from rich.console import Console
from rich.table import Table

console = Console()

def list_gemini_models():
    """
    Calls the Gemini API to list all models available to the current API Key.
    This helps troubleshoot 404 errors by verifying model names and methods.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/bold red] GEMINI_API_KEY not found in environment.")
        return

    # The listModels endpoint for v1beta
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key.strip()}"

    console.print(f"[bold blue]Querying Gemini API for available models...[/bold blue]\n")

    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=30.0)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                
                table = Table(title="Available Gemini Models")
                table.add_column("Model Name", style="cyan")
                table.add_column("Supported Methods", style="magenta")
                table.add_column("Description", style="green")

                for model in models:
                    name = model.get('name', 'N/A').replace('models/', '')
                    methods = ", ".join(model.get('supportedGenerationMethods', []))
                    description = model.get('description', '')[:50] + "..."
                    
                    table.add_row(name, methods, description)

                console.print(table)
                console.print(f"\n[bold green]Total Models Found:[/bold green] {len(models)}")
                
            else:
                console.print(f"[bold red]Error {response.status_code}:[/bold red] {response.text}")

    except Exception as e:
        console.print(f"[bold red]Failed to connect to API:[/bold red] {e}")

if __name__ == "__main__":
    list_gemini_models()