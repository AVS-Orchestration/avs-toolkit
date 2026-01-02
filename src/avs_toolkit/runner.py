import yaml
import json
from pathlib import Path
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.spinner import Spinner

from .providers.ollama import OllamaProvider
from .providers.gemini import GeminiProvider

console = Console()

async def run_story(briefcase_path: str, model: str = "llama3"):
    """
    Executes a Value Story against the configured LLM provider.
    Handles Prompt Construction, Execution, and Product Saving.
    """
    path = Path(briefcase_path)
    with open(path, 'r') as f:
        story = yaml.safe_load(f)

    # 1. Construct the System Prompt (The Agile Persona)
    system_prompt = (
        f"You are operating as: {story['goal']['as_a']}\n"
        f"Your Goal: {story['goal']['i_want']}\n"
        f"The Purpose: {story['goal']['so_that']}\n\n"
        f"Reasoning Pattern: {story['instructions'].get('reasoning_pattern', 'Standard')}\n\n"
        "Follow these execution steps precisely:\n"
    )
    
    steps = story['instructions'].get('execution_steps', [])
    for step in steps:
        system_prompt += f"- Step {step['step_number']}: {step['action']} (Validation: {step['validation_rule']})\n"

    # 2. Construct the Context Payload
    user_payload = "CONTEXT ASSETS:\n"
    for item in story['context_manifest']:
        content = item.get('content', '[Context Missing - Assemble required]')
        
        # FIX: Handle cases where default_path is None (e.g., Web Research tasks)
        raw_path = item.get('default_path')
        if raw_path:
            display_name = Path(raw_path).name
        else:
            # Fallback to key or search query snippet for the label
            display_name = item.get('key') or "Web-Research-Result"
            
        user_payload += f"--- START {display_name} ---\n{content}\n--- END ---\n"

    user_payload += "\n\nBased on the context above, produce the final product now."

    # 3. Select Provider
    metadata = story.get('metadata', {})
    provider_name = metadata.get('provider', 'ollama').lower()
    
    if provider_name == 'google-gemini':
        provider = GeminiProvider()
        # Ensure model is appropriate for Gemini if not specified
        if not model or model == "llama3":
            model = "gemini-2.5-flash" # Default fallback for cloud
    else:
        provider = OllamaProvider()

    # 4. Execute
    generated_text = ""
    with Live(Spinner("dots", text=f"Agent ({provider_name}:{model}) is thinking..."), refresh_per_second=10, transient=True):
        generated_text = await provider.generate(system_prompt, user_payload, model)

    # 5. The Filing Clerk: Save the Product
    if generated_text:
        product_cfg = story.get('product', {})
        raw_output_path = product_cfg.get('output_path', 'outputs')
        output_path = Path(raw_output_path)
        
        # If output_path looks like a file (has an extension), use it directly
        if output_path.suffix:
            save_path = output_path
            output_dir = save_path.parent
        else:
            output_dir = output_path
            filename = f"{story['metadata']['story_id']}_output.md"
            save_path = output_dir / filename
            
        output_dir.mkdir(parents=True, exist_ok=True)
        save_path.write_text(generated_text)
        
        console.print(f"\n[bold green]✓ Product Saved Successfully[/bold green]")
        console.print(f"  Location: [bold]{save_path}[/bold]")
        console.print("\n[dim]Preview of Generated Content:[/dim]")
        console.print(Markdown(generated_text[:500] + "..." if len(generated_text) > 500 else generated_text))
    else:
        console.print("[yellow]Agent returned an empty response.[/yellow]")

# Backward compatibility alias
run_ollama_story = run_story
