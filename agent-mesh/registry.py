from python_a2a.discovery import AgentRegistry, run_registry

registry = AgentRegistry(
    name="A2A Registry Server",
    description="Registry server for agent discovery"
)

if __name__ == "__main__":
    print("[registry] starting on 0.0.0.0:8000")
    run_registry(registry, host="0.0.0.0", port=8000)

# $ python registry.py
# [registry] starting on 0.0.0.0:8000
# … now listening for agent heartbeats …
