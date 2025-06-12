from a2a.sdk import A2AClient

agent_b = A2AClient.discover("http://localhost:5001")
task = agent_b.create_task(
    action="summarize-text",
    input={"text": "..."}
)
result = task.wait_for_completion()
print(result.output)
