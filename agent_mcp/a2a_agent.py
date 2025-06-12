from python_a2a import A2AServer, Message, MessageRole, TextContent, run_server
from python_a2a.mcp import MCPClient
import asyncio

class CalculatorAgent(A2AServer):
    def __init__(self, mcp_url: str):
        super().__init__()
        self.mcp = MCPClient(mcp_url)

    def handle_message(self, message: Message) -> Message:
        user_text = message.content.text.lower()
        try:
            # Extract numbers from text like "add 3 and 5"
            parts = [int(p) for p in user_text.split() if p.isdigit()]
            if len(parts) < 2:
                reply = "Please provide two numbers."
            else:
                x, y = parts[:2]
                result = asyncio.run(self.mcp.call_tool("add", {"x": x, "y": y}))

                reply = f"The answer is {result}"
        except Exception as e:
            reply = f"Error: {str(e)}"

        return Message(
            content=TextContent(text=reply),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

if __name__ == "__main__":
    agent = CalculatorAgent("http://localhost:8001")
    run_server(agent, host="0.0.0.0", port=8000)
