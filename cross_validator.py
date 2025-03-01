import os
from datetime import datetime
from typing import List, Dict
from clients.base_client import LLMClient
from models import create_validation_result, ValidationResultDict
from io import TextIOWrapper


class CrossValidator:
    def __init__(self, clients: List[LLMClient]):
        self.clients = clients
        self._ensure_output_directory()

    def _ensure_output_directory(self):
        """Ensure the output directory exists."""
        os.makedirs("outputs", exist_ok=True)

    def _save_to_file(self, results: List[ValidationResultDict]):
        """Save the results to a file."""
        filename = f"outputs/validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w") as file:
            self._write_to_file(file, results)

    def _write_to_file(self, file: TextIOWrapper, results: List[ValidationResultDict]):
        """Write the results to a file."""
        file.write(f"Question: {results[0]['question']}\n\n")
        for result in results:
            file.write(f"Model: {result['model_name']}\n")
            file.write(f"Timestamp: {result['timestamp']}\n")
            file.write(f"Answer:\n{result['answer']}\n\n")

    def validate(self, question: str) -> List[ValidationResultDict]:
        """Validate an answer across multiple LLMs."""
        results = []
        previous_answer = None
        client_count = len(self.clients)

        for i, client in enumerate(self.clients):
            initial_question = i == 0
            last_question = i == client_count - 1

            try:
                if initial_question:
                    response = client.ask_question(question)
                elif last_question:
                    response = client.summarize_answer(results)
                else:
                    response = client.validate_answer(question, previous_answer)

                cost = client.calculate_costs(response["raw_response"])
                result = create_validation_result(
                    question=question,
                    model_name=client.__class__.__name__,
                    answer=response["text"],
                    cost=cost,
                )
                results.append(result)
                previous_answer = response["text"]

            except Exception as e:
                self._handle_error(client, e)

        self._save_to_file(results)
        return results

    def _handle_error(self, client: LLMClient, error: Exception):
        """Handle errors by printing a message and continuing to the next model."""
        print(
            f"Error with {client.__class__.__name__}: {str(error)}. Continuing to next model."
        )
