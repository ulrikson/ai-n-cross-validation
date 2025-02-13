from dotenv import load_dotenv
from openai_client import OpenAIClient
from gemini_client import GeminiClient
from claude_client import ClaudeClient
from cross_validator import CrossValidator
from markdown_printer import print_markdown

load_dotenv()


def main():
    """Cross-validate an answer across multiple LLMs and print markdown output."""
    try:
        question = input("Enter your question: ")
        clients = [ClaudeClient(), OpenAIClient(), GeminiClient()]
        validator = CrossValidator(clients)

        results = validator.validate(question)

        # Display the final answer (from the last LLM)
        final_result = results[-1]
        print_markdown(final_result.answer)

        # Calculate and display total costs
        total_cost = sum(result.cost for result in results)
        print(f"\nTotal cost for all AI models: ${total_cost:.4f}")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
