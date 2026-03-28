# MCP Adapters & Clients 🔌

## Overview
A collection of adapter and client implementations for various frameworks and platforms. This folder contains bridge code between different systems and MCP (Model Context Protocol), enabling seamless integration of MCP tools across multiple programming environments and libraries.

## Features
- **Framework Adapters**: Connect MCP to popular frameworks
- **Multiple Clients**: Different client implementations
- **Type Safety**: Full type hints and validation
- **Error Handling**: Comprehensive error management
- **Async Support**: Full async/await support
- **Extensible Design**: Easy to add new adapters

## Components

### MCP OpenAI Adapter
**Purpose**: Use MCP tools with OpenAI API

**Features:**
- Call OpenAI models with MCP tools
- Tool calling with function format
- Response parsing and handling
- Token management

**Usage:**
```python
from mcp_adapters import MCPOpenAIAdapter

adapter = MCPOpenAIAdapter(
    openai_api_key="sk-...",
    mcp_server_url="http://localhost:8000/sse"
)

# Call model with tools
response = adapter.call_model(
    "What time is it?",
    tools=adapter.get_tools()
)
```

### Framework-Specific Clients

#### Flask MCP Client
```python
from flask import Flask
from mcp_clients import FlaskMCPClient

app = Flask(__name__)
mcp = FlaskMCPClient(app, "http://localhost:8000/sse")

@app.route("/tool/<tool_name>", methods=["POST"])
def call_tool(tool_name):
    result = mcp.call_tool(tool_name, request.json)
    return {"result": result}
```

#### Django MCP Client
```python
from mcp_clients import DjangoMCPClient

mcp = DjangoMCPClient("http://localhost:8000/sse")

class ToolView(View):
    def post(self, request, tool_name):
        result = mcp.call_tool(tool_name, request.data)
        return JsonResponse({"result": result})
```

#### FastAPI MCP Client
```python
from fastapi import FastAPI
from mcp_clients import FastAPIMCPClient

app = FastAPI()
mcp = FastAPIMCPClient(app, "http://localhost:8000/sse")

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, args: dict):
    result = await mcp.call_tool_async(tool_name, args)
    return {"result": result}
```

## Installation

### From Source
```bash
cd mcp_adapaters_clients
pip install -e .
```

### From Requirements
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables
```bash
export MCP_SERVER_URL="http://localhost:8000/sse"
export MCP_TIMEOUT=30
export MCP_RETRIES=3
export OPENAI_API_KEY="sk-..."
```

### Configuration File
```python
MCP_CONFIG = {
    "servers": {
        "default": {
            "url": "http://localhost:8000/sse",
            "timeout": 30
        },
        "remote": {
            "url": "http://remote.server:8000/sse"
        }
    },
    "cache": {
        "enabled": True,
        "ttl": 3600
    }
}
```

## Adapter Patterns

### Tool Wrapping
```python
class ToolAdapter:
    def __init__(self, mcp_tool):
        self.tool = mcp_tool
    
    def __call__(self, *args, **kwargs):
        # Preprocess
        processed_args = self.preprocess(args)
        # Call MCP tool
        result = self.tool(*processed_args, **kwargs)
        # Postprocess
        return self.postprocess(result)
```

### Error Handling Adapter
```python
class ErrorHandlingAdapter:
    def __init__(self, adapter):
        self.adapter = adapter
    
    async def call_tool(self, name, args):
        try:
            return await self.adapter.call_tool(name, args)
        except ToolError as e:
            return {"error": str(e)}
        except TimeoutError:
            return {"error": "Tool execution timeout"}
        except Exception as e:
            return {"error": "Unexpected error"}
```

### Caching Adapter
```python
class CachingAdapter:
    def __init__(self, adapter, cache_ttl=3600):
        self.adapter = adapter
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    async def call_tool(self, name, args):
        cache_key = f"{name}:{json.dumps(args)}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = await self.adapter.call_tool(name, args)
        self.cache[cache_key] = result
        return result
```

## Advanced Features

### Middleware Pattern
```python
class LoggingMiddleware:
    def __init__(self, next_adapter):
        self.next = next_adapter
    
    async def call_tool(self, name, args):
        print(f"Calling {name} with {args}")
        result = await self.next.call_tool(name, args)
        print(f"Result: {result}")
        return result
```

### Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class RetryAdapter:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def call_tool_with_retry(self, name, args):
        return await self.adapter.call_tool(name, args)
```

### Rate Limiting
```python
from ratelimit import limits, sleep_and_retry
import time

class RateLimitingAdapter:
    @sleep_and_retry
    @limits(calls=100, period=60)
    async def call_tool(self, name, args):
        return await self.adapter.call_tool(name, args)
```

## Testing

### Unit Tests
```python
import pytest

