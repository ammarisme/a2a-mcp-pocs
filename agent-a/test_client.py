# client.py
from python_a2a import A2AClient, Message, TextContent, MessageRole

client = A2AClient("http://localhost:8001/a2a")
msg = Message(content=TextContent(text="Add 3 and 5"), role=MessageRole.USER)
resp = client.send_message(msg)
print("Agent replied:", resp.content.text)
