from mcp import McpServer, Tool
import os

@Tool
def read_file(path: str) -> str:
    """
    Reads the content of a file at the given path.
    """
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {path}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    server = McpServer(tools=[read_file])
    server.run()
