import os
from typing import Any
from google import genai
from google.genai import types
from base_client import LLMClient, LLMResponse
from dotenv import load_dotenv


class GeminiClient(LLMClient):
    INPUT_TOKEN_PRICE = 0.1 / 1000000  # $0.10 per million input tokens
    OUTPUT_TOKEN_PRICE = 0.4 / 1000000  # $0.40 per million output tokens

    def __init__(self):
        super().__init__()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def ask_question(self, question: str) -> LLMResponse:
        print(f"Asking Gemini...")
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT
            ),
        )
        return LLMResponse(text=response.text, raw_response=response)

    def calculate_costs(self, response: Any) -> float:
        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count

        input_cost = input_tokens * GeminiClient.INPUT_TOKEN_PRICE
        output_cost = output_tokens * GeminiClient.OUTPUT_TOKEN_PRICE
        total_cost = input_cost + output_cost

        return total_cost


if __name__ == "__main__":
    load_dotenv()
    client = GeminiClient()
    response = client.ask_question("What is the capital of France?")
    print(response.text)
    print(client.calculate_costs(response.raw_response))
