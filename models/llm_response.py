from dataclasses import dataclass
from typing import Any


@dataclass
class LLMResponse:
    text: str
    raw_response: Any
