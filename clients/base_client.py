from abc import ABC, abstractmethod
from typing import Any
from enum import Enum, auto
from models.llm_response import LLMResponse


class PromptType(Enum):
    DEFAULT = auto()
    VALIDATION = auto()
    SUMMARIZE = auto()


class LLMClient(ABC):
    _VALIDATION_PROMPT = (
        'I asked this question to my friend: "{original_question}" and received this answer: "{previous_answer}". '
        "Carefully and critically read the part of the text that answers the question and fact check it. "
        "Ignore the rest of the text."
        "Return the original text with your annotations and comments in markdown format."
        "Use the same language as the original text."
    )

    _SUMMARIZE_PROMPT = (
        "You've been given a fact checked answer to a question. "
        'The question is: "{original_question}". '
        'The answer is: "{previous_answer}". '
        "The answer contains annotations and comments in markdown format. "
        "Use the annotations and comments to update the answer. "
        "Remove any information that does not answer the question. "
        "Just return the updated answer, do not include any other text."
        "Use the same language as the original text."
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
        self.MODEL = None  # Will be set by ModelSelector

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

    def summarize_answer(
        self, original_question: str, previous_answer: str
    ) -> LLMResponse:
        prompt = self._SUMMARIZE_PROMPT.format(
            original_question=original_question, previous_answer=previous_answer
        )
        return self.ask_question(prompt, PromptType.DEFAULT)

    @abstractmethod
    def calculate_costs(self, response: Any) -> float:
        pass
