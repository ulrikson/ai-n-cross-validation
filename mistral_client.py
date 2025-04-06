from typing import Any, Dict
from client_types import PromptType
from models import create_llm_response
from config import get_system_prompt, get_pricing


def ask_question_mistral(
    client: Any,
    model_name: str,
    question: str,
    prompt_type: PromptType = PromptType.DEFAULT,
) -> Dict[str, Any]:
    """Ask a question to the Mistral LLM."""
    system_prompt = get_system_prompt(
        "default" if prompt_type == PromptType.DEFAULT else "validation"
    )
    completion = client.chat.complete(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )
    return create_llm_response(
        text=completion.choices[0].message.content,
        raw_response=completion,
    )


def calculate_costs_mistral(model_name: str, response: Any) -> float:
    """Calculate the cost of a Mistral response."""
    pricing = get_pricing(model_name)
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    return (
        pricing["input_price"] * input_tokens
        + pricing["output_price"] * output_tokens
    )
