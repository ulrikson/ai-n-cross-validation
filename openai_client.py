import os
from openai import OpenAI
from base_client import LLMClient, LLMResponse
from typing import Any


class OpenAIClient(LLMClient):
    INPUT_TOKEN_PRICE = 2.5 / 1000000  # $2.50 per million input tokens
    OUTPUT_TOKEN_PRICE = 10 / 1000000  # $10.00 per million output tokens

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def ask_question(self, question: str) -> LLMResponse:
        print(f"Asking OpenAI...")
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": question},
            ],
        )
        return LLMResponse(
            text=completion.choices[0].message.content, raw_response=completion
        )

    def calculate_costs(self, response: Any) -> float:
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        input_cost = input_tokens * OpenAIClient.INPUT_TOKEN_PRICE
        output_cost = output_tokens * OpenAIClient.OUTPUT_TOKEN_PRICE
        total_cost = input_cost + output_cost

        return total_cost
