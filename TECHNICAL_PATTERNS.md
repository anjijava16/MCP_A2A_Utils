# MCP & A2A Technical Reference & Architecture Patterns

## Part 1: Architecture Diagrams & Visual Patterns

### 1. Complete System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                     END-USER APPLICATIONS                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ Claude       │  │ Web UI       │  │ Custom Applications       │ │
│  │ Desktop      │  │ Dashboard    │  │ (Node, Python, etc.)     │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────────┘ │
└─────────┼──────────────────┼──────────────────────┼─────────────────┘
          │                  │                      │
          │ JSON-RPC 2.0     │ JSON-RPC 2.0         │ JSON-RPC 2.0
          │ (Stdio)          │ (SSE/HTTP)           │ (SSE/HTTP)
          │                  │                      │
┌─────────▼──────────────────▼──────────────────────▼─────────────────┐
│                      MCP SERVER LAYER                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  │
│  │ FastMCP          │  │ Tool Definitions │  │ Resource Mgmt   │  │
│  │ Framework        │  │                  │  │                 │  │
│  │ - Router         │  │ @mcp.tool()      │  │ @mcp.resource() │  │
│  │ - Transport Mgmt │  │ @mcp.prompt()    │  │ @mcp.sampling() │  │
│  │ - Serialization  │  │ @mcp.sampling()  │  │                 │  │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘  │
│                                                                      │
└────────┬──────────────────────────────────────┬──────────────────────┘
         │                                      │
    ┌────▼────────────────────┐    ┌───────────▼──────────────┐
    │  DOMAIN-SPECIFIC        │    │  DATA & INTEGRATION      │
    │  MCP SERVERS (20+)      │    │  LAYER                   │
    │                         │    │                          │
    │  • Currency Exchange    │    │  ┌──────────────────┐    │
    │  • Weather             │    │  │ External APIs    │    │
    │  • Web Search          │    │  │ ────────────────│    │
    │  • YouTube Transcripts │    │  │ • OpenWeather   │    │
    │  • Math Operations     │    │  │ • Tavily Search │    │
    │  • Database Ops        │    │  │ • CoinGecko     │    │
    │  • Neo4j Graph         │    │  │ • YouTube       │    │
    │  • And 13+ more        │    │  │ • ExchangeRate  │    │
    │                         │    │  └──────────────────┘    │
    │                         │    │                          │
    │                         │    │  ┌──────────────────┐    │
    │                         │    │  │ Data Sources     │    │
    │                         │    │  │ ────────────────│    │
    │                         │    │  │ • Neo4j         │    │
    │                         │    │  │ • PostgreSQL    │    │
    │                         │    │  │ • MySQL         │    │
    │                         │    │  │ • Snowflake     │    │
    │                         │    │  │ • BigQuery      │    │
    │                         │    │  │ • S3/Cloud      │    │
    │                         │    │  └──────────────────┘    │
    │                         │    │                          │
    └────┬────────────────────┘    └──────┬───────────────────┘
         │                                │
┌────────▼────────────────────────────────▼──────────────────────────┐
│              A2A ORCHESTRATION LAYER (Optional)                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  A2A Agent Executor (Google ADK)                          │    │
│  │  ┌──────────────────────────────────────────────────────┐ │    │
│  │  │ Root Agent                                          │ │    │
│  │  │  ┌────────────────────────────────────────────────┐ │ │    │
│  │  │  │ Orchestration logic:                          │ │ │    │
│  │  │  │ - Read user input                             │ │ │    │
│  │  │  │ - Choose sub-agents/tools                      │ │ │    │
│  │  │  │ - Execute in parallel/sequential              │ │ │    │
│  │  │  │ - Aggregate results                           │ │ │    │
│  │  │  │ - Format response                             │ │ │    │
│  │  │  │ - Maintain conversation context               │ │ │    │
│  │  │  └────────────────────────────────────────────────┘ │ │    │
│  │  │                                                     │ │    │
│  │  │ ┌─────────────┬──────────────┬──────────────────┐  │ │    │
│  │  │ │ Sub-Agent 1 │ Sub-Agent 2  │ Sub-Agent N...  │  │ │    │
│  │  │ └──────┬──────┴──────┬───────┴────────┬────────┘  │ │    │
│  │  └────────┼─────────────┼────────────────┼───────────┘ │    │
│  │           │             │                │             │    │
│  └───────────┼─────────────┼────────────────┼─────────────┘    │
│              │             │                │                  │
└──────────────┼─────────────┼────────────────┼──────────────────┘
               │             │                │
          Uses MCP tools/resources from layers above
