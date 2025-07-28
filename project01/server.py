from mcp import McpServer, Tool

@Tool
def hello(name: str) -> str:
    """
    Returns a greeting to the given name.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    server = McpServer(tools=[hello])
    server.run()
