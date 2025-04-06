from typing import Any, Dict, List, Callable
from client_types import PromptType
from config import get_prompt_template


def validate_answer(
    ask_question_fn: Callable,
    original_question: str,
    initial_answer: str,
) -> Dict[str, Any]:
    """Validate an answer using the LLM."""
    prompt = get_prompt_template("validation").format(
        original_question=original_question, initial_answer=initial_answer
    )
    return ask_question_fn(prompt, PromptType.VALIDATION)


def summarize_answer(
    ask_question_fn: Callable,
    discussion: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Summarize a discussion using the LLM."""
    question = discussion[0]["question"]

    full_discussion = "\n\n".join(
        [
            f"Question: {result['question']}\nAnswer: {result['answer']}"
            for result in discussion
        ]
    )
    prompt = get_prompt_template("summarize").format(
        original_question=question, discussion=full_discussion
    )
    return ask_question_fn(prompt, PromptType.DEFAULT)
