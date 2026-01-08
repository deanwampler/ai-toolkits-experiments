#!/usr/bin/env python

import argparse, os, requests, sys, uuid

# This is what the code example showed in in the Langflow GUI,
#   api_key = 'YOUR_API_KEY_HERE'
# But I am putting this code in GitHub, so I don't want to hard-code this value here,
# even for demo code. Instead, I'll read it from my environment:
api_key = os.environ.get('LANGFLOW_API_KEY')
if not api_key:
    print('ERROR: LANGFLOW_API_KEY must be defined in your environment.')
    sys.exit(1)

# The docs say 7860, but I effectively ran two concurrent server instances, once with 
# the desktop app and once using the CLI, so I could use either 7860 or 7861:
def_port=7860
def_flow="13e81448-428c-4037-b50c-30875384e68b"
def_prompt="Give a recipe for chocolate cake and a recipe for apple pie, then add the number of ingredients for each recipe together and tell me how many total ingredients I need."

parser = argparse.ArgumentParser(
    description="Langflow Simple Agent"
)

parser.add_argument("-p", "--port", default=def_port,
    help=f"Langflow server port. Default: {def_port}")
parser.add_argument("-f", "--flow", default=def_flow,
    help=f"Langflow flow identifier. Default: {def_flow}")
parser.add_argument("-v", "--verbose", action="store_true",
    help="Enable verbose output")
parser.add_argument("prompt", nargs="?", default=def_prompt,
    help=f"The prompt. Default: {def_prompt}")

args = parser.parse_args()

url = f"http://localhost:{args.port}/api/v1/run/{args.flow}"  # The complete API endpoint URL for this flow

prompt = args.prompt
if prompt == "default":
    prompt = def_prompt
if args.verbose:
    print("Simple Agent:")
    print(f"  port:   {args.port}")
    print(f"  prompt: {prompt}")
    print(f"  URL:    {url}")

# Request payload configuration
payload = {
    "output_type": "chat",
    "input_type": "chat",
    # This is what the code example showed in in the Langflow GUI,
    # "input_value": "Hello, how are you?" 
    "input_value": prompt,
}
payload["session_id"] = str(uuid.uuid4())

headers = {"x-api-key": api_key}

try:
    # Send API request
    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception for bad status codes

    # Print response
    print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except ValueError as e:
    print(f"Error parsing response: {e}")
