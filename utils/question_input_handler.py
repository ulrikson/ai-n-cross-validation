from pathlib import Path
from enum import Enum


class InputMethod(Enum):
    WRITE = "w"
    FILE = "f"


class QuestionInputHandler:
    @staticmethod
    def get_input_method():
        """Get the user's preferred input method."""
        while True:
            choice = input("Input method: [w]rite or [f]ile [w]: ").lower() or "w"
            if choice in [method.value for method in InputMethod]:
                return InputMethod(choice)

            print("Invalid choice. Please enter 'w' for Write or 'f' for File.")

    @staticmethod
    def get_question_from_console():
        """Get question from console input."""
        return input("Enter your question: ").strip()

    @staticmethod
    def get_question_from_file():
        """Get question from a file."""
        while True:
            filename = input("Enter the path to your question file: ").strip()
            file_path = Path(filename)

            if not file_path.exists():
                print(f"File {filename} does not exist. Please try again.")
                continue

            try:
                with open(file_path, "r") as file:
                    question = file.read().strip()
                    if not question:
                        print("File is empty. Please provide a file with content.")
                        continue
                    return question
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                continue

    @classmethod
    def get_question(cls):
        """Get the question using the user's preferred input method."""
        input_method = cls.get_input_method()

        if input_method == InputMethod.WRITE:
            return cls.get_question_from_console()
        return cls.get_question_from_file()
