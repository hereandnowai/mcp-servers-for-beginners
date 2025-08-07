from mcp import McpClient

client = McpClient(port=8080)

# Example usage
response = client.read_file(path="sample.txt")
print(response)