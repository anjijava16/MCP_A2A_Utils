# Agno Agentic MCP 🤖

## Overview
An MCP integration implementation using the Agno framework for building agentic applications with tool support. This combines the Agno agent framework with MCP tools for creating powerful multi-capability agents.

## Features
- **Agno Integration**: Uses Agno framework for agents
- **Tool Support**: Seamless MCP tool integration
- **Agent Orchestration**: Build complex agent workflows
- **Multi-Step Reasoning**: Chain multiple operations
- **Async Support**: Full async/await support
- **State Management**: Track agent state across steps

## Architecture

```
Agno Agent
├── Core Agent Logic
├── Tool Bindings
│   └── MCP Tools
├── State Management
└── Result Processing
```

## Setup & Usage

### Installation
```bash
pip install agno fastmcp mcp
```

### Configuration
```bash
export AGNO_FRAMEWORK="agno"
export MCP_SERVER_URL="http://localhost:8000/sse"
```

### Running
```python
from agno_agentic_mcp import AgentoAgenticAgent

agent = AgentoAgenticAgent(
    name="my_agent",
    mcp_url="http://localhost:8000/sse"
)

result = agent.run("query or task")
```

## Tool Integration

### Binding MCP Tools
```python
# Automatically load MCP tools
agent.load_mcp_tools(
    server_url="http://localhost:8000/sse"
)

# Or manually add tools
agent.add_tool(tool_definition)
```

### Tool Execution
```python
# Tools execute through agent
result = agent.run(
    "Use weather tool to get NYC weather"
)
# Agent automatically:
# - Selects appropriate tool
# - Prepares arguments
# - Executes tool
# - Processes results
```

## Agent Capabilities

### Multi-Step Reasoning
```python
# Complex task with multiple steps
result = agent.run("""
1. Search for flights to NYC
2. Check hotel prices
3. Compare costs
4. Recommend best option
""")
```

### Tool Selection
```python
# Agent intelligently selects tools
response = agent.run(
    "Find the weather and nearest restaurants"
)
# Agent determines:
# - Needs weather tool
# - Needs restaurant search tool
# - Executes both
# - Synthesizes response
```

## Examples

### Weather Agent
```python
agent = AgentoAgenticAgent(name="weather_agent")
agent.load_mcp_tools()

response = agent.run("What's the weather in NYC?")
```

### Research Agent
```python
agent = AgentoAgenticAgent(name="research_agent")
agent.load_mcp_tools()

response = agent.run("""
Search for papers on machine learning
and summarize recent research trends
""")
```

### Analysis Agent
```python
agent = AgentoAgenticAgent(name="analysis_agent")
agent.load_mcp_tools()

response = agent.run("""
Analyze stock prices for AAPL, GOOG, MSFT
and provide investment recommendations
""")
```

## Advanced Features

### Custom Instructions
```python
SYSTEM_INSTRUCTION = """
You are a helpful assistant that:
- Uses tools efficiently
- Provides clear explanations
- Asks for clarification when needed
"""

agent = AgentoAgenticAgent(
    name="assistant",
    system_instruction=SYSTEM_INSTRUCTION
)
```

### Memory Management
```python
# Agent maintains conversation history
agent.run("First question")
agent.run("Follow-up question")  # Has context

# Get conversation history
history = agent.get_history()
```

### Error Handling
```python
try:
    result = agent.run(task)
except ToolError as e:
    agent.log_error(e)
    # Retry with different approach
except Exception as e:
    agent.handle_error(e)
```

## Notebook Implementation

The folder contains notebook demonstrations:
- Agent initialization
- Tool loading
- Multi-agent coordination
- Error handling
- Result processing

## Testing

### Unit Tests
```python
def test_agent_creation():
    agent = AgentoAgenticAgent(name="test")
    assert agent.name == "test"
    assert agent.tools is not None

def test_tool_execution():
    agent = AgentoAgenticAgent()
    agent.load_mcp_tools()
    result = agent.run("test query")
    assert result is not None
```

## Performance Optimization

### Tool Caching
```python
# Cache tool definitions
agent.cache_tools = True
agent.cache_ttl = 3600
```

### Parallel Execution
```python
# Execute independent tools in parallel
response = agent.run(
    "Get weather, check news, get stock prices"
)
# Agent runs all three tools in parallel
```

## Configuration

### Agent Config
```python
AGENT_CONFIG = {
    "name": "assistant",
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
    "timeout": 30
}
```

## Use Cases
- Virtual assistants
- Research automation
- Data analysis
- Customer service
- Task automation
- Decision support

## Monitoring

### Agent Metrics
```python
metrics = agent.get_metrics()
# Returns:
# - tool_count: number of available tools
# - execution_time: total execution time
# - success_rate: percentage of successful calls
# - tool_usage: breakdown of tool usage
```

## Best Practices
1. Start with clear task definitions
2. Provide good context
3. Use system instructions effectively
4. Handle errors gracefully
5. Monitor tool usage
6. Test with edge cases
7. Document agent behavior

## Troubleshooting

### Tools Not Loading
```python
# Debug tool loading
tools = agent.list_available_tools()
print(f"Loaded {len(tools)} tools")
```

### Execution Issues
```python
# Enable verbose logging
agent.verbose = True
result = agent.run(task)
# Will print detailed execution steps
```

## Dependencies
- agno
- fastmcp
- mcp
- httpx

## Future Enhancements
- [ ] Multi-agent collaboration
- [ ] Advanced planning
- [ ] Better memory management
- [ ] Tool result caching
- [ ] Distributed execution
