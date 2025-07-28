from mcp import McpServer, Tool
import re

def sanitize_input(input_string: str) -> str:
    """
    A basic sanitizer to remove potentially harmful characters.
    This is a very basic example and should be expanded for production use.
    """
    # Remove characters that are not alphanumeric, space, or basic punctuation
    return re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', input_string)

@Tool
def secure_echo(message: str) -> str:
    """
    Echoes back a sanitized message.
    """
    sanitized_message = sanitize_input(message)
    return f"Sanitized message: {sanitized_message}"

def authenticate(token: str) -> bool:
    """
    A simple authentication function.
    In a real application, this would involve checking a database or other secure storage.
    """
    return token == "SECRET_TOKEN"

@Tool
def secure_tool(token: str, data: str) -> str:
    """
    A tool that requires authentication.
    """
    if not authenticate(token):
        return "Error: Authentication failed."
    
    sanitized_data = sanitize_input(data)
    return f"Authenticated and processed data: {sanitized_data}"


if __name__ == "__main__":
    server = McpServer(tools=[secure_echo, secure_tool])
    server.run()
