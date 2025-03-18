SETUP_SCRIPT=$0

export LLAMA_STACK_PORT=5001

# ollama names this model differently, and we must use the ollama name when loading the model
export OLLAMA_INFERENCE_MODEL="llama3.2:3b"
export INFERENCE_MODEL=$OLLAMA_INFERENCE_MODEL
# export INFERENCE_MODEL="meta-llama/Llama-3.2-3B"

export OLLAMA_SAFETY_MODEL="llama-guard3:1b"
export SAFETY_MODEL="meta-llama/Llama-Guard-3-1B"
# export SAFETY_MODEL=$OLLAMA_SAFETY_MODEL

setup_error() {
	echo "$SETUP_SCRIPT: ERROR: $@"
	exit 1
}

[[ $CONDA_PREFIX =~ /envs/llama-stack ]] || setup_error "Wrong conda environment! $CONDA_DEFAULT_ENV (path: $CONDA_PREFIX)"

export PATH_TO_YAMLS="$CONDA_PREFIX/lib/python3.10/site-packages/llama_stack/templates/ollama"