# README for `apple/mlx-lm`

Exploring Apple's MLX deep learning framework.

Contents:

* `mlx-deep-dive-git`: directory for the git repo for [this blog post](https://towardsdatascience.com/deploying-llms-locally-with-apples-mlx-framework-2b3862049a93).
* `mlx-examples-git`: directory for the git repo for Apple's MLX examples.
* `experiments`: Contains `mlx-lm-example.py`, which is basically the same as `mlx-deep-dive-git/mlx-test-deployment.py`, with a few changes. At this time, this folder doesn't have any code based on `mlx-examples-git`.

## The HF MLX Community

The [HF MLX community](https://huggingface.co/mlx-community), which has ported some models to the MLX format. It also offers instructions for CLI tools, etc.

```shell
# The generate command for inference:
model_name='mistralai/Mistral-7B-Instruct-v0.2'
python -m mlx_lm.generate --help
python -m mlx_lm.generate --model $model_name --prompt "hello"

# Model conversion:
python -m mlx_lm.convert --help
python -m mlx_lm.convert --hf-path $model_name -q 
```


## Running Llama 3.3 70B - Simon Willison

Simon published a [blog post](https://simonwillison.net/2024/Dec/9/llama-33-70b/) (and [Substack](https://simonw.substack.com/p/i-can-now-run-a-gpt-4-class-model)) December 9^th^ about how amazing it is that you can run this GPT 4-class model on a laptop, in his case an MacBook Pro M2 with 64GB. He says the model is not likely to run on a machine with much less memory. It appears to require about 38GB of memory, when I attempted to run the following code on a machine with 32GB.

He also [discusses running the model with MLX](https://simonwillison.net/2024/Dec/9/llama-33-70b/#bonus-running-llama-3-3-70b-with-mlx), summarized here.

[Install `uv`](https://github.com/astral-sh/uv), then run the following command:

```shell
uv run --with mlx-lm --python 3.12 python
```

That launched a Python interpreter. Then enter the following to download the 37GB model weights,  [mlx-community/Llama-3.3-70B-Instruct-4bit](https://huggingface.co/mlx-community/Llama-3.3-70B-Instruct-4bit) to `~/.cache/huggingface/hub/models--mlx-community--Llama-3.3-70B-Instruct-4bit`:

```python
from mlx_lm import load, generate
model, tokenizer = load("mlx-community/Llama-3.3-70B-Instruct-4bit")
```

This took well over an hour on my home network...

Now try it:

```python
prompt = "Generate an SVG of a pelican riding a bicycle, start with <svg>"
messages = [{"role": "user", "content": prompt}]
prompt2 = tokenizer.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True
)
response = generate(
    model, tokenizer, prompt=prompt2, verbose=True
)
```

He got an image that isn't great, but not terrible considering the runtime situation.


