from datetime import datetime
from dataclasses import dataclass


@dataclass
class ValidationResult:
    question: str
    model_name: str
    answer: str
    cost: float = 0.0
    timestamp: datetime = datetime.now()
