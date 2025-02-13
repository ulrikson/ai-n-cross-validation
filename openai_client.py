import os
from openai import OpenAI
from base_client import LLMClient
from typing import Any


class OpenAIClient(LLMClient):
    INPUT_TOKEN_PRICE_CENTS = (2.5 / 1000000) * 100  # $2.50 per million input tokens
    OUTPUT_TOKEN_PRICE_CENTS = (10 / 1000000) * 100  # $10.00 per million output tokens

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def ask_question(self, question: str) -> str:
        print(f"Asking OpenAI...")
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )
        self.print_costs(completion)
        return completion.choices[0].message.content

    def print_costs(self, response: Any) -> None:
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        input_cost = input_tokens * OpenAIClient.INPUT_TOKEN_PRICE_CENTS
        output_cost = output_tokens * OpenAIClient.OUTPUT_TOKEN_PRICE_CENTS
        total_cost = input_cost + output_cost

        print(
            f"OpenAI cost (cents): {total_cost:.3f} total ({input_tokens} input tokens + {output_tokens} output tokens)"
        )


if __name__ == "__main__":
    client = OpenAIClient()
    print(client.ask_question("What is the capital of France?"))
