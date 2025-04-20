import os
import json
import logging
from datetime import datetime
from typing import Any, Sequence
from functools import lru_cache
import base64
import io
import boto3
import asyncio
import mcp.server.stdio
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

from mcp.types import Tool


def get_s3_tools() -> list[Tool]:
    return [
        Tool(
            name="s3_bucket_create",
            description="Create a new S3 bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket to create"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="s3_bucket_list",
            description="List all S3 buckets",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="s3_bucket_delete",
            description="Delete an S3 bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket to delete"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="s3_object_upload",
            description="Upload an object to S3",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket"
                    },
                    "object_key": {
                        "type": "string",
                        "description": "Key/path of the object in the bucket"
                    },
                    "file_content": {
                        "type": "string",
                        "description": "Base64 encoded file content for upload"
                    }
                },
                "required": ["bucket_name", "object_key", "file_content"]
            }
        ),
        Tool(
            name="s3_object_delete",
            description="Delete an object from S3",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket"
                    },
                    "object_key": {
                        "type": "string",
                        "description": "Key/path of the object to delete"
                    }
                },
                "required": ["bucket_name", "object_key"]
            }
        ),
        Tool(
            name="s3_object_list",
            description="List objects in an S3 bucket",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket"
                    }
                },
                "required": ["bucket_name"]
            }
        ),
        Tool(
            name="s3_object_read",
            description="Read an object's content from S3",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {
                        "type": "string",
                        "description": "Name of the S3 bucket"
                    },
                    "object_key": {
                        "type": "string",
                        "description": "Key/path of the object to read"
                    }
                },
                "required": ["bucket_name", "object_key"]
            }
        ),
    ]


def get_dynamodb_tools() -> list[Tool]:
    return [
        Tool(
            name="dynamodb_table_create",
            description="Create a new DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "key_schema": {
                        "type": "array",
                        "description": "Key schema for table creation"
                    },
                    "attribute_definitions": {
                        "type": "array",
                        "description": "Attribute definitions for table creation"
                    }
                },
                "required": ["table_name", "key_schema", "attribute_definitions"]
            }
        ),
        Tool(
            name="dynamodb_table_describe",
            description="Get details about a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="dynamodb_table_list",
            description="List all DynamoDB tables",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="dynamodb_table_delete",
            description="Delete a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="dynamodb_table_update",
            description="Update a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "attribute_definitions": {
                        "type": "array",
                        "description": "Updated attribute definitions"
                    }
                },
                "required": ["table_name", "attribute_definitions"]
            }
        ),
        Tool(
            name="dynamodb_item_put",
            description="Put an item into a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "item": {
                        "type": "object",
                        "description": "Item data to put"
                    }
                },
                "required": ["table_name", "item"]
            }
        ),
        Tool(
            name="dynamodb_item_get",
            description="Get an item from a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "key": {
                        "type": "object",
                        "description": "Key to identify the item"
                    }
                },
                "required": ["table_name", "key"]
            }
        ),
        Tool(
            name="dynamodb_item_update",
            description="Update an item in a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "key": {
                        "type": "object",
                        "description": "Key to identify the item"
                    },
                    "item": {
                        "type": "object",
                        "description": "Updated item data"
                    }
                },
                "required": ["table_name", "key", "item"]
            }
        ),
        Tool(
            name="dynamodb_item_delete",
            description="Delete an item from a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "key": {
                        "type": "object",
                        "description": "Key to identify the item"
                    }
                },
                "required": ["table_name", "key"]
            }
        ),
        Tool(
            name="dynamodb_item_query",
            description="Query items in a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "key_condition": {
                        "type": "string",
                        "description": "Key condition expression"
                    },
                    "expression_values": {
                        "type": "object",
                        "description": "Expression attribute values"
                    }
                },
                "required": ["table_name", "key_condition", "expression_values"]
            }
        ),
        Tool(
            name="dynamodb_item_scan",
            description="Scan items in a DynamoDB table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "filter_expression": {
                        "type": "string",
                        "description": "Filter expression"
                    },
                    "expression_attributes": {
                        "type": "object",
                        "properties": {
                            "values": {
                                "type": "object",
                                "description": "Expression attribute values"
                            },
                            "names": {
                                "type": "object",
                                "description": "Expression attribute names"
                            }
                        }
                    }
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="dynamodb_batch_get",
            description="Batch get multiple items from DynamoDB tables",
            inputSchema={
                "type": "object",
                "properties": {
                    "request_items": {
                        "type": "object",
                        "description": "Map of table names to keys to retrieve",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "Keys": {
                                    "type": "array",
                                    "items": {
                                        "type": "object"
                                    }
                                },
                                "ConsistentRead": {
                                    "type": "boolean"
                                },
                                "ProjectionExpression": {
                                    "type": "string"
                                }
                            },
                            "required": ["Keys"]
                        }
                    }
                },
                "required": ["request_items"]
            }
        ),
        Tool(
            name="dynamodb_item_batch_write",
            description="Batch write operations (put/delete) for DynamoDB items",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["put", "delete"],
                        "description": "Type of batch operation (put or delete)"
                    },
                    "items": {
                        "type": "array",
                        "description": "Array of items to process"
                    },
                    "key_attributes": {
                        "type": "array",
                        "description": "For delete operations, specify which attributes form the key",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["table_name", "operation", "items"]
            }
        ),
        Tool(
            name="dynamodb_describe_ttl",
            description="Get the TTL settings for a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    }
                },
                "required": ["table_name"]
            }
        ),

        Tool(
            name="dynamodb_update_ttl",
            description="Update the TTL settings for a table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the DynamoDB table"
                    },
                    "ttl_enabled": {
                        "type": "boolean",
                        "description": "Whether TTL should be enabled"
                    },
                    "ttl_attribute": {
                        "type": "string",
                        "description": "The attribute name to use for TTL"
                    }
                },
                "required": ["table_name", "ttl_enabled", "ttl_attribute"]
            }
        ),
        Tool(
            name="dynamodb_batch_execute",
            description="Execute multiple PartiQL statements in a batch",
            inputSchema={
                "type": "object",
                "properties": {
                    "statements": {
                        "type": "array",
                        "description": "List of PartiQL statements to execute",
                        "items": {
                            "type": "string"
                        }
                    },
                    "parameters": {
                        "type": "array",
                        "description": "List of parameter lists for each statement",
                        "items": {
                            "type": "array"
                        }
                    }
                },
                "required": ["statements", "parameters"]
            }
        ),
    ]


