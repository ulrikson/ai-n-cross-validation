from pathlib import Path


class QuestionInputHandler:
    @staticmethod
    def get_input_method():
        """Get the user's preferred input method."""
        while True:
            choice = input("Choose input method ([W]rite/[F]ile) [W]: ").strip().upper()
            if choice in ["", "W"]:
                return "write"
            if choice == "F":
                return "file"
            print("Invalid choice. Please enter 'W' for Write or 'F' for File.")

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

        if input_method == "write":
            return cls.get_question_from_console()
        return cls.get_question_from_file()
