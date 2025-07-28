from mcp import McpClient
import time

client = McpClient(port=8080)

print("Agent 2: Waiting for result from Agent 1...")
result = None
while result is None:
    result = client.get_value(key="calculation_result")
    if result is None:
        print("Agent 2: Result not ready yet. Waiting...")
        time.sleep(2)

print(f"Agent 2: Got result from Agent 1: {result}")
print("Agent 2: Performing another action with the result.")
final_result = int(result) * 2
print(f"Agent 2: Final result is {final_result}.")
