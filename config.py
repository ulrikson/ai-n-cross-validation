import json
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load the configuration from the JSON file."""
    with open("config.json", "r") as f:
        return json.load(f)


def get_pricing(model_name: str) -> Dict[str, float]:
    """Get the pricing for a specific model."""
    config = load_config()
    if model_name not in config["models"]:
        raise ValueError(f"Model {model_name} not found in pricing configuration")
    return config["models"][model_name]


def get_performance_mode_config(mode: str) -> Dict[str, Dict[str, str]]:
    """Get the configuration for a specific performance mode."""
    config = load_config()
    if mode not in config["performance_modes"]:
        raise ValueError(f"Performance mode {mode} not found in configuration")
    return config["performance_modes"][mode]
