# AWS ElastiCache MCP Server 💾

## Overview
FastMCP-based server for AWS ElastiCache Redis/Memcached operations with fully managed caching service.

## Features
- **Fully Managed**: AWS-managed cache service
- **Redis & Memcached**: Support for both engines
- **High Performance**: Sub-millisecond latency
- **Auto-Failover**: High availability setup
- **Cluster Mode**: Sharding and replication
- **Encryption**: Data encryption support

## Setup & Installation

### Prerequisites
- Python 3.9+
- AWS ElastiCache cluster
- AWS credentials configured

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export ELASTICACHE_ENDPOINT="your-cluster.cache.amazonaws.com"
export ELASTICACHE_PORT="6379"
export ELASTICACHE_PASSWORD="your_password"  # Optional
```

### Running
```bash
python server.py
```

## Tools Available

### get_value
Get value from cache.

### set_value
Set value in cache.

### delete_key
Delete key from cache.

### list_keys
List keys by pattern.

### get_cache_stats
Get cache statistics.

### increment_counter
Increment counter value.

### append_to_list
Append to cache list.

### get_list
Get list from cache.

### set_hash
Set hash in cache.

### get_hash
Get hash from cache.

### flush_cache
Clear entire cache.

## Usage Examples

### Caching Data
```python
# Set with TTL
await client.call_tool("set_value", {
    "key": "user:123:profile",
    "value": "{'name': 'John', 'email': 'john@example.com'}",
    "ttl": 3600
})

# Get cached data
await client.call_tool("get_value", {
    "key": "user:123:profile"
})
```

### Counter Operations
```python
await client.call_tool("increment_counter", {
    "key": "api:requests:today",
    "increment_by": 1
})
```

### Cache Statistics
```python
await client.call_tool("get_cache_stats", {})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
redis>=4.0
```

## Use Cases
- Session caching
- Database query results
- API response caching
- Rate limiting
- Real-time leaderboards
- Shopping carts
- User preferences

## Best Practices
- Use meaningful key names
- Set appropriate TTLs
- Monitor cache hit ratio
- Use compression for large objects
- Implement cache invalidation strategy
- Monitor memory usage

## Performance Tips
- Use pipelining
- Use hashes for object storage
- Implement proper key naming
- Monitor slow commands
- Use cluster mode for scale

## Troubleshooting
- Verify cluster endpoint
- Check security group rules
- Monitor parameter group
- Review CloudWatch metrics
