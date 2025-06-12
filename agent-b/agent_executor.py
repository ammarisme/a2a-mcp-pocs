from python_a2a import A2AServer, Message, TextContent, MessageRole

class HelloWorldAgent(A2AServer):
    def handle_message(self, message: Message) -> Message:
        return Message(
            content=TextContent(text="Hello World"),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )
