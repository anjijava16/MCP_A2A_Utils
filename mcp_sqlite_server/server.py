"""
SQLite MCP Server using FastMCP
Comprehensive SQLite database operations with 28 tools
"""

import asyncio
import sqlite3
from sqlite3 import Error as SQLiteError
import logging
import os
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("SQLite MCP Server 📄")

# Configuration from environment
SQLITE_CONFIG = {
    "database": os.getenv("SQLITE_DATABASE", "sqlite.db"),
}

def get_sqlite_connection() -> sqlite3.Connection:
    """Get SQLite connection with configuration from environment."""
    try:
        conn = sqlite3.connect(SQLITE_CONFIG["database"])
        conn.row_factory = sqlite3.Row
        logger.info(f"✅ Connected to SQLite: {SQLITE_CONFIG['database']}")
        return conn
    except SQLiteError as e:
        logger.error(f"❌ SQLite connection error: {str(e)}")
        raise

# ====================== DDL TOOLS ======================

@mcp.tool()
def sqlite_create_table(table_name: str, columns: str, primary_key: Optional[str] = None) -> Dict[str, Any]:
    """Create a new table.
    
    Args:
        table_name: Table name
        columns: Column definitions (col1 INT, col2 VARCHAR(255), ...)
        primary_key: Primary key column(s)
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        pk_clause = f", PRIMARY KEY ({primary_key})" if primary_key else ""
        query = f"CREATE TABLE {table_name} ({columns}{pk_clause})"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🏗️ Table created: {table_name}")
        return {"success": True, "message": f"Table '{table_name}' created"}
    except SQLiteError as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_drop_table(table_name: str) -> Dict[str, Any]:
    """Drop a table.
    
    Args:
        table_name: Table name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {table_name}")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Table dropped: {table_name}")
        return {"success": True, "message": f"Table '{table_name}' dropped"}
    except SQLiteError as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_list_tables() -> Dict[str, Any]:
    """List all tables in the database.
    
    Returns:
        List of table names
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📋 Found {len(tables)} tables")
        return {"success": True, "tables": tables, "count": len(tables)}
    except SQLiteError as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_describe_table(table_name: str) -> Dict[str, Any]:
    """Describe table structure.
    
    Args:
        table_name: Table name
    
    Returns:
        Table schema information
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [{"name": row[1], "type": row[2], "notnull": row[3], "pk": row[5]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📊 Table described: {table_name}")
        return {"success": True, "columns": columns, "count": len(columns)}
    except SQLiteError as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_alter_table(table_name: str, alter_clause: str) -> Dict[str, Any]:
    """Alter table structure.
    
    Args:
        table_name: Table name
        alter_clause: ALTER clause (ADD COLUMN col INT, RENAME TO new_name, etc.)
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"ALTER TABLE {table_name} {alter_clause}"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✏️ Table altered: {table_name}")
        return {"success": True, "message": f"Table '{table_name}' altered successfully"}
    except SQLiteError as e:
        logger.error(f"❌ Error altering table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_create_view(view_name: str, select_query: str) -> Dict[str, Any]:
    """Create a view.
    
    Args:
        view_name: View name
        select_query: SELECT query for the view
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"CREATE VIEW {view_name} AS {select_query}"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"👁️ View created: {view_name}")
        return {"success": True, "message": f"View '{view_name}' created"}
    except SQLiteError as e:
        logger.error(f"❌ Error creating view: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_drop_view(view_name: str) -> Dict[str, Any]:
    """Drop a view.
    
    Args:
        view_name: View name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP VIEW {view_name}")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ View dropped: {view_name}")
        return {"success": True, "message": f"View '{view_name}' dropped"}
    except SQLiteError as e:
        logger.error(f"❌ Error dropping view: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_list_views() -> Dict[str, Any]:
    """List all views in the database.
    
    Returns:
        List of view names
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
        views = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📋 Found {len(views)} views")
        return {"success": True, "views": views, "count": len(views)}
    except SQLiteError as e:
        logger.error(f"❌ Error listing views: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS ======================

@mcp.tool()
def sqlite_insert_record(table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single record.
    
    Args:
        table_name: Table name
        record: Record data as dictionary
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(record.values()))
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"➕ Record inserted into {table_name}")
        return {"success": True, "message": "Record inserted successfully"}
    except SQLiteError as e:
        logger.error(f"❌ Error inserting record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_insert_multiple_records(table_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple records.
    
    Args:
        table_name: Table name
        records: List of records
    
    Returns:
        Success status and row count
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        if not records:
            return {"success": True, "message": "No records to insert", "inserted": 0}
        
        columns = ", ".join(records[0].keys())
        placeholders = ", ".join(["?"] * len(records[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        for record in records:
            cursor.execute(query, tuple(record.values()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"➕ {len(records)} records inserted into {table_name}")
        return {"success": True, "message": f"{len(records)} records inserted", "inserted": len(records)}
    except SQLiteError as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_update_records(table_name: str, set_clause: str, where_clause: Optional[str] = None) -> Dict[str, Any]:
    """Update records.
    
    Args:
        table_name: Table name
        set_clause: SET clause (col1=val1, col2=val2)
        where_clause: WHERE condition
    
    Returns:
        Success status and affected rows
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        query = f"UPDATE {table_name} SET {set_clause}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        cursor.execute(query)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        logger.info(f"✏️ {affected} records updated in {table_name}")
        return {"success": True, "message": f"{affected} records updated", "affected": affected}
    except SQLiteError as e:
        logger.error(f"❌ Error updating records: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_delete_records(table_name: str, where_clause: str) -> Dict[str, Any]:
    """Delete records.
    
    Args:
        table_name: Table name
        where_clause: WHERE condition
    
    Returns:
        Success status and deleted rows
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        cursor.execute(query)
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ {deleted} records deleted from {table_name}")
        return {"success": True, "message": f"{deleted} records deleted", "deleted": deleted}
    except SQLiteError as e:
        logger.error(f"❌ Error deleting records: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SELECT/QUERY TOOLS ======================

@mcp.tool()
def sqlite_select_all(table_name: str, limit: int = 1000) -> Dict[str, Any]:
    """Select all records from a table.
    
    Args:
        table_name: Table name
        limit: Maximum rows to return
    
    Returns:
        Query results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 SELECT all: {len(rows)} rows from {table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except SQLiteError as e:
        logger.error(f"❌ SELECT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_where(table_name: str, where_clause: str, limit: int = 1000) -> Dict[str, Any]:
    """Select records with WHERE condition.
    
    Args:
        table_name: Table name
        where_clause: WHERE condition
        limit: Maximum rows
    
    Returns:
        Query results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {where_clause} LIMIT {limit}"
        cursor.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 SELECT WHERE: {len(rows)} rows from {table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except SQLiteError as e:
        logger.error(f"❌ SELECT WHERE error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_count(table_name: str) -> Dict[str, Any]:
    """Count total records in a table.
    
    Args:
        table_name: Table name
    
    Returns:
        Record count
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"🔢 COUNT: {count} rows in {table_name}")
        return {"success": True, "count": count}
    except SQLiteError as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_aggregate(table_name: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute aggregate query (SUM, AVG, MIN, MAX, COUNT).
    
    Args:
        table_name: Table name
        agg_column: Column to aggregate
        agg_function: Function (SUM, AVG, MIN, MAX, COUNT)
    
    Returns:
        Aggregate result
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"SELECT {agg_function}({agg_column}) FROM {table_name}"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"📊 {agg_function} of {agg_column}: {result}")
        return {"success": True, "result": result, "function": agg_function}
    except SQLiteError as e:
        logger.error(f"❌ Aggregate error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_distinct(table_name: str, column: str) -> Dict[str, Any]:
    """Get distinct values from a column.
    
    Args:
        table_name: Table name
        column: Column name
    
    Returns:
        List of distinct values
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"SELECT DISTINCT {column} FROM {table_name} LIMIT 1000"
        cursor.execute(query)
        values = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔍 DISTINCT {column}: {len(values)} values")
        return {"success": True, "values": values, "count": len(values)}
    except SQLiteError as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_grouped(table_name: str, group_by: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute GROUP BY query.
    
    Args:
        table_name: Table name
        group_by: Column to group by
        agg_column: Column to aggregate
        agg_function: Aggregate function
    
    Returns:
        Grouped results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"SELECT {group_by}, {agg_function}({agg_column}) as result FROM {table_name} GROUP BY {group_by} LIMIT 1000"
        cursor.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📊 GROUP BY {group_by}: {len(rows)} groups")
        return {"success": True, "rows": rows, "count": len(rows)}
    except SQLiteError as e:
        logger.error(f"❌ GROUP BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_ordered(table_name: str, order_by: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Select records with ORDER BY.
    
    Args:
        table_name: Table name
        order_by: Column to order by
        direction: ASC or DESC
        limit: Maximum rows
    
    Returns:
        Ordered results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} ORDER BY {order_by} {direction} LIMIT {limit}"
        cursor.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 ORDER BY {order_by}: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except SQLiteError as e:
        logger.error(f"❌ ORDER BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_select_join(table1: str, table2: str, join_column: str, join_type: str = "INNER") -> Dict[str, Any]:
    """Execute JOIN query between two tables.
    
    Args:
        table1: First table
        table2: Second table
        join_column: Column to join on
        join_type: INNER, LEFT, RIGHT, FULL
    
    Returns:
        Join results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {table1} {join_type} JOIN {table2} ON {table1}.{join_column} = {table2}.{join_column} LIMIT 1000"
        cursor.execute(query)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔗 {join_type} JOIN: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except SQLiteError as e:
        logger.error(f"❌ JOIN error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_custom_query(sql: str) -> Dict[str, Any]:
    """Execute a custom SQL query.
    
    Args:
        sql: SQL query to execute
    
    Returns:
        Query results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 Custom query executed")
        return {"success": True, "rows": rows, "count": len(rows)}
    except SQLiteError as e:
        logger.error(f"❌ Query error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== ADMINISTRATION TOOLS ======================

@mcp.tool()
def sqlite_create_index(index_name: str, table_name: str, columns: List[str], unique: bool = False) -> Dict[str, Any]:
    """Create an index on a table.
    
    Args:
        index_name: Index name
        table_name: Table name
        columns: List of columns to index
        unique: Create unique index
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        col_clause = ", ".join(columns)
        unique_clause = "UNIQUE " if unique else ""
        query = f"CREATE {unique_clause}INDEX {index_name} ON {table_name} ({col_clause})"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"📑 Index created: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' created"}
    except SQLiteError as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_drop_index(index_name: str) -> Dict[str, Any]:
    """Drop an index.
    
    Args:
        index_name: Index name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP INDEX {index_name}")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Index dropped: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' dropped"}
    except SQLiteError as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_list_indexes(table_name: str) -> Dict[str, Any]:
    """List all indexes for a table.
    
    Args:
        table_name: Table name
    
    Returns:
        List of indexes
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = [{"name": row[1], "unique": bool(row[2])} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📑 Found {len(indexes)} indexes for {table_name}")
        return {"success": True, "indexes": indexes, "count": len(indexes)}
    except SQLiteError as e:
        logger.error(f"❌ Error listing indexes: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_get_table_size(table_name: str) -> Dict[str, Any]:
    """Get table size and statistics.
    
    Args:
        table_name: Table name
    
    Returns:
        Size information
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        # Get page count (SQLite doesn't have standard table size, use page count)
        cursor.execute("PRAGMA page_count()")
        page_count = cursor.fetchone()[0]
        
        cursor.execute("PRAGMA page_size()")
        page_size = cursor.fetchone()[0]
        
        total_size_bytes = page_count * page_size
        
        cursor.close()
        conn.close()
        
        logger.info(f"📏 Table size retrieved: {table_name}")
        return {
            "success": True,
            "row_count": row_count,
            "page_count": page_count,
            "size_bytes": total_size_bytes,
            "size_mb": round(total_size_bytes / (1024 * 1024), 2)
        }
    except SQLiteError as e:
        logger.error(f"❌ Error getting table size: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_vacuum() -> Dict[str, Any]:
    """Vacuum and optimize the database.
    
    Returns:
        Success status
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("VACUUM")
        cursor.execute("ANALYZE")
        cursor.close()
        conn.close()
        
        logger.info(f"🧹 Database vacuumed and analyzed")
        return {"success": True, "message": "Database optimized"}
    except SQLiteError as e:
        logger.error(f"❌ Error vacuuming database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_get_database_stats() -> Dict[str, Any]:
    """Get comprehensive database statistics.
    
    Returns:
        Database statistics
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        stats = {
            "table_count": len(tables),
            "tables": []
        }
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            
            cursor.execute(f"PRAGMA table_info({table})")
            col_count = len(cursor.fetchall())
            
            stats["tables"].append({
                "name": table,
                "row_count": row_count,
                "column_count": col_count
            })
        
        cursor.close()
        conn.close()
        
        logger.info(f"📊 Database stats retrieved")
        return {"success": True, "stats": stats}
    except SQLiteError as e:
        logger.error(f"❌ Error getting database stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def sqlite_integrity_check() -> Dict[str, Any]:
    """Run database integrity check.
    
    Returns:
        Integrity check results
    """
    try:
        conn = get_sqlite_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Integrity check: {result}")
        return {"success": True, "status": result}
    except SQLiteError as e:
        logger.error(f"❌ Error checking integrity: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a SQLite Database Administrator. Your role is to:
- Create and manage tables and views
- Optimize database performance
- Monitor table sizes and database health
- Execute DDL operations safely
- Perform maintenance tasks

Use these tools for DBA tasks:
- sqlite_create_table, sqlite_drop_table, sqlite_list_tables, sqlite_describe_table
- sqlite_create_view, sqlite_drop_view, sqlite_list_views
- sqlite_create_index, sqlite_drop_index, sqlite_list_indexes
- sqlite_vacuum for maintenance
- sqlite_integrity_check for health checks
- sqlite_get_table_size for monitoring
"""

DATA_ENGINEER_PROMPT = """You are a SQLite Data Engineer. Your role is to:
- Design efficient table structures
- Load and transform data
- Manage bulk operations
- Ensure data quality
- Build data pipelines

Use these tools for data engineering:
- sqlite_insert_record, sqlite_insert_multiple_records
- sqlite_update_records, sqlite_delete_records
- sqlite_select_all, sqlite_select_where for validation
- sqlite_custom_query for ETL operations
- sqlite_vacuum for optimization
"""

DATA_ANALYST_PROMPT = """You are a SQLite Data Analyst. Your role is to:
- Query and analyze data efficiently
- Generate insights and reports
- Explore data patterns
- Create analytical queries

Use these tools for analysis:
- sqlite_select_all, sqlite_select_where for exploration
- sqlite_select_aggregate, sqlite_select_grouped for statistics
- sqlite_select_distinct, sqlite_select_ordered for trends
- sqlite_select_join for cross-table analysis
- sqlite_custom_query for complex analysis
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting SQLite MCP Server...")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7086"))
    )

if __name__ == "__main__":
    asyncio.run(main())
