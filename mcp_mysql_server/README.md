# MySQL MCP Server 🐬

## Overview
A FastMCP-based MCP server providing comprehensive MySQL database operations through standardized tools. Execute queries, manage data, and interact with MySQL databases through the Model Context Protocol.

## Features
- **Query Execution**: Execute arbitrary SQL queries with parameterized support
- **Table Management**: List tables, describe schema, manage table structures
- **CRUD Operations**: Create, read, update, delete records efficiently
- **Connection Pooling**: Efficient connection management
- **Error Handling**: Robust error recovery and logging
- **Parameterized Queries**: SQL injection prevention

## Setup & Installation

### Prerequisites
- Python 3.9+
- MySQL 5.7+ or MySQL 8.0+
- Docker (optional)

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
Set environment variables:
```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_password"
export MYSQL_DATABASE="your_database"
export MYSQL_PORT="3306"
```

### Running the Server
```bash
# Stdio transport (default)
python server.py

# With custom settings
MYSQL_HOST=db.example.com MYSQL_USER=admin python server.py
```

## Tools Available

### execute_sql
Execute arbitrary SQL queries with optional parameterization.

**Parameters:**
- `query` (string): SQL query to execute
- `parameters` (array, optional): Query parameters for parameterized queries

**Returns:**
- Success: `{"success": true, "data": [...]}`
- Error: `{"success": false, "error": "..."}`

**Example:**
```python
await client.call_tool("execute_sql", {
    "query": "SELECT * FROM users WHERE age > ? AND status = ?",
    "parameters": [18, "active"]
})
```

### list_tables
List all tables in the configured database.

**Returns:**
```json
{
    "success": true,
    "tables": ["users", "products", "orders"]
}
```

### describe_table
Get detailed structure and column information for a table.

**Parameters:**
- `table_name` (string): Name of the table

**Returns:**
```json
{
    "success": true,
    "columns": [
        {
            "Field": "id",
            "Type": "bigint",
            "Null": "NO",
            "Key": "PRI"
        }
    ]
}
```

### insert_record
Insert a new record into a table.

**Parameters:**
- `table_name` (string): Target table name
- `data` (object): Column-value pairs

**Example:**
```python
await client.call_tool("insert_record", {
    "table_name": "users",
    "data": {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
})
```

### update_record
Update existing records in a table.

**Parameters:**
- `table_name` (string): Target table
- `where_clause` (string): WHERE condition
- `data` (object): Columns to update

**Example:**
```python
await client.call_tool("update_record", {
    "table_name": "users",
    "where_clause": "id = 5",
    "data": {
        "status": "inactive",
        "updated_at": "2024-06-15"
    }
})
```

### delete_record
Delete records from a table.

**Parameters:**
- `table_name` (string): Target table
- `where_clause` (string): WHERE condition

**Example:**
```python
await client.call_tool("delete_record", {
    "table_name": "users",
    "where_clause": "id > 100 AND status = 'inactive'"
})
```

### get_database_stats
Get database statistics including size and table count.

**Returns:**
```json
{
    "success": true,
    "stats": [
        {
            "database_name": "mydb",
            "size_mb": 150.5,
            "table_count": 12
        }
    ]
}
```

## Usage Examples

### Query Data
```python
# Get active users
result = await client.call_tool("execute_sql", {
    "query": "SELECT id, name, email FROM users WHERE status = ? ORDER BY created_at DESC LIMIT 10",
    "parameters": ["active"]
})
```

### Insert Data
```python
# Add new product
result = await client.call_tool("insert_record", {
    "table_name": "products",
    "data": {
        "sku": "PROD001",
        "name": "Widget",
        "price": 29.99,
        "stock": 100
    }
})
```

### Update Data
```python
# Update inventory
result = await client.call_tool("update_record", {
    "table_name": "products",
    "where_clause": "sku = 'PROD001'",
    "data": {
        "price": 24.99,
        "stock": 85
    }
})
```

