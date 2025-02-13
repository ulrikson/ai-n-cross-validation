import os
from typing import Any
import google.generativeai as genai
from base_client import LLMClient


class GeminiClient(LLMClient):
    INPUT_TOKEN_PRICE = 0.1 / 1000000  # $0.10 per million input tokens
    OUTPUT_TOKEN_PRICE = 0.4 / 1000000  # $0.40 per million output tokens

    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def ask_question(self, question: str) -> str:
        print(f"Asking Gemini...")
        response = self.model.generate_content(question)
        self.print_costs(response)
        return response.text

    def print_costs(self, response: Any) -> None:
        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count

        input_cost = input_tokens * GeminiClient.INPUT_TOKEN_PRICE
        output_cost = output_tokens * GeminiClient.OUTPUT_TOKEN_PRICE
        total_cost = input_cost + output_cost

        print(
            f"Gemini cost: ${input_cost:.6f} for {input_tokens} input tokens, ${output_cost:.6f} for {output_tokens} output tokens, ${total_cost:.6f} total"
        )
