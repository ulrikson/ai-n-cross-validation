import os
from datetime import datetime
from typing import List
from clients.base_client import LLMClient
from models.validation_result import ValidationResult
from io import TextIOWrapper


class CrossValidator:
    def __init__(self, clients: List[LLMClient]):
        self.clients = clients
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        """Ensure the output directory exists."""
        os.makedirs("outputs", exist_ok=True)

    def _save_to_file(self, results: List[ValidationResult]):
        """Save the results to a file."""
        filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w") as file:
            self._write_to_file(file, results)

    def _write_to_file(self, file: TextIOWrapper, results: List[ValidationResult]):
        """Write the results to a file."""
        file.write(f"Question: {results[0].question}\n\n")
        for result in results:
            file.write(f"Model: {result.model_name}\n")
            file.write(f"Timestamp: {result.timestamp}\n")
            file.write(f"Answer:\n{result.answer}\n\n")

    def validate(self, question: str) -> List[ValidationResult]:
        """Validate an answer across multiple LLMs."""
        results = []
        previous_answer = None

        for i, client in enumerate(self.clients):
            try:
                response = (
                    client.ask_question(question)
                    if i == 0
                    else client.validate_answer(question, previous_answer)
                )

                cost = client.calculate_costs(response.raw_response)
                result = ValidationResult(
                    question=question,
                    model_name=client.__class__.__name__,
                    answer=response.text,
                    cost=cost,
                )
                results.append(result)
                previous_answer = response.text

            except Exception as e:
                self._handle_error(client, e)

        self._save_to_file(results)
        return results

    def _handle_error(self, client: LLMClient, error: Exception):
        """Handle errors by printing a message and continuing to the next model."""
        print(
            f"Error with {client.__class__.__name__}: {str(error)}. Continuing to next model."
        )
