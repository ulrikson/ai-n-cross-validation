from dotenv import load_dotenv
from model_selector import ModelSelector
from models import ValidationResultDict
from typing import List
import time
from utils import (
    convert_currency,
    print_markdown,
    get_question,
    CURRENCY,
)
from validator import validate_with_models

load_dotenv()


def main():
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
        run_validation_process()
    except Exception as e:
        print(f"Error: {str(e)}")
        raise SystemExit(1)


def run_validation_process() -> None:
    """Run the validation process with selected models."""
    # Get user's performance preference
    selector = ModelSelector()
    mode = selector.get_performance_mode()
    question = get_question()

    start_time = time.time()  # Start time measurement

    results = validate_with_models(
        clients=selector.select_models(mode),
        question=question,
    )

    print_final_answer(results)
    print_total_cost(results, start_time)


def print_final_answer(results: List[ValidationResultDict]) -> None:
    """Print the final answer from the last LLM."""
    final_result = results[-1]
    print_markdown(final_result["answer"])


def print_total_cost(results: List[ValidationResultDict], start_time: float) -> None:
    """Print the total cost."""
    total_cost = (
        sum(result["cost"] for result in results) / 1000000
    )  # Costs are per million tokens

    sek_amount = convert_currency(total_cost, CURRENCY)
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    print_markdown("---")
    print_markdown(f"**Total cost**: {sek_amount:.3f} {CURRENCY}")
    print_markdown(f"**Time taken**: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
