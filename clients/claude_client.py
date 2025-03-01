import os
import anthropic
from .base_client import LLMClient, PromptType
from typing import Any
from dotenv import load_dotenv
from config.pricing_config import get_pricing
from models import create_llm_response, LLMResponseDict


class ClaudeClient(LLMClient):
    def __init__(self):
        super().__init__()
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.MODEL = "claude-3-5-sonnet-latest"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponseDict:
        print(f"{self.MODEL} is thinking...")
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=1024,
            system=self._PROMPTS[prompt_type],
            messages=[
                {"role": "user", "content": question},
            ],
        )
        return create_llm_response(text=response.content[0].text, raw_response=response)

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.MODEL)

        input_cost = response.usage.input_tokens * pricing.input_price
        output_cost = response.usage.output_tokens * pricing.output_price
        total_cost = input_cost + output_cost

        return total_cost


if __name__ == "__main__":
    load_dotenv()
    client = ClaudeClient()
    response = client.ask_question("What is the capital of France?")
    print(response["text"])
    print(client.calculate_costs(response["raw_response"]))
