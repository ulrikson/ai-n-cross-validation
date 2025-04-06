import sys
import time
from typing import Dict, List, Any

from dotenv import load_dotenv

from clients.client_factory import create_client
from model_selector import get_model_configs, get_performance_mode
from utils import (
    convert_to_sek,
    print_markdown,
    get_question,
    console,
    COLORS,
    print_summary_table,
)
from validator import validate_with_models

load_dotenv()


def main() -> None:
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
        mode_arg = _parse_command_args()
        _run_validation_process(mode_arg)
    except Exception as e:
        console.print(f"[{COLORS['error']}]Error:[/] {str(e)}")
        raise SystemExit(1)


def _parse_command_args() -> str:
    """Parse command-line arguments for mode."""
    mode = "fast"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    return mode


def _get_clients_from_mode(mode: str) -> List[Any]:
    """Create client instances based on performance mode."""
    model_configs = get_model_configs(mode)
    clients = [
        create_client(config["provider"], config["model"])
        for config in model_configs.values()
    ]
    return clients


def _display_performance_mode(mode: str) -> None:
    """Display the current performance mode in the console."""
    console.print(f"[{COLORS['info']}]Performance mode:[/] [bold]{mode}[/]")
    console.print()


def _print_model_answer(result: Dict[str, Any]) -> None:
    """Print the model name and its answer with markdown formatting."""
    console.print(
        f"[{COLORS['info']}]Final answer from:[/] [bold]{result['model_name']}[/]"
    )
    console.print()
    print_markdown(result["answer"])


def _display_final_answer(results: List[Dict[str, Any]]) -> None:
    """Display the final answer with proper styling and formatting."""
    final_result = results[-1]
    console.rule("[bold cyan]Cross-Validation Result[/]", style="cyan")
    console.print()
    _print_model_answer(final_result)


def _calculate_total_cost(results: List[Dict[str, Any]]) -> float:
    """Calculate the total cost in USD from micropennies."""
    total = sum(result["cost"] for result in results)
    return total / 1000000


def _display_cost_in_sek(usd_cost: float) -> None:
    """Convert and display the cost in Swedish Krona."""
    sek_amount = convert_to_sek(usd_cost)
    console.print(f"[{COLORS['muted']}]Total cost in SEK: {sek_amount:.3f} SEK[/]")


def _run_validation_process(mode_arg: str) -> None:
    """Run the complete validation process with timing and results display."""
    mode = get_performance_mode(mode_arg)
    question = get_question()

    start_time = time.time()
    _display_performance_mode(mode)

    clients = _get_clients_from_mode(mode)
    results = validate_with_models(clients=clients, question=question)

    _display_final_answer(results)

    total_cost = _calculate_total_cost(results)
    elapsed_time = time.time() - start_time
    print_summary_table(results, elapsed_time, total_cost)


if __name__ == "__main__":
    main()
