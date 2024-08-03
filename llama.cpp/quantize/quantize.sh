#!/usr/bin/env zsh
# Adapted from https://kaitchup.substack.com/p/gguf-quantization-for-fast-and-memory?utm_source=substack&utm_medium=email

LLAMA_CPP_REPO=$(realpath ../llama.cpp-git)
DEFAULT_MODEL_NAME="Qwen/Qwen1.5-1.8B" 
# Allowed quantization formats (are there others?):
ALLOWED_METHODS=('q2_k' 'q3_k_m' 'q4_0' 'q4_k_m' 'q5_0' 'q5_k_m' 'q6_k' 'q8_0')
DEFAULT_METHODS=('q4_0')
ORIG_MODEL_DIR_ROOT="./original_models"
GGUF_MODEL_DIR_ROOT="./gguf_models"
QUANTIZED_MODEL_DIR_ROOT="./quantized_models"

help() {
  cat <<EOF
$0 [-h|--help] [-n|--noop] [-m|--model MODEL] [-f|--format QF] \ 
   [d|download] [c|convert] [q|quantize] [r|run] [a|all]
where:
-h | --help         Print this message and exit.
-n | --noop         Print the commands, but don't execute them.

-m | --model MODEL  Use MODEL (Default: $DEFAULT_MODEL_NAME)
-f | --format QF    Use quantization format. Repeat for using several formats
                    or separate with commas, e.g., "q2_k,q3_k_m"
                    Allowed values: ${ALLOWED_METHODS[@]}
                    Default values: ${DEFAULT_METHODS[@]}

The commands to run can be in any order, but they are executed in the order show.
If you don't specify a command, "download", "convert", and "quantize" are run.

d | download        Download one or more models.
c | convert         Convert models to GGUF format (Done automatically with "download")
q | quantize        Quantize the downloaded models.
r | run             Run an example chat with all the quantized models.
a | all             Do all of the above.

EOF
}

error() {
  echo "ERROR: $@"
  help
  exit 1
}

make_qtype_path() {
  m=$1
  echo "${quantized_model_dir}/$(echo $m | tr '[a-z]' '[A-Z]').gguf"
}

true_false() {
  [[ $1 -eq 0 ]] && echo true || echo false
}

check_for_allowed_methods() {
  local not_found=()
  for m1 in "$@"
  do
    local found
    let found=1
    for m2 in ${ALLOWED_METHODS[@]}
    do
      if [[ "$m1" = "$m2" ]]
      then
        let found=0
        break
      fi
    done
    [[ $found -eq 0 ]] || not_found+=($m1)
  done
  [[ ${#not_found[@]} -eq 0 ]] || error "Unrecognized quantization formats: ${not_found[@]} (allowed: ${ALLOWED_METHODS[@]})"
}

: ${NOOP:=}
let download=1
let convert=1
let quantize=1
let run=1
let at_least_one=1
model_name=
format_methods=()
while [[ $# -gt 0 ]]
do
  case $1 in
    -h|--help)
      help
      exit 0
      ;;
    -n|--noop)
      NOOP=echo
      ;;
    -m|--model)
      shift
      model_name=$1
      ;;
    -f|--format)
      shift
      formats=($(echo "$1" | sed -e 's/,/ /'))
      format_methods+=(${formats[@]})
      ;;
    d|down*)
      let download=0
      let convert=0
      let at_least_one=0
      ;;
    c|con*)
      let convert=0
      let at_least_one=0
      ;;
    q|quan*)
      let quantize=0
      let at_least_one=0
      ;;
    r|run)
      let run=0
      let at_least_one=0
      ;;
    a|all)
      let download=0
      let convert=0
      let quantize=0
      let run=0
      let at_least_one=0
      ;;
    *)
      error "Unrecognized argument $1"
      ;;
  esac
  shift
done

if [[ $at_least_one -ne 0 ]]
then
  let download=0
  let convert=0
  let quantize=0
fi

[[ -n "$model_name" ]] || model_name="$DEFAULT_MODEL_NAME"
[[ ${#format_methods[@]} -gt 0 ]] || format_methods=(${DEFAULT_METHODS[@]})
check_for_allowed_methods "${format_methods[@]}"

echo "$0:"
echo "Model:     $model_name"
echo "Formats:   ${format_methods[@]}"
echo "download?  $(true_false $download)"
echo "convert?   $(true_false $convert)"
echo "quantize?  $(true_false $quantize)"
echo "run?       $(true_false $run)"

orig_model_dir="$ORIG_MODEL_DIR_ROOT/$model_name"
gguf_model_dir="$GGUF_MODEL_DIR_ROOT/$model_name"
gguf_model_path="$gguf_model_dir/FP16.gguf"
quantized_model_dir="$QUANTIZED_MODEL_DIR_ROOT/$model_name"

if [[ $download -eq 0 ]]
then
  echo "=== Downloading model to $orig_model_dir"
  $NOOP rm -rf "$orig_model_dir"
  $NOOP mkdir -p "$orig_model_dir"
  cmd=python
  if [[ -n "$NOOP" ]] 
  then
    echo "Running in python:"
    echo "from huggingface_hub import snapshot_download"
    echo "snapshot_download(repo_id="$model_name", local_dir="$orig_model_dir", local_dir_use_symlinks=False)"
  else
    cat <<EOF | $cmd
from huggingface_hub import snapshot_download
snapshot_download(repo_id="$model_name", local_dir="$orig_model_dir", local_dir_use_symlinks=False)
EOF
  fi
  $NOOP ls -l "$orig_model_dir"
  [[ -n "$NOOP" ]] || [[ -d "$orig_model_dir" ]] || error "Failed to download model to $orig_model_dir"
fi

if [[ $convert -eq 0 ]]
then
  echo "=== Converting model in $orig_model_dir to $gguf_model_path"
  $NOOP mkdir -p "$gguf_model_dir"
  $NOOP python "$LLAMA_CPP_REPO/convert_hf_to_gguf.py" "$orig_model_dir" --outtype f16 --outfile "$gguf_model_path"
  $NOOP ls -l "$gguf_model_path"
  [[ -n "$NOOP" ]] || [[ -d "$gguf_model_path" ]] || error "Failed to convert model to $gguf_model_path"
fi

if [[ $quantize -eq 0 ]]
then
  $NOOP mkdir -p "$quantized_model_dir"
  for m in ${format_methods[@]}
  do
    qtype_path=$(make_qtype_path $m)
    echo "=== Quantizing "$gguf_model_path" to $qtype_path using $m"
    $NOOP "$LLAMA_CPP_REPO/llama-quantize" "$gguf_model_path" "$qtype_path" "$m"
  done
fi

if [[ $run -eq 0 ]]
then
  for m in ${format_methods[@]}
  do
    qtype_path=$(make_qtype_path $m)
    echo "=== Running $qtype_path:"
    $NOOP "$LLAMA_CPP_REPO/llama-cli" -m "$qtype_path" -n 90 --repeat_penalty 1.0 --color -i -r "User:" -f "$LLAMA_CPP_REPO/prompts/chat-with-bob.txt"
  done
fi
