# Cassandra MCP Server 📊

## Overview
FastMCP-based server for Apache Cassandra distributed NoSQL database operations with high availability and scalability support.

## Features
- **Distributed Architecture**: Multi-node cluster support
- **CQL Support**: Cassandra Query Language
- **High Availability**: Replication and failover
- **Scalability**: Horizontal scaling
- **Authentication**: User authentication support
- **Cluster Management**: Multi-node operations

## Setup & Installation

### Prerequisites
- Python 3.9+
- Apache Cassandra 3.0+
- cassandra-driver Python package

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export CASSANDRA_CONTACT_POINTS="localhost,cassandra-2,cassandra-3"
export CASSANDRA_KEYSPACE="myapp"
export CASSANDRA_USER="cassandra"
export CASSANDRA_PASSWORD="password"
```

### Running
```bash
python server.py
```

## Tools Available

### execute_query
Execute CQL queries.

### list_tables
List tables in keyspace.

### describe_table
Get table schema.

### insert_record
Insert records.

### update_record
Update records.

### delete_record
Delete records.

### get_cluster_stats
Get cluster information.

## Usage Examples

### Query Data
```python
await client.call_tool("execute_query", {
    "query": "SELECT * FROM users WHERE user_id = ?",
    "parameters": [123]
})
```

### Insert Data
```python
await client.call_tool("insert_record", {
    "table_name": "users",
    "data": {
        "user_id": 1,
        "name": "John",
        "email": "john@example.com"
    }
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
cassandra-driver>=3.25
```

## Use Cases
- Time-series data
- IoT sensor data
- High-throughput applications
- Distributed caching
- Massive scale operations

## Best Practices
- Use clustering keys properly
- Implement proper TTL strategies
- Monitor replication factor
- Use batch operations
- Optimize for read/write patterns
