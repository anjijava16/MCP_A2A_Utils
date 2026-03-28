# Documentation MCP Servers Ecosystem 📚

## Overview

Comprehensive suite of documentation servers built with Python FastMCP. These servers provide programmatic access to critical documentation for AI, protocols, and frameworks through standardized MCP interface.

## Available Documentation Servers

### 1. 📚 ADK Documentation Server (Port 7099)
**Purpose**: Google Agent Development Kit documentation access  
**Tools**: 9 tools including search, section retrieval, code extraction  
**Features**:
- Real-time fetching from official ADK docs
- Smart section parsing and indexing
- Code example extraction
- Related topic discovery
- Full documentation access

**Best For**: ADK developers learning and building agents

**Key Tools**:
- `search_adk_docs` - Full-text search with context
- `get_adk_overview` - Quick start
- `list_adk_sections` - Browse structure
- `get_adk_section` - Get specific section
- `extract_code_examples` - Get Python examples
- `find_related_topics` - Discover related content
- `search_api_reference` - Look up APIs
- `get_doc_stats` - Documentation statistics
- `reload_documentation` - Refresh from source

---

### 2. 🔗 MCP Protocol Documentation Server (Port 7100)
**Purpose**: Model Context Protocol specification and implementation guide  
**Tools**: 9+ tools for protocol documentation  
**Features**:
- Complete protocol specification
- Implementation patterns and examples
- API reference for MCP decorators
- Best practices guide
- Built-in fallback documentation

**Best For**: MCP server developers and integrators

**Key Tools**:
- `search_mcp_docs` - Search MCP documentation
- `get_mcp_overview` - Protocol overview
- `list_mcp_sections` - Browse topics
- `get_mcp_section` - Get specific section
- `list_mcp_apis` - List all APIs
- `search_mcp_api` - Look up API reference
- `extract_code_examples_mcp` - Get examples
- `get_best_practices` - Best practices guide
- `get_mcp_examples` - Implementation tutorials
- `reload_mcp_docs` - Refresh documentation

---

## Architecture

### Standardized Pattern

All documentation servers follow the same architecture:

```
DocumentationServer
├── Fetch/Load Documentation
├── Parse into Sections
├── Index for Fast Lookup
├── Provide Search & Access Tools
└── Cache with Refresh Capability
```

### Key Components

**1. Content Fetching**
```python
# Fetch from remote source
async def fetch_docs() -> str:
    response = await client.get(url)
    return response.text
```

**2. Section Parsing**
```python
# Parse into logical sections
def _parse_sections():
    sections = re.split(r'^(#{1,3}\s+.*?)$', content)
    # Index sections for fast lookup
```

**3. Caching Layer**
```python
# In-memory cache with refresh
_doc_cache = {
    "content": None,
    "sections": {},
    "last_updated": None
}
```

**4. Tool Implementation**
```python
@mcp.tool()
async def search_docs(query: str) -> dict:
    # Search implementations with context
    # Return structured results
```

## Tool Categories

### Retrieval Tools (Universal)
- **Search**: Full-text search with context
- **List**: Browse available sections
- **Get**: Retrieve specific section
- **Overview**: Quick start overview

### Reference Tools
- **API Search**: Look up specific APIs
- **Code Examples**: Extract code blocks
- **Related Content**: Find related topics

### Utility Tools
- **Statistics**: Get doc size, section count, etc.
- **Reload**: Refresh from remote source
- **Full Access**: Get entire documentation

## Transport Configuration

| Server | Port | Transport | Host |
|--------|------|-----------|------|
| ADK Docs | 7099 | SSE | 0.0.0.0 |
| MCP Protocol | 7100 | SSE | 0.0.0.0 |

## Running All Servers

### Individually
```bash
python adk_mcp_server/server.py          # Port 7099
python mcp_docs_server/server.py         # Port 7100
```

### Together
```bash
# Terminal 1
python adk_mcp_server/server.py

# Terminal 2
python mcp_docs_server/server.py
```

## Claude Desktop Integration

Add all servers to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "adk-docs": {
      "command": "python",
      "args": ["adk_mcp_server/server.py"],
      "env": {}
    },
    "mcp-protocol": {
      "command": "python",
      "args": ["mcp_docs_server/server.py"],
      "env": {}
    }
  }
}
```

## Usage Patterns

### Pattern 1: Learning
1. Get overview with `get_*_overview()`
2. Browse sections with `list_*_sections()`
3. Read specific section with `get_*_section()`
4. Extract examples with `extract_code_examples()`

### Pattern 2: Reference Lookup
1. Search with `search_*_docs()`
2. API lookup with `search_api_reference()`
3. Get detailed section for context

### Pattern 3: Implementation Guide
1. Get overview to understand scope
2. Extract code examples for patterns
3. Look up specific APIs as needed
4. Find best practices for guidance

### Pattern 4: Discovery
1. Use `find_related_topics()` to explore
2. Search for keywords of interest
3. Browse sections that match interests

## Response Format (Standardized)

All tools return structured responses:

```python
{
    "success": True,           # Operation successful
    "message": "...",          # Human readable message
    "error": "..."            # Error details (if failed)
    # Custom fields per tool
}
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Search | <100ms | Full-text over cached content |
| Section Get | <50ms | Pre-indexed section retrieval |
| Overview | <20ms | Cached excerpt from start |
| Code Extract | <200ms | Regex parsing of content |
| Reload | 1-2s | Network fetch from remote |

