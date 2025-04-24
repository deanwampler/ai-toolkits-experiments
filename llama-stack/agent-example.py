# Register a safety shield

from common import create_library_client
import argparse, os, re, sys
import readline  # enhances the input() function with real command-line editing, history, etc.
from termcolor import colored
from types import GeneratorType
from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
from rich import print
from rich.pretty import pprint
from rich.pretty import Pretty
from rich.panel import Panel

# Ollama-compatible names:
def_model = "llama3.2:3B"
# def_model = "llama3.2:1b-instruct-fp16"
# def_model = "llama3.2:3b-instruct-turbo"
# def_model = "llama3.3:70b"                  # 43GB
# def_model = "llama3.3:70b-instruct-fp16"    # 143GB - too big for a laptop, so not tried!
# def_model = "llama3.3:70b-instruct-q4_K_M"  # 43GB - manageable!
# def_model = "llama3-chatqa:70b"             # 40GB - trained by NVIDIA and closest to what the Gofannon example uses with an external service: meta-llama/Llama-3-70b-chat

parser = argparse.ArgumentParser(
                    prog='agent-example',
                    description='An extended version of the Llama Stack agent example here: https://llama-stack.readthedocs.io/en/latest/building_applications/agent.html',
                    epilog='')
parser.add_argument('-m', '--model',
                    default=def_model,
                    help=f"The model to use (default is {def_model})")
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
#    model="meta-llama/Llama-3-70b-chat",
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

# Create a session
session_id = agent.create_session(session_name="Test conversation")

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

if args.streaming and not args.verbose:
    print("NOTE: --verbose turned on automatically when --streaming used.")
    args.verbose = True

def format_response(response) -> Pretty:
    return f"""
Input:  
{response.input_messages}
Output: 
{response.output_message.content}
Steps:
{response.steps}
"""

streaming_msg="non-streaming"
if args.streaming:
    streaming_msg="streaming"

# AgentEventLogger is too fragile! It can't handle some response
# objects, which are different types depending on whether or not 
# you use streaming.
def do_log(response):
    for log in AgentEventLogger().log(response):
        log.print()

def pp_response(response):
    if isinstance(response, GeneratorType):
        if args.verbose:
            print("Generator response...")
        for res in response:
            if args.verbose:
                pprint(res)
            else:
                pprint(res.event.payload.tool_call)
    else:
        if args.verbose:
            print("Non-generator response...")
        pprint(response)

def log_response(response):
    if args.verbose:
        print(f" Skipping logging of the 'response'.")
        # It seems that the logging API should be smarter about handling different types of input.
        # The following _only_ works when the --streaming option is used. Otherwise, it crashes 
        # in the call above to AgentEventLogger().log(response)
        # if isinstance(response, GeneratorType):
        #     for res in response:
        #         do_log(res)
        # else:
        #     do_log(response)

example_prompts = [
    "When did Pope Francis die?",
    "Use google search to determine when Pope Francis died.",
    "What is the current weather in Chicago?",
]

def print_examples():
    print("Examples (enter the number to try them):")
    for i in range(len(example_prompts)):
        print(f"{(i+1):2d}: {example_prompts[i]}")

print(f"""A chat agent example app using {streaming_msg} responses:
Enter your prompts. When finished, enter a blank line or ^D.
""")
user_prompt = " "
while True:
    try:
        print_examples()
        user_prompt = input("> ")
        if user_prompt == "":
            print("Finished!")
            break
        elif re.fullmatch(r'^\d+$', user_prompt):
            index = int(user_prompt)
            num_examples = len(example_prompts)
            if index < 1 or index > num_examples:
                print(f"For running an example, input a number between 1 and {num_examples}")
                continue
            else:
                user_prompt = example_prompts[index-1]
                print(f"Using example prompt> {user_prompt}")
        response = agent.create_turn(
            session_id=session_id,
            messages=[{"role": "user", "content": user_prompt}],
            stream=args.streaming,
        )
        pp_response(response)
        log_response(response)
    except EOFError:
        if args.verbose:
            print("Finished!")
        break
