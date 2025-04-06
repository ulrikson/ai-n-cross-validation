from typing import Any, Dict
from clients.client_types import PromptType
from models import create_llm_response
from config import get_system_prompt, get_pricing


def ask_question_openai(
    client: Any,
    model_name: str,
    question: str,
    prompt_type: PromptType = PromptType.DEFAULT,
) -> Dict[str, Any]:
    """Ask a question to the OpenAI LLM."""
    system_prompt = get_system_prompt(
        "default" if prompt_type == PromptType.DEFAULT else "validation"
    )
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return create_llm_response(
        text=completion.choices[0].message.content, raw_response=completion
    )


def calculate_costs_openai(model_name: str, response: Any) -> float:
    """Calculate the cost of an OpenAI response."""
    pricing = get_pricing(model_name)
    input_cost = response.usage.prompt_tokens * pricing["input_price"]
    output_cost = response.usage.completion_tokens * pricing["output_price"]
    return input_cost + output_cost
