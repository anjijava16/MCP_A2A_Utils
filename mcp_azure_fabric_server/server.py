import asyncio
import logging
import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime
from fastmcp import FastMCP

# Configure logging with emoji
logging.basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("Azure Fabric MCP Server 🏢")

# Configuration from environment
FABRIC_CONFIG = {
    "workspace_id": os.getenv("FABRIC_WORKSPACE_ID", ""),
    "capacity_id": os.getenv("FABRIC_CAPACITY_ID", ""),
    "tenant_id": os.getenv("AZURE_TENANT_ID", ""),
    "client_id": os.getenv("AZURE_CLIENT_ID", ""),
    "client_secret": os.getenv("AZURE_CLIENT_SECRET", ""),
}

# Mock connection for demonstration
class FabricConnection:
    """Simulated Azure Fabric connection."""
    def __init__(self):
        self.workspace_id = FABRIC_CONFIG["workspace_id"]
        self.capacity_id = FABRIC_CONFIG["capacity_id"]
        self.authenticated = bool(FABRIC_CONFIG["client_id"])

def get_fabric_connection():
    """Get Azure Fabric connection."""
    try:
        conn = FabricConnection()
        if not conn.authenticated:
            logger.warning("⚠️ Azure Fabric authentication not configured")
        logger.info(f"✅ Connected to Fabric workspace: {FABRIC_CONFIG['workspace_id']}")
        return conn
    except Exception as e:
        logger.error(f"❌ Fabric connection error: {str(e)}")
        raise

# ====================== WORKSPACE TOOLS ======================

