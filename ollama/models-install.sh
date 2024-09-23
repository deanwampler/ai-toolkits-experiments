models=(
codellama
codellama:13b
starcoder2
starcoder2:7b
starcoder2:15b
codestral
granite-code:3b
granite-code:8b
granite-code:20b)

for model in ${models[@]}
do
  echo $model
  ollama pull "$model"
done
beep