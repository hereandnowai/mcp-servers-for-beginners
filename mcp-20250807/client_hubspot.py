import os, asyncio, httpx
from dotenv import load_dotenv
load_dotenv()

REMOTE = os.getenv("HUBSPOT_MCP_URL")  # e.g. http://localhost:3000/mcp or deployed URL
TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
SID = None  # populated on initialize

async def api(method, params):
    global SID
    payload = {"jsonrpc":"2.0","id":1,"method":method,"params":params}
    headers = {"MCP-Protocol-Version":"2025-06-18","Content-Type":"application/json"}
    if TOKEN: headers["Authorization"]=f"Bearer {TOKEN}"
    if SID: headers["Mcp-Session-Id"]=SID
    async with httpx.AsyncClient(headers=headers) as c:
        r = await c.post(REMOTE, json=payload)
        r.raise_for_status()
        SID = SID or r.headers.get("Mcp-Session-Id")
        return r.json().get("result")

async def main():
    await api("initialize", {})
    res = await api("hubspot_create_contact", {"properties": {"email":"jane.doe@example.com","firstname":"Jane","lastname":"Doe"}})
    print("Response:", res)

if __name__=="__main__":
    asyncio.run(main())