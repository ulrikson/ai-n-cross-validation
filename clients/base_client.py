from abc import ABC, abstractmethod
from typing import Any, List
from enum import Enum, auto
from models.llm_response import LLMResponse
from models.validation_result import ValidationResult


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
        "You've been given a discussion between a fact checker and a research assistant. "
        'The original question was: "{original_question}". '
        'The discussion has been: "{discussion}". '
        "Distill the discussion into a single answer to the question."
        "Elaborate on any points that are not clear."
        "Use the same language as the original text."
        "Return the answer in markdown format."
    )

    _PROMPTS = {  # todo: should be called _SYSTEM_PROMPTS
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

    def summarize_answer(self, discussion: List[ValidationResult]) -> LLMResponse:
        question = discussion[0].question
        full_discussion = "\n\n".join(
            [
                f"Question: {result.question}\nAnswer: {result.answer}"
                for result in discussion
            ]
        )
        prompt = self._SUMMARIZE_PROMPT.format(
            original_question=question, discussion=full_discussion
        )

        return self.ask_question(prompt, PromptType.DEFAULT)

    @abstractmethod
    def calculate_costs(self, response: Any) -> float:
        pass
