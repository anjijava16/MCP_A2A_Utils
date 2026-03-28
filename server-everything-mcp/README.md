# Server Everything MCP 🌍

## Overview
A comprehensive umbrella MCP server that aggregates and provides access to all available MCP servers and tools. This serves as a central hub and discovery mechanism for the entire MCP ecosystem.

## Features
- **Tool Aggregation**: Centralized access to all tools
- **Service Discovery**: Automatic tool and server discovery
- **Unified Interface**: Single entry point for all operations
- **Tool Caching**: Cache tool definitions for performance
- **Health Monitoring**: Monitor connected servers
- **Dynamic Loading**: Load new servers on demand

## Architecture

```
Server Everything MCP (Hub)
├── Tool Registry
├── Server Manager
├── Connection Pool
├── Health Monitor
└── Discovery Engine

Connected Servers:
├── Weather Server
├── Search Server
├── Database Server
├── AWS Server
└── ... (all others)
```

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp
```

### Configuration
Create configuration file:
```yaml
servers:
  weather:
    url: http://localhost:8001/sse
    enabled: true
  search:
    url: http://localhost:8002/sse
    enabled: true
  database:
    url: http://localhost:8003/sse
    enabled: true
```

### Running
```bash
python server_everything.py
```

## Tools Available

### Discovery Tools
- `list_all_tools()` - List all available tools
- `describe_tool(tool_name)` - Get tool description
- `find_tools_by_category(category)` - Find tools by type
- `search_tools(keyword)` - Search tools by keyword

### Server Management
- `list_servers()` - List connected servers
- `get_server_status(server_name)` - Check server health
- `add_server(url, name)` - Register new server
- `remove_server(name)` - Unregister server

### Tool Execution
- `call_tool(tool_name, args)` - Execute tool
- `batch_call_tools(tools_list)` - Execute multiple tools
- `call_tool_on_server(server, tool, args)` - Direct server call

### Caching
- `clear_tool_cache()` - Clear cached tools
- `get_cache_stats()` - Cache statistics
- `set_cache_ttl(ttl)` - Set cache time-to-live

## Tool Discovery

### List All Tools
```python
all_tools = list_all_tools()
# Returns: [
#   {"name": "get_weather", "server": "weather_server", ...},
#   {"name": "search", "server": "search_server", ...},
#   ...
# ]
```

### Search Tools
```python
# Find weather-related tools
weather_tools = find_tools_by_category("weather")

# Search for specific tools
search_tools = search_tools("weather")
```

### Tool Descriptions
```python
# Get detailed tool info
tool_info = describe_tool("get_weather")
# Returns: {
#   "name": "get_weather",
#   "description": "...",
#   "parameters": {...},
#   "server": "weather_server"
# }
```

## Server Management

### Add Server
```python
add_server(
    url="http://localhost:8004/sse",
    name="new_service",
    category="services"
)
```

### Server Health
```python
status = get_server_status("weather_server")
# Returns: {
#   "status": "healthy",
#   "uptime": 3600,
#   "tool_count": 42,
#   "last_seen": "2024-01-01T12:00:00"
# }
```

## Tool Execution

### Single Tool Call
```python
result = call_tool(
    "get_weather",
    {"location": "NYC"}
)
```

### Batch Operations
```python
results = batch_call_tools([
    ("get_weather", {"location": "NYC"}),
    ("search", {"query": "NLP"}),
    ("get_stock_price", {"symbol": "AAPL"})
])
```

### Direct Server Call
```python
result = call_tool_on_server(
    server="weather_server",
    tool="get_weather",
    args={"location": "NYC"}
)
```

## Tool Categories

### By Domain
- **Weather**: Weather queries, forecasts, alerts
- **Search**: Web search, local search, news
- **Finance**: Stock prices, currency conversion, crypto
- **Database**: SQL queries, data management
- **Cloud**: AWS, GCP, Azure operations
- **Analytics**: Data analysis, statistics
- **Communication**: Email, messaging, notifications

## Performance Optimization

### Tool Caching
```python
# Tools cached with TTL
cache_stats = get_cache_stats()
# Returns: {
#   "cached_tools": 150,
#   "cache_size_mb": 2.5,
#   "hit_rate": 0.85,
#   "miss_rate": 0.15
# }

# Adjust TTL
set_cache_ttl(3600)  # 1 hour
```

### Connection Pooling
```python
# Automatic connection pooling
# - Reuses connections
# - Manages pool sizes
# - Handles cleanup
```

### Batch Processing
```python
# Execute multiple tools efficiently
# - Parallelizes where possible
# - Manages dependencies
# - Returns ordered results
```

## Monitoring & Health

### Server Health Monitoring
```python
all_servers = list_servers()

for server in all_servers:
    status = get_server_status(server)
    print(f"{server}: {status['status']}")
    
    if status['status'] != 'healthy':
        # Alert or handle
        handle_unhealthy_server(server)
```

### Metrics
- Total tools available
- Server health status
- Average response time
- Cache hit rate
- Error rate by tool

## API Examples

### Discovery
```python
# Find all available tools
all_tools = list_all_tools()

# Group by category
by_category = {}
for tool in all_tools:
    cat = tool.get('category', 'other')
    by_category.setdefault(cat, []).append(tool)

# Find tools for specific task
task_tools = [t for t in all_tools if 'weather' in t['name']]
```

### Execution
```python
# Execute tool with retry
max_retries = 3
for attempt in range(max_retries):
    try:
        result = call_tool("weather", {"location": "NYC"})
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        wait_time = 2 ** attempt
        await asyncio.sleep(wait_time)
```

## Error Handling

### Tool Not Found
```python
try:
    tool = describe_tool("nonexistent_tool")
except ToolNotFound:
    # Suggest alternatives
    similar = search_tools("nonexistent")
    print(f"Did you mean: {similar}?")
```

### Server Unavailable
```python
try:
    result = call_tool_on_server("unavailable_server", "tool")
except ServerUnavailable:
    # Failover or queue
    queue_request(request)
```

## Testing & Validation

### Tool Validation
```python
# Test all tools are available
all_tools = list_all_tools()
for tool in all_tools:
    try:
        schema = describe_tool(tool['name'])
        assert 'parameters' in schema
    except:
        report_tool_error(tool)
```

### Load Testing
```python
# Test with high load
for i in range(1000):
    call_tool("get_weather", {"location": f"city_{i}"})
```

## Best Practices
1. Use tool discovery before execution
2. Cache frequently used tools
3. Handle server unavailability
4. Monitor health metrics
5. Batch similar operations
6. Implement retry logic
7. Log all tool calls
8. Document tool usage

## Dependencies
- fastmcp
- mcp
- httpx
- pydantic

## Configuration
```python
SERVER_CONFIG = {
    "discovery": {
        "auto_discover": True,
        "discovery_interval": 300
    },
    "caching": {
        "enabled": True,
        "ttl": 3600,
        "max_size": 1000
    },
    "health_check": {
        "interval": 60,
        "timeout": 10
    }
}
```

## Future Enhancements
- [ ] GraphQL query interface
- [ ] Advanced caching strategies
- [ ] Load balancing
- [ ] Circuit breaker pattern
- [ ] Distributed tool execution
- [ ] Analytics dashboard
- [ ] Tool versioning
