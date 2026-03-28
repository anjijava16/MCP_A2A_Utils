# Simple MCP Server 🚀

## Overview
A minimal MCP server implementation demonstrating core MCP concepts and protocol patterns. This server is ideal for learning, testing, and prototyping MCP functionality.

## Features
- **Minimal Setup**: Quick to understand and modify
- **Core Protocol**: Demonstrates MCP fundamentals
- **Easy Extension**: Simple to add new tools
- **Good Documentation**: Well-commented code
- **Perfect for Learning**: Ideal starting point

## Basic Usage

### Installation
```bash
pip install fastmcp mcp
```

### Running
```bash
python simple_server.py
```

## Example Tools
Simple math operations, basic data retrieval, proof-of-concept implementations

## Structure
```
simple_mcp/
├── server.py          # Main server
├── tools.py           # Tool definitions
└── README.md         # This file
```

## Adding Tools

### Simple Tool
```python
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b
```

### Tool with Error Handling
```python
@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Testing
```bash
# Test with MCP client
python -m mcp.client simple_server.py
```

## Use Cases
- Learning MCP
- Prototyping ideas
- Testing frameworks
- Educational purposes
- Reference implementation

## Dependencies
- fastmcp
- mcp

## Future Enhancements
- Add async tools
- Implement resources
- Add error handling patterns
