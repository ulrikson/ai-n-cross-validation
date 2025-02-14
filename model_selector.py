from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Type
from base_client import LLMClient
from claude_client import ClaudeClient
from openai_client import OpenAIClient
from gemini_client import GeminiClient


class PerformanceMode(Enum):
    FAST = "f"
    COMPREHENSIVE = "c"


@dataclass
class ModelConfig:
    client_class: Type[LLMClient]
    model_name: str


class ModelSelector:
    _FAST_MODELS = {
        "claude": ModelConfig(ClaudeClient, "claude-3-5-haiku-latest"),
        "openai": ModelConfig(OpenAIClient, "gpt-4o-mini"),
        "gemini": ModelConfig(GeminiClient, "gemini-2.0-flash"),
    }

    _COMPREHENSIVE_MODELS = {
        "claude": ModelConfig(ClaudeClient, "claude-3-5-sonnet-latest"),
        "openai": ModelConfig(OpenAIClient, "gpt-4o"),
        "gemini": ModelConfig(GeminiClient, "gemini-2.0-flash-thinking-exp"),
    }

    @staticmethod
    def get_performance_mode() -> PerformanceMode:
        while True:
            choice = input(
                "Performance mode? Choose: (f)ast or (c)omprehensive: "
            ).lower()
            if choice in [mode.value for mode in PerformanceMode]:
                return PerformanceMode(choice)
            print("Invalid choice. Please enter 'f' for fast or 'c' for comprehensive.")

    def select_models(self, mode: PerformanceMode) -> List[LLMClient]:
        model_configs = (
            self._FAST_MODELS
            if mode == PerformanceMode.FAST
            else self._COMPREHENSIVE_MODELS
        )

        clients = []
        for config in model_configs.values():
            client = config.client_class()
            client.MODEL = config.model_name
            clients.append(client)

        return clients
