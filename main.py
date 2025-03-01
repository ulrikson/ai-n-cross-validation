from dotenv import load_dotenv
from model_selector import ModelSelector
import time
from models import create_validation_result, ValidationResultDict
from typing import List, Dict, Any
from utils import (
    convert_currency,
    print_markdown,
    get_question,
    save_results_to_file,
    CURRENCY,
)

load_dotenv()


def validate_with_models(
    clients: List[Dict[str, Any]], question: str
) -> List[ValidationResultDict]:
    """Validate an answer across multiple LLMs."""
    results = []
    previous_answer = None
    client_count = len(clients)

    for i, client in enumerate(clients):
        initial_question = i == 0
        last_question = i == client_count - 1

        try:
            if initial_question:
                response = client["ask_question"](question)
            elif last_question:
                response = client["summarize_answer"](results)
            else:
                response = client["validate_answer"](question, previous_answer)

            cost = client["calculate_costs"](response["raw_response"])
            result = create_validation_result(
                question=question,
                model_name=client["name"],
                answer=response["text"],
                cost=cost,
            )
            results.append(result)
            previous_answer = response["text"]

        except Exception as e:
            print(f"Error with {client['name']}: {str(e)}. Continuing to next model.")

    save_results_to_file(results)
    return results


def main():
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
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

    except Exception as e:
        print(f"Error: {str(e)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
