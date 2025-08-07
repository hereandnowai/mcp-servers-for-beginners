import asyncio, httpx

REMOTE = "http://localhost:8000/mcp"

async def main():
    async with httpx.AsyncClient(headers={
        "Content-Type": "application/json",
        "MCP-Protocol-Version": "2025-06-18"
    }) as c:
        init = await c.post(REMOTE, json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{}})
        sid = init.headers.get("Mcp-Session-Id")
        resp = await c.post(REMOTE, headers={"Mcp-Session-Id": sid}, json={
            "jsonrpc":"2.0","id":2,"method":"call_tool","params":{
                "tool_name":"fetch_markdown","arguments":{"url":"https://example.com"}
            }
        })
        print(resp.json().get("result"))

asyncio.run(main())