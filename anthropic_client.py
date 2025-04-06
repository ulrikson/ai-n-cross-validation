from typing import Any, Dict
from client_types import PromptType
from models import create_llm_response
from config import get_system_prompt, get_pricing


def ask_question_claude(
    client: Any,
    model_name: str,
    question: str,
    prompt_type: PromptType = PromptType.DEFAULT,
) -> Dict[str, Any]:
    """Ask a question to the Claude LLM."""
    system_prompt = get_system_prompt(
        "default" if prompt_type == PromptType.DEFAULT else "validation"
    )
    response = client.messages.create(
        model=model_name,
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": question},
        ],
    )
    return create_llm_response(text=response.content[0].text, raw_response=response)


def calculate_costs_claude(model_name: str, response: Any) -> float:
    """Calculate the cost of a Claude response."""
    pricing = get_pricing(model_name)
    input_cost = response.usage.input_tokens * pricing["input_price"]
    output_cost = response.usage.output_tokens * pricing["output_price"]
    return input_cost + output_cost
