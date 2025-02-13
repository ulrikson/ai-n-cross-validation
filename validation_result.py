from datetime import datetime
from dataclasses import dataclass


@dataclass
class ValidationResult:
    question: str
    model_name: str
    answer: str
    timestamp: datetime = datetime.now()
