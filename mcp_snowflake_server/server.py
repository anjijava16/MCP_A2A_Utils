"""
Snowflake MCP Server ❄️
Comprehensive MCP server for Snowflake cloud data platform
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
import snowflake.connector
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Snowflake ❄️")

def get_snowflake_connection():
    """Get Snowflake connection"""
    user = os.getenv("SNOWFLAKE_USER", "")
    password = os.getenv("SNOWFLAKE_PASSWORD", "")
    account = os.getenv("SNOWFLAKE_ACCOUNT", "")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "")
    database = os.getenv("SNOWFLAKE_DATABASE", "")
    schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    
    try:
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        return conn
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

# ==================== WAREHOUSE MANAGEMENT ====================

@mcp.tool()
async def create_warehouse(warehouse_name: str, warehouse_size: str = "XSMALL", auto_suspend: int = 10) -> dict:
    """✨ Create new warehouse"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"CREATE WAREHOUSE IF NOT EXISTS {warehouse_name} WAREHOUSE_SIZE = {warehouse_size} AUTO_SUSPEND = {auto_suspend}"
        cursor.execute(sql)
        
        logger.info(f"✅ Warehouse {warehouse_name} created")
        conn.close()
        return {"success": True, "message": f"Warehouse {warehouse_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating warehouse: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_warehouses() -> dict:
    """📋 List all warehouses"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute("SHOW WAREHOUSES")
        warehouses = cursor.fetchall()
        
        logger.info(f"✅ Found {len(warehouses)} warehouses")
        conn.close()
        return {"success": True, "warehouses": [w[0] for w in warehouses], "count": len(warehouses)}
    except Exception as e:
        logger.error(f"❌ Error listing warehouses: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_warehouse(warehouse_name: str) -> dict:
    """❌ Drop warehouse"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"DROP WAREHOUSE IF EXISTS {warehouse_name}")
        
        logger.info(f"✅ Warehouse {warehouse_name} dropped")
        conn.close()
        return {"success": True, "message": f"Warehouse {warehouse_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping warehouse: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def suspend_warehouse(warehouse_name: str) -> dict:
    """⏸️ Suspend warehouse"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"ALTER WAREHOUSE {warehouse_name} SUSPEND")
        
        logger.info(f"✅ Warehouse {warehouse_name} suspended")
        conn.close()
        return {"success": True, "message": f"Warehouse suspended"}
    except Exception as e:
        logger.error(f"❌ Error suspending warehouse: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def resume_warehouse(warehouse_name: str) -> dict:
    """▶️ Resume warehouse"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"ALTER WAREHOUSE {warehouse_name} RESUME")
        
        logger.info(f"✅ Warehouse {warehouse_name} resumed")
        conn.close()
        return {"success": True, "message": f"Warehouse resumed"}
    except Exception as e:
        logger.error(f"❌ Error resuming warehouse: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def scale_warehouse(warehouse_name: str, warehouse_size: str) -> dict:
    """📈 Scale warehouse size"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"ALTER WAREHOUSE {warehouse_name} SET WAREHOUSE_SIZE = {warehouse_size}")
        
        logger.info(f"✅ Warehouse scaled to {warehouse_size}")
        conn.close()
        return {"success": True, "message": f"Warehouse scaled"}
    except Exception as e:
        logger.error(f"❌ Error scaling warehouse: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DATABASE & SCHEMA OPERATIONS ====================

@mcp.tool()
async def create_database(database_name: str) -> dict:
    """✨ Create database"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        
        logger.info(f"✅ Database {database_name} created")
        conn.close()
        return {"success": True, "message": f"Database {database_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_databases() -> dict:
    """📋 List databases"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        
        logger.info(f"✅ Found {len(databases)} databases")
        conn.close()
        return {"success": True, "databases": [d[1] for d in databases], "count": len(databases)}
    except Exception as e:
        logger.error(f"❌ Error listing databases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_schema(database_name: str, schema_name: str) -> dict:
    """✨ Create schema"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {database_name}.{schema_name}")
        
        logger.info(f"✅ Schema {schema_name} created")
        conn.close()
        return {"success": True, "message": f"Schema {schema_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating schema: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_schemas(database_name: str) -> dict:
    """📋 List schemas in database"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SHOW SCHEMAS IN DATABASE {database_name}")
        schemas = cursor.fetchall()
        
        logger.info(f"✅ Found {len(schemas)} schemas")
        conn.close()
        return {"success": True, "schemas": [s[1] for s in schemas], "count": len(schemas)}
    except Exception as e:
        logger.error(f"❌ Error listing schemas: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== TABLE OPERATIONS ====================

@mcp.tool()
async def create_table(database_name: str, schema_name: str, table_name: str, columns: List[Dict]) -> dict:
    """✨ Create table"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        col_defs = ", ".join([f"{c['name']} {c['type']}" for c in columns])
        sql = f"CREATE TABLE IF NOT EXISTS {database_name}.{schema_name}.{table_name} ({col_defs})"
        cursor.execute(sql)
        
        logger.info(f"✅ Table {table_name} created")
        conn.close()
        return {"success": True, "message": f"Table {table_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_tables(database_name: str, schema_name: str) -> dict:
    """📋 List tables in schema"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SHOW TABLES IN {database_name}.{schema_name}")
        tables = cursor.fetchall()
        
        logger.info(f"✅ Found {len(tables)} tables")
        conn.close()
        return {"success": True, "tables": [t[1] for t in tables], "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(database_name: str, schema_name: str, table_name: str) -> dict:
    """🔎 Describe table structure"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"DESCRIBE TABLE {database_name}.{schema_name}.{table_name}")
        columns = cursor.fetchall()
        
        col_info = [{"name": c[0], "type": c[1]} for c in columns]
        logger.info(f"✅ Retrieved table schema")
        conn.close()
        return {"success": True, "columns": col_info, "count": len(col_info)}
    except Exception as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_table(database_name: str, schema_name: str, table_name: str) -> dict:
    """🗑️ Drop table"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"DROP TABLE IF EXISTS {database_name}.{schema_name}.{table_name}")
        
        logger.info(f"✅ Table {table_name} dropped")
        conn.close()
        return {"success": True, "message": f"Table {table_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def add_column(database_name: str, schema_name: str, table_name: str, column_name: str, column_type: str) -> dict:
    """➕ Add column to table"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"ALTER TABLE {database_name}.{schema_name}.{table_name} ADD COLUMN {column_name} {column_type}"
        cursor.execute(sql)
        
        logger.info(f"✅ Column {column_name} added")
        conn.close()
        return {"success": True, "message": f"Column added"}
    except Exception as e:
        logger.error(f"❌ Error adding column: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DML OPERATIONS ====================

@mcp.tool()
async def insert_rows(database_name: str, schema_name: str, table_name: str, rows: List[Dict]) -> dict:
    """✍️ Insert rows"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        if not rows:
            return {"success": False, "error": "No rows provided"}
        
        columns = list(rows[0].keys())
        col_list = ", ".join(columns)
        
        values_list = []
        for row in rows:
            values = ", ".join([f"'{row[col]}'" if isinstance(row[col], str) else str(row[col]) for col in columns])
            values_list.append(f"({values})")
        
        sql = f"INSERT INTO {database_name}.{schema_name}.{table_name} ({col_list}) VALUES {', '.join(values_list)}"
        cursor.execute(sql)
        
        logger.info(f"✅ Inserted {len(rows)} rows")
        conn.close()
        return {"success": True, "inserted_count": len(rows)}
    except Exception as e:
        logger.error(f"❌ Error inserting rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_rows(database_name: str, schema_name: str, table_name: str, set_clause: str, where_clause: str) -> dict:
    """🔄 Update rows"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"UPDATE {database_name}.{schema_name}.{table_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(sql)
        
        affected = cursor.rowcount
        logger.info(f"✅ Updated {affected} rows")
        conn.close()
        return {"success": True, "affected_count": affected}
    except Exception as e:
        logger.error(f"❌ Error updating rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_rows(database_name: str, schema_name: str, table_name: str, where_clause: str) -> dict:
    """🗑️ Delete rows"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"DELETE FROM {database_name}.{schema_name}.{table_name} WHERE {where_clause}"
        cursor.execute(sql)
        
        affected = cursor.rowcount
        logger.info(f"✅ Deleted {affected} rows")
        conn.close()
        return {"success": True, "deleted_count": affected}
    except Exception as e:
        logger.error(f"❌ Error deleting rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def bulk_insert_from_stage(database_name: str, schema_name: str, table_name: str, stage_path: str) -> dict:
    """⚡ Bulk insert from stage"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"COPY INTO {database_name}.{schema_name}.{table_name} FROM @{stage_path}"
        cursor.execute(sql)
        
        logger.info(f"✅ Bulk insert completed")
        conn.close()
        return {"success": True, "message": "Bulk insert completed"}
    except Exception as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== QUERY OPERATIONS ====================

@mcp.tool()
async def execute_query(query: str) -> dict:
    """🔍 Execute custom query"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        logger.info(f"✅ Query executed, {len(results)} rows returned")
        conn.close()
        return {"success": True, "results": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ Error executing query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def select_all(database_name: str, schema_name: str, table_name: str, limit: int = 100) -> dict:
    """📖 Select all rows with limit"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {database_name}.{schema_name}.{table_name} LIMIT {limit}"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        logger.info(f"✅ Retrieved {len(results)} rows")
        conn.close()
        return {"success": True, "rows": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ Error selecting rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def count_rows(database_name: str, schema_name: str, table_name: str) -> dict:
    """📊 Count rows in table"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"SELECT COUNT(*) FROM {database_name}.{schema_name}.{table_name}"
        cursor.execute(sql)
        count = cursor.fetchone()[0]
        
        logger.info(f"✅ Row count: {count}")
        conn.close()
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ Error counting rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def explain_query(query: str) -> dict:
    """⚙️ Explain query plan"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"EXPLAIN {query}"
        cursor.execute(sql)
        plan = cursor.fetchall()
        
        logger.info(f"✅ Query plan retrieved")
        conn.close()
        return {"success": True, "plan": [str(p) for p in plan]}
    except Exception as e:
        logger.error(f"❌ Error explaining query: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== VIEW OPERATIONS ====================

@mcp.tool()
async def create_view(database_name: str, schema_name: str, view_name: str, query: str) -> dict:
    """🪟 Create view"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"CREATE VIEW IF NOT EXISTS {database_name}.{schema_name}.{view_name} AS {query}"
        cursor.execute(sql)
        
        logger.info(f"✅ View {view_name} created")
        conn.close()
        return {"success": True, "message": f"View {view_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating view: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_view(database_name: str, schema_name: str, view_name: str) -> dict:
    """🗑️ Drop view"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"DROP VIEW IF EXISTS {database_name}.{schema_name}.{view_name}")
        
        logger.info(f"✅ View {view_name} dropped")
        conn.close()
        return {"success": True, "message": f"View {view_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping view: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ACCESS CONTROL ====================

@mcp.tool()
async def create_role(role_name: str) -> dict:
    """👤 Create role"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE ROLE IF NOT EXISTS {role_name}")
        
        logger.info(f"✅ Role {role_name} created")
        conn.close()
        return {"success": True, "message": f"Role {role_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating role: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def grant_privilege(role_name: str, privilege: str, object_type: str, object_name: str) -> dict:
    """🔐 Grant privilege"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"GRANT {privilege} ON {object_type} {object_name} TO ROLE {role_name}"
        cursor.execute(sql)
        
        logger.info(f"✅ Privilege granted")
        conn.close()
        return {"success": True, "message": "Privilege granted"}
    except Exception as e:
        logger.error(f"❌ Error granting privilege: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def revoke_privilege(role_name: str, privilege: str, object_type: str, object_name: str) -> dict:
    """🔓 Revoke privilege"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        sql = f"REVOKE {privilege} ON {object_type} {object_name} FROM ROLE {role_name}"
        cursor.execute(sql)
        
        logger.info(f"✅ Privilege revoked")
        conn.close()
        return {"success": True, "message": "Privilege revoked"}
    except Exception as e:
        logger.error(f"❌ Error revoking privilege: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ADMIN OPERATIONS ====================

@mcp.tool()
async def get_account_info() -> dict:
    """📋 Get account information"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT CURRENT_ACCOUNT(), CURRENT_USER(), CURRENT_WAREHOUSE()")
        info = cursor.fetchone()
        
        logger.info(f"✅ Retrieved account info")
        conn.close()
        return {"success": True, "account": info[0], "user": info[1], "warehouse": info[2]}
    except Exception as e:
        logger.error(f"❌ Error getting account info: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_queries(limit: int = 10) -> dict:
    """📜 List recent queries"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT QUERY_ID, QUERY_TEXT, EXECUTION_TIME FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY(RESULT_LIMIT => {limit}))")
        queries = cursor.fetchall()
        
        logger.info(f"✅ Retrieved {len(queries)} queries")
        conn.close()
        return {"success": True, "queries": [{"id": q[0], "text": q[1], "time_ms": q[2]} for q in queries]}
    except Exception as e:
        logger.error(f"❌ Error listing queries: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def show_parameters(warehouse_name: str = None) -> dict:
    """⚙️ Show warehouse parameters"""
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        if warehouse_name:
            cursor.execute(f"SHOW PARAMETERS IN WAREHOUSE {warehouse_name}")
        else:
            cursor.execute("SHOW PARAMETERS")
        
        params = cursor.fetchall()
        
        logger.info(f"✅ Retrieved {len(params)} parameters")
        conn.close()
        return {"success": True, "parameters": [{"key": p[0], "value": p[1]} for p in params], "count": len(params)}
    except Exception as e:
        logger.error(f"❌ Error showing parameters: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Snowflake MCP server"""
    try:
        logger.info("❄️ Starting Snowflake MCP Server on port 7098")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7098)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
Data Warehouse Administrator Prompt:
You are a Data Warehouse Administrator managing Snowflake infrastructure. Help manage warehouses,
databases, schemas, tables, and optimize performance with proper scaling and configuration.

Data Engineer Prompt:
You are a Data Engineer building data pipelines with Snowflake. Help design schemas, manage data loading,
create views, and optimize ETL processes for large-scale data movement.

Analytics Engineer Prompt:
You are an Analytics Engineer creating analytics-ready datasets in Snowflake. Help design dimensional models,
create views and queries for BI tools, and manage data quality and transformations.
"""
