# Register a safety shield

from common import create_library_client
from prompt import LlamaStackChat, LlamaStackResponseLogger, LlamaStackResponsePrinter
from gofannon.google_search.google_search import GoogleSearch
import argparse, os, re, sys
from termcolor import colored
from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
from rich import print
from rich.pretty import pprint
from rich.pretty import Pretty
from rich.panel import Panel

# Use the driver script `run-agent-example.sh` to drive this program.
# For gofannon and the Google API client:
# See the README for instructions about installing dependencies, etc.

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

google_search = GoogleSearch(api_key=os.getenv("GOOGLE_API_KEY"), engine_id="75be790deec0c42f3")
google_search_for_llama_stack = google_search.export_to_llamastack()

if args.verbose:
    import inspect
    print("Details about `google_search_for_llama_stack`:")
    print(f"Members:")
    for x in inspect.getmembers(google_search_for_llama_stack):
        print(f"  {x} => {str(x)}")
    print(f"str(google_search_for_llama_stack). Static Members:")
    for x in inspect.getmembers_static(google_search_for_llama_stack):
        print(f"  {x} => {str(x)}")
    print(f"Is it a function? {inspect.isfunction(google_search_for_llama_stack)}")
    print(f"The function signature: {str(inspect.signature(google_search_for_llama_stack))}")
    print(f"Code comments:\n{inspect.getcomments(google_search_for_llama_stack)}")
    print(f"The doc string:\n{google_search_for_llama_stack.__doc__}")

# Create the agent, configuring the model and two tools.
agent = Agent(
    client,
    model=args.model,
    instructions="You are a helpful assistant that can use tools to answer questions.",
    sampling_params={
        "strategy": {"type": "top_p", "temperature": 1.0, "top_p": 0.9},
    },
    tools=[
        # Note: While you can also use "builtin::websearch" as a tool,
        # this example shows how to use a client side custom web search tool.
        google_search_for_llama_stack,
        # "builtin::websearch",
        # "builtin::code_interpreter", 
        # "builtin::rag/knowledge_search",
    ],
)

pprint(f"agent.agent_config = {agent.agent_config}")

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

# First, do a "non-streaming" prompt. 
# Update: Now runs an interactive session.

if args.verbose:
    pprint("Locals:")
    pretty = Pretty(locals())
    panel = Panel(pretty)
    print(panel)

# if args.streaming and not args.verbose:
#     print("NOTE: --verbose turned on automatically when --streaming used.")
#     args.verbose = True

streaming_msg="non-streaming"
if args.streaming:
    streaming_msg="streaming"

response_printer = LlamaStackResponsePrinter(args.verbose)
response_logger = LlamaStackResponseLogger(args.verbose)

chat = LlamaStackChat( 
    agent = agent, 
    response_printer = response_printer,
    response_logger = response_logger,
    preamble = f"A chat agent example app using {streaming_msg} responses and gofannon functions:",
    verbose = args.verbose,
    streaming = args.streaming,
    example_prompts = example_prompts)

chat.chat()
