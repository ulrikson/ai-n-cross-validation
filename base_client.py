from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass
from enum import Enum, auto


class PromptType(Enum):
    DEFAULT = auto()
    VALIDATION = auto()


@dataclass
class LLMResponse:
    text: str
    raw_response: Any


class LLMClient(ABC):
    _VALIDATION_PROMPT = (
        'I asked this question to my friend: "{original_question}" and received this answer: "{previous_answer}". '
        "Carefully read the text word by word and fact check each factual statement. "
        "If you find any factual errors, correct them. "
        "If you don't find any errors, just return the original answer. "
        "Ensure the answer answers the original question. "
        "Please return your answer in markdown format."
        "Use the same language as the question."
    )

    _PROMPTS = {
        PromptType.VALIDATION: (
            "You are an experienced fact checker. "
            "You've worked for esteemed publications like The New Yorker and The Economist."
            "You follow their best practices for fact checking."
        ),
        PromptType.DEFAULT: "You are a research assistant.",
    }

    def __init__(self):
        self.system_prompt = self._PROMPTS[PromptType.DEFAULT]

    @abstractmethod
    def ask_question(
        self, question: str, prompt_type: PromptType = PromptType.DEFAULT
    ) -> LLMResponse:
        pass

    def validate_answer(
        self, original_question: str, previous_answer: str
    ) -> LLMResponse:
        prompt = self._VALIDATION_PROMPT.format(
            original_question=original_question, previous_answer=previous_answer
        )
        return self.ask_question(prompt, PromptType.VALIDATION)

    @abstractmethod
    def calculate_costs(self, response: Any) -> float:
        pass
