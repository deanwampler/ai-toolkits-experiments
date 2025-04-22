# README for Llama Stack Experiments

> **NOTE:** This is a long file of _lab notes_. Not everything said at the beginning applied by the time I got to the end!

Following these instructions for use with Ollama:

https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/ollama.html

Here are a few observations.

I started with a conda environment:

```shell
conda create -n llama-stack -y python=3.11 pip
conda activate llama-stack
```

However, it appears that when I ran the recommended `uv` setup command discussed below, it used Python 3.10.

> **NOTE:** Some of the scripts mentioned going forward, such as `./.setup.sh` have been moved to the `old` directory, because ultimately I decided not to use them.

Next, I created a `./.setup.sh` script to set the environment variables, verify the conda environment is working, etc.:

```shell
SETUP_SCRIPT=$0

export LLAMA_STACK_PORT=5001

# ollama names this model differently, and we must use the ollama name when loading the model
export OLLAMA_INFERENCE_MODEL="llama3.2:3b"
export INFERENCE_MODEL=$OLLAMA_INFERENCE_MODEL
# export INFERENCE_MODEL="meta-llama/Llama-3.2-3B"

export OLLAMA_SAFETY_MODEL="llama-guard3:1b"
export SAFETY_MODEL="meta-llama/Llama-Guard-3-1B"
# export SAFETY_MODEL=$OLLAMA_SAFETY_MODEL
...
```

This script is used by the `run-model.sh` and `run-stack.sh` scripts. You don't use it by itself.

The different definitions of the `*_MODEL` variables, some commented out and others used, as well as the use of `PATH_TO_YAMLS`, are explained below.

I then defined a script `run-model.sh` to run the inference and optionally the safety models in Ollama. See `run-model.sh --help` for instructions on how to use it.

