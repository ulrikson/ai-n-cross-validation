from enum import Enum
from typing import List, Dict, Any
from clients import create_client
from config import get_performance_mode_config


class PerformanceMode(Enum):
    FAST = "f"
    COMPREHENSIVE = "c"


class ModelSelector:
    @staticmethod
    def get_performance_mode() -> PerformanceMode:
        while True:
            choice = input("Choose: (f)ast or (c)omprehensive [f]: ").lower() or "f"
            if choice in [mode.value for mode in PerformanceMode]:
                return PerformanceMode(choice)

            print("Invalid choice. Please enter 'f' for fast or 'c' for comprehensive.")

    def select_models(self, mode: PerformanceMode) -> List[Dict[str, Any]]:
        mode_name = "fast" if mode == PerformanceMode.FAST else "comprehensive"
        model_configs = get_performance_mode_config(mode_name)

        clients = []
        for config in model_configs.values():
            client = create_client(config["provider"])
            client["MODEL"] = config["model"]
            clients.append(client)

        return clients
