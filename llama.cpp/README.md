# README for `llama.cpp`

The `quantize` directory adapts the quantization code from https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory?utm_source=substack&utm_medium=email

> **NOTE:** Consider setting up a Python environment with `venv` or `conda`, if you want to keep things separated.

First, you need to build the `llama.cpp` repo, which is installed as a submodule in this directory. If you need to clone it somewhere else, use `git clone https://github.com/ggerganov/llama.cpp`.

Now run _one_ of the following commands from the current directory:

```shell
# You are on a Mac or PC without an NVIDIA GPU installed:
cd llama.cpp && make && pip install -r requirements.txt
# You have an NVIDIA GPU installed:
cd llama.cpp && GGML_CUDA=1 make && pip install -r requirements.txt
```

> **NOTE:** In the blog post above, he uses a different flag, which appears to be obsolete:
> 
> ```
> cd llama.cpp && LLAMA_CUBLAS=1 make && pip install -r requirements.txt
> ```