```

### 2. MCP Protocol Message Flow

```
                         MCP CLIENT
                             │
                             │ 1. Initialize
                             │ {"method": "initialize", "params": {...}}
                             │
                    ┌────────▼────────┐
                    │                 │
                    │  MCP SERVER     │
                    │                 │
                    │ ┌─────────────┐ │
                    │ │ Tool List   │ │
                    │ ├─────────────┤ │
                    │ │ Resources   │ │
                    │ ├─────────────┤ │
                    │ │ Prompts     │ │
                    │ └─────────────┘ │
                    └────────┬────────┘
                             │
                             │ 2. Response
                             │ {"result": {"serverInfo": {...}}}
                             │
                             ▼
                    CLIENT SHOWS TOOLS
                             │
                             │ 3. Call Tool
                             │ {"method": "tools/call",
                             │  "params": {
                             │    "name": "get_exchange_rate",
                             │    "arguments": {...}
                             │  }}
                             │
                    ┌────────▼────────┐
                    │  EXECUTE TOOL   │
                    │                 │
                    │ ┌─────────────┐ │
                    │ │ Validate    │ │
                    │ │ Parameters  │ │
                    │ └──────┬──────┘ │
                    │        │       │
                    │ ┌──────▼──────┐ │
                    │ │ Call        │ │
                    │ │ External    │ │
                    │ │ Service     │ │
                    │ └──────┬──────┘ │
                    │        │       │
                    │ ┌──────▼──────┐ │
                    │ │ Format      │ │
                    │ │ Response    │ │
                    │ └─────────────┘ │
                    └────────┬────────┘
                             │
                             │ 4. Result
                             │ {"type": "text", "text": "..."}
                             │
                             ▼
                     DISPLAY TO USER
