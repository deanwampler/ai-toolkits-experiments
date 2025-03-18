#!/usr/bin/env zsh

export SCRIPT=$0
export ROOT_DIR=$(dirname $SCRIPT)
. $ROOT_DIR/.setup.sh

help() {
	cat <<EOF
Usage: $0 [-h|--help] [-i|--inference] [-s|--safety]
Where
-h | --help          Print this message and exit.
-i | --inference     Run the inference model $INFERENCE_MODEL (default).
-s | --safety        Run the safety model $SAFETY_MODEL.

This script lets you run one or the other model and leaves you at the 
interactive chat prompt. You can safely CTRL-D to exit the prompt
and the rest of this Llama Stack experimental code will still work.

So, if you want to run both the inference and safety model, do the 
following:
   run-model.sh -i
   CTRL-D
   run-model.sh -s
   CTRL-D
EOF
}

error() {
	echo "$SCRIPT: ERROR: $@"
	help
	exit 1
}

which_model=$OLLAMA_INFERENCE_MODEL
which_model_kind=inference
while [[ $# -gt 0 ]]
do
	case $1 in
		-h|--help)
			help
			exit 0
			;;
		-i|--inference)
			which_model=$OLLAMA_INFERENCE_MODEL
			which_model_kind=inference
			;;
		-s|--safety)
			which_model=$OLLAMA_SAFETY_MODEL
			which_model_kind=safety
			;;
		*)
			error "Unrecognized argument: $1"
			exit 1
			;;
	esac
	shift
done

echo "Running $which_model_kind model: $which_model"
$NOOP ollama run $which_model --keepalive 60m
