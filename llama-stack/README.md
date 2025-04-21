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

I decided to try the [getting started](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html) instructions again, using the conda options.

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

Now the [detailed tutorial](https://llama-stack.readthedocs.io/en/latest/getting_started/detailed_tutorial.html) recommends one of these commands for running the stack with `venv` or `conda`:

```shell
INFERENCE_MODEL=llama3.2:3b llama stack build --template ollama --image-type venv --run  # venv
INFERENCE_MODEL=llama3.2:3b llama stack build --template ollama --image-type conda  --image-name llama3-3b-conda --run  # conda
```