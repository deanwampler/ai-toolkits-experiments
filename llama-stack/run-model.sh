#!/usr/bin/env zsh

export SCRIPT=$0
export ROOT_DIR=$(dirname $SCRIPT)
. $ROOT_DIR/.setup.sh

help() {
	cat <<EOF
Usage: $0 [-h|--help] -i|--inference|-s|--safety
Where
-h | --help          Print this message and exit.
-i | --inference     Run the inference model $INFERENCE_MODEL.
-s | --safety        Run the safety model $SAFETY_MODEL.
-n | --no-prompt     If running the inference model, don't use the chat prompt.
                     By default, the script leaves you at the chat prompt.
                     This option is ignored when running just the safety model,
                     where the chat prompt isn't used.

This script lets you run one or both of the inference and security models. 
At least one of --inference or --safety must be specified.

By default, if you run the inference model, it leaves you at the interactive 
chat prompt, unless you use --no-prompt. You can safely CTRL-D to exit the
prompt and the rest of this Llama Stack experimental code will still work. 
So, using the --no-prompt option effectively does the same thing immediately.

EOF
}

error() {
	echo "$SCRIPT: ERROR: $@"
	help
	exit 1
}

no_prompt=false
while [[ $# -gt 0 ]]
do
	case $1 in
		-h|--help)
			help
			exit 0
			;;
		-i|--inference)
			inference=$OLLAMA_INFERENCE_MODEL
			;;
		-s|--safety)
			safety=$OLLAMA_SAFETY_MODEL
			;;
		-n|--no-prompt)
			no_prompt=true
			;;
		*)
			error "Unrecognized argument: $1"
			exit 1
			;;
	esac
	shift
done

run_message() {
	echo "Running $1 model: $2 $3"
	echo "(When finished, run ollama stop $2)"
}

[[ -z $inference ]] && [[ -z $safety ]] && error "Must specify one or both of --inference and --safety"

if [[ -n $safety ]]
then
	run_message "safety" "$safety"
	$NOOP ollama run $safety --keepalive 60m &
fi

if [[ -n $inference ]]
then
	no_prompt_str=
	$no_prompt && no_prompt_str="(no prompt)"
	run_message "inference" "$inference" "$no_prompt_str"
	if [[ -n $NOOP ]]
	then
		$NOOP ollama run "$inference" --keepalive 60m
	elif $no_prompt
	then
		cat <<EOF | ollama run "$inference" --keepalive 60m
EOF
	else
		$NOOP ollama run "$inference" --keepalive 60m
	fi
fi

echo "Running ollama ps"
$NOOP ollama ps