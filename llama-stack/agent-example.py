# Register a safety shield

from common import create_library_client
from prompt import LlamaStackChat, LlamaStackResponseLogger, LlamaStackResponsePrinter
import argparse, os, re, sys
from termcolor import colored
from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
from rich import print
from rich.pretty import pprint
from rich.pretty import Pretty
from rich.panel import Panel

# Use the driver script `run-agent-example.sh` to drive this program.

example_prompts = [
    "When did Pope Francis die?",
    "When did Pope Francis die? Be sure to search for the latest news about him.",
    "Use google search to determine when Pope Francis died.",
]

parser = argparse.ArgumentParser(
                    prog='agent-example',
                    description='An extended version of the Llama Stack agent example here: https://llama-stack.readthedocs.io/en/latest/building_applications/agent.html',
                    epilog='')
parser.add_argument('-m', '--model',
                    help=f"The model to use")
parser.add_argument('-s', '--streaming',
                    action="store_true",
                    help="Run the chat example with streaming output (default is non-streaming)")
parser.add_argument('-v', '--verbose',
                    help="Show verbose output",
                    action='store_true')  # on/off flag
args = parser.parse_args(sys.argv[1:])

client = (
    create_library_client()
)  # or create_http_client() depending on the environment you picked

# Create the agent, configuring the model and two tools.
agent = Agent(
    client,
    model=args.model,
    instructions="You are a helpful assistant that can use tools to answer questions.",
    sampling_params={
        "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
    },
    tools=[
        "builtin::websearch",
        "builtin::code_interpreter", 
        "builtin::rag/knowledge_search",
    ],
)

pprint(f"agent.agent_config = {agent.agent_config}")

# From the original version of this function in the Llama Stack docs:
# Turns:
# Each interaction with an agent is called a “turn” and consists of:
# 1. Input Messages: What the user sends to the agent
# 2. Steps: The agent’s internal processing (inference, tool execution, etc. - see below)
# 3. Output Message: The agent’s response

# Steps:
# Each turn consists of multiple steps that represent the agent’s thought process:
# 1. Inference Steps: The agent generating text responses
# 2. Tool Execution Steps: The agent using tools to gather information
# 3. Shield Call Steps: Safety checks being performed
# Refer to the [Agent Execution Loop](https://llama-stack.readthedocs.io/en/latest/building_applications/agent_execution_loop.html)
# for more details on what happens within an agent turn.

if args.verbose:
    pprint("Locals:")
    pretty = Pretty(locals())
    panel = Panel(pretty)
    print(panel)

streaming_msg="non-streaming"
if args.streaming:
    streaming_msg="streaming"

response_printer = LlamaStackResponsePrinter(args.verbose)
response_logger = LlamaStackResponseLogger(args.verbose)

chat = LlamaStackChat( 
    agent = agent, 
    response_printer = response_printer,
    response_logger = response_logger,
    preamble = f"A chat agent example app using {streaming_msg} responses:",
    verbose = args.verbose,
    streaming = args.streaming,
    example_prompts = example_prompts)

chat.chat()
