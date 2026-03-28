# OpenAI MCP Client 🤖

## Overview
Complete MCP client implementation for integrating with OpenAI models, enabling OpenAI API calls to use MCP tools for function calling and extended capabilities.

## Features
- **Function Calling**: OpenAI compatible tool format
- **Token Management**: Efficient token usage
- **Streaming Support**: Stream model responses
- **Error Handling**: Graceful error recovery
- **Async Support**: Full async/await support
- **Type Safety**: Pydantic-based validation

## Setup & Usage

### Installation
```bash
pip install openai fastmcp mcp
```

### Configuration
```bash
export OPENAI_API_KEY="sk-..."
export MCP_SERVER_URL="http://localhost:8000/sse"
```

### Basic Usage
```python
from openai import AsyncOpenAI
from mcp_openai_adapter import MCPOpenAIAdapter

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
adapter = MCPOpenAIAdapter(
    client=client,
    mcp_server_url="http://localhost:8000/sse"
)

# Use MCP tools with OpenAI
response = await adapter.chat_with_tools(
    model="gpt-4",
    messages=[{"role": "user", "content": "query"}],
    tools=adapter.get_tools()
)
```

## Tool Format Conversion

### MCP Tool → OpenAI Function
```python
# MCP Tool Definition
{
    "name": "get_weather",
    "description": "Get weather for location",
    "inputSchema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        }
    }
}

# Converts to OpenAI Function
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }
}
```

## Usage Examples

### Simple Tool Call
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What's the weather?"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "parameters": {...}
            }
        }
    ]
)
```

### Streaming
```python
response = await client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=tools,
    stream=True
)

async for chunk in response:
    process_chunk(chunk)
```

### Multi-turn Conversation
```python
messages = [
    {"role": "user", "content": "Check weather in NYC"}
]

response = await adapter.chat_with_tools(
    model="gpt-4",
    messages=messages,
    tools=adapter.get_tools()
)

# Handle tool calls
if response.tool_calls:
    for tool_call in response.tool_calls:
        result = await adapter.execute_tool(
            tool_call.function.name,
            json.loads(tool_call.function.arguments)
        )
        messages.append({"role": "assistant", "content": response})
        messages.append({
            "role": "tool",
            "content": str(result),
            "tool_call_id": tool_call.id
        })
    
    # Second turn with results
    response = await adapter.chat_with_tools(
        model="gpt-4",
        messages=messages,
        tools=adapter.get_tools()
    )
```

## Advanced Features

### Token Management
```python
# Track token usage
response = await adapter.chat_with_tools(...)

print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
```

### Model Selection
```python
# Use different models
for model in ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]:
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
```

### Tool Filtering
```python
# Use only specific tools
filtered_tools = [
    t for t in all_tools 
    if t.function.name in ["search", "weather"]
]

response = await client.chat.completions.create(
    model="gpt-4",
    tools=filtered_tools
)
```

## Error Handling

### API Errors
```python
try:
    response = await client.chat.completions.create(...)
except openai.AuthenticationError:
    print("Invalid API key")
except openai.RateLimitError:
    print("Rate limited")
except openai.APIError as e:
    print(f"API error: {e}")
```

### Tool Execution Errors
```python
try:
    result = await adapter.execute_tool(tool_name, args)
except ToolNotFound:
    print(f"Tool {tool_name} not found")
except ToolExecutionError as e:
    print(f"Tool error: {e}")
```

## Performance Optimization

### Batching
```python
# Batch multiple requests
results = await asyncio.gather(
    client.chat.completions.create(...),
    client.chat.completions.create(...),
    client.chat.completions.create(...)
)
```

### Caching
```python
# Cache tool definitions
tools_cache = {}

def get_tools(cache=True):
    if cache and "tools" in tools_cache:
        return tools_cache["tools"]
    
    tools = adapter.get_tools()
    tools_cache["tools"] = tools
    return tools
```

### Rate Limiting
```python
# Respect rate limits
limiter = AsyncLimiter(max_rate=3, time_period=60)

async with limiter:
    response = await client.chat.completions.create(...)
```

## Testing

### Unit Tests
```python
@pytest.mark.asyncio
async def test_tool_conversion():
    adapter = MCPOpenAIAdapter(...)
    tools = adapter.get_tools()
    
    for tool in tools:
        assert "function" in tool
        assert "name" in tool["function"]
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_with_real_openai():
    response = await adapter.chat_with_tools(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}],
        tools=adapter.get_tools()
    )
    
    assert response.content is not None
```

## Best Practices
1. Validate tool definitions
2. Handle rate limiting
3. Use streaming for long responses
4. Manage tokens efficiently
5. Cache tool definitions
6. Implement proper error handling
7. Test with different models
8. Monitor API usage

## Dependencies
- openai
- fastmcp
- mcp
- pydantic

## Configuration
```python
OPENAI_CONFIG = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
    "timeout": 30
}
```

## Troubleshooting

### Tools Not Working
- Verify tool definitions
- Check parameter types
- Test tools independently
- Review error messages

### Performance Issues
- Use streaming for long responses
- Batch requests when possible
- Cache tool definitions
- Monitor token usage

## Future Enhancements
- [ ] Vision tool support
- [ ] File upload handling
- [ ] Advanced caching
- [ ] Cost tracking
- [ ] Model comparison tools
