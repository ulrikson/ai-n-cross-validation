from datetime import datetime
from typing import Any, Dict, Optional


# Simple dictionary type definitions
ModelConfigDict = Dict[str, Any]
ValidationResultDict = Dict[str, Any]
LLMResponseDict = Dict[str, Any]


# Helper functions to create dictionaries
def create_model_config(client_class: Any, model_name: str) -> ModelConfigDict:
    return {"client_class": client_class, "model_name": model_name}


def create_validation_result(
    question: str,
    model_name: str,
    answer: str,
    cost: float = 0.0,
    timestamp: Optional[datetime] = None,
) -> ValidationResultDict:
    return {
        "question": question,
        "model_name": model_name,
        "answer": answer,
        "cost": cost,
        "timestamp": timestamp or datetime.now(),
    }


def create_llm_response(text: str, raw_response: Any) -> LLMResponseDict:
    return {"text": text, "raw_response": raw_response}
