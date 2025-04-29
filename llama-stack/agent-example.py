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

# Use the driver script `run-agent-example.sh` to drive this program.

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

# Create a session
session_id = agent.create_session(session_name="Test conversation")

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

class ResponsePrinter():
    in_step_progress  = False

    def print(self, response):
        if isinstance(response, GeneratorType):
            if args.verbose:
                print("Generator response...")
            for res in response:
                if args.verbose:
                    pprint(res)
                else:
                    # Attempt to cut down on the huge amount of output, especially
                    # when streaming.
                    if res.event.payload.event_type == "step_progress":
                        if self.in_step_progress == False:
                            self.in_step_progress=True
                            print("step results: ", end='')
                        delta = res.event.payload.delta
                        if delta.type == "text":
                            print(delta.text, end='')
                        else:
                            pprint(res)
                    else:
                        if self.in_step_progress == True:
                            self.in_step_progress = False
                            print('')
                        pprint(res)
        else:
            if args.verbose:
                print("Non-generator response...")
            pprint(response)

response_printer = ResponsePrinter()

class ResponseLogger():
    def log(self, response):
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

response_logger = ResponseLogger()

example_prompts = [
    "When did Pope Francis die?",
    "When did Pope Francis die? Be sure to search for the latest news about him.",
    "Use google search to determine when Pope Francis died.",
]

def prompt() -> str:
    print(f"Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.")
    print("Examples (enter the number to try one or 'all' to try all of them):")
    for i in range(len(example_prompts)):
        print(f"{(i+1):2d}: {example_prompts[i]}")
    return input("> ")


print(f"A chat agent example app using {streaming_msg} responses:")
while True:
    try:
        user_prompts = []
        user_prompt = prompt()
        if user_prompt == "" or user_prompt == "q" or user_prompt == "quit":
            print("Finished!")
            break
        elif user_prompt == "all" or user_prompt == "ALL":
            user_prompts = example_prompts
        elif re.fullmatch(r'^\d+$', user_prompt):
            index = int(user_prompt)
            num_examples = len(example_prompts)
            if index < 1 or index > num_examples:
                print(f"For running an example, input a number between 1 and {num_examples}")
                continue
            else:
                user_prompts = [example_prompts[index-1]]
        else:
            user_prompts = [user_prompt]

        for user_prompt in user_prompts:
            print(f"\nUsing prompt> {user_prompt}")
            response = agent.create_turn(
                session_id=session_id,
                messages=[{"role": "user", "content": user_prompt}],
                stream=args.streaming,
            )
            response_printer.print(response)
            response_logger.log(response)
    except EOFError:
        if args.verbose:
            print("Finished!")
        break
