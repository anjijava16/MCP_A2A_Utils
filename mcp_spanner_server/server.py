"""
Google Cloud Spanner MCP Server using FastMCP
Provides tools for Google Cloud Spanner operations
"""

import asyncio
from google.cloud import spanner
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("spanner-mcp-server")

class SpannerConnectionPool:
    def __init__(self, project_id: str, instance_id: str, database_id: str):
        self.project_id = project_id
        self.instance_id = instance_id
        self.database_id = database_id
        
        self.client = spanner.Client(project=project_id)
        self.instance = self.client.instance(instance_id)
        self.database = self.instance.database(database_id)
        logger.info(f"Connected to Spanner: {project_id}/{instance_id}/{database_id}")

db_pool = None

@mcp.tool()
async def execute_query(query: str, parameters: dict = None) -> dict:
    """Execute Spanner query"""
    try:
        with db_pool.database.snapshot() as snapshot:
            params = parameters or {}
            result = snapshot.execute_sql(query, params)
            rows = [row for row in result]
            return {"success": True, "rows": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_tables() -> dict:
    """List tables in database"""
    try:
        query = "SELECT t.table_name FROM information_schema.tables AS t WHERE t.table_schema = 'public'"
        with db_pool.database.snapshot() as snapshot:
            result = snapshot.execute_sql(query)
            tables = [row[0] for row in result]
        return {"success": True, "tables": tables}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """Get table schema"""
    try:
        query = f"""
        SELECT c.column_name, c.spanner_type, is_nullable
        FROM information_schema.columns c
        WHERE c.table_name = @table_name
        """
        with db_pool.database.snapshot() as snapshot:
            result = snapshot.execute_sql(query, {"table_name": table_name})
            columns = [
                {"name": row[0], "type": row[1], "nullable": row[2]}
                for row in result
            ]
        return {"success": True, "columns": columns}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_row(table_name: str, row: dict) -> dict:
    """Insert row into table"""
    try:
        columns = list(row.keys())
        values = [row[col] for col in columns]
        
        with db_pool.database.batch() as batch:
            batch.insert(table_name, columns, [values])
        
        return {"success": True, "message": "Row inserted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_row(table_name: str, key: dict, updates: dict) -> dict:
    """Update row in table"""
    try:
        row_data = {**key, **updates}
        columns = list(row_data.keys())
        values = [row_data[col] for col in columns]
        
        with db_pool.database.batch() as batch:
            batch.update(table_name, columns, [values])
        
        return {"success": True, "message": "Row updated"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_row(table_name: str, key: dict) -> dict:
    """Delete row from table"""
    try:
        key_set = spanner.KeySet([spanner.Key([key[k] for k in key.keys()])])
        
        with db_pool.database.batch() as batch:
            batch.delete(table_name, key_set)
        
        return {"success": True, "message": "Row deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_insert(table_name: str, rows: list) -> dict:
    """Batch insert rows"""
    try:
        if not rows:
            return {"success": True, "inserted_count": 0}
        
        columns = list(rows[0].keys())
        values = [[row[col] for col in columns] for row in rows]
        
        with db_pool.database.batch() as batch:
            batch.insert(table_name, columns, values)
        
        return {"success": True, "inserted_count": len(rows)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_database_info() -> dict:
    """Get database information"""
    try:
        return {
            "success": True,
            "info": {
                "project_id": db_pool.project_id,
                "instance_id": db_pool.instance_id,
                "database_id": db_pool.database_id
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    project_id = os.getenv("GCP_PROJECT_ID")
    instance_id = os.getenv("SPANNER_INSTANCE_ID", "my-instance")
    database_id = os.getenv("SPANNER_DATABASE_ID", "my-database")
    
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is required")
    
    db_pool = SpannerConnectionPool(project_id, instance_id, database_id)
    
    try:
        logger.info("Starting Spanner MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
