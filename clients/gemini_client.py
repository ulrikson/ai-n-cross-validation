import os
from typing import Any
from google import genai
from google.genai import types
from .base_client import LLMClient, LLMResponse, PromptType
from dotenv import load_dotenv
from config.pricing_config import get_pricing


class GeminiClient(LLMClient):
    def __init__(self):
        super().__init__()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.MODEL = "gemini-2.0-flash-thinking-exp"

    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponse:
        print(f"Asking Gemini...")
        response = self.client.models.generate_content(
            model=self.MODEL,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=self._PROMPTS[prompt_type]
            ),
        )
        return LLMResponse(text=response.text, raw_response=response)

    def calculate_costs(self, response: Any) -> float:
        pricing = get_pricing(self.MODEL)

        input_cost = response.usage_metadata.prompt_token_count * pricing.input_price
        output_cost = (
            response.usage_metadata.candidates_token_count * pricing.output_price
        )
        total_cost = input_cost + output_cost

        return total_cost


if __name__ == "__main__":
    load_dotenv()
    client = GeminiClient()
    response = client.ask_question("What is the capital of France?")
    print(response.text)
    print(client.calculate_costs(response.raw_response))