```

### 3. Neo4j Lexical Graph Processing Pipeline

```
INPUT PDF FILES
    │
    │ ┌─────────────────────────────┐
    ├─► Stage 1: Pre-flight Check    │
    │   ├─ Count files              │
    │   ├─ Count pages (est.)        │
    │   ├─ Estimate processing time │
    │   └─ Request confirmation      │
    │   └─ Result: Job ID created    │
    └─────────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │ Stage 2: Parse & Extract          │
    │ (Parallel processing)              │
    │                                    │
    │ For each PDF:                      │
    │  ├─ docling parser ──┐           │
    │  ├─ pymupdf parser   ├─ Extract: │
    │  ├─ text_only        │ ├─ Text   │
    │  └─ vlm_blocks ──────┘ ├─ Tables │
    │                        ├─ Images │
    │                        ├─ Layout │
    │                        └─ Metadata│
    │                                    │
    │  Result: Structured DOM           │
    └────┬──────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │ Stage 3: Neo4j Graph Creation      │
    │                                    │
    │ Document                           │
    │   ├─ Page 1 ──► Element 1.1       │
    │   │         ├─► Element 1.2       │
    │   │         └─ NEXT ──► Element 1.3
    │   ├─ Page 2 ──► Element 2.1       │
    │   │         └─ NEXT ──► Element 2.2
    │   └─ (...)                         │
    │                                    │
    │ Relationships:                      │
    │ - Document --[HAS_PAGE]--> Page  │
    │ - Page --[HAS_ELEMENT]--> Element│
    │ - Element --[NEXT]--> Element    │
    │ - Element --[CONTAINS_IMAGE]---> │
    │                                    │
    │ Result: Graph in Neo4j             │
    └────┬──────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │ Stage 4: Chunking                  │
    │                                    │
    │ Strategies:                         │
    │  ├─ token_window (sliding window) │
    │  ├─ structured (preserve elements)│
    │  ├─ by_section (hierarchical)     │
    │  └─ by_page (page-aligned)        │
    │                                    │
    │ Create Chunk nodes and            │
    │ relationships:                     │
    │ - Document --[HAS_CHUNK]--> Chunk │
    │ - Chunk --[CONTAINS]--> Elements  │
    │                                    │
    │ Metadata:                          │
    │  ├─ token count                   │
    │  ├─ section level                 │
    │  ├─ page number                   │
    │  └─ active/inactive flag          │
    └────┬──────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │ Stage 5: Enrichment (Optional)     │
    │                                    │
    │ ├─ Section Hierarchy               │
    │ │  Generate document outline       │
    │ │  Assign hierarchy levels         │
    │ │                                  │
    │ ├─ Descriptions                    │
    │ │  Use VLM to describe chunks      │
    │ │  Create metadata layer           │
    │ │                                  │
    │ ├─ Embeddings                      │
    │ │  Generate vector embeddings      │
    │ │  Create HNSW index               │
    │ │                                  │
    │ └─ Full-Text Index                 │
    │    Create FTS for keyword search   │
    │                                    │
    │ Result: Enhanced graph             │
    └────┬──────────────────────────────┘
         │
    ┌────▼──────────────────────────────┐
    │ Stage 6: Verification              │
    │                                    │
    │ ├─ Check orphan nodes              │
    │ ├─ Validate NEXT chains            │
    │ ├─ Verify relationships            │
    │ ├─ Collect statistics              │
    │ └─ Reconstruct document            │
    │    (Output as .md for comparison)  │
    │                                    │
    │ Result: Report & validation        │
    └────┬──────────────────────────────┘
         │
         ▼
    OUTPUT RESULTS
    ├─ Job completion status
    ├─ Processing logs
    ├─ Reconstruction files
    ├─ Error reports
    └─ Graph statistics
```

### 4. A2A Multi-Agent Workflow

```
USER REQUEST: "Plan a 5-day trip to Japan for $2000"
    │
    ▼
┌─────────────────────────────────────┐
│ A2A ROOT AGENT                      │
│ • Parses user intent                │
│ • Breaks down into subtasks         │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┬──────────┬──────────┐
        │             │          │          │
        ▼             ▼          ▼          ▼
    ┌────────┐  ┌─────────┐ ┌──────┐  ┌──────┐
    │Currency│  │ Travel  │ │Weather│ │Budget│
    │Agent   │  │ Search  │ │Agent  │ │Agent │
    └────┬───┘  └────┬────┘ └───┬──┘  └───┬──┘
         │           │          │         │
         │ Calls:    │ Calls:    │ Calls:  │ Calls:
         │ Exchange  │ Web       │ Weather │ Calc
         │ Rate API  │ Search    │ API     │ Budget
         │           │          │         │
         ▼           ▼          ▼         ▼
    ┌────────┐  ┌─────────┐ ┌──────┐  ┌──────┐
    │$2000   │  │Top      │ │Spring│ │¥    │
    │=       │  │Flights: │ │Mild  │ │290k  │
    │¥290k   │  │- Tokyo  │ │Rainy │ │ -    │
    │        │  │- Kyoto  │ │      │ │Hotels│
    │        │  │         │ │      │ │&Food │
    │        │  │Deals:   │ │      │ │      │
    │        │  │Save 20% │ │      │ │      │
    │        │  │w/ code  │ │      │ │      │
    └────────┘  └─────────┘ └──────┘  └──────┘
         │           │          │         │
         └───────────┼──────────┼─────────┘
                     │
                ┌────▼──────────────┐
                │ AGGREGATOR AGENT   │
                │ Combines results   │
                │ Formats response   │
                │ Creates itinerary  │
                └────┬───────────────┘
                     │
                     ▼
        RESPONSE TO USER:
        "5-Day Japan Itinerary for ¥290k:
         Day 1: Tokyo (Stay near Shinjuku)
         Day 2-3: Kyoto (Traditional temples)
         Day 4-5: Osaka (Food & culture)
         
         Estimated Cost Breakdown:
         - Flights: ¥120k (20% discount)
         - Hotels: ¥100k (5 nights)
         - Food: ¥50k
         - Transport: ¥20k
         
         Best Season: April (Cherry blossoms)"
