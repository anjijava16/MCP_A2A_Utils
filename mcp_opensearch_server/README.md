# OpenSearch MCP Server 🔎

## Overview
FastMCP-based server for OpenSearch (Elasticsearch alternative) with full-text search and analytics capabilities.

## Features
- **Full-Text Search**: Powerful search capabilities
- **Open Source**: Free alternative to Elasticsearch
- **Scalable**: Distributed search and analytics
- **Analytics**: Real-time analytics
- **Alerting**: Built-in alerting
- **Security**: Fine-grained access control

## Setup & Installation

### Prerequisites
- Python 3.9+
- OpenSearch 1.0+
- Credentials for OpenSearch cluster

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export OPENSEARCH_HOSTS="localhost:9200"
export OPENSEARCH_USER="admin"
export OPENSEARCH_PASSWORD="AdminPassword123!"
export OPENSEARCH_USE_SSL="true"
```

### Running
```bash
python server.py
```

## Tools Available

### list_indices
List all indices in cluster.

### create_index
Create new index with optional settings.

### delete_index
Delete an index.

### index_document
Index a single document.

### get_document
Get document by ID.

### search_documents
Search with query DSL.

### delete_document
Delete document by ID.

### bulk_index
Bulk index multiple documents.

### get_index_stats
Get index statistics.

## Usage Examples

### Create Index
```python
await client.call_tool("create_index", {
    "index_name": "articles",
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "published": {"type": "date"}
        }
    }
})
```

### Index Document
```python
await client.call_tool("index_document", {
    "index_name": "articles",
    "doc_id": "1",
    "document": {
        "title": "OpenSearch Introduction",
        "content": "OpenSearch is a open-source search engine",
        "published": "2024-01-01"
    }
})
```

### Search Documents
```python
await client.call_tool("search_documents", {
    "index_name": "articles",
    "query": {
        "match": {
            "title": "OpenSearch"
        }
    },
    "size": 10
})
```

### Bulk Index
```python
await client.call_tool("bulk_index", {
    "index_name": "articles",
    "documents": [
        {"id": "1", "data": {"title": "Article 1"}},
        {"id": "2", "data": {"title": "Article 2"}}
    ]
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
opensearch-py>=2.0
```

## Use Cases
- Full-text search
- Log analytics
- Application search
- Real-time analytics
- Security analytics
- Business analytics

## Best Practices
- Use appropriate index settings
- Implement proper mappings
- Use filters for performance
- Monitor cluster health
- Implement backup strategy
- Use aliases for index management

## Performance Optimization
- Use dedicated nodes
- Optimize shard configuration
- Implement proper caching
- Use filters instead of queries
- Monitor query performance

## Troubleshooting
- Check cluster health
- Verify index mappings
- Monitor shard allocation
- Review query performance
- Check disk space
