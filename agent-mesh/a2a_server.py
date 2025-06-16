# a2a_server.py
import json
from python_a2a import AgentCard, A2AServer, run_server, Message, MessageRole, TextContent
from shared_context import ContextModel
from python_a2a.discovery import enable_discovery  # <<— you need this import


class ContextualAgent(A2AServer):
    def __init__(self, name: str, url: str):
        card = AgentCard(
            name=name,
            description="A2A agent that echoes and updates conversationHistory",
            url=url,
            version="1.0.0",
            capabilities={
                "google_a2a_compatible": True,
                "parts_array_format": True,
            }
        )
        super().__init__(agent_card=card)

    def handle_message(self, message: Message) -> Message:
        # 1) Parse the incoming JSON from TextContent
        incoming_str = message.content.text
        print("A2A agent recieved message " +incoming_str)
        incoming = json.loads(incoming_str)
        ctx = ContextModel(**incoming)

        # 2) Mutate your context however you like
        print("A2A agent mutating the context")
        latest_user = ctx.conversationHistory[-1]["text"]
        ctx.conversationHistory.append({
            "role": "agent",
            "text": f"Agent got: {latest_user}"
        })
        print(f"Updated context : {ctx.conversationHistory}")

        # 3) Return the full, updated context as JSON‐string in TextContent
        return Message(
            content=TextContent(text=json.dumps(ctx.dict())),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

# if __name__ == "__main__":
#     print("Starting agent on http://0.0.0.0:8001")
#     agent = ContextualAgent(name="CtxAgent", url="http://localhost:8001")
#     run_server(agent, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001
    agent = ContextualAgent(name="CtxAgent", url=f"http://localhost:{port}")

    # register with the registry **before** run_server()
    disc = enable_discovery(agent, registry_url="http://localhost:8000")

    print(f"Starting agent on http://{host}:{port}")
    run_server(agent, host=host, port=port)