```

## Part 2: Code Patterns & Examples

### Pattern 1: Building a Simple MCP Server

```python
"""
Basic MCP server template demonstrating core concepts.
"""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError
from pydantic import Field
import asyncio
import httpx

# Initialize FastMCP server
mcp = FastMCP("SampleService", port=8080)

# ============================================
# SECTION 1: Tool Definitions
# ============================================

@mcp.tool()
async def fetch_data(
    url: str = Field(..., description="URL to fetch"),
    timeout: int = Field(10, description="Request timeout in seconds")
) -> dict:
    """
    Fetch data from a URL.
    
    Returns:
    - status_code: HTTP status code
    - content_length: Size of response
    - preview: First 200 characters of content
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=timeout)
            
            return {
                "status_code": response.status_code,
                "content_length": len(response.content),
                "preview": response.text[:200],
                "headers": dict(response.headers)
            }
    except httpx.TimeoutException:
        raise ToolError(f"Request timed out after {timeout} seconds")
    except Exception as e:
        raise ToolError(f"Failed to fetch URL: {str(e)}")

# ============================================
# SECTION 2: Resource Serving
# ============================================

@mcp.resource("docs://api/{endpoint}")
def get_api_docs(endpoint: str) -> str:
    """
    Serve API documentation for endpoints.
    
    Valid endpoints: users, products, orders
    """
    docs = {
        "users": "GET /users - List all users\nPOST /users - Create user",
        "products": "GET /products - List products\nPOST /products - Add product",
        "orders": "GET /orders - List orders\nPOST /orders - Place order"
    }
    
    if endpoint not in docs:
        return f"Unknown endpoint: {endpoint}\nValid: {', '.join(docs.keys())}"
    
    return docs[endpoint]

# ============================================
# SECTION 3: Prompt Templates
# ============================================

@mcp.prompt()
def generate_request_prompt(endpoint: str, method: str = "GET") -> str:
    """Generate a prompt for API requests."""
    return f"""
    Make a {method} request to the {endpoint} endpoint.
    Include proper error handling and validation.
    Return results in JSON format.
    """

# ============================================
# SECTION 4: Server Startup
# ============================================

if __name__ == "__main__":
    import logging
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run server
    print("🚀 Starting MCP Server on port 8080...")
    print("📡 Transport: SSE")
    print("🔗 Available at: http://localhost:8080/sse")
    
    # Choose transport
    mcp.run(transport="sse")  # or "stdio" for stdio transport
```

### Pattern 2: A2A Agent Implementation

```python
"""
A2A Agent implementation showing orchestration patterns.
"""

from google.adk import agent as agent_lib
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.a2a.client import A2AClient
from typing import Optional
import asyncio
import json

# ============================================
# SECTION 1: Define Agent Tools
# ============================================

class ToolSet:
    """Aggregates tools from multiple MCP servers."""
    
    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
        """Get exchange rate between currencies."""
        # In practice, calls actual MCP server
        rates = {"USD_GBP": 0.7479, "USD_JPY": 149.5, "USD_EUR": 0.92}
        key = f"{from_currency}_{to_currency}"
        return {
            "from": from_currency,
            "to": to_currency,
            "rate": rates.get(key, 1.0)
        }
    
    @staticmethod
    def get_crypto_price(symbol: str) -> dict:
        """Get crypto price."""
        prices = {"bitcoin": 65000, "ethereum": 2800, "cardano": 0.98}
        return {
            "symbol": symbol,
            "price_usd": prices.get(symbol.lower(), 0)
        }

# ============================================
# SECTION 2: Create Root Agent
# ============================================

def create_financial_agent():
    """Create an agent for financial queries."""
    
    root_agent = agent_lib.Agent(
        name="FinancialAdvisor",
        
        instructions="""
        You are a helpful financial advisor. Help users with:
        - Currency conversions
        - Cryptocurrency information
        - Budget calculations
        
        Use available tools to provide accurate, real-time information.
        Always explain your calculations.
        """,
        
        tools=[
            {
                "name": "get_exchange_rate",
                "description": "Get current exchange rate between two currencies",
                "function": ToolSet.get_exchange_rate,
                "parameters": {
                    "from_currency": {"type": "string", "description": "Source currency code"},
                    "to_currency": {"type": "string", "description": "Target currency code"}
                }
            },
            {
                "name": "get_crypto_price",
                "description": "Get current price of cryptocurrency",
                "function": ToolSet.get_crypto_price,
                "parameters": {
                    "symbol": {"type": "string", "description": "Crypto symbol (bitcoin, ethereum, etc.)"}
                }
            }
        ],
        
        model="models/gemini-2.0-flash"
    )
    
    return root_agent

# ============================================
# SECTION 3: Convert to A2A & Run
# ============================================

async def run_server():
    """Start A2A server."""
    
    agent = create_financial_agent()
    
    # Convert to A2A
    app = to_a2a(agent, port=10030)
    
    print("🚀 A2A Agent Server Started")
    print("📡 Listening on http://localhost:10030")
    print("✅ Ready to accept connections")
    
    # Run indefinitely
    await asyncio.Event().wait()

# ============================================
# SECTION 4: Client for Testing
# ============================================

async def run_client():
    """Test client that queries the agent."""
    
    # Wait for server to start
    await asyncio.sleep(2)
    
    client = A2AClient("http://localhost:10030")
    context_id = "test-session-123"
    
    # Test 1: Simple query
    print("\n=== Test 1: Exchange Rate ===")
    response = await client.query(
        "What's 100 USD in GBP?",
        context_id
    )
    print(response["artifacts"][0]["parts"][0]["text"])
    
    # Test 2: Follow-up (maintains context)
    print("\n=== Test 2: Follow-up ===")
    response = await client.query(
        "And how much is Bitcoin?",
        context_id
    )
    print(response["artifacts"][0]["parts"][0]["text"])
    
    # Test 3: Complex query
    print("\n=== Test 3: Complex Query ===")
    response = await client.query(
        "If Bitcoin is $65k and I have $5000 USD, how much Bitcoin can I buy in GBP terms?",
        context_id
    )
    print(response["artifacts"][0]["parts"][0]["text"])

# ============================================
# SECTION 5: Main Entry Point
# ============================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        # Run client: python script.py client
        asyncio.run(run_client())
    else:
        # Run server: python script.py
        asyncio.run(run_server())
```

### Pattern 3: Neo4j Integration

```python
"""
Neo4j database integration pattern with async driver.
"""

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ServerError
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError
from pydantic import Field
import asyncio
from typing import Optional, List, Dict

mcp = FastMCP("GraphService", port=8003)

# ============================================
# SECTION 1: Database Connection Management
# ============================================

class GraphDatabase:
    """Manages Neo4j connections and queries."""
    
    def __init__(self, uri: str, username: str, password: str):
        self.driver = None
        self.uri = uri
        self.username = username
        self.password = password
    
    async def connect(self):
        """Establish database connection."""
        self.driver = AsyncGraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
            max_connection_pool_size=50,
            connection_timeout=15.0
        )
        
        # Test connection
        async with self.driver.session() as session:
            await session.run("RETURN 1")
        
        print("✅ Connected to Neo4j")
    
    async def disconnect(self):
        """Close database connection."""
        if self.driver:
            await self.driver.close()
    
    async def query(self, cypher: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute a Cypher query."""
        try:
            async with self.driver.session() as session:
                result = await session.run(cypher, params or {})
                records = await result.all()
                return [dict(record) for record in records]
        except ServerError as e:
            raise ToolError(f"Database error: {str(e)}")

