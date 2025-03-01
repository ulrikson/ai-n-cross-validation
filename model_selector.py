from enum import Enum
from typing import List, Optional
from clients import create_client, BaseLLMClient
from config import get_performance_mode_config


class PerformanceMode(Enum):
    FAST = "fast"
    COMPREHENSIVE = "comprehensive"


class ModelSelector:
    @staticmethod
    def get_performance_mode(mode_arg: str) -> PerformanceMode:
        """Get performance mode from argument or use default."""

        mode = mode_arg.lower()
        if mode == "fast" or mode == "f":
            return PerformanceMode.FAST
        elif mode == "comprehensive" or mode == "c":
            return PerformanceMode.COMPREHENSIVE
        else:
            print(f"Invalid mode '{mode_arg}'. Using 'fast' mode.")
            return PerformanceMode.FAST

    def select_models(self, mode: PerformanceMode) -> List[BaseLLMClient]:
        """Select models based on performance mode."""
        model_configs = get_performance_mode_config(mode.value)

        clients = []
        for config in model_configs.values():
            client = create_client(
                provider=config["provider"],
                model_name=config["model"],
            )
            clients.append(client)

        return clients
