import sys
import asyncio
import anyio
import traceback
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp.client.session import ClientSession
from mcp.shared.message import SessionMessage

async def stdio_to_stream(stream: MemoryObjectSendStream[SessionMessage]):
    """Reads from stdin and pushes messages to the memory stream."""
    try:
        async with anyio.wrap_file(sys.stdin.buffer) as f:
            while True:
                line = await f.readline()
                if not line:
                    break
                try:
                    msg = SessionMessage.model_validate_json(line)
                    await stream.send(msg)
                except Exception as e:
                    print(f"Client Error reading from stdin: {e}", file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
    except Exception as e:
        print(f"Client Error in stdio_to_stream: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)


async def stream_to_stdio(stream: MemoryObjectReceiveStream[SessionMessage]):
    """Reads from the memory stream and writes messages to stdout."""
    try:
        async with anyio.wrap_file(sys.stdout.buffer) as f:
            async for message in stream:
                await f.write(message.model_dump_json().encode('utf-8') + b'\n')
                await f.flush()
    except Exception as e:
        print(f"Client Error in stream_to_stdio: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

async def main():
    client_to_server_send, client_to_server_receive = anyio.create_memory_object_stream[SessionMessage]()
    server_to_client_send, server_to_client_receive = anyio.create_memory_object_stream[SessionMessage]()

    client = ClientSession(server_to_client_receive, client_to_server_send)

    try:
        async with anyio.create_task_group() as tg:
            tg.start_soon(stdio_to_stream, server_to_client_send)
            tg.start_soon(stream_to_stdio, client_to_server_receive)

            await client.initialize()
            print("Calling run_finance_agent_stock_price on the server...", file=sys.stderr)
            
            response = await client.call_tool(
                "run_finance_agent_stock_price",
                {"input_query": "What are the current stock prices of Google (GOOG) and Reliance Industries (RELIANCE.NS)?"}
            )
            
            print("Server Response:", file=sys.stderr)
            print(response, file=sys.stderr)
            
            client_to_server_send.close()
            server_to_client_send.close()
            tg.cancel_scope.cancel()

    except Exception as e:
        print(f"An error occurred in client main: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client exiting.", file=sys.stderr)
