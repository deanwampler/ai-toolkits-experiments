# Common functions for prompting the user for queries.

import os, re, sys
import readline  # enhances the input() function with real command-line editing, history, etc.
from argparse import Namespace
from termcolor import colored
from types import GeneratorType
from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
# from llama_stack_client.types.agents import TurnResponseEventPayload
from rich import print
from rich.pretty import pprint

class ResponsePrinter():
    in_step_progress  = False

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def non_verbose_print(self, response):
        """
        Override for more fine-grained output, intended for the case when
        "non-verbose" output is required. By default. this function just
        pretty-prints the whole response.
        """
        pprint(response)

    def print(self, response):
        if isinstance(response, GeneratorType):
            for res in response:
                if self.verbose:
                    pprint(res)
                else:
                    non_verbose_print(res)
        else:
            if self.verbose:
                pprint(response)
            else:
                non_verbose_print(response)

class LlamaStackResponsePrinter(ResponsePrinter):

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    def non_verbose_print(self, response):
        """
        Attempt to cut down on the huge amount of output, especially
        when streaming.
        """
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

class ResponseLogger():
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def do_log(self, response):
        pass

    def log(self, response):
        if self.verbose:
            if isinstance(response, GeneratorType):
                for res in response:
                    do_log(res)
            else:
                do_log(response)

class LlamaStackResponseLogger(ResponseLogger):

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    def do_log(self, response):
        """
        It seems that the logging API should be smarter about handling different types of input.
        The following _only_ works when the --streaming option is used. Otherwise, it crashes 
        in the call above to AgentEventLogger().log(response)
        """
        # for log in AgentEventLogger().log(response):
        #     log.print()
        pass

class Chat():
    def __init__(self,
        response_printer: ResponsePrinter,
        response_logger: ResponseLogger,
        preamble: str = "", 
        verbose: bool = False, 
        example_prompts: [str] = []):
        self.preamble = preamble
        self.verbose = verbose
        self.response_printer = response_printer
        self.response_logger = response_logger
        self.example_prompts = example_prompts

    def prompt(self) -> str:
        print(f"Enter your prompts. When finished, enter a blank line, 'q', 'quit', or ^D.")
        print("Examples (enter the number to try one or 'all' to try all of them):")
        for i in range(len(self.example_prompts)):
            print(f"{(i+1):2d}: {self.example_prompts[i]}")
        return input("> ")

    def turn(self, user_prompt: str):
        """
        In specific subclasses, provide a concrete implementation for taking a query-response "turn".
        """
        pass

    def chat(self):
        print(self.preamble)
        while True:
            try:
                user_prompts = []
                user_prompt = self.prompt()
                if user_prompt == "" or user_prompt == "q" or user_prompt == "quit":
                    print("Finished!")
                    break
                elif user_prompt == "all" or user_prompt == "ALL":
                    user_prompts = self.example_prompts
                elif re.fullmatch(r'^\d+$', user_prompt):
                    index = int(user_prompt)
                    num_examples = len(self.example_prompts)
                    if index < 1 or index > num_examples:
                        print(f"For running an example, input a number between 1 and {num_examples}")
                        continue
                    else:
                        user_prompts = [self.example_prompts[index-1]]
                else:
                    user_prompts = [user_prompt]

                for user_prompt in user_prompts:
                    print(f"\nUsing prompt> {user_prompt}")
                    response = self.turn(user_prompt)
                    self.response_printer.print(response)
                    self.response_logger.log(response)
            except EOFError:
                if self.verbose:
                    print("Finished!")
                break


class LlamaStackChat(Chat):
    def __init__(self, 
        agent: Agent, 
        response_printer: ResponsePrinter,
        response_logger: ResponseLogger,
        preamble: str = "", 
        verbose: bool = False, 
        streaming: bool = False,
        example_prompts: [str] = []):
        self.agent = agent
        self.streaming = streaming
        super().__init__(
            response_printer = response_printer,
            response_logger = response_logger,
            preamble = preamble,
            verbose = verbose,
            example_prompts = example_prompts)
        # Create a session
        self.session_id = agent.create_session(session_name="Llama Stack chat")

    def turn(self,
        user_prompt: str):
        return self.agent.create_turn(
                session_id=self.session_id,
                messages=[{"role": "user", "content": user_prompt}],
                stream=self.streaming,
            )
