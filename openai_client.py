import os
from openai import OpenAI
from base_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def ask_question(self, question: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question},
            ],
        )
        return completion.choices[0].message.content

    def validate_answer(self, original_question: str, previous_answer: str) -> str:
        prompt = (
            f'I asked this question: "{original_question}" and received this answer: "{previous_answer}".'
            " Please fact check and verify this answer."
        )
        return self.ask_question(prompt)


if __name__ == "__main__":
    client = OpenAIClient()
    print(client.ask_question("What is the capital of France?"))
