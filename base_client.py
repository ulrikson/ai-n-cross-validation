from abc import ABC, abstractmethod
from typing import Any


class LLMClient(ABC):
    _VALIDATION_PROMPT = (
        'I asked this question to my friend: "{original_question}" and received this answer: "{previous_answer}". '
        "Please read the question, then create your new answer, then finally compare this new answer with the previous answer. "
        "If the new answer is different, please explain why it is different."
        "Please return your answer in markdown format."
        "Use the same language as the question."
    )

    @abstractmethod
    def ask_question(self, question: str) -> str:
        pass

    def validate_answer(self, original_question: str, previous_answer: str) -> str:
        prompt = self._VALIDATION_PROMPT.format(
            original_question=original_question, previous_answer=previous_answer
        )
        return self.ask_question(prompt)

    @abstractmethod
    def print_costs(self, response: Any):
        pass
