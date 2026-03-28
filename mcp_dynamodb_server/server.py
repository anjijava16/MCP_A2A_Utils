"""
AWS DynamoDB MCP Server using FastMCP
Provides tools for AWS DynamoDB NoSQL database operations
"""

import asyncio
import boto3
from botocore.exceptions import ClientError
import logging
from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("dynamodb-mcp-server")

class DynamoDBConnectionPool:
    def __init__(self, region: str, access_key: str = None, secret_key: str = None):
        self.region = region
        kwargs = {"region_name": region}
        
        if access_key and secret_key:
            kwargs["aws_access_key_id"] = access_key
            kwargs["aws_secret_access_key"] = secret_key
        
        self.dynamodb = boto3.resource("dynamodb", **kwargs)
        self.client = boto3.client("dynamodb", **kwargs)
        logger.info(f"Connected to DynamoDB in region {region}")

db_pool = None

@mcp.tool()
async def list_tables() -> dict:
    """List all tables in DynamoDB"""
    try:
        response = db_pool.client.list_tables()
        return {"success": True, "tables": response["TableNames"]}
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """Get table details"""
    try:
        response = db_pool.client.describe_table(TableName=table_name)
        table = response["Table"]
        return {
            "success": True,
            "table": {
                "name": table["TableName"],
                "status": table["TableStatus"],
                "item_count": table.get("ItemCount", 0),
                "size_bytes": table.get("TableSizeBytes", 0),
                "keys": table["KeySchema"],
                "attributes": table["AttributeDefinitions"]
            }
        }
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def put_item(table_name: str, item: dict) -> dict:
    """Put item into table"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        table.put_item(Item=item)
        return {"success": True, "message": "Item put"}
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_item(table_name: str, key: dict) -> dict:
    """Get item from table"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        return {
            "success": True,
            "item": response.get("Item")
        }
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_items(table_name: str, key_condition: dict, limit: int = 10) -> dict:
    """Query items from table"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        response = table.query(
            KeyConditionExpression=key_condition.get("condition"),
            ExpressionAttributeNames=key_condition.get("names", {}),
            ExpressionAttributeValues=key_condition.get("values", {}),
            Limit=limit
        )
        return {
            "success": True,
            "items": response.get("Items", []),
            "count": response.get("Count", 0)
        }
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def scan_table(table_name: str, limit: int = 10) -> dict:
    """Scan table items"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        response = table.scan(Limit=limit)
        return {
            "success": True,
            "items": response.get("Items", []),
            "count": response.get("Count", 0)
        }
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_item(table_name: str, key: dict, updates: dict) -> dict:
    """Update item in table"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        update_expr = "SET " + ", ".join([f"#{k}=:{k}" for k in updates.keys()])
        attr_names = {f"#{k}": k for k in updates.keys()}
        attr_values = {f":{k}": v for k, v in updates.items()}
        
        table.update_item(
            Key=key,
            UpdateExpression=update_expr,
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=attr_values
        )
        return {"success": True, "message": "Item updated"}
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_item(table_name: str, key: dict) -> dict:
    """Delete item from table"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        table.delete_item(Key=key)
        return {"success": True, "message": "Item deleted"}
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_write(table_name: str, items: list) -> dict:
    """Batch write items"""
    try:
        table = db_pool.dynamodb.Table(table_name)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
        
        return {"success": True, "written_count": len(items)}
    except ClientError as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_table_stats(table_name: str) -> dict:
    """Get table statistics"""
    try:
        response = db_pool.client.describe_table(TableName=table_name)
        table = response["Table"]
        
        return {
            "success": True,
            "stats": {
                "item_count": table.get("ItemCount", 0),
                "size_bytes": table.get("TableSizeBytes", 0),
                "read_capacity": table.get("BillingModeSummary", {}).get("LastUpdateToPayPerRequestDateTime"),
                "write_capacity": table.get("BillingModeSummary", {}).get("LastUpdateToPayPerRequestDateTime"),
                "status": table["TableStatus"]
            }
        }
    except ClientError as e:
        return {"success": False, "error": str(e)}

async def main():
    global db_pool
    
    import os
    
    region = os.getenv("AWS_REGION", "us-east-1")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    db_pool = DynamoDBConnectionPool(region, access_key, secret_key)
    
    try:
        logger.info("Starting DynamoDB MCP Server")
        await mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())
