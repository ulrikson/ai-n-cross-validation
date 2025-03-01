from dotenv import load_dotenv
from model_selector import ModelSelector
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
    clients = selector.select_models(mode)
    results = validate_with_models(clients, question)
    elapsed_time = time.time() - start_time  # Calculate elapsed time

    # Display the final answer (from the last LLM)
    final_result = results[-1]
    print_markdown(final_result["answer"])

    # Calculate total costs
    total_cost = sum(result["cost"] for result in results)
    sek_amount = convert_currency(total_cost, CURRENCY)

    print_markdown("---")
    print_markdown(f"**Total cost**: {sek_amount:.3f} {CURRENCY}")
    print_markdown(f"**Time taken**: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
