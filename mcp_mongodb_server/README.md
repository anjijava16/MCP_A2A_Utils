# MongoDB MCP Server 🍃

## Overview
FastMCP-based server for MongoDB NoSQL database operations with support for document management, aggregation pipelines, and advanced queries.

## Features
- **Document Management**: CRUD operations on documents
- **Aggregation**: Complex aggregation pipelines
- **Indexing**: Create and manage indexes
- **Flexible Queries**: MongoDB query syntax support
- **Bulk Operations**: Insert/update multiple documents
- **Statistics**: Collection metrics and analysis

## Setup & Installation

### Prerequisites
- Python 3.9+
- MongoDB 4.0+

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export MONGODB_URI="mongodb://localhost:27017"
export MONGODB_DATABASE="myapp"
```

### Running
```bash
python server.py
```

## Tools Available

### list_collections
List all collections in the database.

### find_documents
Query documents with filtering and limit.

**Example:**
```python
await client.call_tool("find_documents", {
    "collection": "users",
    "filter": {"age": {"$gt": 21}},
    "limit": 10
})
```

### find_one_document
Find a single document.

### insert_document
Insert a single document.

### insert_many
Insert multiple documents at once.

### update_document
Update documents matching a filter.

### delete_documents
Delete documents matching a filter.

### count_documents
Count documents in collection.

### aggregate
Execute aggregation pipeline.

### create_index
Create index on field(s).

### get_collection_stats
Get collection statistics.

## Usage Examples

### Query Documents
```python
await client.call_tool("find_documents", {
    "collection": "products",
    "filter": {
        "category": "electronics",
        "price": {"$lte": 100}
    },
    "limit": 20
})
```

### Aggregation
```python
await client.call_tool("aggregate", {
    "collection": "orders",
    "pipeline": [
        {
            "$group": {
                "_id": "$customer_id",
                "total": {"$sum": "$amount"}
            }
        },
        {
            "$sort": {"total": -1}
        },
        {
            "$limit": 10
        }
    ]
})
```

### Bulk Insert
```python
await client.call_tool("insert_many", {
    "collection": "logs",
    "documents": [
        {"timestamp": "2024-06-15", "level": "INFO", "message": "..."},
        {"timestamp": "2024-06-15", "level": "ERROR", "message": "..."}
    ]
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
pymongo>=4.0
```

## Security Best Practices
- Use authentication with MongoDB
- Enable SSL/TLS
- Implement access control
- Validate input data
- Use proper query filtering

## Advanced Features

### Text Search
```python
await client.call_tool("aggregate", {
    "collection": "documents",
    "pipeline": [
        {
            "$match": {
                "$text": {"$search": "search term"}
            }
        }
    ]
})
```

### Lookups (Joins)
```python
await client.call_tool("aggregate", {
    "collection": "orders",
    "pipeline": [
        {
            "$lookup": {
                "from": "customers",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "customer"
            }
        }
    ]
})
```

## Troubleshooting
- Verify MongoDB is running
- Check connection URI
- Confirm database permissions
- Review logs for detailed errors

## Use Cases
- Document storage
- Content management
- User profiles
- Event tracking
- Analytics data
