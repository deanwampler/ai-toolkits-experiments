# README for `llm`

This section discusses Simon Willison’s wonderful [`llm` tool](https://github.com/simonw/llm).

## Chris Adams' Convenient Scripts

[This post](https://rtl.chrisadams.me.uk/2024/12/how-i-use-llms-neat-tricks-with-simons-llm-tool/) by Chris Adams discusses some `fish` shell functions he uses with VSCode

Here, I port them to `zsh`, modify the function names, and use Sublime Text. I tried using the `$EDITOR` variable instead of hard-coding `subl -w`, but had trouble with `zsh` interpreting `subl -w` as the whole command name, not `subl` with the argument `-w`. 

See the `llm-funcs.sh` file. The functions themselves are described in the blog post.
You can easily replace the `subl -w` with your preferred editor. E.g., if you like VSCode, see the comments in the script.

## Using `llm` with Apple's MLX Framework

(Added, February 23, 2025).

Simon [published a post](https://simonw.substack.com/p/run-llms-on-macos-using-llm-mlx-and) Feb. 17 on support in `llm` for MLX.

You install it using this command:

```shell
llm install llm-mlx
```

Then you can run with any MLX-supported model, e.g.,

```shell
llm mlx download-model mlx-community/Llama-3.2-3B-Instruct-4bit

```

Downloaded from the [mlx-community](https://huggingface.co/mlx-community) on Hugging Face.

Then use it:

```shell
llm -m mlx-community/Llama-3.2-3B-Instruct-4bit 'Python code to traverse a tree, briefly'
```

He suggests defining an `llm` alias for the model:

```shell
llm aliases set l32 mlx-community/Llama-3.2-3B-Instruct-4bit
```

Now the command is shorter:

```shell
llm -m l32 'Python code to traverse a tree, briefly'
```

It's fast and effective!