def get_aws_tools() -> list[Tool]:
    return [
        *get_s3_tools(),
        *get_dynamodb_tools()
    ]
def get_dynamodb_type(value):
    if isinstance(value, str):
        return {'S': value}
    elif isinstance(value, (int, float)):
        return {'N': str(value)}
    elif isinstance(value, bool):
        return {'BOOL': value}
    elif value is None:
        return {'NULL': True}
    elif isinstance(value, list):
        return {'L': [get_dynamodb_type(v) for v in value]}
    elif isinstance(value, dict):
        return {'M': {k: get_dynamodb_type(v) for k, v in value.items()}}
    else:
        raise ValueError(
            f"Unsupported type for DynamoDB: {type(value)}")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aws-mcp-server")


def custom_json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class AWSManager:
    def __init__(self):
        logger.info("Initializing AWSManager")
        self.audit_entries: list[dict] = []

    @lru_cache(maxsize=None)
    def get_boto3_client(self, service_name: str, region_name: str = None):
        """Get a boto3 client using explicit credentials if available"""
        try:
            logger.info(f"Creating boto3 client for service: {service_name}")
            region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
            if not region_name:
                raise ValueError(
                    "AWS region is not specified and not set in the environment.")

            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            if aws_access_key and aws_secret_key:
                logger.debug("Using explicit AWS credentials")
                session = boto3.Session(
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region_name
                )
            else:
                aws_profile = os.getenv("AWS_PROFILE")
                if aws_profile:
                    logger.debug(f"Using AWS profile: {aws_profile}")
                    session = boto3.Session(profile_name=aws_profile, region_name=region_name)
                else:
                    logger.debug("Using default AWS credential chain")
                    session = boto3.Session(region_name=region_name)
            return session.client(service_name)
        except Exception as e:
            logger.error(f"Failed to create boto3 client for {service_name}: {e}")
            raise RuntimeError(f"Failed to create boto3 client: {e}")

    def _synthesize_audit_log(self) -> str:
        """Generate formatted audit log from entries"""
        logger.debug("Synthesizing audit log")
        if not self.audit_entries:
            return "No AWS operations have been performed yet."

        report = "📋 AWS Operations Audit Log 📋\n\n"
        for entry in self.audit_entries:
            report += f"[{entry['timestamp']}]\n"
            report += f"Service: {entry['service']}\n"
            report += f"Operation: {entry['operation']}\n"
            report += f"Parameters: {json.dumps(entry['parameters'], indent=2)}\n"
            report += "-" * 50 + "\n"

        return report

    def log_operation(self, service: str, operation: str, parameters: dict) -> None:
        """Log an AWS operation to the audit log"""
        logger.info(
            f"Logging operation - Service: {service}, Operation: {operation}")
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": service,
            "operation": operation,
            "parameters": parameters
        }
        self.audit_entries.append(audit_entry)


