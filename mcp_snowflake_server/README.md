# Snowflake MCP Server ❄️

## Overview

Comprehensive Model Context Protocol (MCP) server for **Snowflake**, the cloud-native data platform. This server provides 28 powerful tools for warehouse, database, schema, table, and query management through a standardized interface.

## Architecture & Features

- **Cloud-Native**: Built for Snowflake's architecture with warehouse separation
- **Comprehensive**: 28 tools covering all major Snowflake operations
- **SSE Transport**: Server-Sent Events for reliable communication (Port 7098)
- **Role-Based**: 3 role-based prompts (DBA, Data Engineer, Analytics Engineer)
- **Async**: FastMCP with async/await support
- **Error Handling**: Structured error responses with detailed logging

## Tool Categories

### Warehouse Management (6 tools)
- `create_warehouse` - Create new warehouse with size and auto-suspend settings
- `list_warehouses` - List all warehouses in account
- `drop_warehouse` - Remove warehouse
- `suspend_warehouse` - Pause warehouse operations
- `resume_warehouse` - Restart warehouse
- `scale_warehouse` - Change warehouse size dynamically

### Database & Schema Operations (4 tools)
- `create_database` - Create new database
- `list_databases` - List all databases
- `create_schema` - Create schema in database
- `list_schemas` - List schemas in database

### Table Operations (6 tools)
- `create_table` - Create table with column definitions
- `list_tables` - List tables in schema
- `describe_table` - Get table structure and columns
- `drop_table` - Remove table
- `add_column` - Add column to existing table
- Supports timestamps, numeric, string, variant types

### DML Operations (4 tools)
- `insert_rows` - Insert data from values
- `update_rows` - Update rows with SET and WHERE clauses
- `delete_rows` - Delete rows by condition
- `bulk_insert_from_stage` - Load from Snowflake Stage (S3/Azure/GCS)

### Query Operations (5 tools)
- `execute_query` - Run custom SQL queries
- `select_all` - Retrieve rows with limit
- `count_rows` - Get row count for table
- `explain_query` - Analyze query execution plan
- Return structured results for programmatic access

### View Operations (2 tools)
- `create_view` - Create view from query
- `drop_view` - Remove view

### Access Control (3 tools)
- `create_role` - Create new role
- `grant_privilege` - Grant permission to role
- `revoke_privilege` - Remove permission from role

### Admin Operations (3 tools)
- `get_account_info` - Current account, user, warehouse
- `list_queries` - Show recent query execution history
- `show_parameters` - Display warehouse/account parameters

## Environment Setup

Required environment variables:

```bash
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=xy12345  # Account ID without .snowflakecomputing.com
SNOWFLAKE_WAREHOUSE=compute_wh
SNOWFLAKE_DATABASE=analytics
SNOWFLAKE_SCHEMA=public
```

## Installation

```bash
pip install snowflake-connector-python fastmcp
```

## Running the Server

```bash
python mcp_snowflake_server/server.py
```

Server will start on `http://0.0.0.0:7098` with SSE transport.

## Usage Examples

### Create & Configure Warehouse
```python
# Create warehouse
await create_warehouse("analysis_wh", "SMALL", auto_suspend=30)

# List warehouses
warehouses = await list_warehouses()

# Scale up for heavy workload
await scale_warehouse("analysis_wh", "XLARGE")

# Suspend when done
await suspend_warehouse("analysis_wh")
```

### Database & Table Management
```python
# Create database and schema
await create_database("raw_data")
await create_schema("raw_data", "staging")

# Create table
columns = [
    {"name": "id", "type": "NUMBER"},
    {"name": "name", "type": "VARCHAR"},
    {"name": "created_at", "type": "TIMESTAMP"}
]
await create_table("raw_data", "staging", "customers", columns)

# Add column
await add_column("raw_data", "staging", "customers", "email", "VARCHAR")
```

### Data Loading & Querying
```python
# Insert data
rows = [
    {"id": 1, "name": "Alice", "created_at": "2024-01-01"},
    {"id": 2, "name": "Bob", "created_at": "2024-01-02"}
]
await insert_rows("raw_data", "staging", "customers", rows)

# Query
result = await select_all("raw_data", "staging", "customers")

# Count
count = await count_rows("raw_data", "staging", "customers")

# Bulk load from stage
await bulk_insert_from_stage("raw_data", "staging", "customers", "@my_s3_stage")
```

### Access Control
```python
# Create analytics role
await create_role("analytics_viewer")

# Grant permissions
await grant_privilege("analytics_viewer", "SELECT", "TABLE", "raw_data.staging.customers")

# Revoke if needed
await revoke_privilege("analytics_viewer", "SELECT", "TABLE", "raw_data.staging.customers")
```

## Role-Based Prompts

### Data Warehouse Administrator
Manage Snowflake infrastructure, warehouse capacity, scaling, and optimization. Focus on performance, cost, and reliability.

### Data Engineer
Build data pipelines and ETL processes. Design schemas, manage data loading, and optimize transformations for scale.

### Analytics Engineer
Create analytics-ready datasets. Design dimensional models, create BI views, maintain data quality and documentation.

## Performance Notes

- **Warehouse Sizing**: Start with XSMALL, scale up as needed
- **Auto-Suspend**: Set to 5-15 minutes to save cost (default 10)
- **Bulk Loading**: Use `bulk_insert_from_stage` for large datasets (>100k rows)
- **Caching**: Snowflake caches query results automatically
- **Clustering**: Use for large tables (>100GB) with common join/filter columns

## Error Handling

All tools return structured responses:

```python
{
    "success": true/false,
    "message": "...",
    "error": "..." # Only if success=false
}
```

Check `success` field before using results.

## Pricing & Cost Optimization

- **Compute**: $2-4/credit/region (1 credit per 60 seconds per warehouse)
- **Storage**: $20-40/TB/month
- **Data Transfer**: $0.02/GB between regions

Optimize by:
1. Suspending unused warehouses
2. Right-sizing warehouse capacity
3. Using clustering keys for large tables
4. Pruning old data with time-based partitions

## Integration with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "snowflake": {
      "command": "python",
      "args": ["mcp_snowflake_server/server.py"],
      "env": {
        "SNOWFLAKE_USER": "your_user",
        "SNOWFLAKE_PASSWORD": "your_password",
        "SNOWFLAKE_ACCOUNT": "xy12345",
        "SNOWFLAKE_WAREHOUSE": "compute_wh"
      }
    }
  }
}
```

## Support & Resources

- [Snowflake Docs](https://docs.snowflake.com)
- [Snowflake Connector Python](https://github.com/snowflakedb/snowflake-connector-python)
- [Snowflake SQL Reference](https://docs.snowflake.com/en/sql-reference)

---

**Port**: 7098 | **Type**: Cloud Data Platform | **Tools**: 28 | **Updated**: 2024