# ============================================
# SECTION 2: Tool Definitions
# ============================================

db = None  # Global database instance

@mcp.tool()
async def create_document(
    doc_id: str = Field(..., description="Unique document ID"),
    title: str = Field(..., description="Document title"),
    content: str = Field(..., description="Document content")
) -> dict:
    """Create a document node in the graph."""
    
    cypher = """
    CREATE (d:Document {
        id: $doc_id,
        title: $title,
        content: $content,
        created_at: timestamp()
    })
    RETURN d
    """
    
    result = await db.query(cypher, {
        "doc_id": doc_id,
        "title": title,
        "content": content
    })
    
    return {
        "status": "success",
        "document_id": doc_id,
        "message": f"Created document: {title}"
    }

@mcp.tool()
async def add_chunk(
    doc_id: str = Field(..., description="Parent document ID"),
    chunk_text: str = Field(..., description="Chunk content"),
    order: int = Field(..., description="Chunk order in document")
) -> dict:
    """Add a chunk node linked to document."""
    
    cypher = """
    MATCH (d:Document {id: $doc_id})
    CREATE (c:Chunk {
        text: $chunk_text,
        order: $order,
        created_at: timestamp()
    })
    CREATE (d)-[:HAS_CHUNK]->(c)
    RETURN c
    """
    
    result = await db.query(cypher, {
        "doc_id": doc_id,
        "chunk_text": chunk_text,
        "order": order
    })
    
    return {
        "status": "success",
        "chunk_order": order
    }

