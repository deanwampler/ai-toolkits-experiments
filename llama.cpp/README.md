# README for `llama.cpp`

Experiments with [`llama.cpp`](https://github.com/ggerganov/llama.cpp).

## Approach

After using the [Do It Yourself](#do-it-yourself) approach below, I discovered this easier way to work with `llama.cpp`, from this [Hugging Face page](https://huggingface.co/lmstudio-community/Llama-3.3-70B-Instruct-GGUF?show_file_info=Llama-3.3-70B-Instruct-Q4_K_M.gguf&local-app=llama.cpp) on quantized models, in this case using `Llama-3.3-70B-Instruct-Q4_K_M.gguf` (4-bit quantization version created by LMStudio).

Install with HomeBrew:

```shell
brew install llama.cpp
```

Then load and run the model. _If you have a large enough machine,_ try Llama 3.3 70B:

```shell
llama-cli \
  --hf-repo "lmstudio-community/Llama-3.3-70B-Instruct-GGUF" \
  --hf-file Llama-3.3-70B-Instruct-Q4_K_M.gguf \
  -p "You are a helpful assistant" \
  --conversation
```

> **NOTE:** This command took about an hour to download the model on a moderately-fast internet connection and it was too much for my Mac with 32GB of RAM.

So, try a smaller Llama model:

```shell
llama-cli \
  --hf-repo "lmstudio-community/Llama-3.2-3B-Instruct-GGUF" \
  --hf-file Llama-3.2-3B-Instruct-Q3_K_L.gguf \
  -p "You are a helpful assistant" \
  --conversation
```

This worked quickly and effectively on my M1 MacBook Pro with 32GB of RAM.

## Do It Yourself

Follow these instructions to dive into details, such as how to quantize an arbitrary model.

* `quantize`: directory with code to download and quantize models, adapted from the quantization code in https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory

> **NOTE:** Consider setting up a Python environment with `venv` or `conda`, if you want to keep things separated.

First, you can build the `llama.cpp` repo yourself, if you don't want to use the HomeBrew install above. Note that the repo is installed as a submodule in this directory, named `llama.cpp-git` (following the naming convention used for other submodules in this project...). If you want to clone the repo somewhere else, use `git clone https://github.com/ggerganov/llama.cpp` in that directory.

Now run _one_ of the following commands in the `llama.cpp-git` directory (or other location...):

```shell
# You are on a Mac or PC without an NVIDIA GPU installed:
make && pip install -r requirements.txt
# You have an NVIDIA GPU installed:
GGML_CUDA=1 make && pip install -r requirements.txt
```

> **NOTE:** In the "Kaitchup" blog post above, he uses a different flag, which appears to be obsolete:
> 
> ```
> cd llama.cpp-git && LLAMA_CUBLAS=1 make && pip install -r requirements.txt
> ```
