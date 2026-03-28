# Databricks MCP Server 📊

## Overview
FastMCP-based server for Databricks SQL warehouse operations with support for data analytics and SQL execution.

## Features
- **SQL Warehouse**: Managed SQL compute
- **Schema Management**: Multi-schema support
- **Table Operations**: Full CRUD operations
- **Views**: Create and manage views
- **Analytics**: Advanced SQL queries
- **Data Lake**: Unity Catalog support

## Setup & Installation

### Prerequisites
- Python 3.9+
- Databricks Workspace Access
- PAT Token

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export DATABRICKS_HOSTNAME="your-workspace.cloud.databricks.com"
export DATABRICKS_HTTP_PATH="/sql/1.0/warehouses/warehouse-id"
export DATABRICKS_TOKEN="your_pat_token"
```

### Running
```bash
python server.py
```

## Tools Available

### execute_sql
Execute SQL queries (SELECT, INSERT, UPDATE, DELETE).

### list_schemas
List available schemas.

### list_tables
List tables in schema.

### describe_table
Get table schema information.

### create_table
Create new table.

### insert_data
Insert data into table.

### create_view
Create SQL view.

### run_query_and_fetch
Run query with result limit.

### get_database_info
Get workspace information.

## Usage Examples

### Execute Query
```python
await client.call_tool("execute_sql", {
    "query": "SELECT * FROM my_schema.users WHERE status = 'active'"
})
```

### Create Table
```python
await client.call_tool("create_table", {
    "table_name": "customers",
    "schema": "sales",
    "columns": {
        "id": "INT",
        "name": "STRING",
        "email": "STRING",
        "created": "TIMESTAMP"
    }
})
```

### Insert Data
```python
await client.call_tool("insert_data", {
    "table_name": "customers",
    "schema": "sales",
    "data": {
        "name": "John Doe",
        "email": "john@example.com"
    }
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
databricks-sql-connector>=0.4
```

## Use Cases
- Data warehousing
- Business intelligence
- ETL pipelines
- Data science workflows
- Analytics and reporting
- Machine learning

## Best Practices
- Use warehouse clusters
- Optimize queries
- Manage catalog structure
- Monitor warehouse usage
- Implement proper governance

## Performance Tips
- Use partitioning
- Optimize joins
- Cache frequently used data
- Monitor query execution
