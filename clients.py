import os
from typing import Any, List, Dict, Callable
from enum import Enum, auto
from dotenv import load_dotenv
from models import create_llm_response, LLMResponseDict, ValidationResultDict
from config import get_pricing, get_prompt_template, get_system_prompt

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


# Client factory function
def create_client(provider: str, model_name: str):
    """Create a client for the specified provider."""
    clients = {
        "claude": create_claude_client,
        "openai": create_openai_client,
        "mistral": create_mistral_client,
        "gemini": create_gemini_client,
    }

    if provider not in clients:
        raise ValueError(f"Unknown provider: {provider}")

    return clients[provider](model_name)


# Claude client
def create_claude_client(model_name: str):
    """Create a Claude client."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model_name} is thinking...")
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

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model_name)
        input_cost = response.usage.input_tokens * pricing["input_price"]
        output_cost = response.usage.output_tokens * pricing["output_price"]
        return input_cost + output_cost

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model_name,
        "name": "Claude",
    }


# OpenAI client
def create_openai_client(model_name: str):
    """Create an OpenAI client."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model_name} is thinking...")
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

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model_name)
        input_cost = response.usage.prompt_tokens * pricing["input_price"]
        output_cost = response.usage.completion_tokens * pricing["output_price"]
        return input_cost + output_cost

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model_name,
        "name": "OpenAI",
    }


# Mistral client
def create_mistral_client(model_name: str):
    """Create a Mistral client."""
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model_name} is thinking...")
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

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model_name)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return (
            pricing["input_price"] * input_tokens
            + pricing["output_price"] * output_tokens
        )

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model_name,
        "name": "Mistral",
    }


# Gemini client
def create_gemini_client(model_name: str):
    """Create a Gemini client."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model_name} is thinking...")
        system_prompt = get_system_prompt(
            "default" if prompt_type == PromptType.DEFAULT else "validation"
        )
        response = client.models.generate_content(
            model=model_name,
            contents=question,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
        return create_llm_response(text=response.text, raw_response=response)

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model_name)
        input_cost = response.usage_metadata.prompt_token_count * pricing["input_price"]
        output_cost = (
            response.usage_metadata.candidates_token_count * pricing["output_price"]
        )
        return input_cost + output_cost

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model_name,
        "name": "Gemini",
    }


# Helper functions for all clients
def validate_answer(
    ask_fn: Callable, original_question: str, previous_answer: str
) -> LLMResponseDict:
    """Validate an answer using the specified ask function."""
    prompt = get_prompt_template("validation").format(
        original_question=original_question, previous_answer=previous_answer
    )
    return ask_fn(prompt, PromptType.VALIDATION)


def summarize_answer(
    ask_fn: Callable, discussion: List[ValidationResultDict]
) -> LLMResponseDict:
    """Summarize a discussion using the specified ask function."""
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
    return ask_fn(prompt, PromptType.DEFAULT)


# For testing
if __name__ == "__main__":
    load_dotenv()
    client = create_client("claude", "claude-3-5-sonnet-latest")
    response = client["ask_question"]("What is the capital of France?")
    print(response["text"])
    print(client["calculate_costs"](response["raw_response"]))
