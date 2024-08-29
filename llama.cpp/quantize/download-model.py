#!/usr/bin/env python
# Adapted from https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory?utm_source=substack&utm_medium=email

from huggingface_hub import snapshot_download

model_name = "Qwen/Qwen1.5-1.8B" 
#methods = ['q2_k', 'q3_k_m', 'q4_0', 'q4_k_m', 'q5_0', 'q5_k_m', 'q6_k', 'q8_0'] #examples of quantization formats
methods = ['q4_0']
base_model = "./original_model/"
quantized_path = "./quantized_model/"

snapshot_download(repo_id=model_name, local_dir=base_model , local_dir_use_symlinks=False)
original_model = quantized_path+'/FP16.gguf'
