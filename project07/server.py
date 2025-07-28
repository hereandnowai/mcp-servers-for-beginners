import sqlite3
import requests
from mcp import McpServer, Tool

@Tool
def get_user_from_db(user_id: int) -> dict:
    """
    Fetches a user from the database by their ID.
    """
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {"id": user[0], "name": user[1], "email": user[2]}
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

@Tool
def create_github_issue_from_db(user_id: int, repo_owner: str, repo_name: str, token: str) -> str:
    """
    Fetches a user from the database and creates a GitHub issue with their information.
    """
    user = get_user_from_db(user_id)
    if not user or "error" in user:
        return "Error: User not found or database error."

    title = f"New User: {user['name']}"
    body = f"A new user has been added to the database:\n\nName: {user['name']}\nEmail: {user['email']}"

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
    server = McpServer(tools=[get_user_from_db, create_github_issue_from_db])
    server.run()
