# Simple MCP Reference Implementation 📚

## Overview
A minimalist reference implementation of an MCP server demonstrating core concepts. This serves as a learning resource for understanding MCP fundamentals and basic server architecture.

## Features
- **Simple Architecture**: Easy to understand code structure
- **Demo Server**: Complete working example
- **Demo Client**: Example client implementation
- **Minimal Dependencies**: Only essential libraries
- **Clear Documentation**: Well-commented code
- **Learning Resource**: Perfect for beginners

## Setup & Usage

### Installation
```bash
cd simple
python -m venv venv
source venv/bin/activate
pip install fastmcp mcp
```

### Running Demo Server
```bash
python demo_server.py
```

Server output:
```
Starting MCP Server on stdio
Ready to accept connections
```

### Running Demo Client
```bash
python demo_client.py
```

Client output:
```
Connecting to MCP server...
Connected!
Available tools:
  - echo
  - add
  - multiply
Executing tools...
```

## Project Structure

```
simple/
├── demo_server.py    # MCP server implementation
├── demo_client.py    # MCP client implementation
└── __pycache__/
```

## Demo Server Implementation

### Basic Structure
```python
# demo_server.py
import asyncio
from mcp import Tool, Server

# Initialize server
server = Server("simple_demo")

# Define tools
tools = {
    "echo": {
        "description": "Echo the input back",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"]
        }
    }
}

# Register tools
for name, schema in tools.items():
    server.register_tool(name, schema)

# Handle tool calls
@server.call_tool
async def handle_tool_call(name, args):
    if name == "echo":
        return {"result": args["text"]}
    elif name == "add":
        return {"result": args["a"] + args["b"]}
    elif name == "multiply":
        return {"result": args["a"] * args["b"]}

# Main
if __name__ == "__main__":
    asyncio.run(server.run())
```

## Demo Client Implementation

### Basic Structure
```python
# demo_client.py
import asyncio
from mcp import Client

async def main():
    # Create client
    client = Client()
    
    # Connect to server
    await client.connect()
    
    # Get available tools
    tools = await client.list_tools()
    print(f"Available tools: {[t['name'] for t in tools]}")
    
    # Call tool
    result = await client.call_tool("echo", {"text": "hello"})
    print(f"Result: {result}")
    
    # Close connection
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Tools Provided

### Echo Tool
```python
{
    "name": "echo",
    "description": "Echo the input text back",
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"}
        },
        "required": ["text"]
    }
}
```

Example:
```python
result = await client.call_tool("echo", {"text": "Hello World"})
# Returns: {"result": "Hello World"}
```

### Add Tool
```python
{
    "name": "add",
    "description": "Add two numbers",
    "inputSchema": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
}
```

Example:
```python
result = await client.call_tool("add", {"a": 5, "b": 3})
# Returns: {"result": 8}
```

### Multiply Tool
```python
{
    "name": "multiply",
    "description": "Multiply two numbers",
    "inputSchema": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
}
```

Example:
```python
result = await client.call_tool("multiply", {"a": 4, "b": 7})
# Returns: {"result": 28}
```

## Learning Objectives

After studying this implementation, you'll understand:

1. **Basic MCP Structure**
   - Server initialization
   - Tool registration
   - Tool handling

2. **Client Interaction**
   - Connection establishment
   - Tool discovery
   - Tool invocation

3. **Async Programming**
   - Using asyncio
   - Async/await patterns
   - Event handling

4. **Error Handling**
   - Input validation
   - Exception handling
   - Error responses

5. **Message Format**
   - Tool definitions
   - Request/response format
   - Parameter validation

## Running Examples

### Example 1: Basic Echo
```python
# Server receives request
request = {
    "method": "call_tool",
    "params": {
        "name": "echo",
        "arguments": {"text": "Hello"}
    }
}

# Server processes and responds
response = {
    "result": {"result": "Hello"}
}
```

### Example 2: Arithmetic Operations
```python
# Perform addition
result1 = await client.call_tool("add", {"a": 10, "b": 20})
# Returns: {"result": 30}

# Perform multiplication
result2 = await client.call_tool("multiply", {"a": 5, "b": 6})
# Returns: {"result": 30}

# Combined operation
sum_result = await client.call_tool("add", {"a": 10, "b": 20})
product = await client.call_tool("multiply", 
    {"a": sum_result["result"], "b": 2})
# Returns: {"result": 60}
```

## Extending the Implementation

### Adding a New Tool

1. **Define the tool schema**:
```python
tools["divide"] = {
    "description": "Divide two numbers",
    "inputSchema": {
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
}
```

2. **Add handler**:
```python
@server.call_tool
async def handle_tool_call(name, args):
    # ... existing handlers ...
    elif name == "divide":
        if args["b"] == 0:
            return {"error": "Division by zero"}
        return {"result": args["a"] / args["b"]}
```

3. **Test the tool**:
```python
result = await client.call_tool("divide", {"a": 20, "b": 4})
# Returns: {"result": 5.0}
```

## Best Practices Demonstrated

1. **Clear Tool Definitions**
   - Descriptive names
   - Complete schemas
   - Required fields specified

2. **Async Programming**
   - Proper async/await usage
   - Non-blocking operations
   - Proper cleanup

3. **Error Handling**
   - Input validation
   - Graceful error messages
   - Exception handling

4. **Code Organization**
   - Clear structure
   - Separated concerns
   - Reusable components

## Testing

### Manual Testing
```bash
# Terminal 1: Start server
python demo_server.py

# Terminal 2: Run client
python demo_client.py
```

### Automated Testing
```python
import pytest

@pytest.mark.asyncio
async def test_echo_tool():
    client = Client()
    result = await client.call_tool("echo", {"text": "test"})
    assert result["result"] == "test"

@pytest.mark.asyncio
async def test_add_tool():
    client = Client()
    result = await client.call_tool("add", {"a": 2, "b": 3})
    assert result["result"] == 5
```

## Common Modifications

### Change Transport
```python
# Use SSE instead of stdio
server = Server("simple_demo", transport="sse", port=8000)
```

### Add Authentication
```python
# Add API key validation
@server.before_call_tool
async def validate_api_key(request):
    api_key = request.headers.get("Authorization")
    if api_key != "valid_key":
        raise AuthenticationError("Invalid API key")
```

### Add Logging
```python
import logging

logger = logging.getLogger(__name__)

@server.call_tool
async def handle_tool_call(name, args):
    logger.info(f"Calling tool: {name} with args: {args}")
    # ... tool logic ...
```

## Dependencies
- fastmcp
- mcp

## Use Cases for This Implementation
- Learning MCP basics
- Prototyping new tools
- Testing client implementations
- Understanding server lifecycle
- Debugging MCP issues

## Next Steps
After mastering this simple implementation:
1. Study more complex servers (weather, database, etc.)
2. Add more sophisticated tools
3. Implement different transports
4. Add authentication
5. Deploy to production

## Future Enhancements
- [ ] WebSocket transport example
- [ ] Error handling examples
- [ ] Streaming responses
- [ ] Tool chaining examples
