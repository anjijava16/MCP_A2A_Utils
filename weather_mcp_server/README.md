# MCP Weather Server 🌤️

## Overview
A FastMCP-based server that provides real-time weather information integration. This server connects to the National Weather Service (NWS) API to fetch weather data, forecasts, and alerts for any location.

## Features
- **Real-time Weather Data**: Get current weather conditions for any location
- **Weather Alerts**: Retrieve active weather alerts and warnings
- **Forecast Information**: Access detailed weather forecasts
- **NWS API Integration**: Uses the National Weather Service API for accurate data

## Tools Available
- `get_weather(location)` - Get current weather for a location
- `get_alerts()` - Retrieve active weather alerts
- `get_forecast(location)` - Get weather forecast for a location

## Setup & Usage

### Installation
```bash
pip install fastmcp httpx
```

### Running the Server
```bash
# Stdio transport (for Claude Desktop)
python weather.py

# SSE transport (for HTTP clients)
# Typically runs on port 8000
```

### Example Usage
```python
from mcp.server.fastmcp import FastMCP

# The server provides tools for:
# - Querying weather by location
# - Getting weather alerts
# - Retrieving forecast data
```

## Configuration
- **API Base**: Uses National Weather Service API (https://api.weather.gov)
- **User Agent**: weather-app/1.0
- **Timeout**: 30 seconds for API requests

## Files
- `weather.py` - Main weather server implementation
- `welcome_mcp.py` - Alternative implementation

## Dependencies
- fastmcp
- httpx
- mcp

## Error Handling
- Graceful handling of invalid locations
- Timeout management for API requests
- Proper error responses for failed queries
