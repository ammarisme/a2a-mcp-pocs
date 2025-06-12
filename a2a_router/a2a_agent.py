from python_a2a import AgentCard, A2AServer, run_server, Message, TextContent, MessageRole
from python_a2a.discovery import AgentRegistry, run_registry, enable_discovery
import threading

# Create a simple agent that will register with the registry
class SampleAgent(A2AServer):
    """A sample agent that registers with the registry."""

    def __init__(self, name: str, description: str, url: str):
        """Initialize the sample agent."""
        agent_card = AgentCard(
            name=name,
            description=description,
            url=url,
            version="1.0.0",
            capabilities={
                "streaming": False,
                "pushNotifications": False,
                "stateTransitionHistory": False,
                "google_a2a_compatible": True,
                "parts_array_format": True
            }
        )
        super().__init__(agent_card=agent_card)

    def handle_message(self, message: Message) -> Message:
        """Handle incoming messages."""
        return Message(
            content=TextContent(
                text=f"Hello from {self.agent_card.name}! I received: {message.content.text}"
            ),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

registry_port = 8000

# Create and run an agent that registers with the registry
agent = SampleAgent(
    name="Sample Agent",
    description="Sample agent that demonstrates discovery",
    url="http://localhost:8001"
)

# Enable discovery - this registers the agent with the registry
registry_url = f"http://localhost:{registry_port}"
discovery_client = enable_discovery(agent, registry_url=registry_url)

# Run the agent
run_server(agent, host="0.0.0.0", port=8001)