import asyncio
import logging
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
import mysql.connector
from mysql.connector import Error as MySQLError
from fastmcp import FastMCP

# Configure logging with emoji
logging.basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("MySQL MCP Server 🗄️")

# Configuration from environment
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "mysql"),
}

def get_mysql_connection() -> mysql.connector.MySQLConnection:
    """Get MySQL connection with configuration from environment."""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        logger.info(f"✅ Connected to MySQL: {MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}")
        return conn
    except MySQLError as e:
        logger.error(f"❌ MySQL connection error: {str(e)}")
        raise

# ====================== DDL TOOLS ======================

@mcp.tool()
def mysql_create_database(database_name: str, charset: str = "utf8mb4", collation: Optional[str] = None) -> Dict[str, Any]:
    """Create a new database.
    
    Args:
        database_name: Database name
        charset: Character set (default: utf8mb4)
        collation: Collation (default: utf8mb4_unicode_ci)
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        charset_clause = f"CHARACTER SET {charset}"
        collation_clause = f"COLLATE {collation}" if collation else ""
        query = f"CREATE DATABASE `{database_name}` {charset_clause} {collation_clause}"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"📦 Database created: {database_name}")
        return {"success": True, "message": f"Database '{database_name}' created"}
    except MySQLError as e:
        logger.error(f"❌ Error creating database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_drop_database(database_name: str) -> Dict[str, Any]:
    """Drop a database.
    
    Args:
        database_name: Database name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE `{database_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Database dropped: {database_name}")
        return {"success": True, "message": f"Database '{database_name}' dropped"}
    except MySQLError as e:
        logger.error(f"❌ Error dropping database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_list_databases() -> Dict[str, Any]:
    """List all databases.
    
    Returns:
        List of database names
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📋 Found {len(databases)} databases")
        return {"success": True, "databases": databases, "count": len(databases)}
    except MySQLError as e:
        logger.error(f"❌ Error listing databases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_create_table(database_name: str, table_name: str, columns: str, 
                      primary_key: Optional[str] = None, engine: str = "InnoDB") -> Dict[str, Any]:
    """Create a new table.
    
    Args:
        database_name: Database name
        table_name: Table name
        columns: Column definitions (col1 INT, col2 VARCHAR(255), ...)
        primary_key: Primary key column(s)
        engine: Storage engine (InnoDB, MyISAM)
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        pk_clause = f", PRIMARY KEY ({primary_key})" if primary_key else ""
        query = f"CREATE TABLE `{database_name}`.`{table_name}` ({columns}{pk_clause}) ENGINE={engine}"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🏗️ Table created: {database_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' created in '{database_name}'"}
    except MySQLError as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_drop_table(database_name: str, table_name: str) -> Dict[str, Any]:
    """Drop a table.
    
    Args:
        database_name: Database name
        table_name: Table name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE `{database_name}`.`{table_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Table dropped: {database_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' dropped"}
    except MySQLError as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_list_tables(database_name: str) -> Dict[str, Any]:
    """List all tables in a database.
    
    Args:
        database_name: Database name
    
    Returns:
        List of table names
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s", (database_name,))
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"📋 Found {len(tables)} tables in {database_name}")
        return {"success": True, "tables": tables, "count": len(tables)}
    except MySQLError as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_describe_table(database_name: str, table_name: str) -> Dict[str, Any]:
    """Describe table structure.
    
    Args:
        database_name: Database name
        table_name: Table name
    
    Returns:
        Table schema information
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE `{database_name}`.`{table_name}`")
        columns = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"📊 Table described: {database_name}.{table_name}")
        return {"success": True, "columns": columns, "count": len(columns)}
    except MySQLError as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_alter_table(database_name: str, table_name: str, alter_clause: str) -> Dict[str, Any]:
    """Alter table structure.
    
    Args:
        database_name: Database name
        table_name: Table name
        alter_clause: ALTER clause (ADD COLUMN col INT, DROP COLUMN col, etc.)
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = f"ALTER TABLE `{database_name}`.`{table_name}` {alter_clause}"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✏️ Table altered: {database_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' altered successfully"}
    except MySQLError as e:
        logger.error(f"❌ Error altering table: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS ======================

@mcp.tool()
def mysql_insert_record(database_name: str, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single record.
    
    Args:
        database_name: Database name
        table_name: Table name
        record: Record data as dictionary
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        columns = ", ".join([f"`{k}`" for k in record.keys()])
        placeholders = ", ".join(["%s"] * len(record))
        query = f"INSERT INTO `{database_name}`.`{table_name}` ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, tuple(record.values()))
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"➕ Record inserted into {database_name}.{table_name}")
        return {"success": True, "message": "Record inserted successfully"}
    except MySQLError as e:
        logger.error(f"❌ Error inserting record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_insert_multiple_records(database_name: str, table_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple records.
    
    Args:
        database_name: Database name
        table_name: Table name
        records: List of records
    
    Returns:
        Success status and row count
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        if not records:
            return {"success": True, "message": "No records to insert", "inserted": 0}
        
        columns = ", ".join([f"`{k}`" for k in records[0].keys()])
        placeholders = ", ".join(["%s"] * len(records[0]))
        query = f"INSERT INTO `{database_name}`.`{table_name}` ({columns}) VALUES ({placeholders})"
        
        values = [tuple(record.values()) for record in records]
        cursor.executemany(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"➕ {len(records)} records inserted into {database_name}.{table_name}")
        return {"success": True, "message": f"{len(records)} records inserted", "inserted": len(records)}
    except MySQLError as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_update_records(database_name: str, table_name: str, set_clause: str, 
                        where_clause: Optional[str] = None) -> Dict[str, Any]:
    """Update records.
    
    Args:
        database_name: Database name
        table_name: Table name
        set_clause: SET clause (col1=val1, col2=val2)
        where_clause: WHERE condition
    
    Returns:
        Success status and affected rows
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        query = f"UPDATE `{database_name}`.`{table_name}` SET {set_clause}"
        if where_clause:
            query += f" WHERE {where_clause}"
        
        cursor.execute(query)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        
        logger.info(f"✏️ {affected} records updated in {database_name}.{table_name}")
        return {"success": True, "message": f"{affected} records updated", "affected": affected}
    except MySQLError as e:
        logger.error(f"❌ Error updating records: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_delete_records(database_name: str, table_name: str, where_clause: str) -> Dict[str, Any]:
    """Delete records.
    
    Args:
        database_name: Database name
        table_name: Table name
        where_clause: WHERE condition
    
    Returns:
        Success status and deleted rows
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        query = f"DELETE FROM `{database_name}`.`{table_name}` WHERE {where_clause}"
        cursor.execute(query)
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ {deleted} records deleted from {database_name}.{table_name}")
        return {"success": True, "message": f"{deleted} records deleted", "deleted": deleted}
    except MySQLError as e:
        logger.error(f"❌ Error deleting records: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SELECT/QUERY TOOLS ======================

@mcp.tool()
def mysql_select_all(database_name: str, table_name: str, limit: int = 1000) -> Dict[str, Any]:
    """Select all records from a table.
    
    Args:
        database_name: Database name
        table_name: Table name
        limit: Maximum rows to return
    
    Returns:
        Query results
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM `{database_name}`.`{table_name}` LIMIT {limit}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 SELECT all: {len(rows)} rows from {database_name}.{table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except MySQLError as e:
        logger.error(f"❌ SELECT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_where(database_name: str, table_name: str, where_clause: str, limit: int = 1000) -> Dict[str, Any]:
    """Select records with WHERE condition.
    
    Args:
        database_name: Database name
        table_name: Table name
        where_clause: WHERE condition
        limit: Maximum rows
    
    Returns:
        Query results
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM `{database_name}`.`{table_name}` WHERE {where_clause} LIMIT {limit}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 SELECT WHERE: {len(rows)} rows from {database_name}.{table_name}")
        return {"success": True, "rows": rows, "count": len(rows)}
    except MySQLError as e:
        logger.error(f"❌ SELECT WHERE error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_count(database_name: str, table_name: str) -> Dict[str, Any]:
    """Count total records in a table.
    
    Args:
        database_name: Database name
        table_name: Table name
    
    Returns:
        Record count
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM `{database_name}`.`{table_name}`")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"🔢 COUNT: {count} rows in {database_name}.{table_name}")
        return {"success": True, "count": count}
    except MySQLError as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_aggregate(database_name: str, table_name: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute aggregate query (SUM, AVG, MIN, MAX, COUNT).
    
    Args:
        database_name: Database name
        table_name: Table name
        agg_column: Column to aggregate
        agg_function: Function (SUM, AVG, MIN, MAX, COUNT)
    
    Returns:
        Aggregate result
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = f"SELECT {agg_function}({agg_column}) FROM `{database_name}`.`{table_name}`"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        logger.info(f"📊 {agg_function} of {agg_column}: {result}")
        return {"success": True, "result": result, "function": agg_function}
    except MySQLError as e:
        logger.error(f"❌ Aggregate error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_distinct(database_name: str, table_name: str, column: str) -> Dict[str, Any]:
    """Get distinct values from a column.
    
    Args:
        database_name: Database name
        table_name: Table name
        column: Column name
    
    Returns:
        List of distinct values
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = f"SELECT DISTINCT `{column}` FROM `{database_name}`.`{table_name}` LIMIT 1000"
        cursor.execute(query)
        values = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"🔍 DISTINCT {column}: {len(values)} values")
        return {"success": True, "values": values, "count": len(values)}
    except MySQLError as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_grouped(database_name: str, table_name: str, group_by: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute GROUP BY query.
    
    Args:
        database_name: Database name
        table_name: Table name
        group_by: Column to group by
        agg_column: Column to aggregate
        agg_function: Aggregate function
    
    Returns:
        Grouped results
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT `{group_by}`, {agg_function}(`{agg_column}`) as result FROM `{database_name}`.`{table_name}` GROUP BY `{group_by}` LIMIT 1000"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"📊 GROUP BY {group_by}: {len(rows)} groups")
        return {"success": True, "rows": rows, "count": len(rows)}
    except MySQLError as e:
        logger.error(f"❌ GROUP BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_ordered(database_name: str, table_name: str, order_by: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Select records with ORDER BY.
    
    Args:
        database_name: Database name
        table_name: Table name
        order_by: Column to order by
        direction: ASC or DESC
        limit: Maximum rows
    
    Returns:
        Ordered results
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM `{database_name}`.`{table_name}` ORDER BY `{order_by}` {direction} LIMIT {limit}"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 ORDER BY {order_by}: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except MySQLError as e:
        logger.error(f"❌ ORDER BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_select_join(database_name: str, table1: str, table2: str, join_column: str, join_type: str = "INNER") -> Dict[str, Any]:
    """Execute JOIN query between two tables.
    
    Args:
        database_name: Database name
        table1: First table
        table2: Second table
        join_column: Column to join on
        join_type: INNER, LEFT, RIGHT, FULL
    
    Returns:
        Join results
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM `{database_name}`.`{table1}` {join_type} JOIN `{database_name}`.`{table2}` ON `{table1}`.`{join_column}` = `{table2}`.`{join_column}` LIMIT 1000"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔗 {join_type} JOIN: {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except MySQLError as e:
        logger.error(f"❌ JOIN error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_custom_query(database_name: str, sql: str) -> Dict[str, Any]:
    """Execute a custom SQL query.
    
    Args:
        database_name: Database name
        sql: SQL query to execute
    
    Returns:
        Query results
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        logger.info(f"🔎 Custom query executed")
        return {"success": True, "rows": rows, "count": len(rows)}
    except MySQLError as e:
        logger.error(f"❌ Query error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DCL TOOLS ======================

@mcp.tool()
def mysql_grant_permissions(user: str, database_name: str, permissions: List[str]) -> Dict[str, Any]:
    """Grant permissions to a user.
    
    Args:
        user: Username
        database_name: Database name
        permissions: List of permissions (SELECT, INSERT, UPDATE, DELETE, ALL)
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        perm_clause = ", ".join(permissions)
        query = f"GRANT {perm_clause} ON `{database_name}`.* TO '{user}'@'%'"
        
        cursor.execute(query)
        cursor.execute("FLUSH PRIVILEGES")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🔐 Permissions granted to {user}")
        return {"success": True, "message": f"Permissions granted to {user}"}
    except MySQLError as e:
        logger.error(f"❌ Error granting permissions: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_revoke_permissions(user: str, database_name: str, permissions: List[str]) -> Dict[str, Any]:
    """Revoke permissions from a user.
    
    Args:
        user: Username
        database_name: Database name
        permissions: List of permissions to revoke
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        perm_clause = ", ".join(permissions)
        query = f"REVOKE {perm_clause} ON `{database_name}`.* FROM '{user}'@'%'"
        
        cursor.execute(query)
        cursor.execute("FLUSH PRIVILEGES")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🔐 Permissions revoked from {user}")
        return {"success": True, "message": f"Permissions revoked from {user}"}
    except MySQLError as e:
        logger.error(f"❌ Error revoking permissions: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_list_users() -> Dict[str, Any]:
    """List all MySQL users.
    
    Returns:
        List of users
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT User, Host FROM mysql.user")
        users = [{"user": row[0], "host": row[1]} for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"👥 Found {len(users)} users")
        return {"success": True, "users": users, "count": len(users)}
    except MySQLError as e:
        logger.error(f"❌ Error listing users: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== ADMINISTRATION TOOLS ======================

@mcp.tool()
def mysql_optimize_table(database_name: str, table_name: str) -> Dict[str, Any]:
    """Optimize a table.
    
    Args:
        database_name: Database name
        table_name: Table name
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"OPTIMIZE TABLE `{database_name}`.`{table_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"⚡ Table optimized: {database_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' optimized"}
    except MySQLError as e:
        logger.error(f"❌ Error optimizing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_repair_table(database_name: str, table_name: str) -> Dict[str, Any]:
    """Repair a table.
    
    Args:
        database_name: Database name
        table_name: Table name
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"REPAIR TABLE `{database_name}`.`{table_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🔧 Table repaired: {database_name}.{table_name}")
        return {"success": True, "message": f"Table '{table_name}' repaired"}
    except MySQLError as e:
        logger.error(f"❌ Error repairing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_show_table_status(database_name: str, table_name: str) -> Dict[str, Any]:
    """Show table status and statistics.
    
    Args:
        database_name: Database name
        table_name: Table name
    
    Returns:
        Table status information
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SHOW TABLE STATUS FROM `{database_name}` WHERE Name = %s", (table_name,))
        status = cursor.fetchone()
        cursor.close()
        conn.close()
        
        logger.info(f"📊 Table status retrieved: {database_name}.{table_name}")
        return {"success": True, "status": status}
    except MySQLError as e:
        logger.error(f"❌ Error getting table status: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_create_index(database_name: str, table_name: str, index_name: str, columns: List[str]) -> Dict[str, Any]:
    """Create an index on a table.
    
    Args:
        database_name: Database name
        table_name: Table name
        index_name: Index name
        columns: List of columns to index
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        
        col_clause = ", ".join([f"`{col}`" for col in columns])
        query = f"CREATE INDEX `{index_name}` ON `{database_name}`.`{table_name}` ({col_clause})"
        
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"📑 Index created: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' created"}
    except MySQLError as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def mysql_drop_index(database_name: str, table_name: str, index_name: str) -> Dict[str, Any]:
    """Drop an index from a table.
    
    Args:
        database_name: Database name
        table_name: Table name
        index_name: Index name to drop
    
    Returns:
        Success status
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(f"DROP INDEX `{index_name}` ON `{database_name}`.`{table_name}`")
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"🗑️ Index dropped: {index_name}")
        return {"success": True, "message": f"Index '{index_name}' dropped"}
    except MySQLError as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a MySQL Database Administrator. Your role is to:
- Create and manage databases and tables
- Optimize query performance
- Manage user permissions and security
- Monitor table integrity and perform maintenance
- Execute DDL and DCL operations safely

Use these tools for DBA tasks:
- mysql_create_database, mysql_drop_database, mysql_list_databases
- mysql_create_table, mysql_describe_table, mysql_alter_table
- mysql_grant_permissions, mysql_revoke_permissions, mysql_list_users
- mysql_optimize_table, mysql_repair_table, mysql_show_table_status
- mysql_create_index, mysql_drop_index
"""

DATA_ENGINEER_PROMPT = """You are a MySQL Data Engineer. Your role is to:
- Design efficient table structures
- Build and maintain data pipelines
- Load and transform data
- Ensure data quality and consistency
- Manage bulk operations

Use these tools for data engineering:
- mysql_insert_record, mysql_insert_multiple_records
- mysql_update_records, mysql_delete_records
- mysql_select_all, mysql_select_where for data validation
- mysql_select_count, mysql_select_aggregate
- mysql_custom_query for complex ETL operations
- mysql_show_table_status for monitoring
"""

DATA_ANALYST_PROMPT = """You are a MySQL Data Analyst. Your role is to:
- Query and analyze data
- Generate insights and reports
- Explore data patterns and trends
- Create analytical queries
- Support business intelligence

Use these tools for analysis:
- mysql_select_all, mysql_select_where for data exploration
- mysql_select_aggregate, mysql_select_grouped for summary statistics
- mysql_select_distinct, mysql_select_ordered for trend analysis
- mysql_select_join for cross-table analysis
- mysql_select_count for data profiling
- mysql_custom_query for complex analysis
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting MySQL MCP Server...")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7084"))
    )

if __name__ == "__main__":
    asyncio.run(main())
