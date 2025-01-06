"""Simple example of using PydanticAI to construct a Pydantic model from a text input.

Run with:

    uv run -m pydantic_ai_examples.pydantic_model
"""

import os
from determine_model import determine_model

import logfire
from pydantic import BaseModel

from pydantic_ai import Agent

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')

class MyModel(BaseModel):
    city: str
    country: str

model = determine_model()
agent = Agent(model, result_type=MyModel)  # 1 change MyModel to str and it _sometimes_ works.

if __name__ == '__main__':
    result = agent.run_sync('The windy city in the US of A.')
    print(result.data)
    print(result.usage())
