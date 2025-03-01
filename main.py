from dotenv import load_dotenv
from model_selector import ModelSelector
import time
import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from models import create_validation_result, ValidationResultDict
from typing import List, Dict, Any

load_dotenv()

# Currency conversion
CURRENCY = "SEK"
EXCHANGE_RATES = {
    "USD": 1.0,
    "SEK": 10.83,  # Last updated 2025-02-13
}


def convert_currency(amount: float, target_currency: str) -> float:
    """Convert USD amount to target currency."""
    target_currency = target_currency.upper()
    if target_currency not in EXCHANGE_RATES:
        raise ValueError(f"Unsupported currency: {target_currency}")
    return amount * EXCHANGE_RATES[target_currency]


def print_markdown(markdown_text: str) -> None:
    """Print markdown content in the console using Rich."""
    console = Console()
    console.print(Markdown(markdown_text))


def get_question():
    """Get the question from the user via console or file."""
    method = input("Input method: [w]rite or [f]ile [w]: ").lower() or "w"

    if method == "w":
        return input("Enter your question: ").strip()
    elif method == "f":
        while True:
            filename = input("Enter the path to your question file: ").strip()
            file_path = Path(filename)

            if not file_path.exists():
                print(f"File {filename} does not exist. Please try again.")
                continue

            try:
                with open(file_path, "r") as file:
                    question = file.read().strip()
                    if not question:
                        print("File is empty. Please provide a file with content.")
                        continue
                    return question
            except Exception as e:
                print(f"Error reading file: {str(e)}")
    else:
        print("Invalid choice. Please enter 'w' for Write or 'f' for File.")
        return get_question()


def ensure_output_directory():
    """Ensure the output directory exists."""
    os.makedirs("outputs", exist_ok=True)


def save_results_to_file(results: List[ValidationResultDict]):
    """Save the validation results to a file."""
    ensure_output_directory()
    filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as file:
        file.write(f"Question: {results[0]['question']}\n\n")
        for result in results:
            file.write(f"Model: {result['model_name']}\n")
            file.write(f"Timestamp: {result['timestamp']}\n")
            file.write(f"Answer:\n{result['answer']}\n\n")


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
