# LangChain MCP Server & Client 🔗

## Overview
Integration implementations demonstrating how to use MCP servers with LangChain framework. This folder contains client and adapter code for connecting LangChain agents and tools to MCP servers, enabling seamless tool use within LangChain applications.

## Features
- **LangChain Integration**: Connect LangChain tools to MCP servers
- **Tool Adapters**: Convert MCP tools to LangChain tools
- **Agent Support**: Compatible with LangChain agents
- **Multiple Transports**: Supports Stdio and SSE transports
- **Type Safety**: Full type hints and validation
- **Error Handling**: Comprehensive error handling

## Architecture

```
┌─────────────────────────────────┐
│    LangChain Application        │
├─────────────────────────────────┤
│  • Agents                       │
│  • Tools                        │
│  • Chains                       │
└──────────────┬──────────────────┘
               │
        ┌──────▼──────────┐
        │ LangChain MCP   │
        │ Adapter Layer   │
        │  - Tool Convert │
        │  - Response Map │
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ MCP Clients     │
        │  - Stdio        │
        │  - SSE          │
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ MCP Servers     │
        │  - Tools        │
        │  - Resources    │
        └─────────────────┘
```

## Files
- `agntoagentic.ipynb` - Agent-to-agent notebook with MCP integration
- Additional implementation files for MCP-LangChain integration

## Setup & Usage

### Installation
```bash
pip install langchain langgraph mcp httpx
```

### Configuration
```bash
# Set up MCP server connection
export MCP_SERVER_URL="http://localhost:8000/sse"
export MCP_SERVER_TYPE="sse"  # or "stdio"
```

### Basic Usage

#### Connect to MCP Server
```python
from langchain_mcp_adapters import MCPTools

# Create adapter
mcp_tools = MCPTools(
    server_url="http://localhost:8000/sse",
    transport="sse"
)

# Get all available tools
tools = mcp_tools.get_tools()
```

#### Use in LangChain Agent
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Create agent with MCP tools
agent = create_tool_calling_agent(
    llm=model,
    tools=tools,
    prompt=prompt
)

# Run agent
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "query"})
```

## Integration Patterns

### Pattern 1: Simple Tool Use
```python
# Load MCP tools as LangChain tools
tools = mcp_adapter.get_all_tools()

# Use with agent
agent.invoke({"query": "Use these tools to..."})
```

### Pattern 2: Tool Filtering
```python
# Use only specific tools
specific_tools = mcp_adapter.get_tools(
    filter=["weather", "search"]
)

# Create agent with subset
agent = create_agent(llm, specific_tools)
```

### Pattern 3: Tool Wrapping
```python
# Wrap with additional logic
def wrapped_tool(tool):
    def wrapper(*args, **kwargs):
        print(f"Calling {tool.name}")
        result = tool(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

wrapped_tools = [wrapped_tool(t) for t in tools]
```

## Tool Conversion

### MCP Tool → LangChain Tool
The adapter converts MCP tools to LangChain's tool format:

```python
# MCP Tool
{
    "name": "get_weather",
    "description": "Get weather for location",
    "inputSchema": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        }
    }
}

# Becomes LangChain Tool
Tool(
    name="get_weather",
    description="Get weather for location",
    func=async_tool_executor,
    args_schema=LocationSchema
)
```

## Agent Examples

### Weather Agent
```python
from langchain.agents import tool

@tool
def get_location_weather(location: str) -> str:
    """Get weather for a location"""
    return mcp_tools.call("get_weather", {"location": location})

# Use in agent
agent = create_tool_calling_agent(llm, [get_location_weather])
```

### Research Agent
```python
# Load all research-related MCP tools
research_tools = [
    mcp_tools.get_tool("search_arxiv"),
    mcp_tools.get_tool("search_papers"),
    mcp_tools.get_tool("extract_metadata")
]

# Create agent
research_agent = create_agent(llm, research_tools)

# Run research task
research_agent.invoke({"input": "Find papers on ML"})
```

### Database Agent
```python
# Get database tools from MCP server
db_tools = [
    mcp_tools.get_tool("query_database"),
    mcp_tools.get_tool("list_tables"),
    mcp_tools.get_tool("get_schema")
]

# Create agent
db_agent = create_agent(llm, db_tools)

# Query database through agent
result = db_agent.invoke({"input": "What tables exist?"})
```

## Transport Configuration

### Stdio Transport
```python
# For local MCP servers
adapter = MCPTools(
    command="python",
    args=["path/to/server.py"],
    transport="stdio"
)
```

### SSE Transport
```python
# For remote MCP servers
adapter = MCPTools(
    server_url="http://localhost:8000/sse",
    transport="sse"
)
```

### HTTP Transport
```python
# For REST-based MCP servers
adapter = MCPTools(
    server_url="http://localhost:8000",
    transport="http"
)
```

## Error Handling

### Tool Errors
```python
try:
    result = agent.invoke({"input": "query"})
