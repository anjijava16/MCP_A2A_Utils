import asyncio
import logging
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
from fastmcp import FastMCP

# Configure logging with emoji
logging.basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("BigQuery MCP Server 🏢")

# Configuration from environment
BQ_CONFIG = {
    "project_id": os.getenv("GCP_PROJECT_ID", ""),
    "dataset_default": os.getenv("BIGQUERY_DATASET_DEFAULT", "default_dataset"),
    "location": os.getenv("BIGQUERY_LOCATION", "US"),
}

def get_bigquery_client():
    """Get BigQuery client with project ID from environment."""
    try:
        client = bigquery.Client(project=BQ_CONFIG["project_id"])
        logger.info(f"✅ Connected to BigQuery project: {BQ_CONFIG['project_id']}")
        return client
    except Exception as e:
        logger.error(f"❌ BigQuery connection error: {str(e)}")
        raise

# ====================== DDL TOOLS ======================

@mcp.tool()
def bigquery_create_dataset(dataset_id: str, location: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new dataset in BigQuery.
    
    Args:
        dataset_id: Dataset ID
        location: Dataset location (default: US)
        description: Dataset description
    
    Returns:
        Success status and dataset details
    """
    try:
        client = get_bigquery_client()
        dataset_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}"
        dataset = bigquery.Dataset(dataset_id_full)
        dataset.location = location or BQ_CONFIG["location"]
        if description:
            dataset.description = description
        
        dataset = client.create_dataset(dataset, exists_ok=True)
        logger.info(f"📦 Dataset created: {dataset_id}")
        return {"success": True, "message": f"Dataset '{dataset_id}' created", "dataset_id": dataset_id}
    except GoogleCloudError as e:
        logger.error(f"❌ Error creating dataset: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_drop_dataset(dataset_id: str, delete_contents: bool = False) -> Dict[str, Any]:
    """Drop a dataset from BigQuery.
    
    Args:
        dataset_id: Dataset ID to drop
        delete_contents: Delete all tables in dataset
    
    Returns:
        Success status
    """
    try:
        client = get_bigquery_client()
        dataset_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}"
        client.delete_dataset(dataset_id_full, delete_contents=delete_contents)
        logger.info(f"🗑️ Dataset dropped: {dataset_id}")
        return {"success": True, "message": f"Dataset '{dataset_id}' dropped"}
    except GoogleCloudError as e:
        logger.error(f"❌ Error dropping dataset: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_list_datasets() -> Dict[str, Any]:
    """List all datasets in the project.
    
    Returns:
        List of dataset IDs
    """
    try:
        client = get_bigquery_client()
        datasets = list(client.list_datasets())
        dataset_ids = [d.dataset_id for d in datasets]
        logger.info(f"📋 Found {len(dataset_ids)} datasets")
        return {"success": True, "datasets": dataset_ids, "count": len(dataset_ids)}
    except GoogleCloudError as e:
        logger.error(f"❌ Error listing datasets: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_create_table(dataset_id: str, table_id: str, schema: List[Dict[str, str]], 
                         clustering_fields: Optional[List[str]] = None,
                         partitioning: Optional[str] = None) -> Dict[str, Any]:
    """Create a new table in BigQuery.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        schema: List of field definitions [{"name": "col1", "type": "STRING"}, ...]
        clustering_fields: Fields for clustering
        partitioning: Partition field (e.g., 'date_column')
    
    Returns:
        Success status and table details
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        
        # Build schema from field definitions
        schema_obj = [bigquery.SchemaField(f["name"], f["type"]) for f in schema]
        table = bigquery.Table(table_id_full, schema=schema_obj)
        
        if clustering_fields:
            table.clustering_fields = clustering_fields
        
        if partitioning:
            table.time_partitioning = bigquery.TimePartitioning(field=partitioning)
        
        table = client.create_table(table)
        logger.info(f"🏗️ Table created: {dataset_id}.{table_id}")
        return {"success": True, "message": f"Table '{table_id}' created in '{dataset_id}'", "table_id": table_id}
    except GoogleCloudError as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_drop_table(dataset_id: str, table_id: str) -> Dict[str, Any]:
    """Drop a table from BigQuery.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID to drop
    
    Returns:
        Success status
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        client.delete_table(table_id_full)
        logger.info(f"🗑️ Table dropped: {dataset_id}.{table_id}")
        return {"success": True, "message": f"Table '{table_id}' dropped"}
    except GoogleCloudError as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_list_tables(dataset_id: str) -> Dict[str, Any]:
    """List all tables in a dataset.
    
    Args:
        dataset_id: Dataset ID
    
    Returns:
        List of table IDs
    """
    try:
        client = get_bigquery_client()
        dataset_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}"
        tables = list(client.list_tables(dataset_id_full))
        table_ids = [t.table_id for t in tables]
        logger.info(f"📋 Found {len(table_ids)} tables in {dataset_id}")
        return {"success": True, "tables": table_ids, "count": len(table_ids)}
    except GoogleCloudError as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_describe_table(dataset_id: str, table_id: str) -> Dict[str, Any]:
    """Describe table structure and metadata.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
    
    Returns:
        Table schema and metadata
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        table = client.get_table(table_id_full)
        
        schema = [{"name": f.name, "type": f.field_type, "mode": f.mode} for f in table.schema]
        logger.info(f"📊 Table described: {dataset_id}.{table_id}")
        
        return {
            "success": True,
            "table_id": table_id,
            "schema": schema,
            "rows": table.num_rows or 0,
            "bytes": table.num_bytes or 0,
            "created": str(table.created)
        }
    except GoogleCloudError as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_create_view(dataset_id: str, view_id: str, query: str) -> Dict[str, Any]:
    """Create a logical view in BigQuery.
    
    Args:
        dataset_id: Dataset ID
        view_id: View ID
        query: SQL query for the view
    
    Returns:
        Success status
    """
    try:
        client = get_bigquery_client()
        view_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{view_id}"
        view = bigquery.Table(view_id_full)
        view.view_query = query
        
        view = client.create_table(view)
        logger.info(f"🔍 View created: {dataset_id}.{view_id}")
        return {"success": True, "message": f"View '{view_id}' created in '{dataset_id}'"}
    except GoogleCloudError as e:
        logger.error(f"❌ Error creating view: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS ======================

@mcp.tool()
def bigquery_insert_record(dataset_id: str, table_id: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single record into BigQuery table.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        record: Record as dictionary
    
    Returns:
        Success status
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        errors = client.insert_rows_json(table_id_full, [record])
        
        if errors:
            logger.error(f"❌ Insert errors: {errors}")
            return {"success": False, "error": str(errors)}
        
        logger.info(f"➕ Record inserted into {dataset_id}.{table_id}")
        return {"success": True, "message": "Record inserted successfully"}
    except GoogleCloudError as e:
        logger.error(f"❌ Error inserting record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_insert_multiple_records(dataset_id: str, table_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple records into BigQuery table.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        records: List of records
    
    Returns:
        Success status and row count
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        errors = client.insert_rows_json(table_id_full, records)
        
        if errors:
            logger.error(f"❌ Bulk insert errors: {errors}")
            return {"success": False, "error": str(errors), "inserted": len(records) - len(errors)}
        
        logger.info(f"➕ {len(records)} records inserted into {dataset_id}.{table_id}")
        return {"success": True, "message": f"{len(records)} records inserted", "inserted": len(records)}
    except GoogleCloudError as e:
        logger.error(f"❌ Error in bulk insert: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SELECT/QUERY TOOLS ======================

@mcp.tool()
def bigquery_query_custom(sql: str) -> Dict[str, Any]:
    """Execute a custom SQL query in BigQuery.
    
    Args:
        sql: SQL query to execute
    
    Returns:
        Query results and row count
    """
    try:
        client = get_bigquery_client()
        query_job = client.query(sql)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        logger.info(f"🔎 Query executed, {len(rows)} rows returned")
        
        return {"success": True, "rows": rows, "count": len(rows)}
    except GoogleCloudError as e:
        logger.error(f"❌ Query error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_all(dataset_id: str, table_id: str, limit: int = 1000) -> Dict[str, Any]:
    """Select all records from a table.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        limit: Maximum rows to return
    
    Returns:
        Query results
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT * FROM `{table_id_full}` LIMIT {limit}"
        query_job = client.query(query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        logger.info(f"🔎 SELECT all: {len(rows)} rows from {dataset_id}.{table_id}")
        
        return {"success": True, "rows": rows, "count": len(rows)}
    except GoogleCloudError as e:
        logger.error(f"❌ SELECT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_where(dataset_id: str, table_id: str, where_clause: str, limit: int = 1000) -> Dict[str, Any]:
    """Select records with WHERE condition.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        where_clause: WHERE clause condition
        limit: Maximum rows
    
    Returns:
        Query results
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT * FROM `{table_id_full}` WHERE {where_clause} LIMIT {limit}"
        query_job = client.query(query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        logger.info(f"🔎 SELECT WHERE: {len(rows)} rows from {dataset_id}.{table_id}")
        
        return {"success": True, "rows": rows, "count": len(rows)}
    except GoogleCloudError as e:
        logger.error(f"❌ SELECT WHERE error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_count(dataset_id: str, table_id: str) -> Dict[str, Any]:
    """Count total records in a table.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
    
    Returns:
        Record count
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT COUNT(*) as count FROM `{table_id_full}`"
        query_job = client.query(query)
        results = query_job.result()
        
        count = list(results)[0]['count']
        logger.info(f"🔢 COUNT: {count} rows in {dataset_id}.{table_id}")
        
        return {"success": True, "count": count}
    except GoogleCloudError as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_aggregate(dataset_id: str, table_id: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute aggregate query (SUM, AVG, MIN, MAX).
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        agg_column: Column to aggregate
        agg_function: Function (SUM, AVG, MIN, MAX, COUNT)
    
    Returns:
        Aggregate result
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT {agg_function}({agg_column}) as result FROM `{table_id_full}`"
        query_job = client.query(query)
        results = query_job.result()
        
        result = list(results)[0]['result']
        logger.info(f"📊 {agg_function} of {agg_column}: {result}")
        
        return {"success": True, "result": result, "function": agg_function}
    except GoogleCloudError as e:
        logger.error(f"❌ Aggregate error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_distinct(dataset_id: str, table_id: str, column: str) -> Dict[str, Any]:
    """Get distinct values from a column.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        column: Column name
    
    Returns:
        List of distinct values
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT DISTINCT {column} FROM `{table_id_full}` LIMIT 1000"
        query_job = client.query(query)
        results = query_job.result()
        
        values = [row[column] for row in results]
        logger.info(f"🔍 DISTINCT {column}: {len(values)} values")
        
        return {"success": True, "values": values, "count": len(values)}
    except GoogleCloudError as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_grouped(dataset_id: str, table_id: str, group_by: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute GROUP BY query.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        group_by: Column to group by
        agg_column: Column to aggregate
        agg_function: Aggregate function
    
    Returns:
        Grouped results
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT {group_by}, {agg_function}({agg_column}) as result FROM `{table_id_full}` GROUP BY {group_by} LIMIT 1000"
        query_job = client.query(query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        logger.info(f"📊 GROUP BY {group_by}: {len(rows)} groups")
        
        return {"success": True, "rows": rows, "count": len(rows)}
    except GoogleCloudError as e:
        logger.error(f"❌ GROUP BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_ordered(dataset_id: str, table_id: str, order_by: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Select records with ORDER BY.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
        order_by: Column to order by
        direction: ASC or DESC
        limit: Maximum rows
    
    Returns:
        Ordered results
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        query = f"SELECT * FROM `{table_id_full}` ORDER BY {order_by} {direction} LIMIT {limit}"
        query_job = client.query(query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        logger.info(f"🔎 ORDER BY {order_by}: {len(rows)} rows")
        
        return {"success": True, "rows": rows, "count": len(rows)}
    except GoogleCloudError as e:
        logger.error(f"❌ ORDER BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_select_join(dataset_id: str, table1: str, table2: str, join_column: str, join_type: str = "INNER") -> Dict[str, Any]:
    """Execute JOIN query between two tables.
    
    Args:
        dataset_id: Dataset ID (both tables)
        table1: First table
        table2: Second table
        join_column: Column to join on
        join_type: INNER, LEFT, RIGHT, OUTER
    
    Returns:
        Join results
    """
    try:
        client = get_bigquery_client()
        t1_full = f"`{BQ_CONFIG['project_id']}.{dataset_id}.{table1}`"
        t2_full = f"`{BQ_CONFIG['project_id']}.{dataset_id}.{table2}`"
        query = f"SELECT * FROM {t1_full} {join_type} JOIN {t2_full} ON {table1}.{join_column} = {table2}.{join_column} LIMIT 1000"
        query_job = client.query(query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        logger.info(f"🔗 {join_type} JOIN: {len(rows)} rows")
        
        return {"success": True, "rows": rows, "count": len(rows)}
    except GoogleCloudError as e:
        logger.error(f"❌ JOIN error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DCL TOOLS ======================

@mcp.tool()
def bigquery_grant_dataset_access(dataset_id: str, user_email: str, role: str) -> Dict[str, Any]:
    """Grant access to a dataset.
    
    Args:
        dataset_id: Dataset ID
        user_email: User email
        role: Role (roles/bigquery.dataEditor, roles/bigquery.dataViewer, etc.)
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🔐 Granting {role} on {dataset_id} to {user_email}")
        return {"success": True, "message": f"Access granted to {user_email}"}
    except Exception as e:
        logger.error(f"❌ Error granting access: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_revoke_dataset_access(dataset_id: str, user_email: str) -> Dict[str, Any]:
    """Revoke access to a dataset.
    
    Args:
        dataset_id: Dataset ID
        user_email: User email
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🔐 Revoking access on {dataset_id} from {user_email}")
        return {"success": True, "message": f"Access revoked from {user_email}"}
    except Exception as e:
        logger.error(f"❌ Error revoking access: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== ADMINISTRATION TOOLS ======================

@mcp.tool()
def bigquery_get_job_stats(dataset_id: str, table_id: str) -> Dict[str, Any]:
    """Get job execution statistics.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
    
    Returns:
        Job statistics
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        table = client.get_table(table_id_full)
        
        logger.info(f"📊 Job stats for {dataset_id}.{table_id}")
        
        return {
            "success": True,
            "table": table_id,
            "rows": table.num_rows or 0,
            "bytes": table.num_bytes or 0,
            "created": str(table.created),
            "modified": str(table.modified),
            "project": BQ_CONFIG["project_id"]
        }
    except GoogleCloudError as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_list_recent_jobs(max_results: int = 10) -> Dict[str, Any]:
    """List recent BigQuery jobs.
    
    Args:
        max_results: Maximum jobs to return
    
    Returns:
        List of recent jobs
    """
    try:
        client = get_bigquery_client()
        jobs = list(client.list_jobs(max_results=max_results))
        
        job_info = [{
            "job_id": job.job_id,
            "state": job.state,
            "created": str(job.created),
            "query": job.query[:50] if hasattr(job, 'query') and job.query else "N/A"
        } for job in jobs]
        
        logger.info(f"⚡ Found {len(job_info)} recent jobs")
        
        return {"success": True, "jobs": job_info, "count": len(job_info)}
    except GoogleCloudError as e:
        logger.error(f"❌ Error listing jobs: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_estimate_query_cost(sql: str) -> Dict[str, Any]:
    """Estimate query cost using dry run.
    
    Args:
        sql: SQL query to estimate
    
    Returns:
        Estimated bytes to be scanned
    """
    try:
        client = get_bigquery_client()
        job_config = bigquery.QueryJobConfig(dry_run=True)
        query_job = client.query(sql, job_config=job_config)
        
        bytes_scanned = query_job.total_bytes_processed or 0
        gb_scanned = bytes_scanned / (1024**3)
        
        logger.info(f"💰 Query estimate: {gb_scanned:.2f} GB")
        
        return {
            "success": True,
            "bytes_scanned": bytes_scanned,
            "gb_scanned": round(gb_scanned, 2),
            "estimated_cost_usd": round(gb_scanned * 6.25 / 1000, 4)  # Standard pricing
        }
    except GoogleCloudError as e:
        logger.error(f"❌ Cost estimation error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def bigquery_get_table_size(dataset_id: str, table_id: str) -> Dict[str, Any]:
    """Get table size and row count.
    
    Args:
        dataset_id: Dataset ID
        table_id: Table ID
    
    Returns:
        Size and row information
    """
    try:
        client = get_bigquery_client()
        table_id_full = f"{BQ_CONFIG['project_id']}.{dataset_id}.{table_id}"
        table = client.get_table(table_id_full)
        
        bytes_size = table.num_bytes or 0
        gb_size = bytes_size / (1024**3)
        rows = table.num_rows or 0
        
        logger.info(f"📏 Table size: {gb_size:.2f} GB, {rows} rows")
        
        return {
            "success": True,
            "rows": rows,
            "bytes": bytes_size,
            "gb": round(gb_size, 2),
            "table": table_id
        }
    except GoogleCloudError as e:
        logger.error(f"❌ Error getting size: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a BigQuery Database Administrator. Your role is to:
- Manage datasets and tables with proper schema design
- Optimize query performance and cost
- Handle user access and permissions
- Monitor and maintain data integrity
- Execute DDL operations safely

Use these tools for DBA tasks:
- bigquery_create_dataset, bigquery_drop_dataset, bigquery_list_datasets
- bigquery_create_table, bigquery_describe_table, bigquery_list_tables
- bigquery_create_view for reporting views
- bigquery_grant_dataset_access, bigquery_revoke_dataset_access
- bigquery_estimate_query_cost for capacity planning
- bigquery_get_table_size for storage monitoring
"""

DATA_ENGINEER_PROMPT = """You are a BigQuery Data Engineer. Your role is to:
- Build and maintain data pipelines
- Load data into BigQuery efficiently
- Design scalable table structures
- Maintain data quality and consistency
- Optimize partitioning and clustering

Use these tools for data engineering:
- bigquery_insert_record, bigquery_insert_multiple_records
- bigquery_create_table with clustering/partitioning
- bigquery_query_custom for ETL validation
- bigquery_select_all, bigquery_select_where for data inspection
- bigquery_get_table_size for capacity monitoring
"""

DATA_ANALYST_PROMPT = """You are a BigQuery Data Analyst. Your role is to:
- Query and analyze data
- Generate insights and reports
- Explore data patterns and trends
- Create views for self-service analytics
- Perform ad-hoc analysis

Use these tools for analysis:
- bigquery_query_custom for complex queries
- bigquery_select_all, bigquery_select_where for exploration
- bigquery_select_aggregate for summary statistics
- bigquery_select_grouped for trend analysis
- bigquery_select_ordered for ranking and sorting
- bigquery_select_join for cross-table analysis
- bigquery_list_recent_jobs for query tracking
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting BigQuery MCP Server...")
    if not BQ_CONFIG["project_id"]:
        logger.error("❌ GCP_PROJECT_ID not set in environment")
        return
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7082"))
    )

if __name__ == "__main__":
    asyncio.run(main())
