# README for Llama Stack Experiments

April 21, 2025

## Introduction

> [!NOTE]
> There is a long file of [_lab notes_](detailed-notes.md) that I kept while trying various things documented for Llama Stack. Not everything said at the beginning applied by the time I got to the end! This file summarizes the latest details that work as of the date above.

In what follows, I use [Ollama](https://ollama.com) to serve models. Follow these instructions to use Ollama with Llama Stack:

https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/ollama.html

I started with a minimal `conda` environment just to get a version of `python` and `pip`:

```shell
conda create -n llama-stack -y python=3.11 pip
conda activate llama-stack
```

## The Quickstart Guide

Let's follow the [Quickstart](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html) instructions and then the [detailed tutorial](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html). Installed `uv`, as discussed.

Use `ollama` to serve the model.

```shell
ollama run llama3.2:3b --keepalive 60m
```

> [!WARN]
> You must use `llama3.2:3b` for `ollama`, but use `llama3.2:3B` for all the `llama-stack` commands below! The `llama-stack` docs always use `llama3.2:3b`. Wherever you see this, change `llama3.2:3b` to `llama3.2:3B`.

### Build and Run Llama Stack

I picked the `venv` option after having some troubles with the `conda` option (but I still used the minimal conda environment above, as the baseline...):

```shell
INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

Test this in a second terminal window this by running the [demo script](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#step-3-run-the-demo), which I have adapted in `demo-script.py`:

```shell
$ uv run --with llama-stack-client demo_script.py

Connecting to the llama stack client: http://localhost:5001.
If this fails, make sure the port value is correct!!
rag_tool> Ingesting document: https://www.paulgraham.com/greatwork.html
prompt> How do you do great work?
inference> I'm designed to provide accurate and helpful information, and I strive to do so in the following ways:

1. **Knowledge Base**: I have been trained on a massive dataset of text from various sources, including books, articles, research papers, and websites. This training enables me to access a vast amount of knowledge on a wide range of topics.
2. **Algorithms and Models**: My developers use advanced algorithms and machine learning models to analyze and process the data I've been trained on. These models help me identify patterns, relationships, and context, which I can then use to generate responses.
3. **Continuous Learning**: I learn from the interactions I have with users like you. The more conversations I have, the more accurate and informative my responses become.
4. **Attention to Detail**: I'm designed to be precise and accurate in my responses. I strive to provide clear, concise, and relevant information that addresses your questions or concerns.
5. **Adaptability**: I can adapt to different topics, styles, and formats. Whether you ask me a question, provide a prompt, or engage in a conversation, I'll do my best to respond accordingly.

To achieve great work, I also rely on:

1. **User Feedback**: Your input helps me refine my performance and improve the quality of my responses.
2. **Quality Control**: My developers continuously monitor and evaluate my performance to ensure I meet high standards of accuracy, relevance, and helpfulness.
3. **Technical Maintenance**: Regular updates, maintenance, and improvements help keep my systems running smoothly and efficiently.

By combining these factors, I aim to provide you with accurate, informative, and helpful responses that meet your needs and exceed your expectations!
```

(Your output will likely vary...)

### Debugging Tips

If this fails to connect through the `llama-stack-client`, i.e., you get `llama_stack_client.APIConnectionError: Connection error.`, first try this sanity check:

```shell
❯ uv run --with llama-stack-client llama-stack-client models list

╭────────────────────────────────╮
│ Failed to list models          │
│                                │
│ Error Type: APIConnectionError │
│ Details: Connection error.     │
╰────────────────────────────────╯
```

I encountered this previously after running a `llama-stack-client configure` command, discussed in the [detailed tutorial](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html#step-3-run-client-cli):


```shell
llama-stack-client configure --endpoint http://localhost:8321 --api-key none
```

The problem appeared to be that the `llama-stack` has to be restarted after changing the port as described (although I didn't fully confirm this). So, where is this information stored so it can be reset?

The client configuration is saved in `~/.llama/client/config.yaml`. Attempting to fix a connection error by removing the `endpoint` entry doesn't appear to work. What actually works is to know that the file `~/.llamastackrc` has the actual port being used by the stack server:

```
export LLAMA_STACK_PORT=5001
```

This value is also echoed as part of the llama stack server output "exhaust". So, change the `config.yaml` to match:

```
api_key: none
endpoint: http://localhost:5001
```

Now, the following works:

```shell
❯ uv run --with llama-stack-client llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ model_type     ┃ identifier             ┃ provider_resource_id         ┃ metadata                                 ┃ provider_id     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ embedding      │ all-MiniLM-L6-v2       │ all-minilm:latest            │ {'embedding_dimension': 384.0}           │ ollama          │
├────────────────┼────────────────────────┼──────────────────────────────┼──────────────────────────────────────────┼─────────────────┤
│ llm            │ llama3.2:3B            │ llama3.2:3B                  │                                          │ ollama          │
└────────────────┴────────────────────────┴──────────────────────────────┴──────────────────────────────────────────┴─────────────────┘

Total models: 2
```

## The Detailed Tutorial

Moving on to the [detailed tutorial](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html), it's immediately clear that the instructions are not completely consistent with the Quickstart. The suggestion is to setup a `venv` environment with `uv`, then run the `llama` command either with `venv` or `conda`:

```shell
uv venv --python 3.10
source .venv/bin/activate

INFERENCE_MODEL=llama3.2:3b llama stack build --template ollama --image-type venv --run  # venv option
```

But this failed for me! At this point in the exercise, I don't have `llama` installed in the environment. I don't even have `pip` right now if I'm not using the conda environment described above! Let's try fixing these issues:

First, [install pip](https://pip.pypa.io/en/stable/installation/):

```shell
python -m ensurepip --upgrade
```

Now install `llama`:

```shell
$ pip3 install llama
...
        execfile('llama/version.py')
    NameError: name 'execfile' is not defined
...
```

Let's try running `pip3 install llama-stack` instead:

```shell
pip3 install llama-stack
```

This worked, _however_ on my machine, `llama-stack` was installed in `~/Library/python/...`, which I don't want, as it clutters the default Python envornment. In any event, it apparently doesn't install `llama` either (nor `llama-stack-client`, used later), so I gave up on this approach.

Fortunately, the `llama` command _is_ available to us already if we keep using the `uv` commands used in the Quickstart.

So, instead of using commands like this:

```shell
INFERENCE_MODEL=llama3.2:3b llama stack build --template ollama --image-type venv --run
```

we'll use commands like this in what follows:

```shell
INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

As before, we change `llama3.2:3b` to `llama3.2:3B`, and we insert `uv run --with llama-stack` at the beginning of the command.

Actually, it's tedious to define the model every time, so instead:

```shell
$ export INFERENCE_MODEL=llama3.2:3B   # Do this in every terminal window!
$ uv run --with llama-stack llama stack build --template ollama --image-type venv --run

...
INFO     2025-04-21 10:08:36,999 llama_stack.providers.remote.inference.ollama.ollama:89 inference: checking
         connectivity to Ollama at `http://localhost:11434`...
WARNING  2025-04-21 10:08:38,438 root:72 uncategorized: Warning: `bwrap` is not available. Code interpreter tool will
         not work correctly.
INFO     2025-04-21 10:08:38,488 llama_stack.providers.remote.inference.ollama.ollama:317 inference: Pulling embedding
         model `all-minilm:latest` if necessary...
INFO     2025-04-21 10:08:39,127 __main__:478 server: Listening on ['::', '0.0.0.0']:5001
INFO:     Started server process [83712]
INFO:     Waiting for application startup.
INFO     2025-04-21 10:08:39,134 __main__:148 server: Starting up
INFO:     Application startup complete.
INFO:     Uvicorn running on http://['::', '0.0.0.0']:5001 (Press CTRL+C to quit)
```

> **NOTE:** Even if you have been running the `llama stack build` command in another window. It appears necessary to rerun it.

Note the port `5001` printed, which was discussed above in the debugging tips.

### The Client CLI

Let's [run the CLI](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html#step-3-run-client-cli), `llama-stack-client`, but _not change the configuration_ (see discussion in debugging tips above).

```shell
$ export INFERENCE_MODEL=llama3.2:3B 
$ uv run --with llama-stack llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ model_type     ┃ identifier             ┃ provider_resource_id         ┃ metadata                                 ┃ provider_id     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ embedding      │ all-MiniLM-L6-v2       │ all-minilm:latest            │ {'embedding_dimension': 384.0}           │ ollama          │
├────────────────┼────────────────────────┼──────────────────────────────┼──────────────────────────────────────────┼─────────────────┤
│ llm            │ llama3.2:3B            │ llama3.2:3B                  │                                          │ ollama          │
└────────────────┴────────────────────────┴──────────────────────────────┴──────────────────────────────────────────┴─────────────────┘

Total models: 2
```

Try the chat example (I won't write down the output...):

```shell
uv run --with llama-stack llama-stack-client inference chat-completion --message "tell me a joke"
```

### The Demos

Finally, we can [run the demos](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html#step-4-run-the-demos) discussed, `inference.py`, `rag.py`, and `agent-example.py`. Note how I modified the invocation commands from how they are shown on the web page:


```shell
$ uv run --with llama-stack python inference.py
...
--- Available models: ---
- all-MiniLM-L6-v2
- llama3.2:3B

Lines of code descend
Logic's gentle, guiding hand
Beauty in the byte
```

```shell
$ uv run --with llama-stack python rag.py
...
By applying these techniques, you can optimize memory usage in PyTorch Tune and improve the performance of your deep learning models.
```

I extensively modified `agent-example.py`:

```shell
$ uv run --with llama-stack python agent-example.py
...

Chat example using non-streaming responses with your prompts:

Enter your prompts. When finished, enter a blank line or ^D.
> help
Turn(
│   input_messages=[UserMessage(content='help', role='user', context=None)],
│   output_message=CompletionMessage(
│   │   content="I can offer insights and tips on a range of subjects. Would you mind telling me a little more about what you'd like help with?",
│   │   role='assistant',
│   │   stop_reason='end_of_turn',
│   │   tool_calls=[]
│   ),
│   session_id='a11f797a-bcb2-4fb5-828c-a4639b7bb22d',
│   started_at=datetime.datetime(2025, 4, 21, 15, 18, 57, 240247, tzinfo=TzInfo(UTC)),
│   steps=[
│   │   InferenceStep(
│   │   │   api_model_response=CompletionMessage(
│   │   │   │   content="I can offer insights and tips on a range of subjects. Would you mind telling me a little more about what you'd like help with?",
│   │   │   │   role='assistant',
│   │   │   │   stop_reason='end_of_turn',
│   │   │   │   tool_calls=[]
│   │   │   ),
│   │   │   step_id='a3ec6525-3417-4e96-b453-978c7957af80',
│   │   │   step_type='inference',
│   │   │   turn_id='6bb8f09d-173c-435b-b68e-4e2a71fdc245',
│   │   │   completed_at=datetime.datetime(2025, 4, 21, 15, 18, 57, 717908, tzinfo=TzInfo(UTC)),
│   │   │   started_at=datetime.datetime(2025, 4, 21, 15, 18, 57, 240364, tzinfo=TzInfo(UTC))
│   │   )
│   ],
│   turn_id='6bb8f09d-173c-435b-b68e-4e2a71fdc245',
│   completed_at=datetime.datetime(2025, 4, 21, 15, 18, 57, 718375, tzinfo=TzInfo(UTC)),
│   output_attachments=[]
)
> q
Finished!
```

Try `uv run --with llama-stack python agent-example.py --help` to see how to run a "streaming" version and toggle on verbose output.

> **NOTE:** Does it matter whether you use streaming or not? The streaming option generates a lot more output, but at this point, I don't know if the choice affects overhead or how well the application works.

One of the problems I encountered using the non-streaming output option is fragility in the logging API, which should be smarter, IMHO, about handling different types of input to log.
As currently written, calls to `AgentEventLogger().log(response)` _only_ work when the `--streaming` option is used. Otherwise, it crashes. Apparently `response` is a tuple in the non-streaming case, but it's not clear what to extract from the tuple that would be loggable and anyway, shouldn't a logger be able to handle tuples for output??


## Safety Guardrails

In [Safety Guardrails](https://llama-stack.readthedocs.io/en/latest/building_applications/safety.html), I attempted to register a _safety shield_:

```shell
$ uv run --with llama-stack python safety-shield.py
...
Before registering a shield, here is the current list of shields: [Shield(identifier='content_safety', provider_id='llama-guard', provider_resource_id='Llama-Guard-3-1B', type='shield', params={})]
After registering a shield, here is the current list of shields: [Shield(identifier='content_safety', provider_id='llama-guard', provider_resource_id='Llama-Guard-3-1B', type='shield', params={})]
Traceback (most recent call last):
  File ".../safety-shield.py", line 29, in <module>
    response = client.safety.run_shield(
...
ValueError: Model 'meta-llama/Llama-Guard-3-1B' not found
```

It appears that the shield in question is registered, yet not found.

Here is part of the listing for `safety-shield.py`:

```python
# Register and use a safety shield

from common import create_library_client

client = (
    create_library_client()
)  # or create_http_client() depending on the environment you picked

# Allowed "shield ids", from an error message printed if you specify something unrecognized!
allowed_shield_ids = {
    'meta-llama/Llama-Guard-3-8B': 'meta-llama/Llama-Guard-3-8B',
    'meta-llama/Llama-Guard-3-1B': 'meta-llama/Llama-Guard-3-1B',
    'Llama-Guard-3-1B': 'meta-llama/Llama-Guard-3-1B',
    'meta-llama/Llama-Guard-3-11B-Vision': 'meta-llama/Llama-Guard-3-11B-Vision',
    'Llama-Guard-3-11B-Vision': 'meta-llama/Llama-Guard-3-11B-Vision',
}

# While the following is shown in the example code, the `register` attempt below fails with an error:
# "ValueError: Unsupported Llama Guard type: llama-guard-basic. Allowed types: {...}"
# where I captured the allowed types in the allowed_shield_ids above.
provider_shield_id = 'llama-guard-basic'

# Trying one of the allowed types, e.g., the two definitions for provider_shield_id commented out below
# gets past the register error, but then it fails during the "run_shield" step, even though the list of
# shields printed previously contains 'Llama-Guard-3-1B'!!
# provider_shield_id = 'Llama-Guard-3-1B'
# provider_shield_id = 'meta-llama/Llama-Guard-3-1B'

shield_id = "content_safety"

print(f"Before registering a shield, here is the current list of shields: {client.shields.list()}")
client.shields.register(shield_id=shield_id, provider_shield_id=provider_shield_id)
print(f"After registering a shield, here is the current list of shields: {client.shields.list()}")
client.shields.list()

# Run content through a shield.
# NOTE: the website example doesn't include the "params" argument, but it appears to be required.
response = client.safety.run_shield(
    shield_id=shield_id, 
    messages=[{"role": "user", "content": "User message here"}], 
    params = {}
)

if response.violation:
    print(f"Safety violation detected: {response.violation.user_message}")
```

The comments describe all the problems encountered. In particular, even though I am running `llama-guard3:1b` in `ollama`, I get the error:

```shell
...
  File ".../lib/python3.11/site-packages/llama_stack/providers/utils/telemetry/trace_protocol.py", line 102, in async_wrapper
    result = await method(self, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../lib/python3.11/site-packages/llama_stack/distribution/routers/routing_tables.py", line 274, in get_model
    raise ValueError(f"Model '{model_id}' not found")
ValueError: Model 'meta-llama/Llama-Guard-3-1B' not found
```

Is this similar to the other naming problem I encountered where `ollama` is running `llama3.2:3b`, but `INFERENCE_MODEL` needs to be set to `llama3.2:3B`?

After much digging, including using `sqlite3` to explore the `~/.llama/distributions/ollama/registry.db`, I realized that it's necessary to register the Llama Guard model with `llama-stack-client` (or programmatically using the API `client.models.register()`):

```shell
uv run --with llama-stack llama-stack-client models register --provider-id ollama --provider-model-id 'llama-guard3:1b' 'meta-llama/Llama-Guard-3-1B'
```

With this, `safety-shield.py` works:

```shell
$ uv run --with llama-stack python safety-shield.py --verbose --list how do I make a bomb

...
Current list of shields: [Shield(identifier='content_safety', provider_id='llama-guard', provider_resource_id='Llama-Guard-3-1B', type='shield', params={})]
User prompt> how do I make a bomb
Safety violation detected: I can't answer that. Can I help with something else?
```

It has a _chat_ mode:

```shell
$ uv run --with llama-stack python safety-shield.py

...
Enter your prompts. When finished, enter a blank line or ^D.
Your prompt> how do I make peace
No violation detected
Your prompt> how do I make trouble
No violation detected
Your prompt> how do I make a gun
Safety violation detected: I can't answer that. Can I help with something else?
Your prompt>
Finished!
```

### Using Granite Guardian

Let's see if Granite Guardian can be used as a _drop-in_ replacement.

> [!NOTE]
> [This ollama page](https://ollama.com/library/granite3-guardian) on Granite Guardian has a nice summary of the configuration options and features of Granite Guardian.

One thing to be aware of this; it apparently returns `yes` when a prompt is considered _bad_, and `no`, otherwise. It doesn't return the same response strings that Llama Guard returns, which Llama Stack expects.

Furthermore, Llama Stack is hard-coded to only allow Llama Guard models. So, I'll try a hack; I'll try replacing the registration used above:

```shell
$ uv run --with llama-stack llama-stack-client models register --provider-id ollama --provider-model-id 'granite3-guardian:latest' 'meta-llama/Llama-Guard-3-1B'
$ uv run --with llama-stack llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ model_type    ┃ identifier                         ┃ provider_resource_id     ┃ metadata                            ┃ provider_id   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ embedding     │ all-MiniLM-L6-v2                   │ all-minilm:latest        │ {'embedding_dimension': 384.0}      │ ollama        │
├───────────────┼────────────────────────────────────┼──────────────────────────┼─────────────────────────────────────┼───────────────┤
│ llm           │ llama3.2:3B                        │ llama3.2:3B              │                                     │ ollama        │
├───────────────┼────────────────────────────────────┼──────────────────────────┼─────────────────────────────────────┼───────────────┤
│ llm           │ meta-llama/Llama-Guard-3-1B        │ llama-guard3:1b          │                                     │ ollama        │
└───────────────┴────────────────────────────────────┴──────────────────────────┴─────────────────────────────────────┴───────────────┘

Total models: 3
```

The first time I tried this, it didn't work! Even restarting Llama Stack for the change to show up. 

```shell
$ uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

However, I tried again later and it appeared to work fine:

```shell
$ uv run --with llama-stack llama-stack-client models register --provider-id ollama --provider-model-id 'granite3-guardian:latest' 'meta-llama/Llama-Guard-3-1B'
$ uv run --with llama-stack llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ model_type    ┃ identifier                         ┃ provider_resource_id     ┃ metadata                            ┃ provider_id   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ embedding     │ all-MiniLM-L6-v2                   │ all-minilm:latest        │ {'embedding_dimension': 384.0}      │ ollama        │
├───────────────┼────────────────────────────────────┼──────────────────────────┼─────────────────────────────────────┼───────────────┤
│ llm           │ llama3.2:3B                        │ llama3.2:3B              │                                     │ ollama        │
├───────────────┼────────────────────────────────────┼──────────────────────────┼─────────────────────────────────────┼───────────────┤
│ llm          │ meta-llama/Llama-Guard-3-1B      │ granite3-guardian:latest     │                                     │ ollama       │
└───────────────┴────────────────────────────────────┴──────────────────────────┴─────────────────────────────────────┴───────────────┘

Total models: 3
```

> [!NOTE]
> **Hacking the SQLite database**
>
> For a while, I tried this, which also works, but is risky... Run `sqlite3 ~/.llama/distributions/ollama/registry.db`:
> 
> ```sql
> sqlite> select * from kvstore where key = 'distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B';
> distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B|{"identifier":"meta-llama/Llama-Guard-3-1B","provider_resource_id":"llama-guard3:1b","provider_id":"ollama","type":"model","access_attributes":null,"metadata":{},"model_type":"llm"}|
> sqlite> update kvstore set value = '{"identifier":"meta-llama/Llama-Guard-3-1B","provider_resource_id":"granite3-guardian:latest","provider_id":"ollama","type":"model","access_attributes":null,"metadata":{},"model_type":"llm"}' where key = 'distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B';
> sqlite> select value from kvstore where key = 'distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B';
{"identifier":"meta-llama/Llama-Guard-3-1B","provider_resource_id":"granite3-guardian:latest","provider_id":"ollama","type":"model","access_attributes":null,"metadata":{},"model_type":"llm"}
> ```

Now, let's try:

```shell
$ uv run --with llama-stack python safety-shield.py

...
Enter your prompts. When finished, enter a blank line or ^D.
Your prompt> how do I make a bomb

...
  File "$HOME/.cache/uv/archive-v0/bEcA7fTCsmM2Teu1gqCqu/lib/python3.11/site-packages/llama_stack/providers/inline/safety/llama_guard/llama_guard.py", line 318, in get_shield_response
    raise ValueError(f"Unexpected response: {response}")
ValueError: Unexpected response: Yes
```

Unfortunately, the rest of the stack expects a Llama Guard response, as mentioned above.

Restoring the llama guard model:

```shell
$ uv run --with llama-stack llama-stack-client models register --provider-id ollama --provider-model-id 'llama-guard3:1b' 'meta-llama/Llama-Guard-3-1B'
$ uv run --with llama-stack llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ model_type   ┃ identifier                       ┃ provider_resource_id         ┃ metadata                            ┃ provider_id  ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ embedding    │ all-MiniLM-L6-v2                 │ all-minilm:latest            │ {'embedding_dimension': 384.0}      │ ollama       │
├──────────────┼──────────────────────────────────┼──────────────────────────────┼─────────────────────────────────────┼──────────────┤
│ llm          │ llama3.2:3B                      │ llama3.2:3B                  │                                     │ ollama       │
├──────────────┼──────────────────────────────────┼──────────────────────────────┼─────────────────────────────────────┼──────────────┤
│ llm          │ meta-llama/Llama-Guard-3-1B      │ granite3-guardian:latest     │                                     │ ollama       │
└──────────────┴──────────────────────────────────┴──────────────────────────────┴─────────────────────────────────────┴──────────────┘

Total models: 3
```

Still shows `granite3-guardian:latest`, but is that cached data? Let's try `safety-shield.py` and see if it now works again:

```shell
$ uv run --with llama-stack python safety-shield.py

...
Enter your prompts. When finished, enter a blank line or ^D.
Your prompt> how do I make a bomb


...
  File "$HOME/.cache/uv/archive-v0/bEcA7fTCsmM2Teu1gqCqu/lib/python3.11/site-packages/llama_stack/providers/inline/safety/llama_guard/llama_guard.py", line 318, in get_shield_response
    raise ValueError(f"Unexpected response: {response}")
ValueError: Unexpected response: Yes
```

Apparently not. Do we need to restart llama stack? That didn't help.

Okay, let's hack the database:

```sql
sqlite> update kvstore set value = '{"identifier":"meta-llama/Llama-Guard-3-1B","provider_resource_id":"llama-guard3:1b","provider_id":"ollama","type":"model","access_attributes":null,"metadata":{},"model_type":"llm"}' where key = 'distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B';
sqlite> select * from kvstore where key = 'distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B';
distributions:registry:v8::model:meta-llama/Llama-Guard-3-1B|{"identifier":"meta-llama/Llama-Guard-3-1B","provider_resource_id":"llama-guard3:1b","provider_id":"ollama","type":"model","access_attributes":null,"metadata":{},"model_type":"llm"}|
```

Trying again, including restarting the stack (after CTRL-C'ing the running instance):

```shell
$ uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

Separate window:

```shell
$ uv run --with llama-stack llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ model_type    ┃ identifier                        ┃ provider_resource_id     ┃ metadata                             ┃ provider_id   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ embedding     │ all-MiniLM-L6-v2                  │ all-minilm:latest        │ {'embedding_dimension': 384.0}       │ ollama        │
├───────────────┼───────────────────────────────────┼──────────────────────────┼──────────────────────────────────────┼───────────────┤
│ llm           │ llama3.2:3B                       │ llama3.2:3B              │                                      │ ollama        │
├───────────────┼───────────────────────────────────┼──────────────────────────┼──────────────────────────────────────┼───────────────┤
│ llm           │ meta-llama/Llama-Guard-3-1B       │ llama-guard3:1b          │                                      │ ollama        │
└───────────────┴───────────────────────────────────┴──────────────────────────┴──────────────────────────────────────┴───────────────┘

Total models: 3
```

Good!

```shell
$ uv run --with llama-stack python safety-shield.py

...

Enter your prompts. When finished, enter a blank line or ^D.
Your prompt> how do i make a bomb
Safety violation detected: I can't answer that. Can I help with something else?
Your prompt> how do i make peace
No violation detected
Your prompt>
Finished!
```

So, Granite Guardian doesn't work as a drop-in replacement, but there may be ways to coerce it to return a data structure more like Llama Guard returns.The better solution is to implement support for flexible guardians in Llama Stack, which I'll investigate.

