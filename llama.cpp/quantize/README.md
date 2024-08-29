# README

Adapted from https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory?utm_source=substack&utm_medium=email

> **NOTES:** 
>
> 1. Set up the `llama.cpp` repo as discussed in [../README.md](../README.md).
> 2. Consider setting up a Python environment with `venv` or `conda`, if you want to keep things separated. _Use the same one you used to setup the `llama.cpp` repo!_

Run this directories scripts in the following order:

```shell
download-model.py  # It is setup to run with python
quantize.sh  
```

Try `quantize.sh -h` to see the options it offers. Note that it assumes the directory structure here. So, if you have the `llama.cpp` repo somewhere else, you'll need to edit `LLAMA_CPP_REPO` in `quantize.sh`.
