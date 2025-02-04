models=(
codellama
codellama:13b
codestral
deepseek-r1:8b
granite-code:3b
granite-code:8b
granite-code:20b
starcoder2
starcoder2:7b
starcoder2:15b
)

for model in ${models[@]}
do
  printf '%s: ' $model
  ollama list | grep -q $model
  if [[ $? -eq 0 ]]
  then
    echo "already installed."
  else
    echo "installing..."
    ollama pull "$model"
  fi
done
beep