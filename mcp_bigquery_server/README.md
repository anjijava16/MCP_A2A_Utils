# Google BigQuery MCP Server 🏢

## Overview
FastMCP-based server for Google BigQuery data warehouse with 25+ comprehensive tools covering DDL, DML, SELECT, DCL, and administration operations.

## Features
- **Cloud Data Warehouse**: Serverless OLAP analytics
- **Partitioning & Clustering**: Performance optimization
- **Logical Views**: Virtual table support
- **Cost Estimation**: Dry-run query analysis
- **Job Management**: Track and monitor queries
- **Dataset Management**: Fine-grained access control
- **Scalability**: Handle petabyte-scale data

## Setup & Installation

### Prerequisites
- Python 3.9+
- Google Cloud Project with BigQuery enabled
- Service account credentials

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export GCP_PROJECT_ID="your-project-id"
export BIGQUERY_DATASET_DEFAULT="default_dataset"
export BIGQUERY_LOCATION="US"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
export PORT="7082"
```

### Running
```bash
python server.py
```

## Tools Available (25+)

### DDL Tools (7)
- `bigquery_create_dataset` - Create dataset with location
- `bigquery_drop_dataset` - Drop dataset
- `bigquery_list_datasets` - List all datasets
- `bigquery_create_table` - Create table with clustering/partitioning
- `bigquery_drop_table` - Drop table
- `bigquery_list_tables` - List tables in dataset
- `bigquery_describe_table` - Describe table schema
- `bigquery_create_view` - Create logical view

### DML Tools (2)
- `bigquery_insert_record` - Insert single record
- `bigquery_insert_multiple_records` - Bulk insert records

### SELECT/Query Tools (10)
- `bigquery_query_custom` - Execute custom SQL
- `bigquery_select_all` - SELECT all records
- `bigquery_select_where` - SELECT with WHERE clause
- `bigquery_select_count` - COUNT records
- `bigquery_select_aggregate` - Aggregate functions (SUM, AVG, MIN, MAX)
- `bigquery_select_distinct` - Get DISTINCT values
- `bigquery_select_grouped` - GROUP BY query
- `bigquery_select_ordered` - ORDER BY query
- `bigquery_select_join` - JOIN query between tables

### DCL Tools (2)
- `bigquery_grant_dataset_access` - Grant access to dataset
- `bigquery_revoke_dataset_access` - Revoke dataset access

### Administration Tools (4+)
- `bigquery_get_job_stats` - Get table statistics
- `bigquery_list_recent_jobs` - List recent query jobs
- `bigquery_estimate_query_cost` - Estimate query cost with dry-run
- `bigquery_get_table_size` - Get table size and row count

## Usage Examples

### Create Dataset and Table
```python
# Create dataset
await client.call_tool("bigquery_create_dataset", {
    "dataset_id": "analytics",
    "location": "US",
    "description": "Analytics dataset"
})

# Create partitioned table
await client.call_tool("bigquery_create_table", {
    "dataset_id": "analytics",
    "table_id": "events",
    "schema": [
        {"name": "event_id", "type": "STRING"},
        {"name": "event_date", "type": "DATE"},
        {"name": "event_value", "type": "FLOAT64"}
    ],
    "partitioning": "event_date",
    "clustering_fields": ["event_id"]
})
```

### Load Data
```python
# Insert single record
await client.call_tool("bigquery_insert_record", {
    "dataset_id": "analytics",
    "table_id": "events",
    "record": {
        "event_id": "evt_001",
        "event_date": "2024-01-15",
        "event_value": 42.5
    }
})

# Bulk insert
await client.call_tool("bigquery_insert_multiple_records", {
    "dataset_id": "analytics",
    "table_id": "events",
    "records": [
        {"event_id": "evt_002", "event_date": "2024-01-16", "event_value": 35.0},
        {"event_id": "evt_003", "event_date": "2024-01-17", "event_value": 50.2}
    ]
})
```

### Query Data
```python
# Simple select
await client.call_tool("bigquery_select_all", {
    "dataset_id": "analytics",
    "table_id": "events",
    "limit": 100
})

# Aggregation
await client.call_tool("bigquery_select_aggregate", {
    "dataset_id": "analytics",
    "table_id": "events",
    "agg_column": "event_value",
    "agg_function": "SUM"
})

# Custom query
await client.call_tool("bigquery_query_custom", {
    "sql": "SELECT event_date, COUNT(*) as count FROM analytics.events GROUP BY event_date"
})
```

### Cost Estimation
```python
await client.call_tool("bigquery_estimate_query_cost", {
    "sql": "SELECT * FROM analytics.events WHERE event_date = '2024-01-15'"
})
```

## Best Practices

### Schema Design
- Use appropriate data types (FLOAT64 for decimals, not strings)
- Define clustering fields for frequently filtered columns
- Use partitioning for time-series data on DATE/TIMESTAMP columns
- Keep clustering key cardinality moderate (< 100k distinct values)

### Data Loading
- Use batch inserts for better performance
- Load data into staging tables first
- Validate row counts before and after load
- Monitor job costs with dry-run before large queries

### Query Optimization
- Filter data early (push down predicates)
- Use LIMIT in development queries
- Avoid SELECT * in production
- Use approximate aggregation functions for estimates
- Always estimate query costs before running

### Cost Management
- Use partitioning and clustering to limit data scanned
- Use dry-run (estimate_query_cost) before running queries
- Use slots for predictable workloads
- Archive old data to Cloud Storage

### Security
- Use service accounts instead of user credentials
- Grant minimal required roles
- Use IAM for dataset-level access control
- Audit access logs in Cloud Logging

## Role-Specific Prompts

- **DBA Operations**: Dataset/table management, access control, maintenance
- **Data Engineer**: Data loading, pipeline design, ETL validation
- **Data Analyst**: Data exploration, ad-hoc queries, analytics

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
google-cloud-bigquery>=3.0.0
```

## Use Cases
- Event streaming analytics
- User behavior analysis
- Business intelligence dashboards
- Real-time metrics computation
- Data warehouse consolidation
- Cross-regional analytics

## Troubleshooting

### Authentication Issues
- Verify GOOGLE_APPLICATION_CREDENTIALS points to service account JSON
- Check service account has BigQuery Editor role
- Verify GCP_PROJECT_ID is correct

### Query Performance
- Check if table is partitioned/clustered appropriately
- Monitor query execution time in BigQuery UI
- Use EXPLAIN to analyze query plan
- Consider materialized views for repeated aggregations

### Data Quality
- Validate schema before inserts
- Check for NULL values in key columns
- Monitor record counts during loads
- Use data validation queries frequently

## Cost Optimization Tips
- Always use dry-run before running large queries
- Partition by DATE for time-series data
- Cluster by frequently-queried columns
- Use incremental loading instead of full refreshes
- Archive data to Cloud Storage after 90 days

## Ports
- Default: 7082
- Configurable via PORT environment variable
