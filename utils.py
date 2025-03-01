from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
from datetime import datetime
import os
from typing import Dict, List

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


def save_results_to_file(results: List[Dict]):
    """Save the validation results to a file."""
    ensure_output_directory()
    filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as file:
        file.write(f"Question: {results[0]['question']}\n\n")
        for result in results:
            file.write(f"Model: {result['model_name']}\n")
            file.write(f"Timestamp: {result['timestamp']}\n")
            file.write(f"Answer:\n{result['answer']}\n\n")
