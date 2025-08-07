from mcp import McpClient
import random
import time

client = McpClient(port=8080)

print("Agent 1: Performing a complex calculation...")
time.sleep(2) # Simulate work
result = random.randint(1, 100)
print(f"Agent 1: Calculation complete. Result is {result}.")

print("Agent 1: Storing result on the server.")
response = client.set_value(key="calculation_result", value=str(result))
print(f"Agent 1: Server response: {response}")


