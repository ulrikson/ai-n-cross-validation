# AI Cross Validator

## My Goal
My goal for this project is to see how different LLMs can work together to reduce hallucinations.

The main idea is simple. Instead of relying on one AI's answer, we ask multiple AIs the same question. Then, we compare their answers. 

One model, chosen by the user, will answer the question. Meanwhile, two other models will fact-check the response. A fourth model will summarize the findings. 

This approach (hopefully) reduces the biases or errors of individual models.

## ToDos and Known Issues

- [ ] Being able to select what models run in which order

## Getting Started

### Prerequisites

- Python 3.8+
- Environment variables set for API keys:
  - `ANTHROPIC_API_KEY` for Claude
  - `OPENAI_API_KEY` for OpenAI
  - `GEMINI_API_KEY` for Gemini
  - `MISTRAL_API_KEY` for Mistral

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
   MISTRAL_API_KEY=your_mistral_api_key_here
   ```

### Usage

Run the main script to start the cross validation process:

```bash
python main.py
```
