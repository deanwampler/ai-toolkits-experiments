"""Simple example of using PydanticAI to construct a Pydantic model from a text input.

Run with:

    uv run -m pydantic_ai_examples.pydantic_model
"""

import os
import sys

from pydantic_ai_examples.determine_model import determine_model

def help():
    print("""
usage: python -m pydantic_ai_examples.check_determine_model [args]
where the args can be:
-h | --help    Print this message and exit.
default_model  A default model name. If not provided the built-in 
               default value is used.
    """)

if __name__ == '__main__':
    default_model = None
    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            help()
            sys.exit(0)
        else:
            default_model=arg

    model = determine_model(default_model = default_model)
    print(f'(specified default: {default_model})')
