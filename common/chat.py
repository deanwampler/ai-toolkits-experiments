# Common functions for prompting the user for queries.

import os, re, sys
import readline  # enhances the input() function with real command-line editing, history, etc.
from argparse import Namespace
from termcolor import colored
from types import GeneratorType
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
                    self.non_verbose_print(res)
        else:
            if self.verbose:
                pprint(response)
            else:
                self.non_verbose_print(response)


class ResponseLogger():
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def do_log(self, response):
        pass

    def log(self, response):
        if self.verbose:
            if isinstance(response, GeneratorType):
                for res in response:
                    self.do_log(res)
            else:
                self.do_log(response)

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

