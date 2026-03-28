# Azure Fabric MCP Server 🏢

## Overview
FastMCP-based server for Microsoft Azure Fabric with 25+ comprehensive tools covering workspaces, warehouses, lakehouses, DDL, DML, SELECT, DCL, and administration operations.

## Features
- **Unified Analytics Platform**: Data warehouse + data lake + analytics
- **Workspace Management**: Create and manage workspace environments
- **Lakehouse Support**: Unified data lake with SQL semantics
- **Warehouse Operations**: Full SQL support with scalability
- **Real-time Analytics**: Power BI integration ready
- **Fine-grained Access**: Role-based permissions
- **Semantic Models**: Business intelligence layer

## Setup & Installation

### Prerequisites
- Python 3.9+
- Microsoft Azure account with Fabric capacity
- Service principal credentials

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export FABRIC_WORKSPACE_ID="your-workspace-id"
export FABRIC_CAPACITY_ID="your-capacity-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-service-principal-id"
export AZURE_CLIENT_SECRET="your-service-principal-secret"
export PORT="7083"
```

### Running
```bash
python server.py
```

## Tools Available (25+)

### Workspace Tools (3)
- `fabric_list_workspaces` - List all workspaces
- `fabric_create_workspace` - Create new workspace
- `fabric_get_workspace_details` - Get workspace configuration

### DDL Tools (8)
- `fabric_create_lakehouse` - Create lakehouse
- `fabric_create_warehouse` - Create warehouse
- `fabric_create_schema` - Create schema
- `fabric_create_table` - Create table with primary keys
- `fabric_drop_table` - Drop table
- `fabric_list_tables` - List tables in schema
- `fabric_describe_table` - Describe table structure
- `fabric_create_view` - Create logical view

### DML Tools (5)
- `fabric_insert_record` - Insert single record
- `fabric_insert_multiple_records` - Bulk insert records
- `fabric_update_records` - Update records
- `fabric_delete_records` - Delete records

### SELECT/Query Tools (8)
- `fabric_query_custom` - Execute custom SQL
- `fabric_select_all` - SELECT all records
- `fabric_select_where` - SELECT with WHERE clause
- `fabric_select_count` - COUNT records
- `fabric_select_aggregate` - Aggregate functions
- `fabric_select_distinct` - Get DISTINCT values
- `fabric_select_grouped` - GROUP BY query
- `fabric_select_ordered` - ORDER BY query
- `fabric_select_join` - JOIN between tables

### DCL Tools (3)
- `fabric_grant_permissions` - Grant workspace access
- `fabric_revoke_permissions` - Revoke workspace access
- `fabric_list_workspace_members` - List members and roles

### Administration Tools (4+)
- `fabric_get_workspace_capacity` - Get capacity usage
- `fabric_get_table_stats` - Get table statistics
- `fabric_list_activities` - List workspace activities
- `fabric_refresh_semantic_model` - Trigger refresh job

## Usage Examples

### Workspace Setup
```python
# Create workspace
await client.call_tool("fabric_create_workspace", {
    "workspace_name": "Analytics Workspace",
    "capacity_id": "your-capacity-id"
})

# Get workspace details
await client.call_tool("fabric_get_workspace_details", {
    "workspace_id": "your-workspace-id"
})
```

### Create Warehouse and Schema
```python
# Create warehouse
await client.call_tool("fabric_create_warehouse", {
    "workspace_id": "your-workspace-id",
    "warehouse_name": "Sales Warehouse"
})

# Create schema
await client.call_tool("fabric_create_schema", {
    "workspace_id": "your-workspace-id",
    "warehouse_id": "your-warehouse-id",
    "schema_name": "sales"
})
```

### Create and Load Data
```python
# Create table
await client.call_tool("fabric_create_table", {
    "workspace_id": "your-workspace-id",
    "warehouse_id": "your-warehouse-id",
    "schema_name": "sales",
    "table_name": "transactions",
    "columns": "id INT, amount DECIMAL(10,2), date DATE",
    "primary_key": "id"
})

# Insert data
await client.call_tool("fabric_insert_multiple_records", {
    "workspace_id": "your-workspace-id",
    "warehouse_id": "your-warehouse-id",
    "schema_name": "sales",
    "table_name": "transactions",
    "records": [
        {"id": 1, "amount": 100.50, "date": "2024-01-15"},
        {"id": 2, "amount": 250.75, "date": "2024-01-16"}
    ]
})
```

### Query Data
```python
# Simple select
await client.call_tool("fabric_select_all", {
    "workspace_id": "your-workspace-id",
    "warehouse_id": "your-warehouse-id",
    "schema_name": "sales",
    "table_name": "transactions",
    "limit": 100
})

# Aggregation
await client.call_tool("fabric_select_aggregate", {
    "workspace_id": "your-workspace-id",
    "warehouse_id": "your-warehouse-id",
    "schema_name": "sales",
    "table_name": "transactions",
    "agg_column": "amount",
    "agg_function": "SUM"
})
```

### Manage Permissions
```python
# Grant permission
await client.call_tool("fabric_grant_permissions", {
    "workspace_id": "your-workspace-id",
    "principal": "analyst@company.com",
    "role": "Viewer"
})

# List members
await client.call_tool("fabric_list_workspace_members", {
    "workspace_id": "your-workspace-id"
})
```

## Best Practices

### Workspace Design
- Create separate workspaces for dev/test/prod
- Assign appropriate capabilities to each workspace
- Use naming conventions for clarity
- Set appropriate member roles

### Schema & Table Design
- Use schemas to organize related tables
- Define primary keys for all tables
- Use appropriate data types
- Create strategic indexes for common queries

### Data Loading
- Use bulk insert for large data loads
- Validate data before loading
- Monitor capacity during large operations
- Create staging tables for ETL

### Query Performance
- Use WHERE clauses to filter early
- Create views for common queries
- Monitor query execution time
- Use appropriate indexes

### Capacity Management
- Monitor capacity usage regularly
- Plan for growth
- Scale capacity based on demand
- Review activities and resource usage

### Security
- Grant minimal required permissions
- Use service principals for automation
- Audit access regularly
- Encrypt sensitive data

## Role-Specific Prompts

- **DBA Operations**: Workspace/warehouse management, schema design, permissions
- **Data Engineer**: Data pipeline design, ETL, data quality
- **Data Analyst**: Data exploration, reporting, analytics

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
azure-identity>=1.13.0
azure-synapse-spark>=0.9.0
```

## Use Cases
- Enterprise data warehousing
- Real-time analytics
- Data lake management
- Business intelligence
- Data science workspaces
- Cross-functional analytics

## Troubleshooting

### Authentication Issues
- Verify AZURE_CLIENT_ID and AZURE_CLIENT_SECRET
- Check service principal has Fabric permissions
- Verify FABRIC_WORKSPACE_ID and FABRIC_CAPACITY_ID
- Check tenant ID is correct

### Performance Issues
- Monitor workspace capacity usage
- Check table statistics
- Review query execution plans
- Optimize schema design

### Data Quality
- Validate data before loading
- Monitor for NULL values
- Track data lineage
- Regular data audits

## Performance Tips
- Create proper primary key constraints
- Use clustering for large tables
- Batch insert operations
- Optimize view definitions
- Monitor workspace capacity

## Ports
- Default: 7083
- Configurable via PORT environment variable
