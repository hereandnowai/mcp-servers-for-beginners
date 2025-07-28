from mcp import McpClient

client = McpClient(port=8080)

response = client.hello(name="World")
print(response)
