#!/usr/bin/env zsh

export SCRIPT=$0
export ROOT_DIR=$(dirname $SCRIPT)
. $ROOT_DIR/.setup.sh

help() {
	cat <<EOF
Usage: $0 [-h|--help] [-s|--safety]
Where
-h | --help          Print this message and exit.
-s | --safety        Also running the Llama Stack Safety / Shield APIs (with model $SAFETY_MODEL)
EOF
}

error() {
	echo "$SCRIPT: ERROR: $@"
	help
	exit 1
}

which_yaml="run.yaml"
safety_args=
while [[ $# -gt 0 ]]
do
	case $1 in
		-h|--help)
			help
			exit 0
			;;
		-s|--safety)
			# Handle repeated -s flags!
			[[ -z $safety ]] && safety="--env SAFETY_MODEL=$SAFETY_MODEL"
			which_yaml="run-with-safety.yaml"
			;;
		*)
			error "Unrecognized argument: $1"
			exit 1
			;;
	esac
	shift
done

echo running: llama stack run $PATH_TO_YAMLS/$which_yaml \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env SAFETY_MODEL=$SAFETY_MODEL \
  --env OLLAMA_URL=http://localhost:11434

[[ -z $NOOP ]] && llama stack run $PATH_TO_YAMLS/$which_yaml \
  --port $LLAMA_STACK_PORT \
  --env INFERENCE_MODEL=$INFERENCE_MODEL \
  --env SAFETY_MODEL=$SAFETY_MODEL \
  --env OLLAMA_URL=http://localhost:11434
