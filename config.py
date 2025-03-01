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


def get_prompt_template(prompt_type: str) -> str:
    """Get a prompt template by type."""
    config = load_config()
    if prompt_type not in config["prompts"]:
        raise ValueError(f"Prompt template {prompt_type} not found in configuration")
    return config["prompts"][prompt_type]


def get_system_prompt(prompt_type: str) -> str:
    """Get a system prompt by type."""
    config = load_config()
    prompt_type = prompt_type.lower()
    if prompt_type not in config["system_prompts"]:
        raise ValueError(f"System prompt {prompt_type} not found in configuration")
    return config["system_prompts"][prompt_type]
