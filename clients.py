import os
from typing import Any, List, Dict, Callable
from enum import Enum, auto
from dotenv import load_dotenv
from models import create_llm_response, LLMResponseDict, ValidationResultDict
from config.pricing_config import get_pricing

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


# Common prompt templates and system prompts
VALIDATION_PROMPT = (
    'I asked this question to my friend: "{original_question}" and received this answer: "{previous_answer}". '
    "Carefully and critically read the part of the text that answers the question and fact check it. "
    "Ignore the rest of the text."
    "Return the original text with your annotations and comments in markdown format."
    "Use the same language as the original text."
)

SUMMARIZE_PROMPT = (
    "You've been given a discussion between a fact checker and a research assistant. "
    'The original question was: "{original_question}". '
    'The discussion has been: "{discussion}". '
    "Distill the discussion into a single answer to the question."
    "Elaborate on any points that are not clear."
    "Use the same language as the original text."
    "Return the answer in markdown format."
)

SYSTEM_PROMPTS = {
    PromptType.VALIDATION: (
        "You are an experienced fact checker. "
        "You've worked for esteemed publications like The New Yorker and The Economist."
        "You follow their best practices for fact checking."
    ),
    PromptType.DEFAULT: "You are a research assistant.",
}


# Client factory function
def create_client(provider: str):
    """Create a client for the specified provider."""
    clients = {
        "claude": create_claude_client,
        "openai": create_openai_client,
        "mistral": create_mistral_client,
        "gemini": create_gemini_client,
    }

    if provider not in clients:
        raise ValueError(f"Unknown provider: {provider}")

    return clients[provider]()


# Helper functions for all clients
def validate_answer(
    ask_fn: Callable, original_question: str, previous_answer: str
) -> LLMResponseDict:
    """Validate an answer using the specified ask function."""
    prompt = VALIDATION_PROMPT.format(
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
    prompt = SUMMARIZE_PROMPT.format(
        original_question=question, discussion=full_discussion
    )
    return ask_fn(prompt, PromptType.DEFAULT)


# Claude client
def create_claude_client():
    """Create a Claude client."""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model = "claude-3-5-sonnet-latest"

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model} is thinking...")
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPTS[prompt_type],
            messages=[
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(text=response.content[0].text, raw_response=response)

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model)
        input_cost = response.usage.input_tokens * pricing.input_price
        output_cost = response.usage.output_tokens * pricing.output_price
        return input_cost + output_cost

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model,
        "name": "Claude",
    }


# OpenAI client
def create_openai_client():
    """Create an OpenAI client."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4o"

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model} is thinking...")
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[prompt_type]},
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(
            text=completion.choices[0].message.content, raw_response=completion
        )

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model)
        input_cost = response.usage.prompt_tokens * pricing.input_price
        output_cost = response.usage.completion_tokens * pricing.output_price
        return input_cost + output_cost

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model,
        "name": "OpenAI",
    }


# Mistral client
def create_mistral_client():
    """Create a Mistral client."""
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    model = "mistral-large-latest"

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model} is thinking...")
        completion = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPTS[prompt_type]},
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(
            text=completion.choices[0].message.content,
            raw_response=completion,
        )

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return pricing.input_price * input_tokens + pricing.output_price * output_tokens

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model,
        "name": "Mistral",
    }


# Gemini client
def create_gemini_client():
    """Create a Gemini client."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = "gemini-2.0-flash-thinking-exp"

    def ask_question(
        question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{model} is thinking...")
        response = client.models.generate_content(
            model=model,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPTS[prompt_type]
            ),
        )
        return create_llm_response(text=response.text, raw_response=response)

    def calculate_costs(response: Any) -> float:
        pricing = get_pricing(model)
        input_cost = response.usage_metadata.prompt_token_count * pricing.input_price
        output_cost = (
            response.usage_metadata.candidates_token_count * pricing.output_price
        )
        return input_cost + output_cost

    return {
        "ask_question": ask_question,
        "validate_answer": lambda q, a: validate_answer(ask_question, q, a),
        "summarize_answer": lambda d: summarize_answer(ask_question, d),
        "calculate_costs": calculate_costs,
        "MODEL": model,
        "name": "Gemini",
    }


# For testing
if __name__ == "__main__":
    load_dotenv()
    client = create_client("claude")
    response = client["ask_question"]("What is the capital of France?")
    print(response["text"])
    print(client["calculate_costs"](response["raw_response"]))
