from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.text import Text
from pathlib import Path
from datetime import datetime
import os
from typing import Dict, List, Optional, Any, Callable
from functools import partial

console = Console()

COLORS = {
    "primary": "cyan",
    "secondary": "green",
    "accent": "yellow",
    "info": "blue",
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "muted": "grey70",
}

PROVIDER_COLORS = {
    "claude": "purple",
    "openai": "green",
    "gemini": "blue",
    "mistral": "yellow",
}

EXCHANGE_RATES = {
    "SEK": 10.76,  # Last updated 2025-03-01
}


def convert_to_sek(amount: float) -> float:
    """Convert USD amount to SEK."""
    return amount * EXCHANGE_RATES["SEK"]


def print_markdown(markdown_text: str) -> None:
    """Print markdown content in the console using Rich."""
    console.print(Markdown(markdown_text))


def get_provider_from_model_name(model_name: str) -> str:
    """Extract provider name from model name."""
    provider = model_name.split("-")[0].lower()
    if "claude" in model_name.lower():
        return "claude"
    elif "gpt" in model_name.lower() or "o1" in model_name.lower():
        return "openai"
    elif "gemini" in model_name.lower():
        return "gemini"
    elif "mistral" in model_name.lower():
        return "mistral"
    return provider


def get_provider_color(model_name: str) -> str:
    """Get the color associated with a model's provider."""
    provider = get_provider_from_model_name(model_name)
    return PROVIDER_COLORS.get(provider, COLORS["primary"])


def display_header(question: str) -> None:
    """Display a header with the question."""
    console.print()
    console.rule("[bold cyan]AI Cross-Validation[/]", style="cyan")
    console.print(Panel(Text(question, style="white", justify="center"), 
                  title="[bold]Question[/]", 
                  border_style=Style(color="cyan")))
    console.print()


def get_question() -> str:
    """Get the question from the user via console."""
    console.print("[bold cyan]AI Cross-Validation[/]", justify="center")
    console.print()
    return console.input("[bold cyan]Enter your question: [/]").strip()


def ensure_output_directory() -> None:
    """Ensure the output directory exists."""
    os.makedirs("outputs", exist_ok=True)


def save_results_to_file(results: List[Dict[str, Any]]) -> None:
    """Save the validation results to a file."""
    ensure_output_directory()
    filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(filename, "w") as file:
        file.write(f"# Question: \n")
        file.write(f"{results[0]['question']}\n\n")
        for result in results:
            file.write(f"## Model: {result['model_name']}\n")
            file.write(f"Timestamp: {result['timestamp']}\n")
            file.write(f"### Answer:\n{result['answer']}\n\n")
            file.write(f"---\n")

    console.print(f"[{COLORS['info']}]Results saved to:[/] {os.path.abspath(filename)}")


def create_summary_table(results: List[Dict[str, Any]], total_time: float, total_cost: float) -> Table:
    """Create a summary table with model information."""
    table = Table(title="Cross-Validation Summary")
    
    table.add_column("Model", style="bold")
    table.add_column("Provider", style="dim")
    table.add_column("Cost (USD)", justify="right")
    
    for result in results:
        model_name = result["model_name"]
        provider = get_provider_from_model_name(model_name)
        cost = result["cost"] / 1000000  # Convert to dollars
        color = get_provider_color(model_name)
        
        table.add_row(
            f"[{color}]{model_name}[/]",
            provider,
            f"${cost:.6f}",
        )
    
    table.add_section()
    table.add_row(
        "[bold]Total[/]",
        "",
        f"[bold]${total_cost:.6f}[/]",
    )
    
    return table


def print_summary_table(results: List[Dict[str, Any]], total_time: float, total_cost: float) -> None:
    """Print a summary table with model information."""
    table = create_summary_table(results, total_time, total_cost)
    
    console.print()
    console.print(table)
    console.print(f"[{COLORS['muted']}]Total time: {total_time:.2f} seconds[/]")
    console.print()