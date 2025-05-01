# Using the Llama API:

import argparse, os, re, sys
from llama_api_common import LlamaAPIChat, LlamaAPIResponseLogger, LlamaAPIResponsePrinter
from llama_api_client import LlamaAPIClient


example_prompts = [
    "Hello Llama! Can you give me a quick intro?",
    "When did Pope Francis die?",
    "When did Pope Francis die? Be sure to search for the latest news about him.",
    "Use google search to determine when Pope Francis died.",
]

parser = argparse.ArgumentParser(
                    prog='invoke-llama-api',
                    description='Using the Llama API Python SDK',
                    epilog='')
parser.add_argument('-m', '--model',
                    help=f"The model to use",
                    default="Llama-4-Maverick-17B-128E-Instruct-FP8")
parser.add_argument('-v', '--verbose',
                    help="Show verbose output",
                    action='store_true')  # on/off flag
args = parser.parse_args(sys.argv[1:])

api_key = os.environ.get('LLAMA_API_KEY')
if not api_key:
  print("ERROR: environment variable LLAMA_API_KEY is not defined.")
  sys.exit(1)

client = LlamaAPIClient(
    api_key=api_key,
    base_url="https://api.llama.com/v1/",
)

response_printer = LlamaAPIResponsePrinter(args.verbose)
response_logger = LlamaAPIResponseLogger(args.verbose)

chat = LlamaAPIChat( 
    client = client, 
    response_printer = response_printer,
    response_logger = response_logger,
    preamble = f"A chat example using the Llama API:",
    model = args.model,
    verbose = args.verbose,
    example_prompts = example_prompts)

chat.chat()
