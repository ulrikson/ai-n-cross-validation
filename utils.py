from rich.console import Console
from rich.markdown import Markdown
from pathlib import Path
from datetime import datetime
import os
from typing import Dict, List, Optional

# Currency conversion
EXCHANGE_RATES = {
    "SEK": 10.76,  # Last updated 2025-03-01
}


def convert_to_sek(amount: float) -> float:
    """Convert USD amount to SEK."""
    return amount * EXCHANGE_RATES["SEK"]


def print_markdown(markdown_text: str) -> None:
    """Print markdown content in the console using Rich."""
    console = Console()
    console.print(Markdown(markdown_text))


def get_question(input_method: Optional[str] = None) -> str:
    """Get the question from the user via console or file.

    Args:
        input_method: 'write' or 'file', defaults to 'write' if None
    """
    method = input_method.lower() if input_method else "write"

    if method not in ["write", "w", "file", "f"]:
        print(f"Invalid input method '{input_method}'. Using 'write' method.")
        method = "write"

    if method in ["write", "w"]:
        return input("Enter your question: ").strip()
    elif method in ["file", "f"]:
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

    # This should not be reached, but just in case
    return get_question("write")


def ensure_output_directory():
    """Ensure the output directory exists."""
    os.makedirs("outputs", exist_ok=True)


def save_results_to_file(results: List[Dict]):
    """Save the validation results to a file."""
    ensure_output_directory()
    filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

    with open(filename, "w") as file:
        file.write(f"# Question: {results[0]['question']}\n\n")
        for result in results:
            file.write(f"## Model: {result['model_name']}\n")
            file.write(f"Timestamp: {result['timestamp']}\n")
            file.write(f"### Answer:\n{result['answer']}\n\n")
            file.write(f"---\n")
