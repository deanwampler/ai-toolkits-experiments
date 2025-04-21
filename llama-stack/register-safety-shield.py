# Register and use a safety shield

from common import create_library_client

client = (
    create_library_client()
)  # or create_http_client() depending on the environment you picked

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
provider_shield_id = 'llama-guard-basic'

# Trying one of the allowed types, e.g., the two definitions for provider_shield_id commented out below
# gets past the register error, but then it fails during the "run_shield" step, even though the list of
# shields printed previously contains 'Llama-Guard-3-1B'!!
# provider_shield_id = 'Llama-Guard-3-1B'
# provider_shield_id = 'meta-llama/Llama-Guard-3-1B'

shield_id = "content_safety"

print(f"Before registering a shield, here is the current list of shields: {client.shields.list()}")
client.shields.register(shield_id=shield_id, provider_shield_id=provider_shield_id)
print(f"After registering a shield, here is the current list of shields: {client.shields.list()}")
client.shields.list()

# Run content through a shield.
# NOTE: the website example doesn't include the "params" argument, but it appears to be required.
response = client.safety.run_shield(
    shield_id=shield_id, 
    messages=[{"role": "user", "content": "User message here"}], 
    params = {}
)

if response.violation:
    print(f"Safety violation detected: {response.violation.user_message}")
