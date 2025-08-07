# server.py
from mcp.server.fastmcp import FastMCP

# 1. Initialize the FastMCP server
mcp = FastMCP("HelloWorldServer")

# 2. Define a tool using the @mcp.tool() decorator
@mcp.tool()
def hello(name: str) -> str:
    """
    Returns a greeting to the given name.
    """
    return f"Hello, {name}!"

# To run this server, use the command:
# mcp dev server.py 