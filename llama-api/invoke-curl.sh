#!/usr/bin/env zsh

export SCRIPT=$0
export ROOT_DIR=$(dirname $SCRIPT)

default_llama_model="Llama-4-Maverick-17B-128E-Instruct-FP8"

help() {
  cat <<EOF
Usage: $0 [-h|--help] [-n|--noop] [-v|--verbose] query
Where:
-h | --help         Print this message and exit.
-n | --noop         Just print the commands but don't execute them.
-v | --verbose      Use verbose output.
-f | --format       Use "jq" to nicely format the response JSON. Requires jq to be installed.
-m | --model MODEL  Use this Llama model. Default: $default_llama_model
--                  treat the rest of the arguments are treated as the query string.
                    Optional, but useful if you intermix arguments or the query string
                    has words that start with "-"!
query               The rest of the arguments are treated as the query string.
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

: ${NOOP:=}
invoke_help=False
verbose=False
model="$default_llama_model"
query=()
format=False
while [[ $# -gt 0 ]]
do
  case $1 in
    -h|--help)
      invoke_help=True
      ;;
    -n|--noop)
      NOOP=info
      ;;
    -v|--verbose)
      verbose=True
      ;;
    -f|--format)
      format=True
      ;;
    -m|--model)
      shift
      model="$1"
      ;;
    --)
      shift
      break
      ;;
    -*)
      error "Unrecognized option $1"
      ;;
    *)
      query+=("$1")
      ;;
  esac
  shift
done
query+=("$@")

$invoke_help && help && exit 0

auth_bearer="$LLAMA_API_KEY"
[[ -z $auth_bearer ]] && error "LLAMA_API_KEY is empty."
if $format
then
  command -v jq 2>&1 > /dev/null || error "If you use the --format option, jq must be installed."
fi

[[ ${#query} -eq 0 ]] && error "Please specify a query."

if $verbose 
then
  info "$SCRIPT:"
  info "  Model: $model"
  info "  Query: ${query[@]}"
fi

info curl "https://api.llama.com/v1/chat/completions \\ "
info "  -H \"Content-Type: application/json \" \\ "
info "  -H \"Authorization: Bearer <elided> \" \\ "
info "  -d \"{"
info "        \"model\": \"$model\","
info "        \"messages\": ["
info "           {\"role\": \"user\", \"content\": \"${query[@]}\"}"
info "    ]"
info "  }\""

echo "query: ${query[@]}"
[[ -n $NOOP ]] && exit 0

formatter=cat
$format && formatter=("jq" ".")

curl "https://api.llama.com/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $auth_bearer" \
  -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"${query}\"}]}" | ${formatter}