async def main():
    logger.info("Starting AWS MCP Server")

    aws = AWSManager()
    server = Server("aws-mcp-server")

    logger.debug("Registering handlers")

    @server.list_resources()
    async def handle_list_resources() -> list[Resource]:
        logger.debug("Handling list_resources request")
        return [
            Resource(
                uri=AnyUrl("audit://aws-operations"),
                name="AWS Operations Audit Log",
                description="A log of all AWS operations performed through this server",
                mimeType="text/plain",
            )
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        logger.debug(f"Handling read_resource request for URI: {uri}")
        if uri.scheme != "audit":
            logger.error(f"Unsupported URI scheme: {uri.scheme}")
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

        path = str(uri).replace("audit://", "")
        if path != "aws-operations":
            logger.error(f"Unknown resource path: {path}")
            raise ValueError(f"Unknown resource path: {path}")

        return aws._synthesize_audit_log()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available AWS tools"""
        logger.debug("Handling list_tools request")
        return get_aws_tools()

    async def handle_s3_operations(aws: AWSManager, name: str, arguments: dict) -> list[TextContent]:
        """Handle S3-specific operations"""
        s3_client = aws.get_boto3_client('s3')
        response = None

        if name == "s3_bucket_create":
            response = s3_client.create_bucket(Bucket=arguments["bucket_name"],
                                               CreateBucketConfiguration={
                                                   'LocationConstraint': os.getenv("AWS_REGION") or 'us-east-1'
                                               })
        elif name == "s3_bucket_list":
            response = s3_client.list_buckets()
        elif name == "s3_bucket_delete":
            response = s3_client.delete_bucket(Bucket=arguments["bucket_name"])
        elif name == "s3_object_upload":
            response = s3_client.upload_fileobj(
                io.BytesIO(base64.b64decode(arguments["file_content"])),
                arguments["bucket_name"],
                arguments["object_key"])
        elif name == "s3_object_delete":
            response = s3_client.delete_object(
                Bucket=arguments["bucket_name"],
                Key=arguments["object_key"]
            )
        elif name == "s3_object_list":
            response = s3_client.list_objects_v2(
                Bucket=arguments["bucket_name"])
        elif name == "s3_object_read":
            logging.info(f"Reading object: {arguments['object_key']}")
            response = s3_client.get_object(
                Bucket=arguments["bucket_name"],
                Key=arguments["object_key"]
            )
            content = response['Body'].read().decode('utf-8')
            return [TextContent(type="text", text=content)]
        else:
            raise ValueError(f"Unknown S3 operation: {name}")

        aws.log_operation("s3", name.replace("s3_", ""), arguments)
        return [TextContent(type="text", text=f"Operation Result:\n{json.dumps(response, indent=2, default=custom_json_serializer)}")]

    async def handle_dynamodb_operations(aws: AWSManager, name: str, arguments: dict) -> list[TextContent]:
        """Handle DynamoDB-specific operations"""
        dynamodb_client = aws.get_boto3_client('dynamodb')
        response = None

        if name == "dynamodb_table_create":
            response = dynamodb_client.create_table(
                TableName=arguments["table_name"],
                KeySchema=arguments["key_schema"],
                AttributeDefinitions=arguments["attribute_definitions"],
                BillingMode="PAY_PER_REQUEST"
            )
        elif name == "dynamodb_table_describe":
            response = dynamodb_client.describe_table(
                TableName=arguments["table_name"])
        elif name == "dynamodb_table_list":
            response = dynamodb_client.list_tables()
        elif name == "dynamodb_table_delete":
            response = dynamodb_client.delete_table(
                TableName=arguments["table_name"])
        elif name == "dynamodb_table_update":
            update_params = {
                "TableName": arguments["table_name"],
                "AttributeDefinitions": arguments["attribute_definitions"]
            }
            response = dynamodb_client.update_table(**update_params)
        elif name == "dynamodb_describe_ttl":
            response = dynamodb_client.describe_time_to_live(
                TableName=arguments["table_name"]
            )
        elif name == "dynamodb_update_ttl":
            response = dynamodb_client.update_time_to_live(
                TableName=arguments["table_name"],
                TimeToLiveSpecification={
                    'Enabled': arguments["ttl_enabled"],
                    'AttributeName': arguments["ttl_attribute"]
                }
            )
        elif name == "dynamodb_item_put":
            response = dynamodb_client.put_item(
                TableName=arguments["table_name"],
                Item=arguments["item"]
            )
        elif name == "dynamodb_item_get":
            response = dynamodb_client.get_item(
                TableName=arguments["table_name"],
                Key=arguments["key"]
            )
        elif name == "dynamodb_item_update":
            response = dynamodb_client.update_item(
                TableName=arguments["table_name"],
                Key=arguments["key"],
                AttributeUpdates=arguments["item"]
            )
        elif name == "dynamodb_item_delete":
            response = dynamodb_client.delete_item(
                TableName=arguments["table_name"],
                Key=arguments["key"]
            )
        elif name == "dynamodb_item_query":
            response = dynamodb_client.query(
                TableName=arguments["table_name"],
                KeyConditionExpression=arguments["key_condition"],
                ExpressionAttributeValues=arguments["expression_values"]
            )
        elif name == "dynamodb_item_scan":
            scan_params = {"TableName": arguments["table_name"]}

            if "filter_expression" in arguments:
                scan_params["FilterExpression"] = arguments["filter_expression"]

                if "expression_attributes" in arguments:
                    attrs = arguments["expression_attributes"]
                    if "names" in attrs:
                        scan_params["ExpressionAttributeNames"] = attrs["names"]
                    if "values" in attrs:
                        scan_params["ExpressionAttributeValues"] = attrs["values"]

            response = dynamodb_client.scan(**scan_params)
        elif name == "dynamodb_batch_get":
            response = dynamodb_client.batch_get_item(
                RequestItems=arguments["request_items"]
            )
        elif name == "dynamodb_item_batch_write":
            table_name = arguments["table_name"]
            operation = arguments["operation"]
            items = arguments["items"]

            if not items:
                raise ValueError("No items provided for batch operation")

            batch_size = 25
            total_items = len(items)
            processed_items = 0
            failed_items = []

            for i in range(0, total_items, batch_size):
                batch = items[i:i + batch_size]
                request_items = {table_name: []}

                for item in batch:
                    if operation == "put":
                        formatted_item = {k: get_dynamodb_type(
                            v) for k, v in item.items()}
                        request_items[table_name].append({
                            'PutRequest': {'Item': formatted_item}
                        })
                    elif operation == "delete":
                        key_attrs = arguments.get(
                            "key_attributes", list(item.keys()))
                        formatted_key = {k: get_dynamodb_type(
                            item[k]) for k in key_attrs}
                        request_items[table_name].append({
                            'DeleteRequest': {'Key': formatted_key}
                        })

                try:
                    response = dynamodb_client.batch_write_item(
                        RequestItems=request_items)
                    processed_items += len(batch) - len(
                        response.get('UnprocessedItems', {}
                                     ).get(table_name, [])
                    )

                    unprocessed = response.get('UnprocessedItems', {})
                    retry_count = 0
                    max_retries = 3
                    while unprocessed and retry_count < max_retries:
                        await asyncio.sleep(2 ** retry_count)
                        retry_response = dynamodb_client.batch_write_item(
                            RequestItems=unprocessed)
                        unprocessed = retry_response.get(
                            'UnprocessedItems', {})
                        retry_count += 1

                    if unprocessed:
                        failed_items.extend([
                            item['PutRequest']['Item'] if 'PutRequest' in item else item['DeleteRequest']['Key']
                            for item in unprocessed.get(table_name, [])
                        ])

                except Exception as e:
                    logger.error(f"Error processing batch: {str(e)}")
                    failed_items.extend(batch)

            response = {
                "total_items": total_items,
                "processed_items": processed_items,
                "failed_items": len(failed_items),
                "failed_items_details": failed_items if failed_items else None
            }
        elif name == "dynamodb_batch_execute":
            response = dynamodb_client.batch_execute_statement(
                Statements=[{
                    'Statement': statement,
                    'Parameters': params
                } for statement, params in zip(arguments["statements"], arguments["parameters"])]
            )
        else:
            raise ValueError(f"Unknown DynamoDB operation: {name}")

        aws.log_operation("dynamodb", name.replace("dynamodb_", ""), arguments)
        return [TextContent(type="text", text=f"Operation Result:\n{json.dumps(response, indent=2, default=custom_json_serializer)}")]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle AWS tool operations"""
        logger.info(f"Handling tool call: {name}")
        logger.debug(f"Tool arguments: {arguments}")

        if not isinstance(arguments, dict):
            logger.error("Invalid arguments: not a dictionary")
            raise ValueError("Invalid arguments")

        try:
            if name.startswith("s3_"):
                return await handle_s3_operations(aws, name, arguments)
            # elif name.startswith("dynamodb_"):
            #     return await handle_dynamodb_operations(aws, name, arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            logger.error(f"Operation failed: {str(e)}")
            raise RuntimeError(f"Operation failed: {str(e)}")

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-server-aws",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
