from typing import Any, Dict
from client_types import PromptType
from models import create_llm_response
from config import get_system_prompt, get_pricing
from google.genai import types


def ask_question_gemini(
    client: Any,
    model_name: str,
    question: str,
    prompt_type: PromptType = PromptType.DEFAULT,
) -> Dict[str, Any]:
    """Ask a question to the Gemini LLM."""
    system_prompt = get_system_prompt(
        "default" if prompt_type == PromptType.DEFAULT else "validation"
    )
    response = client.models.generate_content(
        model=model_name,
        contents=question,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return create_llm_response(text=response.text, raw_response=response)


def calculate_costs_gemini(model_name: str, response: Any) -> float:
    """Calculate the cost of a Gemini response."""
    pricing = get_pricing(model_name)
    input_cost = response.usage_metadata.prompt_token_count * pricing["input_price"]
    output_cost = (
        response.usage_metadata.candidates_token_count * pricing["output_price"]
    )
    return input_cost + output_cost
