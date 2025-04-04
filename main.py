from dotenv import load_dotenv
from model_selector import ModelSelector
from models import ValidationResultDict
from typing import List
import time
import sys
from utils import (
    convert_to_sek,
    print_markdown,
    get_question,
    console,
    COLORS,
    print_summary_table
)
from validator import validate_with_models
from rich.panel import Panel
from rich.text import Text

load_dotenv()


def main() -> None:
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
        # Parse command-line arguments
        mode_arg = parse_command_args()
        run_validation_process(mode_arg)
    except Exception as e:
        console.print(f"[{COLORS['error']}]Error:[/] {str(e)}")
        raise SystemExit(1)


def parse_command_args() -> str:
    """Parse command-line arguments for mode."""
    # Default value
    mode = "fast"

    # Get argument if it exists
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    return mode


def run_validation_process(mode_arg: str) -> None:
    """Run the validation process with selected models."""
    # Get user's performance preference
    selector = ModelSelector()
    mode = selector.get_performance_mode(mode_arg)
    question = get_question()

    start_time = time.time()  # Start time measurement

    # Display performance mode
    console.print(f"[{COLORS['info']}]Performance mode:[/] [bold]{mode}[/]")
    
    # Run validation
    results = validate_with_models(
        clients=selector.select_models(mode),
        question=question,
    )

    # Print final results
    print_final_answer(results)
    
    # Print summary statistics
    total_cost = calculate_total_cost(results)
    elapsed_time = time.time() - start_time
    print_summary_table(results, elapsed_time, total_cost)
    
    # Print SEK cost
    sek_amount = convert_to_sek(total_cost)
    console.print(f"[{COLORS['muted']}]Total cost in SEK: {sek_amount:.3f} SEK[/]")


def print_final_answer(results: List[ValidationResultDict]) -> None:
    """Print the final answer from the last LLM."""
    final_result = results[-1]
    
    # Display panel with final answer
    console.rule("[bold cyan]Cross-Validation Result[/]", style="cyan")
    console.print()
    
    # Print the model used for the final answer
    console.print(f"[{COLORS['info']}]Final answer from:[/] [bold]{final_result['model_name']}[/]")
    console.print()
    
    # Print the answer itself with markdown formatting
    print_markdown(final_result["answer"])


def calculate_total_cost(results: List[ValidationResultDict]) -> float:
    """Calculate the total cost. Costs are per million tokens."""
    return sum(result["cost"] for result in results) / 1000000


if __name__ == "__main__":
    main()
