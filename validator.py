from typing import List
from models import create_validation_result, ValidationResultDict
from utils import save_results_to_file
from clients import BaseLLMClient


def validate_with_models(
    clients: List[BaseLLMClient], question: str
) -> List[ValidationResultDict]:
    """Validate an answer across multiple LLMs."""
    results = []
    initial_answer = None
    client_count = len(clients)

    for i, client in enumerate(clients):
        initial_question = i == 0
        last_question = i == client_count - 1

        try:
            if initial_question:
                print(f"Asking {client.model_name}...")
                response = client.ask_question(question)
                initial_answer = response["text"]
            elif last_question:
                print(f"Summarizing with {client.model_name}...")
                response = client.summarize_answer(results)
            else:
                print(f"Fact-checking with {client.model_name}...")
                response = client.validate_answer(question, initial_answer)

            cost = client.calculate_costs(response["raw_response"])
            result = create_validation_result(
                question=question,
                model_name=client.model_name,
                answer=response["text"],
                cost=cost,
            )
            results.append(result)

        except Exception as e:
            print(f"Error with {client.model_name}: {str(e)}. Continuing to next model.")

    save_results_to_file(results)
    return results
