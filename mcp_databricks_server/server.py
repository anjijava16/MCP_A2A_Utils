"""
Databricks MCP Server 📊
Comprehensive MCP server for Databricks SQL analytics, MLFlow, and data operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from databricks import sql
from botocore.exceptions import ClientError
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Databricks 📊")

def get_databricks_connection():
    """Get Databricks SQL connection"""
    hostname = os.getenv("DATABRICKS_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    token = os.getenv("DATABRICKS_TOKEN")
    
    if not all([hostname, http_path, token]):
        raise ValueError("Missing Databricks credentials: DATABRICKS_HOSTNAME, DATABRICKS_HTTP_PATH, DATABRICKS_TOKEN")
    
    try:
        conn = sql.connect(
            server_hostname=hostname,
            http_path=http_path,
            access_token=token
        )
        return conn
    except Exception as e:
        logger.error(f"❌ Connection failed: {str(e)}")
        raise

# ==================== CATALOG & SCHEMA OPERATIONS ====================

@mcp.tool()
async def list_catalogs() -> dict:
    """📚 List all catalogs (Unity Catalog)"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW CATALOGS")
        catalogs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Found {len(catalogs)} catalogs")
        return {"success": True, "catalogs": catalogs, "count": len(catalogs)}
    except Exception as e:
        logger.error(f"❌ Error listing catalogs: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_schemas(catalog: Optional[str] = None) -> dict:
    """📋 List schemas in catalog or current workspace"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        if catalog:
            cursor.execute(f"SHOW SCHEMAS IN CATALOG {catalog}")
        else:
            cursor.execute("SHOW SCHEMAS")
        
        schemas = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Found {len(schemas)} schemas")
        return {"success": True, "schemas": schemas, "count": len(schemas)}
    except Exception as e:
        logger.error(f"❌ Error listing schemas: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_schema(schema_name: str, catalog: Optional[str] = None, comment: Optional[str] = None) -> dict:
    """✨ Create new schema"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema_name}" if catalog else schema_name
        query = f"CREATE SCHEMA {full_name}"
        if comment:
            query += f" COMMENT '{comment}'"
        
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Schema {schema_name} created")
        return {"success": True, "message": f"Schema {schema_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating schema: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_schema(schema_name: str, catalog: Optional[str] = None) -> dict:
    """🔎 Get schema details"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema_name}" if catalog else schema_name
        cursor.execute(f"DESCRIBE SCHEMA {full_name}")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        schema_info = {
            "name": schema_name,
            "catalog": catalog or "default",
            "full_info": str(result)
        }
        
        logger.info(f"✅ Retrieved schema info")
        return {"success": True, "schema": schema_info}
    except Exception as e:
        logger.error(f"❌ Error describing schema: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_schema(schema_name: str, catalog: Optional[str] = None, cascade: bool = False) -> dict:
    """🗑️ Drop schema"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema_name}" if catalog else schema_name
        cascade_str = "CASCADE" if cascade else ""
        cursor.execute(f"DROP SCHEMA {full_name} {cascade_str}")
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Schema {schema_name} dropped")
        return {"success": True, "message": f"Schema {schema_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping schema: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== TABLE DDL OPERATIONS ====================

@mcp.tool()
async def list_tables(schema: str, catalog: Optional[str] = None) -> dict:
    """📑 List tables in schema"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}" if catalog else schema
        cursor.execute(f"SHOW TABLES IN {full_name}")
        tables = [row[1] for row in cursor.fetchall() if len(row) > 1]
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Found {len(tables)} tables")
        return {"success": True, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str, schema: str, catalog: Optional[str] = None) -> dict:
    """🔍 Get table schema and statistics"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        cursor.execute(f"DESCRIBE {full_name}")
        
        cols = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        columns = [dict(zip(cols, row)) if cols else {"info": str(row)} for row in rows]
        
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Retrieved table schema")
        return {"success": True, "columns": columns}
    except Exception as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_table(table_name: str, schema: str, columns: dict, catalog: Optional[str] = None, comment: Optional[str] = None) -> dict:
    """✍️ Create new table"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        col_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        
        query = f"CREATE TABLE {full_name} ({col_defs})"
        if comment:
            query += f" COMMENT '{comment}'"
        
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Table {table_name} created")
        return {"success": True, "message": f"Table {table_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_table(table_name: str, schema: str, catalog: Optional[str] = None) -> dict:
    """❌ Drop table"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        cursor.execute(f"DROP TABLE {full_name}")
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Table {table_name} dropped")
        return {"success": True, "message": f"Table {table_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def add_column(table_name: str, schema: str, column_name: str, data_type: str, catalog: Optional[str] = None) -> dict:
    """➕ Add column to table"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        cursor.execute(f"ALTER TABLE {full_name} ADD COLUMN {column_name} {data_type}")
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Column {column_name} added")
        return {"success": True, "message": f"Column {column_name} added"}
    except Exception as e:
        logger.error(f"❌ Error adding column: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== TABLE DML OPERATIONS ====================

@mcp.tool()
async def insert_into(table_name: str, schema: str, data: dict, catalog: Optional[str] = None) -> dict:
    """✍️ Insert single row"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        cols = ", ".join(data.keys())
        vals = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
        
        query = f"INSERT INTO {full_name} ({cols}) VALUES ({vals})"
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Row inserted into {table_name}")
        return {"success": True, "message": "Row inserted"}
    except Exception as e:
        logger.error(f"❌ Error inserting row: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_table(table_name: str, schema: str, updates: dict, where_clause: str, catalog: Optional[str] = None) -> dict:
    """🔄 Update rows"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        set_clause = ", ".join([f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in updates.items()])
        
        query = f"UPDATE {full_name} SET {set_clause} WHERE {where_clause}"
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Rows updated in {table_name}")
        return {"success": True, "message": "Rows updated"}
    except Exception as e:
        logger.error(f"❌ Error updating rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_from(table_name: str, schema: str, where_clause: str, catalog: Optional[str] = None) -> dict:
    """🗑️ Delete rows"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        query = f"DELETE FROM {full_name} WHERE {where_clause}"
        
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Rows deleted from {table_name}")
        return {"success": True, "message": "Rows deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def copy_into(table_name: str, schema: str, file_path: str, catalog: Optional[str] = None, format: str = "PARQUET") -> dict:
    """📦 Bulk load data from file (S3/DBFS)"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        query = f"COPY INTO {full_name} FROM '{file_path}' FILEFORMAT = {format}"
        
        cursor.execute(query)
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Data loaded from {file_path}")
        return {"success": True, "message": f"Data loaded from {file_path}"}
    except Exception as e:
        logger.error(f"❌ Error loading data: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== SQL QUERY OPERATIONS ====================

@mcp.tool()
async def execute_sql(query: str) -> dict:
    """⚡ Execute SQL query"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            cols = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            results = [dict(zip(cols, row)) if cols else {"result": str(row)} for row in rows]
            cursor.close()
            conn.close()
            
            logger.info(f"✅ Query returned {len(results)} rows")
            return {"success": True, "rows": results, "count": len(results)}
        else:
            cursor.close()
            conn.close()
            logger.info(f"✅ Query executed")
            return {"success": True, "message": "Query executed"}
    except Exception as e:
        logger.error(f"❌ Error executing query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_with_limit(query: str, limit: int = 100) -> dict:
    """📊 Run query with result limit"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        safe_query = f"{query} LIMIT {limit}"
        cursor.execute(safe_query)
        
        cols = [desc[0] for desc in cursor.description] if cursor.description else []
        rows = cursor.fetchmany(limit)
        results = [dict(zip(cols, row)) if cols else {"result": str(row)} for row in rows]
        
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Retrieved {len(results)} rows")
        return {"success": True, "rows": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ Error running query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def explain_query(query: str) -> dict:
    """🔍 Get query execution plan"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN {query}")
        
        rows = cursor.fetchall()
        plan = "\n".join([str(row[0]) for row in rows])
        
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Retrieved execution plan")
        return {"success": True, "plan": plan}
    except Exception as e:
        logger.error(f"❌ Error explaining query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def analyze_table(table_name: str, schema: str, catalog: Optional[str] = None) -> dict:
    """📈 Refresh table statistics"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        cursor.execute(f"ANALYZE TABLE {full_name} COMPUTE STATISTICS")
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Statistics analyzed for {table_name}")
        return {"success": True, "message": f"Statistics computed for {table_name}"}
    except Exception as e:
        logger.error(f"❌ Error analyzing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_table_stats(table_name: str, schema: str, catalog: Optional[str] = None) -> dict:
    """📊 Get detailed table statistics"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{table_name}" if catalog else f"{schema}.{table_name}"
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {full_name}")
        row_count = cursor.fetchone()[0]
        
        # Get size (approximate)
        cursor.execute(f"DESCRIBE EXTENDED {full_name}")
        rows = cursor.fetchall()
        size_info = "N/A"
        for row in rows:
            if row and "Location" in str(row):
                size_info = str(row)
        
        cursor.close()
        conn.close()
        
        stats = {
            "table": table_name,
            "row_count": row_count,
            "size_info": size_info
        }
        
        logger.info(f"✅ Retrieved table statistics")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== VIEW OPERATIONS ====================

@mcp.tool()
async def create_view(view_name: str, schema: str, query: str, catalog: Optional[str] = None, is_temp: bool = False) -> dict:
    """👁️ Create view"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{view_name}" if catalog else f"{schema}.{view_name}"
        temp_str = "TEMPORARY" if is_temp else ""
        
        cursor.execute(f"CREATE {temp_str} VIEW {full_name} AS {query}")
        cursor.close()
        conn.close()
        
        logger.info(f"✅ View {view_name} created")
        return {"success": True, "message": f"View {view_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating view: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_view(view_name: str, schema: str, catalog: Optional[str] = None) -> dict:
    """🗑️ Drop view"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        
        full_name = f"{catalog}.{schema}.{view_name}" if catalog else f"{schema}.{view_name}"
        cursor.execute(f"DROP VIEW {full_name}")
        cursor.close()
        conn.close()
        
        logger.info(f"✅ View {view_name} dropped")
        return {"success": True, "message": f"View {view_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping view: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== WORKSPACE & CLUSTER OPERATIONS ====================

@mcp.tool()
async def get_workspace_info() -> dict:
    """🏢 Get workspace information"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_database()")
        current_db = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        info = {
            "current_database": current_db,
            "workspace": os.getenv("DATABRICKS_HOSTNAME", "N/A")
        }
        
        logger.info(f"✅ Retrieved workspace info")
        return {"success": True, "info": info}
    except Exception as e:
        logger.error(f"❌ Error getting workspace info: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_databases() -> dict:
    """📚 List all databases"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall() if row]
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Found {len(databases)} databases")
        return {"success": True, "databases": databases, "count": len(databases)}
    except Exception as e:
        logger.error(f"❌ Error listing databases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_database_objects(schema: str) -> dict:
    """🔎 Get all objects in schema"""
    try:
        conn = get_databricks_connection()
        cursor = conn.cursor()
        cursor.execute(f"SHOW OBJECTS IN {schema}")
        objects = cursor.fetchall()
        cursor.close()
        conn.close()
        
        obj_list = [{"name": obj[0], "type": obj[1]} if len(obj) > 1 else {"name": str(obj)} for obj in objects]
        
        logger.info(f"✅ Found {len(obj_list)} objects")
        return {"success": True, "objects": obj_list, "count": len(obj_list)}
    except Exception as e:
        logger.error(f"❌ Error listing objects: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Databricks MCP server"""
    try:
        logger.info("🚀 Starting Databricks MCP Server on port 7091")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7091)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
DBA Operations Prompt:
You are a Databricks Database Administrator. Help manage catalogs, schemas, table architecture, 
and optimize SQL execution. Focus on data governance, performance tuning, and workspace management.

Data Engineer Prompt:
You are a Data Engineer using Databricks for ETL/ELT pipelines. Help design efficient table schemas, 
bulk data loading via COPY INTO, table optimization, and staging area management. Focus on data quality 
and pipeline reliability.

Analytics Engineer Prompt:
You are an Analytics Engineer building data models in Databricks. Help create views, optimize queries 
for BI tools, manage dimension tables, fact tables, and ensure data integrity for analytics consumption.
"""
