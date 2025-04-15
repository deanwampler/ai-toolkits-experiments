SETUP_SCRIPT=$0

export LLAMA_STACK_PORT=5001

# ollama names this model differently, and we must use the ollama name when loading the model
export OLLAMA_INFERENCE_MODEL="llama3.2:3b"
export INFERENCE_MODEL=$OLLAMA_INFERENCE_MODEL
# export INFERENCE_MODEL="meta-llama/Llama-3.2-3B"

export OLLAMA_SAFETY_MODEL="llama-guard3:1b"
export SAFETY_MODEL="meta-llama/Llama-Guard-3-1B"
# export SAFETY_MODEL=$OLLAMA_SAFETY_MODEL

must_use() {
	echo "$SETUP_SCRIPT: ERROR: Must use the llama-stack conda environment:"
	echo "$SETUP_SCRIPT: ERROR: conda activate llama-stack"
	exit 1
}

check_conda_env() {
	if [[ -z $CONDA_DEFAULT_ENV ]]
	then
		must_use
	elif [[ $CONDA_DEFAULT_ENV != llama-stack ]]
	then
		echo "$SETUP_SCRIPT: ERROR: Wrong conda environment! $CONDA_DEFAULT_ENV (path: $CONDA_PREFIX)"
		must_use
	fi
}

check_conda_env

export PATH_TO_YAMLS="$CONDA_PREFIX/lib/python3.10/site-packages/llama_stack/templates/ollama"