except ToolError as e:
    print(f"Tool error: {e}")
except Exception as e:
    print(f"Agent error: {e}")
```

### Timeout Handling
```python
# Tools with timeout
tool_result = run_with_timeout(
    tool_call,
    timeout=30
)
```

### Retry Logic
```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def call_tool_safe(tool_name, args):
    return await mcp_adapter.call(tool_name, args)
```

## Performance Optimization

### Tool Caching
```python
# Cache tool definitions
cached_tools = mcp_adapter.get_tools(cache=True)
```

### Batch Tool Calls
```python
# Execute multiple tools efficiently
results = await mcp_adapter.call_batch([
    ("tool1", args1),
    ("tool2", args2)
])
```

### Lazy Loading
```python
# Load tools on demand
def get_tool_lazy(name):
    return mcp_adapter.get_tool(name)
```

## Advanced Features

### Custom Tool Wrapper
```python
class CustomMCPTool(Tool):
    def __init__(self, mcp_tool):
        self.mcp_tool = mcp_tool
    
    def invoke(self, args):
        # Custom preprocessing
        processed = self.preprocess(args)
        # Call MCP tool
        result = self.mcp_tool(**processed)
        # Custom postprocessing
        return self.postprocess(result)
```

### Tool Composition
```python
# Compose multiple tools
@tool
def composed_tool(query: str):
    """Use multiple tools together"""
    search_results = mcp.search(query)
    summaries = [mcp.summarize(r) for r in search_results]
    return mcp.compile(summaries)

agent_tools.append(composed_tool)
```

### Conditional Tool Use
```python
# Use different tools based on conditions
def select_tools(task_type):
    if task_type == "research":
        return research_tools
    elif task_type == "database":
        return database_tools
    else:
        return general_tools
```

## Testing & Validation

### Unit Tests
```python
import pytest

@pytest.mark.asyncio
async def test_mcp_tool_conversion():
    adapter = MCPTools(server_url="...")
    tools = adapter.get_tools()
    assert len(tools) > 0
    assert all(hasattr(t, 'invoke') for t in tools)
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_agent_with_mcp_tools():
    agent = create_agent(llm, mcp_tools)
    result = await agent.ainvoke({"input": "test"})
    assert result["output"] is not None
```

## LangChain Ecosystem Integration

### With LangGraph
```python
from langgraph.graph import StateGraph

# Add MCP tools to graph
graph = StateGraph(State)
graph.add_node("agent", create_tool_calling_agent(llm, mcp_tools))
```

### With Chains
```python
from langchain.chains import LLMChain

# Use MCP tools in chain
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    tools=mcp_tools.get_tools()
)
```

### With Memory
```python
from langchain.memory import ConversationBufferMemory

# Agent with memory and MCP tools
memory = ConversationBufferMemory()
agent = create_tool_calling_agent(
    llm=llm,
    tools=mcp_tools.get_tools(),
    memory=memory
)
```

## Notebook: Agent-to-Agent Implementation

The `agntoagentic.ipynb` notebook demonstrates:
1. Setting up MCP server connection
2. Loading and converting MCP tools
3. Creating LangChain agents with MCP tools
4. Multi-agent coordination
5. Tool orchestration patterns
6. Error handling and recovery

## Common Issues & Solutions

### Tools Not Loading
```python
# Debug tool loading
tools = mcp_adapter.get_tools(debug=True)
# Will print tool names and schemas
```

### Type Mismatch
```python
# Ensure tool arguments match schema
tool_definition = mcp_adapter.get_tool_schema("tool_name")
print(tool_definition)  # Check argument types
```

### Connection Errors
```python
# Test connection before creating agent
is_connected = mcp_adapter.test_connection()
if not is_connected:
    print("Cannot connect to MCP server")
```

## Best Practices
1. Always validate tool definitions before use
2. Implement proper error handling
3. Use tool descriptions clearly
4. Cache tool definitions
5. Monitor tool performance
6. Log tool calls for debugging
7. Test with edge cases

## Dependencies
- langchain
- langgraph
- mcp
- httpx
- pydantic

## Documentation
- See `agntoagentic.ipynb` for detailed implementation
- Review LangChain documentation: https://python.langchain.com
- Review MCP specification: https://modelcontextprotocol.io

## Future Enhancements
- [ ] Automatic tool documentation generation
- [ ] Tool recommendation engine
- [ ] Advanced caching strategies
- [ ] Performance profiling
- [ ] Distributed tool execution
- [ ] Tool versioning support
