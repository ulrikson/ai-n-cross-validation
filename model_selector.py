from typing import Dict
from config import get_performance_mode_config


def get_performance_mode(mode_arg: str) -> str:
    """Get performance mode from argument or use default."""
    mode = mode_arg.lower()
    
    if mode in ("fast", "f"):
        return "fast"
    elif mode in ("comprehensive", "c"):
        return "comprehensive" 
    elif mode in ("max", "m"):
        return "max"
    else:
        print(f"Invalid mode '{mode_arg}'. Using 'fast' mode.")
        return "fast"


def get_model_configs(mode: str) -> Dict[str, Dict[str, str]]:
    """Get model configurations for the given performance mode."""
    return get_performance_mode_config(mode)