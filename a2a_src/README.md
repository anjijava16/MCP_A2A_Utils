# A2A Source 🔗

## Overview
The core A2A (Agent-to-Agent) protocol implementation and source code for agent communication and orchestration. This provides the foundational protocol definitions and utilities for multi-agent systems.

## Features
- **A2A Protocol**: Agent-to-agent communication spec
- **Tool Registry**: Centralized tool definitions
- **Agent Discovery**: Service discovery for agents
- **Message Format**: Standardized message schema
- **Authentication**: Agent authentication
- **Orchestration**: Agent coordination

## Setup & Usage

### Installation
```bash
cd a2a_src
pip install -e .
```

### Configuration
```bash
export A2A_PROTOCOL_VERSION="1.0"
export A2A_REGISTRY_URL="http://localhost:8000"
```

## Protocol Specification

### Agent Identity
```python
agent = {
    "id": "agent_uuid",
    "name": "agent_name",
    "version": "1.0.0",
    "capabilities": ["read", "write", "execute"],
    "tools": [{"name": "tool1", ...}]
}
```

### Message Format
```python
message = {
    "id": "msg_uuid",
    "type": "request|response|notification",
    "from_agent": "source_agent_id",
    "to_agent": "target_agent_id",
    "tool": "tool_name",
    "arguments": {},
    "timestamp": "2024-06-15T10:00:00Z",
    "correlation_id": "corr_uuid"
}
```

## Tool Registry

### Registering Tools
```python
registry.register_tool(
    agent_id="agent_1",
    tool={
        "name": "calculate",
        "description": "Perform calculation",
        "input_schema": {...},
        "output_schema": {...}
    }
)
```

### Discovering Tools
```python
# Find all available tools
tools = registry.list_tools()

# Find tools by capability
tools = registry.find_tools(capability="math")

# Find tools by agent
tools = registry.get_agent_tools("agent_1")
```

## Agent Communication

### Direct Call
```python
# Agent A calls Agent B
result = a2a_client.call_remote_tool(
    target_agent="agent_b",
    tool="process_data",
    arguments={"data": [...]}
)
```

### Async Communication
```python
# Non-blocking call
future = a2a_client.call_remote_tool_async(
    target_agent="agent_b",
    tool="long_running_task",
    arguments={...}
)

# Wait for result
result = await future
```

## Multi-Agent Orchestration

### Sequential Execution
```python
# Execute tools in sequence
result = orchestrator.execute_sequence([
    {"agent": "agent_a", "tool": "prepare_data"},
    {"agent": "agent_b", "tool": "process_data"},
    {"agent": "agent_c", "tool": "analyze_results"}
])
```

### Parallel Execution
```python
# Execute tools in parallel
results = await orchestrator.execute_parallel([
    orchestrator.call("agent_a", "tool_1"),
    orchestrator.call("agent_b", "tool_2"),
    orchestrator.call("agent_c", "tool_3")
])
```

### Conditional Execution
```python
# Execute based on conditions
result = orchestrator.execute_conditional(
    condition=lambda x: len(x) > 10,
    on_true={"agent": "agent_a", "tool": "large_dataset_handler"},
    on_false={"agent": "agent_b", "tool": "small_dataset_handler"},
    data=input_data
)
```

## Authentication

### Agent Authentication
```python
# Register agent identity
auth.register_agent(
    agent_id="agent_1",
    public_key="...",
    capabilities=["read", "write"]
)

# Sign message
signed_message = auth.sign_message(message, private_key)

# Verify message
is_valid = auth.verify_message(signed_message, public_key)
```

## Error Handling

### Try-Catch Pattern
```python
try:
    result = a2a_client.call_remote_tool(...)
except AgentNotFoundError:
    # Handle missing agent
    log_error("Agent not found")
except ToolError:
    # Handle tool execution error
    log_error("Tool execution failed")
except TimeoutError:
    # Handle timeout
    log_error("Request timed out")
```

### Retry Logic
```python
result = a2a_client.call_with_retry(
    target_agent="agent_1",
    tool="process",
    arguments={},
    max_retries=3,
    backoff_factor=2
)
```

## Message Transport

### HTTP Transport
```python
transport = HTTPTransport(
    base_url="http://localhost:8000",
    timeout=30
)
```

### WebSocket Transport
```python
transport = WebSocketTransport(
    server_url="ws://localhost:8000",
    reconnect=True
)
```

### Async Transport
```python
transport = AsyncHTTPTransport(
    base_url="http://localhost:8000"
)
```

## Monitoring & Tracing

### Message Tracing
```python
# Enable message tracing
tracer = A2ATracer()

# Trace specific agent
traces = tracer.get_traces(agent_id="agent_1")

# Get execution flow
flow = tracer.get_execution_flow(correlation_id="corr_123")
```

### Performance Metrics
```python
# Get metrics
metrics = monitor.get_metrics()

# Average response time
avg_time = metrics["avg_response_time"]

# Error rate
error_rate = metrics["error_rate"]

# Throughput
throughput = metrics["requests_per_second"]
```

## Testing

### Unit Tests
```python
def test_agent_registration():
    agent_id = registry.register_agent(agent)
    assert agent_id is not None

def test_tool_discovery():
    tools = registry.find_tools(capability="math")
    assert len(tools) > 0
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_agent_communication():
    result = await a2a_client.call_remote_tool(
        target_agent="test_agent",
        tool="echo",
        arguments={"message": "hello"}
    )
    assert result["message"] == "hello"
```

## Configuration

### Protocol Config
```python
A2A_CONFIG = {
    "version": "1.0",
    "timeout": 30,
    "max_message_size": 1000000,
    "compression": "gzip",
    "verification": True
}
```

### Registry Config
```python
REGISTRY_CONFIG = {
    "backend": "redis|memory|database",
    "ttl": 3600,
    "sync_interval": 60
}
```

## Dependencies
- fastmcp
- mcp
- httpx
- websockets

## Use Cases
- Multi-agent systems
- Distributed processing
- Service orchestration
- Workflow automation
- Collaborative agents
- Federated learning

## Best Practices
1. Always sign messages
2. Use proper authentication
3. Implement error handling
4. Monitor performance
5. Use connection pooling
6. Implement retries
7. Log thoroughly
8. Version your protocol

## Future Enhancements
- [ ] End-to-end encryption
- [ ] Advanced scheduling
- [ ] Load balancing
- [ ] Service mesh integration
- [ ] Advanced tracing
