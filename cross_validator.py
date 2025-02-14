import os
from datetime import datetime
from typing import List
from clients.base_client import LLMClient
from validation_result import ValidationResult


class CrossValidator:
    def __init__(self, clients: List[LLMClient]):
        self.clients = clients
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        os.makedirs("outputs", exist_ok=True)

    def _save_to_file(self, results: List[ValidationResult]):
        filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w") as f:
            f.write(f"Question: {results[0].question}\n\n")
            for result in results:
                f.write(f"Model: {result.model_name}\n")
                f.write(f"Timestamp: {result.timestamp}\n")
                f.write(f"Answer:\n{result.answer}\n\n")
                f.write("-" * 80 + "\n\n")

    def validate(self, question: str) -> List[ValidationResult]:
        results = []
        previous_answer = None

        for i, client in enumerate(self.clients):
            if i == 0:
                response = client.ask_question(question)
            else:
                response = client.validate_answer(question, previous_answer)

            cost = client.calculate_costs(response.raw_response)
            result = ValidationResult(
                question=question,
                model_name=client.__class__.__name__,
                answer=response.text,
                cost=cost,
            )
            results.append(result)
            previous_answer = response.text

        self._save_to_file(results)
        return results
