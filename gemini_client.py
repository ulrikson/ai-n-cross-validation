import os
import google.generativeai as genai
from base_client import LLMClient


class GeminiClient(LLMClient):
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def ask_question(self, question: str) -> str:
        print(f"Asking Gemini...")
        response = self.model.generate_content(question)
        return response.text
