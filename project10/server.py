from mcp import McpServer, Tool

# A simple in-memory key-value store to allow agents to communicate
data_store = {}

@Tool
def set_value(key: str, value: str) -> str:
    """
    Sets a value in the shared data store.
    """
    data_store[key] = value
    return f"Value set for key '{key}'."

@Tool
def get_value(key: str) -> str:
    """
    Gets a value from the shared data store.
    """
    return data_store.get(key, None)

if __name__ == "__main__":
    server = McpServer(tools=[set_value, get_value])
    server.run()
