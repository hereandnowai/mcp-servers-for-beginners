from mcp import McpClient

client = McpClient(port=8080)

# Example usage
response = client.query_db(query="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
print(response)

response = client.query_db(query="INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com')")
print(response)

response = client.query_db(query="SELECT * FROM users")
print(response)
