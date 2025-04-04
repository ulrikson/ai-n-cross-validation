import os
from typing import Any, List, Dict, Callable, TypedDict
from enum import Enum, auto
from dotenv import load_dotenv
from models import create_llm_response
from config import get_pricing, get_prompt_template, get_system_prompt
from functools import partial

# Import client libraries
import anthropic
from openai import OpenAI
from mistralai import Mistral
from google import genai
from google.genai import types


class PromptType(Enum):
    DEFAULT = auto()
    VALIDATION = auto()
    SUMMARIZE = auto()


class ClientFunctions(TypedDict):
    ask_question: Callable
    calculate_costs: Callable
    model_name: str


def validate_answer(
    ask_question_fn: Callable,
    original_question: str,
    initial_answer: str,
) -> Dict[str, Any]:
    """Validate an answer using the LLM."""
    prompt = get_prompt_template("validation").format(
        original_question=original_question, initial_answer=initial_answer
    )
    return ask_question_fn(prompt, PromptType.VALIDATION)


def summarize_answer(
    ask_question_fn: Callable,
    discussion: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Summarize a discussion using the LLM."""
    question = discussion[0]["question"]

    full_discussion = "\n\n".join(
        [
            f"Question: {result['question']}\nAnswer: {result['answer']}"
            for result in discussion
        ]
    )
    prompt = get_prompt_template("summarize").format(
        original_question=question, discussion=full_discussion
    )
    return ask_question_fn(prompt, PromptType.DEFAULT)


# ===== Claude client functions =====

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


# ===== OpenAI client functions =====

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


# ===== Mistral client functions =====

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


# ===== Gemini client functions =====

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


# ===== Client factory function =====

def create_client(provider: str, model_name: str) -> ClientFunctions:
    """Create client functions for the specified provider."""
    # Initialize appropriate client based on provider
    if provider == "claude":
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        ask_fn = partial(ask_question_claude, client, model_name)
        cost_fn = partial(calculate_costs_claude, model_name)
    elif provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        ask_fn = partial(ask_question_openai, client, model_name)
        cost_fn = partial(calculate_costs_openai, model_name)
    elif provider == "mistral":
        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        ask_fn = partial(ask_question_mistral, client, model_name)
        cost_fn = partial(calculate_costs_mistral, model_name)
    elif provider == "gemini":
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        ask_fn = partial(ask_question_gemini, client, model_name)
        cost_fn = partial(calculate_costs_gemini, model_name)
    else:
        raise ValueError(f"Unknown provider: {provider}")
    
    # Return client function collection
    return {
        "ask_question": ask_fn,
        "calculate_costs": cost_fn,
        "model_name": model_name,
    }


# For testing
if __name__ == "__main__":
    load_dotenv()
    client = create_client("claude", "claude-3-5-sonnet-latest")
    response = client["ask_question"]("What is the capital of France?", PromptType.DEFAULT)
    print(response["text"])
    print(client["calculate_costs"](response["raw_response"]))