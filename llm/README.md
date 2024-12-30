# README for `llm`

This section discusses Simon Willison’s wonderful [`llm` tool](https://github.com/simonw/llm).

## Chris Adams' Convenient Scripts

[This post](https://rtl.chrisadams.me.uk/2024/12/how-i-use-llms-neat-tricks-with-simons-llm-tool/) by Chris Adams discusses some `fish` shell functions he uses with VSCode

Here, I port them to `zsh`, modify the function names, and use Sublime Text. I tried using the `$EDITOR` variable instead of hard-coding `subl -w`, but had trouble with `zsh` interpreting `subl -w` as the whole command name, not `subl` with the argument `-w`. 

See the `llm-funcs.sh` file. The functions themselves are described in the blog post.
You can easily replace the `subl -w` with your preferred editor. E.g., if you like VSCode, see the comments in the script.
