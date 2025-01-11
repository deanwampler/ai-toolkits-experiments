# README for Tape Agents

[TapeAgents](https://github.com/ServiceNow/TapeAgents?tab=readme-ov-file) is a framework from ServiceNow that facilitates all stages of the LLM Agent development lifecycle.

[arxiv:2412.08445](https://arxiv.org/abs/2412.08445) paper.

Here's a quote from the README:

> **TapeAgents** is a framework that leverages a structured, replayable log (**Tape**) of the agent session to facilitate all stages of the LLM Agent development lifecycle. In TapeAgents, the agent reasons by processing the tape and the LLM output to produce new thoughts, actions, control flow steps and append them to the tape. The environment then reacts to the agent’s actions by likewise appending observation steps to the tape.

## Trying the Example Notebook

In order to try their recommended example notebook, [`intro.ipynb`](https://github.com/ServiceNow/TapeAgents/blob/main/intro.ipynb), I first installed Tape Agents:

```shell
pip install TapeAgents jupyterlab
```

I then downloaded the `intro.ipynb` and tried it out, but immediately ran into problems with the first code cell, where I commented out the OpenAI code and uncommented the code to use cached data. It couldn't find the path for variable `llm_cache_path`, which is `../tests/res/intro_notebook/tapedata.sqlite`.

Trying again with cloning the repo and using its setup instructions.

```shell
git clone git@github.com:ServiceNow/TapeAgents.git TapeAgents-git
cd TapeAgents-git
make setup
```

I activated the `tapeagents` conda environment this process created and then installed Jupyter Lab, which I use:

```shell
conda activate tapeagents
pip install jupyterlab
```

> **Note:** Unlike some of the other projects in this repo, I don't include the `TapeAgents` repo as a submodule, since it's better just to clone if you try it. However, I did save my edits to `./TapeAgents-git/intro.ipynb` to `./intro.ipynb` (see below).

Now running `intro.ipynb` in Juypter Lab, the path problem above still exists. Now it's clear that there is a typo in the path; it should be:
`tests/examples/res/intro_notebook/tapedata.sqlite`.

One cell makes this interesting comment:

> The main new thing in this example is the environment. In TapeAgents framework the environment responds to the agent `Action` steps with `Observation` steps. We expect you to use the environment to encapsulate tool use, retrieval, code execution: everything that is non-deterministic, non-stationary, or computationally heavy. On the contrary, we encourage you to implements the agent's deterministic decision-making in `make_prompt` and `generate_steps` methods.

I stopped about half-way down when it appeared I really needed to use an OpenAI account.

Here is a summary of the changes I made to `intro.ipynb`. First, I commented out the use of `OPENAI_API_KEY` near the top and un-commented the alternative code for reading model results from a local cache.

```
# Now set the OPENAI_API_KEY environment variable to your API key.

# import os
# 
# if "OPENAI_API_KEY" not in os.environ:
#     os.environ["OPENAI_API_KEY"] = "<your-api-key>"
#     # os.environ["OPENAI_ORGANIZATION"] = "" # optional

# If you prefer to skip the OpenAI setup and not make any LLM calls, you can use ones from the cache.
# It will work instead of the real LLM fine as long as the prompts are not changed.
# Uncomment the following lines to use the cache:

from tapeagents import llms
import os

# DeanW: 
# Bug: the path had "tests/res/intro_..."
# I made some other changes, like the message for the assertion exception 
# and the final `print` statement.

llm_cache_path = "tests/examples/res/intro_notebook/tapedata.sqlite"  
if not os.path.exists(llm_cache_path):
    llm_cache_path = f"../{llm_cache_path}"
assert os.path.exists(llm_cache_path), f"llm_cache_path not found: {llm_cache_path}"
llms._REPLAY_SQLITE = llm_cache_path
print(f"Using llm_cache_path = {llm_cache_path}")"
```

Note also I fixed the typo in `llm_cache_path`, discussed previously.

## Final Thoughts

I didn't spend a lot of time exploring TapeAgents, but overall, the _tape_ concept in TapeAgents is an interesting model for how agents can work. I also like their use of `pydantic` to bring in some more robustness through type safety.
