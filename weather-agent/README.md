# Weather Agent

Prototype Google ADK agent that answers weather questions by calling the workspace MCP `weather_search` tool.

## What it does

- Answers current weather questions for a city
- Asks for missing location details instead of guessing
- Keeps responses concise and factual

## Requirements

- Python 3.10+
- Access to the workspace MCP server at `http://localhost:7080/mcp`
- A Google model setup for ADK, such as `GOOGLE_API_KEY` or Vertex AI credentials

## Run

```bash
python3 -m pip install -e .
adk web .
```

## Tool

The agent calls the existing MCP tool:

- `weather_search` with `city` and optional `country_code`
