from mcp import McpClient

client = McpClient(port=8080)

# Example usage
# Replace with your GitHub token, repository owner, and repository name
token = "YOUR_GITHUB_TOKEN"
repo_owner = "YOUR_USERNAME"
repo_name = "YOUR_REPO_NAME"
title = "Test Issue"
body = "This is a test issue created by the MCP client."

response = client.create_github_issue(repo_owner=repo_owner, repo_name=repo_name, title=title, body=body, token=token)
print(response)
