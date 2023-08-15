from typing import Callable, Dict

from guardrails import Prompt
from guardrails.agent.trajectory import Step
from guardrails.llm_providers import openai_chat_wrapper


def match_step_with_classification_prompt(
    step: Step,
    prompt: Prompt,
    fill_fn: Callable[[Step], Dict[str, str]],
) -> bool:
    """
    Check if a step matches a prompt.
    """
    response = openai_chat_wrapper(
        str(prompt.format(**fill_fn(step))),
        temperature=0.1,
        max_tokens=1,
    )

    try:
        return bool(eval(response))
    except ValueError:
        return False