@mcp.tool()
async def search_documents(
    query: str = Field(..., description="Search query"),
    limit: int = Field(10, description="Max results")
) -> List[Dict]:
    """Full-text search documents."""
    
    cypher = """
    MATCH (d:Document)
    WHERE d.title CONTAINS $query OR d.content CONTAINS $query
    RETURN d.id as id, d.title as title, d.content as content
    LIMIT $limit
    """
    
    return await db.query(cypher, {"query": query, "limit": limit})

@mcp.tool()
async def get_document_chunks(
    doc_id: str = Field(..., description="Document ID")
) -> List[Dict]:
    """Retrieve all chunks for a document."""
    
    cypher = """
    MATCH (d:Document {id: $doc_id})-[:HAS_CHUNK]->(c:Chunk)
    RETURN c.text as text, c.order as order
    ORDER BY c.order
    """
    
    return await db.query(cypher, {"doc_id": doc_id})

# ============================================
# SECTION 3: Server Startup & Shutdown
# ============================================

async def main():
    """Main server entry point."""
    
    # Initialize database
    global db
    db = GraphDatabase(
        uri="neo4j://localhost:7687",
        username="neo4j",
        password="password"
    )
    
    await db.connect()
    
    print("🚀 Graph Service MCP Server Starting")
    print("📡 Available at http://localhost:8003/sse")
    
    try:
        # Run MCP server
        await mcp.run_sse_async(host="0.0.0.0", port=8003)
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 4: Error Handling & Resilience

