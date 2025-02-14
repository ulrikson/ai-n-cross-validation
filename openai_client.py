import os
from openai import OpenAI
from base_client import LLMClient, LLMResponse, PromptType
from typing import Any
from dotenv import load_dotenv
from pricing_config import get_pricing


class OpenAIClient(LLMClient):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.MODEL = "gpt-4o"  # Default model, can be overridden

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponse:
        print(f"Asking OpenAI...")
        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self._PROMPTS[prompt_type]},
                {"role": "user", "content": question},
            ],
        )
        return LLMResponse(
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
    print(response.text)
