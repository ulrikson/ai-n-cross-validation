from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    raw_response: Any


class LLMClient(ABC):
    _VALIDATION_PROMPT = (
        'I asked this question to my friend: "{original_question}" and received this answer: "{previous_answer}". '
        "Please fact check the answer, clarify it if needed and return the correct answer. "
        "Please return your answer in markdown format."
        "Use the same language as the question."
    )

    @abstractmethod
    def ask_question(self, question: str) -> LLMResponse:
        pass

    def validate_answer(
        self, original_question: str, previous_answer: str
    ) -> LLMResponse:
        prompt = self._VALIDATION_PROMPT.format(
            original_question=original_question, previous_answer=previous_answer
        )
        return self.ask_question(prompt)

    @abstractmethod
    def calculate_costs(self, response: Any) -> float:
        pass
