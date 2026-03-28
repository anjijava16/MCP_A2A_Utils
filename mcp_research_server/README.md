# MCP Research Server 📚

## Overview
A FastMCP-based server for academic research paper discovery and management. This server integrates with arXiv to search for research papers by topic and organize paper information for later retrieval and analysis.

## Features
- **Paper Search**: Search arXiv for academic papers by topic
- **Bulk Retrieval**: Get multiple papers at once with configurable limits
- **Local Storage**: Save paper information to local filesystem
- **Paper Metadata**: Extract and store paper IDs, titles, authors, abstracts
- **Topic-based Organization**: Organize papers by search topic

## Tools Available
- `search_papers(topic, max_results)` - Search arXiv for papers
  - Parameters:
    - topic: Research topic to search for
    - max_results: Maximum number of papers to retrieve (default: 5)
  - Returns: List of paper IDs found in search

- Additional tools for paper management and retrieval

## Setup & Usage

### Installation
```bash
pip install fastmcp arxiv
```

### Configuration
- **Storage Directory**: Papers stored in `./papers` directory
- **Default Results**: 5 papers per search
- **arXiv API**: Uses public arXiv API (no key required)

### Running the Server
```bash
# Stdio transport
python research_mcp_server.py

# Server runs on port 8001
```

### Example Usage
```python
# Search for papers on machine learning
papers = search_papers(
    topic="machine learning optimization",
    max_results=10
)

# Returns list of paper IDs:
# ["2301.12345", "2301.12346", ...]

# Each paper's information is automatically saved locally
```

## Paper Organization

### Storage Structure
```
papers/
├── <topic1>/
│   ├── paper_1.json
│   ├── paper_2.json
│   └── ...
├── <topic2>/
│   └── ...
└── papers_metadata.json
```

### Paper Information Stored
- Paper ID
- Title
- Authors
- Abstract
- Publication date
- arXiv categories
- Paper URL

## Files
- `research_mcp_server.py` - Main research server implementation

## Use Cases
- **Literature Review**: Systematically search and organize papers
- **Research Discovery**: Find related papers by topic
- **Knowledge Base**: Build local paper database
- **Academic Research**: Support research workflows
- **Trend Analysis**: Track publication trends in specific fields

## Features Details
- **arXiv Integration**: Direct API access to arXiv papers
- **Search Flexibility**: Find papers from various research areas
- **Result Sorting**: Papers sorted by relevance by default
- **Category Support**: Find papers in specific arXiv categories

## Error Handling
- Invalid topic handling
- API timeout management
- Paper availability checks
- Storage error handling

## Dependencies
- fastmcp
- arxiv
- mcp

## Performance
- Fast paper searches
- Efficient arXiv API utilization
- Minimal network overhead
- Local storage for quick access

## Common Searches
```python
# Machine learning papers
search_papers("neural networks", 10)

# Computer vision
search_papers("computer vision", 10)

# Natural language processing
search_papers("transformers NLP", 10)

# Quantum computing
search_papers("quantum", 5)
```

## Future Enhancements
- Full-text search capabilities
- Paper recommendation engine
- Citation tracking
- Author-based searches
- PDF download and parsing
- Annotation and tagging system
