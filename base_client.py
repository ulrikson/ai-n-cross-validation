from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def ask_question(self, question: str) -> str:
        pass

    @abstractmethod
    def validate_answer(self, original_question: str, previous_answer: str) -> str:
        pass 