### Complex Queries
```python
# Join query with aggregation
result = await client.call_tool("execute_sql", {
    "query": """
    SELECT 
        u.name,
        COUNT(o.id) as order_count,
        SUM(o.total) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.created_at > DATE_SUB(NOW(), INTERVAL 1 YEAR)
    GROUP BY u.id
    HAVING COUNT(o.id) > 0
    ORDER BY total_spent DESC
    """,
    "parameters": []
})
```

## Advanced Features

### Transaction Support
```sql
START TRANSACTION;
INSERT INTO audit_log (action, details) VALUES ('user_created', 'John Doe');
UPDATE users SET active_users = active_users + 1;
COMMIT;
```

### Performance Optimization
```python
# Batch inserts
query = """
INSERT INTO logs (timestamp, level, message) VALUES 
(NOW(), 'INFO', ?),
(NOW(), 'WARN', ?),
(NOW(), 'ERROR', ?)
"""
```

### Index Management
```python
# Check indexes
result = await client.call_tool("execute_sql", {
    "query": "SHOW INDEXES FROM users"
})

# Create index
result = await client.call_tool("execute_sql", {
    "query": "CREATE INDEX idx_email ON users(email)"
})
```

## Security Best Practices

### Parameterized Queries
Always use parameters to prevent SQL injection:
```python
# ✅ Good - Safe
await client.call_tool("execute_sql", {
    "query": "SELECT * FROM users WHERE email = ?",
    "parameters": [user_email]
})

# ❌ Bad - SQL Injection Risk
await client.call_tool("execute_sql", {
    "query": f"SELECT * FROM users WHERE email = '{user_email}'"
})
```

### Connection Security
```bash
# Use SSL/TLS
export MYSQL_SSL="true"
export MYSQL_SSL_VERIFY="true"
```

### Access Control
```sql
-- Create restricted user
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON mydb.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
```

## Error Handling

The server provides comprehensive error handling:

```python
result = await client.call_tool("execute_sql", {
    "query": "SELECT * FROM non_existent_table"
})

if not result["success"]:
    print(f"Error: {result['error']}")
    # Handle: "Table 'mydb.non_existent_table' doesn't exist"
```

## Testing

### Unit Tests
```python
import pytest

@pytest.mark.asyncio
async def test_list_tables():
    result = await client.call_tool("list_tables")
    assert result["success"] == True
    assert len(result["tables"]) > 0

@pytest.mark.asyncio
async def test_execute_sql():
    result = await client.call_tool("execute_sql", {
        "query": "SELECT COUNT(*) as count FROM users"
    })
    assert result["success"] == True
```

## Requirements
See `requirements.txt`:
```
fastmcp>=0.1.0
mcp>=0.1.0
mysql-connector-python>=8.0
```

## Configuration Options

### Environment Variables
```bash
MYSQL_HOST              # Database host (default: localhost)
MYSQL_PORT              # Database port (default: 3306)
MYSQL_USER              # Database user
MYSQL_PASSWORD          # Database password
MYSQL_DATABASE          # Database name
```

### Connection Settings
```python
# Adjust in server.py
config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "password",
    "database": "test",
    "autocommit": False,
    "use_unicode": True,
    "charset": "utf8mb4"
}
```

## Performance Tips
1. Use indexes on frequently queried columns
2. Implement connection pooling
3. Use parameterized queries
4. Monitor slow query log
5. Batch operations when possible
6. Use LIMIT for large result sets
7. Optimize JOIN queries

## Troubleshooting

### Connection Issues
```python
# Check connection
result = await client.call_tool("get_database_stats")
if not result["success"]:
    print(f"Connection failed: {result['error']}")
```

### Query Timeouts
```bash
# Increase timeout in MySQL
set global max_connections=1000;
set global wait_timeout=600;
```

### Character Encoding
```bash
# Use UTF-8
export MYSQL_CHARSET="utf8mb4"
```

## Use Cases
- Data analytics and reporting
- Operational database queries
- Batch data processing
- Health monitoring
- Admin operations
- Integration with AI agents

## Dependencies
- fastmcp
- mcp
- mysql-connector-python>=8.0.23

## Future Enhancements
- [ ] Connection pooling optimization
- [ ] Query result caching
- [ ] Stored procedure support
- [ ] View management
- [ ] Backup/restore utilities
- [ ] Replication monitoring
