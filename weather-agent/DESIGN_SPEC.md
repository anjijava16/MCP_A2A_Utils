# DESIGN_SPEC.md

## Overview
Create a prototype Google ADK agent that answers weather questions for cities. The agent should take a city name, optionally a country code, and return the current weather conditions in a concise, user-friendly format.

The agent will use the existing workspace MCP weather tool rather than scraping websites or making unsupported guesses. It should focus on direct weather lookup and brief clarifications when the user’s location is ambiguous.

## Example Use Cases
1. “What’s the weather in Chennai?” → return current temperature, condition, and a short summary.
2. “Weather in London, UK” → use city plus country code when available.
3. “Is it raining in Pune right now?” → answer with current conditions if the weather source exposes precipitation details.
4. “Weather” → ask a clarifying question for the city.
5. “Weather in Springfield” → request country/state clarification if multiple locations are possible.

## Tools Required
- Workspace MCP `weather_search` tool for current weather lookup.
- No external write operations.
- No deployment tooling for this prototype.

## Constraints & Safety Rules
- Do not invent weather data.
- If the city is missing, ask for the city before calling tools.
- If multiple locations are possible, ask for a country code or region.
- Keep responses short unless the user asks for detail.
- Do not provide travel, safety, or emergency advice beyond the weather facts unless asked.

## Success Criteria
- The agent can answer weather queries for a city with a clear current-condition summary.
- The agent asks for missing location details instead of guessing.
- The agent handles ambiguous city names gracefully.
- The agent uses the weather tool rather than fabricated or static responses.

## Edge Cases to Handle
- Missing city name.
- Ambiguous city names across multiple countries.
- Weather lookup failures or unavailable data.
- Non-weather queries, which should be redirected back to weather help.
- Requests that ask for forecasts beyond what the tool can provide, handled by explaining the limitation.
