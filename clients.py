import os
from typing import Any, List
from enum import Enum, auto
from dotenv import load_dotenv
from models import create_llm_response, LLMResponseDict, ValidationResultDict
from config import get_pricing, get_prompt_template, get_system_prompt
from abc import ABC, abstractmethod

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


class BaseLLMClient(ABC):
    """Base abstract class for all LLM clients."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.name = self.__class__.__name__

    @abstractmethod
    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        """Ask a question to the LLM."""
        pass

    @abstractmethod
    def calculate_costs(self, response: Any) -> float:
        """Calculate the cost of a response."""
        pass

    def validate_answer(
        self, original_question: str, initial_answer: str
    ) -> LLMResponseDict:
        """Validate an answer using the LLM."""
        prompt = get_prompt_template("validation").format(
            original_question=original_question, initial_answer=initial_answer
        )
        return self.ask_question(prompt, PromptType.VALIDATION)

    def summarize_answer(
        self, discussion: List[ValidationResultDict]
    ) -> LLMResponseDict:
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
        return self.ask_question(prompt, PromptType.DEFAULT)


class ClaudeClient(BaseLLMClient):
    """Claude client implementation."""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.name = "Claude"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.model_name} is thinking...")
        system_prompt = get_system_prompt(
            "default" if prompt_type == PromptType.DEFAULT else "validation"
        )
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(text=response.content[0].text, raw_response=response)

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.model_name)
        input_cost = response.usage.input_tokens * pricing["input_price"]
        output_cost = response.usage.output_tokens * pricing["output_price"]
        return input_cost + output_cost


class OpenAIClient(BaseLLMClient):
    """OpenAI client implementation."""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.name = "OpenAI"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.model_name} is thinking...")
        system_prompt = get_system_prompt(
            "default" if prompt_type == PromptType.DEFAULT else "validation"
        )
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(
            text=completion.choices[0].message.content, raw_response=completion
        )

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.model_name)
        input_cost = response.usage.prompt_tokens * pricing["input_price"]
        output_cost = response.usage.completion_tokens * pricing["output_price"]
        return input_cost + output_cost


class MistralClient(BaseLLMClient):
    """Mistral client implementation."""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.name = "Mistral"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.model_name} is thinking...")
        system_prompt = get_system_prompt(
            "default" if prompt_type == PromptType.DEFAULT else "validation"
        )
        completion = self.client.chat.complete(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(
            text=completion.choices[0].message.content,
            raw_response=completion,
        )

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.model_name)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return (
            pricing["input_price"] * input_tokens
            + pricing["output_price"] * output_tokens
        )


class GeminiClient(BaseLLMClient):
    """Gemini client implementation."""

    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.name = "Gemini"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.model_name} is thinking...")
        system_prompt = get_system_prompt(
            "default" if prompt_type == PromptType.DEFAULT else "validation"
        )
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=question,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
        return create_llm_response(text=response.text, raw_response=response)

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.model_name)
        input_cost = response.usage_metadata.prompt_token_count * pricing["input_price"]
        output_cost = (
            response.usage_metadata.candidates_token_count * pricing["output_price"]
        )
        return input_cost + output_cost


# Client factory function
def create_client(provider: str, model_name: str) -> BaseLLMClient:
    """Create a client for the specified provider."""
    providers = {
        "claude": ClaudeClient,
        "openai": OpenAIClient,
        "mistral": MistralClient,
        "gemini": GeminiClient,
    }

    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}")

    return providers[provider](model_name)


# For testing
if __name__ == "__main__":
    load_dotenv()
    client = create_client("claude", "claude-3-5-sonnet-latest")
    response = client.ask_question("What is the capital of France?")
    print(response["text"])
    print(client.calculate_costs(response["raw_response"]))
