from agent_executor import HelloWorldAgent
from python_a2a import run_server

if __name__ == "__main__":
    agent = HelloWorldAgent()
    run_server(agent, host="0.0.0.0", port=9999)
