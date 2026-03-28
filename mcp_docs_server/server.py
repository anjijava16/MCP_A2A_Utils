"""
Model Context Protocol (MCP) Documentation Server 🔗
Python FastMCP server for comprehensive MCP protocol documentation
"""

import asyncio
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
import httpx
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("MCP-Docs 🔗")

# Cache for documentation
_doc_cache = {
    "content": None,
    "last_updated": None,
    "sections": {},
    "apis": []
}

async def fetch_mcp_docs() -> str:
    """Fetch MCP documentation from official source"""
    try:
        # Using model context protocol official documentation
        url = "https://modelcontextprotocol.io/docs"
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            logger.info("✅ MCP documentation fetched successfully")
            return response.text
    except Exception as e:
        # Fallback to creating basic MCP docs structure
        logger.warning(f"⚠️ Could not fetch remote docs: {str(e)}, using local structure")
        return _get_local_mcp_docs()

def _get_local_mcp_docs() -> str:
    """Return built-in MCP documentation structure"""
    return """
# Model Context Protocol (MCP) Documentation

## Overview
The Model Context Protocol (MCP) is an open protocol that allows Large Language Models (LLMs) 
and applications to interact with tools and resources through a standardized interface.

## Core Concepts

### Protocol Architecture
- Request-Response Model: Client sends requests, server responds with results
- JSON-RPC 2.0: Message format standard
- Bidirectional Communication: Both client-server can initiate requests

### Message Types
- Tool Call: Client invokes tool on server
- Resource Read: Client reads resource from server
- Capability Negotiation: Exchange of supported features

## Key Components

### Tools
Tools are callable functions that an MCP server can expose. They accept parameters and return results.

```python
@mcp.tool()
async def my_tool(param1: str, param2: int) -> dict:
    '''Tool description'''
    return {"result": "value"}
```

### Resources
Resources are named data sources that clients can read from servers.

```python
@mcp.resource()
async def my_resource() -> str:
    return "resource content"
```

### Prompts
Prompts are reusable prompt templates with arguments.

```python
@mcp.prompt()
async def my_prompt(name: str) -> str:
    return f"Hello, {name}!"
```

## Transport Protocols

### stdio
Standard input/output for local IPC

### SSE (Server-Sent Events)
HTTP-based transport for remote connections

### WebSocket
Bidirectional persistent connections

## Implementation Patterns

### Creating an MCP Server
```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool()
async def my_tool(param: str) -> dict:
    return {"status": "success", "param": param}

async def main():
    await mcp.run_async(transport="sse", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    asyncio.run(main())
```

### Tool Definition Pattern
- Name: Unique identifier for the tool
- Description: What the tool does
- Parameters: Input schema (JSON Schema)
- Returns: Output format specification

### Resource Pattern
- URI: Unique resource identifier
- MIME Type: Content type (text/plain, application/json, etc.)
- Content: Actual resource data

## Best Practices

### Tool Design
1. Single Responsibility: Each tool does one thing well
2. Clear Documentation: Descriptive names and docstrings
3. Error Handling: Graceful error responses
4. Input Validation: Validate parameters before processing

### Resource Management
1. Efficient Loading: Don't load everything upfront
2. Caching: Cache frequently accessed resources
3. Versioning: Track resource versions
4. Cleanup: Proper resource cleanup

### Security
1. Input Validation: Always validate input
2. Rate Limiting: Prevent abuse
3. Access Control: Implement authentication where needed
4. Logging: Track all operations

## Integration Patterns

### With Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
    "mcpServers": {
        "my-server": {
            "command": "python",
            "args": ["server.py"],
            "env": {}
        }
    }
}
```

### Programmatic Clients
Connect to MCP servers from your own applications using standard MCP clients.

### Composing Multiple Servers
Run multiple MCP servers and compose their capabilities through a single interface.

## Error Handling

Standard error response format:
```json
{
    "jsonrpc": "2.0",
    "error": {
        "code": -32000,
        "message": "Error description"
    },
    "id": "request_id"
}
```

## Versioning & Compatibility

- Semantic Versioning: MAJOR.MINOR.PATCH
- Backward Compatibility: Maintain compatibility when possible
- Feature Negotiation: Servers advertise capabilities upfront

## Advanced Topics

### Streaming Results
Return large results incrementally using streaming

### Webhooks & Events
Servers can emit events that clients can subscribe to

### Authentication
Implement authentication tokens for secure server access

### Rate Limiting
Control request rates to prevent abuse

## Troubleshooting

### Connection Issues
- Check transport configuration
- Verify port availability
- Check firewall settings

### Tool Not Found
- Ensure tool is registered with @mcp.tool()
- Check tool name matches exactly
- Verify tool is in correct scope

### Parameter Validation
- Check parameter types
- Ensure required parameters provided
- Validate against JSON Schema

## Examples & Tutorials

### Basic Server
Create a simple server with one tool

### Database Server
Expose database operations through MCP

### API Gateway
Wrap REST APIs as MCP tools

### Search Server
Implement full-text search over resources

## Performance Optimization

### Caching Strategies
- In-memory caching for frequently accessed data
- TTL-based cache invalidation
- Cache warming on startup

### Resource Pooling
- Connection pooling for database operations
- Thread/async task pooling for heavy operations
- Resource reuse across requests

### Scaling
- Horizontal scaling with multiple server instances
- Load balancing across instances
- Distributed caching with Redis/Memcached

## Security Guidelines

### Input Sanitization
Always validate and sanitize user input

### Output Escaping
Properly escape output for the target context

### Access Control
Implement role-based access control (RBAC)

### Audit Logging
Log all operations for compliance and debugging

## Appendix

### Standard Tool Categories
- Database Operations (CRUD)
- File System Operations (read, write, list)
- Network Operations (HTTP, etc.)
- Computation (calculate, analyze)
- Transformation (convert, format)

### Response Status Codes
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Server Error

### Common MIME Types
- text/plain
- application/json
- text/html
- application/xml
"""

