"""Custom tools for the weather agent."""

from __future__ import annotations

import json
from typing import Any

import httpx


MCP_URL = "http://localhost:7080/mcp"


async def _call_mcp_tool(tool_name: str, params: dict[str, Any]) -> str:
    headers = {"Accept": "application/json, text/event-stream"}

    async with httpx.AsyncClient(timeout=60) as client:
        init_response = await client.post(
            MCP_URL,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "weather-agent", "version": "0.1.0"},
                },
            },
            headers=headers,
        )

        session_id = init_response.headers.get("mcp-session-id")
        if not session_id:
            raise RuntimeError("MCP server did not return a session id.")

        response = await client.post(
            MCP_URL,
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": params},
            },
            headers={**headers, "mcp-session-id": session_id},
        )

    payload_text = response.text.strip()
    if not payload_text:
        raise RuntimeError("MCP weather tool returned an empty response.")

    tool_text_parts: list[str] = []
    for line in payload_text.splitlines():
        if not line.startswith("data: "):
            continue
        event_data = json.loads(line[6:])
        result = event_data.get("result")
        if not result:
            if "error" in event_data:
                raise RuntimeError(str(event_data["error"]))
            continue

        for item in result.get("content", []):
            if item.get("type") == "text" and item.get("text"):
                tool_text_parts.append(item["text"])

    if not tool_text_parts:
        return payload_text

    return "\n".join(tool_text_parts)


async def weather_search(city: str, country_code: str | None = None) -> dict[str, Any]:
    """Get current weather for a city.

    Args:
        city: City name to look up.
        country_code: Optional country code to disambiguate locations.

    Returns:
        A JSON-serializable dictionary with the weather lookup result.
    """

    arguments: dict[str, Any] = {"city": city}
    if country_code:
        arguments["country_code"] = country_code

    weather_text = await _call_mcp_tool("weather_search", arguments)
    return {"status": "success", "city": city, "country_code": country_code, "weather": weather_text}
