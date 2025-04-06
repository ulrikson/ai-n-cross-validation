from typing import Callable, TypedDict
from enum import Enum, auto


class PromptType(Enum):
    DEFAULT = auto()
    VALIDATION = auto()
    SUMMARIZE = auto()


class ClientFunctions(TypedDict):
    ask_question: Callable
    calculate_costs: Callable
    model_name: str
