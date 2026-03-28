"""
PostgreSQL MCP Server using FastMCP
Provides tools for PostgreSQL database operations
"""

import asyncio
import psycopg2
from psycopg2 import Error as PostgresError
import json
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("postgresql-mcp-server")

class PostgresConnectionPool:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 5432):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port
        }
        self.connection = None
    
    async def connect(self):
        """Connect to PostgreSQL"""
        try:
            self.connection = psycopg2.connect(**self.config)
            self.connection.autocommit = False
            logger.info("Connected to PostgreSQL database")
        except PostgresError as err:
            logger.error(f"Error connecting to PostgreSQL: {err}")
            raise
    
    async def disconnect(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from PostgreSQL")
    
    async def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Execute SQL query"""
        cursor = None
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch and cursor.description:
                cols = [desc[0] for desc in cursor.description]
                result = [dict(zip(cols, row)) for row in cursor.fetchall()]
                self.connection.commit()
                return result
            else:
                self.connection.commit()
                return {"rows_affected": cursor.rowcount}
        except PostgresError as err:
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
        query = """
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        result = await db_pool.execute_query(query)
        tables = [row["table_name"] for row in result]
        return {"success": True, "tables": tables}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """Get table structure"""
    try:
        query = """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = %s
        """
        result = await db_pool.execute_query(query, (table_name,))
        return {"success": True, "columns": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def insert_record(table_name: str, data: dict) -> dict:
    """Insert a record"""
    try:
        columns = list(data.keys())
        placeholders = ", ".join(["%s"] * len(columns))
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
        set_clause = ", ".join([f"{k}=%s" for k in data.keys()])
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
        query = """
        SELECT 
            schemaname,
            COUNT(*) as table_count,
            SUM(pg_total_relation_size(schemaname||'.'||tablename))::bigint / 1024 / 1024 as size_mb
        FROM pg_tables
        WHERE schemaname = 'public'
        GROUP BY schemaname
        """
        result = await db_pool.execute_query(query)
        return {"success": True, "stats": result}
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

@mcp.tool()
async def list_indexes(table_name: str) -> dict:
    """List indexes for a table"""
    try:
        query = """
        SELECT indexname, indexdef
        FROM pg_indexes
        WHERE tablename = %s
        """
        result = await db_pool.execute_query(query, (table_name,))
        return {"success": True, "indexes": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    host = os.getenv("POSTGRES_HOST", "localhost")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    database = os.getenv("POSTGRES_DATABASE", "test")
    port = int(os.getenv("POSTGRES_PORT", "5432"))
    
    db_pool = PostgresConnectionPool(host, user, password, database, port)
    await db_pool.connect()
    
    try:
        logger.info("Starting PostgreSQL MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