## Caching Strategy

1. **Lazy Load**: Documentation loaded on first request
2. **Section Parsing**: Content parsed into sections for fast lookup
3. **Persistent Cache**: Remains in memory during server lifetime
4. **On-Demand Reload**: Refresh with `reload_*_docs()` tool
5. **Timestamps**: Track last update time

## Error Handling

### Network Failures
- Fallback to built-in documentation (where available)
- Gracefully handle missing remote sources
- Retry logic on timeout

### Content Issues
- Fuzzy matching for section names
- Multiple search patterns for APIs
- Useful error messages when content not found

### Resource Management
- In-memory caching prevents repeated fetches
- Regular memory management
- Configurable cache limits

## Security Considerations

1. **HTTPS**: Remote fetches use HTTPS
2. **Timeouts**: 30-second timeout on fetches
3. **Input Validation**: Regex patterns prevent injection
4. **No Credentials**: No sensitive data in requests

## Extensibility

### Adding New Documentation Server

1. Create new directory: `mcp_*_docs_server/`
2. Implement `server.py` following pattern
3. Add fetch, parse, tools
4. Create README with usage
5. Configure port in `main()` function

### Adding Custom Tools

```python
@mcp.tool()
async def custom_tool(param: str) -> dict:
    """Custom tool description"""
    await ensure_docs_loaded()
    # Implement tool logic
    return {"success": True, "result": ...}
```

## Future Expansion

Potential additional documentation servers:

- **OpenAI API Docs** (Port 7101)
- **Google Cloud Docs** (Port 7102)
- **AWS Documentation** (Port 7103)
- **FastMCP Library** (Port 7104)
- **Python Stdlib Reference** (Port 7105)
- **JavaScript/TypeScript Docs** (Port 7106)

## Comparison Matrix

| Feature | ADK Docs | MCP Protocol | Potential Others |
|---------|:--------:|:------------:|:----------------:|
| Search | ✅ | ✅ | ✅ |
| Browse Sections | ✅ | ✅ | ✅ |
| Code Examples | ✅ | ✅ | ✅ |
| API Reference | ✅ | ✅ | ✅ |
| Best Practices | ✅ | ✅ | ✅ |
| Offline Support | Partial | Yes | Yes |
| Refresh | Yes | Yes | Yes |

## Integration Patterns

### With Database Servers
Combine with data warehouse docs for complete platform knowledge

### With Tool MCP Servers
Use documentation servers to learn about tool development

### With Agent Frameworks
Use ADK & MCP servers to build informed agents

## Troubleshooting

### "Documentation not loading"
1. Check network connectivity
2. Try `reload_documentation()`
3. Falls back to local content if available

### "Search returns no results"
1. Try different keywords
2. Use `list_sections()` to browse
3. Use `find_related_topics()` for discovery

### "Server won't start"
1. Check port is available
2. Verify Python 3.10+
3. Install required packages: `pip install fastmcp httpx`

## Development Guide

### Adding Search Enhancement
```python
# Add filtering by section
@mcp.tool()
async def search_section(query: str, section: str) -> dict:
    content = _doc_cache["sections"][section]
    # Search within specific section
```

### Adding Highlighting
```python
# Return matches with HTML highlights
def highlight_matches(text: str, query: str) -> str:
    return text.replace(query, f"<mark>{query}</mark>")
```

### Adding Curation
```python
# Maintain curated lists of important topics
@mcp.tool()
async def get_essentials() -> dict:
    return _essential_topics  # Pre-curated list
```

## Performance Optimization

1. **Lazy Loading**: Load docs only when needed
2. **Section Indexing**: Pre-parse into sections
3. **Caching**: Keep in memory after first load
4. **Efficient Search**: Use compiled regex patterns
5. **Streaming**: Return large results efficiently

## Monitoring & Logging

All servers use structured logging with emoji prefixes:
- ✅ Success operations
- ❌ Errors and failures
- ⚠️ Warnings and issues
- 📚 Documentation-specific events

## support & Resources

- Individual server READMEs for detailed usage
- Source code for integration patterns
- MCP Protocol documentation for technical details
- AGK documentation for agent building

---

## Quick Reference

| Task | Tools | Servers |
|------|-------|---------|
| Learn ADK | overview, sections, examples | ADK Docs |
| Build MCP Server | overview, patterns, examples | MCP Protocol |
| Look Up API | search_api, api_reference | Both |
| Find Code Example | extract_code_examples | Both |
| Understand Best Practices | get_best_practices | Both |
| Discover Related Topics | find_related_topics | Both |

**Total Servers**: 2 Documentation servers  
**Total Tools**: 18+ documentation access tools  
**Ports**: 7099-7100 (expandable)  
**Transport**: SSE (extensible)  
**Status**: Production-ready ✅

