# MCP AWS Server ☁️

## Overview
An MCP server providing comprehensive AWS service integration. This server enables agents to interact with AWS services including S3 (Simple Storage Service), RDS (Relational Database Service), and other AWS resources for cloud-based operations.

## Features
- **S3 Bucket Operations**: Create, list, upload, download, delete objects
- **RDS Database Management**: List databases, execute queries, manage instances
- **EC2 Integration**: Instance management and information retrieval
- **CloudWatch**: Monitoring and logging integration
- **IAM Support**: Basic IAM operations
- **Resource Discovery**: List and explore AWS resources

## Tools Available

### S3 Tools
- `s3_bucket_create(bucket_name)` - Create new S3 bucket
- `s3_bucket_list()` - List all S3 buckets
- `s3_object_upload(bucket, key, content)` - Upload object to bucket
- `s3_object_list(bucket)` - List objects in bucket
- `s3_object_download(bucket, key)` - Download object from bucket
- `s3_object_delete(bucket, key)` - Delete object from bucket

### RDS Tools
- `rds_list_databases()` - List RDS database instances
- `rds_describe_database(db_id)` - Get database details
- `rds_execute_query(db_id, sql)` - Execute SQL on RDS instance

### EC2 Tools
- `ec2_list_instances()` - List EC2 instances
- `ec2_describe_instance(instance_id)` - Get instance details
- `ec2_start_instance(instance_id)` - Start instance
- `ec2_stop_instance(instance_id)` - Stop instance

### Additional Tools
- CloudWatch metrics
- Monitoring and logging
- Resource tagging
- Cost estimation

## Setup & Usage

### Installation
```bash
pip install fastmcp boto3 mcp
```

### AWS Configuration
Set up AWS credentials:
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment variables
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="us-east-1"

# Option 3: ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

### Running the Server
```bash
# Stdio transport
python server.py

# SSE transport available
```

## Files
- `server.py` - Main AWS server implementation
- `tools.py` - Tool definitions and logic
- `utils.py` - Utility functions
- `__init__.py` - Package initialization
- `mcp_ref.json` - MCP reference documentation
- `mcp_servers.json` - Server configuration

## AWS Service Integration

### S3 Operations
- Create buckets with configurations
- Upload files with metadata
- Download and delete objects
- List bucket contents with filtering
- Set bucket policies and ACLs

### RDS Operations
- Manage database instances
- Execute SQL queries
- Monitor performance metrics
- Backup and restore operations
- Security group management

### EC2 Operations
- Instance lifecycle management
- Security group configuration
- Key pair management
- Elastic IP association
- Load balancer integration

### Monitoring & Logging
- CloudWatch metrics
- Log group management
- Alarm creation and monitoring
- Custom dashboards

## Use Cases
- **Cloud Data Management**: Upload, download, and manage files on S3
- **Database Operations**: Query RDS databases from agents
- **Infrastructure Management**: Control EC2 instances
- **Cloud Analytics**: Monitor performance with CloudWatch
- **Backup & Recovery**: S3-based backup operations
- **Multi-region Deployment**: Deploy resources across regions

## API Examples

### Create S3 Bucket
```python
result = s3_bucket_create("my-data-bucket-2024")
# Creates new bucket with standard configuration
```

### Upload to S3
```python
result = s3_object_upload(
    bucket="my-bucket",
    key="documents/report.pdf",
    content=file_content
)
```

### List RDS Databases
```python
databases = rds_list_databases()
# Returns: List of database instances with details
```

### Execute RDS Query
```python
result = rds_execute_query(
    db_id="mydb-instance",
    sql="SELECT * FROM users WHERE created > NOW() - INTERVAL 7 DAY"
)
```

## Security Features
- **IAM Authentication**: Uses AWS IAM for secure access
- **Credential Management**: Supports multiple credential sources
- **Encryption**: Support for S3 and database encryption
- **VPC Support**: Private network operations
- **Audit Logging**: CloudTrail integration
- **Resource Policies**: Fine-grained access control

## Error Handling
- Proper AWS error handling
- Detailed error messages
- Retry logic for transient failures
- Timeout management
- Connection error recovery

## Performance
- Parallel operations support
- Batch processing capabilities
- Connection pooling
- Caching for frequently accessed resources
- Efficient pagination for large datasets

## Cost Optimization
- Resource monitoring
- Usage reporting
- Cost estimation tools
- Reserved capacity management
- Auto-scaling integration

## Best Practices
1. Use IAM roles, not hardcoded credentials
2. Enable S3 versioning for data protection
3. Set lifecycle policies for old objects
4. Use VPC for RDS instances
5. Enable backup and replication
6. Monitor with CloudWatch
7. Use tags for resource organization

## Boto3 Integration
The server uses boto3 for AWS operations:
- Automatic credential discovery
- Region-aware clients
- Service waiter support
- Built-in error handling
- Async operations support

## Dependencies
- fastmcp
- boto3 (AWS SDK)
- mcp
- botocore (boto3 dependency)

## Configuration Files
- `mcp_ref.json` - Reference documentation for tools
- `mcp_servers.json` - Server configuration details

## Troubleshooting
- Verify AWS credentials configuration
- Check IAM permissions for operations
- Review CloudTrail for operation history
- Enable detailed logging
- Check region settings

## Limitations
- Rate limiting from AWS APIs
- Service quotas and limits
- Regional resource availability
- Cost implications of operations

## Future Enhancements
- Lambda function management
- DynamoDB operations
- SNS/SQS integration
- VPC management
- Route53 DNS management
- Advanced monitoring and analytics
