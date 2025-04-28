# Register a safety shield

from common import create_library_client
from gofannon.google_search.google_search import GoogleSearch
import argparse, os, re, sys
import readline  # enhances the input() function with real command-line editing, history, etc.
from termcolor import colored
from types import GeneratorType
from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
# from llama_stack_client.types.agents import TurnResponseEventPayload
from rich import print
from rich.pretty import pprint
from rich.pretty import Pretty
from rich.panel import Panel

# For gofannon and the Google API client:
# pip install git+https://github.com/rawkintrevo/gofannon.git@161 --quiet
# pip install google-api-python-client

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

# if args.streaming and not args.verbose:
#     print("NOTE: --verbose turned on automatically when --streaming used.")
#     args.verbose = True

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
    step_progress_str = ""
    in_step_progress  = False

    def print(response):
        if isinstance(response, GeneratorType):
            if args.verbose:
                print("Generator response...")
            for res in response:
                if args.verbose:
                    pprint(res)
                else:
                    # if isinstance(res, AgentTurnResponseStepProgressPayload):
                    if res.event.payload.event_type == "step_progress":
                        in_step_progress=True
                        step_progress_str+=res.event.payload.delta.text
                        # print(res.event.payload.delta.text, end='')
                    else:
                        if in_step_progress == True:
                            pprint(f"step results: {step_progress_str}")
                            in_step_progress = False
                            step_progress_str = ''
                        pprint(res)
        else:
            if args.verbose:
                print("Non-generator response...")
            pprint(response)

response_printer = ResponsePrinter()

class ResponseLogger():
    def log(response):
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
    "Use google search to determine when Pope Francis died.",
    "What is the current weather in Chicago?",
]

def prompt() -> str:
    print(f"Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.")
    print("Examples (enter the number to try them):")
    for i in range(len(example_prompts)):
        print(f"{(i+1):2d}: {example_prompts[i]}")
    return input("> ")

print(f"A chat agent example app using {streaming_msg} responses:")
while True:
    try:
        user_prompt = prompt()
        if user_prompt == "" or user_prompt == "q" or user_prompt == "quit":
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
        response_printer.print(response)
        response_logger.log(response)
    except EOFError:
        if args.verbose:
            print("Finished!")
        break
