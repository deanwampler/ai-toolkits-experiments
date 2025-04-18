# Register a safety shield

from common import create_library_client
import argparse
import sys
from types import GeneratorType
from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
from rich import print
from rich.pretty import pprint
from rich.pretty import Pretty
from rich.panel import Panel

parser = argparse.ArgumentParser(
                    prog='agent-example',
                    description='An extended version of the Llama Stack agent example here: https://llama-stack.readthedocs.io/en/latest/building_applications/agent.html',
                    epilog='')
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
    model="llama3.2:3B",
#    model="meta-llama/Llama-3-70b-chat",
    instructions="You are a helpful assistant that can use tools to answer questions.",
    tools=["builtin::code_interpreter", "builtin::rag/knowledge_search"],
)

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
    return Pretty(f"""
Input:  
{response.input_messages}
Output: 
{response.output_message.content}
Steps:
{response.steps}
""")

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
        for res in response:
            pprint(res)
    else:
        pprint(res)

def log_response(response):
    if args.verbose:
        print(f" Skipping logging of the 'response'.")
    # if isinstance(response, GeneratorType):
    #     for res in response:
    #         do_log(res)
    # else:
    #     do_log(response)

print(f"Chat example using {streaming_msg} responses with your prompts:")
print("\nEnter your prompts. When finished, enter a blank line or ^D.")
user_prompt = " "
while True:
    try:
        user_prompt = input("> ")
        response = agent.create_turn(
            session_id=session_id,
            messages=[{"role": "user", "content": user_prompt}],
            stream=args.streaming,
        )
        if user_prompt == "":
            if args.verbose:
                print("Finished!")
            break
        pp_response(response)
        log_response(response)
    except EOFError:
        if args.verbose:
            print("Finished!")
        break
