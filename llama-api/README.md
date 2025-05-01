# README for `llama-api`

April 30, 2025

Yesterday at LlamaCon, Meta announced a new hosted service, [Llama API]() for running inference, tuning, etc. with Llama models. I signed up for the service to try it out.

At first, you go on a waiting list, but I was quickly given access, within a few hours.

After creating an account, they gave me a _bearer API key_ to use, which I stored in an environment variable `LLAMA_API_KEY` and won't show here (for obvious reasons... Also, for simplicity, I won't show error checking to be sure it is defined). They also provided a curl command to try and two Python alternatives. Let's try all three.

## Using the Curl Command

Here is the `curl` command:

```shell
curl "https://api.llama.com/v1/chat/completions" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $LLAMA_API_KEY" \
-d '{
      "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
      "messages": [
        {"role": "user", "content": "Hello Llama! Can you give me a quick intro?"}
      ]
}'
```

There are also two Python API options, one for Llama API and one for OpenAI:

I created a helper script, `invoke-curl.sh`, for this purpose. It expects the API key to be defined in an environment variable `LLAMA_API_KEY`. It gives you some options, including `--format` for passing the returned JSON through `jq` for nice formatting. (`jq` must be installed.)

```shell
$ ./invoke-curl.sh --format --verbose 'Hello Llama! Can you give me a quick intro?'
./invoke.sh:  INFO: ./invoke.sh:
./invoke.sh:  INFO:   Model: Llama-4-Maverick-17B-128E-Instruct-FP8
./invoke.sh:  INFO:   Query: Hello Llama! Can you give me a quick intro?
./invoke.sh:  INFO: curl https://api.llama.com/v1/chat/completions \
./invoke.sh:  INFO:   -H "Content-Type: application/json " \
./invoke.sh:  INFO:   -H "Authorization: Bearer <elided> " \
./invoke.sh:  INFO:   -d "{
./invoke.sh:  INFO:         "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
./invoke.sh:  INFO:         "messages": [
./invoke.sh:  INFO:            {"role": "user", "content": "Hello Llama! Can you give me a quick intro?"}
./invoke.sh:  INFO:     ]
./invoke.sh:  INFO:   }"
query: Hello Llama! Can you give me a quick intro?
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   660  100   519  100   141    902    245 --:--:-- --:--:-- --:--:--  1147
{
  "completion_message": {
    "content": {
      "type": "text",
      "text": "I'm Llama, a Meta-designed model here to adapt to your conversational style. Whether you need quick answers, deep dives into ideas, or just want to vent, joke or brainstorm—I'm here for it. What’s on your mind?"
    },
    "role": "assistant",
    "stop_reason": "stop",
    "tool_calls": []
  },
  "metrics": [
    {
      "metric": "num_completion_tokens",
      "value": 51,
      "unit": "tokens"
    },
    {
      "metric": "num_prompt_tokens",
      "value": 22,
      "unit": "tokens"
    },
    {
      "metric": "num_total_tokens",
      "value": 73,
      "unit": "tokens"
    }
  ]
}
```

## Using the Python (Llama API)

The corresponding Python example using the Llama API is the following, with the added code to get the API key from the environment:

```python
import os
from llama_api_client import LlamaAPIClient

api_key = os.environ['LLAMA_API_KEY']
client = LlamaAPIClient(
    api_key=api_key,
    base_url="https://api.llama.com/",
)

response = client.chat.completions.create(
    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=[
        {"role": "user", "content": "Hello Llama! Can you give me a quick intro?"},
    ],
)

print(response)
```

To use this new API, you have to run `pip install llama-api-client` and also install `rich` and `termcolor` for my wrapper script. I'll use a `uv` environment again and I named the Python file `invoke-llama-api.py`, which is actually adapted from `../llama-stack/agent-example.py` to use the shared helper code to create a chat tool:

```shell
$ uv run --with llama-api-client pip install rich termcolor # one time only!
$ uv run --with llama-api-client invoke-llama-api.py
...
llama_api_client.NotFoundError: Error code: 404 - {'title': 'Not Found', 'detail': "Path '/chat/completions' was not found", 'status': 404}
...
```

There is a typo in the example; the base URL needs to be `base_url="https://api.llama.com/v1/"`. Fixing that:


```shell
$ uv run --with llama-api-client invoke-llama-api.py
A chat example using the Llama API:
Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.
Examples (enter the number to try one or 'all' to try all of them):
 1: Hello Llama! Can you give me a quick intro?
 2: When did Pope Francis die?
 3: When did Pope Francis die? Be sure to search for the latest news about him.
 4: Use google search to determine when Pope Francis died.
> 1

Using prompt> Hello Llama! Can you give me a quick intro?
CreateChatCompletionResponse(
│   completion_message=CompletionMessage(
│   │   content=MessageTextContentItem(
│   │   │   text="I'm Llama, a Meta-designed model here to adapt to your conversational style. Whether you need quick answers, deep dives into ideas, or just want to vent, joke or brainstorm—I'm here for it. What’s on your mind?",
│   │   │   type='text'
│   │   ),
│   │   role='assistant',
│   │   stop_reason='stop',
│   │   tool_calls=[]
│   ),
│   metrics=[
│   │   Metric(metric='num_completion_tokens', value=51.0, unit='tokens'),
│   │   Metric(metric='num_prompt_tokens', value=22.0, unit='tokens'),
│   │   Metric(metric='num_total_tokens', value=73.0, unit='tokens')
│   ]
)
Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.
Examples (enter the number to try one or 'all' to try all of them):
 1: Hello Llama! Can you give me a quick intro?
 2: When did Pope Francis die?
 3: When did Pope Francis die? Be sure to search for the latest news about him.
 4: Use google search to determine when Pope Francis died.
>
Finished!
```

## Using the Llama API through OpenAI

You can also go through the OpenAI API. In the following example, note that you still use the `llama_api_key`, rather than an OpenAI API key. You'll also need to `pip install openai`:

```python
import os
from openai import OpenAI

api_key = os.environ['LLAMA_API_KEY']
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
```
(Note that this example already had the required `/v1/` part of the path.) Let's try it.

My expanded chat version is `invoke-open-ai.py`:

```shell
$ uv run --with openai --with llama_api_client invoke-open-ai.py

A chat example using the Llama API OpenAI integration:
Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.
Examples (enter the number to try one or 'all' to try all of them):
 1: Hello Llama! Can you give me a quick intro?
 2: When did Pope Francis die?
 3: When did Pope Francis die? Be sure to search for the latest news about him.
 4: Use google search to determine when Pope Francis died.
> 1

Using prompt> Hello Llama! Can you give me a quick intro?
ChatCompletion(
│   id='AmELyFD-msNOBO6Q1EaVGvs',
│   choices=[
│   │   Choice(
│   │   │   finish_reason='stop',
│   │   │   index=0,
│   │   │   logprobs=ChoiceLogprobs(content=None, refusal=None),
│   │   │   message=ChatCompletionMessage(
│   │   │   │   content="I'm Llama, a Meta-designed model here to adapt to your conversational style. Whether you need quick answers, deep dives into ideas, or just want to vent, joke or brainstorm—I'm here for it. What’s on your mind?",
│   │   │   │   refusal='',
│   │   │   │   role='assistant',
│   │   │   │   annotations=None,
│   │   │   │   audio=None,
│   │   │   │   function_call=None,
│   │   │   │   tool_calls=[],
│   │   │   │   id='AmELyFD-msNOBO6Q1EaVGvs'
│   │   │   )
│   │   )
│   ],
│   created=1746126394,
│   model='Llama-4-Maverick-17B-128E-Instruct-FP8',
│   object='chat.completions',
│   service_tier=None,
│   system_fingerprint=None,
│   usage=CompletionUsage(
│   │   completion_tokens=51,
│   │   prompt_tokens=22,
│   │   total_tokens=73,
│   │   completion_tokens_details=None,
│   │   prompt_tokens_details=None
│   )
)
Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.
Examples (enter the number to try one or 'all' to try all of them):
 1: Hello Llama! Can you give me a quick intro?
 2: When did Pope Francis die?
 3: When did Pope Francis die? Be sure to search for the latest news about him.
 4: Use google search to determine when Pope Francis died.
>
Finished!
```

So, the three invocation options work well. Next I'll have to investigate additional features available through this new service.
