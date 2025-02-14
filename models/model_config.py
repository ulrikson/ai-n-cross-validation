from dataclasses import dataclass
from typing import Type
from clients.base_client import LLMClient


@dataclass
class ModelConfig:
    client_class: Type[LLMClient]
    model_name: str
