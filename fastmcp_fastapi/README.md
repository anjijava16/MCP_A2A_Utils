# FastMCP + FastAPI Integration 🚀

## Overview
This is a bridge implementation demonstrating how to integrate FastMCP servers with FastAPI applications. It shows how to combine MCP (Model Context Protocol) tools with FastAPI's web framework for creating hybrid applications with both web endpoints and MCP tool capabilities.

## Features
- **Dual Framework Integration**: Combines FastAPI and FastMCP in single application
- **Web API Endpoints**: Traditional REST API endpoints
- **MCP Tools**: Model Context Protocol tools alongside web routes
- **Async Support**: Full async/await implementation
- **Tool Context**: Access FastAPI context in MCP tools
- **Hybrid Architecture**: Best of both worlds

## Architecture

```
FastAPI Application
├── REST API Endpoints
│   └── /api/status - Server status
│   └── /api/data - Data endpoints
│
└── MCP Server
    ├── Tools
    │   ├── query_database
    │   ├── get_weather
    │   └── ...
    └── Resources
        └── Shared functionality
```

## Setup & Usage

### Installation
```bash
pip install fastapi fastmcp uvicorn httpx
```

### Running the Server
```bash
# Start FastAPI with MCP integration
python fastapi_fastmcp.py

# Server runs on http://localhost:8000
# FastMCP available for tool calls
# FastAPI serves REST endpoints
```

Access endpoints:
- Web: http://localhost:8000/api/status
- API Docs: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json

## Files
- `fastapi_fastmcp.py` - Main integration implementation

## Implementation Details

### FastAPI Setup
```python
from fastapi import FastAPI

api = FastAPI()

@api.get("/api/status")
def status():
    return {"status": "ok"}
```

### MCP Integration
```python
from fastmcp import FastMCP

mcp = FastMCP("API Tools")

@mcp.tool()
async def query_database(query: str) -> dict:
    """Run a database query"""
    return {"result": "data"}
```

### Combined Server
Both FastAPI and MCP run in the same application, sharing:
- Request context
- Shared utilities
- Database connections
- Configuration

## Tools Available

### Database Tools
- `query_database(query)` - Execute database queries

### Weather Tools
- `get_weather(city, ctx)` - Get weather information (with context support)

### Additional Tools
- Can be extended with more functionality
- Share state with FastAPI application
- Access request context and dependencies

## Use Cases
- **API with Tool Support**: Add tool-based capabilities to REST API
- **Hybrid Applications**: Combine traditional APIs with AI agent tools
- **Claude/GPT Integration**: Agents use either API endpoints or MCP tools
- **Unified Backend**: Single deployment for multiple interfaces
- **Migration Path**: Gradually transition to MCP-based architecture

## API Examples

### REST Endpoint
```bash
curl http://localhost:8000/api/status
# Returns: {"status": "ok"}
```

### OpenAPI Documentation
```bash
curl http://localhost:8000/openapi.json
# Returns: OpenAPI schema for all endpoints
```

### Swagger UI
Visit: http://localhost:8000/docs
- Interactive API testing
- Tool documentation
- Parameter exploration

## Advanced Integration

### Shared Context
MCP tools can access FastAPI context:
```python
@mcp.tool()
async def get_weather(city: str, ctx: Context):
    """Get weather with FastAPI context"""
    # Can access ctx for shared state
    return current_weather
```

### Database Connections
Share database connections between FastAPI and MCP:
```python
# Single connection pool
db = get_database_connection()

# Used by both FastAPI routes and MCP tools
```

### Error Handling
Unified error handling across both frameworks:
```python
# FastAPI: Returns HTTP error codes
# MCP: Returns tool error codes
# Both use same underlying handlers
```

## Deployment

### Local Development
```bash
python fastapi_fastmcp.py
```

### Production with Uvicorn
```bash
uvicorn fastapi_fastmcp:api --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY fastapi_fastmcp.py .
CMD ["uvicorn", "fastapi_fastmcp:api", "--host", "0.0.0.0", "--port", "8000"]
```

## Performance Considerations
- **Async Operations**: Both frameworks fully async
- **Shared Resources**: Efficient resource utilization
- **Connection Pooling**: Single pool for both interfaces
- **Caching**: Shared caching layer
- **Load Distribution**: Balance between API calls and tool calls

## Security
- **Authentication**: Can implement for both APIs and tools
- **Rate Limiting**: Protect against abuse
- **Input Validation**: Pydantic validation in FastAPI
- **Error Messages**: No sensitive info exposed
- **CORS**: Handle cross-origin requests

## Extensibility

### Adding More Endpoints
```python
@api.get("/api/data/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "data": ...}
```

### Adding More Tools
```python
@mcp.tool()
def new_tool(param: str) -> str:
    return f"Result: {param}"
```

### Middleware
```python
@api.middleware("http")
async def add_middleware(request, call_next):
    response = await call_next(request)
    return response
```

## Monitoring & Logging
- FastAPI request logging
- MCP tool execution tracking
- Performance metrics
- Error reporting
- Activity audit logs

## Testing

### Unit Tests
```python
from fastapi.testclient import TestClient

client = TestClient(api)

def test_status():
    response = client.get("/api/status")
    assert response.status_code == 200
```

### Tool Tests
```python
# Test MCP tools independently
result = await mcp._tools["query_database"].fn(query="SELECT *")
assert result["status"] == "success"
```

## Integration Patterns

### Pattern 1: API First
- Expose MCP tools through API endpoints
- Tools act as backend for API

### Pattern 2: Tool First
- Primary interface is MCP tools
- FastAPI provides auxiliary endpoints

### Pattern 3: Hybrid
- Both interfaces equally important
- Share all functionality

## Dependencies
- fastapi
- fastmcp
- uvicorn
- httpx
- pydantic

## Troubleshooting
- Check port availability
- Verify all imports
- Test endpoints with curl/Postman
- Review logs for errors
- Validate tool definitions

## Future Enhancements
- WebSocket support for real-time tools
- GraphQL interface
- gRPC endpoints
- Advanced authentication
- Multi-tenancy support
- Kubernetes deployment patterns
- Monitoring and observability

## Example Use Case
A financial application could use:
- **FastAPI**: REST API for user interface
- **MCP Tools**: Currency conversion, rate lookups, calculations
- **Shared**: Database connections, configuration

Both interfaces serve the application in their best way.
