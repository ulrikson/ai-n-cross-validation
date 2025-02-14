from dotenv import load_dotenv
from cross_validator import CrossValidator
from utils.markdown_printer import print_markdown
from utils.currency_converter import CurrencyConverter
from model_selector import ModelSelector
import time

load_dotenv()

CURRENCY = "SEK"


def main():
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
        # Get user's performance preference
        selector = ModelSelector()
        mode = selector.get_performance_mode()

        # Get user's question
        question = input("Enter your question: ")

        start_time = time.time()  # Start time measurement
        clients = selector.select_models(mode)
        validator = CrossValidator(clients)

        results = validator.validate(question)
        elapsed_time = time.time() - start_time  # Calculate elapsed time

        # Display the final answer (from the last LLM)
        final_result = results[-1]
        print_markdown(final_result.answer)

        # Calculate total costs
        total_cost = sum(result.cost for result in results)
        sek_amount = CurrencyConverter.convert(total_cost, CURRENCY)

        print_markdown("---")
        print_markdown(f"**Total cost**: {sek_amount:.3f} {CURRENCY}")
        print_markdown(f"**Time taken**: {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
