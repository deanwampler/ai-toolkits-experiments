# README for OpenCode

[OpenCode](https://opencode.ai/) is an open-source, AI coding agent.

I installed it with Brew:

```shell
brew install anomalyco/tap/opencode
```

I decided to try one of their recommendations for a terminal, [WezTerm](https://wezterm.org/), which proved easy enough to configure to my tastes. However, in subsequent experiments with both WezTerm and iTerm, I didn't notice any differences in features.

> [!TIP]
> I discovered by accident that if you make the terminal window wide enough, it shows some useful runtime information in a vertical bar on the right-hand side.

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

So I entered, "Check all markdown and python files in the repo", but that returned nothing.

Actually, inspecting the results separately, I think this is correct, as the only TODOs are actually in libraries under `.venv`, etc.

But other queries also returned nothing useful, so I switched to `gpt-oss:20b` and got better results.

It seems good as a terminal UI. Selection is a bit "finicky" but workable.

## Integration with Editors and IDEs

The `/export` command is very nice for capturing your session in a markdown file and opening it in your default `EDITOR`.

The `/editor` command opens a blank file in Sublime Text that is supposed to be for editing queries, but how is it used? I tried editing a prompt, then saving the file and nothing happened anywhere that I can see.

Both commands close the GUI in the terminal. There isn't an obvious way to go back and a quick search of the docs didn't help.

I added it to VS Code by installing the `opencode` plugin. That seemed to work better than following the suggestion to just run `opencode` at a terminal prompt. Then using `cmd+shift+esc` opened the same TUI, but in VS Code.
