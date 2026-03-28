# AWS MCP Docs Client 📚

## Overview
A documentation and integration client for AWS services using MCP. This provides access to AWS documentation, tutorials, API references, and enables querying AWS documentation through MCP tools.

## Features
- **AWS Documentation Access**: Search and retrieve AWS docs
- **Service Integration**: Connect to AWS service documentation
- **API References**: Access API documentation
- **Code Samples**: Get code examples from AWS docs
- **Best Practices**: Access AWS best practices
- **Tutorial Discovery**: Find relevant tutorials

## Setup & Usage

### Installation
```bash
pip install fastmcp mcp httpx
```

### Configuration
```bash
export AWS_DOCS_CACHE_DIR="./aws_docs_cache"
export AWS_REGION="us-east-1"
```

### Running
```python
from aws_mcp_docs_client import AWSDocsClient

client = AWSDocsClient()
docs = client.get_service_docs("s3")
```

## Tools Available

### Documentation Search
- `search_aws_docs(query)` - Search AWS documentation
- `get_service_docs(service_name)` - Get service documentation
- `get_api_reference(service, operation)` - Get API details
- `find_code_samples(service, topic)` - Find code examples

### Service Documentation
- `get_service_overview(service)` - Service overview
- `get_pricing_info(service)` - Pricing details
- `get_quotas(service)` - Service quotas
- `get_supported_regions(service)` - Available regions

### Best Practices
- `get_security_best_practices(service)` - Security docs
- `get_performance_best_practices(service)` - Performance tips
- `get_cost_optimization(service)` - Cost tips

## Search Examples

### Service Documentation
```python
# Get S3 documentation
s3_docs = client.get_service_docs("s3")
# Returns: {
#   "name": "Amazon S3",
#   "description": "...",
#   "features": [...],
#   "pricing": {...},
#   "regions": [...]
# }
```

### API Reference
```python
# Get specific API operation
api_doc = client.get_api_reference(
    service="dynamodb",
    operation="PutItem"
)
# Returns: {
#   "operation_name": "PutItem",
#   "description": "...",
#   "parameters": {...},
#   "examples": [...]
# }
```

### Code Samples
```python
# Find code examples
samples = client.find_code_samples(
    service="lambda",
    topic="python handler"
)
# Returns: [code examples with explanations]
```

## Service Categories

### Compute
- EC2, ECS, EKS, Lambda, ElasticBeanstalk
- AppRunner, Lightsail, Batch

### Storage
- S3, EBS, EFS, Backup, DataSync
- FSx, StorageGateway

### Database
- RDS, DynamoDB, ElastiCache, Redshift
- DocumentDB, Neptune, QLDB

### Networking
- VPC, CloudFront, Route53, ELB
- Direct Connect, Transit Gateway

### Analytics
- Redshift, Athena, EMR, QuickSight
- Kinesis, Data Pipeline, Glue

### Security
- IAM, KMS, Secrets Manager, ACM
- Security Hub, GuardDuty, Macie

## Integration Patterns

### Getting Started with Service
```python
# Step 1: Get overview
overview = client.get_service_overview("s3")
print(overview["key_features"])

# Step 2: Check pricing
pricing = client.get_pricing_info("s3")
print(f"Standard storage: {pricing['storage_cost']}/GB/month")

# Step 3: Find samples
samples = client.find_code_samples("s3", "upload file")
print(samples[0]["code"])
```

### Architecture Planning
```python
# Research services for solution
services = ["EC2", "RDS", "S3", "CloudFront"]

for service in services:
    print(f"\n{service}:")
    docs = client.get_service_docs(service)
    print(f"  Use cases: {docs['use_cases']}")
    print(f"  Pricing: {docs['pricing_model']}")
    print(f"  Regions: {len(docs['supported_regions'])}")
```

## Best Practices Guide

### Security Best Practices
```python
practices = client.get_security_best_practices("s3")
# Contains:
# - Access control strategies
# - Encryption options
# - Audit logging setup
# - Compliance guidance
```

### Performance Best Practices
```python
practices = client.get_performance_best_practices("dynamodb")
# Contains:
# - Partition key design
# - Scaling strategies
# - Query optimization
# - Monitoring setup
```

### Cost Optimization
```python
tips = client.get_cost_optimization("ec2")
# Contains:
# - Instance type selection
# - Reserved instances
# - Spot instances
# - Auto-scaling strategies
```

## Caching Strategy

### Local Cache
```python
# Documentation is cached locally
# Cache structure:
# ./aws_docs_cache/
# ├── s3/
# ├── ec2/
# ├── dynamodb/
# └── ...
```

### Cache Updates
```python
# Update cache with latest docs
client.update_cache("s3")

# Or refresh all
client.refresh_all_docs()
```

## Use Cases
- Learning AWS services
- Architecture planning
- Code development
- Best practice research
- Pricing analysis
- Compliance checking
- Troubleshooting

## Performance

### Offline Access
```python
# Cached docs available offline
# - Fast local access
# - No network required
# - Regular updates recommended
```

### Search Performance
```python
# Fast search through cached docs
# Indexed for quick retrieval
# Full-text search support
```

## API Examples

### Search Operations
```python
# Search across all services
results = client.search_aws_docs("Lambda concurrency")
# Returns matching docs with relevance scores

# Search specific service
s3_results = client.search_aws_docs(
    "versioning",
    service="s3"
)
```

### Regional Information
```python
# Get services in specific region
services = client.get_services_in_region("eu-west-1")

# Get regions for service
regions = client.get_supported_regions("rds")

# Check pricing by region
pricing = client.get_pricing_info("ec2", region="us-east-1")
```

## Testing

### Unit Tests
```python
def test_service_docs():
    docs = client.get_service_docs("s3")
    assert docs["name"] == "Amazon S3"
    assert "features" in docs

def test_search():
    results = client.search_aws_docs("Lambda")
    assert len(results) > 0
```

## Dependencies
- fastmcp
- mcp
- httpx
- Beautiful Soup (for HTML parsing)

## Configuration

### Cache Settings
```python
CACHE_CONFIG = {
    "directory": "./aws_docs_cache",
    "max_age_days": 7,
    "auto_update": True,
    "compression": "gzip"
}
```

## Best Practices
1. Keep documentation cache updated
2. Use specific service searches
3. Check pricing regularly
4. Review best practices
5. Validate examples before use
6. Monitor service updates
7. Document decisions

## Troubleshooting

### Cache Issues
```python
# Reset cache
client.clear_cache()

# Rebuild cache
client.rebuild_cache()
```

### Search Not Finding Results
```python
# Try broader search
results = client.search_aws_docs("database")
# Will return multiple services
```

## Future Enhancements
- [ ] Real-time documentation updates
- [ ] CloudFormation templates
- [ ] Terraform modules
- [ ] CDK examples
- [ ] Service comparison tools
- [ ] Training recommendations
- [ ] Certification guides
