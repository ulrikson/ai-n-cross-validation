from enum import Enum
from typing import List
from clients.base_client import LLMClient
from clients.claude_client import ClaudeClient
from clients.mistral_client import MistralClient
from clients.openai_client import OpenAIClient
from clients.gemini_client import GeminiClient
from models import create_model_config


class PerformanceMode(Enum):
    FAST = "f"
    COMPREHENSIVE = "c"


class ModelSelector:
    _FAST_MODELS = {
        "gemini": create_model_config(GeminiClient, "gemini-2.0-flash"),
        "openai": create_model_config(OpenAIClient, "gpt-4o-mini"),
        "claude": create_model_config(ClaudeClient, "claude-3-5-haiku-latest"),
        "mistral": create_model_config(MistralClient, "mistral-small-latest"),
    }

    _COMPREHENSIVE_MODELS = {
        "gemini": create_model_config(GeminiClient, "gemini-2.0-flash-thinking-exp"),
        "openai": create_model_config(OpenAIClient, "gpt-4o"),
        "claude": create_model_config(ClaudeClient, "claude-3-5-sonnet-latest"),
        "mistral": create_model_config(MistralClient, "mistral-large-latest"),
    }

    @staticmethod
    def get_performance_mode() -> PerformanceMode:
        while True:
            choice = input("Choose: (f)ast or (c)omprehensive [f]: ").lower() or "f"
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
            client = config["client_class"]()
            client.MODEL = config["model_name"]
            clients.append(client)

        return clients
