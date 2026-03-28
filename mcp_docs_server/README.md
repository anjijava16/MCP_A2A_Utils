# MCP Protocol Documentation Server 🔗

## Overview

Custom Python FastMCP server providing comprehensive documentation for the **Model Context Protocol (MCP)**. Access protocol specifications, implementation patterns, best practices, and API references through a standardized interface.

## Architecture & Features

- **Protocol Documentation**: Complete MCP specification and guides
- **Implementation Examples**: Python code patterns and examples
- **API Reference**: All MCP classes, decorators, and functions
- **Best Practices**: Proven patterns and guidelines
- **9+ Tools**: Search, extract, retrieve documentation
- **SSE Transport**: Server-Sent Events on port 7100
- **Local Fallback**: Built-in documentation if remote fetch fails

## Tool Categories

**Core Documentation** (4)
- `search_mcp_docs` - Full-text search across all docs
- `get_mcp_overview` - Quick start guide
- `list_mcp_sections` - Browse available sections
- `get_mcp_section` - Retrieve specific section

**API Reference** (2)
- `list_mcp_apis` - List all MCP APIs and classes
- `search_mcp_api` - Look up specific API

**Learning Resources** (3)
- `extract_code_examples_mcp` - Get Python code examples
- `get_best_practices` - Best practices guide
- `get_mcp_examples` - Implementation examples

**Utilities** (1)
- `reload_mcp_docs` - Refresh documentation

## Environment Setup

```bash
# No required environment variables
# Optional: customize doc source if needed
```

## Installation

```bash
pip install fastmcp httpx
```

## Running the Server

```bash
python mcp_docs_server/server.py
```

Server will start on `http://0.0.0.0:7100` with SSE transport.

## Usage Examples

### Search Documentation
```python
# Find information about tools
results = await search_mcp_docs("tools", max_results=5)

# Find details about resources
results = await search_mcp_docs("resource", max_results=3)
```

### Browse Topics
```python
# See all available sections
sections = await list_mcp_sections()

# Get specific section
content = await get_mcp_section("Architecture")

# Or use fuzzy matching
content = await get_mcp_section("tools")  # Works with "Tool Definition Pattern"
```

### API Reference
```python
# List all MCP APIs
apis = await list_mcp_apis()

# Look up specific API
ref = await search_mcp_api("FastMCP")
```

### Code Examples
```python
# Get Python code examples
examples = await extract_code_examples_mcp()

# Get implementation patterns
patterns = await get_best_practices()

# Get tutorials
tutorials = await get_mcp_examples()
```

## Key Sections

### Core Concepts
- Protocol Architecture
- Message Types
- Key Components (Tools, Resources, Prompts)

### Implementation Guide
- FastMCP Server Setup
- Tool Definition Pattern
- Resource Pattern
- Parameter Validation

### Transport Protocols
- stdio (IPC)
- SSE (HTTP)
- WebSocket

### Integration Patterns
- Claude Desktop Integration
- Programmatic Clients
- Server Composition

### Best Practices
- Tool Design
- Resource Management
- Security Guidelines
- Error Handling

### Advanced Topics
- Streaming Results
- Webhooks & Events
- Authentication
- Rate Limiting

## Performance

| Operation | Speed | Coverage |
|-----------|-------|----------|
| Search | <100ms | Full text |
| Section Retrieval | <50ms | Single section |
| API List | <20ms | All APIs |
| Code Extraction | <200ms | All examples |

## Features

- **Full-Text Search**: Search entire protocol docs
- **Section Navigation**: Quick access to topics
- **Code Examples**: Extract Python implementation patterns
- **API Discovery**: List and lookup all APIs
- **Fuzzy Matching**: Find sections with partial names
- **Local Fallback**: Works even if remote docs unavailable

## Common Workflows

### Learning MCP from Scratch
```python
# 1. Get overview
overview = await get_mcp_overview()

# 2. Browse topics
sections = await list_mcp_sections()

# 3. Read specific section
core = await get_mcp_section("Core Concepts")

# 4. See examples
examples = await extract_code_examples_mcp()
```

