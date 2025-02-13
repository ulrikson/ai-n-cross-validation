# AI Cross Validator

AI Cross Validator is a project that leverages multiple AI models to answer questions. By cross validating responses from several large language models (LLMs) like Claude, OpenAI's GPT, and Gemini, the project aims to provide more reliable and robust answers that are less likely to be incorrect.

## Overview

The core idea behind this project is simple: instead of relying on a single AI's response, we ask multiple AIs the same question and then compare or validate their answers. This approach can help mitigate individual model biases or errors, giving you increased confidence in the final answer.

## Key Benefits

- **Improved Accuracy**: By validating responses across multiple AIs, you reduce the risk of an outlier or incorrect answer.
- **Reduced Bias**: Each model may have its own weaknesses; cross validation helps balance these out.
- **Transparency**: Get insight on each model's response, including cost details based on token usage.
- **Flexibility**: Easily integrate additional AI models by extending the common interface.

## Features

- **Multi-AI Integration**: Supports Claude, OpenAI (GPT-4o), and Gemini.
- **Cross Validation**: Compare responses from different models to derive a consensus.
- **Cost Tracking**: Prints the pricing cost of each call based on tokens consumed.
- **Modular Design**: Follows SOLID principles and best practices, keeping functions simple and maintainable.

## Getting Started

### Prerequisites

- Python 3.8+
- Environment variables set for API keys:
  - `ANTHROPIC_API_KEY` for Claude
  - `OPENAI_API_KEY` for OpenAI
  - `GEMINI_API_KEY` for Gemini

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ulrikson/ai-n-cross-validator.git
   cd ai-n-cross-validator
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys:
   ```env
   ANTHROPIC_API_KEY=your_claude_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Usage

Run the main script to start the cross validation process:

```bash
python main.py
```
