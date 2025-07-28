from mcp import McpClient

client = McpClient(port=8080)

# Example usage of secure_echo
response = client.secure_echo(message="Hello! This is a test with some special characters: !@#$%^&*()")
print(response)

# Example usage of secure_tool with a valid token
response = client.secure_tool(token="SECRET_TOKEN", data="This is some sensitive data.")
print(response)

# Example usage of secure_tool with an invalid token
response = client.secure_tool(token="WRONG_TOKEN", data="This should fail.")
print(response)
