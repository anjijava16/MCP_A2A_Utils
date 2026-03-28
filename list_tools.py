welcome@jaisairams-Laptop A2A_Examples % more /tmp/list_tools.py
#!/usr/bin/env python3
import json
import sys

try:
    import httpx
    import asyncio

    async def list_tools():
        headers = {"Accept": "application/json, text/event-stream"}
        async with httpx.AsyncClient(timeout=10) as client:
            # Initialize
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
            print("Init:", json.dumps(init_resp.json(), indent=2))
            
            # List tools
            tools_resp = await client.post(
                "http://localhost:7080/mcp",
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/list",
                    "params": {}
                },
                headers=headers
            )
            print("\nTools:", json.dumps(tools_resp.json(), indent=2))

    asyncio.run(list_tools())
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
