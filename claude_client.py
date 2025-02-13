import os
import anthropic
from base_client import LLMClient, LLMResponse
from typing import Any


class ClaudeClient(LLMClient):
    INPUT_TOKEN_PRICE = 3 / 1000000  # $3 per million input tokens
    OUTPUT_TOKEN_PRICE = 15 / 1000000  # $15 per million output tokens

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def ask_question(self, question: str) -> LLMResponse:
        print(f"Asking Claude...")
        response = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": question},
            ],
        )
        return LLMResponse(text=response.content[0].text, raw_response=response)

    def calculate_costs(self, response: Any) -> float:
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        input_cost = input_tokens * ClaudeClient.INPUT_TOKEN_PRICE
        output_cost = output_tokens * ClaudeClient.OUTPUT_TOKEN_PRICE
        total_cost = input_cost + output_cost

        return total_cost
