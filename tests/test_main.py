import unittest
import subprocess
import sys
import os
from io import StringIO
from unittest.mock import patch


class TestMainExecution(unittest.TestCase):
    """Test running the main.py script with input."""

    def test_main_with_question(self):
        """Test that main.py can run with 'f' mode and a question."""

        # Path to the main.py script - one directory up from tests
        main_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py"
        )

        # Run the process with input piped in
        process = subprocess.Popen(
            [sys.executable, main_path, "f"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Send a question to stdin
        stdout, stderr = process.communicate(input="hello :)\n")

        # Check that the process completed successfully
        self.assertEqual(process.returncode, 0, f"Process failed with error: {stderr}")

        # Verify that some output was generated
        self.assertTrue(len(stdout) > 0, "No output was generated")

        # Check that the output contains expected elements
        self.assertIn("AI Cross-Validation", stdout, "Missing expected output header")


if __name__ == "__main__":
    unittest.main()
