# Google Cloud Spanner MCP Server 🌍

## Overview
FastMCP-based server for Google Cloud Spanner relational database with global scale and strong consistency.

## Features
- **Global Distribution**: Multi-region replication
- **ACID Transactions**: Full ACID compliance
- **Strong Consistency**: Serializable consistency
- **Horizontal Scaling**: Automatic scaling
- **Automatic Backup**: Built-in backup and recovery
- **High Availability**: 99.999% SLA

## Setup & Installation

### Prerequisites
- Python 3.9+
- Google Cloud Project
- Spanner Instance and Database
- gcloud CLI configured

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export GCP_PROJECT_ID="your-project-id"
export SPANNER_INSTANCE_ID="my-instance"
export SPANNER_DATABASE_ID="my-database"
```

### Running
```bash
python server.py
```

## Tools Available

### execute_query
Execute SQL queries.

### list_tables
List all tables in database.

### describe_table
Get table schema.

### insert_row
Insert single row.

### update_row
Update existing row.

### delete_row
Delete row by key.

### batch_insert
Batch insert rows.

### get_database_info
Get database information.

## Usage Examples

### Execute Query
```python
await client.call_tool("execute_query", {
    "query": "SELECT * FROM users WHERE status = @status",
    "parameters": {"status": "active"}
})
```

### Insert Row
```python
await client.call_tool("insert_row", {
    "table_name": "users",
    "row": {
        "id": "123",
        "name": "John",
        "email": "john@example.com"
    }
})
```

### Batch Insert
```python
await client.call_tool("batch_insert", {
    "table_name": "users",
    "rows": [
        {"id": "1", "name": "User 1"},
        {"id": "2", "name": "User 2"}
    ]
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
google-cloud-spanner>=3.0
```

## Use Cases
- Global applications
- Financial transactions
- Large-scale databases
- Multi-region systems
- Strongly consistent data

## Best Practices
- Use composite primary keys
- Design for scalability
- Use node pools appropriately
- Monitor replication lag
- Implement proper backups

## Performance Tips
- Use batch operations
- Index frequently queried columns
- Partition data effectively
- Monitor CPU usage
