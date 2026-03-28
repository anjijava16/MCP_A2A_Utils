# Snowflake MCP 🏔️

## Overview
A comprehensive guide and implementation for building and evaluating LangGraph agents with MCP tools integrated with Snowflake data warehouse. This project demonstrates how to evaluate agent performance using TruLens when interacting with Snowflake data.

## Features
- **LangGraph Agents**: State-of-the-art agent orchestration framework
- **MCP Tool Integration**: Use MCP servers as agent tools
- **Snowflake Integration**: Connect to Snowflake data warehouse
- **Agent Evaluation**: TruLens-based evaluation and monitoring
- **Performance Metrics**: Comprehensive evaluation framework
- **Multi-agent Patterns**: Complex orchestration examples

## Architecture

```
┌──────────────────────────────────────────┐
│    LangGraph Agent                       │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │ State Management                   │  │
│  └────────────────────────────────────┘  │
│  ┌────────────────────────────────────┐  │
│  │ Tool Invocation                    │  │
│  │  ├── MCP Tools                     │  │
│  │  ├── Snowflake Queries             │  │
│  │  └── Data Processing               │  │
│  └────────────────────────────────────┘  │
└──────────────┬───────────────────────────┘
               │
        ┌──────▼──────────┐
        │ Snowflake       │
        │ Data Warehouse  │
        │  - Tables       │
        │  - Queries      │
        │  - Analytics    │
        └─────────────────┘
        
        ┌──────────────────┐
        │ TruLens          │
        │ Evaluation       │
        │  - Metrics       │
        │  - Feedback      │
        │  - Monitoring    │
        └──────────────────┘
```

## Setup & Usage

### Installation
```bash
# Clone or navigate to folder
cd snowflake_mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install langraph trulens-core trulens-snowflake
pip install snowflake-connector-python
pip install mcp fastmcp
```

### Configuration

#### Snowflake Connection
Set environment variables:
```bash
export SNOWFLAKE_USER="your_username"
export SNOWFLAKE_PASSWORD="your_password"
export SNOWFLAKE_ACCOUNT="your_account"
export SNOWFLAKE_WAREHOUSE="your_warehouse"
export SNOWFLAKE_DATABASE="your_database"
export SNOWFLAKE_SCHEMA="your_schema"
```

Or create config file:
```python
SNOWFLAKE_CONFIG = {
    "user": "username",
    "password": "password",
    "account": "account_id",
    "warehouse": "warehouse_name",
    "database": "database_name",
    "schema": "schema_name"
}
```

### Running the Notebook

```bash
# Start Jupyter
jupyter notebook

# Open: build-and-evaluate-langgraph-agents-with-mcp-tools-trulens.ipynb
```

## Files
- `build-and-evaluate-langgraph-agents-with-mcp-tools-trulens.ipynb` - Main implementation notebook

## Notebook Contents

### 1. Project Setup
- Environment configuration
- Dependency installation
- Library imports

### 2. Agent Definition
- LangGraph agent creation
- Tool definition and registration
- State management setup

### 3. MCP Tool Integration
- Loading MCP servers
- Registering MCP tools with agent
- Tool invocation from agent

### 4. Snowflake Integration
- Connection setup
- Query execution
- Data retrieval and processing

### 5. Agent Evaluation with TruLens
- Define evaluation metrics
- Set up feedback mechanisms
- Run agent traces
- Collect evaluation data

### 6. Results Analysis
- Performance metrics
- Tool usage statistics
- Evaluation dashboard
- Optimization recommendations

## Key Concepts

### LangGraph
State-based agent framework:
```python
from langgraph.graph import StateGraph

# Define agent state
class AgentState(TypedDict):
    messages: List[BaseMessage]
    context: dict

# Create graph
graph = StateGraph(AgentState)
```

### MCP Tools
Tools via Model Context Protocol:
```python
# Load from MCP server
mcp_client = MCPClient(server_url)
tools = mcp_client.get_tools()

# Register with agent
graph.add_tool(tools[0])
```

### Snowflake Queries
Execute SQL against data warehouse:
```python
# Execute query
results = snowflake_client.query("""
    SELECT * FROM table
    WHERE condition = true
""")
```

### TruLens Evaluation
Evaluate agent quality:
```python
from trulens_core import Tru, Select
from trulens_core.feedback import Feedback

# Define feedback
feedback = Feedback(evaluation_function)

# Run evaluation
results = tru.run_feedback(
    agent_response,
    feedback_functions=[feedback]
)
```