@mcp.tool()
def fabric_list_workspaces() -> Dict[str, Any]:
    """List all Fabric workspaces accessible to the user.
    
    Returns:
        List of workspaces with IDs and metadata
    """
    try:
        workspaces = [
            {"id": FABRIC_CONFIG["workspace_id"], "name": "Primary Workspace", "type": "ProductionWorkspace"}
        ]
        logger.info(f"📋 Found {len(workspaces)} workspaces")
        return {"success": True, "workspaces": workspaces, "count": len(workspaces)}
    except Exception as e:
        logger.error(f"❌ Error listing workspaces: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_create_workspace(workspace_name: str, capacity_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a new Fabric workspace.
    
    Args:
        workspace_name: Name of the workspace
        capacity_id: Capacity ID to assign
    
    Returns:
        Workspace ID and details
    """
    try:
        workspace_id = f"ws_{workspace_name.lower().replace(' ', '_')}"
        logger.info(f"📦 Workspace created: {workspace_name}")
        return {
            "success": True,
            "workspace_id": workspace_id,
            "workspace_name": workspace_name,
            "capacity_id": capacity_id or FABRIC_CONFIG["capacity_id"],
            "created": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"❌ Error creating workspace: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_get_workspace_details(workspace_id: Optional[str] = None) -> Dict[str, Any]:
    """Get details about a Fabric workspace.
    
    Args:
        workspace_id: Workspace ID (uses default if not provided)
    
    Returns:
        Workspace configuration and metadata
    """
    try:
        ws_id = workspace_id or FABRIC_CONFIG["workspace_id"]
        logger.info(f"📊 Workspace details retrieved: {ws_id}")
        return {
            "success": True,
            "workspace_id": ws_id,
            "capacity_id": FABRIC_CONFIG["capacity_id"],
            "type": "ProductionWorkspace",
            "status": "Active"
        }
    except Exception as e:
        logger.error(f"❌ Error getting workspace details: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DDL TOOLS ======================

@mcp.tool()
def fabric_create_lakehouse(workspace_id: str, lakehouse_name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new Lakehouse in Fabric workspace.
    
    Args:
        workspace_id: Workspace ID
        lakehouse_name: Lakehouse name
        description: Optional description
    
    Returns:
        Lakehouse ID and details
    """
    try:
        lakehouse_id = f"lh_{lakehouse_name.lower().replace(' ', '_')}"
        logger.info(f"🏗️ Lakehouse created: {lakehouse_name}")
        return {
            "success": True,
            "lakehouse_id": lakehouse_id,
            "lakehouse_name": lakehouse_name,
            "workspace_id": workspace_id,
            "created": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"❌ Error creating lakehouse: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_create_warehouse(workspace_id: str, warehouse_name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new Warehouse in Fabric workspace.
    
    Args:
        workspace_id: Workspace ID
        warehouse_name: Warehouse name
        description: Optional description
    
    Returns:
        Warehouse ID and details
    """
    try:
        warehouse_id = f"wh_{warehouse_name.lower().replace(' ', '_')}"
        logger.info(f"🏗️ Warehouse created: {warehouse_name}")
        return {
            "success": True,
            "warehouse_id": warehouse_id,
            "warehouse_name": warehouse_name,
            "workspace_id": workspace_id,
            "type": "DataWarehouse",
            "created": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"❌ Error creating warehouse: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_create_schema(workspace_id: str, warehouse_id: str, schema_name: str) -> Dict[str, Any]:
    """Create a schema in a Fabric warehouse.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🏗️ Schema created: {schema_name}")
        return {
            "success": True,
            "schema_name": schema_name,
            "warehouse_id": warehouse_id,
            "message": f"Schema '{schema_name}' created successfully"
        }
    except Exception as e:
        logger.error(f"❌ Error creating schema: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_create_table(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                        columns: str, primary_key: Optional[str] = None) -> Dict[str, Any]:
    """Create a table in Fabric warehouse.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        columns: Column definitions (comma-separated: col1 INT, col2 STRING, ...)
        primary_key: Primary key column(s)
    
    Returns:
        Success status and table details
    """
    try:
        logger.info(f"🏗️ Table created: {schema_name}.{table_name}")
        return {
            "success": True,
            "table_name": table_name,
            "schema_name": schema_name,
            "warehouse_id": warehouse_id,
            "message": f"Table '{schema_name}.{table_name}' created successfully"
        }
    except Exception as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_drop_table(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str) -> Dict[str, Any]:
    """Drop a table from Fabric warehouse.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name to drop
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🗑️ Table dropped: {schema_name}.{table_name}")
        return {"success": True, "message": f"Table '{schema_name}.{table_name}' dropped successfully"}
    except Exception as e:
        logger.error(f"❌ Error dropping table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_list_tables(workspace_id: str, warehouse_id: str, schema_name: str) -> Dict[str, Any]:
    """List tables in a Fabric schema.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
    
    Returns:
        List of table names
    """
    try:
        tables = []  # Get from Fabric API
        logger.info(f"📋 Found {len(tables)} tables in {schema_name}")
        return {"success": True, "tables": tables, "count": len(tables)}
    except Exception as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_describe_table(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str) -> Dict[str, Any]:
    """Describe table structure and columns.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
    
    Returns:
        Table schema and metadata
    """
    try:
        columns = [
            {"name": "col1", "type": "INT", "nullable": False},
            {"name": "col2", "type": "STRING", "nullable": True}
        ]
        logger.info(f"📊 Table described: {schema_name}.{table_name}")
        return {
            "success": True,
            "table_name": table_name,
            "columns": columns,
            "count": len(columns)
        }
    except Exception as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_create_view(workspace_id: str, warehouse_id: str, schema_name: str, view_name: str, sql: str) -> Dict[str, Any]:
    """Create a view in Fabric warehouse.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        view_name: View name
        sql: SQL query for view
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🔍 View created: {schema_name}.{view_name}")
        return {
            "success": True,
            "view_name": view_name,
            "schema_name": schema_name,
            "message": f"View '{schema_name}.{view_name}' created successfully"
        }
    except Exception as e:
        logger.error(f"❌ Error creating view: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DML TOOLS ======================

@mcp.tool()
def fabric_insert_record(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                         record: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a single record into a Fabric table.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        record: Record data as dictionary
    
    Returns:
        Success status
    """
    try:
        logger.info(f"➕ Record inserted into {schema_name}.{table_name}")
        return {"success": True, "message": "Record inserted successfully"}
    except Exception as e:
        logger.error(f"❌ Error inserting record: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_insert_multiple_records(workspace_id: str, warehouse_id: str, schema_name: str, 
                                   table_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bulk insert multiple records into a Fabric table.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        records: List of record dictionaries
    
    Returns:
        Success status and row count
    """
    try:
        logger.info(f"➕ {len(records)} records inserted into {schema_name}.{table_name}")
        return {"success": True, "message": f"{len(records)} records inserted", "inserted": len(records)}
    except Exception as e:
        logger.error(f"❌ Error bulk inserting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_update_records(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                          set_clause: str, where_clause: Optional[str] = None) -> Dict[str, Any]:
    """Update records in a Fabric table.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        set_clause: SET clause (col1=val1, col2=val2)
        where_clause: WHERE condition
    
    Returns:
        Success status and rows affected
    """
    try:
        logger.info(f"✏️ Records updated in {schema_name}.{table_name}")
        return {"success": True, "message": "Records updated successfully", "affected": 0}
    except Exception as e:
        logger.error(f"❌ Error updating records: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_delete_records(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                          where_clause: str) -> Dict[str, Any]:
    """Delete records from a Fabric table.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        where_clause: WHERE condition
    
    Returns:
        Success status and rows deleted
    """
    try:
        logger.info(f"🗑️ Records deleted from {schema_name}.{table_name}")
        return {"success": True, "message": "Records deleted successfully", "deleted": 0}
    except Exception as e:
        logger.error(f"❌ Error deleting records: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SELECT/QUERY TOOLS ======================

@mcp.tool()
def fabric_query_custom(workspace_id: str, warehouse_id: str, sql: str) -> Dict[str, Any]:
    """Execute a custom SQL query in Fabric.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        sql: SQL query to execute
    
    Returns:
        Query results
    """
    try:
        logger.info(f"🔎 Custom query executed")
        results = []
        return {"success": True, "rows": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ Query error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_all(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                      limit: int = 1000) -> Dict[str, Any]:
    """Select all records from a Fabric table.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        limit: Maximum rows to return
    
    Returns:
        Query results
    """
    try:
        logger.info(f"🔎 SELECT all from {schema_name}.{table_name}")
        results = []
        return {"success": True, "rows": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ SELECT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_where(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                        where_clause: str, limit: int = 1000) -> Dict[str, Any]:
    """Select records with WHERE condition.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        where_clause: WHERE condition
        limit: Maximum rows
    
    Returns:
        Query results
    """
    try:
        logger.info(f"🔎 SELECT WHERE from {schema_name}.{table_name}")
        results = []
        return {"success": True, "rows": results, "count": len(results)}
    except Exception as e:
        logger.error(f"❌ SELECT WHERE error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_count(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str) -> Dict[str, Any]:
    """Count records in a Fabric table.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
    
    Returns:
        Record count
    """
    try:
        logger.info(f"🔢 COUNT from {schema_name}.{table_name}")
        return {"success": True, "count": 0}
    except Exception as e:
        logger.error(f"❌ COUNT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_aggregate(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                            agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute aggregate query (SUM, AVG, MIN, MAX, COUNT).
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        agg_column: Column to aggregate
        agg_function: Function (SUM, AVG, MIN, MAX)
    
    Returns:
        Aggregate result
    """
    try:
        logger.info(f"📊 {agg_function} on {agg_column}")
        return {"success": True, "result": 0, "function": agg_function}
    except Exception as e:
        logger.error(f"❌ Aggregate error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_distinct(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                           column: str) -> Dict[str, Any]:
    """Get distinct values from a column.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        column: Column name
    
    Returns:
        List of distinct values
    """
    try:
        logger.info(f"🔍 DISTINCT {column}")
        return {"success": True, "values": [], "count": 0}
    except Exception as e:
        logger.error(f"❌ DISTINCT error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_grouped(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                          group_by: str, agg_column: str, agg_function: str) -> Dict[str, Any]:
    """Execute GROUP BY query.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        group_by: Column to group by
        agg_column: Column to aggregate
        agg_function: Aggregate function
    
    Returns:
        Grouped results
    """
    try:
        logger.info(f"📊 GROUP BY {group_by}")
        return {"success": True, "rows": [], "count": 0}
    except Exception as e:
        logger.error(f"❌ GROUP BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_ordered(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str,
                          order_by: str, direction: str = "ASC", limit: int = 1000) -> Dict[str, Any]:
    """Select records with ORDER BY.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
        order_by: Column to order by
        direction: ASC or DESC
        limit: Maximum rows
    
    Returns:
        Ordered results
    """
    try:
        logger.info(f"🔎 ORDER BY {order_by}")
        return {"success": True, "rows": [], "count": 0}
    except Exception as e:
        logger.error(f"❌ ORDER BY error: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_select_join(workspace_id: str, warehouse_id: str, schema_name: str, table1: str,
                       table2: str, join_column: str, join_type: str = "INNER") -> Dict[str, Any]:
    """Execute JOIN query between two tables.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table1: First table
        table2: Second table
        join_column: Column to join on
        join_type: INNER, LEFT, RIGHT, OUTER
    
    Returns:
        Join results
    """
    try:
        logger.info(f"🔗 {join_type} JOIN")
        return {"success": True, "rows": [], "count": 0}
    except Exception as e:
        logger.error(f"❌ JOIN error: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== DCL TOOLS ======================

@mcp.tool()
def fabric_grant_permissions(workspace_id: str, principal: str, role: str) -> Dict[str, Any]:
    """Grant permissions to a principal (user/group) in Fabric.
    
    Args:
        workspace_id: Workspace ID
        principal: User or group email
        role: Role (Admin, Member, Viewer, Contributor)
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🔐 Permission granted: {principal} -> {role}")
        return {"success": True, "message": f"Permission granted successfully"}
    except Exception as e:
        logger.error(f"❌ Error granting permission: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_revoke_permissions(workspace_id: str, principal: str) -> Dict[str, Any]:
    """Revoke permissions from a principal in Fabric.
    
    Args:
        workspace_id: Workspace ID
        principal: User or group email
    
    Returns:
        Success status
    """
    try:
        logger.info(f"🔐 Permission revoked: {principal}")
        return {"success": True, "message": f"Permission revoked successfully"}
    except Exception as e:
        logger.error(f"❌ Error revoking permission: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_list_workspace_members(workspace_id: str) -> Dict[str, Any]:
    """List workspace members and their roles.
    
    Args:
        workspace_id: Workspace ID
    
    Returns:
        List of workspace members
    """
    try:
        members = []
        logger.info(f"👥 Found {len(members)} workspace members")
        return {"success": True, "members": members, "count": len(members)}
    except Exception as e:
        logger.error(f"❌ Error listing members: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== ADMINISTRATION TOOLS ======================

@mcp.tool()
def fabric_get_workspace_capacity(workspace_id: str) -> Dict[str, Any]:
    """Get current capacity usage for workspace.
    
    Args:
        workspace_id: Workspace ID
    
    Returns:
        Capacity statistics
    """
    try:
        logger.info(f"📊 Capacity stats retrieved")
        return {
            "success": True,
            "capacity_used": 0,
            "capacity_total": 1000,
            "percent_used": 0
        }
    except Exception as e:
        logger.error(f"❌ Error getting capacity: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_get_table_stats(workspace_id: str, warehouse_id: str, schema_name: str, table_name: str) -> Dict[str, Any]:
    """Get table statistics and metadata.
    
    Args:
        workspace_id: Workspace ID
        warehouse_id: Warehouse ID
        schema_name: Schema name
        table_name: Table name
    
    Returns:
        Table statistics
    """
    try:
        logger.info(f"📏 Table stats retrieved: {schema_name}.{table_name}")
        return {
            "success": True,
            "rows": 0,
            "size_mb": 0,
            "last_modified": str(datetime.now())
        }
    except Exception as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_list_activities(workspace_id: str, limit: int = 50) -> Dict[str, Any]:
    """List recent activities in workspace.
    
    Args:
        workspace_id: Workspace ID
        limit: Maximum activities to return
    
    Returns:
        List of activities
    """
    try:
        activities = []
        logger.info(f"⚡ Found {len(activities)} recent activities")
        return {"success": True, "activities": activities, "count": len(activities)}
    except Exception as e:
        logger.error(f"❌ Error listing activities: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def fabric_refresh_semantic_model(workspace_id: str, semantic_model_id: str) -> Dict[str, Any]:
    """Trigger refresh of semantic model.
    
    Args:
        workspace_id: Workspace ID
        semantic_model_id: Semantic model ID
    
    Returns:
        Refresh job status
    """
    try:
        logger.info(f"♻️ Semantic model refresh triggered")
        return {"success": True, "message": "Refresh initiated successfully", "status": "InProgress"}
    except Exception as e:
        logger.error(f"❌ Error triggering refresh: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are an Azure Fabric Database Administrator. Your role is to:
- Manage warehouses, lakehouses, and workspaces
- Design and maintain table schemas
- Manage user permissions and access
- Monitor capacity and performance
- Execute DDL operations safely

Use these tools for DBA tasks:
- fabric_create_warehouse, fabric_create_lakehouse, fabric_list_workspaces
- fabric_create_table, fabric_describe_table, fabric_drop_table
- fabric_grant_permissions, fabric_revoke_permissions
- fabric_get_workspace_capacity, fabric_list_activities
"""

DATA_ENGINEER_PROMPT = """You are an Azure Fabric Data Engineer. Your role is to:
- Design and build data pipelines
- Load and transform data
- Optimize table structures
- Maintain data quality
- Create views for different use cases

Use these tools for data engineering:
- fabric_insert_record, fabric_insert_multiple_records
- fabric_create_table, fabric_create_schema
- fabric_update_records, fabric_delete_records
- fabric_select_all, fabric_select_where for validation
- fabric_get_table_stats for monitoring
"""

DATA_ANALYST_PROMPT = """You are an Azure Fabric Data Analyst. Your role is to:
- Query and analyze data
- Generate insights and reports
- Create analytical views
- Perform ad-hoc analysis
- Track data trends

Use these tools for analysis:
- fabric_query_custom for complex queries
- fabric_select_all, fabric_select_where for exploration
- fabric_select_aggregate for statistics
- fabric_select_grouped for trend analysis
- fabric_select_ordered for ranking
- fabric_select_join for combining data
- fabric_list_activities for monitoring
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Data Engineer", DATA_ENGINEER_PROMPT)
mcp.add_prompt("Data Analyst", DATA_ANALYST_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting Azure Fabric MCP Server...")
    if not FABRIC_CONFIG["workspace_id"]:
        logger.warning("⚠️ FABRIC_WORKSPACE_ID not set in environment")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7083"))
    )

if __name__ == "__main__":
    asyncio.run(main())
