from enum import Enum
from typing import List, Dict, Any
from clients import create_client


class PerformanceMode(Enum):
    FAST = "f"
    COMPREHENSIVE = "c"


class ModelSelector:
    _FAST_MODELS = {
        "gemini": {"provider": "gemini", "model": "gemini-2.0-flash"},
        "openai": {"provider": "openai", "model": "gpt-4o-mini"},
        "claude": {"provider": "claude", "model": "claude-3-5-haiku-latest"},
        "mistral": {"provider": "mistral", "model": "mistral-small-latest"},
    }

    _COMPREHENSIVE_MODELS = {
        "gemini": {"provider": "gemini", "model": "gemini-2.0-flash-thinking-exp"},
        "openai": {"provider": "openai", "model": "gpt-4o"},
        "claude": {"provider": "claude", "model": "claude-3-5-sonnet-latest"},
        "mistral": {"provider": "mistral", "model": "mistral-large-latest"},
    }

    @staticmethod
    def get_performance_mode() -> PerformanceMode:
        while True:
            choice = input("Choose: (f)ast or (c)omprehensive [f]: ").lower() or "f"
            if choice in [mode.value for mode in PerformanceMode]:
                return PerformanceMode(choice)

            print("Invalid choice. Please enter 'f' for fast or 'c' for comprehensive.")

    def select_models(self, mode: PerformanceMode) -> List[Dict[str, Any]]:
        model_configs = (
            self._FAST_MODELS
            if mode == PerformanceMode.FAST
            else self._COMPREHENSIVE_MODELS
        )

        clients = []
        for config in model_configs.values():
            client = create_client(config["provider"])
            client["MODEL"] = config["model"]
            clients.append(client)

        return clients
