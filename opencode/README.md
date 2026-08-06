# README for OpenCode

[OpenCode](https://opencode.ai/) is an open-source, AI coding agent.

I installed it with Brew:

```shell
brew install anomalyco/tap/opencode
```

I also thought I would try one of their recommendations for a terminal, but I downloaded a few and decided I wasn't interested in figuring out how to configure them the way that I like. iTerm should be good enough...

In what follows, iTerm appeared to work well.

## Running OpenCode with Project Tapestry

```shell
opencode .../tapestry
```

First, I used the `/models` command, then ctrl+a to select `ollama` and my preferred model, `gemma4:12b-mlx`.

Then I ran the query, "find the TODOs in the code base", but all it printed out was `Thought: 11.3s` (for example) for each step and messages like `Grep "TODO|FIXME" in src`, but didn't show anything.

So I asked, "Show the TODOs found" and it failed:

```
I couldn't find any TODO or FIXME tags in the Python files listed because the previous grep commands returned "No files found" for those patterns.
Would you like me to search for other keywords (e.g., NOTE, DEBUG) or check non-Python files?
```

So I entered, "Check all markdown and pythong files in the repo", but that returned nothing.

Actually, inspecting the results separately, I think this is correct, as the only TODOs are actually in libraries under `.venv`, etc.

Otherwise, it seems okay as a terminal UI. Selection is a bit "finicky" but workable.
