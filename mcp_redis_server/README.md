# Redis MCP Server ⚡

## Overview
FastMCP-based server for Redis in-memory data store with support for strings, lists, sets, hashes, and advanced operations.

## Features
- **In-Memory Speed**: Ultra-fast data access
- **Multiple Data Types**: Strings, lists, sets, hashes, sorted sets
- **Expiration**: TTL support for automatic cleanup
- **Persistence**: RDB and AOF support
- **Publish-Subscribe**: Event streaming
- **Caching**: Perfect for caching layer

## Setup & Installation

### Prerequisites
- Python 3.9+
- Redis 6.0+

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
```bash
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_DB="0"
export REDIS_PASSWORD="password"  # Optional
```

### Running
```bash
python server.py
```

## Tools Available

### String Operations
- `get_value(key)` - Get string value
- `set_value(key, value, ttl)` - Set string value with optional TTL

### List Operations
- `push_to_list(key, values)` - Push to list end
- `pop_from_list(key, count)` - Pop from list start
- `get_list_range(key, start, end)` - Get list range

### Set Operations
- `add_to_set(key, values)` - Add to set
- `get_set_members(key)` - Get all set members

### Hash Operations
- `set_hash(key, data)` - Set hash fields
- `get_hash(key)` - Get entire hash

### Key Management
- `delete_key(key)` - Delete key
- `check_key_exists(key)` - Check if key exists
- `list_keys(pattern)` - List keys by pattern

### Server
- `get_redis_info()` - Get server info
- `flush_database()` - Clear database

## Usage Examples

### String Caching
```python
# Set with TTL
await client.call_tool("set_value", {
    "key": "user:123:cache",
    "value": "{'name': 'John', 'email': 'john@example.com'}",
    "ttl": 3600  # 1 hour
})

# Get value
await client.call_tool("get_value", {
    "key": "user:123:cache"
})
```

### List Operations
```python
# Queue operations
await client.call_tool("push_to_list", {
    "key": "task_queue",
    "values": ["task1", "task2", "task3"]
})

# Pop from queue
await client.call_tool("pop_from_list", {
    "key": "task_queue",
    "count": 1
})
```

### Set Operations
```python
# Tags storage
await client.call_tool("add_to_set", {
    "key": "post:123:tags",
    "values": ["python", "database", "api"]
})

# Get all tags
await client.call_tool("get_set_members", {
    "key": "post:123:tags"
})
```

### Hash Operations
```python
# Store user object
await client.call_tool("set_hash", {
    "key": "user:789",
    "data": {
        "name": "Jane",
        "email": "jane@example.com",
        "created": "2024-01-01"
    }
})

# Get user
await client.call_tool("get_hash", {
    "key": "user:789"
})
```

## Requirements
```
fastmcp>=0.1.0
mcp>=0.1.0
redis>=4.0
```

## Use Cases
- Session storage
- Caching layer
- Rate limiting
- Task queues
- Real-time leaderboards
- Pub/Sub messaging
- Distributed locks

## Best Practices
1. Use meaningful key names
2. Set appropriate TTLs
3. Implement connection pooling
4. Monitor memory usage
5. Use pipelining for bulk operations
6. Implement error handling
7. Monitor slow commands

## Performance Tips
- Use MGET for multiple keys
- Pipeline commands
- Use appropriate data structures
- Monitor memory usage
- Enable persistence when needed

## Troubleshooting
- Check Redis service running
- Verify connection parameters
- Monitor memory availability
- Review slow log for bottlenecks
