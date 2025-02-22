"""Simple example of using PydanticAI to construct a Pydantic model from a text input.

Run with:

    uv run -m pydantic_ai_examples.pydantic_model
"""

import os
from pydantic_ai_examples.determine_model import determine_model

import logfire
from pydantic import BaseModel

from pydantic_ai import Agent

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')

class MyModel(BaseModel):
    city: str
    country: str

model = determine_model()
agent = Agent(model, result_type=MyModel)  
#agent = Agent(model, result_type=MyModel.model_json_schema()) # Causes type failure.
#agent = Agent(model, result_type=str)  # Change MyModel to str and it _sometimes_ works.

if __name__ == '__main__':
    user_prompt = 'The windy city in the US of A.'
    full_prompt = """{
  "model": "%s",
  "messages": [{"role": "user", "content": "%s"}],
  "stream": false,
  "format": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      },
      "country": {
        "type": "string"
      },
    },
    "required": [
      "city",
      "country", 
    ]
  }
}""" % (model, user_prompt)

    print("Using the full prompt:")
    result = agent.run_sync(full_prompt)
    print(result.data)
    print(result.usage())

    print("Using just the user prompt:")
    result = agent.run_sync(user_prompt)
    print(result.data)
    print(result.usage())
