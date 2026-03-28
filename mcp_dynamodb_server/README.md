# AWS DynamoDB MCP Server 🚀

## Overview
FastMCP-based server for AWS DynamoDB NoSQL database operations with full support for serverless, on-demand, and provisioned capacity models.

## Features
- **Fully Managed**: AWS-managed NoSQL
- **Serverless**: Pay-per-request pricing
- **Global Tables**: Multi-region replication
- **Query Support**: Key and scan queries
- **Batch Operations**: Efficient bulk operations
- **Auto-scaling**: Automatic capacity management

## Setup & Installation

### Prerequisites
- Python 3.9+
- AWS Account with DynamoDB access
- AWS credentials configured

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export AWS_REGION="us-east-1"
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
```

### Running
```bash
python server.py
```

## Tools Available

### list_tables
List all DynamoDB tables.

### describe_table
Get detailed table information.

### put_item
Insert or overwrite item.

### get_item
Retrieve specific item.

### query_items
Query items using key conditions.

### scan_table
Scan table items with pagination.

### update_item
Update existing item attributes.

### delete_item
Delete item from table.

### batch_write
Batch write multiple items.

### get_table_stats
Get table statistics and metrics.

## Usage Examples

### Create and Put Item
```python
await client.call_tool("put_item", {
    "table_name": "users",
    "item": {
        "user_id": "123",
        "name": "John",
        "email": "john@example.com",
        "created": "2024-06-15"
    }
})
```

### Query Items
```python
await client.call_tool("query_items", {
    "table_name": "users",
    "key_condition": {
        "condition": "user_id = :uid",
        "values": {":uid": "123"}
    },
    "limit": 10
})
```

### Batch Write
```python
await client.call_tool("batch_write", {
    "table_name": "users",
    "items": [
        {"user_id": "1", "name": "User 1"},
        {"user_id": "2", "name": "User 2"},
        {"user_id": "3", "name": "User 3"}
    ]
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
boto3>=1.26
```

## Use Cases
- Web applications
- Mobile backends
- Real-time analytics
- IoT applications
- Gaming leaderboards
- Serverless architecture

## Best Practices
- Use TTL for expiring data
- Implement query optimization
- Monitor consumed capacity
- Use batch operations
- Design efficient key schemas

## Troubleshooting
- Verify AWS credentials
- Check table permissions
- Monitor read/write capacity
- Review CloudWatch metrics
