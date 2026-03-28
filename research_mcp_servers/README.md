# Research MCP Servers 📚

## Overview
Advanced research and knowledge base servers providing capabilities for searching, analyzing, and managing academic papers, research data, and computational resources through MCP tools.

## Features
- **Paper Search**: ArXiv, PubMed, and academic databases
- **Data Analysis**: Statistical analysis and visualization
- **Knowledge Management**: Store and retrieve research data
- **Citation Management**: Handle academic citations
- **Research Workflow**: Support for research pipelines

## Server Collection

### ArXiv Search Server
**Purpose**: Search academic papers on ArXiv

**Tools:**
- `search_arxiv(query, max_results)` - Search papers
- `get_paper_metadata(paper_id)` - Get paper details
- `get_paper_pdf(paper_id)` - Download PDF

## Setup & Usage

### Installation
```bash
pip install fastmcp arxiv mcp httpx
```

### Running Servers
```bash
# Start research server
python research_mcp_server.py

# Multiple servers can run on different ports
python arxiv_server.py --port 8001
python pubmed_server.py --port 8002
```

## Features
- Academic database integration
- Citation management
- Paper metadata extraction
- Research data organization
- Publication tracking
- Collaboration tools

## Dependencies
- fastmcp
- arxiv
- mcp
- Academic database APIs

## Use Cases
- Literature reviews
- Research discovery
- Paper management
- Citation tracking
- Collaboration
