# Common functions for prompting the user for queries for Llama Stack.

import os, re, sys
# hack the path to find the "common" module.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.chat import Chat, ResponseLogger, ResponsePrinter
from llama_api_client import LlamaAPIClient
from openai import OpenAI

from rich import print
from rich.pretty import pprint

import uuid
from termcolor import cprint


class LlamaAPIResponsePrinter(ResponsePrinter):

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    def non_verbose_print(self, response):
        """
        Attempt to cut down on the huge amount of output, especially
        when streaming.
        """
        pprint(response)


class LlamaAPIResponseLogger(ResponseLogger):

    def __init__(self, verbose: bool = False):
        super().__init__(verbose)

    def do_log(self, response):
        """
        At this time, there is nothing different from "printing" above, so we do nothing here.
        """
        return None


class LlamaAPIChat(Chat):
    def __init__(self, 
        client: LlamaAPIClient, 
        response_printer: ResponsePrinter,
        response_logger: ResponseLogger,
        model: str,
        preamble: str = "", 
        verbose: bool = False, 
        example_prompts: [str] = []):
        self.client = client
        self.model = model
        super().__init__(
            response_printer = response_printer,
            response_logger = response_logger,
            preamble = preamble,
            verbose = verbose,
            example_prompts = example_prompts)

    def turn(self,
        user_prompt: str):
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
    )

# Compare this to LlamaAPIChat and you can see they closely patterned the LLama API
# after OpenAI's Python API.
class LlamaAPIOpenAIChat(Chat):
    def __init__(self, 
        client: OpenAI, 
        response_printer: ResponsePrinter,
        response_logger: ResponseLogger,
        model: str,
        preamble: str = "", 
        verbose: bool = False, 
        example_prompts: [str] = []):
        self.client = client
        self.model = model
        super().__init__(
            response_printer = response_printer,
            response_logger = response_logger,
            preamble = preamble,
            verbose = verbose,
            example_prompts = example_prompts)

    def turn(self,
        user_prompt: str):
        return self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": user_prompt},
            ],
        )
