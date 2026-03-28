
import httpx
import asyncio
import json

async def list_tools():
    headers = {"Accept": "application/json, text/event-stream"}
    
    async with httpx.AsyncClient(timeout=30) as client:
        # Initialize first
        init_resp = await client.post(
            "http://localhost:7080/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "list-tools", "version": "1.0.0"}
                }
            },
            headers=headers
        )
        
        # Get session ID from response header
        session_id = init_resp.headers.get("mcp-session-id")
        print(f"Session ID: {session_id}\n")
        
        # Add session ID to headers for subsequent requests
        session_headers = {**headers, "mcp-session-id": session_id}
        
        # List tools
        response = await client.post(
            "http://localhost:7080/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            },
            headers=session_headers
        )
        
        print(f"Tools status: {response.status_code}\n")
        
        for line in response.text.strip().split('\n'):
            if line.startswith('data: '):
                data_json = line[6:]
                data = json.loads(data_json)
                
                if "result" in data and "tools" in data["result"]:
                    print("Available Tools:")
                    print("=" * 60)
                    for tool in data["result"]["tools"]:
                        print(f"\n✓ {tool['name']}")
                        if "description" in tool:
                            print(f"  Description: {tool['description']}")
                        if "inputSchema" in tool:
                            props = tool["inputSchema"].get("properties", {})
                            if props:
                                print(f"  Parameters: {', '.join(props.keys())}")

asyncio.run(list_tools())
