from typing import List
from models import create_validation_result, ValidationResultDict
from utils import save_results_to_file, console, COLORS, display_header, get_provider_color
from clients import BaseLLMClient


def validate_with_models(
    clients: List[BaseLLMClient], question: str
) -> List[ValidationResultDict]:
    """Validate an answer across multiple LLMs."""
    results = []
    initial_answer = None
    client_count = len(clients)
    
    # Display the question header
    display_header(question)

    for i, client in enumerate(clients):
        initial_question = i == 0
        last_question = i == client_count - 1

        try:
            # Create appropriate action message
            if initial_question:
                action = "Generating initial answer"
            elif last_question:
                action = "Summarizing discussion"
            else:
                action = "Fact-checking"
                
            # Set up simple status message with provider-specific color
            color = get_provider_color(client.model_name)
            action_msg = f"{action} using {client.model_name}..."
            console.print(f"[bold {color}]{action_msg}[/]")
            
            # Execute the model call
            if initial_question:
                response = client.ask_question(question)
                initial_answer = response["text"]
            elif last_question:
                response = client.summarize_answer(results)
            else:
                response = client.validate_answer(question, initial_answer)
            
            # Calculate costs
            cost = client.calculate_costs(response["raw_response"])
            
            # Create result
            result = create_validation_result(
                question=question,
                model_name=client.model_name,
                answer=response["text"],
                cost=cost,
            )
            results.append(result)
            
            # Print completion indicator with timing details
            console.print(f"[{COLORS['success']}]✓[/] {client.model_name} completed - Cost: ${cost/1000000:.6f}")
            
        except Exception as e:
            console.print(f"[{COLORS['error']}]Error with {client.model_name}:[/] {str(e)}")
            console.print(f"[{COLORS['muted']}]Continuing to next model...[/]")

    save_results_to_file(results)
    return results
