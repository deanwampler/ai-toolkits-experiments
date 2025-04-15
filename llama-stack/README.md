# README for Llama Stack Experiments

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


