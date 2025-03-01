import os
from openai import OpenAI
from .base_client import LLMClient, PromptType
from typing import Any
from dotenv import load_dotenv
from config.pricing_config import get_pricing
from models import create_llm_response, LLMResponseDict


class OpenAIClient(LLMClient):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.MODEL = "gpt-4o"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.MODEL} is thinking...")
        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self._PROMPTS[prompt_type]},
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(
            text=completion.choices[0].message.content, raw_response=completion
        )

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.MODEL)

        input_cost = response.usage.prompt_tokens * pricing.input_price
        output_cost = response.usage.completion_tokens * pricing.output_price
        total_cost = input_cost + output_cost

        return total_cost


if __name__ == "__main__":
    load_dotenv()
    client = OpenAIClient()
    response = client.ask_question("What is the capital of France?")
    print(response["text"])
