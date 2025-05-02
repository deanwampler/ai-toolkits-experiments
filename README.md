# README for `ai-toolkits-experiments`

My experiments with different Gen AI tool kits. Initially, I focused on evaluating opens for local inference on personal computers, mostly Apple Silicon Macs. However, I have also looked at application patterns like RAG, agents, and [Model Context Protocol](model-context-protocol) (MCP), as well as tool kits like [llm](llm) and [Llama Stack](llama-stack). So, this is a grab bag of stuff...

For many of the sections, I use [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) of other tool repos. To get those submdules when you clone the repo, pass `--recurse-submodules` to `git clone`, or initialize them separately.

All at once:

```shell
git clone --recurse-submodules https://github.com/deanwampler/ai-toolkits-experiments
```

Or after cloning the repo, do the following:

```shell
cd ai-toolkits-experiments
git submodule update --init --recursive
```

## Notes on Particular Projects

The project folders have their own READMEs, which document additional setup that may be required, etc.
