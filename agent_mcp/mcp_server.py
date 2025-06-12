from python_a2a.mcp import FastMCP, text_response
from python_a2a import run_server

mcp = FastMCP(
    name="calculator-mcp",
    description="Adds two numbers via MCP",
    version="1.0.0"
)

@mcp.tool(name="add", description="Add two integers")
def add_tool(params: dict) -> str:
    x = int(params["x"])
    y = int(params["y"])
    return text_response(str(x + y))

if __name__ == "__main__":
    run_server(mcp, host="0.0.0.0", port=8001)
