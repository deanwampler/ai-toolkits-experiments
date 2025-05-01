# Invoking LLama API through the OpenAI API:

import os, sys
from openai import OpenAI

# NOTE: Uses the LLAMA_API_KEY, not an OpenAI API key.
api_key = os.environ.get('LLAMA_API_KEY')
if not api_key:
  print("ERROR: environment variable LLAMA_API_KEY is not defined.")
  sys.exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://api.llama.com/compat/v1/",
)

response = client.chat.completions.create(
    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=[
        {"role": "user", "content": "Hello Llama! Can you give me a quick intro?"},
    ],
)

print(response)

