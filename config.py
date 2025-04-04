import json
import os
from typing import Dict, Any
from functools import lru_cache


@lru_cache(maxsize=1)
def load_config() -> Dict[str, Any]:
    """Load the configuration from the JSON file (cached for efficiency)."""
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


def read_prompt_file(filename: str) -> str:
    """Read a prompt from a markdown file."""
    filepath = os.path.join("prompts", filename)
    with open(filepath, "r") as f:
        return f.read().strip()


def get_prompt_template(prompt_type: str) -> str:
    """Get a prompt template by type."""
    prompt_file_map = {
        "validation": "validation_prompt.md",
        "summarize": "summarize_prompt.md",
    }

    if prompt_type not in prompt_file_map:
        raise ValueError(f"Prompt template {prompt_type} not found")

    file = prompt_file_map[prompt_type]
    return read_prompt_file(file)


def get_system_prompt(prompt_type: str) -> str:
    """Get a system prompt by type."""
    prompt_type = prompt_type.lower()
    system_prompt_file_map = {
        "default": "default_system_prompt.md",
        "validation": "validation_system_prompt.md",
    }

    if prompt_type not in system_prompt_file_map:
        raise ValueError(f"System prompt {prompt_type} not found")

    return read_prompt_file(system_prompt_file_map[prompt_type])
