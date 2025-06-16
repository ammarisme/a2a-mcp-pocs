# run_client.py
import json
import requests
from python_a2a import Message, TextContent, MessageRole
from python_a2a.discovery import DiscoveryClient
from shared_context import ContextModel

def main():
    # 1) Build your initial ContextModel
    ctx = ContextModel(
        schemaVersion="v1",
        userId="user123",
        conversationHistory=[{"role": "user", "text": "Hello, agent!"}]
    )

    # 2) Discover the A2A agent
    disc = DiscoveryClient(agent_card=None)
    disc.add_registry("http://localhost:8000")
    agents = disc.discover()

    print("🔍 Discovered agents:")
    for a in agents:
        print(f" • {a.name} @ {a.url} → capabilities={a.capabilities}")
    if not agents:
        print("❌  No agents found.")
        return

    agent = next(a for a in agents if a.capabilities.get("google_a2a_compatible"))

    # 3) Send the full context as JSON string to /a2a
    endpoint = f"{agent.url}/a2a"
    payload = {
        "content": {"type": "text", "text": json.dumps(ctx.model_dump())},
        "role": "user",
        "conversation_id": ctx.userId
    }
    resp = requests.post(endpoint, json=payload)
    resp.raise_for_status()

    # 4) Extract the JSON-string from the 'parts' array
    body = resp.json()

    # Find the first text part
    parts = body.get("parts", [])
    if not parts:
        raise RuntimeError(f"No parts in response: {body}")
    # look for a part with type 'text'
    text_part = next((p for p in parts if p.get("type") == "text"), parts[0])
    updated_str = text_part["text"]

    # 5) Parse and print the updated context
    updated = json.loads(updated_str)
    print("Updated context:")
    print(json.dumps(updated, indent=2))


if __name__ == "__main__":
    main()
