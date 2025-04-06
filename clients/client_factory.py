import os
from functools import partial
from clients.client_types import ClientFunctions

# Import LLM-specific clients
import anthropic
from openai import OpenAI
from mistralai import Mistral
from google import genai

# Import client functions
from clients.anthropic_client import ask_question_claude, calculate_costs_claude
from clients.openai_client import ask_question_openai, calculate_costs_openai
from clients.mistral_client import ask_question_mistral, calculate_costs_mistral
from clients.gemini_client import ask_question_gemini, calculate_costs_gemini


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