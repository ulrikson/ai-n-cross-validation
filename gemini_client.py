import os
import google.generativeai as genai
from base_client import LLMClient


class GeminiClient(LLMClient):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def ask_question(self, question: str) -> str:
        response = self.model.generate_content(question)
        return response.text

    def validate_answer(self, original_question: str, previous_answer: str) -> str:
        prompt = f'I asked this question: "{original_question}" and received this answer: "{previous_answer}". Please fact check and verify this answer.'
        return self.ask_question(prompt)
