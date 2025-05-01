# Using the Llama API:

import os, sys
from llama_api_client import LlamaAPIClient

api_key = os.environ.get('LLAMA_API_KEY')
if not api_key:
  print("ERROR: environment variable LLAMA_API_KEY is not defined.")
  sys.exit(1)

client = LlamaAPIClient(
    api_key=api_key,
    base_url="https://api.llama.com/v1/",
)
#info curl "https://api.llama.com/v1/chat/completions \\ "

response = client.chat.completions.create(
    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=[
        {"role": "user", "content": "Hello Llama! Can you give me a quick intro?"},
    ],
)

print(response)
