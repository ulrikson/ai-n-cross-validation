import os
from mistralai import Mistral
from .base_client import LLMClient, PromptType
from typing import Any, Dict
from dotenv import load_dotenv
from config.pricing_config import get_pricing
from models import create_llm_response, LLMResponseDict


class MistralClient(LLMClient):
    def __init__(self):
        super().__init__()
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.MODEL = "mistral-large-latest"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.MODEL} is thinking...")
        completion = self.client.chat.complete(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self._PROMPTS[prompt_type]},
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(
            text=completion.choices[0].message.content,
            raw_response=completion,
        )

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.MODEL)
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        return pricing.input_price * input_tokens + pricing.output_price * output_tokens


if __name__ == "__main__":
    load_dotenv()
    client = MistralClient()
    response = client.ask_question("What is the capital of France?")
    print(response["text"])
    print(client.calculate_costs(response["raw_response"]))
