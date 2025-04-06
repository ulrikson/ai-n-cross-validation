from typing import List, Dict, Any, Tuple
from models import create_validation_result
from utils import (
    save_results_to_file,
    console,
    COLORS,
    display_header,
    get_provider_color,
)
from validation_helpers import validate_answer, summarize_answer


def _display_action_status(client: Dict[str, Any], action: str) -> None:
    """Display the current action status."""
    color = get_provider_color(client["model_name"])
    action_msg = f"{action} using {client['model_name']}..."
    console.print(f"[bold {color}]{action_msg}[/]")


def _determine_action(index: int, total_count: int) -> str:
    """Determine the action based on client index."""
    if index == 0:
        return "Generating initial answer"
    elif index == total_count - 1:
        return "Summarizing discussion"
    else:
        return "Fact-checking"


def _process_client(
    client: Dict[str, Any],
    question: str,
    index: int,
    total_count: int,
    initial_answer: str,
    results: List[Dict[str, Any]],
) -> Tuple[Dict[str, Any], str]:
    """Process a single client's response."""
    action = _determine_action(index, total_count)
    _display_action_status(client, action)

    if index == 0:
        response = client["ask_question"](question, None)
        initial_answer_text = response["text"]
        return response, initial_answer_text
    elif index == total_count - 1:
        response = summarize_answer(client["ask_question"], results)
        return response, initial_answer
    else:
        response = validate_answer(client["ask_question"], question, initial_answer)
        return response, initial_answer


def _calculate_and_create_result(
    client: Dict[str, Any], question: str, response: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate costs and create validation result."""
    cost = client["calculate_costs"](response["raw_response"])

    result = create_validation_result(
        question=question,
        model_name=client["model_name"],
        answer=response["text"],
        cost=cost,
    )

    console.print(
        f"[{COLORS['success']}]✓[/] {client['model_name']} completed - Cost: ${cost/1000000:.6f}"
    )
    return result


def _handle_client_error(client: Dict[str, Any], error: Exception) -> None:
    """Handle errors during client processing."""
    console.print(
        f"[{COLORS['error']}]Error with {client['model_name']}:[/] {str(error)}"
    )
    console.print(f"[{COLORS['muted']}]Continuing to next model...[/]")


def validate_with_models(
    clients: List[Dict[str, Any]], question: str
) -> List[Dict[str, Any]]:
    """Coordinate validation across multiple LLMs."""
    display_header(question)
    results = []
    initial_answer = None

    for i, client in enumerate(clients):
        try:
            response, initial_answer = _process_client(
                client, question, i, len(clients), initial_answer, results
            )
            result = _calculate_and_create_result(client, question, response)
            results.append(result)
        except Exception as e:
            _handle_client_error(client, e)

    save_results_to_file(results)
    return results