### Building an MCP Server
```python
# 1. Find implementation guide
guide = await get_mcp_section("Implementation Guide")

# 2. Get code examples
examples = await extract_code_examples_mcp()

# 3. Find best practices
practices = await get_best_practices()

# 4. Look up specific APIs
api_ref = await search_mcp_api("FastMCP")
```

### Protocol Deep Dive
```python
# 1. Search for specific concepts
results = await search_mcp_docs("bidirectional", max_results=10)

# 2. Get detailed sections
transport = await get_mcp_section("Transport Protocols")

# 3. Find advanced patterns
advanced = await search_mcp_docs("streaming", max_results=5)
```

## Integration with Claude Desktop

```json
{
  "mcpServers": {
    "mcp-protocol": {
      "command": "python",
      "args": ["mcp_docs_server/server.py"],
      "env": {}
    }
  }
}
```

## Documentation Structure

```
Model Context Protocol Documentation
├── Overview
├── Core Concepts
│   ├── Protocol Architecture
│   ├── Message Types
│   └── Key Components
├── Implementation Guide
│   ├── Creating Servers
│   ├── Tool Definition
│   ├── Resource Pattern
│   └── Transport Setup
├── Integration Patterns
├── Best Practices
├── Examples & Tutorials
└── Advanced Topics
```

## Response Examples

### Search Results
```json
{
    "success": true,
    "query": "tools",
    "matches": [
        {
            "line": 42,
            "match": "Tools are callable functions that an MCP server can expose",
            "context": "surrounding context..."
        }
    ],
    "count": 3
}
```

### Section Content
```json
{
    "success": true,
    "section": "Tool Definition Pattern",
    "content": "full section content..."
}
```

### API List
```json
{
    "success": true,
    "apis": ["FastMCP", "tool", "resource", "prompt", ...],
    "count": 25
}
```

### Code Examples
```json
{
    "success": true,
    "code_blocks": [
        "from fastmcp import FastMCP\nmcp = FastMCP('MyServer')",
        "@mcp.tool()\nasync def my_tool(param: str)..."
    ],
    "total_code_blocks": 18,
    "message": "Showing first 5 code blocks"
}
```

## Role-Based Prompts

### MCP Protocol Expert
Deep understanding of MCP specification. Help with protocol design, advanced integration patterns, and solving complex architectural challenges.

### MCP Server Developer
Building practical MCP servers. Help with implementation, debugging server code, optimizing performance, and following best practices.

### MCP Integration Architect
Designing systems using MCP. Help with server composition, architecture planning, security implementation, and scaling strategies.

## Troubleshooting

### Docs won't load
```python
# Reload from source
await reload_mcp_docs()

# Falls back to built-in docs if needed
```

### Search returns nothing
```python
# Try different keywords
await search_mcp_docs("architecture", max_results=10)

# Browse sections directly
sections = await list_mcp_sections()
```

### Need specific implementation
```python
# Get code examples
examples = await extract_code_examples_mcp()

# Get best practices
practices = await get_best_practices()
```

## Advanced Features

### Smart Caching
- Lazy load on first request
- Parse into sections for fast lookup
- Persists during server lifetime
- Reload on demand

### Code Block Detection
- Automatically finds Python code blocks
- Preserves language hints
- Maintains formatting

### Fuzzy Section Matching
```python
# All work:
await get_mcp_section("Implementation Guide")
await get_mcp_section("implementation")
await get_mcp_section("guide")
```

## Resource Usage

- **Memory**: ~1MB (documentation cache)
- **Network**: One-time fetch on startup (varies)
- **CPU**: Minimal (text operations)
- **Storage**: None (in-memory)

## Comparison with Official MCP Documentation

| Aspect | This Server | Official Docs |
|--------|:-----------:|:-------------:|
| Search | Fast (in-memory) | Google search |
| Access | Programmatic | Browser only |
| Integration | MCP tools | Manual lookup |
| Offline | Partial | No |
| Real-time | Yes | Always current |
| Custom Tools | Easy | N/A |

## Support & Resources

- [MCP Official Website](https://modelcontextprotocol.io)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [FastMCP Library](https://github.com/jlouis/fastmcp)

---

**Port**: 7100 | **Type**: Documentation Server | **Tools**: 9+ | **Content**: MCP Protocol Spec
