# Use a safety shield with optional registration

import argparse, sys
import readline  # enhances the input() function with real command-line editing, history, etc.
from common import create_library_client

# Allowed "shield ids", from an error message printed if you specify something unrecognized!
allowed_shield_ids = {
    'meta-llama/Llama-Guard-3-8B': 'meta-llama/Llama-Guard-3-8B',
    'meta-llama/Llama-Guard-3-1B': 'meta-llama/Llama-Guard-3-1B',
    'Llama-Guard-3-1B': 'meta-llama/Llama-Guard-3-1B',
    'meta-llama/Llama-Guard-3-11B-Vision': 'meta-llama/Llama-Guard-3-11B-Vision',
    'Llama-Guard-3-11B-Vision': 'meta-llama/Llama-Guard-3-11B-Vision',
}

# While the following is shown in the example code, the `register` attempt below fails with an error:
# "ValueError: Unsupported Llama Guard type: llama-guard-basic. Allowed types: {...}"
# where I captured the allowed types in the allowed_shield_ids above.
# def_provider_shield_id = 'llama-guard-basic'
# def_provider_shield_id = 'llama-guard'

# Trying one of the allowed types, e.g., the two definitions for def_provider_shield_id commented out below
# gets past the register error, but then it fails during the "run_shield" step, even though the list of
# shields printed previously contains 'Llama-Guard-3-1B'!!
def_provider_shield_id = 'Llama-Guard-3-1B'
# def_provider_shield_id = 'meta-llama/Llama-Guard-3-1B'

parser = argparse.ArgumentParser(
                    prog='safety-shield',
                    description='An extended version of the Llama Stack safety shield example here: https://llama-stack.readthedocs.io/en/latest/building_applications/safety.html',
                    epilog='')
parser.add_argument('--id', '--provider-shield-id', 
                    default=def_provider_shield_id,
                    help=f"The 'provider' shield id. (default: {def_provider_shield_id})")
parser.add_argument('-r', '--register',
                    help="Register the 'provider' shield id. If not provided, assumes it is already registered.",
                    action='store_true')  # on/off flag
parser.add_argument('-l', '--list',
                    help="List the current list of registered shields.",
                    action='store_true')  # on/off flag
parser.add_argument('-v', '--verbose',
                    help="Show verbose output",
                    action='store_true')  # on/off flag
parser.add_argument('prompt', nargs='*',
                    help="The rest of the arguments form a user prompt to test against the shield. If not provided, you'll be prompted.")
args = parser.parse_args(sys.argv[1:])

client = (
    create_library_client()
)  # or create_http_client() depending on the environment you picked

shield_id = "content_safety"

if args.register:
    if args.list:
        print(f"Before registering a shield, here is the current list of shields: {client.shields.list()}")
    client.shields.register(shield_id=shield_id, provider_shield_id=args.id)
if args.list:
    print(f"Current list of shields: {client.shields.list()}")

# Run the prompt through a shield (or ask for the prompts).

def check_prompt(prompt):
    if args.verbose:
        print(f"prompt> {prompt}")
    # NOTE: the website example doesn't include the "params" argument, but it appears to be required.
    response = client.safety.run_shield(
        shield_id=shield_id, 
        messages=[{"role": "user", "content": prompt}], 
        params = {}
    )
    if response.violation:
        print(f"Safety violation detected: {response.violation.user_message}")
    else:
        print("No violation detected")

if len(args.prompt) > 0:
    check_prompt(' '.join(args.prompt))
else:
    print("\nEnter your prompts. When finished, enter a blank line or ^D.")
    user_prompt = " "
    while True:
        try:
            user_prompt = input("Your prompt> ")
            if user_prompt == "":
                print("Finished!")
                break
            check_prompt(user_prompt)
        except EOFError:
            if args.verbose:
                print("Finished!")
            break
