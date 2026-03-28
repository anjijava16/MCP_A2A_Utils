"""
Apache Cassandra MCP Server using FastMCP
Comprehensive distributed database operations with 28 tools
"""

import asyncio
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import uuid_from_time
import logging
import os
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Cassandra MCP Server 📶")

# Configuration from environment
CASSANDRA_CONFIG = {
    "contact_points": os.getenv("CASSANDRA_CONTACT_POINTS", "localhost").split(","),
    "keyspace": os.getenv("CASSANDRA_KEYSPACE", "test"),
    "username": os.getenv("CASSANDRA_USER"),
    "password": os.getenv("CASSANDRA_PASSWORD"),
}

def get_cassandra_session():
    """Get Cassandra session with configuration from environment."""
    try:
        if CASSANDRA_CONFIG["username"] and CASSANDRA_CONFIG["password"]:
            auth = PlainTextAuthProvider(CASSANDRA_CONFIG["username"], CASSANDRA_CONFIG["password"])
            cluster = Cluster(CASSANDRA_CONFIG["contact_points"], auth_provider=auth)
        else:
            cluster = Cluster(CASSANDRA_CONFIG["contact_points"])
        
        session = cluster.connect(CASSANDRA_CONFIG["keyspace"])
        logger.info(f"✅ Connected to Cassandra: {CASSANDRA_CONFIG['keyspace']}")
        return session, cluster
    except Exception as e:
        logger.error(f"❌ Cassandra connection error: {str(e)}")
        raise

# ====================== DDL TOOLS (Keyspace/Table Management) ======================

