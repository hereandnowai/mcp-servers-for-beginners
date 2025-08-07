from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

server_params = StdioServerParameters(
    command="python",              # The executable to run
    args=["calculator_server.py"], # The server script (you’ll need to create this)
    env=None                       # Optional: environment variables (None uses defaults)
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("\n=== Available Tools ===")
            for tool in tools:
                print(f"- {tool}")
            print("========================\n")

            expression = input("Enter a math expression (e.g., '5 * 7'): ")

            result = await session.call_tool(
                "evaluate_expression",
                arguments={"expression": expression}
            )
            result = result.content[0].text
            print("\n=== Calculation Result ===")
            print(f"Expression: {expression}")
            print(f"Result: {result}")
            print("==========================\n")

if __name__ == "__main__":
    asyncio.run(run())