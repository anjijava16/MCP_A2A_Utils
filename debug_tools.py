#!/usr/bin/env python3
import httpx
import asyncio
import sys

async def list_tools():
    headers = {"Accept": "application/json, text/event-stream"}
    async with httpx.AsyncClient(timeout=10) as client:
        # Initialize
        try:
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
            print(f"Status: {init_resp.status_code}")
            print(f"Raw response: {init_resp.text}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

asyncio.run(list_tools())