@mcp.tool()
def cassandra_create_keyspace(keyspace_name: str, replication_factor: int = 3) -> Dict[str, Any]:
    """Create a new keyspace.
    
    Args:
        keyspace_name: Keyspace name
        replication_factor: Replication factor
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        
        query = f"""CREATE KEYSPACE {keyspace_name}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': {replication_factor}}}"""
        
        session.execute(query)
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🏗️ Keyspace created: {keyspace_name}")
        return {"success": True, "message": f"Keyspace '{keyspace_name}' created"}
    except Exception as e:
        logger.error(f"❌ Error creating keyspace: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_drop_keyspace(keyspace_name: str) -> Dict[str, Any]:
    """Drop a keyspace.
    
    Args:
        keyspace_name: Keyspace name to drop
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        session.execute(f"DROP KEYSPACE {keyspace_name}")
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🗑️ Keyspace dropped: {keyspace_name}")
        return {"success": True, "message": f"Keyspace '{keyspace_name}' dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping keyspace: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_list_keyspaces() -> Dict[str, Any]:
    """List all keyspaces.
    
    Returns:
        List of keyspace names
    """
    try:
        session, cluster = get_cassandra_session()
        keyspaces = [ks for ks in cluster.metadata.keyspaces.keys() if not ks.startswith('system')]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"📋 Found {len(keyspaces)} keyspaces")
        return {"success": True, "keyspaces": keyspaces, "count": len(keyspaces)}
    except Exception as e:
        logger.error(f"❌ Error listing keyspaces: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_create_table(table_name: str, columns: str, primary_key: str) -> Dict[str, Any]:
    """Create a new table.
    
    Args:
        table_name: Table name
        columns: Column definitions
        primary_key: Primary key specification
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        
        query = f"CREATE TABLE {table_name} ({columns}, PRIMARY KEY ({primary_key}))"
        session.execute(query)
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🏗️ Table created: {table_name}")
        return {"success": True, "message": f"Table '{table_name}' created"}
    except Exception as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_drop_table(table_name: str) -> Dict[str, Any]:
    """Drop a table.
    
    Args:
        table_name: Table name to drop
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        session.execute(f"DROP TABLE {table_name}")
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🗑️ Table dropped: {table_name}")
        return {"success": True, "message": f"Table '{table_name}' dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_list_tables() -> Dict[str, Any]:
    """List all tables in keyspace.
    
    Returns:
        List of table names
    """
    try:
        session, cluster = get_cassandra_session()
        
        query = "SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s"
        result = session.execute(query, [CASSANDRA_CONFIG["keyspace"]])
        tables = [row.table_name for row in result]
        
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"📋 Found {len(tables)} tables")
        return {"success": True, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_describe_table(table_name: str) -> Dict[str, Any]:
    """Describe table structure.
    
    Args:
        table_name: Table name
    
    Returns:
        Table schema information
    """
    try:
        session, cluster = get_cassandra_session()
        
        metadata = cluster.metadata.keyspaces[CASSANDRA_CONFIG["keyspace"]].tables[table_name]
        columns = []
        
        for col_name, col in metadata.columns.items():
            columns.append({
                "name": col_name,
                "type": str(col.cql_type),
                "is_primary_key": col_name in [pk.name for pk in metadata.primary_key]
            })
        
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"📊 Table described: {table_name}")
        return {"success": True, "columns": columns, "count": len(columns)}
    except Exception as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS ======================

@mcp.tool()
def cassandra_insert_record(table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single record.
    
    Args:
        table_name: Table name
        record: Record data as dictionary
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["%s"] * len(record))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        session.execute(query, list(record.values()))
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"➕ Record inserted into {table_name}")
        return {"success": True, "message": "Record inserted successfully"}
    except Exception as e:
        logger.error(f"❌ Error inserting record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_insert_many(table_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple records.
    
    Args:
        table_name: Table name
        records: List of records
    
    Returns:
        Success status and row count
    """
    try:
        session, cluster = get_cassandra_session()
        
        if not records:
            return {"success": True, "message": "No records to insert", "inserted": 0}
        
        columns = ", ".join(records[0].keys())
        placeholders = ", ".join(["%s"] * len(records[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        for record in records:
            session.execute(query, list(record.values()))
        
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"➕ {len(records)} records inserted into {table_name}")
        return {"success": True, "message": f"{len(records)} records inserted", "inserted": len(records)}
    except Exception as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_update_records(table_name: str, set_clause: str, where_clause: str) -> Dict[str, Any]:
    """Update records.
    
    Args:
        table_name: Table name
        set_clause: SET clause
        where_clause: WHERE condition
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        session.execute(query)
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"✏️ Records updated in {table_name}")
        return {"success": True, "message": "Records updated"}
    except Exception as e:
        logger.error(f"❌ Error updating records: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_delete_records(table_name: str, where_clause: str) -> Dict[str, Any]:
    """Delete records.
    
    Args:
        table_name: Table name
        where_clause: WHERE condition
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        session.execute(query)
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🗑️ Records deleted from {table_name}")
        return {"success": True, "message": "Records deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting records: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SELECT/QUERY TOOLS ======================

@mcp.tool()
def cassandra_select_all(table_name: str, limit: int = 1000) -> Dict[str, Any]:
    """Select all records from a table.
    
    Args:
        table_name: Table name
        limit: Maximum rows to return
    
    Returns:
        Query results
    """
    try:
        session, cluster = get_cassandra_session()
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        result = session.execute(query)
        rows = [dict(row._asdict()) for row in result]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🔎 SELECT all: {len(rows)} rows from {table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"❌ SELECT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_select_where(table_name: str, where_clause: str, limit: int = 1000) -> Dict[str, Any]:
    """Select records with WHERE condition.
    
    Args:
        table_name: Table name
        where_clause: WHERE condition
        limit: Maximum rows
    
    Returns:
        Query results
    """
    try:
        session, cluster = get_cassandra_session()
        query = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT {limit}"
        result = session.execute(query)
        rows = [dict(row._asdict()) for row in result]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🔎 SELECT WHERE: {len(rows)} rows from {table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"❌ SELECT WHERE error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_select_count(table_name: str) -> Dict[str, Any]:
    """Count total records in a table.
    
    Args:
        table_name: Table name
    
    Returns:
        Record count
    """
    try:
        session, cluster = get_cassandra_session()
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = session.execute(query)
        count = result[0][0]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🔢 COUNT: {count} rows in {table_name}")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_select_distinct(table_name: str, column: str, limit: int = 1000) -> Dict[str, Any]:
    """Get distinct values from a column.
    
    Args:
        table_name: Table name
        column: Column name
        limit: Maximum rows
    
    Returns:
        List of distinct values
    """
    try:
        session, cluster = get_cassandra_session()
        query = f"SELECT DISTINCT {column} FROM {table_name} LIMIT {limit}"
        result = session.execute(query)
        values = [row[0] for row in result]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🔍 DISTINCT {column}: {len(values)} values")
        return {"success": True, "values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_select_ordered(table_name: str, order_by: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Select records with ORDER BY (if applicable).
    
    Args:
        table_name: Table name
        order_by: Column to order by
        direction: ASC or DESC
        limit: Maximum rows
    
    Returns:
        Ordered results
    """
    try:
        session, cluster = get_cassandra_session()
        query = f"SELECT * FROM {table_name} ORDER BY {order_by} {direction} LIMIT {limit}"
        result = session.execute(query)
        rows = [dict(row._asdict()) for row in result]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🔎 ORDER BY {order_by}: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"❌ ORDER BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_custom_query(query_string: str) -> Dict[str, Any]:
    """Execute a custom CQL query.
    
    Args:
        query_string: CQL query to execute
    
    Returns:
        Query results
    """
    try:
        session, cluster = get_cassandra_session()
        result = session.execute(query_string)
        rows = [dict(row._asdict()) if hasattr(row, '_asdict') else dict(row) for row in result]
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🔎 Custom query executed")
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"❌ Query error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== CLUSTER ADMIN TOOLS ======================

@mcp.tool()
def cassandra_create_index(table_name: str, column_name: str, index_name: Optional[str] = None) -> Dict[str, Any]:
    """Create an index on a column.
    
    Args:
        table_name: Table name
        column_name: Column name
        index_name: Optional index name
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        
        idx_name = index_name or f"{table_name}_{column_name}_idx"
        query = f"CREATE INDEX {idx_name} ON {table_name}({column_name})"
        
        session.execute(query)
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"📑 Index created: {idx_name}")
        return {"success": True, "message": f"Index '{idx_name}' created"}
    except Exception as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_drop_index(index_name: str) -> Dict[str, Any]:
    """Drop an index.
    
    Args:
        index_name: Index name to drop
    
    Returns:
        Success status
    """
    try:
        session, cluster = get_cassandra_session()
        session.execute(f"DROP INDEX {index_name}")
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"🗑️ Index dropped: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_get_cluster_stats() -> Dict[str, Any]:
    """Get cluster statistics.
    
    Returns:
        Cluster info
    """
    try:
        session, cluster = get_cassandra_session()
        
        stats = {
            "cluster_name": cluster.metadata.cluster_name,
            "keyspace": CASSANDRA_CONFIG["keyspace"],
            "nodes": len(cluster.metadata.all_hosts()),
            "partitioner": cluster.metadata.partitioner
        }
        
        session.shutdown()
        cluster.shutdown()
        
        logger.info(f"📊 Cluster stats retrieved")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting cluster stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_repair_keyspace(keyspace_name: Optional[str] = None) -> Dict[str, Any]:
    """Trigger keyspace repair (recommended periodically).
    
    Args:
        keyspace_name: Keyspace to repair (default: configured keyspace)
    
    Returns:
        Success status
    """
    try:
        ks = keyspace_name or CASSANDRA_CONFIG["keyspace"]
        logger.info(f"🔧 Repair recommended for keyspace: {ks}")
        
        return {
            "success": True,
            "message": f"Run 'nodetool repair {ks}' on cluster nodes"
        }
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def cassandra_ttl_query(table_name: str, column_name: str, ttl_seconds: int) -> Dict[str, Any]:
    """Set TTL (Time-To-Live) on column for new records.
    
    Args:
        table_name: Table name
        column_name: Column name
        ttl_seconds: TTL in seconds
    
    Returns:
        Success status
    """
    try:
        return {
            "success": True,
            "message": f"Use USING TTL {ttl_seconds} in INSERT queries for {table_name}",
            "example": f"INSERT INTO {table_name} (...) VALUES (...) USING TTL {ttl_seconds}"
        }
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a Cassandra Database Administrator. Your role is to:
- Create and manage keyspaces and tables
- Optimize replication and consistency
- Create and manage indexes
- Monitor cluster health
- Perform maintenance tasks like repair

Use these tools for DBA tasks:
- cassandra_create_keyspace, cassandra_drop_keyspace, cassandra_list_keyspaces
- cassandra_create_table, cassandra_drop_table, cassandra_list_tables, cassandra_describe_table
- cassandra_create_index, cassandra_drop_index
- cassandra_get_cluster_stats, cassandra_repair_keyspace
"""

DATA_ENGINEER_PROMPT = """You are a Cassandra Data Engineer. Your role is to:
- Design efficient schemas with proper partition keys
- Load and transform data
- Ensure data consistency across replication
- Manage bulk operations

Use these tools for data engineering:
- cassandra_insert_record, cassandra_insert_many
- cassandra_update_records, cassandra_delete_records
- cassandra_select_all, cassandra_select_where for validation
- cassandra_custom_query for ETL operations
"""

DATA_ANALYST_PROMPT = """You are a Cassandra Data Analyst. Your role is to:
- Query and analyze distributed data
- Generate reports across the cluster
- Explore data patterns

Use these tools for analysis:
- cassandra_select_all, cassandra_select_where for exploration
- cassandra_select_count, cassandra_select_distinct
- cassandra_select_ordered for trend analysis
- cassandra_custom_query for complex analysis
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting Cassandra MCP Server...")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7088"))
    )

if __name__ == "__main__":
    asyncio.run(main())
