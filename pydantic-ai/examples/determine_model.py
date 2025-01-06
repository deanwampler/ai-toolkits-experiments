"""
Shared code to determine the model to use. Adapted from pydantic_model.py.
Added by Dean Wampler. See the README.
"""

import os
from typing import cast
from pydantic_ai.models import KnownModelName

def determine_model(default_model: str = None) -> str:
    """
    Read the environment variable, `PYDANTIC_AI_MODEL`, and return its value.
    If not defined, then return the value of `default_model`, unless it is
    `None`, in which case return `openai:gpt-4o`.
    This function also prints which model string it is returning.
    """
    if not default_model:
        default_model = 'openai:gpt-4o'
    model = cast(KnownModelName, os.getenv('PYDANTIC_AI_MODEL', default_model))
    print(f'Using model: {model}')
    return model
