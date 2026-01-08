#!/usr/bin/env zsh

curl --request POST \
     --url 'http://localhost:7860/api/v1/run/13e81448-428c-4037-b50c-30875384e68b?stream=false' \
     --header 'Content-Type: application/json' \
     --header "x-api-key: $LANGFLOW_API_KEY" \
     --data '{
       "output_type": "chat",
       "input_type": "chat",
       "input_value": "Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need.",
       "session_id": "4d912c0c-d9a1-4121-9c8d-c236097cf06d"
     }'
