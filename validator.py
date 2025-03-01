from typing import List, Dict, Any
from models import create_validation_result, ValidationResultDict
from utils import save_results_to_file


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