@pytest.mark.asyncio
async def test_adapter():
    adapter = MockAdapter()
    result = await adapter.call_tool("test_tool", {})
    assert result is not None
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_with_real_server():
    adapter = MCPAdapter("http://localhost:8000/sse")
    result = await adapter.call_tool("weather", {"city": "NYC"})
    assert "temperature" in result
```

### Mock Servers
```python
class MockMCPServer:
    def __init__(self):
        self.tools = {
            "test_tool": self.test_tool_impl
        }
    
    async def call_tool(self, name, args):
        if name in self.tools:
            return await self.tools[name](args)
        raise ToolNotFound(name)
```

## Integration Examples

### OpenAI + MCP Tools
```python
from openai import OpenAI
from mcp_adapters import MCPOpenAIAdapter

client = OpenAI()
mcp_adapter = MCPOpenAIAdapter(
    client=client,
    mcp_url="http://localhost:8000/sse"
)

# Use MCP tools with OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "query"}],
    tools=mcp_adapter.get_tools_for_openai()
)
```

### Anthropic + MCP Tools
```python
import anthropic
from mcp_adapters import MCPAnthropicAdapter

client = anthropic.Anthropic()
mcp = MCPAnthropicAdapter("http://localhost:8000/sse")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=mcp.get_tools_for_anthropic(),
    messages=[{"role": "user", "content": "query"}]
)
```

### Custom Framework
```python
from mcp_clients import BaseMCPClient

class CustomFrameworkClient(BaseMCPClient):
    def __init__(self, framework, mcp_url):
        super().__init__(mcp_url)
        self.framework = framework
    
    async def invoke_tool(self, tool_name, args):
        return await self.call_tool(tool_name, args)
```

## Performance Optimization

### Connection Pooling
```python
from mcp_adapters import PooledMCPAdapter

adapter = PooledMCPAdapter(
    server_url="http://localhost:8000/sse",
    pool_size=10
)
```

### Batch Operations
```python
# Execute multiple tools efficiently
results = await adapter.batch_call([
    ("tool1", args1),
    ("tool2", args2),
    ("tool3", args3)
])
```

### Result Caching
```python
adapter = CachingMCPAdapter(
    base_adapter=MCPAdapter(...),
    ttl=3600  # Cache for 1 hour
)
```

## Error Recovery

### Automatic Retry
```python
adapter = RetryingMCPAdapter(
    base_adapter=mcp,
    max_retries=3,
    backoff_factor=2
)
```

### Fallback Adapters
```python
primary = MCPAdapter("http://primary:8000/sse")
fallback = MCPAdapter("http://fallback:8000/sse")

adapter = FallbackMCPAdapter(
    primary=primary,
    fallback=fallback
)
```

### Circuit Breaker
```python
from mcp_adapters import CircuitBreakerAdapter

adapter = CircuitBreakerAdapter(
    base_adapter=mcp,
    failure_threshold=5,
    timeout=60
)
```

## Monitoring & Observability

### Metrics Collection
```python
adapter = MetricsAdapter(
    base_adapter=mcp,
    metrics_registry=prometheus_registry
)

# Collects:
# - Tool call count
# - Execution time
# - Error rate
# - Cache hit rate
```

### Logging
```python
import logging

logger = logging.getLogger("mcp_adapters")
handler = logging.FileHandler("mcp_adapter.log")
logger.addHandler(handler)

adapter = LoggingAdapter(mcp, logger)
```

## Files & Structure
- `__init__.py` - Package initialization
- `mcp_openai_client_exp_.py` - Experimental OpenAI integration
- Additional adapter implementations

## Dependencies
- mcp
- httpx
- pydantic
- (Framework-specific: openai, anthropic, fastapi, flask, django, etc.)

## Best Practices
1. Use appropriate adapter layers
2. Implement proper error handling
3. Cache tool definitions
4. Monitor performance
5. Log tool calls for debugging
6. Use connection pooling
7. Implement retry logic
8. Test with edge cases

## Troubleshooting

### Connection Issues
```python
# Check adapter configuration
try:
    adapter.test_connection()
except ConnectionError:
    print("Cannot connect to MCP server")
```

### Tool Loading
```python
# Debug tool loading
tools = adapter.get_tools(debug=True)
```

### Error Handling
```python
# Catch specific errors
try:
    result = await adapter.call_tool(name, args)
except ToolNotFound:
    print(f"Tool {name} not found")
except ToolExecutionError as e:
    print(f"Tool execution failed: {e}")
```

## Future Enhancements
- [ ] More framework adapters
- [ ] Advanced caching strategies
- [ ] Performance profiling tools
- [ ] Distributed tool execution
- [ ] Advanced monitoring
- [ ] Auto-scaling support
