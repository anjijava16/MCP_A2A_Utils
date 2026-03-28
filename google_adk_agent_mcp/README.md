# Google ADK Currency Agent 💱

## Overview
A Google Agent Development Kit (ADK) based agent specialized in currency conversion and financial exchange operations. This agent uses the A2A (Agent-to-Agent) protocol to provide real-time currency conversion capabilities integrated with MCP tools.

## Features
- **Currency Conversion**: Real-time exchange rates between currencies
- **Cryptocurrency Integration**: Get crypto prices and conversions
- **Multi-currency Support**: Support for 150+ global currencies
- **A2A Protocol**: Agent-to-Agent communication for orchestration
- **MCP Tool Integration**: Leverages MCP servers for data access
- **Context Awareness**: Maintains conversation context for multi-turn interactions
- **Intelligent Routing**: Uses Claude/Gemini to understand user intent

## Architecture
- **Framework**: Google ADK (Agent Development Kit)
- **Protocol**: A2A (Agent-to-Agent with JSON-RPC)
- **Model**: Uses Gemini 2.5 Flash by default
- **Tools**: Loads tools from MCP servers via HTTP/SSE

## Setup & Usage

### Installation
```bash
pip install google-cloud-aiplatform google-adk
```

### Configuration
Set up environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
export MCP_SERVER_URL="http://localhost:7080/sse"
export MODEL_API_KEY="your-api-key"  # For Gemini API
```

Ensure MCP server is running:
```bash
# In another terminal
cd ../mysql_mcp_server
python currency_mcp_server.py
```

### Running the Agent

#### Start A2A Server
```bash
python currency_agent.py

# Server starts on port 10030
# Shows: "🚀 Starting Currency Agent A2A server on port 10030..."
```

#### Test with Client (in another terminal)
```bash
python test_client.py

# Runs test queries and shows responses
```

## Files
- `currency_agent.py` - Main A2A agent server
- `test_client.py` - Test client for agent communication

## Tool Integration

### Loaded Tools
The agent automatically loads tools from MCP server:
- `get_exchange_rate(from_currency, to_currency)` - Exchange rates
- `get_crypto_prices(symbols, vs_currency)` - Cryptocurrency prices
- Any other tools available from MCP server

### MCP Server Connection
```python
MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=os.getenv("MCP_SERVER_URL", "http://localhost:7080/sse")
    )
)
```

## API & Usage

### Starting the Agent
```bash
python currency_agent.py
```

Server logs show:
```
--- 🔧 Loading MCP tools from MCP Server... ---
--- 🤖 Creating ADK Currency Agent... ---
--- 🚀 Starting Currency Agent A2A server on port 10030... ---
```

### Client Usage
```python
from google.adk.a2a.client import A2AClient

client = A2AClient("http://localhost:10030")

# Single turn
response = client.query(
    message="What is 100 USD in GBP?",
    context_id="session-123"
)

# Multi-turn (maintains context)
response2 = client.query(
    message="And how much is Bitcoin?",
    context_id="session-123"
)
```

## Agent Instructions

The agent follows custom system instructions:
```
You are a specialized assistant for currency conversions.
Your sole purpose is to use the 'get_exchange_rate' tool 
to answer questions about currency exchange rates.

If asked about unrelated topics, politely decline.
Focus only on currency-related queries.
```

Can be customized in `currency_agent.py`:
```python
SYSTEM_INSTRUCTION = (
    "Your custom instructions here..."
)
```

## Response Format

### Success Response
```json
{
    "id": "task-id",
    "status": "completed",
    "artifacts": [
        {
            "name": "conversion_result",
            "parts": [
                {
                    "kind": "text",
                    "text": "100 USD equals approximately 74.79 GBP"
                }
            ]
        }
    ],
    "history": [ /* conversation history */ ]
}
```

### Multi-turn Example
```
Turn 1 - User: "How much is 100 USD?"
Agent: "Please specify target currency"

Turn 2 - User: "in GBP"
Agent: "100 USD = 74.79 GBP"
```

## A2A Protocol Details

### Connection Flow
1. Client connects to A2A agent on port 10030
2. Agent loads MCP tools from configured server
3. Client sends query (first turn)
4. Agent processes and returns response with context ID
5. Client uses context ID for follow-up queries
6. Agent maintains conversation history per context

### Message Structure
```python
{
    "message": "What is 100 USD in CAD?",
    "context_id": "session-123"  # For conversation tracking
}
```

## Use Cases
- **Travel Planning**: Convert currency for trips
- **Financial Transactions**: Exchange rate lookups
- **Business Operations**: Multi-currency financial operations
- **Investment Decisions**: Real-time crypto and currency data
- **Personal Finance**: Currency conversion tools
- **API Integration**: Currency conversion as a service

## Integration Points

### With MCP Servers
- Connects to currency MCP server for real data
- Leverages existing tool ecosystem
- SSE transport for HTTP communication

### With Google ADK
- Uses ADK for agent orchestration
- Supports multi-turn conversations
- Integrates with Gemini models
- Provides A2A protocol interface

### With Claude/Other LLMs
- Can be extended to work with other LLMs
- Follows MCP protocol for compatibility
- Demonstrates tool use patterns

## Security Considerations
- **Credential Management**: Uses Google Cloud credentials
- **API Key Security**: Environment-based configuration
- **Tool Access Control**: Only currency-related operations
- **Error Handling**: No credential leaks in responses
- **Context Isolation**: Per-user context management

## Performance
- Fast currency lookup through MCP tools
- Caching of exchange rates
- Efficient SSE communication
- Minimal latency for currency conversions
- Scalable A2A architecture

## Customization

### Change Model
Edit `currency_agent.py`:
```python
root_agent = LlmAgent(
    model="models/gemini-2.0-flash",  # Change model
    ...
)
```

### Add More Tools
Extend MCP server to include:
```python
# In MCP server
@mcp.tool()
def additional_tool():
    pass
```

Agent automatically loads new tools.

### Modify Instructions
```python
SYSTEM_INSTRUCTION = (
    "Your new instructions..."
)
```

## Monitoring & Debugging

### Check Logs
```bash
# Server logs show:
# - Tool loading status
# - Query processing
# - Error details
```

### View Responses
```bash
# Client shows:
# - Full response JSON
# - Conversation history
# - Status and artifacts
```

## Testing & Validation

### Test Client Usage
```bash
python test_client.py

# Runs:
# - Single turn request
# - Query task
# - Multi-turn conversation
```

### Manual Testing
```python
client = A2AClient("http://localhost:10030")
result = client.query("Test query", "test-context")
print(result)
```

## Dependencies
- google-cloud-aiplatform
- google-adk
- mcp
- httpx (for HTTP communication)

## Troubleshooting
- Verify MCP server is running on port 7080
- Check Google credentials configuration
- Ensure currency tools are available
- Review agent logs for errors
- Validate A2A protocol communication

## Future Enhancements
- Support for additional financial tools
- Portfolio tracking
- Historical rate analysis
- Automated alerts
- Real-time market data
- Multiple data sources
- Advanced financial calculations
