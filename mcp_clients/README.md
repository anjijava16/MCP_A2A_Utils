# MCP Clients 🔌

## Overview
A collection of MCP client implementations and utilities for connecting to MCP servers. This folder contains client code for testing, integration, and consuming MCP tools from various applications and frameworks.

## Features
- **Multiple Client Types**: Different client implementations for various use cases
- **Protocol Support**: Supports both Stdio and SSE transports
- **Tool Integration**: Easily invoke MCP tools from applications
- **Error Handling**: Robust error handling and recovery
- **Async Support**: Full async/await support for non-blocking operations
- **Server-agnostic**: Works with any MCP-compliant server

## Files
- `mcp_chatbot.py` - Chatbot client implementation using MCP tools

## Client Types

### MCP Chatbot Client
A conversational chatbot client that uses MCP tools to enhance responses.

**Features:**
- Multi-turn conversation support
- Tool invocation within conversations
- Context awareness
- Response generation based on tool results
- Integration with LLM models

**Usage:**
```bash
python mcp_chatbot.py
```

## Setup & Usage

### Installation
```bash
pip install mcp httpx aiohttp
```

### Basic Client Connection
```python
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioClientTransport

# Stdio transport
transport = StdioClientTransport(
    command="python",
    args=["path/to/server.py"]
)

async with ClientSession(transport) as session:
    # Use the session to call tools
    pass
```

### SSE Transport Client
```python
from mcp.client.sse import SSEClientTransport

# SSE transport
transport = SSEClientTransport(url="http://localhost:8000/sse")

async with ClientSession(transport) as session:
    # Connect to SSE-based server
    pass
```

## Common Operations

### List Available Tools
```python
async with ClientSession(transport) as session:
    response = await session.list_tools()
    print(response.tools)  # List of available tools
```

### Invoke a Tool
```python
async with ClientSession(transport) as session:
    result = await session.call_tool(
        name="tool_name",
        arguments={"param": "value"}
    )
    print(result)
```

### List Resources
```python
async with ClientSession(transport) as session:
    response = await session.list_resources()
    print(response.resources)  # Available resources
```

### Read a Resource
```python
async with ClientSession(transport) as session:
    contents = await session.read_resource("resource://path")
```

## Chatbot Implementation

The chatbot client demonstrates:
- Server connection management
- Tool discovery and listing
- Tool invocation in conversations
- Response formatting
- Error handling

**Example Flow:**
```
User: "What's the weather in NYC?"
    ↓
Client lists available tools
    ↓
Client finds "get_weather" tool
    ↓
Client calls tool with parameters
    ↓
Tool returns: "Sunny, 72°F"
    ↓
Client formats response to user
```

## Use Cases
- **Tool Testing**: Test MCP servers before deployment
- **Agent Integration**: Integrate with AI agents and chatbots
- **API Wrappers**: Create API wrappers around MCP tools
- **Debugging**: Debug MCP server functionality
- **Monitoring**: Monitor MCP tool availability
- **Data Piping**: Chain multiple tools together

## Advanced Patterns

### Error Handling
```python
from mcp.types import ToolError

try:
    result = await session.call_tool(name, arguments)
except ToolError as e:
    print(f"Tool error: {e}")
except Exception as e:
    print(f"Client error: {e}")
```

### Retry Logic
```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def call_tool_with_retry(session, name, args):
    return await session.call_tool(name, args)
```

### Tool Chaining
```python
# Call one tool with output from another
result1 = await session.call_tool("tool1", {"input": "data"})
result2 = await session.call_tool("tool2", {"input": result1})
```

### Concurrent Tool Calls
```python
import asyncio

# Call multiple tools in parallel
results = await asyncio.gather(
    session.call_tool("tool1", {}),
    session.call_tool("tool2", {}),
    session.call_tool("tool3", {})
)
```

## Connection Management

### Connection Pooling
```python
class ClientPool:
    def __init__(self, transport):
        self.transport = transport
        self.sessions = []
    
    async def get_session(self):
        # Reuse or create new session
        pass
```

### Timeout Configuration
```python
transport = SSEClientTransport(
    url="http://localhost:8000/sse",
    timeout=30
)
```

### Reconnection Logic
```python
async def call_with_reconnect(session, name, args):
    try:
        return await session.call_tool(name, args)
    except ConnectionError:
        await session.reconnect()
        return await session.call_tool(name, args)
```

## Integration Examples

### With FastAPI
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/tool-call")
async def call_tool(tool_name: str, arguments: dict):
    async with ClientSession(transport) as session:
        return await session.call_tool(tool_name, arguments)
```

### With LangChain
```python
from langchain_mcp_adapters.client import MCPClient

client = MCPClient({"weather": {...}})
tools = client.get_tools()
```

### With Discord Bots
```python
class ToolBot(commands.Cog):
    async def get_tool_result(self, tool_name, args):
        async with ClientSession(transport) as session:
            return await session.call_tool(tool_name, args)
```

## Monitoring & Observability

### Logging
```python
import logging

logger = logging.getLogger("mcp_client")
handler = logging.StreamHandler()
logger.addHandler(handler)
```

### Metrics
```python
# Track:
# - Tool call count
# - Execution time
# - Error rate
# - Success rate
```

## Best Practices
1. Always handle ToolError exceptions
2. Implement timeout management
3. Use connection pooling for efficiency
4. Log all tool invocations
5. Validate tool arguments before calling
6. Implement retry logic for reliability
7. Cache tool metadata
8. Monitor performance metrics

## Testing Clients

### Unit Tests
```python
@pytest.mark.asyncio
async def test_tool_call():
    async with ClientSession(mock_transport) as session:
        result = await session.call_tool("test_tool", {})
        assert result is not None
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_against_real_server():
    transport = SSEClientTransport(url="http://localhost:8000/sse")
    async with ClientSession(transport) as session:
        tools = await session.list_tools()
        assert len(tools.tools) > 0
```

## Troubleshooting
- Verify server is running
- Check transport configuration
- Validate tool names and arguments
- Review error messages
- Check logs for details
- Test with MCP Inspector

## Dependencies
- mcp (MCP protocol)
- httpx (HTTP client)
- aiohttp (Alternative HTTP client)

## Future Enhancements
- Built-in retry mechanisms
- Advanced error recovery
- Performance optimization
- Caching layer
- Tool result validation
- Execution history tracking
- Advanced analytics
