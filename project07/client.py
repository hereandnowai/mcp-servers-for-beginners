from mcp import McpClient

client = McpClient(port=8080)

# Example usage
# Replace with your GitHub token, repository owner, and repository name
token = "YOUR_GITHUB_TOKEN"
repo_owner = "YOUR_USERNAME"
repo_name = "YOUR_REPO_NAME"

# First, let's add a user to the database
client.query_db(query="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
client.query_db(query="INSERT INTO users (name, email) VALUES ('Jane Doe', 'jane.doe@example.com')")

# Now, let's create a GitHub issue for this user
response = client.create_github_issue_from_db(user_id=1, repo_owner=repo_owner, repo_name=repo_name, token=token)
print(response)
