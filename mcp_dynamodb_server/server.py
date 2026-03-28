"""
AWS DynamoDB MCP Server 📊
Comprehensive MCP server for AWS DynamoDB operations with full DDL, DML, Query, and Admin tooling
"""

import asyncio
import boto3
import json
import logging
import os
from typing import Any, Dict, List, Optional
from decimal import Decimal
from botocore.exceptions import ClientError
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("DynamoDB 📊")

def get_dynamodb_connection():
    """Get DynamoDB resource and client connection"""
    region = os.getenv("AWS_REGION", "us-east-1")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    kwargs = {"region_name": region}
    if access_key and secret_key:
        kwargs["aws_access_key_id"] = access_key
        kwargs["aws_secret_access_key"] = secret_key
    
    dynamodb = boto3.resource("dynamodb", **kwargs)
    client = boto3.client("dynamodb", **kwargs)
    return dynamodb, client

def decimal_to_float(obj):
    """Convert Decimal objects to float for JSON serialization"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# ==================== TABLE DDL OPERATIONS ====================

@mcp.tool()
async def create_table(table_name: str, partition_key: str, partition_key_type: str, 
                       sort_key: Optional[str] = None, sort_key_type: Optional[str] = None,
                       read_capacity: int = 5, write_capacity: int = 5) -> dict:
    """✅ Create new DynamoDB table with partition and optional sort key"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        
        key_schema = [{"AttributeName": partition_key, "KeyType": "HASH"}]
        attr_definitions = [{"AttributeName": partition_key, "AttributeType": partition_key_type}]
        
        if sort_key:
            key_schema.append({"AttributeName": sort_key, "KeyType": "RANGE"})
            attr_definitions.append({"AttributeName": sort_key, "AttributeType": sort_key_type})
        
        params = {
            "TableName": table_name,
            "KeySchema": key_schema,
            "AttributeDefinitions": attr_definitions,
            "BillingMode": "PROVISIONED",
            "ProvisionedThroughput": {
                "ReadCapacityUnits": read_capacity,
                "WriteCapacityUnits": write_capacity
            }
        }
        
        dynamodb.create_table(**params)
        logger.info(f"✅ Table {table_name} created successfully")
        return {"success": True, "message": f"Table {table_name} created"}
    except ClientError as e:
        logger.error(f"❌ Error creating table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_table(table_name: str) -> dict:
    """🔎 Get detailed table information"""
    try:
        _, client = get_dynamodb_connection()
        response = client.describe_table(TableName=table_name)
        table = response["Table"]
        
        return {
            "success": True,
            "table": {
                "name": table["TableName"],
                "status": table["TableStatus"],
                "arn": table["TableArn"],
                "item_count": table.get("ItemCount", 0),
                "size_bytes": table.get("TableSizeBytes", 0),
                "partition_key": table["KeySchema"][0]["AttributeName"],
                "sort_key": table["KeySchema"][1]["AttributeName"] if len(table["KeySchema"]) > 1 else None,
                "read_capacity": table.get("ProvisionedThroughput", {}).get("ReadCapacityUnits"),
                "write_capacity": table.get("ProvisionedThroughput", {}).get("WriteCapacityUnits"),
                "billing_mode": table.get("BillingModeSummary", {}).get("BillingMode", "PROVISIONED")
            }
        }
    except ClientError as e:
        logger.error(f"❌ Error describing table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_tables() -> dict:
    """📋 List all tables in DynamoDB"""
    try:
        _, client = get_dynamodb_connection()
        response = client.list_tables()
        logger.info(f"✅ Listed {len(response['TableNames'])} tables")
        return {"success": True, "tables": response["TableNames"], "count": len(response["TableNames"])}
    except ClientError as e:
        logger.error(f"❌ Error listing tables: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_table(table_name: str) -> dict:
    """❌ Delete a table (irreversible)"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        table.delete()
        logger.info(f"✅ Table {table_name} deleted")
        return {"success": True, "message": f"Table {table_name} deleted"}
    except ClientError as e:
        logger.error(f"❌ Error deleting table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_table_throughput(table_name: str, read_capacity: int, write_capacity: int) -> dict:
    """⚡ Update table read/write provisioned throughput"""
    try:
        _, client = get_dynamodb_connection()
        client.update_table(
            TableName=table_name,
            ProvisionedThroughput={
                "ReadCapacityUnits": read_capacity,
                "WriteCapacityUnits": write_capacity
            }
        )
        logger.info(f"✅ Updated throughput for {table_name}")
        return {"success": True, "message": f"Throughput updated to R:{read_capacity}/W:{write_capacity}"}
    except ClientError as e:
        logger.error(f"❌ Error updating throughput: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def enable_pay_per_request(table_name: str) -> dict:
    """💰 Switch table to pay-per-request billing mode"""
    try:
        _, client = get_dynamodb_connection()
        client.update_table(
            TableName=table_name,
            BillingMode="PAY_PER_REQUEST"
        )
        logger.info(f"✅ {table_name} switched to pay-per-request")
        return {"success": True, "message": f"Table switched to PAY_PER_REQUEST"}
    except ClientError as e:
        logger.error(f"❌ Error switching billing mode: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== GLOBAL SECONDARY INDEX (GSI) OPERATIONS ====================

@mcp.tool()
async def create_gsi(table_name: str, index_name: str, partition_key: str, 
                     partition_key_type: str, sort_key: Optional[str] = None,
                     sort_key_type: Optional[str] = None, read_capacity: int = 5) -> dict:
    """🔑 Create Global Secondary Index (GSI)"""
    try:
        _, client = get_dynamodb_connection()
        
        key_schema = [{"AttributeName": partition_key, "KeyType": "HASH"}]
        attr_definitions = [{"AttributeName": partition_key, "AttributeType": partition_key_type}]
        
        if sort_key:
            key_schema.append({"AttributeName": sort_key, "KeyType": "RANGE"})
            attr_definitions.append({"AttributeName": sort_key, "AttributeType": sort_key_type})
        
        gsi = {
            "IndexName": index_name,
            "KeySchema": key_schema,
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": read_capacity,
                "WriteCapacityUnits": read_capacity
            }
        }
        
        client.update_table(
            TableName=table_name,
            AttributeDefinitions=attr_definitions,
            GlobalSecondaryIndexUpdates=[
                {"Create": gsi}
            ]
        )
        logger.info(f"✅ GSI {index_name} created")
        return {"success": True, "message": f"GSI {index_name} created on {table_name}"}
    except ClientError as e:
        logger.error(f"❌ Error creating GSI: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_gsi(table_name: str, index_name: str) -> dict:
    """🗑️ Delete Global Secondary Index"""
    try:
        _, client = get_dynamodb_connection()
        client.update_table(
            TableName=table_name,
            GlobalSecondaryIndexUpdates=[
                {"Delete": {"IndexName": index_name}}
            ]
        )
        logger.info(f"✅ GSI {index_name} deleted")
        return {"success": True, "message": f"GSI {index_name} deleted"}
    except ClientError as e:
        logger.error(f"❌ Error deleting GSI: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_gsi(table_name: str) -> dict:
    """📑 List all Global Secondary Indexes"""
    try:
        _, client = get_dynamodb_connection()
        response = client.describe_table(TableName=table_name)
        gsi_list = response["Table"].get("GlobalSecondaryIndexes", [])
        
        indexes = [
            {
                "name": idx["IndexName"],
                "status": idx["IndexStatus"],
                "size_bytes": idx.get("IndexSizeBytes", 0),
                "item_count": idx.get("ItemCount", 0)
            }
            for idx in gsi_list
        ]
        
        logger.info(f"✅ Found {len(indexes)} GSIs")
        return {"success": True, "indexes": indexes, "count": len(indexes)}
    except ClientError as e:
        logger.error(f"❌ Error listing GSI: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== ITEM DML OPERATIONS ====================

@mcp.tool()
async def put_item(table_name: str, item: dict) -> dict:
    """✍️ Put (insert/overwrite) a single item"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        table.put_item(Item=item)
        logger.info(f"✅ Item inserted into {table_name}")
        return {"success": True, "message": "Item inserted"}
    except ClientError as e:
        logger.error(f"❌ Error putting item: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_put_items(table_name: str, items: List[dict]) -> dict:
    """📦 Batch insert multiple items efficiently"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        with table.batch_writer(batch_size=25) as batch:
            for item in items:
                batch.put_item(Item=item)
        
        logger.info(f"✅ Batch inserted {len(items)} items")
        return {"success": True, "inserted_count": len(items)}
    except ClientError as e:
        logger.error(f"❌ Error batch putting items: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_item(table_name: str, key: dict, consistent_read: bool = False) -> dict:
    """📖 Get a single item by key"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        response = table.get_item(Key=key, ConsistentRead=consistent_read)
        
        item = response.get("Item")
        logger.info(f"✅ Retrieved item from {table_name}")
        return {"success": True, "item": json.loads(json.dumps(item, default=decimal_to_float)) if item else None}
    except ClientError as e:
        logger.error(f"❌ Error getting item: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_get_items(table_name: str, keys: List[dict]) -> dict:
    """🎯 Batch get multiple items by keys"""
    try:
        _, client = get_dynamodb_connection()
        
        request_items = {
            table_name: {
                "Keys": keys
            }
        }
        
        response = client.batch_get_item(RequestItems=request_items)
        items = response.get("Responses", {}).get(table_name, [])
        
        logger.info(f"✅ Retrieved {len(items)} items")
        return {"success": True, "items": json.loads(json.dumps(items, default=decimal_to_float)), "count": len(items)}
    except ClientError as e:
        logger.error(f"❌ Error batch getting items: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def update_item(table_name: str, key: dict, updates: dict, add_attributes: bool = False) -> dict:
    """🔄 Update attributes of an item"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        if add_attributes:
            update_expr = "SET " + ", ".join([f"#{k}={k}" for k in updates.keys()])
        else:
            update_expr = "SET " + ", ".join([f"#{k}=:{k}" for k in updates.keys()])
        
        attr_names = {f"#{k}": k for k in updates.keys()}
        attr_values = {f":{k}": v for k, v in updates.items()} if not add_attributes else {}
        
        table.update_item(
            Key=key,
            UpdateExpression=update_expr,
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=attr_values if attr_values else None
        )
        logger.info(f"✅ Item updated in {table_name}")
        return {"success": True, "message": "Item updated"}
    except ClientError as e:
        logger.error(f"❌ Error updating item: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def delete_item(table_name: str, key: dict) -> dict:
    """🗑️ Delete a single item"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        table.delete_item(Key=key)
        logger.info(f"✅ Item deleted from {table_name}")
        return {"success": True, "message": "Item deleted"}
    except ClientError as e:
        logger.error(f"❌ Error deleting item: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def batch_delete_items(table_name: str, keys: List[dict]) -> dict:
    """🧹 Batch delete multiple items"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        with table.batch_writer() as batch:
            for key in keys:
                batch.delete_item(Key=key)
        
        logger.info(f"✅ Deleted {len(keys)} items")
        return {"success": True, "deleted_count": len(keys)}
    except ClientError as e:
        logger.error(f"❌ Error batch deleting: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== QUERY OPERATIONS ====================

@mcp.tool()
async def query_items(table_name: str, partition_key: str, partition_value: Any, 
                      sort_key: Optional[str] = None, sort_op: str = "=") -> dict:
    """🔍 Query items by partition key (and optionally sort key)"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        from boto3.dynamodb.conditions import Key
        
        key_expr = Key(partition_key).eq(partition_value)
        
        if sort_key:
            if sort_op == "=":
                key_expr = key_expr & Key(sort_key).eq(partition_value)
            elif sort_op == "begins_with":
                key_expr = key_expr & Key(sort_key).begins_with(partition_value)
            elif sort_op == ">":
                key_expr = key_expr & Key(sort_key).gt(partition_value)
            elif sort_op == "<":
                key_expr = key_expr & Key(sort_key).lt(partition_value)
        
        response = table.query(KeyConditionExpression=key_expr, Limit=100)
        items = response.get("Items", [])
        
        logger.info(f"✅ Query returned {len(items)} items")
        return {"success": True, "items": json.loads(json.dumps(items, default=decimal_to_float)), "count": len(items)}
    except Exception as e:
        logger.error(f"❌ Error querying items: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_with_filter(table_name: str, partition_key: str, partition_value: Any, 
                            filter_attr: str, filter_value: Any, filter_op: str = "=") -> dict:
    """🎯 Query with additional filter expression"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        from boto3.dynamodb.conditions import Key, Attr
        
        key_expr = Key(partition_key).eq(partition_value)
        
        if filter_op == "=":
            filter_expr = Attr(filter_attr).eq(filter_value)
        elif filter_op == "contains":
            filter_expr = Attr(filter_attr).contains(filter_value)
        elif filter_op == "begins_with":
            filter_expr = Attr(filter_attr).begins_with(filter_value)
        else:
            filter_expr = Attr(filter_attr).eq(filter_value)
        
        response = table.query(
            KeyConditionExpression=key_expr,
            FilterExpression=filter_expr,
            Limit=100
        )
        items = response.get("Items", [])
        
        logger.info(f"✅ Filtered query returned {len(items)} items")
        return {"success": True, "items": json.loads(json.dumps(items, default=decimal_to_float)), "count": len(items)}
    except Exception as e:
        logger.error(f"❌ Error in filtered query: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def scan_table(table_name: str, limit: int = 100) -> dict:
    """📊 Scan entire table (expensive operation)"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        response = table.scan(Limit=limit)
        items = response.get("Items", [])
        
        logger.info(f"✅ Table scan returned {len(items)} items")
        return {"success": True, "items": json.loads(json.dumps(items, default=decimal_to_float)), "count": len(items)}
    except ClientError as e:
        logger.error(f"❌ Error scanning table: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def scan_with_filter(table_name: str, filter_attr: str, filter_value: Any, limit: int = 100) -> dict:
    """🔎 Scan table with filter expression"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        from boto3.dynamodb.conditions import Attr
        
        response = table.scan(
            FilterExpression=Attr(filter_attr).eq(filter_value),
            Limit=limit
        )
        items = response.get("Items", [])
        
        logger.info(f"✅ Filtered scan returned {len(items)} items")
        return {"success": True, "items": json.loads(json.dumps(items, default=decimal_to_float)), "count": len(items)}
    except Exception as e:
        logger.error(f"❌ Error in filtered scan: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def query_by_gsi(table_name: str, index_name: str, partition_key: str, partition_value: Any) -> dict:
    """🔑 Query using a Global Secondary Index"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        from boto3.dynamodb.conditions import Key
        
        response = table.query(
            IndexName=index_name,
            KeyConditionExpression=Key(partition_key).eq(partition_value),
            Limit=100
        )
        items = response.get("Items", [])
        
        logger.info(f"✅ GSI query returned {len(items)} items")
        return {"success": True, "items": json.loads(json.dumps(items, default=decimal_to_float)), "count": len(items)}
    except Exception as e:
        logger.error(f"❌ Error querying GSI: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def count_items(table_name: str, partition_key: Optional[str] = None, partition_value: Optional[Any] = None) -> dict:
    """📈 Count items in table or by key"""
    try:
        dynamodb, _ = get_dynamodb_connection()
        table = dynamodb.Table(table_name)
        
        if partition_key:
            from boto3.dynamodb.conditions import Key
            response = table.query(
                KeyConditionExpression=Key(partition_key).eq(partition_value),
                Select="COUNT"
            )
        else:
            response = table.scan(Select="COUNT")
        
        count = response.get("Count", 0)
        logger.info(f"✅ Item count: {count}")
        return {"success": True, "count": count}
    except Exception as e:
        logger.error(f"❌ Error counting items: {str(e)}")
        return {"success": False, "error": str(e)}

# ==================== TTL & ADMIN OPERATIONS ====================

@mcp.tool()
async def enable_ttl(table_name: str, ttl_attribute: str) -> dict:
    """⏰ Enable Time-To-Live (TTL) on an attribute"""
    try:
        _, client = get_dynamodb_connection()
        client.update_time_to_live(
            TableName=table_name,
            TimeToLiveSpecification={
                "AttributeName": ttl_attribute,
                "Enabled": True
            }
        )
        logger.info(f"✅ TTL enabled on {ttl_attribute}")
        return {"success": True, "message": f"TTL enabled on attribute {ttl_attribute}"}
    except ClientError as e:
        logger.error(f"❌ Error enabling TTL: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def describe_ttl(table_name: str) -> dict:
    """🕐 Get TTL specification"""
    try:
        _, client = get_dynamodb_connection()
        response = client.describe_time_to_live(TableName=table_name)
        ttl_spec = response.get("TimeToLiveDescription", {})
        
        return {
            "success": True,
            "ttl": {
                "attribute": ttl_spec.get("AttributeName"),
                "status": ttl_spec.get("TimeToLiveStatus")
            }
        }
    except ClientError as e:
        logger.error(f"❌ Error describing TTL: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def enable_streams(table_name: str, stream_view_type: str = "NEW_AND_OLD_IMAGES") -> dict:
    """🌊 Enable DynamoDB Streams"""
    try:
        _, client = get_dynamodb_connection()
        client.update_table(
            TableName=table_name,
            StreamSpecification={
                "StreamEnabled": True,
                "StreamViewType": stream_view_type
            }
        )
        logger.info(f"✅ Streams enabled on {table_name}")
        return {"success": True, "message": f"Streams enabled with view type {stream_view_type}"}
    except ClientError as e:
        logger.error(f"❌ Error enabling streams: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def get_table_stats(table_name: str) -> dict:
    """📊 Get comprehensive table statistics"""
    try:
        _, client = get_dynamodb_connection()
        response = client.describe_table(TableName=table_name)
        table = response["Table"]
        
        stats = {
            "table_name": table["TableName"],
            "status": table["TableStatus"],
            "item_count": table.get("ItemCount", 0),
            "size_bytes": table.get("TableSizeBytes", 0),
            "size_mb": round(table.get("TableSizeBytes", 0) / 1024 / 1024, 2),
            "read_capacity": table.get("ProvisionedThroughput", {}).get("ReadCapacityUnits"),
            "write_capacity": table.get("ProvisionedThroughput", {}).get("WriteCapacityUnits"),
            "billing_mode": table.get("BillingModeSummary", {}).get("BillingMode", "PROVISIONED"),
            "arn": table["TableArn"]
        }
        
        logger.info(f"✅ Retrieved stats for {table_name}")
        return {"success": True, "stats": stats}
    except ClientError as e:
        logger.error(f"❌ Error getting stats: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_backup(table_name: str, backup_name: str) -> dict:
    """💾 Create on-demand backup"""
    try:
        _, client = get_dynamodb_connection()
        response = client.create_backup(
            TableName=table_name,
            BackupName=backup_name
        )
        backup_arn = response["BackupDetails"]["BackupArn"]
        logger.info(f"✅ Backup created: {backup_name}")
        return {"success": True, "backup_arn": backup_arn, "message": f"Backup {backup_name} created"}
    except ClientError as e:
        logger.error(f"❌ Error creating backup: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def list_backups(table_name: str) -> dict:
    """📋 List all backups for a table"""
    try:
        _, client = get_dynamodb_connection()
        response = client.list_backups(TableName=table_name)
        backups = response.get("BackupSummaries", [])
        
        backup_info = [
            {
                "name": b["BackupName"],
                "status": b["BackupStatus"],
                "creation_time": str(b["BackupCreationDateTime"]),
                "size_bytes": b.get("BackupSizeBytes", 0)
            }
            for b in backups
        ]
        
        logger.info(f"✅ Found {len(backup_info)} backups")
        return {"success": True, "backups": backup_info, "count": len(backup_info)}
    except ClientError as e:
        logger.error(f"❌ Error listing backups: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
async def restore_backup(backup_arn: str, target_table_name: str) -> dict:
    """♻️ Restore table from backup"""
    try:
        _, client = get_dynamodb_connection()
        client.restore_table_from_backup(
            TargetTableName=target_table_name,
            BackupArn=backup_arn
        )
        logger.info(f"✅ Table restored to {target_table_name}")
        return {"success": True, "message": f"Table restored to {target_table_name}"}
    except ClientError as e:
        logger.error(f"❌ Error restoring backup: {str(e)}")
        return {"success": False, "error": str(e)}

async def main():
    """Start the DynamoDB MCP server"""
    try:
        logger.info("🚀 Starting DynamoDB MCP Server on port 7090")
        await mcp.run_async(transport="sse", host="0.0.0.0", port=7090)
    except KeyboardInterrupt:
        logger.info("⏹️ Shutting down server")

if __name__ == "__main__":
    asyncio.run(main())

# ==================== ROLE-BASED PROMPTS ====================
"""
DBA Operations Prompt:
You are a DynamoDB Database Administrator. Help manage table architecture, throughput capacity, backups, 
and monitoring. Focus on scaling strategies, billing optimization, and performance tuning. Use tools to 
describe tables, manage throughput, create backups, and monitor table statistics.

Data Engineer Prompt:
You are a Data Engineer working with DynamoDB. Help design efficient data models, manage GSIs for query patterns,
batch operations for bulk data loading, and data migration tasks. Focus on query optimization and schema design.

Data Analyst Prompt:
You are a Data Analyst querying DynamoDB tables. Help explore data through queries, scans, and aggregations.
Focus on retrieving insights from data, working with filters, and analyzing item distributions across keys.
"""
