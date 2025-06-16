# langgraph_operator.py
import requests
from python_a2a.discovery import DiscoveryClient
from shared_context import ContextModel

class A2AContextCallNode:
    """
    LangGraph custom node: takes a ContextModel, POSTs it to the discovered A2A agent,
    and returns the updated ContextModel.
    """
    def __init__(self, registry_url: str):
        self.discovery = DiscoveryClient(agent_card=None)
        self.discovery.add_registry(registry_url)

    def run(self, ctx: ContextModel) -> ContextModel:
        # 1. Discover (once, cached under the hood)
        agents = self.discovery.discover()
        # filter by capability
        agent = next(
            a for a in agents
            if a.capabilities.get("google_a2a_compatible")
        )
        endpoint = f"{agent.url}/message"  # adjust path if your server uses a different route

        # 2. Blocking HTTP POST of full context
        payload = {
            "content": {"data": ctx.dict()},
            "role": "user",
            "conversation_id": ctx.userId
        }
        resp = requests.post(endpoint, json=payload)
        resp.raise_for_status()

        # 3. Load back into our model
        updated = resp.json()["content"]["data"]
        return ContextModel(**updated)
