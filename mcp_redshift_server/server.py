"""
AWS Redshift MCP Server - Comprehensive Data Warehouse Operations
Data warehousing with 25+ tools covering DDL, DML, SELECT, and DCL operations
"""

import asyncio
import logging
import os
import json
from typing import Optional, List, Dict, Any

try:
    import psycopg2
    from psycopg2 import Error, sql
    REDSHIFT_AVAILABLE = True
except ImportError:
    REDSHIFT_AVAILABLE = False
    Error = Exception
    sql = None

from fastmcp import FastMCP

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("AWS Redshift MCP Server 🏗️")

# ============================================================================
# REDSHIFT DATABASE CONFIGURATION
# ============================================================================
REDSHIFT_CONFIG = {
    "host": os.getenv("REDSHIFT_HOST", "localhost"),
    "port": int(os.getenv("REDSHIFT_PORT", 5439)),
    "user": os.getenv("REDSHIFT_USER", "awsuser"),
    "password": os.getenv("REDSHIFT_PASSWORD", "Password123!"),
    "database": os.getenv("REDSHIFT_DATABASE", "dev"),
}


def get_redshift_connection(database: Optional[str] = None):
    """Create and return a Redshift database connection."""
    if not REDSHIFT_AVAILABLE:
        raise ImportError(
            "psycopg2 is not installed. "
            "Install with: pip install psycopg2-binary"
        )
    try:
        config = REDSHIFT_CONFIG.copy()
        if database:
            config["database"] = database
        connection = psycopg2.connect(**config)
        logger.info("✅ Redshift connection established")
        return connection
    except Error as e:
        logger.error(f"❌ Redshift connection error: {e}")
        raise


# ============================================================================
# REDSHIFT DDL TOOLS (8 tools)
# ============================================================================