async def ensure_docs_loaded():
    """Load docs into cache if not already present"""
    if _doc_cache["content"] is None:
        try:
            _doc_cache["content"] = await fetch_mcp_docs()
            _doc_cache["last_updated"] = datetime.now().isoformat()
            _parse_sections()
            logger.info("✅ MCP Documentation loaded and parsed")
        except Exception as e:
            logger.error(f"❌ Failed to load documentation: {str(e)}")
            raise

def _parse_sections():
    """Parse documentation into sections for indexing"""
    content = _doc_cache["content"]
    
    # Split by major sections
    sections = re.split(r'^(#{1,3}\s+.*?)$', content, flags=re.MULTILINE)
    
    current_section = "Overview"
    for i, section in enumerate(sections):
        if section.startswith('#'):
            current_section = section.strip('#').strip()
        else:
            if current_section not in _doc_cache["sections"]:
                _doc_cache["sections"][current_section] = []
            _doc_cache["sections"][current_section].append(section)
    
    # Extract API references
    _extract_apis()

def _extract_apis():
    """Extract API definitions from documentation"""
    content = _doc_cache["content"]
    
    # Find @mcp decorators and class/function definitions
    patterns = [
        r'@mcp\.\w+\(\)',
        r'class\s+(\w+)',
        r'def\s+(\w+)\(',
        r'async\s+def\s+(\w+)\('
    ]
    
    apis = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        apis.update(matches)
    
    _doc_cache["apis"] = list(apis)

# ==================== DOCUMENTATION RETRIEVAL ====================

