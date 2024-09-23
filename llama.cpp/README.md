# README for `llama.cpp`

Experiments with [`llama.cpp`](https://github.com/ggerganov/llama.cpp).

Contents:

* `quantize`: directory with code to download and quantize models, adapted from the quantization code in https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory?utm_source=substack&utm_medium=email
* `download-model.py`: Download a model.

> **NOTE:** Consider setting up a Python environment with `venv` or `conda`, if you want to keep things separated.

First, you need to build the `llama.cpp` repo, which is installed as a submodule in this directory, named `llama.cpp-git` (following the naming convention used for other submodules in this repo...). If you need to clone it somewhere else, use `git clone https://github.com/ggerganov/llama.cpp`.

Now run _one_ of the following commands from the current directory:

```shell
# You are on a Mac or PC without an NVIDIA GPU installed:
cd llama.cpp-git && make && pip install -r requirements.txt
# You have an NVIDIA GPU installed:
cd llama.cpp-git && GGML_CUDA=1 make && pip install -r requirements.txt
```

> **NOTE:** In the blog post above, he uses a different flag, which appears to be obsolete:
> 
> ```
> cd llama.cpp-git && LLAMA_CUBLAS=1 make && pip install -r requirements.txt
> ```
