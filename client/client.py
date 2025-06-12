from python_a2a import A2AClient, Message, TextContent, MessageRole

client = A2AClient("http://localhost:8000/a2a")
msg = Message(content=TextContent(text="Add 3 and 5"), role=MessageRole.USER)

response = client.send_message(msg)
print("Agent replied:", response.content.text)
