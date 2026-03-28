# MCP Math Server 🧮

## Overview
A lightweight FastMCP-based server providing basic mathematical operations. This server exposes common arithmetic operations as MCP tools for integration with AI agents and models.

## Features
- **Basic Arithmetic**: Addition, subtraction, multiplication, division
- **Simple Operations**: Quick mathematical computations
- **Agent Integration**: Tools designed for AI agent usage
- **Type Safety**: Pydantic-validated inputs and outputs

## Tools Available
- `add(a, b)` - Add two numbers
- `multiply(a, b)` - Multiply two numbers
- Additional math operations can be easily extended

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp
```

### Running the Server
```bash
# Stdio transport (for Claude Desktop)
python math.py --transport stdio

# SSE transport (for HTTP clients)
# Can be configured to run on specific port
```

### Example Usage
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b
```

## Architecture
- **Transport**: Supports both Stdio and SSE
- **Framework**: Uses FastMCP for minimal boilerplate
- **Type Safety**: All tools are type-hinted with Pydantic

## Files
- `math.py` - Main math server implementation

## Use Cases
- Agent decision-making requiring calculations
- AI model integration for mathematical operations
- Tool suite expansion for computational tasks

## Performance
- Minimal latency
- No external API calls
- Pure computation-based operations

## Extensibility
The architecture allows easy addition of more operations:
- Trigonometric functions
- Power operations
- Statistical calculations
- Complex number operations

## Dependencies
- fastmcp
- mcp
