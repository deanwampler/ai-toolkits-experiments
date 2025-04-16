import os
import uuid
from termcolor import cprint

from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client.lib.agents.event_logger import EventLogger
from llama_stack_client.types import Document

def create_http_client():
    from llama_stack_client import LlamaStackClient

    return LlamaStackClient(
        base_url=f"http://localhost:{os.environ['LLAMA_STACK_PORT']}"
    )


def create_library_client(template="ollama"):
    from llama_stack import LlamaStackAsLibraryClient

    client = LlamaStackAsLibraryClient(template)
    client.initialize()
    return client
