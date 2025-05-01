# Common functions for prompting the user for queries for Llama Stack.

import os, re, sys
# hack the path to find the "common" module.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.chat import Chat, ResponseLogger, ResponsePrinter

from llama_stack_client import AgentEventLogger
from llama_stack_client import Agent
# from llama_stack_client.types.agents import TurnResponseEventPayload
from rich import print
from rich.pretty import pprint

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
