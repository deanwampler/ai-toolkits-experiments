models=(
codellama
codellama:13b
starcoder2
starcoder2:7b
starcoder2:15b
codestral)

for model in ${models[@]}
do
  echo $model
  ollama pull "$model"
done
beep