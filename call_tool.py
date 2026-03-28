#!/usr/bin/env python3
"""
Script to call MCP tools via mcp.json configuration.
Usage: python3 call_tool.py <tool_name> <json_params>
Example: python3 call_tool.py tavily_search '{"query": "latest news", "include_answer": true, "max_results": 5}'
"""

import httpx
import asyncio
import json
import sys

async def call_mcp_tool(tool_name: str, params: dict):
    headers = {"Accept": "application/json, text/event-stream"}
    
    async with httpx.AsyncClient(timeout=60) as client:
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
                    "clientInfo": {"name": "tool-caller", "version": "1.0.0"}
                }
            },
            headers=headers
        )
        
        # Get session ID
        session_id = init_resp.headers.get("mcp-session-id")
        session_headers = {**headers, "mcp-session-id": session_id}
        
        # Call tool
        response = await client.post(
            "http://localhost:7080/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": params
                }
            },
            headers=session_headers
        )
        
        print(f"Status: {response.status_code}\n")
        
        for line in response.text.strip().split('\n'):
            if line.startswith('data: '):
                data_json = line[6:]
                data = json.loads(data_json)
                
                if "result" in data:
                    result = data["result"]
                    if "content" in result:
                        for item in result["content"]:
                            if item.get("type") == "text":
                                print(item["text"])
                elif "error" in data:
                    print(f"Error: {data['error']}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 call_tool.py <tool_name> [json_params]")
        print("\nAvailable tools:")
        print("  1. tavily_search")
        print("     Params: query (str), include_answer (bool), max_results (int)")
        print("  2. get_crypto_prices")
        print("     Params: symbols (str), vs_currency (str)")
        print("  3. get_exchange_rate")
        print("     Params: currency_from (str), currency_to (str), currency_date (str)")
        print("  4. weather_search")
        print("     Params: city (str), country_code (str)")
        print("\nExample:")
        print('  python3 call_tool.py tavily_search \'{"query": "AI news", "include_answer": true, "max_results": 3}\'')
        sys.exit(1)
    
    tool_name = sys.argv[1]
    
    if len(sys.argv) > 2:
        params = json.loads(sys.argv[2])
    else:
        params = {}
    
    asyncio.run(call_mcp_tool(tool_name, params))

if __name__ == "__main__":
    main()
