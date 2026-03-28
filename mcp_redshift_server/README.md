# AWS Redshift MCP Server 🏗️

## Overview
FastMCP-based server for AWS Redshift data warehouse with 28 comprehensive tools covering DDL, DML, SELECT, DCL, and administration operations.

## Features
- **Data Warehouse**: Full OLAP capabilities
- **Distributed Architecture**: DISTKEY and SORTKEY optimization
- **S3 Integration**: COPY from S3 for bulk loading
- **Schema Management**: Multiple schema support
- **Performance Tuning**: VACUUM and ANALYZE operations
- **Access Control**: Fine-grained user permissions
- **Analytics**: Complex aggregations and JOINs

## Setup & Installation

### Prerequisites
- Python 3.9+
- AWS Redshift cluster
- psycopg2 (PostgreSQL driver)

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export REDSHIFT_HOST="your-cluster.redshift.amazonaws.com"
export REDSHIFT_PORT="5439"
export REDSHIFT_USER="awsuser"
export REDSHIFT_PASSWORD="your_password"
export REDSHIFT_DATABASE="dev"
export PORT="7081"
```

### Running
```bash
python server.py
```

## Tools Available (28)

### DDL Tools (8)
- `redshift_create_schema` - Create schema
- `redshift_drop_schema` - Drop schema
- `redshift_list_schemas` - List schemas
- `redshift_create_table` - Create table with DISTKEY/SORTKEY
- `redshift_drop_table` - Drop table
- `redshift_list_tables` - List tables
- `redshift_describe_table` - Describe table structure
- `redshift_alter_table` - Modify table

### DML Tools (5)
- `redshift_insert_record` - Insert single record
- `redshift_insert_multiple_records` - Bulk insert
- `redshift_update_records` - Update records
- `redshift_delete_records` - Delete records
- `redshift_copy_from_s3` - COPY from S3

### SELECT/Query Tools (9)
- `redshift_select_all` - Select all records
- `redshift_select_where` - SELECT with WHERE
- `redshift_select_count` - COUNT records
- `redshift_select_aggregate` - SUM, AVG, MIN, MAX, COUNT
- `redshift_select_distinct` - Get distinct values
- `redshift_select_grouped` - GROUP BY
- `redshift_select_ordered` - ORDER BY
- `redshift_select_join` - JOIN tables
- `redshift_custom_query` - Execute custom SQL

### DCL Tools (3)
- `redshift_grant_permissions` - Grant permissions
- `redshift_revoke_permissions` - Revoke permissions
- `redshift_list_users` - List all users

### Administration Tools (3)
- `redshift_vacuum` - VACUUM table
- `redshift_analyze` - ANALYZE table
- `redshift_get_table_stats` - Get table statistics

## Usage Examples

### Create Schema and Table
```python
# Create schema
await client.call_tool("redshift_create_schema", {
    "schema_name": "analytics"
})

# Create table with distribution and sort keys
await client.call_tool("redshift_create_table", {
    "schema_name": "analytics",
    "table_name": "sales",
    "columns": "id INT, amount DECIMAL(10,2), date DATE",
    "distribution_key": "id",
    "sort_key": "date"
})
```

### Load Data from S3
```python
await client.call_tool("redshift_copy_from_s3", {
    "schema_name": "analytics",
    "table_name": "sales",
    "s3_path": "s3://my-bucket/sales-data/",
    "iam_role": "arn:aws:iam::123456789:role/RedshiftRole"
})
```

### Query Data
```python
await client.call_tool("redshift_select_grouped", {
    "schema_name": "analytics",
    "table_name": "sales",
    "group_by": "date",
    "aggregate_column": "amount",
    "aggregate_function": "SUM"
})
```

### Manage Permissions
```python
await client.call_tool("redshift_grant_permissions", {
    "schema_name": "analytics",
    "table_name": "sales",
    "user": "analyst_user",
    "permissions": ["SELECT", "INSERT"]
})
```

## Best Practices

### Schema Design
- Choose DISTKEY on frequently joined columns
- Use SORTKEY for frequently filtered or range-queried columns
- Minimize data redistribution by aligning DISTKEYs
- Monitor table statistics with unsorted_pct

### Data Loading
- Use COPY command from S3 for bulk loads
- Validate row counts before and after load
- Use appropriate compression (GZIP, LZOP)
- Batch multiple files in S3 prefix

### Performance
- Run VACUUM regularly to reclaim storage
- Run ANALYZE after large data loads
- Monitor query performance in query log
- Use EXPLAIN ANALYZE for query optimization

### Security
- Grant minimal required permissions
- Use IAM roles instead of passwords when possible
- Encrypt data in transit (SSL/TLS)
- Audit user access and permissions

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
psycopg2-binary>=2.9
```

## Use Cases
- Business intelligence dashboards
- Data warehouse OLAP queries
- Historical data analysis
- Cross-functional data sharing
- Large-scale aggregations
- Multi-dimensional analysis

## Troubleshooting

### Connection Issues
- Verify cluster endpoint and port
- Check security group allows inbound on port 5439
- Verify IAM user has correct permissions

### Performance Issues
- Check DISTKEY distribution
- Run ANALYZE to update statistics
- Monitor unsorted_pct, target < 5%
- Review query execution plans

### Data Load Issues
- Validate S3 path format
- Verify IAM role permissions for S3
- Check data format matches table definition
- Review load error table for issues

## Performance Tips
- Use DISTKEY on join columns
- Keep SORTKEY columns minimal
- Batch COPY operations
- Use appropriate table encoding (DELTA, LZO)
- Monitor WLM queue performance

## Ports
- Default: 7081
- Configurable via PORT environment variable
