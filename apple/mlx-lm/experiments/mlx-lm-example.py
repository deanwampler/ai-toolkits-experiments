#!/usr/bin/env python
# Adapted from https://towardsdatascience.com/deploying-llms-locally-with-apples-mlx-framework-2b3862049a93
from typing import Tuple
from mlx_lm import load, generate
import argparse

# To use the Mistral model, you need to be logged into HF 
# (https://huggingface.co/docs/huggingface_hub/en/guides/cli#huggingface-cli-login)
# and you have to agree to to Mistral's terms for using the model 
# (https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2/tree/main).

example_models=[
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mlx-community/Mistral-7B-v0.2-4bit",
    "mlx-community/Hermes-2-Pro-Mistral-7B-4bit",
    "mlx-community/Mixtral-8x7B-Instruct-v0.1",
    "mlx-community/Mixtral-8x22B-4bit",
    "mlx-community/Mixtral-8x22B-Instruct-v0.1-4bit",
    "mlx-community/Mixtral-8x22B-Instruct-v0.1-8bit",
    "mlx-community/granite-20b-code-base-8bit",
    "mlx-community/granite-20b-code-base-4bit",
    "mlx-community/granite-20b-code-instruct-4bit"
]

example_prompt_formats={
    "mistral": lambda prompt: f"""<s>[INST] {prompt} [/INST]""",
    "mixtral": lambda prompt: f"""<s>[INST] {prompt} [/INST]""",
}
default_prompt_format = lambda prompt: prompt

def format_prompt(model_name: str, prompt: str) -> str:
    for key in example_prompt_formats.keys():
        if key in model_name.lower():
            return example_prompt_formats[key](prompt)
    return default_prompt_format(prompt)
    
def parse_args() -> Tuple[str, str]:
    model_names_help = ", ".join(example_models)
    parser = argparse.ArgumentParser(
        prog='mlx-lm-example',
        description="Uses Apple's MLX library to download a model and do inference on the user-supplied prompt",
        epilog="""The rest of the arguments are considered a prompt. If there are none, 
        you will be asked to enter one or more prompts. 
        In that case, enter :q or :exit to quit. Example models: """)

    model_help = f"""Model name to use, e.g., {model_names_help}"""
        
    parser.add_argument('-m', '--model', help=model_help)
    parser.add_argument('-v', '--verbose', help='Enable verbose output',
                        action='store_true')
    parser.add_argument('prompt', nargs='*', help='prompt for the model')

    args, unknown = parser.parse_known_args()

    model_name=""
    if args.model:
        model_name=args.model
    else:
        q = f"Please enter a number between 1 and {len(example_models)}, inclusive, or q to quit:"
        while not model_name:
            print(q)
            for i in range(len(example_models)):
                print(f"{i+1}: {example_models[i]}")
            pick = input(">  ").strip()
            if pick == "q":
                exit(0)
            elif pick == "":
                pass
            else:
                try:
                    i = int(pick)-1
                    match i:
                        case i if i < 0 or i >= len(example_models): 
                            print(f"ERROR: invalid input: {pick}.", end=" ")
                        case i:
                            model_name=example_models[int(i)]
                except ValueError:
                    print(f"ERROR: invalid input: {pick}.", end=" ")

    if unknown:
        print(f"ERROR: Unknown arguments: {unknown}")
        exit(1)

    prompt = " ".join(args.prompt).strip()
    if prompt:
        prompt_msg = prompt
        if len(prompt_msg) > 40:
            prompt_msg = f"{prompt_msg[:40]}..."
        print(f"Using model {model_name} with prompt: \"{prompt_msg}\"")
    else:
        print(f"Using model {model_name}")
    return model_name, prompt, args.verbose

def prompt_loop(first_prompt: str, model_name: str, verbose: bool):
    prompt = first_prompt
    while prompt != ":q" and prompt!= ":exit":
        if prompt:
            prompt2 = format_prompt(model_name, prompt)
            if verbose:
                print(f"Full prompt: {prompt2}")
            response = generate(model, tokenizer, prompt=prompt2, verbose=verbose)
            print(response)
        if first_prompt:
            return
        prompt = input("prompt (:q or :exit to quit)> ")
        

if __name__ == "__main__":
    model_name, prompt, verbose = parse_args()
    model, tokenizer = load(model_name)
    prompt_loop(prompt, model_name, verbose)
