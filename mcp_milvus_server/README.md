# Milvus MCP Server 🎯

## Overview
FastMCP-based server for Milvus open-source vector database with support for large-scale similarity search.

## Features
- **Open Source**: Community-driven vector database
- **Scalable**: Distributed architecture
- **Multiple Indexes**: HNSW, IVF, Flat support
- **Partitioning**: Data partitioning support
- **Flexible Schema**: Support for various field types
- **GPU Support**: Optional GPU acceleration

## Setup & Installation

### Prerequisites
- Python 3.9+
- Milvus 2.0+ (standalone or cluster)
- pymilvus library

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export MILVUS_HOST="localhost"
export MILVUS_PORT="19530"
```

### Running
```bash
python server.py
```

## Tools Available

### list_collections
List all collections in Milvus.

### get_collection_info
Get collection metadata and schema.

### insert_vectors
Insert vectors into collection.

### search_vectors
Search for similar vectors.

### delete_entities
Delete entities by ID.

### flush_collection
Flush collection to disk.

### create_partition
Create data partition.

### drop_partition
Drop data partition.

### create_index
Create index on field.

### get_collection_stats
Get collection statistics.

## Usage Examples

### Insert Vectors
```python
await client.call_tool("insert_vectors", {
    "collection_name": "documents",
    "vectors_data": [
        [1, [0.1, 0.2, 0.3]],
        [2, [0.2, 0.3, 0.4]],
        [3, [0.3, 0.4, 0.5]]
    ]
})
```

### Search Vectors
```python
await client.call_tool("search_vectors", {
    "collection_name": "documents",
    "query_vector": [0.15, 0.25, 0.35],
    "top_k": 10
})
```

### Create Index
```python
await client.call_tool("create_index", {
    "collection_name": "documents",
    "field_name": "embeddings",
    "index_params": {
        "metric_type": "L2",
        "index_type": "HNSW"
    }
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
pymilvus>=2.0
```

## Use Cases
- Semantic search
- Recommendation systems
- Image similarity search
- Document retrieval
- Duplicate detection
- Content-based search

## Best Practices
- Use appropriate index types
- Partition data by time
- Monitor memory usage
- Batch insert operations
- Use proper field types
- Create indexes before load

## Index Selection
- **HNSW**: Fast, memory efficient
- **IVF_FLAT**: Accurate, requires more memory
- **FLAT**: Exact search, slowest

## Performance Tips
- Use partitioning
- Create indexes
- Batch operations
- Monitor memory
- Tune HNSW parameters

## Troubleshooting
- Check Milvus service running
- Verify port configuration
- Monitor memory usage
- Review vector dimensions
- Check index status
