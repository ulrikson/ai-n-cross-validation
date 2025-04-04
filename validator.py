from typing import List, Dict, Any
from models import create_validation_result
from utils import save_results_to_file, console, COLORS, display_header, get_provider_color
from clients import validate_answer, summarize_answer


def validate_with_models(
    clients: List[Dict[str, Any]], question: str
) -> List[Dict[str, Any]]:
    """Validate an answer across multiple LLMs using functional approach."""
    results = []
    initial_answer = None
    client_count = len(clients)
    
    display_header(question)

    for i, client in enumerate(clients):
        initial_question = i == 0
        last_question = i == client_count - 1
        
        try:
            if initial_question:
                action = "Generating initial answer"
            elif last_question:
                action = "Summarizing discussion"
            else:
                action = "Fact-checking"
                
            color = get_provider_color(client["model_name"])
            action_msg = f"{action} using {client['model_name']}..."
            console.print(f"[bold {color}]{action_msg}[/]")
            
            if initial_question:
                response = client["ask_question"](question, None)
                initial_answer = response["text"]
            elif last_question:
                response = summarize_answer(client["ask_question"], results)
            else:
                response = validate_answer(client["ask_question"], question, initial_answer)
            
            cost = client["calculate_costs"](response["raw_response"])
            
            result = create_validation_result(
                question=question,
                model_name=client["model_name"],
                answer=response["text"],
                cost=cost,
            )
            results.append(result)
            
            console.print(f"[{COLORS['success']}]✓[/] {client['model_name']} completed - Cost: ${cost/1000000:.6f}")
            
        except Exception as e:
            console.print(f"[{COLORS['error']}]Error with {client['model_name']}:[/] {str(e)}")
            console.print(f"[{COLORS['muted']}]Continuing to next model...[/]")
    
    save_results_to_file(results)
    return results