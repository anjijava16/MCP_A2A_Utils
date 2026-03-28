import asyncio
import logging
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
import psycopg2
from psycopg2 import Error as PostgresError
from psycopg2.extras import DictCursor
from fastmcp import FastMCP

# Configure logging with emoji
logging.basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("PostgreSQL MCP Server 🐘")

# Configuration from environment
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "database": os.getenv("POSTGRES_DATABASE", "postgres"),
}

def get_postgres_connection() -> psycopg2.extensions.connection:
    """Get PostgreSQL connection with configuration from environment."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        logger.info(f"✅ Connected to PostgreSQL: {POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}")
        return conn
    except PostgresError as e:
        logger.error(f"❌ PostgreSQL connection error: {str(e)}")
        raise

# ====================== DDL TOOLS ======================

@mcp.tool()
def postgresql_create_database(database_name: str, owner: Optional[str] = None, encoding: str = "UTF8") -> Dict[str, Any]:
    """Create a new database.
    
    Args:
        database_name: Database name
        owner: Database owner
        encoding: Encoding (default: UTF8)
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        
        owner_clause = f"OWNER {owner}" if owner else ""
        query = f"CREATE DATABASE {database_name} ENCODING '{encoding}' {owner_clause}"
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"📦 Database created: {database_name}")
        return {"success": True, "message": f"Database '{database_name}' created"}
    except PostgresError as e:
        logger.error(f"❌ Error creating database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_drop_database(database_name: str) -> Dict[str, Any]:
    """Drop a database.
    
    Args:
        database_name: Database name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE {database_name}")
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Database dropped: {database_name}")
        return {"success": True, "message": f"Database '{database_name}' dropped"}
    except PostgresError as e:
        logger.error(f"❌ Error dropping database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_list_databases() -> Dict[str, Any]:
    """List all databases.
    
    Returns:
        List of database names
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname")
        databases = [row["datname"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📋 Found {len(databases)} databases")
        return {"success": True, "databases": databases, "count": len(databases)}
    except PostgresError as e:
        logger.error(f"❌ Error listing databases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_create_table(schema_name: str, table_name: str, columns: str, 
                           primary_key: Optional[str] = None) -> Dict[str, Any]:
    """Create a new table.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        columns: Column definitions (col1 INT, col2 VARCHAR(255), ...)
        primary_key: Primary key column(s)
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        pk_clause = f", PRIMARY KEY ({primary_key})" if primary_key else ""
        query = f"CREATE TABLE {schema_name}.{table_name} ({columns}{pk_clause})"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🏗️ Table created: {schema_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' created in '{schema_name}'"}
    except PostgresError as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_drop_table(schema_name: str, table_name: str) -> Dict[str, Any]:
    """Drop a table.
    
    Args:
        schema_name: Schema name
        table_name: Table name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE {schema_name}.{table_name}")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Table dropped: {schema_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' dropped"}
    except PostgresError as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_list_tables(schema_name: str = "public") -> Dict[str, Any]:
    """List all tables in a schema.
    
    Args:
        schema_name: Schema name
    
    Returns:
        List of table names
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name"
        cursor.execute(query, (schema_name,))
        tables = [row["table_name"] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📋 Found {len(tables)} tables in {schema_name}")
        return {"success": True, "tables": tables, "count": len(tables)}
    except PostgresError as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_describe_table(schema_name: str, table_name: str) -> Dict[str, Any]:
    """Describe table structure.
    
    Args:
        schema_name: Schema name
        table_name: Table name
    
    Returns:
        Table schema information
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = "SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_schema = %s AND table_name = %s"
        cursor.execute(query, (schema_name, table_name))
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"📊 Table described: {schema_name}.{table_name}")
        return {"success": True, "columns": columns, "count": len(columns)}
    except PostgresError as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_alter_table(schema_name: str, table_name: str, alter_clause: str) -> Dict[str, Any]:
    """Alter table structure.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        alter_clause: ALTER clause (ADD COLUMN col INT, DROP COLUMN col, etc.)
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        query = f"ALTER TABLE {schema_name}.{table_name} {alter_clause}"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✏️ Table altered: {schema_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' altered successfully"}
    except PostgresError as e:
        logger.error(f"❌ Error altering table: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS ======================

@mcp.tool()
def postgresql_insert_record(schema_name: str, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single record.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        record: Record data as dictionary
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["%s"] * len(record))
        query = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(record.values()))
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"➕ Record inserted into {schema_name}.{table_name}")
        return {"success": True, "message": "Record inserted successfully"}
    except PostgresError as e:
        logger.error(f"❌ Error inserting record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_insert_multiple_records(schema_name: str, table_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple records.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        records: List of records
    
    Returns:
        Success status and row count
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        if not records:
            return {"success": True, "message": "No records to insert", "inserted": 0}
        
        columns = ", ".join(records[0].keys())
        placeholders = ", ".join(["%s"] * len(records[0]))
        query = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"
        
        for record in records:
            cursor.execute(query, tuple(record.values()))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"➕ {len(records)} records inserted into {schema_name}.{table_name}")
        return {"success": True, "message": f"{len(records)} records inserted", "inserted": len(records)}
    except PostgresError as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_update_records(schema_name: str, table_name: str, set_clause: str, 
                             where_clause: Optional[str] = None) -> Dict[str, Any]:
    """Update records.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        set_clause: SET clause (col1=val1, col2=val2)
        where_clause: WHERE condition
    
    Returns:
        Success status and affected rows
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        query = f"UPDATE {schema_name}.{table_name} SET {set_clause}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        cursor.execute(query)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        logger.info(f"✏️ {affected} records updated in {schema_name}.{table_name}")
        return {"success": True, "message": f"{affected} records updated", "affected": affected}
    except PostgresError as e:
        logger.error(f"❌ Error updating records: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_delete_records(schema_name: str, table_name: str, where_clause: str) -> Dict[str, Any]:
    """Delete records.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        where_clause: WHERE condition
    
    Returns:
        Success status and deleted rows
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        query = f"DELETE FROM {schema_name}.{table_name} WHERE {where_clause}"
        cursor.execute(query)
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ {deleted} records deleted from {schema_name}.{table_name}")
        return {"success": True, "message": f"{deleted} records deleted", "deleted": deleted}
    except PostgresError as e:
        logger.error(f"❌ Error deleting records: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SELECT/QUERY TOOLS ======================

@mcp.tool()
def postgresql_select_all(schema_name: str, table_name: str, limit: int = 1000) -> Dict[str, Any]:
    """Select all records from a table.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        limit: Maximum rows to return
    
    Returns:
        Query results
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(f"SELECT * FROM {schema_name}.{table_name} LIMIT {limit}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 SELECT all: {len(rows)} rows from {schema_name}.{table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except PostgresError as e:
        logger.error(f"❌ SELECT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_where(schema_name: str, table_name: str, where_clause: str, limit: int = 1000) -> Dict[str, Any]:
    """Select records with WHERE condition.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        where_clause: WHERE condition
        limit: Maximum rows
    
    Returns:
        Query results
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = f"SELECT * FROM {schema_name}.{table_name} WHERE {where_clause} LIMIT {limit}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 SELECT WHERE: {len(rows)} rows from {schema_name}.{table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except PostgresError as e:
        logger.error(f"❌ SELECT WHERE error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_count(schema_name: str, table_name: str) -> Dict[str, Any]:
    """Count total records in a table.
    
    Args:
        schema_name: Schema name
        table_name: Table name
    
    Returns:
        Record count
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {schema_name}.{table_name}")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"🔢 COUNT: {count} rows in {schema_name}.{table_name}")
        return {"success": True, "count": count}
    except PostgresError as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_aggregate(schema_name: str, table_name: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute aggregate query (SUM, AVG, MIN, MAX, COUNT).
    
    Args:
        schema_name: Schema name
        table_name: Table name
        agg_column: Column to aggregate
        agg_function: Function (SUM, AVG, MIN, MAX, COUNT)
    
    Returns:
        Aggregate result
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        query = f"SELECT {agg_function}({agg_column}) FROM {schema_name}.{table_name}"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"📊 {agg_function} of {agg_column}: {result}")
        return {"success": True, "result": result, "function": agg_function}
    except PostgresError as e:
        logger.error(f"❌ Aggregate error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_distinct(schema_name: str, table_name: str, column: str) -> Dict[str, Any]:
    """Get distinct values from a column.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        column: Column name
    
    Returns:
        List of distinct values
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        query = f"SELECT DISTINCT {column} FROM {schema_name}.{table_name} LIMIT 1000"
        cursor.execute(query)
        values = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔍 DISTINCT {column}: {len(values)} values")
        return {"success": True, "values": values, "count": len(values)}
    except PostgresError as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_grouped(schema_name: str, table_name: str, group_by: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute GROUP BY query.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        group_by: Column to group by
        agg_column: Column to aggregate
        agg_function: Aggregate function
    
    Returns:
        Grouped results
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = f"SELECT {group_by}, {agg_function}({agg_column}) as result FROM {schema_name}.{table_name} GROUP BY {group_by} LIMIT 1000"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"📊 GROUP BY {group_by}: {len(rows)} groups")
        return {"success": True, "rows": rows, "count": len(rows)}
    except PostgresError as e:
        logger.error(f"❌ GROUP BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_ordered(schema_name: str, table_name: str, order_by: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Select records with ORDER BY.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        order_by: Column to order by
        direction: ASC or DESC
        limit: Maximum rows
    
    Returns:
        Ordered results
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = f"SELECT * FROM {schema_name}.{table_name} ORDER BY {order_by} {direction} LIMIT {limit}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 ORDER BY {order_by}: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except PostgresError as e:
        logger.error(f"❌ ORDER BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_select_join(schema_name: str, table1: str, table2: str, join_column: str, join_type: str = "INNER") -> Dict[str, Any]:
    """Execute JOIN query between two tables.
    
    Args:
        schema_name: Schema name
        table1: First table
        table2: Second table
        join_column: Column to join on
        join_type: INNER, LEFT, RIGHT, FULL
    
    Returns:
        Join results
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = f"SELECT * FROM {schema_name}.{table1} {join_type} JOIN {schema_name}.{table2} ON {table1}.{join_column} = {table2}.{join_column} LIMIT 1000"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔗 {join_type} JOIN: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except PostgresError as e:
        logger.error(f"❌ JOIN error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_custom_query(sql: str) -> Dict[str, Any]:
    """Execute a custom SQL query.
    
    Args:
        sql: SQL query to execute
    
    Returns:
        Query results
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 Custom query executed")
        return {"success": True, "rows": rows, "count": len(rows)}
    except PostgresError as e:
        logger.error(f"❌ Query error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DCL TOOLS ======================

@mcp.tool()
def postgresql_grant_permissions(role: str, schema_name: str, table_name: Optional[str] = None, permissions: Optional[List[str]] = None) -> Dict[str, Any]:
    """Grant permissions to a role.
    
    Args:
        role: Role name
        schema_name: Schema name
        table_name: Table name (optional, for table-level perms)
        permissions: List of permissions (SELECT, INSERT, UPDATE, DELETE, ALL)
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        if not permissions:
            permissions = ["USAGE", "CREATE"]
        
        perm_clause = ", ".join(permissions)
        
        if table_name:
            query = f"GRANT {perm_clause} ON {schema_name}.{table_name} TO {role}"
        else:
            query = f"GRANT {perm_clause} ON SCHEMA {schema_name} TO {role}"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🔐 Permissions granted to {role}")
        return {"success": True, "message": f"Permissions granted to {role}"}
    except PostgresError as e:
        logger.error(f"❌ Error granting permissions: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_revoke_permissions(role: str, schema_name: str, table_name: Optional[str] = None, permissions: Optional[List[str]] = None) -> Dict[str, Any]:
    """Revoke permissions from a role.
    
    Args:
        role: Role name
        schema_name: Schema name
        table_name: Table name (optional)
        permissions: List of permissions to revoke
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        if not permissions:
            permissions = ["USAGE", "CREATE"]
        
        perm_clause = ", ".join(permissions)
        
        if table_name:
            query = f"REVOKE {perm_clause} ON {schema_name}.{table_name} FROM {role}"
        else:
            query = f"REVOKE {perm_clause} ON SCHEMA {schema_name} FROM {role}"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🔐 Permissions revoked from {role}")
        return {"success": True, "message": f"Permissions revoked from {role}"}
    except PostgresError as e:
        logger.error(f"❌ Error revoking permissions: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_list_roles() -> Dict[str, Any]:
    """List all PostgreSQL roles.
    
    Returns:
        List of roles
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute("SELECT rolname, rolsuper, rolinherit FROM pg_roles WHERE rolname NOT LIKE 'pg_%' ORDER BY rolname")
        roles = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"👥 Found {len(roles)} roles")
        return {"success": True, "roles": roles, "count": len(roles)}
    except PostgresError as e:
        logger.error(f"❌ Error listing roles: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== ADMINISTRATION TOOLS ======================

@mcp.tool()
def postgresql_vacuum_table(schema_name: str, table_name: str, analyze: bool = True) -> Dict[str, Any]:
    """Vacuum a table.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        analyze: Also run ANALYZE
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        conn.autocommit = True
        cursor = conn.cursor()
        
        query = f"VACUUM"
        if analyze:
            query += " ANALYZE"
        query += f" {schema_name}.{table_name}"
        
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"🧹 Table vacuumed: {schema_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' vacuumed"}
    except PostgresError as e:
        logger.error(f"❌ Error vacuuming table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_create_index(schema_name: str, table_name: str, index_name: str, columns: List[str]) -> Dict[str, Any]:
    """Create an index on a table.
    
    Args:
        schema_name: Schema name
        table_name: Table name
        index_name: Index name
        columns: List of columns to index
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        col_clause = ", ".join(columns)
        query = f"CREATE INDEX {index_name} ON {schema_name}.{table_name} ({col_clause})"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"📑 Index created: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' created"}
    except PostgresError as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_drop_index(schema_name: str, index_name: str) -> Dict[str, Any]:
    """Drop an index.
    
    Args:
        schema_name: Schema name
        index_name: Index name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP INDEX {schema_name}.{index_name}")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Index dropped: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' dropped"}
    except PostgresError as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def postgresql_get_table_size(schema_name: str, table_name: str) -> Dict[str, Any]:
    """Get table size and statistics.
    
    Args:
        schema_name: Schema name
        table_name: Table name
    
    Returns:
        Size information
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor(cursor_factory=DictCursor)
        query = f"SELECT pg_size_pretty(pg_total_relation_size('{schema_name}.{table_name}')) as size, pg_total_relation_size('{schema_name}.{table_name}') as size_bytes"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        logger.info(f"📏 Table size retrieved: {schema_name}.{table_name}")
        return {"success": True, "size": result["size"], "bytes": result["size_bytes"]}
    except PostgresError as e:
        logger.error(f"❌ Error getting table size: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a PostgreSQL Database Administrator. Your role is to:
- Create and manage databases, schemas, and tables
- Optimize query performance
- Manage user roles and permissions
- Monitor table size and perform maintenance
- Execute DDL and DCL operations safely

Use these tools for DBA tasks:
- postgresql_create_database, postgresql_drop_database, postgresql_list_databases
- postgresql_create_table, postgresql_describe_table, postgresql_alter_table
- postgresql_grant_permissions, postgresql_revoke_permissions, postgresql_list_roles
- postgresql_vacuum_table for maintenance
- postgresql_create_index, postgresql_drop_index
- postgresql_get_table_size for monitoring
"""

DATA_ENGINEER_PROMPT = """You are a PostgreSQL Data Engineer. Your role is to:
- Design efficient table structures with proper schemas
- Build and maintain data pipelines
- Load and transform data
- Ensure data quality and consistency
- Manage bulk operations and performance

Use these tools for data engineering:
- postgresql_insert_record, postgresql_insert_multiple_records
- postgresql_update_records, postgresql_delete_records
- postgresql_select_all, postgresql_select_where for validation
- postgresql_select_count, postgresql_select_aggregate
- postgresql_custom_query for ETL operations
- postgresql_vacuum_table for optimization
"""

DATA_ANALYST_PROMPT = """You are a PostgreSQL Data Analyst. Your role is to:
- Query and analyze data efficiently
- Generate insights and reports
- Explore data patterns and trends
- Create analytical queries
- Support business intelligence requirements

Use these tools for analysis:
- postgresql_select_all, postgresql_select_where for exploration
- postgresql_select_aggregate, postgresql_select_grouped for statistics
- postgresql_select_distinct, postgresql_select_ordered for trends
- postgresql_select_join for cross-table analysis
- postgresql_select_count for profiling
- postgresql_custom_query for complex analysis
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting PostgreSQL MCP Server...")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7085"))
    )

if __name__ == "__main__":
    asyncio.run(main())
