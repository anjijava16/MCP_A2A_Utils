# MCP Tavily Search Server 🔍

## Overview
A FastMCP-based web search server powered by the Tavily AI search engine. This server provides intelligent web search capabilities with structured results including answer snippets, relevant sources, and raw content.

## Features
- **Web Search**: Search the internet for information across topics
- **Answer Generation**: Get direct answers to search queries
- **Source Quality**: Returns highly relevant sources with content chunks
- **Time-based Filtering**: Filter results by time range (days parameter)
- **Configurable Results**: Control the number and depth of search results
- **Content Extraction**: Get raw content from sources automatically

## Tools Available
- `search_tavily(query, max_results)` - Perform web search with specified query
  - Search depth: basic (fast) or advanced (comprehensive)
  - Includes automatic answer generation
  - Returns structured results with sources and content

## Setup & Usage

### Installation
```bash
pip install fastmcp httpx python-dotenv
```

### Configuration
Create a `.env` file with your Tavily API key:
```
TAVILY_API_KEY=your_api_key_here
```

Get your API key from: https://tavily.com

### Running the Server
```bash
# Stdio transport
python tavily.py

# The server will use configured API key from environment
```

### Example Usage
```python
# Search for information
result = search_tavily(
    query="latest AI trends 2024",
    max_results=5
)

# Returns:
# - Answer: Direct answer to the query
# - Results: List of relevant sources
# - Content: Key excerpts from each source
# - Metadata: Publication dates, URLs, etc.
```

## Features Details
- **Topic**: Set to "general" for broad searches
- **Search Depth**: 
  - basic: Fast search with essential results
  - advanced: More comprehensive results (slower)
- **Chunks Per Source**: Number of content chunks from each source (default: 3)
- **Max Results**: Number of sources to return (default: 5)
- **Time Range**: Filter by recent days (default: last 3 days)

## Files
- `tavily.py` - Main Tavily search server implementation

## Configuration Parameters
- **API Endpoint**: https://api.tavily.com/search
- **Default Results**: 5 sources
- **Default Time Range**: Last 3 days
- **Default Chunks**: 3 per source

## Error Handling
- Missing API key validation
- Request timeout handling
- Source availability verification
- Result formatting and sanitization

## Performance
- Fast search with basic depth setting
- Configurable result depth for accuracy vs speed tradeoff
- Automatic content extraction and formatting