## Agent Patterns

### Pattern 1: Data Query Agent
```
User Query
    ↓
Agent parses intent
    ↓
Constructs SQL
    ↓
Executes on Snowflake
    ↓
Formats results
    ↓
Returns to user
```

### Pattern 2: Analysis Agent
```
User Request
    ↓
Retrieves data via tools
    ↓
Performs analysis
    ↓
Generates insights
    ↓
Returns with explanation
```

### Pattern 3: Multi-step Workflow
```
Complex Task
    ↓
├─ Step 1: Data collection (MCP tool)
├─ Step 2: Processing (Local)
├─ Step 3: Enrichment (Snowflake)
└─ Step 4: Reporting (Agent synthesis)
    ↓
Final Result
```

## Evaluation Metrics

### Agent Quality
- Accuracy: Does agent answer correctly?
- Completeness: Does agent use all relevant tools?
- Efficiency: Does agent use minimal steps?
- Safety: Does agent avoid harmful actions?

### Tool Usage
- Tool invoke frequency
- Tool success rate
- Tool result quality
- Tool selection appropriateness

### Data Quality
- Data accuracy
- Result consistency
- Edge case handling
- Error recovery

## Example Use Cases

### 1. Business Intelligence Agent
```
"What were sales trends in Q3?"
    ↓
Agent queries Snowflake
    ↓
Analyzes trends
    ↓
Generates report
```

### 2. Data Exploration Agent
```
"Show me unusual patterns in customer data"
    ↓
Loads data via query
    ↓
Applies statistical analysis
    ↓
Highlights anomalies
```

### 3. Reporting Agent
```
"Generate monthly revenue report"
    ↓
Collects data from multiple tables
    ↓
Performs calculations
    ↓
Formats as report
```

## Monitoring & Observability

### Tracing
```python
# Traces capture:
# - Agent decisions
# - Tool calls
# - Tool results
# - Final output
```

### Feedback
```python
# Feedback functions evaluate:
# - Response relevance
# - Factuality
# - Harmfulness
# - Answer quality
```

### Dashboards
TruLens provides:
- Interactive dashboards
- Performance metrics
- Feedback history
- Leaderboards

## Best Practices

1. **Define Clear Metrics**
   - What constitutes success?
   - How to measure quality?
   - What edge cases matter?

2. **Comprehensive Testing**
   - Test with various inputs
   - Include edge cases
   - Evaluate error handling

3. **Iterative Improvement**
   - Review evaluation results
   - Identify failure patterns
   - Refine agent prompts/tools

4. **Performance Monitoring**
   - Track metrics over time
   - Alert on degradation
   - Optimize slow operations

5. **Documentation**
   - Document tool capabilities
   - Record known limitations
   - Keep examples updated

## Troubleshooting

### Snowflake Connection Issues
```python
# Test connection
conn = snowflake.connector.connect(**config)
cursor = conn.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchone())
```

### Tool Invocation Failures
- Verify tool names match MCP definitions
- Check tool argument types
- Review error messages in logs
- Test tools independently

### Evaluation Problems
- Ensure feedback functions are pure
- Check feedback data format
- Verify metric definitions
- Review TruLens documentation

## Performance Optimization

### Query Optimization
- Use appropriate indexes
- Optimize SQL queries
- Cache frequent results
- Use warehouse clustering

### Agent Optimization
- Reduce tool invocation overhead
- Batch operations
- Implement caching
- Optimize state management

## Dependencies
- langgraph
- trulens-core
- trulens-snowflake
- snowflake-connector-python
- mcp
- fastmcp

## Additional Resources
- LangGraph Documentation: https://langchain-ai.github.io/langgraph
- TruLens Documentation: https://www.trulens.org
- Snowflake Documentation: https://docs.snowflake.com
- MCP Specification: https://modelcontextprotocol.io

## Future Enhancements
- [ ] Real-time streaming data
- [ ] Advanced caching
- [ ] Multi-language agents
- [ ] Custom feedback functions
- [ ] A/B testing framework
- [ ] Advanced analytics
- [ ] Production deployment guide

## Contributing
Submit improvements and bug reports via:
1. Detailed issue description
2. Reproducible example
3. Proposed solution (optional)

## Support
For issues or questions:
- Review notebook documentation
- Check TruLens/LangGraph docs
- Test components independently
- Review logs for details
