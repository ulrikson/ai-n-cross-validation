from datetime import datetime
from typing import Any, Dict, Optional, TypedDict


class ModelConfig(TypedDict):
    client_type: str
    model_name: str


class ValidationResult(TypedDict):
    question: str
    model_name: str
    answer: str
    cost: float
    timestamp: datetime


class LLMResponse(TypedDict):
    text: str
    raw_response: Any


def create_model_config(client_type: str, model_name: str) -> ModelConfig:
    """Create an immutable model configuration."""
    return {"client_type": client_type, "model_name": model_name}


def create_validation_result(
    question: str,
    model_name: str,
    answer: str,
    cost: float = 0.0,
    timestamp: Optional[datetime] = None,
) -> ValidationResult:
    """Create an immutable validation result."""
    return {
        "question": question,
        "model_name": model_name,
        "answer": answer,
        "cost": cost,
        "timestamp": timestamp or datetime.now(),
    }


def create_llm_response(text: str, raw_response: Any) -> LLMResponse:
    """Create an immutable LLM response."""
    return {"text": text, "raw_response": raw_response}