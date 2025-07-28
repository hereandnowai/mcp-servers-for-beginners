import requests
from mcp import McpServer, Tool

@Tool
def send_slack_message(channel: str, message: str, token: str) -> str:
    """
    Sends a message to a Slack channel.
    """
    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {token}"},
            json={"channel": channel, "text": message}
        )
        response.raise_for_status()
        return "Message sent successfully"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    server = McpServer(tools=[send_slack_message])
    server.run()
