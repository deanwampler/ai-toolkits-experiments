#!/usr/bin/env zsh

export SCRIPT=$0
export ROOT_DIR=$(dirname $SCRIPT)

models=(
  "granite3.3:8b"                 #    5GB
  "llama3.2:3B"                   #    2GB
  "llama3.2:1b-instruct-fp16"     #    1.5GB
  "llama3.3:70b"                  #   43GB
  "llama3.3:70b-instruct-fp16"    #  143GB - too big for a laptop, so not tried!
  "llama3.3:70b-instruct-q4_K_M"  #   43GB - manageable size, but is this identical to llama3.3:70b?
  "llama3-chatqa:70b"             #   40GB - trained by NVIDIA and closest to what 
  )

models_help() {
	prefix="$1"
	for i in {1..${#models[@]}}
	do
		echo "$prefix  $i: ${models[$i]}"
	done
}

help() {
	cat <<EOF
Usage: $0 [-h|--help] [-n|--noop] [-v|--verbose] [-g|--gofannon] [model|number]
Where:
-h | --help         Print this message and exit.
-n | --noop         Just print the commands but don't execute them.
-v | --verbose      Use verbose output.
-s | --streaming    Use the streaming option.
-g | --gofannon     Run the agent-example-gofannon.py example instead of the "standard" example.
model | number      Run the specified model or the number corresponding to these models:
$(models_help "                    ")
                    Default: the script prompts you for the model.
EOF
}

do_error() {
	echo "$SCRIPT: ERROR: $@"
	help
	exit 1
}
error() {
	do_error "$@" 2>&1
}

info() {
	echo "$SCRIPT:  INFO: $@"
}

model=
parse_model_string() {
	index=$1  # user inputs _and_ zsh arrays index 1:N
	if [[ $index =~ '[0123456789]+' ]]
	then
		if (( 1 <= $index && $index <= ${#models[@]} ))
		then
			model=${models[$index]}
		else
			error "The number ${index} must be between 1 and ${#models[@]}, inclusive."
		fi
	else
		model=$1
	fi
}

: ${NOOP:=}
streaming=""
verbose=""
example_suffix=
while [[ $# -gt 0 ]]
do
	case $1 in
		-h|--help)
			help
			exit 0
			;;
		-n|--noop)
			NOOP=info
			;;
		-v|--verbose)
			verbose="--verbose"
			;;
		-s|--streaming)
			streaming="--streaming"
			;;
		-g|--gofannon)
			example_suffix="-gofannon"
			;;
		-*)
			error "Unrecognized option $1"
			;;
		*)
			parse_model_string "$1"
			;;
	esac
	shift
done

while [[ -z $model ]]
do
	echo "Input model name or a number for the following models."
	models_help ""
	printf "> "
	read input
	case $input in
		q|quit)
			info quitting
			exit 0
			;;
		*)
			parse_model_string "$input"
	esac
done
[[ -n "$example_suffix" ]] && info "Running the gofannon example."

info "export INFERENCE_MODEL=$model"
info "uv run --with llama-stack python agent-example${example_suffix}.py $verbose --model $model $streaming"
if [[ -z $NOOP ]]
then
	export INFERENCE_MODEL=$model
	uv run --with llama-stack python agent-example${example_suffix}.py $verbose --model $model $streaming
fi
