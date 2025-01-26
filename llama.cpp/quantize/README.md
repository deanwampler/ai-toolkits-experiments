# README

Adapted from https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory?utm_source=substack&utm_medium=email

See `../README.md` for an easier way to work with pre-built `llama.cpp` when you just want to use it for running models. The contents of this folder are useful if you want to dive into `llama.cpp` capabilities, such quantizing your own models.  


> **NOTES:** 
>
> 1. Set up the `llama.cpp` repo as discussed in [../README.md](../README.md).
> 1. Consider setting up a Python environment with `venv` or `conda`, if you want to keep things separated. _Use the same one you used to setup the `llama.cpp` repo!_

Run this directory's `quantize.sh` script:

```shell
quantize.sh  
```

Try `quantize.sh -h` to see the options it offers. Note that it assumes the directory structure here. So, if you have the `llama.cpp` repo somewhere else, i.e., not in `../llama.cpp-git`, then you'll need to pass the `--repo REPOPATH` argument to `quantize.sh`.
