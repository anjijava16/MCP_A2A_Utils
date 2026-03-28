"""
Apache Cassandra MCP Server using FastMCP
Provides tools for Cassandra distributed database operations
"""

import asyncio
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.util import uuid_from_time
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("cassandra-mcp-server")

class CassandraConnectionPool:
    def __init__(self, contact_points: list, keyspace: str, username: str = None, password: str = None):
        self.contact_points = contact_points
        self.keyspace = keyspace
        self.username = username
        self.password = password
        self.cluster = None
        self.session = None
    
    async def connect(self):
        """Connect to Cassandra cluster"""
        try:
            if self.username and self.password:
                auth = PlainTextAuthProvider(self.username, self.password)
                self.cluster = Cluster(self.contact_points, auth_provider=auth)
            else:
                self.cluster = Cluster(self.contact_points)
            
            self.session = self.cluster.connect(self.keyspace)
            logger.info(f"Connected to Cassandra cluster, keyspace: {self.keyspace}")
        except Exception as err:
            logger.error(f"Error connecting to Cassandra: {err}")
            raise
    
    async def disconnect(self):
        """Close Cassandra connection"""
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()
            logger.info("Disconnected from Cassandra")

db_pool = None

@mcp.tool()
async def execute_query(query: str, parameters: list = None) -> dict:
    """Execute CQL query"""
    try:
        if parameters:
            result = db_pool.session.execute(query, parameters)
        else:
            result = db_pool.session.execute(query)
        
        rows = []
        if result:
            for row in result:
                rows.append(dict(row._asdict()))
        
        return {"success": True, "rows": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_tables() -> dict:
    """List all tables in keyspace"""
    try:
        query = """
        SELECT table_name FROM system_schema.tables 
        WHERE keyspace_name = %s
        """
        result = db_pool.session.execute(query, [db_pool.keyspace])
        tables = [row.table_name for row in result]
        return {"success": True, "tables": tables}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """Get table schema"""
    try:
        metadata = db_pool.cluster.metadata.keyspaces[db_pool.keyspace].tables[table_name]
        columns = []
        for col_name, col in metadata.columns.items():
            columns.append({
                "name": col_name,
                "type": str(col.cql_type),
                "is_primary_key": col_name in [pk.name for pk in metadata.primary_key]
            })
        return {"success": True, "columns": columns}
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
        values = [data[col] for col in columns]
        db_pool.session.execute(query, values)
        return {"success": True, "message": "Record inserted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_record(table_name: str, where_clause: str, data: dict) -> dict:
    """Update records"""
    try:
        set_clause = ", ".join([f"{k}=%s" for k in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        values = list(data.values())
        db_pool.session.execute(query, values)
        return {"success": True, "message": "Records updated"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_record(table_name: str, where_clause: str) -> dict:
    """Delete records"""
    try:
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        db_pool.session.execute(query)
        return {"success": True, "message": "Records deleted"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_cluster_stats() -> dict:
    """Get cluster statistics"""
    try:
        stats = {
            "cluster_name": db_pool.cluster.metadata.cluster_name,
            "keyspace": db_pool.keyspace,
            "peers": len(db_pool.cluster.metadata.all_hosts())
        }
        return {"success": True, "stats": stats}
    except Exception as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    contact_points = os.getenv("CASSANDRA_CONTACT_POINTS", "localhost").split(",")
    keyspace = os.getenv("CASSANDRA_KEYSPACE", "system")
    username = os.getenv("CASSANDRA_USER")
    password = os.getenv("CASSANDRA_PASSWORD")
    
    db_pool = CassandraConnectionPool(contact_points, keyspace, username, password)
    await db_pool.connect()
    
    try:
        logger.info("Starting Cassandra MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    finally:
        await db_pool.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
