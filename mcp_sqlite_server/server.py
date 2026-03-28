"""
SQLite MCP Server using FastMCP
Provides tools for SQLite database operations
"""

import asyncio
import sqlite3
from sqlite3 import Error as SQLiteError
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("sqlite-mcp-server")

class SQLiteConnectionPool:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.connection = None
    
    async def connect(self):
        """Connect to SQLite"""
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connected to SQLite: {self.database_path}")
        except SQLiteError as err:
            logger.error(f"Error connecting to SQLite: {err}")
            raise
    
    async def disconnect(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from SQLite")
    
    async def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Execute SQL query"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                cols = [desc[0] for desc in cursor.description] if cursor.description else []
                result = [dict(zip(cols, row)) for row in cursor.fetchall()]
                self.connection.commit()
                return result
            else:
                self.connection.commit()
                return {"rows_affected": cursor.rowcount}
        except SQLiteError as err:
            self.connection.rollback()
            logger.error(f"Query execution error: {err}")
            raise
        finally:
            if cursor:
                cursor.close()

db_pool = None

@mcp.tool()
async def execute_sql(query: str, parameters: list = None) -> dict:
    """Execute arbitrary SQL query"""
    try:
        result = await db_pool.execute_query(query, tuple(parameters) if parameters else None)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_tables() -> dict:
    """List all tables in the database"""
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        result = await db_pool.execute_query(query)
        tables = [row["name"] for row in result]
        return {"success": True, "tables": tables}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """Get table structure"""
    try:
        query = f"PRAGMA table_info({table_name})"
        result = await db_pool.execute_query(query)
        columns = [{
            "name": row["name"],
            "type": row["type"],
            "notnull": row["notnull"],
            "pk": row["pk"]
        } for row in result]
        return {"success": True, "columns": columns}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_record(table_name: str, data: dict) -> dict:
    """Insert a record"""
    try:
        columns = list(data.keys())
        placeholders = ", ".join(["?"] * len(columns))
        col_names = ", ".join(columns)
        query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
        values = tuple(data.values())
        result = await db_pool.execute_query(query, values, fetch=False)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_record(table_name: str, where_clause: str, data: dict) -> dict:
    """Update records"""
    try:
        set_clause = ", ".join([f"{k}=?" for k in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        values = tuple(data.values())
        result = await db_pool.execute_query(query, values, fetch=False)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_record(table_name: str, where_clause: str) -> dict:
    """Delete records"""
    try:
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        result = await db_pool.execute_query(query, fetch=False)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_database_stats() -> dict:
    """Get database statistics"""
    try:
        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables = await db_pool.execute_query(tables_query)
        
        stats = {
            "table_count": len(tables),
            "tables": []
        }
        
        for table in tables:
            count_query = f"SELECT COUNT(*) as count FROM {table['name']}"
            count = await db_pool.execute_query(count_query)
            stats["tables"].append({
                "name": table["name"],
                "row_count": count[0]["count"]
            })
        
        return {"success": True, "stats": stats}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_index(index_name: str, table_name: str, columns: list) -> dict:
    """Create an index"""
    try:
        col_str = ", ".join(columns)
        query = f"CREATE INDEX {index_name} ON {table_name}({col_str})"
        result = await db_pool.execute_query(query, fetch=False)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    db_path = os.getenv("SQLITE_DATABASE", "test.db")
    
    db_pool = SQLiteConnectionPool(db_path)
    await db_pool.connect()
    
    try:
        logger.info("Starting SQLite MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
