# Register a safety shield

from common import create_library_client

client = (
    create_library_client()
)  # or create_http_client() depending on the environment you picked

# Allowed "shield ids"
allowed_shield_ids = {
    'Llama-Guard-3-8B': 'meta-llama/Llama-Guard-3-8B', 
    'meta-llama/Llama-Guard-3-8B': 'meta-llama/Llama-Guard-3-8B', 
    'Llama-Guard-3-1B': 'meta-llama/Llama-Guard-3-1B', 
    # 'llama-guard3:1b': 'llama-guard3:1b', 
    'meta-llama/Llama-Guard-3-1B': 'meta-llama/Llama-Guard-3-1B', 
    'Llama-Guard-3-11B-Vision': 'meta-llama/Llama-Guard-3-11B-Vision', 
    'meta-llama/Llama-Guard-3-11B-Vision': 'meta-llama/Llama-Guard-3-11B-Vision'
}
#provider_shield_id = 'llama-guard3:1b' #'Llama-Guard-3-1B'
provider_shield_id = 'Llama-Guard-3-1B'
shield_id = "content_safety"

print(f"Before registering a shield: {client.shields.list()}")
client.shields.register(shield_id=shield_id, provider_shield_id=provider_shield_id)
print(f"After registering a shield: {client.shields.list()}")
client.shields.list()

# Run content through shield
response = client.safety.run_shield(
    shield_id=shield_id, 
    messages=[{"role": "user", "content": "User message here"}], 
    params = {}
)

if response.violation:
    print(f"Safety violation detected: {response.violation.user_message}")
