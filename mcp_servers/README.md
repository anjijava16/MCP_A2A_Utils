# MCP Servers (Aggregated) 📦

## Overview
A unified MCP servers project structure containing multiple server implementations and references. This directory serves as an organizational hub for various MCP server implementations with shared configurations and utilities.

## Structure

```
mcp_servers/
├── pyproject.toml              # Project configuration
├── A2A/                        # A2A protocol servers
├── mcp_end_end/               # End-to-end implementations
└── mcp_server_aws/            # AWS service servers
```

### A2A Directory
A2A protocol implementations for agent-to-agent communication servers:
- Agent communication protocols
- Service discovery
- Message routing
- Multi-agent orchestration

### mcp_end_end Directory
Complete end-to-end MCP server implementations demonstrating full lifecycle:
- Protocol implementation
- Tool definitions
- Transport layers
- Error handling
- Testing strategies

### mcp_server_aws Directory
AWS-integrated MCP servers for cloud operations:
- AWS service integration
- S3 operations
- RDS database operations
- Lambda invocation
- Cloud resource management

## Setup & Usage

### Installation
```bash
cd mcp_servers
pip install -e .
```

### Project Configuration
```toml
[project]
name = "mcp-servers"
version = "1.0.0"
description = "Unified MCP servers implementation"

[project.optional-dependencies]
a2a = ["google-adk", "protobuf"]
aws = ["boto3", "botocore"]
dev = ["pytest", "black", "mypy"]
```

## Running Servers

### A2A Protocol Server
```bash
# Start A2A server
python -m mcp_servers.a2a.server
```

### End-to-End Server
```bash
# Start end-to-end implementation
python -m mcp_servers.mcp_end_end.server
```

### AWS Server
```bash
# Start AWS integration server
export AWS_REGION=us-east-1
python -m mcp_servers.mcp_server_aws.server
```

## Tools & Features

### Shared Tools
All servers in this project share:
- Input validation
- Error handling
- Logging
- Configuration management

### Server-Specific Tools

#### A2A Tools
- Agent registration
- Service discovery
- Message routing
- Protocol negotiation

#### End-to-End Tools
- Complete workflow execution
- Multi-step operations
- State management
- Comprehensive error handling

#### AWS Tools
- S3 bucket operations
- RDS database queries
- Lambda function invocation
- EC2 instance management
- CloudWatch monitoring

## Configuration

### Shared Configuration
```python
# config.py
MCP_CONFIG = {
    "server_name": "mcp_servers",
    "version": "1.0.0",
    "default_port": 8000,
    "timeout": 30,
    "max_connections": 100
}
```

### Environment Variables
```bash
# General
export MCP_SERVER_PORT=8000
export MCP_LOG_LEVEL=INFO

# AWS
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# A2A
export A2A_REGISTRY_URL=http://localhost:8001
export A2A_AGENT_ID=agent_1
```

## Development Guidelines

### Adding New Server
1. Create directory: `mcp_servers/my_server/`
2. Implement: `__init__.py`, `server.py`, `tools.py`
3. Add tests: `tests/test_my_server.py`
4. Update: `pyproject.toml` with dependencies
5. Document: Create `README.md`

### Directory Layout
```
my_server/
├── __init__.py          # Package initialization
├── server.py            # Main server implementation
├── tools.py             # Tool definitions and handlers
├── config.py            # Configuration
├── utils.py             # Utilities and helpers
└── tests/
    ├── __init__.py
    ├── test_server.py
    └── test_tools.py
```

### Tool Definition Template
```python
# tools.py
from mcp import Tool

tools = {
    "my_tool": {
        "description": "Tool description",
        "inputSchema": {
            "type": "object",
            "properties": {
                "param1": {"type": "string"},
                "param2": {"type": "integer"}
            },
            "required": ["param1"]
        }
    }
}

async def handle_my_tool(args):
    """Handle my_tool invocation"""
    param1 = args["param1"]
    param2 = args.get("param2", 0)
    
    # Execute tool logic
    result = perform_operation(param1, param2)
    
    return {"result": result}
```

## Testing

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_server.py

# Run with coverage
pytest --cov=mcp_servers tests/
```

### Test Template
```python
import pytest
from mcp_servers.my_server.server import MyMCPServer

@pytest.fixture
async def server():
    server = MyMCPServer()
    await server.initialize()
    yield server
    await server.shutdown()

@pytest.mark.asyncio
async def test_tool_execution(server):
    result = await server.execute_tool("my_tool", {"param1": "value"})
    assert result is not None
```

## Logging & Monitoring

### Logger Configuration
```python
import logging

logger = logging.getLogger(__name__)

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics
```python
# Track tool usage
metrics = {
    "tool_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0,
    "avg_response_time": 0
}

def record_metric(tool_name, success, response_time):
    metrics["tool_calls"] += 1
    if success:
        metrics["successful_calls"] += 1
    else:
        metrics["failed_calls"] += 1
```

## Deployment

### Local Development
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run server in development mode
python -m mcp_servers.a2a.server --debug
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY mcp_servers/ ./mcp_servers/

CMD ["python", "-m", "mcp_servers.a2a.server"]
```

### Cloud Deployment
```bash
# Deploy to Cloud Run
gcloud run deploy mcp-servers \
  --source . \
  --platform managed \
  --region us-central1

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
```

## Best Practices
1. Document all tools thoroughly
2. Implement comprehensive error handling
3. Use async/await for I/O operations
4. Add proper logging
5. Write unit tests
6. Follow consistent code style
7. Version your APIs
8. Monitor performance

## Troubleshooting

### Server Won't Start
- Check port availability
- Verify dependencies installed
- Check configuration
- Review logs

### Tool Not Working
- Verify tool is registered
- Check input parameters
- Review error messages
- Enable debug logging

## Contributing
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

## Future Enhancements
- [ ] Integrated monitoring dashboard
- [ ] Advanced scheduling
- [ ] Distributed execution
- [ ] Enhanced security
- [ ] Performance optimization
