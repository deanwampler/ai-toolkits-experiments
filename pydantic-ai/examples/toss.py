"""Simple example of using PydanticAI to construct a Pydantic model from a text input.

Run with:

    uv run -m pydantic_ai_examples.pydantic_model
"""

import os
from determine_model import determine_model

if __name__ == '__main__':
    model = determine_model()
    print(f'Using model: {model}')
