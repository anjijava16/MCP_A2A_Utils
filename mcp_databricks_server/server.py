"""
Databricks MCP Server using FastMCP
Provides tools for Databricks SQL and data analytics operations
"""

import asyncio
from databricks import sql
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("databricks-mcp-server")

class DatabricksConnectionPool:
    def __init__(self, hostname: str, http_path: str, token: str):
        self.hostname = hostname
        self.http_path = http_path
        self.token = token
        self.connection = None
    
    async def connect(self):
        """Connect to Databricks"""
        try:
            self.connection = sql.connect(
                server_hostname=self.hostname,
                http_path=self.http_path,
                access_token=self.token
            )
            logger.info(f"Connected to Databricks: {self.hostname}")
        except Exception as err:
            logger.error(f"Error connecting to Databricks: {err}")
            raise
    
    async def disconnect(self):
        """Close Databricks connection"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from Databricks")

db_pool = None

@mcp.tool()
async def execute_sql(query: str) -> dict:
    """Execute SQL query"""
    try:
        cursor = db_pool.connection.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            cols = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            results = [dict(zip(cols, row)) for row in rows]
            return {"success": True, "rows": results}
        else:
            cursor.close()
            return {"success": True, "message": f"Query executed: {cursor.rowcount} rows affected"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_schemas() -> dict:
    """List schemas in Databricks"""
    try:
        cursor = db_pool.connection.cursor()
        cursor.execute("SHOW SCHEMAS")
        rows = cursor.fetchall()
        schemas = [row[0] for row in rows if row]
        cursor.close()
        return {"success": True, "schemas": schemas}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_tables(schema: str = None) -> dict:
    """List tables"""
    try:
        cursor = db_pool.connection.cursor()
        if schema:
            cursor.execute(f"SHOW TABLES IN {schema}")
        else:
            cursor.execute("SHOW TABLES")
        
        rows = cursor.fetchall()
        tables = [row[1] if len(row) > 1 else row[0] for row in rows if row]
        cursor.close()
        return {"success": True, "tables": tables}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str, schema: str = None) -> dict:
    """Describe table schema"""
    try:
        cursor = db_pool.connection.cursor()
        full_name = f"{schema}.{table_name}" if schema else table_name
        cursor.execute(f"DESCRIBE {full_name}")
        
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        columns = [dict(zip(cols, row)) for row in rows]
        cursor.close()
        return {"success": True, "columns": columns}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_table(table_name: str, columns: dict, schema: str = None) -> dict:
    """Create table"""
    try:
        cursor = db_pool.connection.cursor()
        col_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
        full_name = f"{schema}.{table_name}" if schema else table_name
        query = f"CREATE TABLE {full_name} ({col_defs})"
        cursor.execute(query)
        cursor.close()
        return {"success": True, "message": f"Table {table_name} created"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_data(table_name: str, data: dict, schema: str = None) -> dict:
    """Insert data into table"""
    try:
        cursor = db_pool.connection.cursor()
        full_name = f"{schema}.{table_name}" if schema else table_name
        
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {full_name} ({cols}) VALUES ({placeholders})"
        
        cursor.execute(query, list(data.values()))
        cursor.close()
        return {"success": True, "message": "Data inserted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_view(view_name: str, query: str, schema: str = None) -> dict:
    """Create view"""
    try:
        cursor = db_pool.connection.cursor()
        full_name = f"{schema}.{view_name}" if schema else view_name
        cursor.execute(f"CREATE VIEW {full_name} AS {query}")
        cursor.close()
        return {"success": True, "message": f"View {view_name} created"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def run_query_and_fetch(query: str, limit: int = 100) -> dict:
    """Run query with limit"""
    try:
        cursor = db_pool.connection.cursor()
        cursor.execute(query)
        
        cols = [desc[0] for desc in cursor.description]
        rows = cursor.fetchmany(limit)
        results = [dict(zip(cols, row)) for row in rows]
        cursor.close()
        
        return {"success": True, "rows": results, "row_count": len(results)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_database_info() -> dict:
    """Get Databricks workspace info"""
    try:
        cursor = db_pool.connection.cursor()
        cursor.execute("SELECT current_database()")
        current_db = cursor.fetchone()[0]
        cursor.close()
        
        return {
            "success": True,
            "current_database": current_db,
            "hostname": db_pool.hostname
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    hostname = os.getenv("DATABRICKS_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    token = os.getenv("DATABRICKS_TOKEN")
    
    if not all([hostname, http_path, token]):
        raise ValueError("Missing Databricks credentials in environment variables")
    
    db_pool = DatabricksConnectionPool(hostname, http_path, token)
    await db_pool.connect()
    
    try:
        logger.info("Starting Databricks MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
