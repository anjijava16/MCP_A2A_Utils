# Qdrant MCP Server 🔷

## Overview
FastMCP-based server for Qdrant vector database with focus on compatibility, speed, and ease of use.

## Features
- **Easy to Use**: Python-native interface
- **Flexible**: Multiple distance metrics
- **Scalable**: Distributed architecture available
- **Fast**: Optimized vector search
- **Filtering**: Payload-based filtering
- **Open Source**: Community-driven

## Setup & Installation

### Prerequisites
- Python 3.9+
- Qdrant 0.10+
- Running Qdrant service

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export QDRANT_URL="http://localhost:6333"
export QDRANT_API_KEY="optional_api_key"
```

### Running
```bash
python server.py
```

## Tools Available

### list_collections
List all collections.

### collection_info
Get collection metadata.

### upsert_points
Add or update points.

### search_points
Search for similar vectors.

### get_point
Retrieve specific point.

### delete_point
Delete point by ID.

### delete_collection
Delete entire collection.

### count_points
Count points in collection.

### scroll_points
Scroll through points.

### get_server_info
Get server status.

## Usage Examples

### Upsert Points
```python
await client.call_tool("upsert_points", {
    "collection_name": "documents",
    "points": [
        {
            "id": 1,
            "vector": [0.1, 0.2, 0.3],
            "payload": {"title": "Document 1"}
        },
        {
            "id": 2,
            "vector": [0.2, 0.3, 0.4],
            "payload": {"title": "Document 2"}
        }
    ]
})
```

### Search Points
```python
await client.call_tool("search_points", {
    "collection_name": "documents",
    "query_vector": [0.15, 0.25, 0.35],
    "top_k": 10
})
```

### Scroll Points
```python
await client.call_tool("scroll_points", {
    "collection_name": "documents",
    "limit": 10,
    "offset": 0
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
qdrant-client>=2.0
```

## Use Cases
- Semantic search
- Recommendation systems
- Image search
- Similar document finding
- Anomaly detection
- Pattern matching

## Distance Metrics
- **Cosine**: Angular distance (normalized vectors)
- **L2**: Euclidean distance
- **Dot**: Dot product similarity

## Best Practices
- Use appropriate distance metrics
- Add informative payloads
- Index vectors after upload
- Use filtering for better results
- Batch operations
- Monitor collection size

## Performance Optimization
- Use HNSW index
- Batch upsert operations
- Filter during search
- Use appropriate parameters
- Monitor memory usage

## Troubleshooting
- Verify Qdrant service running
- Check API key if required
- Monitor memory allocation
- Review vector dimensions
- Check network connectivity
