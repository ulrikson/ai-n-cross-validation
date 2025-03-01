Cleaning up main.py

## Step 1: Move utils functions to a separate file
- move: convert_currency, print_markdown, get_question, ensure_output_directory, save_results_to_file to utils.py

## Step 2: Move model function to a separate file
- move: validate_with_models to validator.py

## Step 3: refactor the try catch block in main.py
- refactor: move the logic in the try part to a separate function. keep it in the main.py