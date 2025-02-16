from enum import Enum
from typing import List
from clients.base_client import LLMClient
from clients.claude_client import ClaudeClient
from clients.mistral_client import MistralClient
from clients.openai_client import OpenAIClient
from clients.gemini_client import GeminiClient
from models.model_config import ModelConfig


class PerformanceMode(Enum):
    FAST = "f"
    COMPREHENSIVE = "c"


class ModelSelector:
    _FAST_MODELS = {
        "openai": ModelConfig(OpenAIClient, "gpt-4o-mini"),
        "claude": ModelConfig(ClaudeClient, "claude-3-5-haiku-latest"),
        "gemini": ModelConfig(GeminiClient, "gemini-2.0-flash"),
        "mistral": ModelConfig(MistralClient, "mistral-small-latest"),
    }

    _COMPREHENSIVE_MODELS = {
        "openai": ModelConfig(OpenAIClient, "gpt-4o"),
        "claude": ModelConfig(ClaudeClient, "claude-3-5-sonnet-latest"),
        "gemini": ModelConfig(GeminiClient, "gemini-2.0-flash-thinking-exp"),
        "mistral": ModelConfig(MistralClient, "mistral-large-latest"),
    }

    @staticmethod
    def get_performance_mode() -> PerformanceMode:
        while True:
            choice = input("Choose: (f)ast or (c)omprehensive: ").lower()
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
