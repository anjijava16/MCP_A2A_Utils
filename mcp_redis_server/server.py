"""
Redis MCP Server using FastMCP
Comprehensive in-memory data store/cache operations with 28 tools
"""

import asyncio
import redis
from redis import Redis
import json
import logging
import os
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP

logging.basicConfig(format="[%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("Redis MCP Server 💾")

# Configuration from environment
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", "6379")),
    "db": int(os.getenv("REDIS_DB", "0")),
    "password": os.getenv("REDIS_PASSWORD"),
    "decode_responses": True
}

def get_redis_client() -> Redis:
    """Get Redis client with configuration from environment."""
    try:
        client = redis.Redis(**{k: v for k, v in REDIS_CONFIG.items() if v is not None})
        client.ping()
        logger.info(f"✅ Connected to Redis: {REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/{REDIS_CONFIG['db']}")
        return client
    except Exception as e:
        logger.error(f"❌ Redis connection error: {str(e)}")
        raise

# ====================== STRING OPERATIONS (8 tools) ======================

@mcp.tool()
def redis_set_string(key: str, value: str, ttl_seconds: Optional[int] = None) -> Dict[str, Any]:
    """Set a string value with optional TTL.
    
    Args:
        key: Redis key
        value: String value
        ttl_seconds: Time-to-live in seconds
    
    Returns:
        Success status
    """
    try:
        client = get_redis_client()
        if ttl_seconds:
            client.setex(key, ttl_seconds, value)
        else:
            client.set(key, value)
        logger.info(f"➕ String set: {key}")
        return {"success": True, "message": f"String '{key}' set successfully"}
    except Exception as e:
        logger.error(f"❌ Error setting string: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_get_string(key: str) -> Dict[str, Any]:
    """Get a string value.
    
    Args:
        key: Redis key
    
    Returns:
        String value or None
    """
    try:
        client = get_redis_client()
        value = client.get(key)
        logger.info(f"🔎 String retrieved: {key}")
        return {"success": True, "value": value}
    except Exception as e:
        logger.error(f"❌ Error getting string: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_mset_strings(key_values: Dict[str, str]) -> Dict[str, Any]:
    """Set multiple string key-value pairs.
    
    Args:
        key_values: Dictionary of key-value pairs
    
    Returns:
        Success status
    """
    try:
        client = get_redis_client()
        client.mset(key_values)
        logger.info(f"➕ {len(key_values)} strings set")
        return {"success": True, "count": len(key_values)}
    except Exception as e:
        logger.error(f"❌ Error setting strings: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_mget_strings(keys: List[str]) -> Dict[str, Any]:
    """Get multiple string values.
    
    Args:
        keys: List of Redis keys
    
    Returns:
        Dictionary of key-value pairs
    """
    try:
        client = get_redis_client()
        values = client.mget(keys)
        result = {k: v for k, v in zip(keys, values)}
        logger.info(f"🔎 {len(keys)} strings retrieved")
        return {"success": True, "values": result, "count": len(result)}
    except Exception as e:
        logger.error(f"❌ Error getting strings: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_increment(key: str, amount: int = 1) -> Dict[str, Any]:
    """Increment a numeric string value.
    
    Args:
        key: Redis key
        amount: Amount to increment
    
    Returns:
        New value
    """
    try:
        client = get_redis_client()
        new_value = client.incrby(key, amount)
        logger.info(f"➕ Key incremented: {key}")
        return {"success": True, "value": new_value}
    except Exception as e:
        logger.error(f"❌ Error incrementing: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_append_string(key: str, value: str) -> Dict[str, Any]:
    """Append to a string value.
    
    Args:
        key: Redis key
        value: Value to append
    
    Returns:
        New length
    """
    try:
        client = get_redis_client()
        length = client.append(key, value)
        logger.info(f"✏️ String appended: {key}")
        return {"success": True, "length": length}
    except Exception as e:
        logger.error(f"❌ Error appending: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_get_string_range(key: str, start: int = 0, end: int = -1) -> Dict[str, Any]:
    """Get substring from a string value.
    
    Args:
        key: Redis key
        start: Start index
        end: End index
    
    Returns:
        Substring
    """
    try:
        client = get_redis_client()
        value = client.getrange(key, start, end)
        logger.info(f"🔎 String range retrieved: {key}")
        return {"success": True, "value": value}
    except Exception as e:
        logger.error(f"❌ Error getting range: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== KEY MANAGEMENT (6 tools) ======================

@mcp.tool()
def redis_delete_keys(keys: List[str]) -> Dict[str, Any]:
    """Delete one or more keys.
    
    Args:
        keys: List of keys to delete
    
    Returns:
        Number of keys deleted
    """
    try:
        client = get_redis_client()
        count = client.delete(*keys)
        logger.info(f"🗑️ {count} keys deleted")
        return {"success": True, "deleted": count}
    except Exception as e:
        logger.error(f"❌ Error deleting: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_keys_pattern(pattern: str = "*") -> Dict[str, Any]:
    """List keys matching a pattern.
    
    Args:
        pattern: Key pattern (e.g., "user:*")
    
    Returns:
        List of matching keys
    """
    try:
        client = get_redis_client()
        keys = client.keys(pattern)
        logger.info(f"📋 Found {len(keys)} keys matching {pattern}")
        return {"success": True, "keys": list(keys), "count": len(keys)}
    except Exception as e:
        logger.error(f"❌ Error listing keys: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_exists_keys(keys: List[str]) -> Dict[str, Any]:
    """Check if keys exist.
    
    Args:
        keys: List of keys to check
    
    Returns:
        Count of existing keys
    """
    try:
        client = get_redis_client()
        count = client.exists(*keys)
        logger.info(f"🔍 {count}/{len(keys)} keys exist")
        return {"success": True, "exists": count, "total": len(keys)}
    except Exception as e:
        logger.error(f"❌ Error checking existence: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_set_ttl(key: str, ttl_seconds: int) -> Dict[str, Any]:
    """Set Time-To-Live for a key.
    
    Args:
        key: Redis key
        ttl_seconds: TTL in seconds
    
    Returns:
        Success status
    """
    try:
        client = get_redis_client()
        result = client.expire(key, ttl_seconds)
        logger.info(f"⏱️ TTL set for key: {key}")
        return {"success": True, "message": f"TTL set to {ttl_seconds}s", "set": result}
    except Exception as e:
        logger.error(f"❌ Error setting TTL: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_get_ttl(key: str) -> Dict[str, Any]:
    """Get remaining TTL for a key.
    
    Args:
        key: Redis key
    
    Returns:
        TTL in seconds or -1 (no expiry) or -2 (key doesn't exist)
    """
    try:
        client = get_redis_client()
        ttl = client.ttl(key)
        logger.info(f"⏱️ TTL retrieved for key: {key}")
        return {"success": True, "ttl_seconds": ttl}
    except Exception as e:
        logger.error(f"❌ Error getting TTL: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_rename_key(old_key: str, new_key: str) -> Dict[str, Any]:
    """Rename a key.
    
    Args:
        old_key: Current key name
        new_key: New key name
    
    Returns:
        Success status
    """
    try:
        client = get_redis_client()
        client.rename(old_key, new_key)
        logger.info(f"✏️ Key renamed: {old_key} → {new_key}")
        return {"success": True, "message": f"Key renamed to '{new_key}'"}
    except Exception as e:
        logger.error(f"❌ Error renaming: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== LIST OPERATIONS (5 tools) ======================

@mcp.tool()
def redis_list_push(key: str, values: List[str], position: str = "right") -> Dict[str, Any]:
    """Push values to a list.
    
    Args:
        key: Redis key
        values: Values to push
        position: "left" or "right"
    
    Returns:
        New list length
    """
    try:
        client = get_redis_client()
        if position.lower() == "left":
            length = client.lpush(key, *values)
        else:
            length = client.rpush(key, *values)
        logger.info(f"➕ {len(values)} values pushed to list: {key}")
        return {"success": True, "length": length}
    except Exception as e:
        logger.error(f"❌ Error pushing to list: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_list_pop(key: str, count: int = 1, position: str = "right") -> Dict[str, Any]:
    """Pop values from a list.
    
    Args:
        key: Redis key
        count: Number of values to pop
        position: "left" or "right"
    
    Returns:
        Popped values
    """
    try:
        client = get_redis_client()
        if position.lower() == "left":
            values = [client.lpop(key) for _ in range(count)]
        else:
            values = [client.rpop(key) for _ in range(count)]
        values = [v for v in values if v is not None]
        logger.info(f"🔎 {len(values)} values popped from list: {key}")
        return {"success": True, "values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ Error popping from list: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_list_range(key: str, start: int = 0, end: int = -1) -> Dict[str, Any]:
    """Get range from a list.
    
    Args:
        key: Redis key
        start: Start index
        end: End index
    
    Returns:
        List elements
    """
    try:
        client = get_redis_client()
        values = client.lrange(key, start, end)
        logger.info(f"🔎 Retrieved {len(values)} elements from list: {key}")
        return {"success": True, "values": values, "count": len(values)}
    except Exception as e:
        logger.error(f"❌ Error getting list range: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_list_length(key: str) -> Dict[str, Any]:
    """Get list length.
    
    Args:
        key: Redis key
    
    Returns:
        List length
    """
    try:
        client = get_redis_client()
        length = client.llen(key)
        logger.info(f"🔢 List length retrieved: {key}")
        return {"success": True, "length": length}
    except Exception as e:
        logger.error(f"❌ Error getting list length: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_list_trim(key: str, start: int = 0, end: int = -1) -> Dict[str, Any]:
    """Trim a list to specified range.
    
    Args:
        key: Redis key
        start: Start index
        end: End index
    
    Returns:
        Success status
    """
    try:
        client = get_redis_client()
        client.ltrim(key, start, end)
        logger.info(f"✂️ List trimmed: {key}")
        return {"success": True, "message": "List trimmed"}
    except Exception as e:
        logger.error(f"❌ Error trimming list: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SET OPERATIONS (4 tools) ======================

@mcp.tool()
def redis_set_add(key: str, members: List[str]) -> Dict[str, Any]:
    """Add members to a set.
    
    Args:
        key: Redis key
        members: Members to add
    
    Returns:
        Number of members added
    """
    try:
        client = get_redis_client()
        count = client.sadd(key, *members)
        logger.info(f"➕ {count} members added to set: {key}")
        return {"success": True, "added": count}
    except Exception as e:
        logger.error(f"❌ Error adding to set: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_set_members(key: str) -> Dict[str, Any]:
    """Get all set members.
    
    Args:
        key: Redis key
    
    Returns:
        Set members
    """
    try:
        client = get_redis_client()
        members = client.smembers(key)
        logger.info(f"🔎 Retrieved {len(members)} members from set: {key}")
        return {"success": True, "members": list(members), "count": len(members)}
    except Exception as e:
        logger.error(f"❌ Error getting set members: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_set_remove(key: str, members: List[str]) -> Dict[str, Any]:
    """Remove members from a set.
    
    Args:
        key: Redis key
        members: Members to remove
    
    Returns:
        Number of members removed
    """
    try:
        client = get_redis_client()
        count = client.srem(key, *members)
        logger.info(f"🗑️ {count} members removed from set: {key}")
        return {"success": True, "removed": count}
    except Exception as e:
        logger.error(f"❌ Error removing from set: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_set_cardinality(key: str) -> Dict[str, Any]:
    """Get set cardinality (member count).
    
    Args:
        key: Redis key
    
    Returns:
        Cardinality
    """
    try:
        client = get_redis_client()
        cardinality = client.scard(key)
        logger.info(f"🔢 Set cardinality retrieved: {key}")
        return {"success": True, "cardinality": cardinality}
    except Exception as e:
        logger.error(f"❌ Error getting cardinality: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== HASH OPERATIONS (3 tools) ======================

@mcp.tool()
def redis_hash_set(key: str, field_values: Dict[str, str]) -> Dict[str, Any]:
    """Set hash fields.
    
    Args:
        key: Redis key
        field_values: Dictionary of field-value pairs
    
    Returns:
        Number of fields added
    """
    try:
        client = get_redis_client()
        count = client.hset(key, mapping=field_values)
        logger.info(f"➕ {count} fields set in hash: {key}")
        return {"success": True, "set": count}
    except Exception as e:
        logger.error(f"❌ Error setting hash: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_hash_get(key: str, field: Optional[str] = None) -> Dict[str, Any]:
    """Get hash field(s).
    
    Args:
        key: Redis key
        field: Specific field (optional, get all if not specified)
    
    Returns:
        Hash data
    """
    try:
        client = get_redis_client()
        if field:
            value = client.hget(key, field)
            logger.info(f"🔎 Hash field retrieved: {key}.{field}")
            return {"success": True, "value": value}
        else:
            data = client.hgetall(key)
            logger.info(f"🔎 Hash retrieved: {key}")
            return {"success": True, "data": data, "count": len(data)}
    except Exception as e:
        logger.error(f"❌ Error getting hash: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_hash_delete(key: str, fields: List[str]) -> Dict[str, Any]:
    """Delete hash fields.
    
    Args:
        key: Redis key
        fields: Fields to delete
    
    Returns:
        Number of fields deleted
    """
    try:
        client = get_redis_client()
        count = client.hdel(key, *fields)
        logger.info(f"🗑️ {count} fields deleted from hash: {key}")
        return {"success": True, "deleted": count}
    except Exception as e:
        logger.error(f"❌ Error deleting hash fields: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== SERVER ADMINISTRATION (2 tools) ======================

@mcp.tool()
def redis_server_info() -> Dict[str, Any]:
    """Get Redis server information.
    
    Returns:
        Server info
    """
    try:
        client = get_redis_client()
        info = client.info()
        logger.info(f"📊 Server info retrieved")
        return {
            "success": True,
            "info": {
                "version": info.get("redis_version"),
                "uptime_seconds": info.get("uptime_in_seconds"),
                "connected_clients": info.get("connected_clients"),
                "used_memory_mb": round(info.get("used_memory", 0) / (1024 * 1024), 2),
                "total_commands": info.get("total_commands_processed"),
                "keys": info.get("db0", {}).get("keys", 0) if "db0" in info else 0
            }
        }
    except Exception as e:
        logger.error(f"❌ Error getting info: {str(e)}")
        return {"success": False, "error": str(e)}

@mcp.tool()
def redis_flush_database(flush_type: str = "current") -> Dict[str, Any]:
    """Flush Redis database(s).
    
    Args:
        flush_type: "current" for current DB, "all" for all databases
    
    Returns:
        Success status
    """
    try:
        client = get_redis_client()
        if flush_type.lower() == "all":
            client.flushall()
            logger.info(f"🗑️ All databases flushed")
            return {"success": True, "message": "All databases flushed"}
        else:
            client.flushdb()
            logger.info(f"🗑️ Current database flushed")
            return {"success": True, "message": "Current database flushed"}
    except Exception as e:
        logger.error(f"❌ Error flushing: {str(e)}")
        return {"success": False, "error": str(e)}

# ====================== PROMPTS ======================

DBA_PROMPT = """You are a Redis Database Administrator. Your role is to:
- Manage Redis keys and data structures
- Optimize memory usage
- Monitor server health and performance
- Set up TTLs and expiration policies
- Manage multiple databases

Use these tools for DBA tasks:
- redis_keys_pattern, redis_exists_keys for exploration
- redis_set_ttl, redis_get_ttl for expiration management
- redis_rename_key  for key management
- redis_server_info for monitoring
- redis_flush_database for maintenance
"""

DEVELOPER_PROMPT = """You are a Redis Developer. Your role is to:
- Implement caching strategies
- Store and retrieve application data
- Manage sessions and user data
- Use appropriate data structures

Use these tools for development:
- redis_set_string, redis_get_string for basic caching
- redis_list_push, redis_list_pop for queue operations
- redis_set_add, redis_set_members for tagging
- redis_hash_set, redis_hash_get for structured data
- redis_increment for counters
"""

ANALYTICS_PROMPT = """You are a Redis Analytics Engineer. Your role is to:
- Query cached analytics data
- Analyze key patterns and usage
- Monitor real-time metrics
- Track set and list operations

Use these tools for analytics:
- redis_keys_pattern for discovering metrics
- redis_server_info for performance metrics
- redis_list_length, redis_set_cardinality for size metrics
- redis_get_ttl for expiration analysis
"""

mcp.add_prompt("DBA Operations", DBA_PROMPT)
mcp.add_prompt("Developer", DEVELOPER_PROMPT)
mcp.add_prompt("Analytics", ANALYTICS_PROMPT)

# ====================== MAIN ======================

async def main():
    logger.info("🚀 Starting Redis MCP Server...")
    
    await mcp.run_async(
        transport="sse",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7089"))
    )

if __name__ == "__main__":
    asyncio.run(main())