@mcp.tool()
def redshift_create_schema(schema_name: str):
    """Create a new schema in Redshift.

    Args:
        schema_name: Name of the schema to create.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 📦 Tool: redshift_create_schema called for '{schema_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Schema '{schema_name}' created successfully")
        return {"success": True, "message": f"Schema '{schema_name}' created successfully", "schema": schema_name}
    except Exception as e:
        logger.error(f"❌ Error creating schema: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_drop_schema(schema_name: str, cascade: bool = False, confirm: bool = False):
    """Drop a schema from Redshift.

    Args:
        schema_name: Name of the schema to drop.
        cascade: If True, drop schema and all objects within it.
        confirm: Must be True to confirm deletion.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🗑️ Tool: redshift_drop_schema called for '{schema_name}' ---")
    if not confirm:
        return {"success": False, "error": "Set confirm=True to confirm schema deletion."}
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cascade_str = "CASCADE" if cascade else "RESTRICT"
        cursor.execute(f"DROP SCHEMA IF EXISTS {schema_name} {cascade_str}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Schema '{schema_name}' dropped successfully")
        return {"success": True, "message": f"Schema '{schema_name}' dropped successfully"}
    except Exception as e:
        logger.error(f"❌ Error dropping schema: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_list_schemas():
    """List all schemas in Redshift database.

    Returns:
        A dictionary containing a list of all schemas.
    """
    logger.info("--- 📋 Tool: redshift_list_schemas called ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('pg_catalog', 'information_schema')")
        schemas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(schemas)} schemas")
        return {"success": True, "schemas": schemas, "count": len(schemas)}
    except Exception as e:
        logger.error(f"❌ Error listing schemas: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_create_table(schema_name: str, table_name: str, columns: str, distribution_key: Optional[str] = None, sort_key: Optional[str] = None):
    """Create a new table in Redshift with distribution and sort keys.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        columns: Column definitions.
        distribution_key: Column to distribute data on (DISTKEY).
        sort_key: Columns for sort order (SORTKEY).

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🏗️ Tool: redshift_create_table called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns})"
        if distribution_key:
            sql_stmt += f" DISTKEY({distribution_key})"
        if sort_key:
            sql_stmt += f" SORTKEY({sort_key})"
        cursor.execute(sql_stmt)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Table '{schema_name}.{table_name}' created successfully")
        return {"success": True, "message": f"Table '{schema_name}.{table_name}' created successfully"}
    except Exception as e:
        logger.error(f"❌ Error creating table: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_drop_table(schema_name: str, table_name: str, confirm: bool = False):
    """Drop a table from Redshift.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        confirm: Must be True to confirm deletion.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🗑️ Tool: redshift_drop_table called for '{schema_name}.{table_name}' ---")
    if not confirm:
        return {"success": False, "error": "Set confirm=True to confirm table deletion."}
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Table '{schema_name}.{table_name}' dropped successfully")
        return {"success": True, "message": f"Table dropped successfully"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_list_tables(schema_name: str):
    """List all tables in a schema.

    Args:
        schema_name: Name of the schema.

    Returns:
        A dictionary containing table names.
    """
    logger.info(f"--- 📋 Tool: redshift_list_tables called for '{schema_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}' AND table_type = 'BASE TABLE'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(tables)} tables in '{schema_name}'")
        return {"success": True, "schema": schema_name, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_describe_table(schema_name: str, table_name: str):
    """Describe table structure and columns.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.

    Returns:
        A dictionary containing column details.
    """
    logger.info(f"--- 🔍 Tool: redshift_describe_table called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable, column_default, ordinal_position
            FROM information_schema.columns
            WHERE table_schema = '{schema_name}' AND table_name = '{table_name}'
            ORDER BY ordinal_position
        """)
        columns = []
        for row in cursor.fetchall():
            columns.append({
                "name": row[0],
                "type": row[1],
                "nullable": row[2],
                "default": row[3],
                "position": row[4]
            })
        cursor.close()
        conn.close()
        logger.info(f"✅ Table described: {len(columns)} columns")
        return {"success": True, "table": table_name, "columns": columns, "column_count": len(columns)}
    except Exception as e:
        logger.error(f"❌ Error describing table: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_alter_table(schema_name: str, table_name: str, alter_statement: str):
    """Modify table structure.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        alter_statement: The ALTER TABLE clause.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🔧 Tool: redshift_alter_table called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"ALTER TABLE {schema_name}.{table_name} {alter_statement}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Table altered successfully")
        return {"success": True, "message": "Table altered successfully"}
    except Exception as e:
        logger.error(f"❌ Error altering table: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# REDSHIFT DML TOOLS (5 tools)
# ============================================================================

@mcp.tool()
def redshift_insert_record(schema_name: str, table_name: str, data: Dict[str, Any]):
    """Insert a single record into a table.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        data: Dictionary of column-value pairs.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- ➕ Tool: redshift_insert_record called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql_stmt = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql_stmt, list(data.values()))
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Record inserted into '{schema_name}.{table_name}'")
        return {"success": True, "message": "Record inserted successfully"}
    except Exception as e:
        logger.error(f"❌ Error inserting record: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_insert_multiple_records(schema_name: str, table_name: str, records: List[Dict[str, Any]]):
    """Bulk insert multiple records.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        records: List of dictionaries with column-value pairs.

    Returns:
        A dictionary with number of rows inserted.
    """
    logger.info(f"--- ➕ Tool: redshift_insert_multiple_records called for '{schema_name}.{table_name}' ---")
    if not records:
        return {"success": False, "error": "No records provided"}
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        columns = ", ".join(records[0].keys())
        placeholders = ", ".join(["%s"] * len(records[0]))
        sql_stmt = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"
        for record in records:
            cursor.execute(sql_stmt, list(record.values()))
        conn.commit()
        rows = len(records)
        cursor.close()
        conn.close()
        logger.info(f"✅ {rows} records inserted")
        return {"success": True, "message": f"{rows} records inserted", "rows_inserted": rows}
    except Exception as e:
        logger.error(f"❌ Error bulk inserting: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_update_records(schema_name: str, table_name: str, updates: Dict[str, Any], condition: str):
    """Update records based on condition.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        updates: Dictionary of column-value pairs to update.
        condition: WHERE clause condition.

    Returns:
        A dictionary with number of rows affected.
    """
    logger.info(f"--- ✏️ Tool: redshift_update_records called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        set_clause = ", ".join(f"{k} = %s" for k in updates.keys())
        sql_stmt = f"UPDATE {schema_name}.{table_name} SET {set_clause} WHERE {condition}"
        cursor.execute(sql_stmt, list(updates.values()))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        logger.info(f"✅ {rows_affected} rows updated")
        return {"success": True, "message": f"{rows_affected} rows updated", "rows_affected": rows_affected}
    except Exception as e:
        logger.error(f"❌ Error updating records: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_delete_records(schema_name: str, table_name: str, condition: str, confirm: bool = False):
    """Delete records based on condition.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        condition: WHERE clause condition.
        confirm: Must be True to confirm deletion.

    Returns:
        A dictionary with number of rows deleted.
    """
    logger.info(f"--- 🗑️ Tool: redshift_delete_records called for '{schema_name}.{table_name}' ---")
    if not confirm:
        return {"success": False, "error": "Set confirm=True to confirm deletion"}
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"DELETE FROM {schema_name}.{table_name} WHERE {condition}"
        cursor.execute(sql_stmt)
        conn.commit()
        rows_deleted = cursor.rowcount
        cursor.close()
        conn.close()
        logger.info(f"✅ {rows_deleted} rows deleted")
        return {"success": True, "message": f"{rows_deleted} rows deleted", "rows_deleted": rows_deleted}
    except Exception as e:
        logger.error(f"❌ Error deleting records: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_copy_from_s3(schema_name: str, table_name: str, s3_path: str, iam_role: str):
    """Copy data from S3 into Redshift table using COPY command.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        s3_path: S3 path to data (s3://bucket/prefix/).
        iam_role: IAM role ARN for S3 access.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 📥 Tool: redshift_copy_from_s3 called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        copy_sql = f"COPY {schema_name}.{table_name} FROM '{s3_path}' IAM_ROLE '{iam_role}' CSV"
        cursor.execute(copy_sql)
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Data copied from S3")
        return {"success": True, "message": "Data copied from S3 successfully"}
    except Exception as e:
        logger.error(f"❌ Error copying from S3: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# REDSHIFT SELECT/QUERY TOOLS (9 tools)
# ============================================================================

@mcp.tool()
def redshift_select_all(schema_name: str, table_name: str, limit: int = 100):
    """Select all records from a table.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        limit: Maximum records to return.

    Returns:
        A dictionary with records.
    """
    logger.info(f"--- 🔎 Tool: redshift_select_all called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {schema_name}.{table_name} LIMIT {limit}")
        columns = [desc[0] for desc in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} records")
        return {"success": True, "records": records, "count": len(records)}
    except Exception as e:
        logger.error(f"❌ Error selecting all: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_where(schema_name: str, table_name: str, condition: str, limit: int = 100):
    """Select records with WHERE condition.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        condition: WHERE clause condition.
        limit: Maximum records to return.

    Returns:
        A dictionary with matching records.
    """
    logger.info(f"--- 🔎 Tool: redshift_select_where called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {schema_name}.{table_name} WHERE {condition} LIMIT {limit}")
        columns = [desc[0] for desc in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} records with condition")
        return {"success": True, "records": records, "count": len(records)}
    except Exception as e:
        logger.error(f"❌ Error in select_where: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_count(schema_name: str, table_name: str, condition: Optional[str] = None):
    """Count records in a table.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        condition: Optional WHERE clause.

    Returns:
        A dictionary with record count.
    """
    logger.info(f"--- 🔢 Tool: redshift_select_count called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"SELECT COUNT(*) FROM {schema_name}.{table_name}"
        if condition:
            sql_stmt += f" WHERE {condition}"
        cursor.execute(sql_stmt)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        logger.info(f"✅ Count: {count}")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ Error counting: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_aggregate(schema_name: str, table_name: str, function: str, column: str, condition: Optional[str] = None):
    """Perform aggregate function (SUM, AVG, MIN, MAX, COUNT).

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        function: Aggregate function (SUM, AVG, MIN, MAX, COUNT).
        column: Column to aggregate.
        condition: Optional WHERE clause.

    Returns:
        A dictionary with aggregate result.
    """
    logger.info(f"--- 📊 Tool: redshift_select_aggregate called for {function}({column}) ---")
    allowed_functions = {"SUM", "AVG", "MIN", "MAX", "COUNT"}
    func_upper = function.upper()
    if func_upper not in allowed_functions:
        return {"success": False, "error": f"Invalid function '{function}'"}
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"SELECT {func_upper}({column}) FROM {schema_name}.{table_name}"
        if condition:
            sql_stmt += f" WHERE {condition}"
        cursor.execute(sql_stmt)
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        logger.info(f"✅ {func_upper}({column}) = {result}")
        return {"success": True, "function": func_upper, "column": column, "result": result}
    except Exception as e:
        logger.error(f"❌ Error in aggregate: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_distinct(schema_name: str, table_name: str, column: str, limit: int = 100):
    """Get distinct values from a column.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        column: Column name.
        limit: Maximum values to return.

    Returns:
        A dictionary with distinct values.
    """
    logger.info(f"--- 🔎 Tool: redshift_select_distinct called for '{column}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column} FROM {schema_name}.{table_name} LIMIT {limit}")
        values = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(values)} distinct values")
        return {"success": True, "column": column, "values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ Error in select_distinct: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_grouped(schema_name: str, table_name: str, group_by: str, aggregate_column: str, aggregate_function: str = "COUNT", limit: int = 100):
    """Group records and apply aggregate function.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        group_by: Column to group by.
        aggregate_column: Column for aggregate function.
        aggregate_function: Aggregate function (COUNT, SUM, AVG, MIN, MAX).
        limit: Maximum groups to return.

    Returns:
        A dictionary with grouped results.
    """
    logger.info(f"--- 📊 Tool: redshift_select_grouped called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"SELECT {group_by}, {aggregate_function}({aggregate_column}) AS aggregate_value FROM {schema_name}.{table_name} GROUP BY {group_by} LIMIT {limit}"
        cursor.execute(sql_stmt)
        columns = [desc[0] for desc in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} groups")
        return {"success": True, "group_by": group_by, "records": records, "count": len(records)}
    except Exception as e:
        logger.error(f"❌ Error in select_grouped: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_ordered(schema_name: str, table_name: str, order_by: str, direction: str = "ASC", limit: int = 100):
    """Select records sorted by a column.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        order_by: Column to sort by.
        direction: Sort direction (ASC or DESC).
        limit: Maximum records to return.

    Returns:
        A dictionary with sorted records.
    """
    logger.info(f"--- 🔃 Tool: redshift_select_ordered called for '{schema_name}.{table_name}' ---")
    direction = direction.upper()
    if direction not in ("ASC", "DESC"):
        return {"success": False, "error": "direction must be 'ASC' or 'DESC'"}
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"SELECT * FROM {schema_name}.{table_name} ORDER BY {order_by} {direction} LIMIT {limit}"
        cursor.execute(sql_stmt)
        columns = [desc[0] for desc in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} ordered records")
        return {"success": True, "records": records, "count": len(records), "order_by": order_by}
    except Exception as e:
        logger.error(f"❌ Error in select_ordered: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_select_join(schema_name: str, table1: str, table2: str, join_condition: str, limit: int = 100):
    """Join two tables.

    Args:
        schema_name: Name of the schema.
        table1: First table name.
        table2: Second table name.
        join_condition: JOIN ON condition.
        limit: Maximum records to return.

    Returns:
        A dictionary with joined records.
    """
    logger.info(f"--- 🔗 Tool: redshift_select_join called for '{table1}' JOIN '{table2}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        sql_stmt = f"SELECT * FROM {schema_name}.{table1} INNER JOIN {schema_name}.{table2} ON {join_condition} LIMIT {limit}"
        cursor.execute(sql_stmt)
        columns = [desc[0] for desc in cursor.description]
        records = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        logger.info(f"✅ Retrieved {len(records)} joined records")
        return {"success": True, "records": records, "count": len(records)}
    except Exception as e:
        logger.error(f"❌ Error in select_join: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_custom_query(query: str, params: Optional[List[Any]] = None):
    """Execute a custom SQL query.

    Args:
        query: Full SQL query string.
        params: Optional parameter values for parameterized queries.

    Returns:
        A dictionary with results.
    """
    logger.info(f"--- ⚡ Tool: redshift_custom_query called ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT") or query_upper.startswith("SHOW") or query_upper.startswith("DESCRIBE"):
            columns = [desc[0] for desc in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            logger.info(f"✅ Query returned {len(records)} records")
            return {"success": True, "records": records, "count": len(records)}
        else:
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"✅ Query affected {rows_affected} rows")
            return {"success": True, "rows_affected": rows_affected}
    except Exception as e:
        logger.error(f"❌ Error in custom query: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# REDSHIFT DCL TOOLS (3 tools)
# ============================================================================

@mcp.tool()
def redshift_grant_permissions(schema_name: str, table_name: str, user: str, permissions: List[str]):
    """Grant permissions to a user.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        user: Username to grant permissions to.
        permissions: List of permissions (SELECT, INSERT, UPDATE, DELETE, ALL).

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🔐 Tool: redshift_grant_permissions called for user '{user}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        perms_str = ",".join(permissions)
        cursor.execute(f"GRANT {perms_str} ON {schema_name}.{table_name} TO {user}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Permissions granted to {user}")
        return {"success": True, "message": f"Permissions granted to {user}"}
    except Exception as e:
        logger.error(f"❌ Error granting permissions: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_revoke_permissions(schema_name: str, table_name: str, user: str, permissions: List[str]):
    """Revoke permissions from a user.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.
        user: Username to revoke permissions from.
        permissions: List of permissions to revoke.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🔐 Tool: redshift_revoke_permissions called for user '{user}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        perms_str = ",".join(permissions)
        cursor.execute(f"REVOKE {perms_str} ON {schema_name}.{table_name} FROM {user}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ Permissions revoked from {user}")
        return {"success": True, "message": f"Permissions revoked from {user}"}
    except Exception as e:
        logger.error(f"❌ Error revoking permissions: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_list_users():
    """List all users in Redshift cluster.

    Returns:
        A dictionary with list of users.
    """
    logger.info("--- 👥 Tool: redshift_list_users called ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT usename, usesuper FROM pg_user ORDER BY usename")
        users = []
        for row in cursor.fetchall():
            users.append({"username": row[0], "is_superuser": row[1]})
        cursor.close()
        conn.close()
        logger.info(f"✅ Found {len(users)} users")
        return {"success": True, "users": users, "count": len(users)}
    except Exception as e:
        logger.error(f"❌ Error listing users: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# REDSHIFT ADMINISTRATION TOOLS (3 tools)
# ============================================================================

@mcp.tool()
def redshift_vacuum(schema_name: str, table_name: str):
    """Run VACUUM on a table to reclaim storage and optimize.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 🧹 Tool: redshift_vacuum called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        conn.set_isolation_level(0)  # Autocommit mode
        cursor = conn.cursor()
        cursor.execute(f"VACUUM {schema_name}.{table_name}")
        cursor.close()
        conn.close()
        logger.info(f"✅ VACUUM completed for '{schema_name}.{table_name}'")
        return {"success": True, "message": "VACUUM completed"}
    except Exception as e:
        logger.error(f"❌ Error in VACUUM: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_analyze(schema_name: str, table_name: str):
    """Run ANALYZE on a table to update statistics.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.

    Returns:
        A dictionary with success or error message.
    """
    logger.info(f"--- 📈 Tool: redshift_analyze called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"ANALYZE {schema_name}.{table_name}")
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"✅ ANALYZE completed")
        return {"success": True, "message": "ANALYZE completed"}
    except Exception as e:
        logger.error(f"❌ Error in ANALYZE: {e}")
        return {"success": False, "error": str(e)}


@mcp.tool()
def redshift_get_table_stats(schema_name: str, table_name: str):
    """Get table statistics and information.

    Args:
        schema_name: Name of the schema.
        table_name: Name of the table.

    Returns:
        A dictionary with table statistics.
    """
    logger.info(f"--- 📊 Tool: redshift_get_table_stats called for '{schema_name}.{table_name}' ---")
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT 
                schemaname,
                tablename,
                n_rows,
                size,
                unsorted_pct
            FROM svv_table_info
            WHERE schemaname = '{schema_name}' AND tablename = '{table_name}'
        """)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            stats = {
                "schema": result[0],
                "table": result[1],
                "row_count": result[2],
                "size_bytes": result[3],
                "unsorted_percentage": result[4]
            }
            logger.info(f"✅ Retrieved table statistics")
            return {"success": True, "stats": stats}
        else:
            return {"success": False, "error": "Table not found"}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# PROMPTS
# ============================================================================

@mcp.prompt()
def redshift_dba_prompt() -> str:
    """Prompt for Redshift Database Administrator."""
    return """You are an AWS Redshift Database Administrator. Your responsibilities:
1. Managing schemas and table structures
2. Optimizing data warehouse performance with distribution and sort keys
3. Managing user permissions and access control
4. Monitoring table statistics and performance
5. Loading data efficiently from S3
6. Running VACUUM and ANALYZE operations

Best practices:
- Choose appropriate DISTKEY to minimize data movement
- Use SORTKEY for frequently joined or filtered columns
- Regularly run VACUUM and ANALYZE for performance
- Monitor unsorted_pct in table statistics
- Use COPY command for bulk data loading from S3
- Implement fine-grained access controls with GRANT/REVOKE"""


@mcp.prompt()
def redshift_data_engineer_prompt() -> str:
    """Prompt for Redshift Data Engineer."""
    return """You are a Redshift Data Engineer specializing in ETL pipelines and data loading.
Your focus:
1. Designing efficient warehouse schemas with proper distribution
2. Building ETL processes using COPY from S3
3. Managing bulk data operations efficiently
4. Optimizing query performance

Engineering workflow:
- Create schemas and tables with optimized distribution
- Load data efficiently from S3 using COPY
- Validate data counts before and after loads
- Use bulk INSERT for smaller datasets
- Monitor pipeline performance and table statistics"""


@mcp.prompt()
def redshift_analyst_prompt() -> str:
    """Prompt for Redshift Data Analyst."""
    return """You are a Redshift Data Analyst specializing in business intelligence.
Your responsibilities:
1. Querying the data warehouse for insights
2. Building reports and dashboards
3. Analyzing business metrics and trends
4. Providing data-driven recommendations

Analytical approach:
- Use aggregate functions for KPI calculations
- Group and sort data for analysis
- Use JOINs to combine data from multiple tables
- Filter with WHERE clauses for specific insights
- Count and distinct operations for data quality checks"""


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7081))
    logger.info(f"🚀 AWS Redshift MCP server starting on port {port}")
    
    logger.info("📋 Available Tools:")
    logger.info("\n--- REDSHIFT DDL TOOLS (8) ---")
    logger.info("  1. redshift_create_schema      - Create a schema")
    logger.info("  2. redshift_drop_schema        - Drop a schema")
    logger.info("  3. redshift_list_schemas       - List all schemas")
    logger.info("  4. redshift_create_table       - Create table with DISTKEY/SORTKEY")
    logger.info("  5. redshift_drop_table         - Drop a table")
    logger.info("  6. redshift_list_tables        - List tables in schema")
    logger.info("  7. redshift_describe_table     - Describe table columns")
    logger.info("  8. redshift_alter_table        - Modify table structure")
    
    logger.info("\n--- REDSHIFT DML TOOLS (5) ---")
    logger.info("  9. redshift_insert_record          - Insert single record")
    logger.info("  10. redshift_insert_multiple_records - Bulk insert records")
    logger.info("  11. redshift_update_records        - Update records by condition")
    logger.info("  12. redshift_delete_records        - Delete records by condition")
    logger.info("  13. redshift_copy_from_s3          - COPY data from S3")
    
    logger.info("\n--- REDSHIFT SELECT/QUERY TOOLS (9) ---")
    logger.info("  14. redshift_select_all       - Select all records")
    logger.info("  15. redshift_select_where     - Select with WHERE condition")
    logger.info("  16. redshift_select_count     - Count records")
    logger.info("  17. redshift_select_aggregate - SUM, AVG, MIN, MAX, COUNT")
    logger.info("  18. redshift_select_distinct  - Get distinct values")
    logger.info("  19. redshift_select_grouped   - GROUP BY aggregation")
    logger.info("  20. redshift_select_ordered   - ORDER BY sorting")
    logger.info("  21. redshift_select_join      - JOIN tables")
    logger.info("  22. redshift_custom_query     - Execute custom SQL")
    
    logger.info("\n--- REDSHIFT DCL TOOLS (3) ---")
    logger.info("  23. redshift_grant_permissions     - Grant user permissions")
    logger.info("  24. redshift_revoke_permissions    - Revoke user permissions")
    logger.info("  25. redshift_list_users            - List all users")
    
    logger.info("\n--- REDSHIFT ADMINISTRATION TOOLS (3) ---")
    logger.info("  26. redshift_vacuum          - VACUUM table for optimization")
    logger.info("  27. redshift_analyze         - ANALYZE table statistics")
    logger.info("  28. redshift_get_table_stats - Get table statistics")
    
    logger.info(f"\n✅ Total Tools: 28  |  Port: {port}")
    logger.info("\n🎯 Available Prompts (3):")
    logger.info("  1. redshift_dba_prompt          - Database administration")
    logger.info("  2. redshift_data_engineer_prompt - Data engineering & ETL")
    logger.info("  3. redshift_analyst_prompt       - Analytics & reporting")
    
    asyncio.run(
        mcp.run_async(
            transport="sse",
            host="0.0.0.0",
            port=port,
        )
    )
