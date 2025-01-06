# README for Pydantic-AI

I experimented with [`pydantic-ai`](https://github.com/pydantic/pydantic-ai/) part of the [`pydantic`](https://ai.pydantic.dev) tools. What's appealing about this library is the use of type checking for values exchanged between tools, among other benefits. Before proceeding, see the `pydantic-ai` [README](https://github.com/pydantic/pydantic-ai/).

## Experiments

I used `ollama` and adapted the [examples](https://github.com/pydantic/pydantic-ai/examples) to try using three models instead of `openai:gpt-4o`:

* `ollama:granite3-moe:3b`
* `ollama:granite3-dense:8B`
* `ollama:llama3.2:3B`

As you might expect, each model gave different results and sometimes one worked better than another, as discussed below.

For convenience, I defined which model to use by defining a shell environment variable, `PYDANTIC_AI_MODEL`, in the `.initrc` file in this directory, which is sourced as follows:

```shell
. initrc
```

(However, I do something more _dynamic_ below...)

Because I needed to tweak the examples to not use OpenAI, I used this convenience command to copy them from the installed code (after pip installing the library; see below):

```shell
python -m pydantic_ai_examples --copy-to examples/
```

Hence, the contents of the `examples` directory is the output of this command, with my additional edits, including the following:

1. Define a helper function, `determine_model`, in a new file, `examples/determine_model.py`, that reads the environment variable and returns a string with the desired model or a default value.
1. Modify most of the examples to import the function and use it to get the correct model, then pass the value to the `Agent` constructor, rather than hard-code the OpenAI model.

> **TODO** Not all the examples successfully execute with all the models I tried. There is work to do to figure out how to make them work with different, smaller models, like the Granite and Llama models chosen. See notes below.

## References

* Running the examples: https://ai.pydantic.dev/examples/#running-examples
* Using `ollama`: 
	* https://ai.pydantic.dev/models/#ollama
	* https://github.com/pydantic/pydantic-ai/blob/main/docs/api/models/ollama.md

## Setup Steps

Setup:

```shell
pip install 'pydantic-ai[examples]'
pip install 'pydantic-ai[openai]'   # necessary for Ollama, too.
```

Next, as discussed above, I created local copies of the examples (which are also in the GitHub repo...):

```shell
python -m pydantic_ai_examples --copy-to examples/
```

I then made the edits discussed above.

## Trying the Examples

First, start Ollama:

```shell
ollama serve  # start ollama
```

Then for each example I tried using the three models. Recall they are:

* `ollama:granite3-moe:3b`
* `ollama:granite3-dense:8B`
* `ollama:llama3.2:3B`

So, for `ollama:granite3-moe:3b`, I used the following commands:

```shell
ollama run granite3-moe:3b 
# CTRL-D out of the CLI; the model will still be running.
PYDANTIC_AI_MODEL=ollama:granite3-moe:3b python examples.<example>.py
ollama stop granite3-moe:3b
```

Repeat for `granite3-dense:8b` and `llama3.2:3B`...

> **NOTE:** If I were running the examples directly from the pip installed library, the command would be:
> ```shell
> PYDANTIC_AI_MODEL=ollama:granite3-moe:3b python -m pydantic_ai_examples.<example> 
> ```

In what follows, I'll just show the `python examples/<example>` command and .pydescribe what happens with each model.

### `pydantic_model`

(I.e., `examples/pydantic_model.py`)

First I tried `granite3-moe:3b`:

```shell
PYDANTIC_AI_MODEL=ollama:granite3-moe:3b python examples/pydantic_model.py
```

Unfortunately, I got type validation errors on the results (apparently, a common issue. See, for example, [this issue](https://github.com/pydantic/pydantic-ai/issues/200)).

```
Using model: ollama:granite3-moe:3b
02:21:54.959 agent run prompt=The windy city in the US of A.
02:21:54.959   preparing model and tools run_step=1
02:21:54.960   model request
02:21:55.386   handle model response
02:21:55.387   preparing model and tools run_step=2
02:21:55.387   model request
02:21:55.753   handle model response
Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/pydantic-ai/examples/pydantic_model.py", line 27, in <module>
    result = agent.run_sync('The windy city in the US of A.')
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 334, in run_sync
    return asyncio.get_event_loop().run_until_complete(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 267, in run
    final_result, tool_responses = await self._handle_model_response(model_response, run_context)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 889, in _handle_model_response
    return await self._handle_text_response(text, run_context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 907, in _handle_text_response
    self._incr_result_retry(run_context)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 1082, in _incr_result_retry
    raise exceptions.UnexpectedModelBehavior(
pydantic_ai.exceptions.UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation
```

It defeats the benefit of type checking, but if you change the `result_type=MyModel` to `result_type=str` on line 24 (see the `# 1` comment), it does "succeed":

```
Using model: ollama:granite3-moe:3b
02:33:24.887 agent run prompt=The windy city in the US of A.
02:33:24.888   preparing model and tools run_step=1
02:33:24.888   model request
02:33:26.111   handle model response
The Windy City is Chicago, Illinois, USA. It's known for its vibrant culture, iconic architecture, and deep-dish pizza.
Usage(requests=1, request_tokens=18, response_tokens=34, total_tokens=52, details=None)
```

Note, I also tried using `result_type=None`, but still got the validation error.

However, `granite3-dense:8b` worked.

```shell
PYDANTIC_AI_MODEL=ollama:granite3-dense:8b python examples/pydantic_model.py
```

Output:

```
sing model: ollama:granite3-dense:8b
02:23:22.795 agent run prompt=The windy city in the US of A.
02:23:22.796   preparing model and tools run_step=1
02:23:22.796   model request
02:23:25.533   handle model response
city='Chicago' country='US'
Usage(requests=1, request_tokens=85, response_tokens=19, total_tokens=104, details=None)
```

(One run gave me the city's tagline, "the windy city", instead of "Chicago".)

Also, `llama3.2:3B` produced the expected result:

```shell
PYDANTIC_AI_MODEL=ollama:llama3.2:3B python examples/pydantic_model.py
```

```
Using model: ollama:llama3.2:3B
02:03:37.822 agent run prompt=The windy city in the US of A.
02:03:37.823   preparing model and tools run_step=1
02:03:37.823   model request
02:03:39.119   handle model response
city='Chicago' country='USA'
Usage(requests=1, request_tokens=173, response_tokens=23, total_tokens=196, details=None)
```

### `pydantic_ai_examples.bank_support`

First I tried `granite3-moe:3b`, but it threw the different error than the validation error previously:

```shell
PYDANTIC_AI_MODEL=ollama:granite3-moe:3b python examples/bank_support.py
```

```
Using model: ollama:granite3-moe:3b
/Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/pydantic-ai/examples/bank_support.py:80: LogfireNotConfiguredWarning: No logs or spans will be created until `logfire.configure()` has been called. Set the environment variable LOGFIRE_IGNORE_NO_CONFIG=1 or add ignore_no_config=true in pyproject.toml to suppress this warning.
  result = support_agent.run_sync('What is my balance?', deps=deps)
Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/pydantic-ai/examples/bank_support.py", line 80, in <module>
    result = support_agent.run_sync('What is my balance?', deps=deps)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 334, in run_sync
    return asyncio.get_event_loop().run_until_complete(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 267, in run
    final_result, tool_responses = await self._handle_model_response(model_response, run_context)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 889, in _handle_model_response
    return await self._handle_text_response(text, run_context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 907, in _handle_text_response
    self._incr_result_retry(run_context)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 1082, in _incr_result_retry
    raise exceptions.UnexpectedModelBehavior(
pydantic_ai.exceptions.UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation
```

Trying `granite3-dense:8b`:

```shell
PYDANTIC_AI_MODEL=ollama:granite3-dense:8b python examples/bank_support.py
```

But it threw a validation error:

```
Using model: ollama:granite3-dense:8b
/Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/pydantic-ai/examples/bank_support.py:80: LogfireNotConfiguredWarning: No logs or spans will be created until `logfire.configure()` has been called. Set the environment variable LOGFIRE_IGNORE_NO_CONFIG=1 or add ignore_no_config=true in pyproject.toml to suppress this warning.
  result = support_agent.run_sync('What is my balance?', deps=deps)
Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai-misc/ai-toolkits-experiments/pydantic-ai/examples/bank_support.py", line 80, in <module>
    result = support_agent.run_sync('What is my balance?', deps=deps)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 334, in run_sync
    return asyncio.get_event_loop().run_until_complete(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/asyncio/base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 267, in run
    final_result, tool_responses = await self._handle_model_response(model_response, run_context)
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 889, in _handle_model_response
    return await self._handle_text_response(text, run_context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 907, in _handle_text_response
    self._incr_result_retry(run_context)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/pydantic-ai/lib/python3.11/site-packages/pydantic_ai/agent.py", line 1082, in _incr_result_retry
    raise exceptions.UnexpectedModelBehavior(
pydantic_ai.exceptions.UnexpectedModelBehavior: Exceeded maximum retries (1) for result validation
```


Trying `llama3.2:3b`:

```shell
PYDANTIC_AI_MODEL=ollama:llama3.2:3b python examples/bank_support.py
```

It threw the same validation error.

### Comments on the Three Models so Far

When I "cheated" with the return typing while using `granite3-moe:3b` for the first example, it printed a nice answer. Most likely, this model is not powerful enough to use for structured output, although it's possible that a "stronger" prompt would have helped. 

Both `granite3-dense:8B` and `llama3.2:3B` worked for this simple task, but struggled for the more advanced `bank_support` example.

### Others

TODO.

