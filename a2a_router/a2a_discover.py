from python_a2a.discovery import DiscoveryClient, AgentRegistry

# Create a discovery client (without registering)
discovery_client = DiscoveryClient(agent_card=None)  # You can also pass your own agent card
discovery_client.add_registry("http://localhost:8000")

# Discover all agents
agents = discovery_client.discover()

for agent in agents:
    print(f"Found agent: {agent.name} at {agent.url}")
    print(f"Capabilities: {agent.capabilities}")

# You can also filter agents by capabilities
weather_agents = [agent for agent in agents
                 if agent.capabilities.get("weather_forecasting")]

for agent in weather_agents:
    print(f"Found weather agent: {agent.name} at {agent.url}")