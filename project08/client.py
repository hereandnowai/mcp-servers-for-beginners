from mcp import McpClient
import time

client = McpClient(port=8080)

# This client will periodically check for new emails
while True:
    print("Checking for new emails...")
    response = client.check_emails_and_add_tasks()
    print(response)
    print("Current tasks:", client.list_tasks())
    time.sleep(60) # Check every minute
