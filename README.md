# MCP_understanding



# MCP Servers and A2A Utilities - Comprehensive Deep Dive

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Project Architecture Overview](#project-architecture-overview)
3. [Model Context Protocol (MCP) - Explained](#model-context-protocol-mcp---explained)
4. [Core Components & Implementations](#core-components--implementations)
5. [Technology Stack](#technology-stack)
6. [MCP Server Implementations](#mcp-server-implementations)
7. [A2A (Agent-to-Agent) Integration](#a2a-agent-to-agent-integration)
8. [Advanced Implementations](#advanced-implementations)
9. [Deployment & Configuration](#deployment--configuration)
10. [Use Cases & Examples](#use-cases--examples)
11. [Best Practices & Lessons Learned](#best-practices--lessons-learned)

---

## Executive Summary

This project is a **comprehensive exploration and implementation suite for the Model Context Protocol (MCP)** combined with **Google's Agent-to-Agent (A2A) framework**. It demonstrates how to build, orchestrate, and deploy AI agents with multiple specialized tools and services.

**Key Highlights:**
- 20+ MCP server implementations (FastMCP, various domain-specific servers)
- Full integration with Google ADK (Agent Development Kit)
- A2A protocol support for complex agent orchestration
- Real-world examples: Currency conversion, Weather, YouTube transcript extraction, Neo4j GraphRAG
- SSE (Server-Sent Events) and Stdio transport protocols
- Multi-agent coordination patterns
- Production-ready patterns with error handling and observability

---

## Project Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Applications                          │
│           (Claude Desktop, Custom Clients, UIs)                │
└────────────────────────────────────────────────────────────────┐
                            │
                ┌───────────┴───────────┐
                │                       │
         ┌──────▼──────┐        ┌──────▼──────┐
         │ MCP Servers │        │ A2A Agents  │
         │   (SPIs)    │        │  (Agentic)  │
         └──────┬──────┘        └──────┬──────┘
                │                      │
         ┌──────▼──────────────────────▼──────┐
         │      Transport Layer               │
         │  (Stdio, SSE, JSON-RPC 2.0)       │
         └──────┬──────────────────────┬──────┘
                │                      │
    ┌───────────▼──────┐   ┌──────────▼──────────┐
    │  External APIs   │   │  Data Sources       │
    │  - Web Search    │   │  - Neo4j Graph DB  │
    │  - Exchange Rates│   │  - BigQuery        │
    │  - Crypto Prices │   │  - PostgreSQL      │
    │  - Weather       │   │  - MySQL           │
    │  - YouTube       │   │  - Snowflake       │
    └──────────────────┘   └────────────────────┘
```

### Project Structure

```
MCP_servers_and_a2a_utils/
├── Core Entry Points
│   ├── agent.py                          # Multi-server MCP agent orchestration
│   ├── call_tool.py                      # Tool invocation wrapper
│   ├── list_tools.py                     # Tool discovery & introspection
│   └── debug_tools.py                    # Debugging utilities
│
├── MCP Servers (20+ implementations)
│   ├── mcp_weather_server/               # FastMCP weather service
│   ├── mcp_tavily_search/                # Web search integration
│   ├── mcp_math_server/                  # Mathematical operations
│   ├── mcp_youtube_extraction_server/    # YouTube transcript extraction
│   ├── mcp_database_server/              # Database operations
│   ├── mysql_mcp_server/                 # MySQL-specific server
│   ├── mcp_server_aws/                   # AWS integration
│   ├── mcp_snowflake/                    # Snowflake data warehouse
│   ├── neo4j-mcp-workspace-template/     # Graph database (5 specialized servers)
│   └── [15+ other specialized servers]
│
├── A2A Integration Layer
│   ├── a2a_src/                          # A2A protocol implementation
│   ├── agno_agentic_mcp/                 # Agno + Agentic framework
│   ├── google_adk_agent_mcp/             # Google ADK agents
│   │   ├── currency_agent.py             # Live A2A agent example
│   │   └── test_client.py                # A2A client test harness
│   └── [Multiple agentic frameworks]
│
├── Framework & Adapter Layer
│   ├── mcp_adapaters_clients/            # MCP client adapters
│   ├── fastmcp_fastapi/                  # FastMCP + FastAPI bridge
│   ├── langchain_mcp_server_client/      # LangChain integration
│   └── firebase/storage/remote/          # Remote storage backends
│
├── Documentation & Configuration
│   ├── README.md                         # Project overview
│   ├── MCP_Readme.md                     # MCP-specific details
│   ├── MCP_A2A_SSE_Studio.md             # SSE & A2A protocols
│   ├── MCP_INspect_TEST.md               # MCP Inspector usage
│   ├── claude_config.json                # Claude Desktop config
│   └── copilot-instructions.md           # Copilot integration
│
└── Configuration & Environment
    ├── pyproject.toml                    # Python project definition
    ├── requirements.txt                  # Core dependencies
    └── [Virtual environment configs]
```

---

## Model Context Protocol (MCP) - Explained

### What is MCP?

The **Model Context Protocol** is a standardized, open protocol for connecting AI models (like Claude) with external tools, data sources, and context providers. It enables models to:
- **Access tools** to perform actions
- **Read resources** (files, documents, data)
- **Invoke prompts** for structured interactions
- **Request sampling** (experimental features)

### MCP Architecture

```
┌─────────────────┐                    ┌──────────────────┐
│   MCP Client    │◄──JSON-RPC 2.0─────► MCP Server       │
│  (e.g., Claude) │   (Stdio/SSE)       (Tool Provider)   │
└─────────────────┘                    └──────────────────┘
        │
    Uses:
        │
    ├─ Tools: Execute tasks
    ├─ Resources: Access data
    ├─ Prompts: Structured requests
    └─ Sampling: LLM interactions
```

### Key Concepts

#### **1. Tools**
Server-exposed functions that clients can call. Examples:
```python
@mcp.tool()
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Get current exchange rate between two currencies."""
    # Implementation
    return rate_data
```

**Characteristics:**
- Strongly typed with Pydantic models
- Include descriptions & annotations
- Support async operations
- Return structured data

#### **2. Resources**
Data sources that clients can read. Examples:
```python
@mcp.resource("papers://folders")
def get_available_folders() -> str:
    """List available paper folders."""
    return folder_listing
```

**Types:**
- Text-based (documents, logs)
- Binary (images, PDFs)
- Hierarchical (folder structures)

#### **3. Prompts**
Reusable prompt templates with parameters:
```python
@mcp.prompt()
def generate_search_prompt(topic: str, num_papers: int = 5) -> str:
    """Generate a prompt for finding academic papers."""
    return f"Find {num_papers} papers about {topic}..."
```

#### **4. Tool Annotations**
Metadata that helps clients understand tool behavior:
```python
annotations=ToolAnnotations(
    title="Chunk Lexical Graph",
    readOnlyHint=False,           # Can modify data
    destructiveHint=False,        # Won't delete critical data
    idempotentHint=False,         # May have side effects
    openWorldHint=False,          # Operates on closed knowledge
)
```

### Transport Protocols

#### **Stdio Transport**
- **Uses:** Unix pipes / stdin/stdout
- **Best for:** Desktop applications, claude-desktop-config.json
- **Characteristics:** Synchronous request-response, low latency
- **Setup:**
  ```json
  {
    "command": "python",
    "args": ["server.py"],
    "transport": "stdio"
  }
  ```

#### **SSE Transport (Server-Sent Events)**
- **Uses:** HTTP with EventStream
- **Best for:** Web services, microservices, cloud deployment
- **Characteristics:** Asynchronous, bidirectional streaming
- **Example:**
  ```python
  mcp = FastMCP("currency", port=7080)
  await mcp.run_sse_async(host="0.0.0.0", port=7080)
  ```

### MCP Protocol Flow

```
Client                                  Server
  │                                       │
  ├─ Initialize                          │
  │  {"jsonrpc": "2.0", "id": 1,        │
  │   "method": "initialize", ...}──────► 
  │                                    ┌─┤
  │                          ◄────────┤─ {"result": {"serverInfo": ...}}
  │                                    └─┤
  │
  ├─ List Tools                          │
  │  {"jsonrpc": "2.0", "id": 2,        │
  │   "method": "tools/list"}───────────►
  │                           ┌──────────┤
  │                  ◄────────┤ {"tools": [...]}
  │                           └──────────┤
  │
  ├─ Call Tool                           │
  │  {"jsonrpc": "2.0", "id": 3,        │
  │   "method": "tools/call",           │
  │   "params": {...}}─────────────────►
  │                     ┌────────────────┤
  │             ◄───────┤ {"result": "..."}
  │                     └────────────────┤
```

### Tool Result Types

MCP tools return structured results:

```python
# Success Result
{
    "type": "text",
    "text": "The exchange rate is 1.3794 CAD per USD"
}

# Tool Error
{
    "type": "text",
    "text": "Error: Invalid currency code",
    "isError": true
}

# Multi-part Result (images, formatted content)
{
    "type": "image",
    "data": "base64-encoded-image-data",
    "mimeType": "image/png"
}
```

---

## Core Components & Implementations

### 1. **FastMCP Framework**

FastMCP is the primary framework used in this project for building MCP servers.

**Advantages:**
- Minimal boilerplate
- Automatic tool registration
- Built-in async support
- SSE and Stdio transports included
- Pydantic integration for type safety

**Basic Structure:**
```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("MyServer", port=8000)

# Register tools
@mcp.tool()
async def my_tool(param: str) -> str:
    return f"Result: {param}"

# Register resources
@mcp.resource("docs://{path}")
def get_docs(path: str) -> str:
    return read_file(path)

# Run server
if __name__ == "__main__":
    mcp.run(transport='sse')  # or 'stdio'
```

### 2. **LangChain MCP Adapters**

Bridges MCP servers with LangChain agents:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async with MultiServerMCPClient({
    "tavily": {
        "command": "python",
        "args": ["servers/tavily.py"],
        "transport": "stdio"
    }
}) as client:
    tools = client.get_tools()
    agent = create_react_agent(model, tools)
    response = await agent.ainvoke({"messages": [...]})
```

### 3. **MCP Inspector**

Browser-based tool for testing and debugging MCP servers:

```bash
npx @modelcontextprotocol/inspector

# Starts on http://127.0.0.1:6274
# Test tools, resources, and prompts in real-time
```

**Features:**
- Visual tool/resource explorer
- Real-time tool invocation
- Parameter validation
- Response inspection
- Error diagnosis

---

## Technology Stack

### Core Dependencies

```
FastMCP 2.14.1              # MCP server framework
mcp                         # Official MCP protocol library
httpx                       # Async HTTP client
pydantic                    # Type validation & schemas

Optional Integrations:
- langchain-core            # LangChain framework
- langchain-mcp-adapters    # MCP-LangChain bridge
- langchain-openai          # OpenAI integration
- langgraph                  # Agent orchestration
- google.adk                 # Google Agent Development Kit
- neo4j                      # Graph database driver
- pymupdf                    # PDF processing
- docling                    # Document parsing
- pandas                     # Data manipulation
- requests                   # HTTP library
- beautifulsoup4             # HTML parsing
```

### Python Ecosystem Integration

```
Python 3.11+
├─ Async/Await (asyncio, aiohttp)
├─ Type Hints (typing, pydantic)
├─ JSON-RPC 2.0 Protocol
├─ Environment Management (.zprofile, os.environ)
└─ Package Management (pip, uv)
```

---

## MCP Server Implementations

### 1. **Currency & Exchange Server**

**Location:** `google_adk_agent_mcp/`

```python
# Server: Provides exchange rate and crypto price tools
@mcp.tool()
def get_exchange_rate(currency_from: str, currency_to: str) -> dict:
    """Get real-time exchange rates via ExchangeRate-API."""
    
@mcp.tool()
def get_crypto_prices(symbols: str, vs_currency: str) -> dict:
    """Get cryptocurrency prices via CoinGecko API."""
```

**Usage Pattern:**
```
User Query: "How much is 100 USD in GBP?"
         ↓
Agent calls get_exchange_rate("USD", "GBP")
         ↓
Returns: {"rate": 0.7479, "conversion": 74.79}
         ↓
Agent formats response: "100 USD = 74.79 GBP"
```

### 2. **Weather Server**

**Location:** `mcp_weather_server/`

```python
@mcp.tool()
async def get_weather(city: str, country_code: str = "") -> dict:
    """Get current weather for any city using OpenWeatherMap API."""
    # Returns: temperature, conditions, humidity, wind speed, etc.
```

### 3. **Web Search Server**

**Location:** `mcp_tavily_search/`

```python
@mcp.tool()
async def tavily_search(query: str, max_results: int = 5) -> list:
    """Search the web using Tavily AI search engine."""
    # Returns structured search results with summaries
```

### 4. **YouTube Transcript Extractor**

**Location:** `mcp_youtube_extraction_server/`

```python
@mcp.tool()
def extract_transcript(video_url: str) -> str:
    """Extract and return transcript from YouTube videos."""
    # Uses youtube-transcript-api
    # Returns full transcript with timestamps
```

### 5. **Mathematical Operations Server**

**Location:** `mcp_math_server/`

```python
@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate mathematical expressions safely."""
    # Supports complex math with numexpr library
```

### 6. **Neo4j Graph Database Servers**

**Location:** `neo4j-mcp-workspace-template/`

Five specialized MCP servers for graph knowledge management:

#### **A. Data Modeling (`neo4j-data-modeling`)**
- Define graph schemas
- Create ontologies
- Manage entity types and relationships

#### **B. Ingest (`neo4j-ingest`)**
- Load data from files (CSV, JSON)
- Parse structured/unstructured documents
- Create nodes and relationships

#### **C. Lexical Graph (`neo4j-lexical-graph`)**
**Most Complex Implementation in this project**

```python
@mcp.tool()
async def create_lexical_graph(path: str) -> str:
    """
    Create a complete lexical graph from PDFs:
    1. Parse PDFs (docling, pymupdf)
    2. Extract elements (tables, images, text)
    3. Create nodes in Neo4j
    4. Build reading order chains
    """
    
    # Strategies: token_window, structured, by_section, by_page
    # Supports parallel processing via ProcessPoolExecutor
    # Includes VLM-based element description generation
```

**Detailed Tool Set:**
1. **`create_lexical_graph`** - Ingest PDFs as structured graphs
2. **`check_processing_status`** - Monitor background jobs
3. **`cancel_processing`** - Stop running jobs
4. **`chunk_lexical_graph`** - Split documents into semantic chunks
5. **`assign_section_hierarchy`** - Create document outline structure
6. **`generate_chunk_descriptions`** - Use LLMs to describe chunks
7. **`embed_chunks`** - Generate and store embeddings
8. **`verify_lexical_graph`** - Validate graph integrity
9. **`reconstruct_document`** - Export graph back to Markdown

#### **D. Entity Graph (`neo4j-entity-graph`)**
- Extract named entities
- Create entity relationships
- Build semantic networks

#### **E. GraphRAG (`neo4j-graphrag`)**
- Implement RAG (Retrieval Augmented Generation)
- Query graph for context
- Generate AI responses from graph data

### 7. **Database Servers**

#### **MySQL Server**
```python
@mcp.tool()
async def execute_query(database: str, query: str) -> dict:
    """Execute SQL queries against MySQL database."""
    
@mcp.tool()
async def list_tables(database: str) -> list:
    """List all tables in a database."""
```

#### **Snowflake Integration**
```python
@mcp.tool()
async def query_snowflake(sql: str) -> dict:
    """Execute queries on Snowflake data warehouse."""
```

#### **AWS Integration**
```python
@mcp.tool()
async def list_s3_objects(bucket: str) -> list:
    """List objects in AWS S3 bucket."""
    
@mcp.tool()
async def get_rds_databases() -> list:
    """List RDS database instances."""
```

---

## A2A (Agent-to-Agent) Integration

### What is A2A?

Agent-to-Agent (A2A) protocol enables **orchestration of multiple agents working together**. It's part of Google's agent ecosystem.

### A2A Architecture

```
┌──────────────┐
│ Client Apps  │
└────────┬─────┘
         │ A2A Protocol (JSON-RPC)
    ┌────▼──────────────────────────┐
    │   A2A Agent Executor          │
    │   (Runs on port 10030)        │
    │                               │
    │  ┌─────────────────────────┐  │
    │  │ Root Agent              │  │
    │  │ - Orchestrates tasks    │  │
    │  │ - Routes to sub-agents  │  │
    │  │ - Manages context       │  │
    │  └──────────────┬──────────┘  │
    │                 │             │
    │  ┌──────────────▼───────┐     │
    │  │ MCP Tools            │     │
    │  │ (Currency, Weather,  │     │
    │  │  Search, etc.)       │     │
    │  └──────────────────────┘     │
    └───────────────────────────────┘
         │
    ┌────▼────────────────────────────┐
    │ External Services               │
    │ (APIs, Databases, LLMs)         │
    └─────────────────────────────────┘
```

### A2A Implementation Example

**File:** `google_adk_agent_mcp/currency_agent.py`

```python
from google.adk import agent as agent_lib
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from mcp_toolset import MCPToolset

# Step 1: Load MCP tools
mcp_tools = MCPToolset(
    server_url="http://localhost:7080/mcp"
).get_tools()

# Step 2: Define root agent
root_agent = agent_lib.Agent(
    instructions="Help users with currency conversion and financial queries",
    tools=[*mcp_tools, *other_tools],
    model="models/gemini-2.0-flash"
)

# Step 3: Convert to A2A
a2a_app = to_a2a(root_agent, port=10030)

# Step 4: Run server
if __name__ == "__main__":
    a2a_app.run()
```

### A2A Client Communication

**File:** `google_adk_agent_mcp/test_client.py`

```python
from google.adk.a2a.client import A2AClient
import json

# Connect to A2A agent
client = A2AClient("http://localhost:10030")

# Single-turn request
response = client.query(
    message="What is 100 USD in CAD?",
    context_id="session-123"
)

# Multi-turn conversation
context_id = "session-456"

# First turn
response1 = client.query("How much is 100 USD?", context_id)
# Agent: "Please specify target currency"

# Second turn (history is maintained)
response2 = client.query("in GBP", context_id)
# Agent: "100 USD = 74.79 GBP"

# Response structure:
{
    "id": "task-id",
    "status": "completed",
    "artifacts": [
        {
            "name": "conversion_result",
            "parts": [{"kind": "text", "text": "..."}]
        }
    ],
    "history": [
        {"role": "user", "text": "..."},
        {"role": "agent", "text": "..."}
    ]
}
```

### Multi-Agent Orchestration

A2A enables complex workflows:

```
Task: Comprehensive financial analysis

1. Currency Converter Agent
   - Converts amounts between currencies
   - Calls: get_exchange_rate()

2. Crypto Analyst Agent
   - Analyzes cryptocurrency trends
   - Calls: get_crypto_prices()

3. Summary Agent
   - Combines insights
   - Calls: tavily_search() for market news

Client Request
    │
    ├─► A2A Router
    │   │
    │   ├─► Sub-Agent 1 (Currency) ──► MCP Currency Server
    │   │
    │   ├─► Sub-Agent 2 (Crypto) ────► MCP Crypto Server
    │   │
    │   └─► Sub-Agent 3 (Summary) ───► MCP Search Server
    │       │
    ├─ Aggregate Results
    └─► Return to Client
```

---

## Advanced Implementations

### 1. **Lexical Graph Processing Pipeline**

The Neo4j Lexical Graph server demonstrates advanced MCP patterns:

#### **Processing Flow**

```
Input PDF Files
    │
    ├─ Pre-Flight Phase
    │  ├── Count files and pages
    │  ├── Estimate processing time
    │  └── Request user confirmation
    │
    ├─ Parse Phase (Async, Parallel)
    │  ├── docling (modern, multi-format)
    │  ├── pymupdf (fast, structured)
    │  ├── text_only (fallback)
    │  └── vlm_blocks (vision-based)
    │
    ├─ Element Extraction
    │  ├── Text blocks
    │  ├── Tables (preserved as structured data)
    │  ├── Images (base64 encoded)
    │  ├── Headings (hierarchical)
    │  └── Metadata
    │
    ├─ Neo4j Graph Creation
    │  ├── Create Document node
    │  ├── Create Page nodes
    │  ├── Create Element nodes
    │  ├── Link with relationships
    │  └── Build reading order NEXT chains
    │
    ├─ Chunking Phase
    │  ├── token_window (overlapping)
    │  ├── structured (by elements)
    │  ├── by_section (uses hierarchy)
    │  └── by_page (page-aware)
    │
    ├─ Enrichment Phase
    │  ├── Create section hierarchy
    │  ├── Generate descriptions (LLM)
    │  ├── Create embeddings
    │  └── Index for full-text search
    │
    ├─ Verification Phase
    │  ├── Check orphan nodes
    │  ├── Validate NEXT chains
    │  ├── Count statistics
    │  └── Reconstruct as Markdown
    │
    └─ Output
       ├── Success report
       ├── Processing logs
       ├── Reconstruction files
       └── Graph statistics
```

#### **Job Management Pattern**

```python
class Job:
    job_id: str
    status: JobStatus  # PENDING, RUNNING, COMPLETE, FAILED
    progress: float    # 0.0 to 1.0
    elapsed: timedelta
    files_completed: int
    files_total: int
    
    def to_status_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "progress_percentage": self.progress * 100,
            "elapsed_seconds": self.elapsed.total_seconds(),
            "files": f"{self.files_completed}/{self.files_total}",
            "eta_seconds": self.estimate_remaining()
        }
```

#### **Async Processing Pattern**

```python
@mcp.tool()
async def create_lexical_graph(path: str) -> str:
    # Create background job
    job = Job(job_id=uuid4(), status=JobStatus.PENDING)
    _job_manager.add_job(job)
    
    # Start processing in background
    asyncio.create_task(_process_async(job))
    
    # Return immediately with job ID
    return json.dumps({
        "status": "processing",
        "job_id": job.job_id,
        "message": "Processing started. Check status with check_processing_status()"
    })

async def _process_async(job: Job):
    try:
        job.status = JobStatus.RUNNING
        
        # Count files
        pdf_files = list(path.glob("*.pdf"))
        job.files_total = len(pdf_files)
        
        # Process each file
        for i, pdf in enumerate(pdf_files):
            await process_pdf(pdf, neo4j_driver, database)
            job.files_completed = i + 1
            job.progress = (i + 1) / job.files_total
            
        job.status = JobStatus.COMPLETE
    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)
```

### 2. **Document Reconstruction**

The ability to reconstruct documents from graph demonstrates graph integrity:

```python
async def reconstruct_document(document_id: str, output_dir: str) -> str:
    """
    Reconstructs original document structure:
    
    From Graph:
    Document {id} ──HAS_PAGE──► Page {pageNumber}
                 ──HAS_ELEMENT─► Element {type, text, position}
    
    Creates reading-order chain via NEXT relationships
    
    Outputs:
    1. Element-based reconstruction (reading order)
    2. Chunk-based reconstruction (if chunks exist)
    3. Both as .md files for comparison
    """
    
    # Restore from graph
    elements = await get_elements_in_order(document_id)
    
    # Group by page
    pages = {}
    for element in elements:
        page_num = element.page_number
        if page_num not in pages:
            pages[page_num] = []
        pages[page_num].append(element)
    
    # Generate Markdown
    md_lines = []
    for page_num in sorted(pages.keys()):
        md_lines.append(f"# Page {page_num + 1}")
        for elem in pages[page_num]:
            if elem.type == "heading":
                md_lines.append(f"{'#' * (elem.level + 1)} {elem.text}")
            elif elem.type == "table":
                md_lines.append(f"\n**[TABLE]**\n{elem.text}\n")
            else:
                md_lines.append(elem.text)
    
    # Write output
    output_file.write_text("\n".join(md_lines))
    return f"Reconstruction saved to {output_file}"
```

### 3. **Multi-Framework Integration**

The project demonstrates integration across multiple AI frameworks:

```
┌──────────────────────────────────────────────────────┐
│          Integration Points                          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  LangChain ◄────► MCP Servers                       │
│                  (via MultiServerMCPClient)         │
│                                                      │
│  Google ADK ◄──► A2A Protocol ◄─────► MCP Servers   │
│                  (via MCPToolset)                    │
│                                                      │
│  FastAPI ◄─────► FastMCP ◄─────► Transport          │
│                  (SSE bridge)      (Stdio/SSE)       │
│                                                      │
│  Claude Desktop ◄── Stdio ──► MCP Servers           │
│                  (stdio.json)                        │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Deployment & Configuration

### 1. **Local Development Setup**

#### **Installation**
```bash
# Clone or navigate to project
cd MCP_servers_and_a2a_utils

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install fastmcp mcp httpx

# For specific features:
pip install python-dotenv neo4j pymupdf docling-core
pip install google-cloud-aiplatform  # For Google ADK
pip install langchain langchain-mcp-adapters  # For LangChain integration
```

#### **Environment Setup**
```bash
# Create .zprofile or .env with:
export OPENAI_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."
export OPENWEATHERMAP_API_KEY="..."
export NEO4J_URI="neo4j://localhost:7687"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="password"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

### 2. **Running Individual Servers**

#### **FastMCP Currency Server**
```bash
cd google_adk_agent_mcp
python -m uvicorn currency_agent:app --host 0.0.0.0 --port 7080

# Server starts with SSE at http://0.0.0.0:7080/sse
```

#### **Neo4j Lexical Graph Server**
```bash
cd neo4j-mcp-workspace-template/mcp-neo4j-lexical-graph

# Stdio transport (for Claude Desktop)
python -m mcp_neo4j_lexical_graph.server --transport stdio

# SSE transport (for HTTP clients)
python -m mcp_neo4j_lexical_graph.server --transport sse --host 0.0.0.0 --port 8002
```

#### **Weather Server**
```bash
cd mcp_weather_server
python weather.py  # Starts on port 8000
```

### 3. **Claude Desktop Configuration**

**File:** `claude_config.json`

```json
{
  "mcpServers": {
    "currency": {
      "command": "python",
      "args": ["google_adk_agent_mcp/currency_agent.py"],
      "transport": "stdio"
    },
    "weather": {
      "command": "python",
      "args": ["mcp_weather_server/weather.py"],
      "transport": "stdio"
    },
    "neo4j_lexical": {
      "command": "python",
      "args": ["neo4j-mcp-workspace-template/mcp-neo4j-lexical-graph/src/mcp_neo4j_lexical_graph/server.py"],
      "env": {
        "NEO4J_URI": "neo4j://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "password"
      }
    }
  }
}
```

**Usage in Claude Desktop:**
1. Copy `claude_config.json` to `~/.claude/resources/mcp.json`
2. Restart Claude Desktop
3. Tools from all servers available to Claude

### 4. **MCP Inspector Debugging**

```bash
# Start inspector
npx @modelcontextprotocol/inspector

# Open in browser
http://127.0.0.1:6274/?MCP_PROXY_AUTH_TOKEN=<token>

# Test tools:
# - Select server
# - List available tools
# - Invoke with parameters
# - View results and errors
```

### 5. **Running A2A Agent**

```bash
# Start A2A server
cd google_adk_agent_mcp
python currency_agent.py

# Server runs on port 10030
# Logs show connection status

# In another terminal, run client
python test_client.py

# Creates conversation with agent
```

---

## Use Cases & Examples

### 1. **Currency Conversion Workflow**

```
User: "How much is 100 USD in GBP?"
│
▼
Claude/Agent processes query
│
├─ Recognizes: Currency conversion needed
├─ Identifies: Source=USD, Target=GBP, Amount=100
│
▼
Calls MCP Tool: get_exchange_rate("USD", "GBP")
│
▼
A2A Agent (or Claude) receives tool result:
{
  "rate": 0.7479,
  "from": "USD",
  "to": "GBP",
  "conversion": 100 * 0.7479 = 74.79
}
│
▼
Formats response: "100 USD equals approximately 74.79 GBP"
│
▼
Returns to user
```

**Components Used:**
- Currency Exchange Server (MCP)
- A2A Protocol Layer (Optional)
- Tool Invocation Engine
- Response Formatting

### 2. **Document Ingestion & RAG**

```
Process: Upload Research Papers → Build Knowledge Graph → Query with RAG

Step 1: Ingest Document
┌──────────────────────────┐
│ User uploads: paper.pdf  │
└──────────────┬───────────┘
               │
               ▼
        ┌────────────────────┐
        │ Neo4j Lexical      │
        │ create_lexical_    │
        │ graph(pdf_path)    │
        └────────┬───────────┘
                 │
      Processing in background
                 │
        ┌────────▼──────────────┐
        │ Job Status            │
        │ - Parse PDF           │
        │ - Extract elements    │
        │ - Create nodes/edges  │
        │ - Build reading order │
        └────────┬──────────────┘
                 │
               Complete
                 │
        ┌────────▼──────────────┐
        │ Document Graph        │
        │ - Document node       │
        │ - Page nodes          │
        │ - Element nodes       │
        │ - Chunk nodes         │
        │ - Relationship indexes│
        └──────────────────────┘

Step 2: Query with RAG
┌──────────────────────┐
│ User Query: Explain  │
│ the paper's main     │
│ contribution         │
└──────────┬───────────┘
           │
           ▼
    ┌──────────────────────┐
    │ GraphRAG Server      │
    │ query_with_rag(...)  │
    └──────────┬───────────┘
               │
    ┌──────────▼──────────────────┐
    │ 1. Vector search in embeddings
    │ 2. Retrieve context chunks   │
    │ 3. Extract entity paths      │
    │ 4. Build prompt with context │
    └──────────┬──────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │ LLM (Claude)         │
    │ Generate answer      │
    └──────────┬───────────┘
               │
               ▼
    Return RAG-augmented response
```

### 3. **Multi-Agent Collaboration**

```
Task: Comprehensive Travel Planning

User Request: "Plan a trip to Japan with $5000 budget"
│
▼
A2A Router decides:
│
├─► Currency Agent
│   "Convert $5000 to JPY"
│   Calls: get_exchange_rate("USD", "JPY")
│   Returns: ≈750,000 JPY estimate
│
├─► Search Agent
│   "Find flights and hotels in Japan"
│   Calls: tavily_search("Japan flights hotels")
│   Returns: Recent deals and recommendations
│
├─► Weather Agent
│   "Check Japan climate for travel dates"
│   Calls: get_weather("Tokyo", "JP")
│   Returns: Seasonal weather patterns
│
└─► Aggregator Agent
    Combines all information:
    - Budget in local currency
    - Available options
    - Best seasons
    Returns: Comprehensive travel plan

Response to User:
"With $5000 (≈750,000 JPY), you can:
- Stay 10-14 days
- Visit 2-3 cities
- Best season: Spring/Fall
- Current flight deals available..."
```

### 4. **Real-Time Data Applications**

**Crypto Portfolio Tracker**

```python
# Runs as A2A agent
@tool
async def get_portfolio_summary(portfolio_dict: dict) -> str:
    """
    Tracks cryptocurrency holdings and provides real-time analysis
    
    portfolio_dict = {
        "bitcoin": 0.5,
        "ethereum": 5.0,
        "cardano": 1000.0
    }
    """
    
    prices = {}
    total_value = 0
    
    for symbol, amount in portfolio_dict.items():
        price = await get_crypto_prices(symbol, "usd")
        value = amount * price
        prices[symbol] = {
            "amount": amount,
            "price_per_unit": price,
            "total_value": value
        }
        total_value += value
    
    return format_portfolio_report(prices, total_value)
```

---

## Best Practices & Lessons Learned

### 1. **MCP Server Design**

#### **✅ Do's**
- Use strong type hints with Pydantic models
- Provide detailed docstrings for all tools
- Include tool annotations for client clarity
- Handle errors gracefully with ToolError
- Support async operations
- Validate input parameters
- Return structured, parseable results

#### **❌ Don'ts**
- Don't assume client error handling
- Don't expose system implementation details
- Don't create tools that require extensive setup
- Don't return raw exception messages to users
- Don't make blocking operations without timeout
- Don't expose sensitive credentials in tool descriptions

#### **Example: Proper Tool Design**

```python
from pydantic import Field
from mcp.types import ToolError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ExampleServer")

@mcp.tool()
async def safe_operation(
    parameter: str = Field(
        ...,
        description="Clear description of what this parameter does",
        json_schema_extra={"example": "good_value"}
    ),
    timeout: int = Field(
        30,
        description="Maximum seconds to wait for operation"
    )
) -> dict:
    """
    Descriptive tool docstring explaining:
    - What the tool does
    - When to use it
    - What it returns
    - Possible error conditions
    """
    try:
        # Validate input
        if not parameter:
            raise ToolError("Parameter cannot be empty")
        
        if timeout < 1 or timeout > 300:
            raise ToolError("Timeout must be between 1 and 300 seconds")
        
        # Perform operation
        result = await perform_operation(parameter, timeout=timeout)
        
        # Return structured result
        return {
            "status": "success",
            "result": result,
            "metadata": {"operation": "safe_operation"}
        }
        
    except ToolError:
        # Re-raise known errors
        raise
    except Exception as e:
        # Log and convert unknown errors
        logger.error(f"Operation failed: {e}")
        raise ToolError(f"Operation failed: {str(e)}")
```

### 2. **A2A Agent Orchestration**

#### **Agent Design Patterns**

```python
# Pattern 1: Hierarchical Agents
root_agent
├── currency_sub_agent
│   └── Tools: exchange_rate, crypto_prices
├── search_sub_agent
│   └── Tools: web_search, news
└── analysis_sub_agent
    └── Tools: sentiment_analysis, trend_detection

# Pattern 2: Tool-Sharing Agents
agent_a ─┬─► shared_tool_1
         ├─► shared_tool_2
agent_b ─┘   (reduces duplication)

# Pattern 3: Fan-Out-Fan-In
root_agent
├─ Task 1 → agent_1 → task_1a, task_1b (parallel)
├─ Task 2 → agent_2 → task_2a, task_2b (parallel)
└─ Combine results
```

### 3. **Error Handling Patterns**

```python
# Pattern 1: Graceful Degradation
@mcp.tool()
async def get_data_with_fallback(primary_source: str) -> dict:
    try:
        return await fetch_from_primary(primary_source)
    except ConnectionError:
        logger.warning(f"Primary source {primary_source} unavailable")
        return await fetch_from_fallback()
    except TimeoutError:
        logger.warning("Operation timed out, returning cached data")
        return get_cached_data()

# Pattern 2: Structured Error Responses
@mcp.tool()
async def safe_tool(param: str) -> dict:
    try:
        result = await process(param)
        return {
            "status": "success",
            "data": result
        }
    except ValidationError as e:
        raise ToolError(f"Invalid input: {e.message}")
    except PermissionError as e:
        raise ToolError(f"Permission denied: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise ToolError(f"Internal error occurred")
```

### 4. **Performance Optimization**

#### **Async/Concurrent Patterns**

```python
# ❌ Slow: Sequential processing
for pdf_file in pdf_files:
    await process_pdf(pdf_file)  # Processes one at a time

# ✅ Fast: Parallel processing
tasks = [process_pdf(pdf) for pdf in pdf_files]
results = await asyncio.gather(*tasks, return_exceptions=True)

# ✅ Better: Bounded concurrency
semaphore = asyncio.Semaphore(max_workers)
async def process_bounded(pdf):
    async with semaphore:
        return await process_pdf(pdf)

tasks = [process_bounded(pdf) for pdf in pdf_files]
results = await asyncio.gather(*tasks)

# ✅ Best for CPU-bound: Process pool
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as pool:
    results = await asyncio.get_event_loop().run_in_executor(
        pool, cpu_intensive_function, argument
    )
```

#### **Database Connection Pooling**

```python
# Neo4j connection pooling (automatic)
from neo4j import AsyncGraphDatabase

driver = AsyncGraphDatabase.driver(
    "neo4j://localhost:7687",
    auth=("neo4j", "password"),
    max_connection_pool_size=100,
    connection_timeout=30.0
)

# Properly close when shutting down
await driver.close()
```

### 5. **Testing MCP Servers**

```python
# Test tool invocation
@pytest.mark.asyncio
async def test_get_exchange_rate():
    mcp = create_mcp_server()
    
    result = await mcp._tools["get_exchange_rate"].fn(
        currency_from="USD",
        currency_to="GBP"
    )
    
    assert result["status"] == "success"
    assert "rate" in result
    assert result["rate"] > 0

# Test error handling
@pytest.mark.asyncio
async def test_invalid_currency():
    mcp = create_mcp_server()
    
    with pytest.raises(ToolError):
        await mcp._tools["get_exchange_rate"].fn(
            currency_from="INVALID",
            currency_to="GBP"
        )

# Integration test with MCP Inspector
def test_server_startup():
    server = subprocess.Popen(
        ["python", "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(2)  # Wait for server
    
    response = requests.get("http://localhost:8000/mcp")
    assert response.status_code == 200
    
    server.terminate()
```

### 6. **Documentation Best Practices**

Each tool should document:
```python
@mcp.tool()
async def comprehensive_tool(
    required_param: str = Field(
        ...,
        description="What this parameter does"
    ),
    optional_param: int = Field(
        42,
        description="What this controls",
        ge=1, le=100  # Validation
    )
) -> dict:
    """
    [1-2 sentence summary]
    
    [Detailed explanation of functionality]
    
    Parameters:
    - required_param: [Description with examples]
    - optional_param: [Description with range/options]
    
    Returns:
    {
        "status": "success" or "error",
        "data": [Actual return data structure],
        "metadata": [Optional metadata]
    }
    
    Raises:
    - ToolError: When [specific condition]
    
    Examples:
    >>> result = await comprehensive_tool("value", optional_param=50)
    >>> print(result["data"])
    """
```

---

## Advanced Topics

### 1. **Custom Transport Protocol**

While Stdio and SSE are standard, you can implement custom transports:

```python
from mcp.server import Server
from mcp.server.base import *

class CustomTransport(ServerTransport):
    """Custom transport implementation."""
    
    async def read(self) -> ServerMessage:
        """Read message from source."""
        pass
    
    async def write(self, message: ServerMessage) -> None:
        """Write message to destination."""
        pass

# Use custom transport
await mcp_server.run(CustomTransport())
```

### 2. **Resource Streaming**

For large resources, implement streaming:

```python
@mcp.resource("data://large-dataset/{id}")
async def stream_dataset(id: str):
    # Stream data in chunks instead of loading all at once
    async def generate():
        async for chunk in fetch_chunks(id):
            yield chunk
    
    return {
        "uri": f"data://large-dataset/{id}",
        "mimeType": "application/octet-stream",
        "contents": [
            {"type": "text", "text": chunk} async for chunk in generate()
        ]
    }
```

### 3. **LLM Sampling (Experimental)**

The MCP specification includes sampling support for generating text:

```python
@server.sampling()
async def sample_text(
    messages: list,
    model: str = "claude-3-sonnet",
    max_tokens: int = 1024
) -> SamplingMessage:
    """Use Claude to generate text within MCP context."""
    # Implementation uses Claude API
```

### 4. **Monitoring & Observability**

```python
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def with_metrics(func):
    """Decorator to track tool execution metrics."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        import time
        start = time.time()
        
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start
            
            logger.info(
                "Tool executed",
                extra={
                    "tool": func.__name__,
                    "duration_ms": duration * 1000,
                    "status": "success"
                }
            )
            return result
        except Exception as e:
            duration = time.time() - start
            logger.error(
                "Tool failed",
                extra={
                    "tool": func.__name__,
                    "duration_ms": duration * 1000,
                    "error": str(e)
                }
            )
            raise
    
    return wrapper

@mcp.tool()
@with_metrics
async def monitored_tool():
    """Tool with automatic metrics collection."""
    pass
```

---

## Troubleshooting Guide

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Connection refused" in Inspector | Server not running | Start server with `python server.py` first |
| Tool not appearing in list | Import error or decorator not applied | Check @mcp.tool() decorator, verify imports |
| A2A "Input required" state | Agent waiting for clarification | Client should send followup message |
| Neo4j connection timeout | Database unreachable | Verify NEO4J_URI, username, password |
| Out of memory in PDF processing | Too many large PDFs in parallel | Reduce max_parallel parameter |
| SSE stream closed unexpectedly | Network timeout or server crash | Check server logs, increase timeout settings |
| Tool results not serializable | Non-JSON-compatible data type | Convert to string or structured format |

---

## Conclusion

This project represents a **comprehensive, production-ready ecosystem** for building AI agents with:

1. **Flexible Tool Integration** - 20+ specialized MCP servers
2. **Multi-Framework Support** - LangChain, Google ADK, FastAPI
3. **Sophisticated Orchestration** - A2A protocol for agent collaboration
4. **Advanced Processing** - ML pipeline for document understanding
5. **Real-World Examples** - Currency, weather, search, RAG systems

The architecture demonstrates how to **bridge AI models with external capabilities** through standardized protocols, enabling complex, multi-step workflows while maintaining clean abstractions and separation of concerns.

**Key Takeaways:**
- **MCP is protocol-agnostic** - Works with any AI model/client
- **Async/concurrent patterns are essential** - For performance and scalability
- **Type safety matters** - Pydantic validation prevents errors early
- **Documentation is critical** - Tool descriptions enable better model decisions
- **Error handling builds trust** - Graceful degradation improves reliability
- **Observability enables debugging** - Logging and monitoring are essential

This project serves as an **excellent reference implementation** for anyone building AI-powered systems with tool use, RAG, or multi-agent orchestration.


# Installation steps
1. pip install uv
2. uv init MCP_servers_and_a2a_utils
3. uv run mcp install main.py
4. uv run mcp 


# References

1. https://medium.com/data-and-beyond/the-model-context-protocol-mcp-the-ultimate-guide-c40539e2a8e7
2. https://github.com/coleam00/ottomator-agents/blob/main/nba-agent/nba_agent.py
3. https://www.youtube.com/watch?v=v_6EXt6T83I
4. https://modelcontextprotocol.io/introduction
5. https://github.com/coleam00/ottomator-agents/tree/main/pydantic-ai-mcp-agent

# Example References
1. https://www.dremio.com/blog/building-a-basic-mcp-server-with-python/
2. https://github.com/HeetVekariya/Linear-Regression-MCP
3. https://github.com/singlestore-labs/mcp-server-singlestore
4. https://github.com/jlowin/fastmcp
5. https://github.com/awslabs/mcp/blob/main/src/aws-documentation-mcp-server/awslabs/aws_documentation_mcp_server/server.py

# MCP workshop here
1. https://github.com/akranga/mcp-workshop
