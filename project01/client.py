# client.py
import asyncio
from fastmcp import Client

async def main():
    # Create a client instance pointing to the running server URL
    client = Client("http://127.0.0.1:6274")

    # Use an async context manager to handle the connection
    async with client:
        print("Pinging server...")
        await client.ping()
        print("Server is reachable.")

        # Execute the 'hello' tool
        print("Calling 'hello' tool...")
        result = await client.tools.hello(name="World")
        print(f"Result of hello(name='World'): {result}")

if __name__ == "__main__":
    asyncio.run(main())