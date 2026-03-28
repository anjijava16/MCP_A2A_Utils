# PostgreSQL MCP Server 🐘

## Overview
FastMCP-based server for PostgreSQL database operations with support for querying, data management, indexing, and advanced PostgreSQL features.

## Features
- **Full SQL Support**: Execute complex PostgreSQL queries
- **Index Management**: Create and manage database indexes
- **CRUD Operations**: Complete data manipulation
- **Connection Management**: Efficient connection handling
- **Error Recovery**: Robust error handling
- **Advanced Features**: Supports triggers, views, stored procedures

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 10+

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export POSTGRES_HOST="localhost"
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="your_password"
export POSTGRES_DATABASE="your_database"
export POSTGRES_PORT="5432"
```

### Running
```bash
python server.py
```

## Tools Available

### execute_sql
Execute arbitrary PostgreSQL queries with parameterized support.

**Example:**
```python
await client.call_tool("execute_sql", {
    "query": "SELECT * FROM users WHERE age > %s",
    "parameters": [21]
})
```

### list_tables
List all tables in the database.

### describe_table
Get detailed column information for a table.

### insert_record
Insert records with automatic parameter binding.

### update_record
Update records with WHERE clause conditions.

### delete_record
Delete records based on conditions.

### get_database_stats
Get database size and table count statistics.

### create_index
Create new indexes for performance optimization.

### list_indexes
View all indexes on a specific table.

## Usage Examples

### Query Data
```python
result = await client.call_tool("execute_sql", {
    "query": """
    SELECT u.id, u.name, COUNT(o.id) as order_count
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.created_at > NOW() - INTERVAL '1 year'
    GROUP BY u.id
    ORDER BY order_count DESC
    LIMIT 10
    """,
    "parameters": []
})
```

### Create Index
```python
result = await client.call_tool("create_index", {
    "index_name": "idx_users_email",
    "table_name": "users",
    "columns": ["email"]
})
```

## Advanced Features

### JSON Support
```python
# JSON operations
await client.call_tool("execute_sql", {
    "query": "SELECT data->>'name' as name FROM users WHERE data->'active' = 'true'",
    "parameters": []
})
```

### Window Functions
```python
await client.call_tool("execute_sql", {
    "query": """
    SELECT id, amount,
           ROW_NUMBER() OVER (ORDER BY amount DESC) as rank
    FROM transactions
    """,
    "parameters": []
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
psycopg2-binary>=2.9.0
```

## Security
- Always use parameterized queries
- Use SSL for remote connections
- Implement connection timeouts
- Enable query logging

## Troubleshooting
- Check PostgreSQL service is running
- Verify credentials
- Check connection limits
- Review logs for detailed errors

## Use Cases
- Complex analytical queries
- Real-time data processing
- JSON data handling
- Advanced analytics
- Enterprise data management