@mcp.tool()
async def search_mcp_docs(query: str, max_results: int = 5) -> dict:
    """🔍 Search MCP documentation"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"].lower()
        query_lower = query.lower()
        
        matches = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if query_lower in line:
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                context = '\n'.join(lines[start:end])
                
                matches.append({
                    "line": i + 1,
                    "match": line.strip(),
                    "context": context
                })
        
        matches = matches[:max_results]
        logger.info(f"✅ Found {len(matches)} matches for '{query}'")
        return {
            "success": True,
            "query": query,
            "matches": matches,
            "count": len(matches)
        }
    except Exception as e:
        logger.error(f"❌ Error searching docs: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_mcp_overview() -> dict:
    """📖 Get MCP documentation overview"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        overview = content[:1500] if len(content) > 1500 else content
        
        logger.info("✅ Retrieved MCP overview")
        return {
            "success": True,
            "overview": overview,
            "last_updated": _doc_cache["last_updated"]
        }
    except Exception as e:
        logger.error(f"❌ Error getting overview: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_mcp_sections() -> dict:
    """📋 List all MCP documentation sections"""
    try:
        await ensure_docs_loaded()
        
        sections = list(_doc_cache["sections"].keys())
        
        logger.info(f"✅ Listed {len(sections)} sections")
        return {
            "success": True,
            "sections": sections,
            "count": len(sections)
        }
    except Exception as e:
        logger.error(f"❌ Error listing sections: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_mcp_section(section_name: str) -> dict:
    """🔎 Get MCP documentation section"""
    try:
        await ensure_docs_loaded()
        
        if section_name not in _doc_cache["sections"]:
            matches = [s for s in _doc_cache["sections"].keys() if section_name.lower() in s.lower()]
            if not matches:
                return {"success": False, "error": f"Section '{section_name}' not found"}
            section_name = matches[0]
        
        content = '\n'.join(_doc_cache["sections"][section_name])
        
        logger.info(f"✅ Retrieved section: {section_name}")
        return {
            "success": True,
            "section": section_name,
            "content": content
        }
    except Exception as e:
        logger.error(f"❌ Error getting section: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_mcp_apis() -> dict:
    """🔌 List all MCP APIs and classes"""
    try:
        await ensure_docs_loaded()
        
        logger.info(f"✅ Listed {len(_doc_cache['apis'])} APIs")
        return {
            "success": True,
            "apis": _doc_cache["apis"],
            "count": len(_doc_cache["apis"])
        }
    except Exception as e:
        logger.error(f"❌ Error listing APIs: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def search_mcp_api(api_name: str) -> dict:
    """🔌 Search for MCP API reference"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        
        patterns = [
            f'`{api_name}',
            f'class {api_name}',
            f'def {api_name}',
            f'async def {api_name}'
        ]
        
        matches = {}
        for pattern in patterns:
            count = content.count(pattern)
            if count > 0:
                matches[pattern] = count
        
        if not matches:
            return {"success": False, "message": f"No reference found for '{api_name}'"}
        
        logger.info(f"✅ Found API reference for {api_name}")
        return {
            "success": True,
            "api_name": api_name,
            "patterns_found": matches
        }
    except Exception as e:
        logger.error(f"❌ Error searching API: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def extract_code_examples_mcp() -> dict:
    """💻 Extract Python code examples from MCP docs"""
    try:
        await ensure_docs_loaded()
        
        content = _doc_cache["content"]
        code_blocks = re.findall(r'```(?:python|py)?\n(.*?)\n```', content, re.DOTALL)
        
        logger.info(f"✅ Found {len(code_blocks)} code examples")
        return {
            "success": True,
            "code_blocks": code_blocks[:5],
            "total_code_blocks": len(code_blocks),
            "message": "Showing first 5 code blocks"
        }
    except Exception as e:
        logger.error(f"❌ Error extracting code: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_best_practices() -> dict:
    """✨ Get MCP best practices from documentation"""
    try:
        await ensure_docs_loaded()
        
        # Get Best Practices section
        section = await get_mcp_section("Best Practices")
        
        logger.info("✅ Retrieved best practices")
        return section
    except Exception as e:
        logger.error(f"❌ Error getting best practices: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_mcp_examples() -> dict:
    """📚 Get MCP implementation examples"""
    try:
        await ensure_docs_loaded()
        
        # Get Examples section
        section = await get_mcp_section("Examples & Tutorials")
        
        logger.info("✅ Retrieved examples")
        return section
    except Exception as e:
        logger.error(f"❌ Error getting examples: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def reload_mcp_docs() -> dict:
    """🔄 Reload MCP documentation"""
    try:
        _doc_cache["content"] = None
        _doc_cache["last_updated"] = None
        _doc_cache["sections"] = {}
        _doc_cache["apis"] = []
        
        await ensure_docs_loaded()
        
        logger.info("✅ MCP documentation reloaded")
        return {
            "success": True,
            "message": "Documentation reloaded",
            "last_updated": _doc_cache["last_updated"]
        }
    except Exception as e:
        logger.error(f"❌ Error reloading: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the MCP Documentation server"""
    try:
        logger.info("🔗 Starting MCP Documentation MCP Server on port 7100")
        await ensure_docs_loaded()
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7100)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
MCP Protocol Expert Prompt:
You are an expert in Model Context Protocol. Help developers understand the protocol,
design MCP servers, integrate with clients, and follow best practices for building
agentic systems with MCP.

MCP Server Developer Prompt:
You are building MCP servers. Help implement tools, resources, and prompts. Debug issues
with server implementation, optimize performance, and ensure protocol compliance.

MCP Integration Architect Prompt:
You are designing integrations using MCP. Help plan server architectures, compose multiple
servers, design secure implementations, and scale MCP systems.
"""
