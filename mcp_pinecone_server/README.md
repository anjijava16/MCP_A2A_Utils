# Pinecone MCP Server 🔍

## Overview
FastMCP-based server for Pinecone vector database with support for semantic search and RAG (Retrieval Augmented Generation).

## Features
- **Vector Search**: Semantic similarity search
- **Managed Service**: Fully hosted vector database
- **Namespaces**: Logical data partitioning
- **Metadata Filtering**: Filter by attributes
- **Scalability**: Automatic scaling
- **Low Latency**: Sub-100ms query latency

## Setup & Installation

### Prerequisites
- Python 3.9+
- Pinecone Account and API Key
- Indexes already created in Pinecone

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export PINECONE_API_KEY="your_api_key"
export PINECONE_ENVIRONMENT="us-west1-gcp"  # Optional
```

### Running
```bash
python server.py
```

## Tools Available

### list_indexes
List all Pinecone indexes.

### get_index_stats
Get index statistics and metadata.

### upsert_vectors
Add or update vectors in index.

### query_vectors
Query similar vectors with metadata.

### get_vector
Retrieve specific vector by ID.

### delete_vectors
Delete vectors from index.

### delete_namespace
Clear namespace data.

### update_vector_metadata
Update vector metadata.

## Usage Examples

### Upsert Vectors
```python
await client.call_tool("upsert_vectors", {
    "index_name": "documents",
    "vectors": [
        ("doc1", [0.1, 0.2, 0.3], {"title": "Document 1"}),
        ("doc2", [0.2, 0.3, 0.4], {"title": "Document 2"})
    ],
    "namespace": "prod"
})
```

### Query Vectors
```python
await client.call_tool("query_vectors", {
    "index_name": "documents",
    "query_vector": [0.15, 0.25, 0.35],
    "top_k": 10,
    "namespace": "prod"
})
```

### Get Index Stats
```python
await client.call_tool("get_index_stats", {
    "index_name": "documents"
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
pinecone-client>=3.0
```

## Use Cases
- Semantic search
- Document retrieval
- RAG systems
- Recommendation engines
- Similarity matching
- Content discovery
- Embeddings storage

## Best Practices
- Use meaningful vector IDs
- Add useful metadata
- Use namespaces for data isolation
- Monitor index size and cost
- Implement batch operations
- Use appropriate dimension sizes

## Performance Optimization
- Use namespaces for scale
- Batch upsert operations
- Filter using metadata
- Monitor query latency
- Use sparse-dense indices

## Troubleshooting
- Verify API key permissions
- Check index dimensions match
- Monitor vector count limits
- Review embedding dimensions
