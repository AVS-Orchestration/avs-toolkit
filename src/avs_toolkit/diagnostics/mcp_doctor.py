import subprocess
import os
import shutil
from rich.console import Console
from rich.table import Table

console = Console()

def check_runtime(cmd: str) -> bool:
    """Checks if a command-line tool (npx, uv, etc.) is available in the PATH."""
    return shutil.which(cmd) is not None

def get_version(cmd: str, args: list = ["--version"]) -> str:
    """Attempts to get the version string for a tool."""
    try:
        # Some tools use -v or version instead of --version
        result = subprocess.run([cmd] + args, capture_output=True, text=True, check=True, timeout=5)
        return result.stdout.strip().split('\n')[0]
    except Exception:
        return "Unknown"

def run_diagnostics():
    """Performs a comprehensive check of the Hybrid AVS infrastructure."""
    console.print("\n[bold blue]AVS Toolkit: Infrastructure Diagnostic (The Doctor)[/bold blue]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("System Component", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="green")

    # 1. Check Core Runtimes (The Foundation)
    runtimes = [
        ("uv", "Required for Python/Story management"),
        ("node", "Required for MCP tools (Firecrawl)"),
        ("npx", "Required for ephemeral Node servers"),
        ("ollama", "Required for local execution")
    ]

    for cmd, desc in runtimes:
        is_ready = check_runtime(cmd)
        status = "[green]Ready[/green]" if is_ready else "[red]Missing[/red]"
        version = get_version(cmd) if is_ready else "N/A"
        table.add_row(f"{cmd.upper()}\n[dim]{desc}[/dim]", status, version)

    # 2. Check API Keys (The Fuel)
    keys = ["GEMINI_API_KEY", "TAVILY_API_KEY", "FIRECRAWL_API_KEY"]
    for key in keys:
        val = os.getenv(key)
        status = "[green]Set[/green]" if val else "[yellow]Not Set[/yellow]"
        detail = f"{key[:4]}...{key[-4:]}" if val else "Required for search/scrape"
        table.add_row(key, status, detail)

    console.print(table)

    # 3. Final Recommendations
    missing_critical = []
    if not check_runtime("node") or not check_runtime("npx"):
        missing_critical.append("Node.js/npx")
        console.print("\n[bold yellow]⚠ Advice:[/bold yellow] Node.js is missing. Install it from [bold]nodejs.org[/bold] to enable Web Scraping.")
    
    if not os.getenv("GEMINI_API_KEY"):
        console.print("[bold yellow]⚠ Advice:[/bold yellow] Gemini Key is missing. Web Research will fail.")

    if not missing_critical:
        console.print("\n[bold green]Success:[/bold green] Your workstation is AVS-ready.")
    else:
        console.print(f"\n[bold red]Action Required:[/bold red] Please resolve the missing {', '.join(missing_critical)} components.")

    console.print("\n[bold blue]Diagnostic Complete.[/bold blue]\n")