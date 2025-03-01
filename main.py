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
)
from validator import validate_with_models

load_dotenv()


def main():
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
        # Parse command-line arguments
        mode_arg, input_method_arg = parse_command_args()
        run_validation_process(mode_arg, input_method_arg)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise SystemExit(1)


def parse_command_args():
    """Parse command-line arguments for mode and input method.

    Returns:
        Tuple of (mode, input_method)
    """
    # Default values
    mode = None
    input_method = None

    # Get arguments if they exist
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    if len(sys.argv) > 2:
        input_method = sys.argv[2]

    return mode, input_method


def run_validation_process(mode_arg=None, input_method_arg=None) -> None:
    """Run the validation process with selected models."""
    # Get user's performance preference
    selector = ModelSelector()
    mode = selector.get_performance_mode(mode_arg)
    question = get_question(input_method_arg)

    start_time = time.time()  # Start time measurement

    results = validate_with_models(
        clients=selector.select_models(mode),
        question=question,
    )

    print_final_answer(results)
    print_markdown("---")
    print_total_cost(results)
    print_total_time(start_time)


def print_final_answer(results: List[ValidationResultDict]) -> None:
    """Print the final answer from the last LLM."""
    final_result = results[-1]
    print_markdown(final_result["answer"])


def print_total_cost(results: List[ValidationResultDict]) -> None:
    """Print the total cost in SEK."""
    total_cost = calculate_total_cost(results)
    sek_amount = convert_to_sek(total_cost)

    print_markdown(f"**Total cost**: {sek_amount:.3f} SEK")


def calculate_total_cost(results: List[ValidationResultDict]) -> float:
    """Calculate the total cost. Costs are per million tokens."""
    return sum(result["cost"] for result in results) / 1000000


def print_total_time(start_time: float) -> None:
    """Print the total time taken for the validation process."""
    elapsed_time = time.time() - start_time
    print_markdown(f"**Total time**: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
