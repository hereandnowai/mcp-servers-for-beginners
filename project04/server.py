import requests
from mcp import McpServer, Tool

@Tool
def create_github_issue(repo_owner: str, repo_name: str, title: str, body: str, token: str) -> str:
    """
    Creates a new issue on a GitHub repository.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return "Issue created successfully!"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    server = McpServer(tools=[create_github_issue])
    server.run()