```python
"""
Advanced error handling and resilience patterns.
"""

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolError
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

mcp = FastMCP("ResilientService", port=8004)
logger = logging.getLogger(__name__)

# ============================================
# SECTION 1: Retry Patterns
# ============================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_external_api_with_retry(url: str) -> dict:
    """Call external API with automatic retry."""
    # Will retry up to 3 times with exponential backoff
    return await fetch_with_timeout(url, timeout=5)

# ============================================
# SECTION 2: Graceful Degradation
# ============================================

@mcp.tool()
async def get_data_with_fallback(source: str):
    """Try primary source, fall back to secondary."""
    
    try:
        # Try primary
        return await fetch_from_primary(source)
    
    except ConnectionError:
        logger.warning(f"Primary source down: {source}")
        try:
            # Try secondary
            return await fetch_from_secondary(source)
        except ConnectionError:
            logger.warning(f"Secondary source also down")
            # Try cache
            cached = get_cached_data(source)
            if cached:
                return {"data": cached, "from_cache": True}
            
            raise ToolError("All sources unavailable")

# ============================================
# SECTION 3: Circuit Breaker Pattern
# ============================================

class CircuitBreaker:
    """Prevents cascading failures."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func, *args, **kwargs):
        """Call function with circuit breaker protection."""
        
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise ToolError("Service unavailable (circuit open)")
        
        try:
            result = await func(*args, **kwargs)
            
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            
            return result
        
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            
            if self.failures >= self.failure_threshold:
                self.state = "open"
            
            raise

# ============================================
# SECTION 4: Structured Logging
# ============================================

@mcp.tool()
async def operation_with_logging(user_id: str, amount: float):
    """Operation with comprehensive logging."""
    
    request_id = uuid4().hex
    
    try:
        logger.info(
            "Operation started",
            extra={
                "request_id": request_id,
                "user_id": user_id,
                "amount": amount
            }
        )
        
        result = await perform_operation(user_id, amount)
        
        logger.info(
            "Operation succeeded",
            extra={
                "request_id": request_id,
                "user_id": user_id,
                "result": result
            }
        )
        
        return result
    
    except ValueError as e:
        logger.warning(
            "Invalid input",
            extra={
                "request_id": request_id,
                "error": str(e)
            }
        )
        raise ToolError(f"Invalid input: {e}")
    
    except Exception as e:
        logger.error(
            "Operation failed",
            extra={
                "request_id": request_id,
                "error": str(e),
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        raise ToolError("Operation failed")
```

## Part 3: Testing Patterns

### Testing MCP Servers

```python
"""
Testing patterns for MCP servers.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from mcp.server.fastmcp import FastMCP

# ============================================
# Unit Tests
# ============================================

@pytest.fixture
async def mcp_server():
    """Create MCP server for testing."""
    server = FastMCP("TestServer")
    
    @server.tool()
    async def test_tool(param: str) -> str:
        return f"Result: {param}"
    
    return server

@pytest.mark.asyncio
async def test_tool_invocation(mcp_server):
    """Test that tools can be invoked correctly."""
    
    result = await mcp_server._tools["test_tool"].fn(param="test")
    
    assert result == "Result: test"

@pytest.mark.asyncio
async def test_tool_error_handling(mcp_server):
    """Test error handling in tools."""
    
    @pytest.fixture
    def error_server():
        server = FastMCP("ErrorServer")
        
        @server.tool()
        async def failing_tool():
            raise ValueError("Test error")
        
        return server
    
    with pytest.raises(ValueError):
        await error_server._tools["failing_tool"].fn()

# ============================================
# Integration Tests
# ============================================

@pytest.mark.asyncio
async def test_server_startup():
    """Test server initialization."""
    
    server = FastMCP("IntegrationTest")
    
    @server.tool()
    async def dummy():
        return "ok"
    
    # Verify server has tools
    assert "dummy" in server._tools

@pytest.mark.asyncio
async def test_multiple_tool_calls():
    """Test sequential tool invocations."""
    
    server = FastMCP("MultiTest")
    call_order = []
    
    @server.tool()
    async def tool1():
        call_order.append(1)
        return "tool1"
    
    @server.tool()
    async def tool2():
        call_order.append(2)
        return "tool2"
    
    await server._tools["tool1"].fn()
    await server._tools["tool2"].fn()
    
    assert call_order == [1, 2]

# ============================================
# Mock Tests
# ============================================

@pytest.mark.asyncio
async def test_with_mocked_external_call():
    """Test tool that calls external services."""
    
    server = FastMCP("MockTest")
    
    @server.tool()
    async def fetch_data(url: str):
        # In real code, calls actual API
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    
    # Mock the HTTP call
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"data": "mocked"})
        mock_get.return_value = mock_response
        
        result = await server._tools["fetch_data"].fn(url="http://test.com")
        
        assert result == {"data": "mocked"}
```

---

## Conclusion

This reference guide provides:

1. **Visual Architecture Diagrams** - Understand system components and data flow
2. **Code Patterns** - Proven implementations for common scenarios
3. **Best Practices** - Patterns for resilience, testing, and monitoring
4. **Real-World Examples** - Directly applicable code samples

Use these patterns as templates for building your own MCP servers and A2A agents!
