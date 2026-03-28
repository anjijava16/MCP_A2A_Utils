"""
Google Cloud Spanner MCP Server 🌍
Comprehensive MCP server for Spanner distributed SQL database operations
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from google.cloud import spanner
from google.api_core.exceptions import AlreadyExists, NotFound
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Spanner 🌍")

def get_spanner_connection():
    """Get Spanner client, instance, and database connection"""
    project_id = os.getenv("GCP_PROJECT_ID")
    instance_id = os.getenv("SPANNER_INSTANCE_ID", "my-instance")
    database_id = os.getenv("SPANNER_DATABASE_ID", "my-database")
    
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is required")
    
    client = spanner.Client(project=project_id)
    instance = client.instance(instance_id)
    database = instance.database(database_id)
    
    return client, instance, database

# ==================== INSTANCE OPERATIONS ====================

@mcp.tool()
async def list_instances() -> dict:
    """📋 List all Spanner instances in project"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        client = spanner.Client(project=project_id)
        
        instances = list(client.list_instances())
        instance_info = [
            {
                "id": inst.instance_id,
                "display_name": inst.display_name,
                "state": inst.state,
                "node_count": inst.node_count,
                "config": inst.instance_config
            }
            for inst in instances
        ]
        
        logger.info(f"✅ Found {len(instance_info)} instances")
        return {"success": True, "instances": instance_info, "count": len(instance_info)}
    except Exception as e:
        logger.error(f"❌ Error listing instances: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_instance(instance_id: str) -> dict:
    """🔎 Get instance details"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        client = spanner.Client(project=project_id)
        instance = client.instance(instance_id)
        instance.reload()
        
        info = {
            "id": instance.instance_id,
            "display_name": instance.display_name,
            "state": instance.state,
            "node_count": instance.node_count,
            "config": instance.instance_config,
            "labels": dict(instance.labels)
        }
        
        logger.info(f"✅ Retrieved instance {instance_id}")
        return {"success": True, "instance": info}
    except Exception as e:
        logger.error(f"❌ Error describing instance: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DATABASE OPERATIONS ====================

@mcp.tool()
async def list_databases(instance_id: str) -> dict:
    """📚 List all databases in instance"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        client = spanner.Client(project=project_id)
        instance = client.instance(instance_id)
        
        databases = list(instance.list_databases())
        db_info = [
            {
                "id": db.database_id,
                "state": db.state,
                "version_retention_period": db.version_retention_period
            }
            for db in databases
        ]
        
        logger.info(f"✅ Found {len(db_info)} databases")
        return {"success": True, "databases": db_info, "count": len(db_info)}
    except Exception as e:
        logger.error(f"❌ Error listing databases: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_database(database_id: str, instance_id: Optional[str] = None) -> dict:
    """✨ Create new database"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        instance_id = instance_id or os.getenv("SPANNER_INSTANCE_ID", "my-instance")
        
        client = spanner.Client(project=project_id)
        instance = client.instance(instance_id)
        database = instance.database(database_id)
        
        operation = database.create()
        operation.result(timeout=120)
        
        logger.info(f"✅ Database {database_id} created")
        return {"success": True, "message": f"Database {database_id} created"}
    except AlreadyExists:
        logger.error(f"❌ Database already exists: {database_id}")
        return {"success": False, "error": f"Database {database_id} already exists"}
    except Exception as e:
        logger.error(f"❌ Error creating database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_database(database_id: str, instance_id: Optional[str] = None) -> dict:
    """❌ Drop database (irreversible)"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        instance_id = instance_id or os.getenv("SPANNER_INSTANCE_ID", "my-instance")
        
        client = spanner.Client(project=project_id)
        instance = client.instance(instance_id)
        database = instance.database(database_id)
        
        database.drop()
        
        logger.info(f"✅ Database {database_id} dropped")
        return {"success": True, "message": f"Database {database_id} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping database: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_database_info() -> dict:
    """🏢 Get current database information"""
    try:
        _, _, database = get_spanner_connection()
        database.reload()
        
        info = {
            "database_id": database.database_id,
            "state": database.state,
            "version_retention_period": database.version_retention_period
        }
        
        logger.info(f"✅ Retrieved database info")
        return {"success": True, "info": info}
    except Exception as e:
        logger.error(f"❌ Error getting database info: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== TABLE DDL OPERATIONS ====================

@mcp.tool()
async def list_tables() -> dict:
    """📑 List all tables in database"""
    try:
        _, _, database = get_spanner_connection()
        
        with database.snapshot() as snapshot:
            result = snapshot.execute_sql(
                "SELECT t.table_name FROM information_schema.tables AS t WHERE t.table_schema = 'public'"
            )
            tables = [row[0] for row in result]
        
        logger.info(f"✅ Found {len(tables)} tables")
        return {"success": True, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """🔍 Get table schema"""
    try:
        _, _, database = get_spanner_connection()
        
        with database.snapshot() as snapshot:
            result = snapshot.execute_sql(
                f"""SELECT c.column_name, c.spanner_type, is_nullable 
                   FROM information_schema.columns c 
                   WHERE c.table_name = @table_name""",
                {"table_name": table_name}
            )
            columns = [
                {"name": row[0], "type": row[1], "nullable": row[2]}
                for row in result
            ]
        
        logger.info(f"✅ Retrieved schema for {table_name}")
        return {"success": True, "columns": columns}
    except Exception as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_table(table_name: str, ddl: str) -> dict:
    """✍️ Create new table with DDL"""
    try:
        _, _, database = get_spanner_connection()
        
        operation = database.update_ddl([ddl])
        operation.result(timeout=120)
        
        logger.info(f"✅ Table {table_name} created")
        return {"success": True, "message": f"Table {table_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_table(table_name: str) -> dict:
    """🗑️ Drop table"""
    try:
        _, _, database = get_spanner_connection()
        
        ddl = f"DROP TABLE {table_name}"
        operation = database.update_ddl([ddl])
        operation.result(timeout=120)
        
        logger.info(f"✅ Table {table_name} dropped")
        return {"success": True, "message": f"Table {table_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def add_column(table_name: str, column_name: str, data_type: str, nullable: bool = True) -> dict:
    """➕ Add column to table"""
    try:
        _, _, database = get_spanner_connection()
        
        nullable_str = "" if nullable else "NOT NULL"
        ddl = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type} {nullable_str}"
        operation = database.update_ddl([ddl])
        operation.result(timeout=120)
        
        logger.info(f"✅ Column {column_name} added to {table_name}")
        return {"success": True, "message": f"Column {column_name} added"}
    except Exception as e:
        logger.error(f"❌ Error adding column: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== INDEX OPERATIONS ====================

@mcp.tool()
async def create_index(index_name: str, table_name: str, columns: List[str], unique: bool = False) -> dict:
    """🔑 Create index"""
    try:
        _, _, database = get_spanner_connection()
        
        column_str = ", ".join(columns)
        unique_str = "UNIQUE" if unique else ""
        ddl = f"CREATE {unique_str} INDEX {index_name} ON {table_name}({column_str})"
        operation = database.update_ddl([ddl])
        operation.result(timeout=120)
        
        logger.info(f"✅ Index {index_name} created")
        return {"success": True, "message": f"Index {index_name} created"}
    except Exception as e:
        logger.error(f"❌ Error creating index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def drop_index(index_name: str) -> dict:
    """🗑️ Drop index"""
    try:
        _, _, database = get_spanner_connection()
        
        ddl = f"DROP INDEX {index_name}"
        operation = database.update_ddl([ddl])
        operation.result(timeout=120)
        
        logger.info(f"✅ Index {index_name} dropped")
        return {"success": True, "message": f"Index {index_name} dropped"}
    except Exception as e:
        logger.error(f"❌ Error dropping index: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_indexes(table_name: str) -> dict:
    """📑 List indexes on table"""
    try:
        _, _, database = get_spanner_connection()
        
        with database.snapshot() as snapshot:
            result = snapshot.execute_sql(
                f"""SELECT i.index_name, i.is_unique 
                   FROM information_schema.indexes i 
                   WHERE i.table_name = @table_name""",
                {"table_name": table_name}
            )
            indexes = [{"name": row[0], "unique": row[1]} for row in result]
        
        logger.info(f"✅ Found {len(indexes)} indexes")
        return {"success": True, "indexes": indexes, "count": len(indexes)}
    except Exception as e:
        logger.error(f"❌ Error listing indexes: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== DML OPERATIONS ====================

@mcp.tool()
async def insert_row(table_name: str, row: dict) -> dict:
    """✍️ Insert single row"""
    try:
        _, _, database = get_spanner_connection()
        
        columns = list(row.keys())
        values = [row[col] for col in columns]
        
        with database.batch() as batch:
            batch.insert(table_name, columns, [values])
        
        logger.info(f"✅ Row inserted into {table_name}")
        return {"success": True, "message": "Row inserted"}
    except Exception as e:
        logger.error(f"❌ Error inserting row: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_insert(table_name: str, rows: List[dict]) -> dict:
    """📦 Batch insert multiple rows"""
    try:
        _, _, database = get_spanner_connection()
        
        if not rows:
            return {"success": True, "inserted_count": 0}
        
        columns = list(rows[0].keys())
        values = [[row[col] for col in columns] for row in rows]
        
        with database.batch() as batch:
            batch.insert(table_name, columns, values)
        
        logger.info(f"✅ Inserted {len(rows)} rows")
        return {"success": True, "inserted_count": len(rows)}
    except Exception as e:
        logger.error(f"❌ Error batch inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_row(table_name: str, row: dict) -> dict:
    """🔄 Update row"""
    try:
        _, _, database = get_spanner_connection()
        
        columns = list(row.keys())
        values = [row[col] for col in columns]
        
        with database.batch() as batch:
            batch.update(table_name, columns, [values])
        
        logger.info(f"✅ Row updated in {table_name}")
        return {"success": True, "message": "Row updated"}
    except Exception as e:
        logger.error(f"❌ Error updating row: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_update(table_name: str, rows: List[dict]) -> dict:
    """📦 Batch update multiple rows"""
    try:
        _, _, database = get_spanner_connection()
        
        if not rows:
            return {"success": True, "updated_count": 0}
        
        columns = list(rows[0].keys())
        values = [[row[col] for col in columns] for row in rows]
        
        with database.batch() as batch:
            batch.update(table_name, columns, values)
        
        logger.info(f"✅ Updated {len(rows)} rows")
        return {"success": True, "updated_count": len(rows)}
    except Exception as e:
        logger.error(f"❌ Error batch updating: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_row(table_name: str, key_values: dict) -> dict:
    """🗑️ Delete single row by key"""
    try:
        _, _, database = get_spanner_connection()
        
        key_set = spanner.KeySet([spanner.Key([key_values[k] for k in sorted(key_values.keys())])])
        
        with database.batch() as batch:
            batch.delete(table_name, key_set)
        
        logger.info(f"✅ Row deleted from {table_name}")
        return {"success": True, "message": "Row deleted"}
    except Exception as e:
        logger.error(f"❌ Error deleting row: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_delete(table_name: str, key_values_list: List[dict]) -> dict:
    """🧹 Batch delete multiple rows"""
    try:
        _, _, database = get_spanner_connection()
        
        if not key_values_list:
            return {"success": True, "deleted_count": 0}
        
        keys = [spanner.Key([kv[k] for k in sorted(kv.keys())]) for kv in key_values_list]
        key_set = spanner.KeySet(keys)
        
        with database.batch() as batch:
            batch.delete(table_name, key_set)
        
        logger.info(f"✅ Deleted {len(key_values_list)} rows")
        return {"success": True, "deleted_count": len(key_values_list)}
    except Exception as e:
        logger.error(f"❌ Error batch deleting: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== QUERY OPERATIONS ====================

@mcp.tool()
async def execute_query(query: str, parameters: Optional[dict] = None) -> dict:
    """⚡ Execute SQL query"""
    try:
        _, _, database = get_spanner_connection()
        
        with database.snapshot() as snapshot:
            params = parameters or {}
            result = snapshot.execute_sql(query, params)
            rows = [list(row) for row in result]
        
        logger.info(f"✅ Query returned {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"❌ Error executing query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_with_limit(query: str, limit: int = 100, parameters: Optional[dict] = None) -> dict:
    """📊 Execute query with result limit"""
    try:
        _, _, database = get_spanner_connection()
        
        safe_query = f"{query} LIMIT {limit}"
        
        with database.snapshot() as snapshot:
            params = parameters or {}
            result = snapshot.execute_sql(safe_query, params)
            rows = [list(row) for row in result]
        
        logger.info(f"✅ Query returned {len(rows)} rows")
        return {"success": True, "rows": rows, "count": len(rows)}
    except Exception as e:
        logger.error(f"❌ Error executing query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_row_count(table_name: str) -> dict:
    """📈 Get row count for table"""
    try:
        _, _, database = get_spanner_connection()
        
        with database.snapshot() as snapshot:
            result = snapshot.execute_sql(f"SELECT COUNT(*) FROM {table_name}")
            count = list(result)[0][0]
        
        logger.info(f"✅ Row count: {count}")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ Error counting rows: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def distinct_values(table_name: str, column_name: str) -> dict:
    """🔎 Get distinct values for column"""
    try:
        _, _, database = get_spanner_connection()
        
        with database.snapshot() as snapshot:
            result = snapshot.execute_sql(f"SELECT DISTINCT {column_name} FROM {table_name}")
            values = [row[0] for row in result]
        
        logger.info(f"✅ Found {len(values)} distinct values")
        return {"success": True, "values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ Error getting distinct values: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== TRANSACTION OPERATIONS ====================

@mcp.tool()
async def read_write_transaction(queries: List[dict]) -> dict:
    """🔄 Execute multiple operations in transaction"""
    try:
        _, _, database = get_spanner_connection()
        
        def transaction_callback(transaction):
            for query_dict in queries:
                query = query_dict.get("query")
                query_type = query_dict.get("type", "execute")
                
                if query_type == "execute":
                    transaction.execute_update(query)
                elif query_type == "select":
                    result = transaction.execute_sql(query)
                    list(result)
        
        database.run_in_transaction(transaction_callback)
        
        logger.info(f"✅ Transaction executed with {len(queries)} operations")
        return {"success": True, "message": f"Transaction completed"}
    except Exception as e:
        logger.error(f"❌ Error in transaction: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ADMIN & MONITORING ====================

@mcp.tool()
async def create_backup(backup_id: str, instance_id: Optional[str] = None, retention_days: int = 30) -> dict:
    """💾 Create database backup"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        instance_id = instance_id or os.getenv("SPANNER_INSTANCE_ID", "my-instance")
        database_id = os.getenv("SPANNER_DATABASE_ID", "my-database")
        
        client = spanner.Client(project=project_id)
        instance = client.instance(instance_id)
        database = instance.database(database_id)
        
        backup = instance.backup(backup_id)
        operation = backup.create(database, retention_period_days=retention_days)
        operation.result(timeout=300)
        
        logger.info(f"✅ Backup {backup_id} created")
        return {"success": True, "message": f"Backup {backup_id} created"}
    except Exception as e:
        logger.error(f"❌ Error creating backup: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_backups(instance_id: Optional[str] = None) -> dict:
    """📋 List all backups"""
    try:
        project_id = os.getenv("GCP_PROJECT_ID")
        instance_id = instance_id or os.getenv("SPANNER_INSTANCE_ID", "my-instance")
        
        client = spanner.Client(project=project_id)
        instance = client.instance(instance_id)
        
        backups = list(instance.list_backups())
        backup_info = [
            {
                "id": b.backup_id,
                "state": b.state,
                "create_time": str(b.create_time),
                "expire_time": str(b.expire_time)
            }
            for b in backups
        ]
        
        logger.info(f"✅ Found {len(backup_info)} backups")
        return {"success": True, "backups": backup_info, "count": len(backup_info)}
    except Exception as e:
        logger.error(f"❌ Error listing backups: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_database_stats() -> dict:
    """📊 Get database statistics"""
    try:
        _, _, database = get_spanner_connection()
        database.reload()
        
        stats = {
            "database_id": database.database_id,
            "state": database.state,
            "version_retention_period": database.version_retention_period
        }
        
        logger.info(f"✅ Retrieved database statistics")
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the Spanner MCP server"""
    try:
        logger.info("🚀 Starting Spanner MCP Server on port 7092")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7092)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
DBA Operations Prompt:
You are a Google Cloud Spanner Database Administrator. Help manage instances, databases, 
indexes, and backups. Focus on global consistency, scaling strategies, and disaster recovery 
across multi-region deployments.

Data Engineer Prompt:
You are a Data Engineer using Spanner for distributed data operations. Help design schemas 
for global scaling, bulk loading via batch operations, and optimizing transactions for strong consistency.

Analytics Engineer Prompt:
You are an Analytics Engineer querying Spanner for insights. Help write efficient SQL queries,
optimize index usage for query performance, and analyze data across globally distributed tables.
"""
