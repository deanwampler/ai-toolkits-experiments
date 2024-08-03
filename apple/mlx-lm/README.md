# README for mlx-lm

Exploring Apple's MLX deep learning framework.

The `mlx-deep-dive` directory is a git repo for [this blog post](https://towardsdatascience.com/deploying-llms-locally-with-apples-mlx-framework-2b3862049a93).

The `mlx-lm-example.py` is basically the same as `mlx-deep-dive/mlx-test-deployment.py`, with a few changes. 

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

