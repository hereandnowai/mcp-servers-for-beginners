from mcp import McpClient

client = McpClient(port=8080)

# Example usage
# Replace with your Slack bot token and channel name
token = "YOUR_SLACK_BOT_TOKEN"
channel = "#general"
message = "Hello from MCP!"

response = client.send_slack_message(channel=channel, message=message, token=token)
print(response)
