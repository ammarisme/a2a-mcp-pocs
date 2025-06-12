from python_a2a.discovery import AgentRegistry, run_registry

# Create a registry
registry = AgentRegistry(
    name="A2A Registry Server",
    description="Registry server for agent discovery"
)

# Run the registry server
run_registry(registry, host="0.0.0.0", port=8000)