Then, I adapted and the commands from the [Via Conda](https://llama-stack.readthedocs.io/en/latest/distributions/self_hosted_distro/ollama.html#via-conda) section:

```shell
uv pip install llama-stack

llama stack build --template ollama --image-type conda

llama stack run ./run.yaml \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env OLLAMA_URL=http://localhost:11434

# also tried
llama stack run ./run-with-safety.yaml \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env SAFETY_MODEL=$SAFETY_MODEL \
  --env OLLAMA_URL=http://localhost:11434
```

First, the "stack build" didn't generate the required yaml files that the instructions said would be generated, at least, assuming they would have been written in the current directory, as implied by the two `llama stack` commands. 

However, I found them in `$CONDA_PREFIX/lib/python3.10/site-packages/llama_stack/templates/ollama`. That's why `PATH_TO_YAMLS` is defined in `./.setup.sh` to use this path, which I then used in another script `run-stack.sh` that executes the two `llama stack run ...` commands above, e.g., `llama stack run $PATH_TO_YAMLS/run.yaml ...`.

Also, note how `INFERENCE_MODEL` and `SAFETY_MODEL` are defined in `./.setup.sh` and the commented-out lines. The instructions say that `INFERENCE_MODEL="meta-llama/Llama-3.2-3B"` should be correct (for the model I'm using), but I got an error that only the Ollama name, `llama-guard3:1b` was available. That wasn't the case for the safety model, where the Llama name shown worked as specified.

With these changes, my `run-stack.sh --safety` script worked. (The `--safety` option tells it to use both the inference and safety models. Try `run-shack.sh --help`.) It then waited for some other processes to use the stack.

With the runtime environment working using Ollama, I next visited the [Quick Start](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#run-inference-with-python-sdk) page and tried the inference example shown.

```shell
. .setup.sh
python inference.py > inference.log
```

(Some details were changed in the copy of `inference.log` you will find in this repo to protect the innocent...)

It worked, printing out a lot YAML information, ending with this:

```
...

--- Available models: ---
- all-MiniLM-L6-v2
- llama-guard3:1b
- llama3.2:3b
- meta-llama/Llama-Guard-3-1B

Here is a haiku about coding:

Lines of code unfold
Logic's gentle, secret dance
Beauty in the bits
```

Incidentally, the log mentions providers available, including one for Model Context Protocol, which we have been discussing in $THE_DAY_JOB.

Next, I tried the [RAG example](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html#your-first-rag-agent). 

```shell
python rag.py > rag.log
```

More long output, ending with...

```
...
User> How to optimize memory usage in torchtune? use the knowledge_search tool to get information.
inference> [knowledge_search(query="torchtune memory optimization")]"
```

Unfortunately, the Quick Start guide doesn't tell you what the output should be, so I assume both runs succeeded, because no errors were mentioned and the output seems reasonable...

## The CLI Client

(April 15, 2025)

https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html#step-3-run-client-cli

```shell
$ llama-stack-client -h
Usage: llama-stack-client [OPTIONS] COMMAND [ARGS]...

  Welcome to the llama-stack-client CLI - a command-line interface for
  interacting with Llama Stack

Options:
  -h, --help       Show this message and exit.
  --version        Show the version and exit.
  --endpoint TEXT  Llama Stack distribution endpoint
  --api-key TEXT   Llama Stack distribution API key
  --config TEXT    Path to config file

Commands:
  configure          Configure Llama Stack Client CLI.
  datasets           Manage datasets.
  eval               Run evaluation tasks.
  eval_tasks         Manage evaluation tasks.
  inference          Inference (chat).
  inspect            Inspect server configuration.
  models             Manage GenAI models.
  post_training      Post-training.
  providers          Manage API providers.
  scoring_functions  Manage scoring functions.
  shields            Manage safety shield services.
  toolgroups         Manage available tool groups.
  vector_dbs         Manage vector databases.

$ llama-stack-client configure --endpoint http://localhost:8321 --api-key none
Done! You can now use the Llama Stack Client CLI with endpoint http://localhost:8321
```

But some subsequent commands didn't work:

```shell
$ llama-stack-client shields list
╭────────────────────────────────╮
│ Failed to list shields         │
│                                │
│ Error Type: APIConnectionError │
│ Details: Connection error.     │
╰────────────────────────────────╯

$ llama-stack-client models list
╭────────────────────────────────╮
│ Failed to list models          │
│                                │
│ Error Type: APIConnectionError │
│ Details: Connection error.     │
╰────────────────────────────────╯
```

## Restarting

(April 15, 2025)

I decided to try the [detailed tutorial](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html) instructions again, using the conda options.

I got the same connection errors afterwards, but I noticed that I can't ping any of `localhost`, `127.0.0.1` or the actual IP address of my laptop.

So, I switched to my home Mac.

```shell
$ conda env create -f llama-stack.yaml
$ conda activate llama-stack
$ INFERENCE_MODEL=llama3.2:3b llama stack build --template ollama --image-type conda  --image-name llama3-3b-conda --run 
```

But the last command fails because `llama` isn't installed already. So, I'll switch to the [Quickstart](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html) instructions that use `uv` instead for this step (also available on the detailed tutorial page...).

```shell
INFERENCE_MODEL=llama3.2:3b uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

But the model is actually `llama3.2:3B`:

```shell
INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

> **NOTE:** The quick start and detailed tutorial pages should be consistent about how to run the stack!

Since we're on the quick start page, let's try the demo shown. See `demo_script.py` in this directory.

```shell
$ uv run --with llama-stack-client demo_script.py

Installed 32 packages in 137ms
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

Looks good. 

Back to the CLI commands:

```shell
yes | conda create -n stack-client python=3.10
conda activate stack-client
pip install llama-stack-client
llama-stack-client configure --endpoint http://localhost:8321 --api-key none
```

Try the CLI commands that failed before:

```shell
$ llama-stack-client models list

Available Models

┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ model_type     ┃ identifier             ┃ provider_resource_id         ┃ metadata                                 ┃ provider_id     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ llm            │ llama3.2:3B            │ llama3.2:3B                  │                                          │ ollama          │
├────────────────┼────────────────────────┼──────────────────────────────┼──────────────────────────────────────────┼─────────────────┤
│ embedding      │ all-MiniLM-L6-v2       │ all-minilm:latest            │ {'embedding_dimension': 384.0}           │ ollama          │
└────────────────┴────────────────────────┴──────────────────────────────┴──────────────────────────────────────────┴─────────────────┘

Total models: 2

$ llama-stack-client shields list
(nothing...)
```

Success!! So, it may be the network configuration of my work laptop is incompatible with this CLI!!

## Looking at Safety Support

(April 15, 2025)

https://llama-stack.readthedocs.io/en/latest/building_applications/safety.html#safety-guardrails

Let's try the code shown in this section, captured in `register-safety-shield.py` with lots of corrections to make it work!!

```shell
$ python register-safety-shield.py
Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/llama-stack/register-safety-shield.py", line 6, in <module>
    create_library_client()
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/llama-stack/common.py", line 18, in create_library_client
    from llama_stack import LlamaStackAsLibraryClient
ModuleNotFoundError: No module named 'llama_stack'
```

Hmm. Using `uv` earlier probably means it's not installed in the Conda environment. So, let's try this:

```shell
$ INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack python register-safety-shield.py

No module named 'aiosqlite'
Using llama-stack as a library requires installing dependencies depending on the template (providers) you choose.

Please run:

llama stack build --template ollama --image-type venv


Traceback (most recent call last):
...
```

Okay...

```shell
❯ llama stack build --template ollama --image-type venv

zsh: command not found: llama
```

How about this?

```shell
❯ uv run --with llama-stack llama stack build --template ollama --image-type venv

...
Build Successful!
```

Trying again with the the register script:

```shell
$ INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack python register-safety-shield.py

...
ValueError: Model 'meta-llama/Llama-Guard-3-1B' not found
```

The real name appears to be `llama-guard3:1b`, at least in `ollama`, but the API hard-codes the allowed values. See the `allowed_shield_ids` in `register-safety-shield.py`, which was taken from an error message of the allowed ids.

I'll come back to this issue later.

## Retrying the Examples from the Detailed Tutorial

```shell
$ INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack python inference.py

...
--- Available models: ---
- all-MiniLM-L6-v2
- llama3.2:3B

Lines of code descend
Logic's gentle, guiding hand
Beauty in the byte
```

```shell
$ INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack python rag.py

...
User> How to optimize memory usage in torchtune? use the knowledge_search tool to get information.
inference> To optimize memory usage in PyTorch Tune, you can try the following:
...
```

Note that previously when I had everything installed in the conda environment, it was sufficient to run just `python rag.py`, etc.

## Trying the Agents Example

https://llama-stack.readthedocs.io/en/latest/building_applications/agent.html

See `agent-example.py`, which fixes some bugs in the example.

```shell
INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack python agent-example.py
```

## New Trials...

(April 21, 2025)

Picking up again on Monday, I ran into new problems which _may_ be due to the discovery that I needed to upgraded `miniforge`, which appeared to wipe out my existing environments. So, first, I recreated the `llama-stack` conda environment:

```shell
cd [root of this repo]
conda env create --name llama-stack --file llama-stack/llama-stack-conda.yaml
conda activate llama-stack
```

Then I attempted to run the same command I had used previously above:

```shell
$ INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack llama stack build --template ollama --image-type venv --run

Error building stack: Please specify an image name when building a venv image
```

Okay. Something I missed has changed. Since I've been using `conda`, let's try the `conda` alternative.

```shell
INFERENCE_MODEL=llama3.2:3B llama stack build --template ollama --image-type conda  --image-name llama3-3b-conda --run
```

> **NOTE:** As before, you have to use `llama3.2:3B`, not `llama3.2:3b`, as documented.

Of course, this creates yet another `conda` environment, `llama3-3b-conda`..., but it appears to work.

Sanity check: verify the examples still work...


```shell
$ INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack python inference.py

Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/llama-stack/inference.py", line 7, in <module>
    create_library_client()
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/llama-stack/common.py", line 21, in create_library_client
    client.initialize()
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/library_client.py", line 139, in initialize
    return asyncio.run(self.async_client.initialize())
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/asyncio/runners.py", line 44, in run
    return loop.run_until_complete(main)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/asyncio/base_events.py", line 649, in run_until_complete
    return future.result()
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/library_client.py", line 209, in initialize
    self.impls = await construct_stack(self.config, self.custom_provider_registry)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/stack.py", line 220, in construct_stack
    dist_registry, _ = await create_dist_registry(run_config.metadata_store, run_config.image_name)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/store/registry.py", line 191, in create_dist_registry
    await dist_registry.initialize()
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/store/registry.py", line 136, in initialize
    await self._ensure_initialized()
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/store/registry.py", line 126, in _ensure_initialized
    objects = _parse_registry_values(values)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/llama_stack/distribution/store/registry.py", line 50, in _parse_registry_values
    obj = pydantic.TypeAdapter(RoutableObjectWithProvider).validate_json(value)
  File "/opt/homebrew/Caskroom/miniforge/base/envs/llama-stack/lib/python3.10/site-packages/pydantic/type_adapter.py", line 446, in validate_json
    return self.validator.validate_json(
pydantic_core._pydantic_core.ValidationError: 1 validation error for tagged-union[Model,Shield,VectorDB,Dataset,ScoringFn,Benchmark,Tool,ToolGroup]
scoring_function.params.basic.aggregation_functions.0
  Input should be 'average', 'median', 'categorical_count' or 'accuracy' [type=enum, input_value='weighted_average', input_type=str]
    For further information visit https://errors.pydantic.dev/2.10/v/enum
```

Okay...

## Starting Over

Let's start over with the [Quickstart](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html) instructions and then the [detailed tutorial](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html), this time not using `conda`:

From the Quickstart, I have `uv` installed and I minimal `conda` environment just with Python 3.11 and `pip`:

```shell
ollama run llama3.2:3b --keepalive 60m
```

Again, change `llama3.2:3b` to `llama3.2:3B`:

```shell
INFERENCE_MODEL=llama3.2:3B uv run --with llama-stack llama stack build --template ollama --image-type venv --run
```

Run the demo script:

```shell
$ uv run --with llama-stack-client demo_script.py

Installed 31 packages in 89ms
Traceback (most recent call last):
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_transports/default.py", line 101, in map_httpcore_exceptions
    yield
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_transports/default.py", line 250, in handle_request
    resp = self._pool.handle_request(req)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 256, in handle_request
    raise exc from None
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_sync/connection_pool.py", line 236, in handle_request
    response = connection.handle_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 101, in handle_request
    raise exc
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 78, in handle_request
    stream = self._connect(request)
             ^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_sync/connection.py", line 124, in _connect
    stream = self._network_backend.connect_tcp(**kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_backends/sync.py", line 207, in connect_tcp
    with map_exceptions(exc_map):
  File "/opt/homebrew/Caskroom/miniforge/base/envs/python-311/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpcore/_exceptions.py", line 14, in map_exceptions
    raise to_exc(exc) from exc
httpcore.ConnectError: [Errno 61] Connection refused

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 953, in _request
    response = self._client.send(
               ^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_client.py", line 914, in send
    response = self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_client.py", line 942, in _send_handling_auth
    response = self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_client.py", line 979, in _send_handling_redirects
    response = self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_client.py", line 1014, in _send_single_request
    response = transport.handle_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_transports/default.py", line 249, in handle_request
    with map_httpcore_exceptions():
  File "/opt/homebrew/Caskroom/miniforge/base/envs/python-311/lib/python3.11/contextlib.py", line 158, in __exit__
    self.gen.throw(typ, value, traceback)
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ConnectError: [Errno 61] Connection refused

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/llama-stack/demo_script.py", line 6, in <module>
    models = client.models.list()
             ^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/resources/models.py", line 93, in list
    return self._get(
           ^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 1171, in get
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 917, in request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 977, in _request
    return self._retry_request(
           ^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 1054, in _retry_request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 977, in _request
    return self._retry_request(
           ^^^^^^^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 1054, in _retry_request
    return self._request(
           ^^^^^^^^^^^^^^
  File "/Users/deanwampler/.cache/uv/archive-v0/0pH67HMgHBF4_guS-NIJg/lib/python3.11/site-packages/llama_stack_client/_base_client.py", line 987, in _request
    raise APIConnectionError(request=request) from err
llama_stack_client.APIConnectionError: Connection error.
```

If fails to connect to the client.

```shell
❯ uv run --with llama-stack-client llama-stack-client models list

╭────────────────────────────────╮
│ Failed to list models          │
│                                │
│ Error Type: APIConnectionError │
│ Details: Connection error.     │
╰────────────────────────────────╯
```

I had previously run a `llama-stack-client` config. command. Where is this information stored so I can reset it?

I found it in `~/.llama/client/config.yaml`. I removed the `endpoint` entry, but it still failed. What actually worked was to notice the file `~/.llamastackrc`, which has the following:

```
export LLAMA_STACK_PORT=5001
```

This value is also echoed as part of the llama stack server output "exhaust". I then changed the `config.yaml` as follows:

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

> **NOTE:** Make sure all this is in the docs! I suspect the page that tells you how to use the following `llama-stack-client configure` command should also tell you to restart the stack!!

```shell
llama-stack-client configure --endpoint http://localhost:8321 --api-key none
```

Now, does the demo script work:

```shell
$ uv run --with llama-stack-client demo_script.py
```

NO! Same error as before!! However, `demo_script.py` hard-coded the wrong port for the server. Changing the value to `5001` worked.

Let's confirm the [other examples](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html#step-4-run-the-demos) work: `inference.py`, `rag.py`, and `agent-example.py`. (Note how I modified the invocation commands from how they are shown on the web page.)

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
>
Finished!
```

Try `uv run --with llama-stack python agent-example.py --help` to see how to run a "streaming" version and toggle on verbose output.

One of the problems I encountered using the non-streaming output option is fragility in the logging API, which should be smarter, IMHO, about handling different types of input to log.
A call to to `AgentEventLogger().log(response)` _only_ works when the `--streaming` option is used. Otherwise, it crashes. Apparently `response` is a tuple in the non-streaming case, but it's not clear what to extract from the tuple that is loggable and anyway, shouldn't a logger be more resilient??


## Safety Guardrails - Revisited

In [Safety Guardrails](https://llama-stack.readthedocs.io/en/latest/building_applications/safety.html), I attempted to register a _safety shield_:

```shell
$ uv run --with llama-stack python safety-shield.py
...
Before registering a shield, here is the current list of shields: [Shield(identifier='content_safety', provider_id='llama-guard', provider_resource_id='Llama-Guard-3-1B', type='shield', params={})]
After registering a shield, here is the current list of shields: [Shield(identifier='content_safety', provider_id='llama-guard', provider_resource_id='Llama-Guard-3-1B', type='shield', params={})]
Traceback (most recent call last):
  File "/Users/deanwampler/projects/ai/ai-toolkits-experiments/llama-stack/safety-shield.py", line 29, in <module>
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

One thing to be aware of is it apparently returns `yes` when a prompt is considered _bad_, and `no`, otherwise. It doesn't return a `response` object that Llama Guard returns.

First, I'll try a hack; Llama Stack is hard-coded to only allow Llama Guard models. So, I'll try replacing the registration used above:

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

Now, when you try
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

```shell
$ uv run --with llama-stack python safety-shield.py

...
Enter your prompts. When finished, enter a blank line or ^D.
Your prompt> how do I make a bomb

...
  File "/Users/deanwampler/.cache/uv/archive-v0/bEcA7fTCsmM2Teu1gqCqu/lib/python3.11/site-packages/llama_stack/providers/inline/safety/llama_guard/llama_guard.py", line 318, in get_shield_response
    raise ValueError(f"Unexpected response: {response}")
ValueError: Unexpected response: Yes
```

Unfortunately, the rest of the stack expects a Llama Guard response.

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
  File "/Users/deanwampler/.cache/uv/archive-v0/bEcA7fTCsmM2Teu1gqCqu/lib/python3.11/site-packages/llama_stack/providers/inline/safety/llama_guard/llama_guard.py", line 318, in get_shield_response
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

So, Granite Guardian doesn't work as a drop-in replacement, but there may be ways to coerce it to return a data structure more like Llama Guard returns.
