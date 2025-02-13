from dotenv import load_dotenv
from openai_client import OpenAIClient
from gemini_client import GeminiClient
from cross_validator import CrossValidator

load_dotenv()


def main():
    """Cross-validate an answer across multiple LLMs."""
    try:
        question = input("Enter your question: ")
        clients = [OpenAIClient(), GeminiClient()]
        validator = CrossValidator(clients)

        results = validator.validate(question)

        # Display the final answer (from the last LLM)
        final_result = results[-1]
        print("\nFinal Validated Answer:")
        print(final_result.answer)

        print("\nAll responses have been saved to the outputs directory.")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
