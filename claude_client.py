import os
import anthropic
from base_client import LLMClient


class ClaudeClient(LLMClient):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def ask_question(self, question: str) -> str:
        print(f"Asking Claude...")
        response = self.client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}],
        )
        return response.content[0].text
