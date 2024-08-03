from huggingface_hub import snapshot_download

model_name = "Qwen/Qwen1.5-1.8B" 
#methods = ['q2_k', 'q3_k_m', 'q4_0', 'q4_k_m', 'q5_0', 'q5_k_m', 'q6_k', 'q8_0'] #examples of quantization formats
methods = ['q4_0']
base_model = "./original_model/"
quantized_path = "./quantized_model/"